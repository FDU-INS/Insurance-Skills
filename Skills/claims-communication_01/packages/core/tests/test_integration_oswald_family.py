"""Integration tests: Oswald Family cross-product scenario.

This module tests end-to-end generation across all HealthSim products
using a realistic multi-member family scenario.

The Oswald Family:
- Mark Oswald (65, Medicare, Type 2 diabetes)
- Sarah Oswald (63, Commercial, healthy)
- Michael Oswald (32, Commercial, healthy)
"""

import pytest
from datetime import date, timedelta

from healthsim.generation import (
    # Profile
    ProfileExecutor,
    ProfileSpecification,
    # Journey
    JourneyEngine,
    JourneySpecification,
    Timeline,
    create_simple_journey,
    get_journey_template,
    # Triggers
    CrossProductCoordinator,
    LinkedEntity,
    # Handlers
    register_all_handlers,
)


# =============================================================================
# Family Member Profiles
# =============================================================================

MARK_OSWALD_PROFILE = {
    "generation": {
        "count": 1,
        "seed": 19590815,  # Based on birthdate
        "products": ["patientsim", "membersim", "rxmembersim"]
    },
    "demographics": {
        "first_name": "Mark",
        "last_name": "Oswald",
        "gender": "M",
        "birth_date": "1959-08-15",
        "age": 65,
        "address": {
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        }
    },
    "clinical": {
        "conditions": [
            {"code": "E11.9", "description": "Type 2 diabetes mellitus", "onset_date": "2020-01-15"},
            {"code": "I10", "description": "Essential hypertension", "onset_date": "2015-03-10"},
            {"code": "E78.5", "description": "Hyperlipidemia", "onset_date": "2018-06-20"}
        ],
        "medications": [
            {"rxnorm": "860975", "name": "Metformin 500mg", "start_date": "2020-01-20"},
            {"rxnorm": "197884", "name": "Lisinopril 10mg", "start_date": "2015-03-15"},
            {"rxnorm": "617311", "name": "Atorvastatin 20mg", "start_date": "2018-06-25"}
        ],
        "labs": {
            "a1c": 7.2,
            "ldl": 95,
            "egfr": 72
        }
    },
    "coverage": {
        "plan_type": "Medicare Advantage",
        "plan_id": "MA-GOLD-001",
        "effective_date": "2024-01-01",
        "group_id": "GRP-OSWALD"
    }
}

SARAH_OSWALD_PROFILE = {
    "generation": {
        "count": 1,
        "seed": 19610422,
        "products": ["patientsim", "membersim"]
    },
    "demographics": {
        "first_name": "Sarah",
        "last_name": "Oswald",
        "gender": "F",
        "birth_date": "1961-04-22",
        "age": 63,
        "address": {
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        }
    },
    "clinical": {
        "conditions": [],
        "medications": [],
        "labs": {}
    },
    "coverage": {
        "plan_type": "Commercial PPO",
        "plan_id": "COM-PPO-001",
        "effective_date": "2024-01-01",
        "group_id": "GRP-EMPLOYER-ABC"
    }
}


# =============================================================================
# Test Class
# =============================================================================

