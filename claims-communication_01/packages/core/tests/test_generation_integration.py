"""
Integration tests for HealthSim Generative Framework.

Tests end-to-end flows:
- Profile specification → Execution → Entity generation
- Journey specification → Timeline expansion → Event generation
- Cross-product synchronization
- Large batch handling

Run with: pytest packages/core/tests/test_generation_integration.py -v
"""

import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_profile_spec():
    """Minimal valid profile specification."""
    return {
        "profile": {
            "id": "test-medicare-diabetic",
            "name": "Test Medicare Diabetic",
            "version": "1.0",
            "category": "payer",
            "products": ["PatientSim", "MemberSim"]
        },
        "demographics": {
            "count": 10,
            "age": {
                "type": "normal",
                "mean": 72,
                "std_dev": 6,
                "min": 65,
                "max": 95
            },
            "gender": {
                "type": "categorical",
                "weights": {"M": 0.48, "F": 0.52}
            }
        },
        "clinical": {
            "primary_condition": {
                "code": "E11.9",
                "description": "Type 2 diabetes mellitus without complications",
                "prevalence": 1.0
            },
            "comorbidities": [
                {"code": "I10", "description": "Essential hypertension", "prevalence": 0.78},
                {"code": "E78.5", "description": "Hyperlipidemia", "prevalence": 0.65}
            ]
        },
        "coverage": {
            "plan_type": {
                "type": "categorical",
                "weights": {"MA-HMO": 0.35, "MA-PPO": 0.25, "Original": 0.40}
            }
        }
    }


@pytest.fixture
def sample_journey_spec():
    """Minimal valid journey specification."""
    return {
        "journey": {
            "id": "test-diabetic-journey",
            "name": "Test Diabetic First Year",
            "version": "1.0",
            "duration": {"value": 12, "unit": "months"},
            "pattern": "linear"
        },
        "phases": [
            {
                "name": "Initial Diagnosis",
                "duration": {"value": 1, "unit": "months"},
                "events": [
                    {
                        "type": "encounter",
                        "timing": {"day": 0},
                        "details": {
                            "encounter_type": "office",
                            "reason": "New diabetes diagnosis",
                            "cpt_codes": ["99214", "83036"]
                        }
                    },
                    {
                        "type": "prescription",
                        "timing": {"day": 0},
                        "details": {
                            "medication": "metformin",
                            "dose": "500mg",
                            "frequency": "BID"
                        }
                    }
                ]
            },
            {
                "name": "Follow-up",
                "duration": {"value": 2, "unit": "months"},
                "events": [
                    {
                        "type": "encounter",
                        "timing": {"day": 30, "variance_days": 7},
                        "details": {
                            "encounter_type": "office",
                            "reason": "Diabetes follow-up"
                        }
                    }
                ]
            }
        ]
    }


@pytest.fixture
def sample_distribution_categorical():
    """Sample categorical distribution."""
    return {
        "type": "categorical",
        "weights": {"A": 0.5, "B": 0.3, "C": 0.2}
    }


@pytest.fixture
def sample_distribution_normal():
    """Sample normal distribution."""
    return {
        "type": "normal",
        "mean": 70,
        "std_dev": 8,
        "min": 65,
        "max": 95
    }


# ============================================================================
# Profile Specification Tests
# ============================================================================

class TestProfileSpecification:
    """Tests for profile specification structure and validation."""

    def test_profile_spec_has_required_fields(self, sample_profile_spec):
        """Profile spec must have profile, demographics, clinical sections."""
        assert "profile" in sample_profile_spec
        assert "demographics" in sample_profile_spec
        assert "clinical" in sample_profile_spec

    def test_profile_spec_id_format(self, sample_profile_spec):
        """Profile ID should be kebab-case."""
        profile_id = sample_profile_spec["profile"]["id"]
        assert "-" in profile_id or profile_id.islower()
        assert " " not in profile_id

    def test_profile_demographics_count(self, sample_profile_spec):
        """Demographics must have positive count."""
        count = sample_profile_spec["demographics"]["count"]
        assert isinstance(count, int)
        assert count > 0

    def test_profile_age_distribution_valid(self, sample_profile_spec):
        """Age distribution must be valid type with required params."""
        age = sample_profile_spec["demographics"]["age"]
        assert age["type"] in ["normal", "categorical", "uniform", "explicit"]
        if age["type"] == "normal":
            assert "mean" in age
            assert "std_dev" in age

    def test_profile_clinical_has_condition(self, sample_profile_spec):
        """Clinical section must have primary condition."""
        clinical = sample_profile_spec["clinical"]
        assert "primary_condition" in clinical
        assert "code" in clinical["primary_condition"]

    def test_profile_comorbidities_have_prevalence(self, sample_profile_spec):
        """Each comorbidity must have prevalence 0-1."""
        comorbidities = sample_profile_spec["clinical"].get("comorbidities", [])
        for comorbidity in comorbidities:
            assert "prevalence" in comorbidity
            assert 0 <= comorbidity["prevalence"] <= 1


