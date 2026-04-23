"""Tests for product-specific event handlers."""

import pytest
from datetime import date

from healthsim.generation.journey_engine import (
    JourneyEngine,
    TimelineEvent,
    create_simple_journey,
)
from healthsim.generation.handlers import (
    PatientSimHandlers,
    MemberSimHandlers,
    RxMemberSimHandlers,
    TrialSimHandlers,
    create_patientsim_handlers,
    create_membersim_handlers,
    create_rxmembersim_handlers,
    create_trialsim_handlers,
    register_all_handlers,
)


class TestPatientSimHandlers:
    """Tests for PatientSim handlers."""
    
    def test_creation(self):
        """Test creating handlers."""
        handlers = PatientSimHandlers(seed=42)
        assert handlers.seed == 42
    
    def test_handle_diagnosis(self):
        """Test diagnosis handler."""
        handlers = PatientSimHandlers(seed=42)
        
        entity = {"patient_id": "P001", "name": "Test Patient"}
        event = TimelineEvent(
            timeline_event_id="e1",
            journey_id="j1",
            event_definition_id="ed1",
            scheduled_date=date(2025, 1, 1),
            event_type="diagnosis",
            event_name="Diabetes Diagnosis",
            result={"parameters": {"icd10": "E11.9", "description": "Type 2 diabetes"}}
        )
        
        result = handlers.handle_diagnosis(entity, event, {})
        
        assert result["patient_id"] == "P001"
        assert result["icd10"] == "E11.9"
        assert result["clinical_status"] == "active"
        assert "condition_id" in result
    
    def test_handle_encounter(self):
        """Test encounter handler."""
        handlers = PatientSimHandlers(seed=42)
        
        entity = {"patient_id": "P001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 15), event_type="encounter",
            event_name="Follow-up Visit"
        )
        
        result = handlers.handle_encounter(entity, event, {})
        
        assert result["patient_id"] == "P001"
        assert result["encounter_type"] == "outpatient"
        assert result["status"] == "completed"
    
    def test_handle_lab_order(self):
        """Test lab order handler."""
        handlers = PatientSimHandlers(seed=42)
        
        entity = {"patient_id": "P001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 1), event_type="lab_order",
            event_name="A1C Test",
            result={"parameters": {"loinc": "4548-4", "test_name": "Hemoglobin A1c"}}
        )
        
        result = handlers.handle_lab_order(entity, event, {})
        
        assert result["patient_id"] == "P001"
        assert result["loinc"] == "4548-4"
        assert result["status"] == "ordered"
    
    def test_handle_lab_result(self):
        """Test lab result handler generates realistic values."""
        handlers = PatientSimHandlers(seed=42)
        
        # Diabetic patient
        entity = {"patient_id": "P001", "conditions": ["E11.9"]}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 5), event_type="lab_result",
            event_name="A1C Result",
            result={"parameters": {"loinc": "4548-4"}}
        )
        
        result = handlers.handle_lab_result(entity, event, {})
        
        assert result["patient_id"] == "P001"
        assert result["loinc"] == "4548-4"
        assert 4.0 <= result["value"] <= 14.0
        assert result["unit"] == "%"
    
    def test_handle_medication_order(self):
        """Test medication order handler."""
        handlers = PatientSimHandlers(seed=42)
        
        entity = {"patient_id": "P001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 3), event_type="medication_order",
            event_name="Start Metformin",
            result={"parameters": {"rxnorm": "860975", "drug_name": "Metformin 500 MG"}}
        )
        
        result = handlers.handle_medication_order(entity, event, {})
        
        assert result["patient_id"] == "P001"
        assert result["rxnorm"] == "860975"
        assert result["status"] == "active"
    
    def test_register_all(self):
        """Test registering all handlers with engine."""
        handlers = PatientSimHandlers(seed=42)
        engine = JourneyEngine(seed=42)
        
        handlers.register_all(engine)
        
        # Check handlers are registered
        assert "patientsim" in engine._handlers
        assert "diagnosis" in engine._handlers["patientsim"]
        assert "encounter" in engine._handlers["patientsim"]