class TestOswaldFamilyIntegration:
    """Integration tests for Oswald Family scenario."""
    
    @pytest.fixture
    def coordinator(self):
        """Create a coordinator with all handlers registered."""
        coord = CrossProductCoordinator()
        
        # Create engines for each product
        engines = {
            "patientsim": JourneyEngine(seed=42),
            "membersim": JourneyEngine(seed=42),
            "rxmembersim": JourneyEngine(seed=42),
        }
        
        # Register all handlers with each engine
        for product, engine in engines.items():
            register_all_handlers(engine, seed=42)
            coord.register_product_engine(product, engine)
        
        return coord, engines
    
    def test_mark_profile_generation(self):
        """Test generating Mark's profile."""
        from healthsim.generation import ProfileSpecification
        
        # Create simplified profile spec for testing
        # Use normal with tight bounds for deterministic-like results
        spec = ProfileSpecification(
            id="mark-profile",
            name="Mark Profile",
            generation={"count": 1, "seed": 19590815},
            demographics={
                "age": {"type": "normal", "mean": 65, "std_dev": 0.1, "min": 65, "max": 65},
                "gender": {"type": "categorical", "weights": {"M": 1.0}}
            }
        )
        
        executor = ProfileExecutor(spec, seed=19590815)
        result = executor.execute()
        
        assert len(result.entities) == 1
        entity = result.entities[0]
        assert entity.age == 65
        assert entity.gender == "M"
    
    def test_mark_diabetic_journey(self, coordinator):
        """Test Mark's diabetic care journey."""
        coord, engines = coordinator
        
        # Create linked entity for Mark
        mark = coord.create_linked_entity("OSWALD-MARK", {
            "patient_id": "P-MARK-001",
            "member_id": "M-MARK-001",
            "rx_member_id": "RX-MARK-001"
        })
        
        # Create diabetic journey
        journey = create_simple_journey(
            "mark-diabetes-care",
            "Mark's Diabetes Care",
            events=[
                {"event_id": "dx", "name": "Diabetes Diagnosis", "event_type": "diagnosis",
                 "product": "patientsim", "delay": {"days": 0},
                 "parameters": {"icd10": "E11.9", "description": "Type 2 diabetes"}},
                {"event_id": "a1c_order", "name": "Initial A1C", "event_type": "lab_order",
                 "product": "patientsim", "delay": {"days": 3}, "depends_on": "dx",
                 "parameters": {"loinc": "4548-4"}},
                {"event_id": "metformin", "name": "Start Metformin", "event_type": "medication_order",
                 "product": "patientsim", "delay": {"days": 5}, "depends_on": "dx",
                 "parameters": {"rxnorm": "860975", "drug_name": "Metformin 500mg"}},
                {"event_id": "enrollment", "name": "Plan Enrollment", "event_type": "new_enrollment",
                 "product": "membersim", "delay": {"days": 0},
                 "parameters": {"plan_type": "MA"}},
            ],
            products=["patientsim", "membersim"]
        )
        
        # Create timeline
        patient_engine = engines["patientsim"]
        mark_entity = {"patient_id": "P-MARK-001", "member_id": "M-MARK-001", "age": 65}
        timeline = patient_engine.create_timeline(
            mark_entity, "patient", journey, date(2025, 1, 1)
        )
        coord.add_timeline(mark, "patientsim", timeline)
        
        # Execute events
        results = patient_engine.execute_timeline(
            timeline, mark_entity, up_to_date=date(2025, 1, 15)
        )
        
        # Verify all events executed
        assert len(results) == 4
        assert all(r["status"] == "executed" for r in results)
        
        # Verify event sequence
        event_types = [r["event_type"] for r in results]
        assert "diagnosis" in event_types
        assert "lab_order" in event_types
        assert "medication_order" in event_types
        assert "new_enrollment" in event_types
    
    def test_mark_claims_generation(self, coordinator):
        """Test that Mark's clinical events generate claims."""
        coord, engines = coordinator
        
        mark = coord.create_linked_entity("OSWALD-MARK", {
            "patient_id": "P-MARK-001",
            "member_id": "M-MARK-001"
        })
        
        # Journey with clinical events that should trigger claims
        journey = create_simple_journey(
            "mark-visit",
            "Mark Office Visit",
            events=[
                {"event_id": "visit", "name": "Office Visit", "event_type": "encounter",
                 "product": "patientsim", "delay": {"days": 0}},
                {"event_id": "claim", "name": "Office Visit Claim", "event_type": "claim_professional",
                 "product": "membersim", "delay": {"days": 3}, "depends_on": "visit"},
            ],
            products=["patientsim", "membersim"]
        )
        
        engine = engines["patientsim"]
        mark_entity = {"patient_id": "P-MARK-001", "member_id": "M-MARK-001"}
        timeline = engine.create_timeline(mark_entity, "patient", journey, date(2025, 1, 1))
        
        results = engine.execute_timeline(timeline, mark_entity, up_to_date=date(2025, 1, 10))
        
        assert len(results) == 2
        
        # Check claim has proper structure
        claim_result = next(r for r in results if r["event_type"] == "claim_professional")
        assert claim_result["status"] == "executed"
        assert "outputs" in claim_result
    
    def test_multi_member_generation(self, coordinator):
        """Test generating multiple family members."""
        coord, engines = coordinator
        
        # Create both Mark and Sarah
        mark = coord.create_linked_entity("OSWALD-MARK", {
            "patient_id": "P-MARK-001",
            "member_id": "M-MARK-001"
        })
        
        sarah = coord.create_linked_entity("OSWALD-SARAH", {
            "patient_id": "P-SARAH-001",
            "member_id": "M-SARAH-001"
        })
        
        # Mark's journey (diabetic)
        mark_journey = create_simple_journey(
            "mark-care", "Mark Care",
            events=[
                {"event_id": "dx", "name": "Diagnosis", "event_type": "diagnosis",
                 "product": "patientsim", "delay": {"days": 0},
                 "parameters": {"icd10": "E11.9"}},
            ],
            products=["patientsim"]
        )
        
        # Sarah's journey (wellness)
        sarah_journey = create_simple_journey(
            "sarah-wellness", "Sarah Wellness",
            events=[
                {"event_id": "awv", "name": "Annual Wellness", "event_type": "encounter",
                 "product": "patientsim", "delay": {"days": 0}},
            ],
            products=["patientsim"]
        )
        
        engine = engines["patientsim"]
        
        # Create timelines
        mark_timeline = engine.create_timeline(
            {"patient_id": "P-MARK-001"}, "patient", mark_journey, date(2025, 1, 1)
        )
        sarah_timeline = engine.create_timeline(
            {"patient_id": "P-SARAH-001"}, "patient", sarah_journey, date(2025, 1, 1)
        )
        
        coord.add_timeline(mark, "patientsim", mark_timeline)
        coord.add_timeline(sarah, "patientsim", sarah_timeline)
        
        # Execute both
        mark_results = engine.execute_timeline(
            mark_timeline, {"patient_id": "P-MARK-001"}, date(2025, 1, 31)
        )
        sarah_results = engine.execute_timeline(
            sarah_timeline, {"patient_id": "P-SARAH-001"}, date(2025, 1, 31)
        )
        
        assert len(mark_results) == 1
        assert len(sarah_results) == 1
        assert mark_results[0]["event_type"] == "diagnosis"
        assert sarah_results[0]["event_type"] == "encounter"
    
    def test_journey_template_usage(self, coordinator):
        """Test using built-in journey template."""
        coord, engines = coordinator
        
        # Get diabetic first year template
        journey = get_journey_template("diabetic-first-year")
        
        assert journey.journey_id == "diabetic-first-year"
        assert len(journey.events) > 0
        
        # Create timeline
        engine = engines["patientsim"]
        mark_entity = {"patient_id": "P-MARK-001", "age": 65}
        timeline = engine.create_timeline(
            mark_entity, "patient", journey, date(2025, 1, 1)
        )
        
        # Should have multiple events
        assert len(timeline.events) >= 4  # At minimum: dx, a1c, metformin, followup
    
    def test_reproducibility(self, coordinator):
        """Test that same seed produces same results."""
        coord, engines = coordinator
        
        journey = create_simple_journey(
            "test", "Test",
            events=[
                {"event_id": "e1", "name": "Event 1", "event_type": "encounter",
                 "product": "patientsim", "delay": {"days": 10, "days_min": 5, "days_max": 15, "distribution": "uniform"}},
            ]
        )
        
        # First run
        engine1 = JourneyEngine(seed=12345)
        register_all_handlers(engine1, seed=12345)
        timeline1 = engine1.create_timeline(
            {"patient_id": "P001"}, "patient", journey, date(2025, 1, 1)
        )
        
        # Second run with same seed
        engine2 = JourneyEngine(seed=12345)
        register_all_handlers(engine2, seed=12345)
        timeline2 = engine2.create_timeline(
            {"patient_id": "P001"}, "patient", journey, date(2025, 1, 1)
        )
        
        # Same dates
        assert timeline1.events[0].scheduled_date == timeline2.events[0].scheduled_date
    
    def test_cross_product_coordination(self, coordinator):
        """Test cross-product event coordination."""
        coord, engines = coordinator
        
        mark = coord.create_linked_entity("OSWALD-MARK", {
            "patient_id": "P-MARK-001",
            "member_id": "M-MARK-001",
            "rx_member_id": "RX-MARK-001"
        })
        
        # Verify linked entity structure
        assert mark.patient_id == "P-MARK-001"
        assert mark.member_id == "M-MARK-001"
        assert mark.rx_member_id == "RX-MARK-001"
        
        # Verify all engines registered
        assert "patientsim" in coord._product_engines
        assert "membersim" in coord._product_engines
        assert "rxmembersim" in coord._product_engines