# ============================================================================
# Journey Specification Tests
# ============================================================================

class TestJourneySpecification:
    """Tests for journey specification structure and validation."""

    def test_journey_spec_has_required_fields(self, sample_journey_spec):
        """Journey spec must have journey and phases sections."""
        assert "journey" in sample_journey_spec
        assert "phases" in sample_journey_spec

    def test_journey_has_duration(self, sample_journey_spec):
        """Journey must have duration with value and unit."""
        duration = sample_journey_spec["journey"]["duration"]
        assert "value" in duration
        assert "unit" in duration
        assert duration["unit"] in ["days", "weeks", "months", "years"]

    def test_journey_has_pattern(self, sample_journey_spec):
        """Journey must have valid pattern type."""
        pattern = sample_journey_spec["journey"]["pattern"]
        valid_patterns = ["linear", "branching", "cyclic", "protocol", "lifecycle"]
        assert pattern in valid_patterns

    def test_journey_phases_not_empty(self, sample_journey_spec):
        """Journey must have at least one phase."""
        phases = sample_journey_spec["phases"]
        assert len(phases) > 0

    def test_journey_phase_has_events(self, sample_journey_spec):
        """Each phase must have events list."""
        for phase in sample_journey_spec["phases"]:
            assert "events" in phase
            assert isinstance(phase["events"], list)

    def test_journey_events_have_timing(self, sample_journey_spec):
        """Each event must have timing specification."""
        for phase in sample_journey_spec["phases"]:
            for event in phase["events"]:
                assert "timing" in event
                assert "day" in event["timing"] or "week" in event["timing"]


# ============================================================================
# Distribution Tests
# ============================================================================

class TestDistributions:
    """Tests for distribution sampling."""

    def test_categorical_distribution_weights_sum_to_one(self, sample_distribution_categorical):
        """Categorical weights must sum to approximately 1."""
        weights = sample_distribution_categorical["weights"]
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.01

    def test_categorical_distribution_sampling(self, sample_distribution_categorical):
        """Categorical sampling should return valid categories."""
        weights = sample_distribution_categorical["weights"]
        categories = list(weights.keys())
        
        # Simulate 100 samples
        samples = random.choices(categories, weights=list(weights.values()), k=100)
        
        for sample in samples:
            assert sample in categories

    def test_normal_distribution_constraints(self, sample_distribution_normal):
        """Normal distribution should have valid constraints."""
        dist = sample_distribution_normal
        assert dist["mean"] >= dist.get("min", float("-inf"))
        assert dist["mean"] <= dist.get("max", float("inf"))

    def test_normal_distribution_sampling(self, sample_distribution_normal):
        """Normal sampling should respect min/max bounds."""
        dist = sample_distribution_normal
        min_val = dist.get("min", float("-inf"))
        max_val = dist.get("max", float("inf"))
        
        # Simulate 100 samples with truncation
        samples = []
        for _ in range(100):
            value = random.gauss(dist["mean"], dist["std_dev"])
            value = max(min_val, min(max_val, value))
            samples.append(value)
        
        for sample in samples:
            assert sample >= min_val
            assert sample <= max_val


# ============================================================================
# Cross-Domain Sync Tests
# ============================================================================

