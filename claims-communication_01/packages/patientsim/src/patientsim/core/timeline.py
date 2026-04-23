"""Clinical timeline management for patient care events.

This module extends healthsim.temporal.Timeline with healthcare-specific
event types and management capabilities.
"""

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any

from healthsim.temporal import EventDelay, Timeline, TimelineEvent


class ClinicalEventType(str, Enum):
    """Types of clinical events in a patient's care journey."""

    # Encounters
    ADMISSION = "admission"
    DISCHARGE = "discharge"
    TRANSFER = "transfer"

    # Diagnostics
    DIAGNOSIS = "diagnosis"
    LAB_ORDER = "lab_order"
    LAB_RESULT = "lab_result"
    IMAGING_ORDER = "imaging_order"
    IMAGING_RESULT = "imaging_result"

    # Treatment
    MEDICATION_START = "medication_start"
    MEDICATION_STOP = "medication_stop"
    PROCEDURE = "procedure"
    SURGERY = "surgery"

    # Assessment
    VITAL_SIGNS = "vital_signs"
    ASSESSMENT = "assessment"
    CONSULTATION = "consultation"

    # Documentation
    NOTE = "note"
    CARE_PLAN = "care_plan"

    # Follow-up
    FOLLOW_UP = "follow_up"
    REFERRAL = "referral"


@dataclass
class ClinicalEvent(TimelineEvent[dict[str, Any]]):
    """A clinical event with healthcare-specific metadata.

    Extends TimelineEvent with clinical context like provider, location,
    and associated clinical data references.
    """

    # Clinical context
    clinical_type: ClinicalEventType | None = None
    provider_id: str | None = None
    location: str | None = None
    department: str | None = None

    # References to clinical data
    encounter_id: str | None = None
    diagnosis_code: str | None = None
    procedure_code: str | None = None
    medication_code: str | None = None
    lab_code: str | None = None

    # Clinical notes
    clinical_notes: str | None = None

    def __post_init__(self) -> None:
        """Initialize event type from clinical type if not set."""
        super().__post_init__()
        if self.clinical_type and not self.event_type:
            self.event_type = self.clinical_type.value