class TestPerformanceBatch:
    """Performance tests for batch generation."""
    
    def test_batch_profile_generation(self):
        """Test generating a batch of profiles."""
        from healthsim.generation import ProfileSpecification
        
        spec = ProfileSpecification(
            id="batch-profile",
            name="Batch Profile",
            generation={"count": 100, "seed": 42},
            demographics={
                "age": {"type": "normal", "mean": 65, "std_dev": 10, "min": 50, "max": 90},
                "gender": {"type": "categorical", "weights": {"M": 0.48, "F": 0.52}}
            }
        )
        
        executor = ProfileExecutor(spec, seed=42)
        result = executor.execute()
        
        assert len(result.entities) == 100
        
        # Check distribution roughly matches
        ages = [e.age for e in result.entities]
        avg_age = sum(ages) / len(ages)
        assert 60 <= avg_age <= 70  # Should be around 65
        
        genders = [e.gender for e in result.entities]
        male_pct = genders.count("M") / len(genders)
        assert 0.35 <= male_pct <= 0.65  # Roughly balanced
    
    def test_batch_journey_generation(self):
        """Test generating journeys for a batch of patients."""
        engine = JourneyEngine(seed=42)
        register_all_handlers(engine, seed=42)
        
        journey = create_simple_journey(
            "batch-test", "Batch Test",
            events=[
                {"event_id": "e1", "name": "Visit", "event_type": "encounter",
                 "product": "patientsim", "delay": {"days": 0}},
            ]
        )
        
        # Generate 50 timelines
        timelines = []
        for i in range(50):
            patient = {"patient_id": f"P{i:03d}"}
            timeline = engine.create_timeline(patient, "patient", journey, date(2025, 1, 1))
            timelines.append(timeline)
        
        assert len(timelines) == 50
        
        # All should have same number of events
        assert all(len(t.events) == 1 for t in timelines)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
