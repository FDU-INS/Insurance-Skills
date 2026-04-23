"""Tests for clinical timeline functionality."""

from datetime import date, datetime, timedelta

from healthsim.temporal import EventStatus

from patientsim.core import ClinicalEvent, ClinicalEventType, ClinicalTimeline


class TestClinicalTimeline:
    """Tests for ClinicalTimeline class."""

    def test_timeline_creation(self) -> None:
        """Test creating a clinical timeline."""
        # Arrange & Act
        timeline = ClinicalTimeline(patient_mrn="MRN12345")

        # Assert
        assert timeline.patient_mrn == "MRN12345"
        assert len(timeline) == 0
        assert timeline.current_encounter_id is None

    def test_add_admission(self) -> None:
        """Test adding an admission event."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        admission_time = datetime(2025, 1, 26, 14, 30)

        # Act
        event = timeline.add_admission(
            admission_time=admission_time,
            facility="General Hospital",
            department="Emergency",
            chief_complaint="Chest pain",
        )

        # Assert
        assert len(timeline) == 1
        assert event.clinical_type == ClinicalEventType.ADMISSION
        assert event.location == "General Hospital"
        assert event.department == "Emergency"
        assert event.payload["chief_complaint"] == "Chest pain"
        assert timeline.current_encounter_id is not None

    def test_add_discharge(self) -> None:
        """Test adding a discharge event."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        admission_time = datetime(2025, 1, 26, 14, 30)
        discharge_time = datetime(2025, 1, 27, 10, 0)

        timeline.add_admission(admission_time, facility="Hospital")

        # Act
        event = timeline.add_discharge(
            discharge_time=discharge_time,
            disposition="Home",
            discharge_diagnosis="Stable angina",
        )

        # Assert
        assert len(timeline) == 2
        assert event.clinical_type == ClinicalEventType.DISCHARGE
        assert event.payload["disposition"] == "Home"
        assert timeline.current_encounter_id is None  # Cleared after discharge

    def test_add_diagnosis(self) -> None:
        """Test adding a diagnosis event."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")

        # Act
        event = timeline.add_diagnosis(
            diagnosis_code="E11.9",
            description="Type 2 diabetes mellitus",
            diagnosed_date=datetime(2025, 1, 15),
            provider_id="DR001",
        )

        # Assert
        assert len(timeline) == 1
        assert event.clinical_type == ClinicalEventType.DIAGNOSIS
        assert event.diagnosis_code == "E11.9"
        assert event.provider_id == "DR001"

    def test_add_lab_order_and_result(self) -> None:
        """Test adding lab order and result events."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        order_time = datetime(2025, 1, 26, 8, 0)
        result_time = datetime(2025, 1, 26, 10, 30)

        # Act
        order = timeline.add_lab_order(
            lab_code="2345-7",
            test_name="Glucose",
            order_time=order_time,
            provider_id="DR001",
        )

        result = timeline.add_lab_result(
            lab_code="2345-7",
            test_name="Glucose",
            value="95",
            unit="mg/dL",
            result_time=result_time,
        )

        # Assert
        assert len(timeline) == 2
        assert order.clinical_type == ClinicalEventType.LAB_ORDER
        assert result.clinical_type == ClinicalEventType.LAB_RESULT
        assert result.payload["value"] == "95"
        assert result.payload["unit"] == "mg/dL"

    def test_add_medication_start_and_stop(self) -> None:
        """Test adding medication start and stop events."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        start_time = datetime(2025, 1, 26, 9, 0)
        stop_time = datetime(2025, 1, 28, 9, 0)

        # Act
        start = timeline.add_medication_start(
            medication_code="860975",
            medication_name="Metformin",
            dose="500 mg",
            route="PO",
            frequency="BID",
            start_time=start_time,
            indication="Type 2 diabetes",
        )

        stop = timeline.add_medication_stop(
            medication_code="860975",
            medication_name="Metformin",
            stop_time=stop_time,
            reason="Patient completed course",
        )

        # Assert
        assert len(timeline) == 2
        assert start.clinical_type == ClinicalEventType.MEDICATION_START
        assert stop.clinical_type == ClinicalEventType.MEDICATION_STOP
        assert start.medication_code == "860975"

    def test_add_procedure(self) -> None:
        """Test adding a procedure event."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        procedure_time = datetime(2025, 1, 26, 14, 0)

        # Act
        event = timeline.add_procedure(
            procedure_code="93000",
            description="Electrocardiogram",
            procedure_time=procedure_time,
            provider_id="DR001",
            location="Cardiology Lab",
        )

        # Assert
        assert len(timeline) == 1
        assert event.clinical_type == ClinicalEventType.PROCEDURE
        assert event.procedure_code == "93000"
        assert event.location == "Cardiology Lab"

    def test_add_vital_signs(self) -> None:
        """Test adding vital signs event."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        obs_time = datetime(2025, 1, 26, 14, 0)

        # Act
        event = timeline.add_vital_signs(
            observation_time=obs_time,
            temperature=98.6,
            heart_rate=72,
            respiratory_rate=16,
            systolic_bp=120,
            diastolic_bp=80,
            spo2=98,
        )

        # Assert
        assert len(timeline) == 1
        assert event.clinical_type == ClinicalEventType.VITAL_SIGNS
        assert event.payload["heart_rate"] == 72
        assert event.payload["systolic_bp"] == 120

    def test_add_note(self) -> None:
        """Test adding a clinical note event."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        note_time = datetime(2025, 1, 26, 10, 0)

        # Act
        event = timeline.add_note(
            note_type="Progress Note",
            text="Patient reports improvement in symptoms.",
            note_time=note_time,
            author="Dr. Jane Smith",
        )

        # Assert
        assert len(timeline) == 1
        assert event.clinical_type == ClinicalEventType.NOTE
        assert event.clinical_notes == "Patient reports improvement in symptoms."
        assert event.provider_id == "Dr. Jane Smith"

    def test_add_follow_up(self) -> None:
        """Test adding a follow-up event."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        follow_up_date = date(2025, 2, 15)

        # Act
        event = timeline.add_follow_up(
            follow_up_date=follow_up_date,
            reason="Diabetes management",
            provider_id="DR001",
        )

        # Assert
        assert len(timeline) == 1
        assert event.clinical_type == ClinicalEventType.FOLLOW_UP
        assert event.payload["reason"] == "Diabetes management"

    def test_get_diagnoses(self) -> None:
        """Test getting all diagnosis events."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        timeline.add_diagnosis("E11.9", "Type 2 diabetes")
        timeline.add_diagnosis("I10", "Essential hypertension")
        timeline.add_lab_result("2345-7", "Glucose", "95")  # Not a diagnosis

        # Act
        diagnoses = timeline.get_diagnoses()

        # Assert
        assert len(diagnoses) == 2
        assert all(d.clinical_type == ClinicalEventType.DIAGNOSIS for d in diagnoses)

    def test_get_medications_all(self) -> None:
        """Test getting all medication events."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        timeline.add_medication_start("860975", "Metformin", "500 mg", "PO", "BID")
        timeline.add_medication_start("860975", "Lisinopril", "10 mg", "PO", "QD")

        # Act
        medications = timeline.get_medications(active_only=False)

        # Assert
        assert len(medications) == 2

    def test_get_medications_active_only(self) -> None:
        """Test getting only active medications."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        timeline.add_medication_start("860975", "Metformin", "500 mg", "PO", "BID")
        timeline.add_medication_start("123456", "Lisinopril", "10 mg", "PO", "QD")
        timeline.add_medication_stop("860975", "Metformin")  # Stop Metformin

        # Act
        active_meds = timeline.get_medications(active_only=True)

        # Assert
        assert len(active_meds) == 1
        assert active_meds[0].medication_code == "123456"  # Only Lisinopril

    def test_get_labs(self) -> None:
        """Test getting all lab result events."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        timeline.add_lab_order("2345-7", "Glucose")
        timeline.add_lab_result("2345-7", "Glucose", "95", "mg/dL")
        timeline.add_lab_result("2339-0", "HbA1c", "7.2", "%")

        # Act
        labs = timeline.get_labs()

        # Assert
        assert len(labs) == 2  # Only results, not orders

    def test_get_procedures(self) -> None:
        """Test getting all procedure events."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        timeline.add_procedure("93000", "ECG")
        timeline.add_procedure("71046", "Chest X-ray")
        timeline.add_diagnosis("I10", "Hypertension")  # Not a procedure

        # Act
        procedures = timeline.get_procedures()

        # Assert
        assert len(procedures) == 2

    def test_get_vitals(self) -> None:
        """Test getting all vital sign events."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        timeline.add_vital_signs(heart_rate=72, systolic_bp=120, diastolic_bp=80)
        timeline.add_vital_signs(heart_rate=76, systolic_bp=118, diastolic_bp=78)

        # Act
        vitals = timeline.get_vitals()

        # Assert
        assert len(vitals) == 2

    def test_get_encounter_events(self) -> None:
        """Test getting events for a specific encounter."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")
        admission = timeline.add_admission(datetime.now(), encounter_id="ENC001")
        enc_id = admission.encounter_id

        # Add events during encounter
        timeline.add_diagnosis("E11.9", "Diabetes")  # Has encounter_id from current_encounter
        timeline.add_lab_result("2345-7", "Glucose", "95")

        # Discharge
        timeline.add_discharge(datetime.now() + timedelta(hours=4))

        # Add event after discharge (no encounter)
        timeline.add_follow_up(date.today() + timedelta(days=14))

        # Act
        encounter_events = timeline.get_encounter_events(enc_id)

        # Assert
        assert len(encounter_events) >= 3  # Admission, diagnosis, lab
        assert all(e.encounter_id == enc_id for e in encounter_events)

    def test_encounter_id_tracking(self) -> None:
        """Test that encounter ID is correctly tracked."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")

        # Act - Add admission (sets current_encounter_id)
        _admission = timeline.add_admission(datetime.now())
        enc_id = timeline.current_encounter_id

        # Add events during encounter
        diagnosis = timeline.add_diagnosis("E11.9", "Diabetes")

        # Assert - Events should have encounter ID
        assert diagnosis.encounter_id == enc_id

        # Act - Discharge (clears current_encounter_id)
        timeline.add_discharge(datetime.now() + timedelta(hours=4))

        # Add event after discharge
        follow_up = timeline.add_follow_up(date.today() + timedelta(days=14))

        # Assert
        assert timeline.current_encounter_id is None
        assert follow_up.encounter_id is None

    def test_timeline_sorting(self) -> None:
        """Test that events are sorted by timestamp."""
        # Arrange
        timeline = ClinicalTimeline(patient_mrn="MRN12345")

        # Add events out of order
        t3 = datetime(2025, 1, 26, 14, 0)
        t1 = datetime(2025, 1, 26, 8, 0)
        t2 = datetime(2025, 1, 26, 10, 0)

        timeline.add_vital_signs(observation_time=t3)
        timeline.add_lab_result("2345-7", "Glucose", "95", result_time=t1)
        timeline.add_diagnosis("E11.9", "Diabetes", diagnosed_date=t2)

        # Assert - Should be sorted
        events = list(timeline)
        assert len(events) == 3
        # Events should be in chronological order
        timestamps = [e.timestamp or e.scheduled_date for e in events]
        assert timestamps == sorted(timestamps)


class TestClinicalEvent:
    """Tests for ClinicalEvent class."""

    def test_clinical_event_creation(self) -> None:
        """Test creating a clinical event."""
        # Arrange & Act
        event = ClinicalEvent(
            clinical_type=ClinicalEventType.DIAGNOSIS,
            name="Diabetes diagnosis",
            diagnosis_code="E11.9",
            provider_id="DR001",
        )

        # Assert
        assert event.clinical_type == ClinicalEventType.DIAGNOSIS
        assert event.event_type == "diagnosis"  # Set from clinical_type
        assert event.diagnosis_code == "E11.9"
        assert event.status == EventStatus.PENDING

    def test_clinical_event_mark_executed(self) -> None:
        """Test marking event as executed."""
        # Arrange
        event = ClinicalEvent(clinical_type=ClinicalEventType.LAB_ORDER)

        # Act
        event.mark_executed(result={"value": "95"})

        # Assert
        assert event.status == EventStatus.EXECUTED
        assert event.result == {"value": "95"}

    def test_clinical_event_mark_failed(self) -> None:
        """Test marking event as failed."""
        # Arrange
        event = ClinicalEvent(clinical_type=ClinicalEventType.PROCEDURE)

        # Act
        event.mark_failed("Patient refused procedure")

        # Assert
        assert event.status == EventStatus.FAILED
        assert event.error == "Patient refused procedure"
