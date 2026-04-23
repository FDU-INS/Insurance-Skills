"""Tests for product-specific event handlers."""

import pytest
from datetime import date, datetime

from healthsim.generation.handlers import (
    BaseEventHandler,
    PatientSimHandlers,
    MemberSimHandlers,
    RxMemberSimHandlers,
    TrialSimHandlers,
)
from healthsim.generation.journey_engine import (
    JourneyEngine,
    TimelineEvent,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def timeline_event():
    """Create a basic timeline event."""
    return TimelineEvent(
        timeline_event_id="te-001",
        journey_id="test-journey",
        event_definition_id="e1",
        scheduled_date=date(2024, 1, 15),
        event_type="encounter",
        event_name="Test Event",
        product="patientsim"
    )


@pytest.fixture
def patient_entity():
    """Create a patient entity."""
    return {
        "patient_id": "P001",
        "name": "John Smith",
        "age": 65,
        "gender": "M",
        "conditions": ["E11.9", "I10"]
    }


@pytest.fixture
def member_entity():
    """Create a member entity."""
    return {
        "member_id": "M001",
        "name": "Jane Doe",
        "age": 45,
        "plan_type": "Commercial"
    }


@pytest.fixture
def rx_member_entity():
    """Create an rx member entity."""
    return {
        "rx_member_id": "RX001",
        "member_id": "M001",
        "name": "Bob Wilson"
    }


@pytest.fixture
def subject_entity():
    """Create a trial subject entity."""
    return {
        "subject_id": "SUBJ-001",
        "screening_number": "SCR-001",
        "age": 55
    }


# =============================================================================
# PatientSimHandlers Tests
# =============================================================================

class TestPatientSimHandlers:
    """Tests for PatientSimHandlers."""

    @pytest.fixture
    def handlers(self):
        """Create handlers fixture."""
        return PatientSimHandlers(seed=42)

    def test_initialization(self, handlers):
        """Test handler initialization."""
        assert handlers.seed == 42
        assert handlers.default_facility is not None
        assert len(handlers.providers) > 0

    def test_get_entity_id_from_dict(self, handlers):
        """Test extracting entity ID from dict."""
        entity = {"patient_id": "P123"}
        assert handlers._get_entity_id(entity) == "P123"

    def test_generate_id_deterministic(self, handlers):
        """Test ID generation is deterministic."""
        id1 = handlers._generate_id("ENC", "P001", "evt1")
        id2 = handlers._generate_id("ENC", "P001", "evt1")
        assert id1 == id2

    def test_generate_id_unique_per_event(self, handlers):
        """Test different events get different IDs."""
        id1 = handlers._generate_id("ENC", "P001", "evt1")
        id2 = handlers._generate_id("ENC", "P001", "evt2")
        assert id1 != id2

    def test_select_provider(self, handlers):
        """Test provider selection."""
        provider = handlers._select_provider()
        assert "provider_id" in provider
        assert "npi" in provider

    def test_select_provider_by_specialty(self, handlers):
        """Test provider selection by specialty."""
        provider = handlers._select_provider("Internal Medicine")
        assert provider["specialty"] == "Internal Medicine"

    # -------------------------------------------------------------------------
    # ADT Event Tests
    # -------------------------------------------------------------------------

    def test_handle_admission(self, handlers, patient_entity, timeline_event):
        """Test admission handler."""
        timeline_event.event_type = "admission"
        
        result = handlers.handle_admission(patient_entity, timeline_event, {})
        
        assert "encounter_id" in result
        assert result["patient_id"] == "P001"
        assert result["encounter_type"] == "inpatient"
        assert result["adt_type"] == "A01"
        assert result["status"] == "active"

    def test_handle_discharge(self, handlers, patient_entity, timeline_event):
        """Test discharge handler."""
        timeline_event.event_type = "discharge"
        
        result = handlers.handle_discharge(patient_entity, timeline_event, {})
        
        assert result["patient_id"] == "P001"
        assert result["adt_type"] == "A03"
        assert result["status"] == "completed"

    # -------------------------------------------------------------------------
    # Clinical Event Tests
    # -------------------------------------------------------------------------

    def test_handle_encounter(self, handlers, patient_entity, timeline_event):
        """Test encounter handler."""
        result = handlers.handle_encounter(patient_entity, timeline_event, {})
        
        assert "encounter_id" in result
        assert result["patient_id"] == "P001"
        assert result["encounter_type"] == "outpatient"
        assert result["status"] == "completed"
        assert "provider" in result

    def test_handle_diagnosis(self, handlers, patient_entity, timeline_event):
        """Test diagnosis handler."""
        timeline_event.event_type = "diagnosis"
        timeline_event.result = {"parameters": {"icd10": "E11.9", "description": "Type 2 diabetes"}}
        
        result = handlers.handle_diagnosis(patient_entity, timeline_event, {})
        
        assert "condition_id" in result
        assert result["icd10"] == "E11.9"
        assert result["clinical_status"] == "active"

    def test_handle_lab_order(self, handlers, patient_entity, timeline_event):
        """Test lab order handler."""
        timeline_event.event_type = "lab_order"
        
        result = handlers.handle_lab_order(patient_entity, timeline_event, {})
        
        assert "order_id" in result
        assert result["order_type"] == "laboratory"
        assert result["status"] == "ordered"
        assert "ordering_provider" in result

    def test_handle_lab_result(self, handlers, patient_entity, timeline_event):
        """Test lab result handler."""
        timeline_event.event_type = "lab_result"
        
        result = handlers.handle_lab_result(patient_entity, timeline_event, {})
        
        assert "result_id" in result
        assert "value" in result
        assert "unit" in result
        assert result["status"] == "final"

    def test_lab_value_diabetic_patient(self, handlers, patient_entity, timeline_event):
        """Test A1C value for diabetic patient is elevated."""
        # Patient has E11 (diabetes)
        timeline_event.event_type = "lab_result"
        timeline_event.result = {"parameters": {"loinc": "4548-4"}}
        
        # Sample multiple times - diabetic patients should have higher A1C
        values = []
        for i in range(20):
            h = PatientSimHandlers(seed=i)
            result = h.handle_lab_result(patient_entity, timeline_event, {})
            values.append(result["value"])
        
        avg = sum(values) / len(values)
        assert avg > 6.5  # Diabetic range

    def test_handle_medication_order(self, handlers, patient_entity, timeline_event):
        """Test medication order handler."""
        timeline_event.event_type = "medication_order"
        timeline_event.result = {"parameters": {"rxnorm": "860975", "drug_name": "Metformin 500 MG"}}
        
        result = handlers.handle_medication_order(patient_entity, timeline_event, {})
        
        assert "medication_order_id" in result
        assert result["rxnorm"] == "860975"
        assert result["status"] == "active"
        assert "prescriber" in result

    def test_handle_procedure(self, handlers, patient_entity, timeline_event):
        """Test procedure handler."""
        timeline_event.event_type = "procedure"
        
        result = handlers.handle_procedure(patient_entity, timeline_event, {})
        
        assert "procedure_id" in result
        assert "cpt" in result
        assert result["status"] == "completed"

    def test_register_all(self, handlers):
        """Test registering all handlers with engine."""
        engine = JourneyEngine(seed=42)
        
        handlers.register_all(engine)
        
        assert "patientsim" in engine._handlers
        assert "encounter" in engine._handlers["patientsim"]
        assert "admission" in engine._handlers["patientsim"]
        assert "lab_order" in engine._handlers["patientsim"]


# =============================================================================
# MemberSimHandlers Tests
# =============================================================================

class TestMemberSimHandlers:
    """Tests for MemberSimHandlers."""

    @pytest.fixture
    def handlers(self):
        """Create handlers fixture."""
        return MemberSimHandlers(seed=42)

    def test_initialization(self, handlers):
        """Test handler initialization."""
        assert handlers.seed == 42
        assert len(handlers.plans) > 0

    def test_select_plan(self, handlers):
        """Test plan selection."""
        plan = handlers._select_plan()
        assert "plan_id" in plan
        assert "plan_name" in plan

    def test_select_plan_by_type(self, handlers):
        """Test plan selection by type."""
        plan = handlers._select_plan("MA")
        assert plan["plan_type"] == "MA"

    # -------------------------------------------------------------------------
    # Enrollment Event Tests
    # -------------------------------------------------------------------------

    def test_handle_new_enrollment(self, handlers, member_entity, timeline_event):
        """Test new enrollment handler."""
        timeline_event.event_type = "new_enrollment"
        timeline_event.product = "membersim"
        
        result = handlers.handle_new_enrollment(member_entity, timeline_event, {})
        
        assert "enrollment_id" in result
        assert result["member_id"] == "M001"
        assert "plan" in result
        assert result["status"] == "active"

    def test_handle_termination(self, handlers, member_entity, timeline_event):
        """Test termination handler."""
        timeline_event.event_type = "termination"
        
        result = handlers.handle_termination(member_entity, timeline_event, {})
        
        assert result["member_id"] == "M001"
        assert result["status"] == "terminated"
        assert "termination_reason" in result

    def test_handle_plan_change(self, handlers, member_entity, timeline_event):
        """Test plan change handler."""
        timeline_event.event_type = "plan_change"
        
        result = handlers.handle_plan_change(member_entity, timeline_event, {})
        
        assert result["member_id"] == "M001"
        assert "new_plan" in result
        assert "change_reason" in result

    # -------------------------------------------------------------------------
    # Claims Event Tests
    # -------------------------------------------------------------------------

    def test_handle_claim_professional(self, handlers, member_entity, timeline_event):
        """Test professional claim handler."""
        timeline_event.event_type = "claim_professional"
        
        result = handlers.handle_claim_professional(member_entity, timeline_event, {})
        
        assert "claim_id" in result
        assert result["claim_type"] == "professional"
        assert result["billed_amount"] > 0
        assert result["allowed_amount"] <= result["billed_amount"]
        assert result["paid_amount"] <= result["allowed_amount"]

    def test_handle_claim_institutional(self, handlers, member_entity, timeline_event):
        """Test institutional claim handler."""
        timeline_event.event_type = "claim_institutional"
        
        result = handlers.handle_claim_institutional(member_entity, timeline_event, {})
        
        assert "claim_id" in result
        assert result["claim_type"] == "institutional"
        # Institutional claims should be larger
        assert result["billed_amount"] >= 5000

    def test_handle_claim_pharmacy(self, handlers, member_entity, timeline_event):
        """Test pharmacy claim handler."""
        timeline_event.event_type = "claim_pharmacy"
        
        result = handlers.handle_claim_pharmacy(member_entity, timeline_event, {})
        
        assert "claim_id" in result
        assert result["claim_type"] == "pharmacy"
        assert "copay" in result
        assert "days_supply" in result

    # -------------------------------------------------------------------------
    # Quality Event Tests
    # -------------------------------------------------------------------------

    def test_handle_gap_identified(self, handlers, member_entity, timeline_event):
        """Test gap identified handler."""
        timeline_event.event_type = "gap_identified"
        timeline_event.result = {"parameters": {"measure": "CDC"}}
        
        result = handlers.handle_gap_identified(member_entity, timeline_event, {})
        
        assert "gap_id" in result
        assert result["measure"] == "CDC"
        assert result["status"] == "open"

    def test_handle_gap_closed(self, handlers, member_entity, timeline_event):
        """Test gap closed handler."""
        timeline_event.event_type = "gap_closed"
        
        result = handlers.handle_gap_closed(member_entity, timeline_event, {})
        
        assert result["member_id"] == "M001"
        assert result["status"] == "closed"

    def test_register_all(self, handlers):
        """Test registering all handlers with engine."""
        engine = JourneyEngine(seed=42)
        
        handlers.register_all(engine)
        
        assert "membersim" in engine._handlers
        assert "new_enrollment" in engine._handlers["membersim"]
        assert "claim_professional" in engine._handlers["membersim"]


# =============================================================================
# RxMemberSimHandlers Tests
# =============================================================================

class TestRxMemberSimHandlers:
    """Tests for RxMemberSimHandlers."""

    @pytest.fixture
    def handlers(self):
        """Create handlers fixture."""
        return RxMemberSimHandlers(seed=42)

    def test_initialization(self, handlers):
        """Test handler initialization."""
        assert handlers.seed == 42
        assert len(handlers.pharmacies) > 0

    def test_select_pharmacy(self, handlers):
        """Test pharmacy selection."""
        pharmacy = handlers._select_pharmacy()
        assert "pharmacy_id" in pharmacy
        assert "npi" in pharmacy

    # -------------------------------------------------------------------------
    # Prescription Event Tests
    # -------------------------------------------------------------------------

    def test_handle_new_rx(self, handlers, rx_member_entity, timeline_event):
        """Test new prescription handler."""
        timeline_event.event_type = "new_rx"
        timeline_event.product = "rxmembersim"
        
        result = handlers.handle_new_rx(rx_member_entity, timeline_event, {})
        
        assert "rx_id" in result
        assert result["member_id"] == "RX001"
        assert "rxnorm" in result
        assert result["status"] == "active"
        assert result["refills_remaining"] > 0

    def test_handle_fill(self, handlers, rx_member_entity, timeline_event):
        """Test prescription fill handler."""
        timeline_event.event_type = "fill"
        
        result = handlers.handle_fill(rx_member_entity, timeline_event, {})
        
        assert "fill_id" in result
        assert "pharmacy" in result
        assert result["status"] == "dispensed"

    def test_handle_refill(self, handlers, rx_member_entity, timeline_event):
        """Test prescription refill handler."""
        timeline_event.event_type = "refill"
        
        result = handlers.handle_refill(rx_member_entity, timeline_event, {})
        
        assert "fill_id" in result
        assert result["is_refill"] is True
        assert result["fill_number"] >= 2

    def test_handle_reversal(self, handlers, rx_member_entity, timeline_event):
        """Test claim reversal handler."""
        timeline_event.event_type = "reversal"
        
        result = handlers.handle_reversal(rx_member_entity, timeline_event, {})
        
        assert result["status"] == "reversed"
        assert "reversal_reason" in result

    # -------------------------------------------------------------------------
    # Therapy Event Tests
    # -------------------------------------------------------------------------

    def test_handle_therapy_start(self, handlers, rx_member_entity, timeline_event):
        """Test therapy start handler."""
        timeline_event.event_type = "therapy_start"
        
        result = handlers.handle_therapy_start(rx_member_entity, timeline_event, {})
        
        assert "therapy_id" in result
        assert result["status"] == "active"
        assert "therapy_class" in result

    def test_handle_therapy_change(self, handlers, rx_member_entity, timeline_event):
        """Test therapy change handler."""
        timeline_event.event_type = "therapy_change"
        
        result = handlers.handle_therapy_change(rx_member_entity, timeline_event, {})
        
        assert "change_type" in result
        assert "reason" in result

    def test_handle_therapy_discontinue(self, handlers, rx_member_entity, timeline_event):
        """Test therapy discontinuation handler."""
        timeline_event.event_type = "therapy_discontinue"
        
        result = handlers.handle_therapy_discontinue(rx_member_entity, timeline_event, {})
        
        assert result["status"] == "discontinued"
        assert "reason" in result

    # -------------------------------------------------------------------------
    # Adherence Event Tests
    # -------------------------------------------------------------------------

    def test_handle_adherence_gap(self, handlers, rx_member_entity, timeline_event):
        """Test adherence gap handler."""
        timeline_event.event_type = "adherence_gap"
        
        result = handlers.handle_adherence_gap(rx_member_entity, timeline_event, {})
        
        assert "gap_id" in result
        assert result["status"] == "open"
        assert "days_without_medication" in result

    def test_handle_mpr_threshold(self, handlers, rx_member_entity, timeline_event):
        """Test MPR threshold handler."""
        timeline_event.event_type = "mpr_threshold"
        timeline_event.result = {"parameters": {"mpr": 0.85, "threshold": 0.80}}
        
        result = handlers.handle_mpr_threshold(rx_member_entity, timeline_event, {})
        
        assert result["mpr"] == 0.85
        assert result["is_adherent"] is True

    def test_handle_mpr_threshold_non_adherent(self, handlers, rx_member_entity, timeline_event):
        """Test MPR threshold for non-adherent member."""
        timeline_event.event_type = "mpr_threshold"
        timeline_event.result = {"parameters": {"mpr": 0.65, "threshold": 0.80}}
        
        result = handlers.handle_mpr_threshold(rx_member_entity, timeline_event, {})
        
        assert result["is_adherent"] is False

    def test_register_all(self, handlers):
        """Test registering all handlers with engine."""
        engine = JourneyEngine(seed=42)
        
        handlers.register_all(engine)
        
        assert "rxmembersim" in engine._handlers
        assert "new_rx" in engine._handlers["rxmembersim"]
        assert "fill" in engine._handlers["rxmembersim"]


# =============================================================================
# TrialSimHandlers Tests
# =============================================================================

class TestTrialSimHandlers:
    """Tests for TrialSimHandlers."""

    @pytest.fixture
    def handlers(self):
        """Create handlers fixture."""
        return TrialSimHandlers(seed=42)

    def test_initialization(self, handlers):
        """Test handler initialization."""
        assert handlers.seed == 42
        assert len(handlers.sites) > 0
        assert len(handlers.arms) > 0

    def test_select_site(self, handlers):
        """Test site selection."""
        site = handlers._select_site()
        assert "site_id" in site
        assert "pi" in site

    # -------------------------------------------------------------------------
    # Enrollment Event Tests
    # -------------------------------------------------------------------------

    def test_handle_screening(self, handlers, subject_entity, timeline_event):
        """Test screening handler."""
        timeline_event.event_type = "screening"
        timeline_event.product = "trialsim"
        
        result = handlers.handle_screening(subject_entity, timeline_event, {})
        
        assert "screening_id" in result
        assert result["subject_id"] == "SUBJ-001"
        assert "site" in result
        assert result["screen_status"] in ["passed", "failed"]

    def test_handle_screening_pass_rate(self, handlers, subject_entity, timeline_event):
        """Test screening pass rate."""
        timeline_event.event_type = "screening"
        timeline_event.result = {"parameters": {"pass_rate": 0.75}}
        
        passed = 0
        for i in range(100):
            h = TrialSimHandlers(seed=i)
            result = h.handle_screening(subject_entity, timeline_event, {})
            if result["screen_status"] == "passed":
                passed += 1
        
        # Should be roughly 75%
        assert 60 < passed < 90

    def test_handle_randomization(self, handlers, subject_entity, timeline_event):
        """Test randomization handler."""
        timeline_event.event_type = "randomization"
        
        result = handlers.handle_randomization(subject_entity, timeline_event, {})
        
        assert "randomization_id" in result
        assert result["treatment_arm"] in ["Treatment", "Placebo", "Active Comparator"]
        assert "randomization_number" in result

    def test_handle_randomization_arm_weights(self, handlers, subject_entity, timeline_event):
        """Test randomization respects arm weights."""
        timeline_event.event_type = "randomization"
        timeline_event.result = {"parameters": {"arm_weights": {"Treatment": 0.7, "Placebo": 0.3}}}
        
        arms = {"Treatment": 0, "Placebo": 0}
        for i in range(100):
            h = TrialSimHandlers(seed=i)
            result = h.handle_randomization(subject_entity, timeline_event, {})
            if result["treatment_arm"] in arms:
                arms[result["treatment_arm"]] += 1
        
        # Treatment should be more common
        assert arms["Treatment"] > arms["Placebo"]

    def test_handle_withdrawal(self, handlers, subject_entity, timeline_event):
        """Test withdrawal handler."""
        timeline_event.event_type = "withdrawal"
        
        result = handlers.handle_withdrawal(subject_entity, timeline_event, {})
        
        assert result["subject_id"] == "SUBJ-001"
        assert "withdrawal_reason" in result
        assert "withdrawal_type" in result

    # -------------------------------------------------------------------------
    # Visit Event Tests
    # -------------------------------------------------------------------------

    def test_handle_scheduled_visit(self, handlers, subject_entity, timeline_event):
        """Test scheduled visit handler."""
        timeline_event.event_type = "scheduled_visit"
        timeline_event.result = {"parameters": {"visit_number": 2, "visit_name": "Week 4"}}
        
        result = handlers.handle_scheduled_visit(subject_entity, timeline_event, {})
        
        assert "visit_id" in result
        assert result["visit_number"] == 2
        assert result["visit_name"] == "Week 4"
        assert result["status"] == "completed"

    def test_handle_unscheduled_visit(self, handlers, subject_entity, timeline_event):
        """Test unscheduled visit handler."""
        timeline_event.event_type = "unscheduled_visit"
        
        result = handlers.handle_unscheduled_visit(subject_entity, timeline_event, {})
        
        assert "visit_id" in result
        assert result["visit_type"] == "unscheduled"
        assert "reason" in result

    # -------------------------------------------------------------------------
    # Safety Event Tests
    # -------------------------------------------------------------------------

    def test_handle_adverse_event(self, handlers, subject_entity, timeline_event):
        """Test adverse event handler."""
        timeline_event.event_type = "adverse_event"
        timeline_event.result = {"parameters": {"term": "Headache", "severity": "Mild"}}
        
        result = handlers.handle_adverse_event(subject_entity, timeline_event, {})
        
        assert "ae_id" in result
        assert result["ae_term"] == "Headache"
        assert result["severity"] == "Mild"
        assert result["serious"] is False

    def test_handle_serious_adverse_event(self, handlers, subject_entity, timeline_event):
        """Test serious adverse event handler."""
        timeline_event.event_type = "serious_adverse_event"
        timeline_event.result = {"parameters": {"term": "Hospitalization", "criteria": ["hospitalization"]}}
        
        result = handlers.handle_serious_adverse_event(subject_entity, timeline_event, {})
        
        assert "sae_id" in result
        assert result["serious"] is True
        assert "seriousness_criteria" in result

    # -------------------------------------------------------------------------
    # Protocol Event Tests
    # -------------------------------------------------------------------------

    def test_handle_protocol_deviation(self, handlers, subject_entity, timeline_event):
        """Test protocol deviation handler."""
        timeline_event.event_type = "protocol_deviation"
        
        result = handlers.handle_protocol_deviation(subject_entity, timeline_event, {})
        
        assert "deviation_id" in result
        assert "category" in result
        assert "severity" in result

    def test_handle_dose_modification(self, handlers, subject_entity, timeline_event):
        """Test dose modification handler."""
        timeline_event.event_type = "dose_modification"
        timeline_event.result = {"parameters": {"type": "dose_reduction", "reduction_level": 1}}
        
        result = handlers.handle_dose_modification(subject_entity, timeline_event, {})
        
        assert result["subject_id"] == "SUBJ-001"
        assert result["modification_type"] == "dose_reduction"
        assert "reason" in result

    def test_register_all(self, handlers):
        """Test registering all handlers with engine."""
        engine = JourneyEngine(seed=42)
        
        handlers.register_all(engine)
        
        assert "trialsim" in engine._handlers
        assert "screening" in engine._handlers["trialsim"]
        assert "randomization" in engine._handlers["trialsim"]
        assert "adverse_event" in engine._handlers["trialsim"]


# =============================================================================
# Integration Tests
# =============================================================================

class TestHandlerIntegration:
    """Integration tests for handlers with journey engine."""

    def test_patientsim_journey_execution(self):
        """Test PatientSim handlers execute in a journey."""
        from healthsim.generation.journey_engine import create_simple_journey
        
        engine = JourneyEngine(seed=42)
        handlers = PatientSimHandlers(seed=42)
        handlers.register_all(engine)
        
        journey = create_simple_journey(
            journey_id="test-patient-journey",
            name="Test Patient Journey",
            events=[
                {"event_id": "e1", "name": "Office Visit", "event_type": "encounter",
                 "product": "patientsim", "delay": {"days": 0}},
                {"event_id": "e2", "name": "Lab Order", "event_type": "lab_order",
                 "product": "patientsim", "delay": {"days": 0}, "depends_on": "e1"},
            ],
            products=["patientsim"]
        )
        
        patient = {"patient_id": "P001", "name": "Test Patient"}
        timeline = engine.create_timeline(patient, "patient", journey, date(2024, 1, 1))
        
        results = engine.execute_timeline(timeline, patient, up_to_date=date(2024, 12, 31))
        
        assert len(results) == 2
        assert all(r["status"] == "executed" for r in results)

    def test_membersim_journey_execution(self):
        """Test MemberSim handlers execute in a journey."""
        from healthsim.generation.journey_engine import create_simple_journey
        
        engine = JourneyEngine(seed=42)
        handlers = MemberSimHandlers(seed=42)
        handlers.register_all(engine)
        
        journey = create_simple_journey(
            journey_id="test-member-journey",
            name="Test Member Journey",
            events=[
                {"event_id": "e1", "name": "Enrollment", "event_type": "new_enrollment",
                 "product": "membersim", "delay": {"days": 0}},
                {"event_id": "e2", "name": "First Claim", "event_type": "claim_professional",
                 "product": "membersim", "delay": {"days": 30}, "depends_on": "e1"},
            ],
            products=["membersim"]
        )
        
        member = {"member_id": "M001"}
        timeline = engine.create_timeline(member, "member", journey, date(2024, 1, 1))
        
        results = engine.execute_timeline(timeline, member, up_to_date=date(2024, 12, 31))
        
        assert len(results) == 2
        assert all(r["status"] == "executed" for r in results)

    def test_cross_product_handler_registration(self):
        """Test multiple product handlers can be registered."""
        engine = JourneyEngine(seed=42)
        
        PatientSimHandlers(seed=42).register_all(engine)
        MemberSimHandlers(seed=42).register_all(engine)
        RxMemberSimHandlers(seed=42).register_all(engine)
        TrialSimHandlers(seed=42).register_all(engine)
        
        assert "patientsim" in engine._handlers
        assert "membersim" in engine._handlers
        assert "rxmembersim" in engine._handlers
        assert "trialsim" in engine._handlers

    def test_handler_reproducibility(self):
        """Test handlers produce reproducible results."""
        patient = {"patient_id": "P001", "conditions": ["E11"]}
        event = TimelineEvent(
            timeline_event_id="te-001",
            journey_id="j1",
            event_definition_id="e1",
            scheduled_date=date(2024, 1, 15),
            event_type="lab_result",
            event_name="A1C Test",
            result={"parameters": {"loinc": "4548-4"}}
        )
        
        h1 = PatientSimHandlers(seed=42)
        h2 = PatientSimHandlers(seed=42)
        
        r1 = h1.handle_lab_result(patient, event, {})
        r2 = h2.handle_lab_result(patient, event, {})
        
        assert r1["value"] == r2["value"]
        assert r1["result_id"] == r2["result_id"]