@dataclass
class ClinicalTimeline(Timeline[dict[str, Any]]):
    """Timeline specialized for clinical events in patient care.

    Extends the base Timeline with healthcare-specific methods for managing
    encounters, diagnoses, labs, medications, and other clinical events.

    Example:
        >>> timeline = ClinicalTimeline(patient_mrn="MRN12345")
        >>> timeline.add_admission(datetime.now(), facility="General Hospital")
        >>> timeline.add_diagnosis("E11.9", "Type 2 Diabetes")
        >>> timeline.add_lab_order("2345-7", "Glucose")
    """

    # Patient reference
    patient_mrn: str = ""

    # Active encounter tracking
    current_encounter_id: str | None = None

    def add_clinical_event(
        self,
        event_type: ClinicalEventType,
        scheduled_date: date | datetime | None = None,
        delay: EventDelay | None = None,
        **kwargs: Any,
    ) -> ClinicalEvent:
        """Add a clinical event to the timeline.

        Args:
            event_type: Type of clinical event
            scheduled_date: When the event occurs
            delay: Optional delay configuration
            **kwargs: Additional event attributes

        Returns:
            The created ClinicalEvent
        """
        event = ClinicalEvent(
            clinical_type=event_type,
            event_type=event_type.value,
            name=kwargs.pop("name", event_type.value),
            scheduled_date=scheduled_date,
            delay_from_previous=delay or EventDelay(),
            **kwargs,
        )
        self.add_event(event)
        return event

    def add_admission(
        self,
        admission_time: datetime,
        encounter_id: str | None = None,
        facility: str | None = None,
        department: str | None = None,
        chief_complaint: str | None = None,
    ) -> ClinicalEvent:
        """Add an admission event.

        Args:
            admission_time: When patient was admitted
            encounter_id: Unique encounter identifier
            facility: Hospital/facility name
            department: Department/unit
            chief_complaint: Patient's chief complaint

        Returns:
            The created admission event
        """
        enc_id = encounter_id or f"ENC-{len(self.events):06d}"
        self.current_encounter_id = enc_id

        return self.add_clinical_event(
            ClinicalEventType.ADMISSION,
            scheduled_date=admission_time,
            name=f"Admission - {chief_complaint or 'Unspecified'}",
            encounter_id=enc_id,
            location=facility,
            department=department,
            payload={"chief_complaint": chief_complaint},
        )

    def add_discharge(
        self,
        discharge_time: datetime,
        disposition: str | None = None,
        discharge_diagnosis: str | None = None,
    ) -> ClinicalEvent:
        """Add a discharge event.

        Args:
            discharge_time: When patient was discharged
            disposition: Where patient went (home, SNF, etc.)
            discharge_diagnosis: Primary discharge diagnosis

        Returns:
            The created discharge event
        """
        event = self.add_clinical_event(
            ClinicalEventType.DISCHARGE,
            scheduled_date=discharge_time,
            name=f"Discharge - {disposition or 'Home'}",
            encounter_id=self.current_encounter_id,
            payload={
                "disposition": disposition,
                "discharge_diagnosis": discharge_diagnosis,
            },
        )
        self.current_encounter_id = None
        return event

    def add_diagnosis(
        self,
        diagnosis_code: str,
        description: str,
        diagnosed_date: date | datetime | None = None,
        provider_id: str | None = None,
    ) -> ClinicalEvent:
        """Add a diagnosis event.

        Args:
            diagnosis_code: ICD-10 code
            description: Diagnosis description
            diagnosed_date: When diagnosis was made
            provider_id: Provider who made the diagnosis

        Returns:
            The created diagnosis event
        """
        return self.add_clinical_event(
            ClinicalEventType.DIAGNOSIS,
            scheduled_date=diagnosed_date or datetime.now(),
            name=f"Diagnosis: {description}",
            diagnosis_code=diagnosis_code,
            provider_id=provider_id,
            encounter_id=self.current_encounter_id,
            payload={"description": description},
        )

    def add_lab_order(
        self,
        lab_code: str,
        test_name: str,
        order_time: datetime | None = None,
        provider_id: str | None = None,
    ) -> ClinicalEvent:
        """Add a lab order event.

        Args:
            lab_code: LOINC code
            test_name: Name of the test
            order_time: When lab was ordered
            provider_id: Ordering provider

        Returns:
            The created lab order event
        """
        return self.add_clinical_event(
            ClinicalEventType.LAB_ORDER,
            scheduled_date=order_time or datetime.now(),
            name=f"Lab Order: {test_name}",
            lab_code=lab_code,
            provider_id=provider_id,
            encounter_id=self.current_encounter_id,
            payload={"test_name": test_name},
        )

    def add_lab_result(
        self,
        lab_code: str,
        test_name: str,
        value: str,
        unit: str | None = None,
        result_time: datetime | None = None,
        abnormal_flag: str | None = None,
    ) -> ClinicalEvent:
        """Add a lab result event.

        Args:
            lab_code: LOINC code
            test_name: Name of the test
            value: Result value
            unit: Unit of measurement
            result_time: When result was finalized
            abnormal_flag: Abnormality indicator (H, L, etc.)

        Returns:
            The created lab result event
        """
        return self.add_clinical_event(
            ClinicalEventType.LAB_RESULT,
            scheduled_date=result_time or datetime.now(),
            name=f"Lab Result: {test_name} = {value} {unit or ''}".strip(),
            lab_code=lab_code,
            encounter_id=self.current_encounter_id,
            payload={
                "test_name": test_name,
                "value": value,
                "unit": unit,
                "abnormal_flag": abnormal_flag,
            },
        )

    def add_medication_start(
        self,
        medication_code: str,
        medication_name: str,
        dose: str,
        route: str,
        frequency: str,
        start_time: datetime | None = None,
        provider_id: str | None = None,
        indication: str | None = None,
    ) -> ClinicalEvent:
        """Add a medication start event.

        Args:
            medication_code: RxNorm code
            medication_name: Name of medication
            dose: Dose amount
            route: Route of administration
            frequency: Dosing frequency
            start_time: When medication started
            provider_id: Prescribing provider
            indication: Reason for medication

        Returns:
            The created medication start event
        """
        return self.add_clinical_event(
            ClinicalEventType.MEDICATION_START,
            scheduled_date=start_time or datetime.now(),
            name=f"Start Med: {medication_name} {dose} {route} {frequency}",
            medication_code=medication_code,
            provider_id=provider_id,
            encounter_id=self.current_encounter_id,
            payload={
                "medication_name": medication_name,
                "dose": dose,
                "route": route,
                "frequency": frequency,
                "indication": indication,
            },
        )

    def add_medication_stop(
        self,
        medication_code: str,
        medication_name: str,
        stop_time: datetime | None = None,
        reason: str | None = None,
    ) -> ClinicalEvent:
        """Add a medication stop event.

        Args:
            medication_code: RxNorm code
            medication_name: Name of medication
            stop_time: When medication was stopped
            reason: Reason for stopping

        Returns:
            The created medication stop event
        """
        return self.add_clinical_event(
            ClinicalEventType.MEDICATION_STOP,
            scheduled_date=stop_time or datetime.now(),
            name=f"Stop Med: {medication_name}",
            medication_code=medication_code,
            encounter_id=self.current_encounter_id,
            payload={"medication_name": medication_name, "reason": reason},
        )

    def add_procedure(
        self,
        procedure_code: str,
        description: str,
        procedure_time: datetime | None = None,
        provider_id: str | None = None,
        location: str | None = None,
    ) -> ClinicalEvent:
        """Add a procedure event.

        Args:
            procedure_code: CPT or ICD-10-PCS code
            description: Procedure description
            procedure_time: When procedure was performed
            provider_id: Performing provider
            location: Where procedure was performed

        Returns:
            The created procedure event
        """
        return self.add_clinical_event(
            ClinicalEventType.PROCEDURE,
            scheduled_date=procedure_time or datetime.now(),
            name=f"Procedure: {description}",
            procedure_code=procedure_code,
            provider_id=provider_id,
            location=location,
            encounter_id=self.current_encounter_id,
            payload={"description": description},
        )

    def add_vital_signs(
        self,
        observation_time: datetime | None = None,
        temperature: float | None = None,
        heart_rate: int | None = None,
        respiratory_rate: int | None = None,
        systolic_bp: int | None = None,
        diastolic_bp: int | None = None,
        spo2: int | None = None,
    ) -> ClinicalEvent:
        """Add a vital signs event.

        Args:
            observation_time: When vitals were taken
            temperature: Temperature in Fahrenheit
            heart_rate: Heart rate in bpm
            respiratory_rate: Respiratory rate per minute
            systolic_bp: Systolic blood pressure
            diastolic_bp: Diastolic blood pressure
            spo2: Oxygen saturation percentage

        Returns:
            The created vital signs event
        """
        bp_str = f"{systolic_bp}/{diastolic_bp}" if systolic_bp and diastolic_bp else ""

        return self.add_clinical_event(
            ClinicalEventType.VITAL_SIGNS,
            scheduled_date=observation_time or datetime.now(),
            name=f"Vitals: HR={heart_rate or '?'} BP={bp_str or '?'}",
            encounter_id=self.current_encounter_id,
            payload={
                "temperature": temperature,
                "heart_rate": heart_rate,
                "respiratory_rate": respiratory_rate,
                "systolic_bp": systolic_bp,
                "diastolic_bp": diastolic_bp,
                "spo2": spo2,
            },
        )

    def add_note(
        self,
        note_type: str,
        text: str,
        note_time: datetime | None = None,
        author: str | None = None,
    ) -> ClinicalEvent:
        """Add a clinical note event.

        Args:
            note_type: Type of note (Progress Note, H&P, etc.)
            text: Note content
            note_time: When note was written
            author: Author of the note

        Returns:
            The created note event
        """
        return self.add_clinical_event(
            ClinicalEventType.NOTE,
            scheduled_date=note_time or datetime.now(),
            name=f"Note: {note_type}",
            provider_id=author,
            clinical_notes=text,
            encounter_id=self.current_encounter_id,
            payload={"note_type": note_type, "text": text},
        )

    def add_follow_up(
        self,
        follow_up_date: date | datetime,
        reason: str | None = None,
        provider_id: str | None = None,
    ) -> ClinicalEvent:
        """Add a follow-up appointment event.

        Args:
            follow_up_date: Scheduled follow-up date
            reason: Reason for follow-up
            provider_id: Provider to follow up with

        Returns:
            The created follow-up event
        """
        return self.add_clinical_event(
            ClinicalEventType.FOLLOW_UP,
            scheduled_date=follow_up_date,
            name=f"Follow-up: {reason or 'General'}",
            provider_id=provider_id,
            payload={"reason": reason},
        )

    # Query methods specific to clinical events

    def get_diagnoses(self) -> list[ClinicalEvent]:
        """Get all diagnosis events."""
        return [
            e
            for e in self.events
            if isinstance(e, ClinicalEvent) and e.clinical_type == ClinicalEventType.DIAGNOSIS
        ]

    def get_medications(self, active_only: bool = False) -> list[ClinicalEvent]:
        """Get medication events.

        Args:
            active_only: If True, only return medications without a stop event

        Returns:
            List of medication events
        """
        starts = [
            e
            for e in self.events
            if isinstance(e, ClinicalEvent)
            and e.clinical_type == ClinicalEventType.MEDICATION_START
        ]

        if not active_only:
            return starts

        # Find stopped medications
        stopped_codes = {
            e.medication_code
            for e in self.events
            if isinstance(e, ClinicalEvent) and e.clinical_type == ClinicalEventType.MEDICATION_STOP
        }

        return [e for e in starts if e.medication_code not in stopped_codes]

    def get_labs(self) -> list[ClinicalEvent]:
        """Get all lab result events."""
        return [
            e
            for e in self.events
            if isinstance(e, ClinicalEvent) and e.clinical_type == ClinicalEventType.LAB_RESULT
        ]

    def get_procedures(self) -> list[ClinicalEvent]:
        """Get all procedure events."""
        return [
            e
            for e in self.events
            if isinstance(e, ClinicalEvent) and e.clinical_type == ClinicalEventType.PROCEDURE
        ]

    def get_vitals(self) -> list[ClinicalEvent]:
        """Get all vital sign events."""
        return [
            e
            for e in self.events
            if isinstance(e, ClinicalEvent) and e.clinical_type == ClinicalEventType.VITAL_SIGNS
        ]

    def get_encounter_events(self, encounter_id: str) -> list[ClinicalEvent]:
        """Get all events for a specific encounter.

        Args:
            encounter_id: The encounter ID to filter by

        Returns:
            List of events for that encounter
        """
        return [
            e
            for e in self.events
            if isinstance(e, ClinicalEvent) and e.encounter_id == encounter_id
        ]