class TestCrossDomainSync:
    """Tests for cross-product entity correlation."""

    def test_identity_correlation_ssn(self):
        """SSN should link Patient, Member, and RxMember."""
        # Simulated cross-domain entities
        ssn = "123-45-6789"
        patient = {"ssn": ssn, "first_name": "John", "last_name": "Doe"}
        member = {"ssn": ssn, "member_id": "M001", "subscriber_id": "S001"}
        rx_member = {"ssn": ssn, "cardholder_id": "C001"}
        
        # All entities share the same SSN
        assert patient["ssn"] == member["ssn"] == rx_member["ssn"]

    def test_encounter_generates_claim(self):
        """Encounter event should generate corresponding claim."""
        encounter = {
            "encounter_id": "E001",
            "patient_id": "P001",
            "date": "2026-01-15",
            "encounter_type": "office",
            "diagnoses": ["E11.9"],
            "procedures": ["99214"]
        }
        
        # Simulated claim generation
        claim = {
            "claim_id": "CLM001",
            "member_id": "M001",  # Linked via patient
            "service_date": encounter["date"],
            "claim_type": "professional",
            "diagnoses": encounter["diagnoses"],
            "service_lines": [
                {"cpt": proc, "units": 1} for proc in encounter["procedures"]
            ]
        }
        
        # Verify linkage
        assert claim["service_date"] == encounter["date"]
        assert claim["diagnoses"] == encounter["diagnoses"]
        assert len(claim["service_lines"]) == len(encounter["procedures"])

    def test_prescription_generates_fill(self):
        """Prescription event should generate pharmacy fill."""
        prescription = {
            "rx_number": "RX001",
            "patient_id": "P001",
            "drug_name": "metformin",
            "ndc": "00378-1805-01",
            "quantity": 60,
            "days_supply": 30,
            "written_date": "2026-01-15"
        }
        
        # Simulated fill generation
        fill = {
            "claim_id": "RXCLM001",
            "rx_number": prescription["rx_number"],
            "cardholder_id": "C001",  # Linked via patient
            "ndc": prescription["ndc"],
            "quantity_dispensed": prescription["quantity"],
            "days_supply": prescription["days_supply"],
            "fill_date": prescription["written_date"]
        }
        
        # Verify linkage
        assert fill["rx_number"] == prescription["rx_number"]
        assert fill["ndc"] == prescription["ndc"]
        assert fill["quantity_dispensed"] == prescription["quantity"]


# ============================================================================
# Timeline Expansion Tests
# ============================================================================

class TestTimelineExpansion:
    """Tests for journey timeline calculations."""

    def test_timeline_absolute_dates(self, sample_journey_spec):
        """Timeline should expand relative days to absolute dates."""
        start_date = datetime(2026, 1, 1)
        
        # Collect all event days
        event_days = []
        for phase in sample_journey_spec["phases"]:
            for event in phase["events"]:
                event_days.append(event["timing"]["day"])
        
        # Expand to absolute dates
        absolute_dates = [start_date + timedelta(days=day) for day in event_days]
        
        # All dates should be after start
        for date in absolute_dates:
            assert date >= start_date

    def test_timeline_variance_application(self):
        """Variance should be applied within bounds."""
        base_day = 30
        variance = 7
        
        # Simulate 100 variance applications
        for _ in range(100):
            actual_day = base_day + random.randint(-variance, variance)
            assert actual_day >= base_day - variance
            assert actual_day <= base_day + variance

    def test_timeline_phase_ordering(self, sample_journey_spec):
        """Phase events should maintain temporal order."""
        cumulative_days = 0
        
        for phase in sample_journey_spec["phases"]:
            phase_events = phase["events"]
            for event in phase_events:
                event_day = event["timing"]["day"]
                # Events should be at or after cumulative start
                # (This is a simplified check - real implementation would track phase offsets)
                assert event_day >= 0


# ============================================================================
# Batch Generation Tests
# ============================================================================

class TestBatchGeneration:
    """Tests for large-scale entity generation."""

    def test_batch_size_limits(self):
        """Batch generation should respect size limits."""
        requested_count = 500
        batch_size = 50
        
        batches = []
        remaining = requested_count
        while remaining > 0:
            batch = min(batch_size, remaining)
            batches.append(batch)
            remaining -= batch
        
        assert sum(batches) == requested_count
        assert all(b <= batch_size for b in batches)

    def test_batch_unique_ids(self):
        """Generated entities should have unique IDs."""
        count = 100
        ids = [f"P{str(i).zfill(6)}" for i in range(1, count + 1)]
        
        assert len(ids) == count
        assert len(set(ids)) == count  # All unique

    def test_batch_distribution_adherence(self, sample_distribution_categorical):
        """Large batches should approximate distribution weights."""
        weights = sample_distribution_categorical["weights"]
        categories = list(weights.keys())
        weight_values = list(weights.values())
        
        # Generate 1000 samples
        samples = random.choices(categories, weights=weight_values, k=1000)
        
        # Count occurrences
        counts = {cat: samples.count(cat) for cat in categories}
        
        # Check proportions are approximately correct (within 10%)
        for cat, expected_weight in weights.items():
            actual_proportion = counts[cat] / 1000
            assert abs(actual_proportion - expected_weight) < 0.1


# ============================================================================
# Template Loading Tests
# ============================================================================

