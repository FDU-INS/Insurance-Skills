"""Tests for HL7v2 message generation."""

from datetime import date, datetime

from healthsim.person import PersonName

from patientsim.core.models import (
    Diagnosis,
    DiagnosisType,
    Encounter,
    EncounterClass,
    EncounterStatus,
    Gender,
    Patient,
)
from patientsim.formats.hl7v2.generator import HL7v2Generator
from patientsim.formats.hl7v2.segments import (
    COMPONENT_SEP,
    FIELD_SEP,
    build_dg1_segment,
    build_evn_segment,
    build_msh_segment,
    build_pid_segment,
    build_pv1_segment,
    escape_hl7,
    format_hl7_date,
    format_hl7_datetime,
)


class TestHL7Utilities:
    """Tests for HL7v2 utility functions."""

    def test_escape_hl7(self) -> None:
        """Test HL7 special character escaping."""
        assert escape_hl7("Normal text") == "Normal text"
        assert escape_hl7("Text|with|pipes") == "Text\\F\\with\\F\\pipes"
        assert escape_hl7("Text^with^carets") == "Text\\S\\with\\S\\carets"
        assert escape_hl7("Text~with~tildes") == "Text\\R\\with\\R\\tildes"

    def test_format_hl7_datetime(self) -> None:
        """Test HL7 datetime formatting."""
        dt = datetime(2024, 1, 15, 14, 30, 45)
        assert format_hl7_datetime(dt) == "20240115143045"

    def test_format_hl7_date(self) -> None:
        """Test HL7 date formatting."""
        dt = date(2024, 1, 15)
        assert format_hl7_date(dt) == "20240115"


class TestMSHSegment:
    """Tests for MSH segment builder."""

    def test_build_msh_segment(self) -> None:
        """Test building MSH segment."""
        timestamp = datetime(2024, 1, 15, 14, 30, 45)
        msh = build_msh_segment(
            message_type="ADT",
            trigger_event="A01",
            message_control_id="MSG001",
            timestamp=timestamp,
        )

        fields = msh.split(FIELD_SEP)

        assert fields[0] == "MSH"
        assert fields[1] == "^~\\&"  # Encoding characters
        assert fields[2] == "PATIENTSIM"  # Sending application
        assert fields[6] == "20240115143045"  # Timestamp
        assert "ADT^A01" in fields[8]  # Message type
        assert fields[9] == "MSG001"  # Control ID
        assert fields[10] == "P"  # Processing ID
        assert fields[11] == "2.5"  # Version

    def test_msh_custom_applications(self) -> None:
        """Test MSH with custom application names."""
        msh = build_msh_segment(
            message_type="ADT",
            trigger_event="A01",
            message_control_id="MSG002",
            timestamp=datetime.now(),
            sending_application="APP1",
            receiving_application="APP2",
        )

        fields = msh.split(FIELD_SEP)
        assert fields[2] == "APP1"
        assert fields[4] == "APP2"


class TestEVNSegment:
    """Tests for EVN segment builder."""

    def test_build_evn_segment(self) -> None:
        """Test building EVN segment."""
        timestamp = datetime(2024, 1, 15, 10, 30)
        evn = build_evn_segment(
            event_type="A01",
            event_timestamp=timestamp,
        )

        fields = evn.split(FIELD_SEP)

        assert fields[0] == "EVN"
        assert fields[1] == "A01"  # Event type
        assert fields[2] == "20240115103000"  # Event timestamp

    def test_evn_with_reason_code(self) -> None:
        """Test EVN segment with event reason code."""
        evn = build_evn_segment(
            event_type="A03",
            event_timestamp=datetime.now(),
            event_reason_code="01",
        )

        fields = evn.split(FIELD_SEP)
        assert fields[4] == "01"  # Event reason code (EVN-4)


