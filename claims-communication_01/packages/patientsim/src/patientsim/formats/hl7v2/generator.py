"""HL7v2 message generator.

Generates HL7v2 ADT messages from PatientSim objects.
"""

import uuid
from datetime import datetime

from patientsim.core.models import Diagnosis, Encounter, Patient
from patientsim.formats.hl7v2.segments import (
    build_dg1_segment,
    build_evn_segment,
    build_msh_segment,
    build_pid_segment,
    build_pv1_segment,
)


class HL7v2Generator:
    """Generates HL7v2 messages from PatientSim objects.

    Example:
        >>> generator = HL7v2Generator()
        >>> message = generator.generate_adt_a01(patient, encounter)
        >>> print(message)
    """

    def __init__(
        self,
        sending_application: str = "PATIENTSIM",
        sending_facility: str = "HOSPITAL",
        receiving_application: str = "EMR",
        receiving_facility: str = "HOSPITAL",
    ) -> None:
        """Initialize message generator.

        Args:
            sending_application: Name of sending application
            sending_facility: Name of sending facility
            receiving_application: Name of receiving application
            receiving_facility: Name of receiving facility
        """
        self.sending_application = sending_application
        self.sending_facility = sending_facility
        self.receiving_application = receiving_application
        self.receiving_facility = receiving_facility

    def _generate_message_control_id(self) -> str:
        """Generate a unique message control ID.

        Returns:
            Message control ID
        """
        return str(uuid.uuid4())[:20].replace("-", "").upper()

    def _build_message(self, segments: list[str]) -> str:
        """Build complete HL7v2 message from segments.

        Args:
            segments: List of segment strings

        Returns:
            Complete HL7v2 message with proper line endings
        """
        return "\r".join(segments) + "\r"

    def generate_adt_a01(
        self,
        patient: Patient,
        encounter: Encounter,
        diagnoses: list[Diagnosis] | None = None,
        timestamp: datetime | None = None,
    ) -> str:
        """Generate ADT^A01 (Admit/visit notification) message.

        Args:
            patient: Patient object
            encounter: Encounter object
            diagnoses: Optional list of diagnoses
            timestamp: Message timestamp (defaults to now)

        Returns:
            HL7v2 ADT^A01 message
        """
        timestamp = timestamp or datetime.now()
        event_timestamp = encounter.admission_time or timestamp
        message_control_id = self._generate_message_control_id()

        segments = []

        # MSH - Message Header
        msh = build_msh_segment(
            message_type="ADT",
            trigger_event="A01",
            message_control_id=message_control_id,
            timestamp=timestamp,
            sending_application=self.sending_application,
            sending_facility=self.sending_facility,
            receiving_application=self.receiving_application,
            receiving_facility=self.receiving_facility,
        )
        segments.append(msh)

        # EVN - Event Type
        evn = build_evn_segment(
            event_type="A01",
            event_timestamp=event_timestamp,
        )
        segments.append(evn)

        # PID - Patient Identification
        pid = build_pid_segment(patient)
        segments.append(pid)

        # PV1 - Patient Visit
        pv1 = build_pv1_segment(encounter)
        segments.append(pv1)

        # DG1 - Diagnosis (optional)
        if diagnoses:
            for idx, diagnosis in enumerate(diagnoses, start=1):
                dg1 = build_dg1_segment(
                    diagnosis_code=diagnosis.code,
                    diagnosis_text=diagnosis.description,
                    set_id=idx,
                    diagnosis_type="F" if diagnosis.type == "final" else "W",
                )
                segments.append(dg1)

        return self._build_message(segments)

    def generate_adt_a03(
        self,
        patient: Patient,
        encounter: Encounter,
        diagnoses: list[Diagnosis] | None = None,
        timestamp: datetime | None = None,
    ) -> str:
        """Generate ADT^A03 (Discharge/end visit) message.

        Args:
            patient: Patient object
            encounter: Encounter object
            diagnoses: Optional list of diagnoses
            timestamp: Message timestamp (defaults to now)

        Returns:
            HL7v2 ADT^A03 message
        """
        timestamp = timestamp or datetime.now()
        event_timestamp = encounter.discharge_time or timestamp
        message_control_id = self._generate_message_control_id()

        segments = []

        # MSH - Message Header
        msh = build_msh_segment(
            message_type="ADT",
            trigger_event="A03",
            message_control_id=message_control_id,
            timestamp=timestamp,
            sending_application=self.sending_application,
            sending_facility=self.sending_facility,
            receiving_application=self.receiving_application,
            receiving_facility=self.receiving_facility,
        )
        segments.append(msh)

        # EVN - Event Type
        evn = build_evn_segment(
            event_type="A03",
            event_timestamp=event_timestamp,
        )
        segments.append(evn)

        # PID - Patient Identification
        pid = build_pid_segment(patient)
        segments.append(pid)

        # PV1 - Patient Visit
        pv1 = build_pv1_segment(encounter)
        segments.append(pv1)

        # DG1 - Diagnosis (optional)
        if diagnoses:
            for idx, diagnosis in enumerate(diagnoses, start=1):
                dg1 = build_dg1_segment(
                    diagnosis_code=diagnosis.code,
                    diagnosis_text=diagnosis.description,
                    set_id=idx,
                    diagnosis_type="F",  # Final diagnosis at discharge
                )
                segments.append(dg1)

        return self._build_message(segments)

    def generate_adt_a08(
        self,
        patient: Patient,
        encounter: Encounter,
        diagnoses: list[Diagnosis] | None = None,
        timestamp: datetime | None = None,
    ) -> str:
        """Generate ADT^A08 (Update patient information) message.

        Args:
            patient: Patient object
            encounter: Encounter object
            diagnoses: Optional list of diagnoses
            timestamp: Message timestamp (defaults to now)

        Returns:
            HL7v2 ADT^A08 message
        """
        timestamp = timestamp or datetime.now()
        message_control_id = self._generate_message_control_id()

        segments = []

        # MSH - Message Header
        msh = build_msh_segment(
            message_type="ADT",
            trigger_event="A08",
            message_control_id=message_control_id,
            timestamp=timestamp,
            sending_application=self.sending_application,
            sending_facility=self.sending_facility,
            receiving_application=self.receiving_application,
            receiving_facility=self.receiving_facility,
        )
        segments.append(msh)

        # EVN - Event Type
        evn = build_evn_segment(
            event_type="A08",
            event_timestamp=timestamp,
        )
        segments.append(evn)

        # PID - Patient Identification
        pid = build_pid_segment(patient)
        segments.append(pid)

        # PV1 - Patient Visit
        pv1 = build_pv1_segment(encounter)
        segments.append(pv1)

        # DG1 - Diagnosis (optional)
        if diagnoses:
            for idx, diagnosis in enumerate(diagnoses, start=1):
                dg1 = build_dg1_segment(
                    diagnosis_code=diagnosis.code,
                    diagnosis_text=diagnosis.description,
                    set_id=idx,
                    diagnosis_type="F" if diagnosis.type == "final" else "W",
                )
                segments.append(dg1)

        return self._build_message(segments)