class TestMemberSimHandlers:
    """Tests for MemberSim handlers."""
    
    def test_handle_new_enrollment(self):
        """Test enrollment handler."""
        handlers = MemberSimHandlers(seed=42)
        
        entity = {"member_id": "M001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 1), event_type="new_enrollment",
            event_name="New Enrollment"
        )
        
        result = handlers.handle_new_enrollment(entity, event, {})
        
        assert result["member_id"] == "M001"
        assert result["status"] == "active"
        assert "plan" in result
    
    def test_handle_claim_professional(self):
        """Test professional claim handler."""
        handlers = MemberSimHandlers(seed=42)
        
        entity = {"member_id": "M001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 15), event_type="claim_professional",
            event_name="Office Visit Claim"
        )
        
        result = handlers.handle_claim_professional(entity, event, {})
        
        assert result["member_id"] == "M001"
        assert result["claim_type"] == "professional"
        assert result["billed_amount"] > 0
        assert result["paid_amount"] <= result["allowed_amount"]
    
    def test_handle_claim_pharmacy(self):
        """Test pharmacy claim handler."""
        handlers = MemberSimHandlers(seed=42)
        
        entity = {"member_id": "M001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 5), event_type="claim_pharmacy",
            event_name="Rx Claim",
            result={"parameters": {"drug_name": "Metformin 500mg", "quantity": 30}}
        )
        
        result = handlers.handle_claim_pharmacy(entity, event, {})
        
        assert result["member_id"] == "M001"
        assert result["claim_type"] == "pharmacy"
        assert result["quantity"] == 30
    
    def test_handle_gap_identified(self):
        """Test quality gap handler."""
        handlers = MemberSimHandlers(seed=42)
        
        entity = {"member_id": "M001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 2, 1), event_type="gap_identified",
            event_name="A1C Gap",
            result={"parameters": {"measure": "CDC", "description": "A1C not completed"}}
        )
        
        result = handlers.handle_gap_identified(entity, event, {})
        
        assert result["member_id"] == "M001"
        assert result["measure"] == "CDC"
        assert result["status"] == "open"


class TestRxMemberSimHandlers:
    """Tests for RxMemberSim handlers."""
    
    def test_handle_new_rx(self):
        """Test new prescription handler."""
        handlers = RxMemberSimHandlers(seed=42)
        
        entity = {"rx_member_id": "RX001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 3), event_type="new_rx",
            event_name="New Rx",
            result={"parameters": {"rxnorm": "860975", "drug_name": "Metformin"}}
        )
        
        result = handlers.handle_new_rx(entity, event, {})
        
        assert result["member_id"] == "RX001"
        assert result["rxnorm"] == "860975"
        assert result["status"] == "active"
    
    def test_handle_fill(self):
        """Test fill handler."""
        handlers = RxMemberSimHandlers(seed=42)
        
        entity = {"rx_member_id": "RX001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 5), event_type="fill",
            event_name="Initial Fill"
        )
        
        result = handlers.handle_fill(entity, event, {})
        
        assert result["member_id"] == "RX001"
        assert result["status"] == "dispensed"
        assert "pharmacy" in result
    
    def test_handle_therapy_start(self):
        """Test therapy start handler."""
        handlers = RxMemberSimHandlers(seed=42)
        
        entity = {"rx_member_id": "RX001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 5), event_type="therapy_start",
            event_name="Start Antidiabetic",
            result={"parameters": {"therapy_class": "antidiabetic", "indication": "Type 2 Diabetes"}}
        )
        
        result = handlers.handle_therapy_start(entity, event, {})
        
        assert result["member_id"] == "RX001"
        assert result["therapy_class"] == "antidiabetic"
        assert result["status"] == "active"