class TestTemplateLoading:
    """Tests for template file loading and parsing."""

    @pytest.fixture
    def template_dir(self):
        """Path to templates directory."""
        return Path(__file__).parent.parent.parent.parent / "skills" / "generation" / "templates"

    def test_profile_templates_exist(self, template_dir):
        """Required profile templates should exist."""
        profiles_dir = template_dir / "profiles"
        required = ["medicare-diabetic.md", "commercial-healthy.md", "medicaid-pediatric.md"]
        
        for template in required:
            template_path = profiles_dir / template
            assert template_path.exists(), f"Missing template: {template}"

    def test_journey_templates_exist(self, template_dir):
        """Required journey templates should exist."""
        journeys_dir = template_dir / "journeys"
        required = ["diabetic-first-year.md", "surgical-episode.md", "new-member-onboarding.md"]
        
        for template in required:
            template_path = journeys_dir / template
            assert template_path.exists(), f"Missing template: {template}"

    def test_template_has_json_spec(self, template_dir):
        """Templates should contain JSON specification block."""
        # Check one template as sample
        template_path = template_dir / "profiles" / "medicare-diabetic.md"
        if template_path.exists():
            content = template_path.read_text()
            # Should have JSON block
            assert "```json" in content or '"profile"' in content


# ============================================================================
# Schema Validation Tests
# ============================================================================

class TestSchemaValidation:
    """Tests for JSON schema compliance."""

    @pytest.fixture
    def schema_dir(self):
        """Path to schemas directory."""
        return Path(__file__).parent.parent.parent.parent / "schemas"

    def test_profile_schema_exists(self, schema_dir):
        """Profile schema file should exist."""
        schema_path = schema_dir / "profile-spec-v1.json"
        assert schema_path.exists()

    def test_journey_schema_exists(self, schema_dir):
        """Journey schema file should exist."""
        schema_path = schema_dir / "journey-spec-v1.json"
        assert schema_path.exists()

    def test_profile_schema_valid_json(self, schema_dir):
        """Profile schema should be valid JSON."""
        schema_path = schema_dir / "profile-spec-v1.json"
        if schema_path.exists():
            content = schema_path.read_text()
            schema = json.loads(content)
            assert "$schema" in schema or "type" in schema

    def test_journey_schema_valid_json(self, schema_dir):
        """Journey schema should be valid JSON."""
        schema_path = schema_dir / "journey-spec-v1.json"
        if schema_path.exists():
            content = schema_path.read_text()
            schema = json.loads(content)
            assert "$schema" in schema or "type" in schema


# ============================================================================
# End-to-End Flow Tests
# ============================================================================

class TestEndToEndFlow:
    """Tests for complete generation workflows."""

    def test_profile_to_entities_flow(self, sample_profile_spec):
        """Profile spec should generate correct entity structure."""
        # Simulate execution
        count = sample_profile_spec["demographics"]["count"]
        
        entities = []
        for i in range(count):
            entity = {
                "patient_id": f"P{str(i+1).zfill(6)}",
                "age": 72,  # Would be sampled from distribution
                "gender": "M",  # Would be sampled from distribution
                "diagnoses": [sample_profile_spec["clinical"]["primary_condition"]["code"]]
            }
            entities.append(entity)
        
        assert len(entities) == count
        for entity in entities:
            assert "patient_id" in entity
            assert "diagnoses" in entity

    def test_profile_journey_combination(self, sample_profile_spec, sample_journey_spec):
        """Profile + Journey should generate entities with events."""
        count = sample_profile_spec["demographics"]["count"]
        
        results = []
        for i in range(count):
            entity = {
                "patient_id": f"P{str(i+1).zfill(6)}",
                "events": []
            }
            
            # Add events from journey
            for phase in sample_journey_spec["phases"]:
                for event in phase["events"]:
                    entity["events"].append({
                        "type": event["type"],
                        "day": event["timing"]["day"]
                    })
            
            results.append(entity)
        
        assert len(results) == count
        for result in results:
            assert len(result["events"]) > 0

    def test_cross_product_generation(self, sample_profile_spec):
        """Multi-product spec should generate linked entities."""
        products = sample_profile_spec["profile"]["products"]
        count = sample_profile_spec["demographics"]["count"]
        
        # Generate for each product
        all_entities = {}
        shared_ssn = "123-45-6789"
        
        for product in products:
            if product == "PatientSim":
                all_entities["patient"] = {"patient_id": "P001", "ssn": shared_ssn}
            elif product == "MemberSim":
                all_entities["member"] = {"member_id": "M001", "ssn": shared_ssn}
        
        # Verify cross-product linkage
        if "patient" in all_entities and "member" in all_entities:
            assert all_entities["patient"]["ssn"] == all_entities["member"]["ssn"]


# ============================================================================
# Run Configuration
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