class TestPIDSegment:
    """Tests for PID segment builder."""

    def test_build_pid_segment(self) -> None:
        """Test building PID segment."""
        patient = Patient(
            id="patient-001",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        pid = build_pid_segment(patient)
        fields = pid.split(FIELD_SEP)

        assert fields[0] == "PID"
        assert fields[1] == "1"  # Set ID
        assert fields[3] == "MRN12345"  # Patient ID
        assert f"Doe{COMPONENT_SEP}John" in fields[5]  # Patient name
        assert fields[7] == "19590315"  # Birth date
        assert fields[8] == "M"  # Gender

    def test_pid_deceased_patient(self) -> None:
        """Test PID segment for deceased patient."""
        patient = Patient(
            id="patient-002",
            mrn="MRN99999",
            name=PersonName(given_name="Jane", family_name="Smith"),
            birth_date=date(1952, 7, 20),
            gender=Gender.FEMALE,
            deceased=True,
            death_date=date(2024, 1, 15),
        )

        pid = build_pid_segment(patient)
        fields = pid.split(FIELD_SEP)

        # Check deceased indicator (PID-30, but might be beyond basic fields)
        assert "20240115" in pid  # Death date should be in the segment
        assert fields[8] == "F"  # Gender


class TestPV1Segment:
    """Tests for PV1 segment builder."""

    def test_build_pv1_segment(self) -> None:
        """Test building PV1 segment."""
        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN12345",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
            discharge_time=datetime(2024, 1, 18, 14, 0),
        )

        pv1 = build_pv1_segment(encounter)
        fields = pv1.split(FIELD_SEP)

        assert fields[0] == "PV1"
        assert fields[1] == "1"  # Set ID
        assert fields[2] == "E"  # Patient class (Emergency)
        assert fields[19] == "ENC001"  # Visit number
        assert fields[44] == "20240115103000"  # Admit datetime
        assert fields[45] == "20240118140000"  # Discharge datetime

    def test_pv1_inpatient(self) -> None:
        """Test PV1 for inpatient encounter."""
        encounter = Encounter(
            encounter_id="ENC002",
            patient_mrn="MRN12345",
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.IN_PROGRESS,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        pv1 = build_pv1_segment(encounter)
        fields = pv1.split(FIELD_SEP)

        assert fields[2] == "I"  # Patient class (Inpatient - PV1-2)
        assert fields[4] == "1"  # Admission type (Emergency - PV1-4)


class TestDG1Segment:
    """Tests for DG1 segment builder."""

    def test_build_dg1_segment(self) -> None:
        """Test building DG1 segment."""
        dg1 = build_dg1_segment(
            diagnosis_code="A41.9",
            diagnosis_text="Sepsis, unspecified organism",
            set_id=1,
            diagnosis_type="F",
        )

        fields = dg1.split(FIELD_SEP)

        assert fields[0] == "DG1"
        assert fields[1] == "1"  # Set ID
        assert "A41.9" in fields[3]  # Diagnosis code
        assert "Sepsis" in fields[3]  # Diagnosis text
        assert "I10" in fields[3]  # ICD-10 code system
        assert fields[6] == "F"  # Diagnosis type


class TestADTA01Message:
    """Tests for ADT^A01 message generation."""

    def test_generate_adt_a01(self) -> None:
        """Test generating ADT^A01 admission message."""
        patient = Patient(
            id="patient-003",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN12345",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        generator = HL7v2Generator()
        message = generator.generate_adt_a01(patient, encounter)

        # Split into segments
        segments = message.split("\r")

        # Should have at least MSH, EVN, PID, PV1
        assert len(segments) >= 4

        # Check segment types
        assert segments[0].startswith("MSH")
        assert segments[1].startswith("EVN")
        assert segments[2].startswith("PID")
        assert segments[3].startswith("PV1")

        # Check message type in MSH
        assert "ADT^A01" in segments[0]

        # Check patient name in PID
        assert "Doe^John" in segments[2]

        # Check encounter ID in PV1
        assert "ENC001" in segments[3]

    def test_adt_a01_with_diagnoses(self) -> None:
        """Test ADT^A01 with diagnosis segments."""
        patient = Patient(
            id="patient-004",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN12345",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        diagnoses = [
            Diagnosis(
                code="A41.9",
                description="Sepsis",
                type=DiagnosisType.FINAL,
                patient_mrn="MRN12345",
                encounter_id="ENC001",
                diagnosed_date=date(2024, 1, 15),
            ),
        ]

        generator = HL7v2Generator()
        message = generator.generate_adt_a01(patient, encounter, diagnoses=diagnoses)

        segments = message.split("\r")

        # Should have MSH, EVN, PID, PV1, DG1
        assert len(segments) >= 5

        # Check for DG1 segment
        dg1_segments = [s for s in segments if s.startswith("DG1")]
        assert len(dg1_segments) == 1
        assert "A41.9" in dg1_segments[0]


class TestADTA03Message:
    """Tests for ADT^A03 message generation."""

    def test_generate_adt_a03(self) -> None:
        """Test generating ADT^A03 discharge message."""
        patient = Patient(
            id="patient-005",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN12345",
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
            discharge_time=datetime(2024, 1, 18, 14, 0),
            discharge_disposition="HOME",
        )

        generator = HL7v2Generator()
        message = generator.generate_adt_a03(patient, encounter)

        segments = message.split("\r")

        # Check message type
        assert "ADT^A03" in segments[0]

        # Check EVN event type
        assert "|A03|" in segments[1]

        # Check discharge disposition in PV1
        pv1_segment = [s for s in segments if s.startswith("PV1")][0]
        assert "01" in pv1_segment  # HOME disposition code


class TestADTA08Message:
    """Tests for ADT^A08 message generation."""

    def test_generate_adt_a08(self) -> None:
        """Test generating ADT^A08 update message."""
        patient = Patient(
            id="patient-006",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN12345",
            class_code=EncounterClass.INPATIENT,
            status=EncounterStatus.IN_PROGRESS,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        generator = HL7v2Generator()
        message = generator.generate_adt_a08(patient, encounter)

        segments = message.split("\r")

        # Check message type
        assert "ADT^A08" in segments[0]

        # Check EVN event type
        assert "|A08|" in segments[1]


class TestMessageStructure:
    """Tests for overall message structure and format."""

    def test_message_has_proper_line_endings(self) -> None:
        """Test that messages use proper HL7 line endings."""
        patient = Patient(
            id="patient-007",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN12345",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        generator = HL7v2Generator()
        message = generator.generate_adt_a01(patient, encounter)

        # Should end with \r
        assert message.endswith("\r")

        # Should have \r between segments
        assert "\r" in message

    def test_message_control_id_unique(self) -> None:
        """Test that each message gets a unique control ID."""
        patient = Patient(
            id="patient-008",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN12345",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        generator = HL7v2Generator()
        msg1 = generator.generate_adt_a01(patient, encounter)
        msg2 = generator.generate_adt_a01(patient, encounter)

        # Extract message control IDs from MSH-10
        msh1 = msg1.split("\r")[0]
        msh2 = msg2.split("\r")[0]

        control_id1 = msh1.split(FIELD_SEP)[9]
        control_id2 = msh2.split(FIELD_SEP)[9]

        # Should be different
        assert control_id1 != control_id2

    def test_custom_facility_names(self) -> None:
        """Test generator with custom facility names."""
        patient = Patient(
            id="patient-009",
            mrn="MRN12345",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1959, 3, 15),
            gender=Gender.MALE,
        )

        encounter = Encounter(
            encounter_id="ENC001",
            patient_mrn="MRN12345",
            class_code=EncounterClass.EMERGENCY,
            status=EncounterStatus.FINISHED,
            admission_time=datetime(2024, 1, 15, 10, 30),
        )

        generator = HL7v2Generator(
            sending_application="MYAPP",
            sending_facility="MYFAC",
        )
        message = generator.generate_adt_a01(patient, encounter)

        msh = message.split("\r")[0]
        fields = msh.split(FIELD_SEP)

        assert fields[2] == "MYAPP"
        assert fields[3] == "MYFAC"