class TestTrialSimHandlers:
    """Tests for TrialSim handlers."""
    
    def test_handle_screening(self):
        """Test screening handler."""
        handlers = TrialSimHandlers(seed=42)
        
        entity = {"subject_id": "SUBJ-001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 1), event_type="screening",
            event_name="Screening Visit"
        )
        
        result = handlers.handle_screening(entity, event, {})
        
        assert result["subject_id"] == "SUBJ-001"
        assert result["screen_status"] in ["passed", "failed"]
        assert "site" in result
    
    def test_handle_randomization(self):
        """Test randomization handler."""
        handlers = TrialSimHandlers(seed=42)
        
        entity = {"subject_id": "SUBJ-001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 1, 8), event_type="randomization",
            event_name="Randomization"
        )
        
        result = handlers.handle_randomization(entity, event, {})
        
        assert result["subject_id"] == "SUBJ-001"
        assert result["treatment_arm"] in ["Treatment", "Placebo"]
    
    def test_handle_adverse_event(self):
        """Test adverse event handler."""
        handlers = TrialSimHandlers(seed=42)
        
        entity = {"subject_id": "SUBJ-001"}
        event = TimelineEvent(
            timeline_event_id="e1", journey_id="j1", event_definition_id="ed1",
            scheduled_date=date(2025, 2, 15), event_type="adverse_event",
            event_name="AE Report",
            result={"parameters": {"term": "Nausea", "severity": "Mild"}}
        )
        
        result = handlers.handle_adverse_event(entity, event, {})
        
        assert result["subject_id"] == "SUBJ-001"
        assert result["ae_term"] == "Nausea"
        assert result["serious"] is False


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_create_handlers(self):
        """Test handler factory functions."""
        ps = create_patientsim_handlers(42)
        ms = create_membersim_handlers(42)
        rx = create_rxmembersim_handlers(42)
        ts = create_trialsim_handlers(42)
        
        assert isinstance(ps, PatientSimHandlers)
        assert isinstance(ms, MemberSimHandlers)
        assert isinstance(rx, RxMemberSimHandlers)
        assert isinstance(ts, TrialSimHandlers)
    
    def test_register_all_handlers(self):
        """Test registering all handlers."""
        engine = JourneyEngine(seed=42)
        register_all_handlers(engine, seed=42)
        
        # Check all products registered
        assert "patientsim" in engine._handlers
        assert "membersim" in engine._handlers
        assert "rxmembersim" in engine._handlers
        assert "trialsim" in engine._handlers


class TestEndToEndWithHandlers:
    """End-to-end tests with handlers and journey engine."""
    
    def test_diabetic_journey_execution(self):
        """Test executing diabetic journey with handlers."""
        # Create engine with handlers
        engine = JourneyEngine(seed=42)
        register_all_handlers(engine, seed=42)
        
        # Create journey
        journey = create_simple_journey(
            "test-diabetes",
            "Test Diabetes",
            events=[
                {"event_id": "dx", "name": "Diagnosis", "event_type": "diagnosis",
                 "product": "patientsim", "delay": {"days": 0},
                 "parameters": {"icd10": "E11.9"}},
                {"event_id": "med", "name": "Metformin", "event_type": "medication_order",
                 "product": "patientsim", "delay": {"days": 3}, "depends_on": "dx",
                 "parameters": {"rxnorm": "860975"}},
            ],
            products=["patientsim"]
        )
        
        # Create timeline
        patient = {"patient_id": "P001", "name": "Test Patient"}
        timeline = engine.create_timeline(patient, "patient", journey, date(2025, 1, 1))
        
        # Execute
        results = engine.execute_timeline(timeline, patient, up_to_date=date(2025, 1, 10))
        
        assert len(results) == 2
        assert results[0]["status"] == "executed"
        assert results[1]["status"] == "executed"
