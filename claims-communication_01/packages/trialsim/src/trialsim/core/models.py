"""Core data models for TrialSim.

These models represent the fundamental entities in clinical trials:
subjects, sites, protocols, visits, adverse events, and exposures.
"""

from datetime import date, datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class ArmType(str, Enum):
    """Treatment arm types."""
    TREATMENT = "treatment"
    PLACEBO = "placebo"
    ACTIVE_COMPARATOR = "active_comparator"
    NO_INTERVENTION = "no_intervention"


class SubjectStatus(str, Enum):
    """Subject enrollment status."""
    SCREENING = "screening"
    SCREEN_FAILED = "screen_failed"
    ENROLLED = "enrolled"
    RANDOMIZED = "randomized"
    ON_TREATMENT = "on_treatment"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"
    LOST_TO_FOLLOWUP = "lost_to_followup"


class VisitType(str, Enum):
    """Visit classification."""
    SCREENING = "screening"
    BASELINE = "baseline"
    RANDOMIZATION = "randomization"
    SCHEDULED = "scheduled"
    UNSCHEDULED = "unscheduled"
    EARLY_TERMINATION = "early_termination"
    FOLLOW_UP = "follow_up"
    END_OF_STUDY = "end_of_study"


class AESeverity(str, Enum):
    """Adverse event severity (CTCAE grading)."""
    GRADE_1 = "grade_1_mild"
    GRADE_2 = "grade_2_moderate"
    GRADE_3 = "grade_3_severe"
    GRADE_4 = "grade_4_life_threatening"
    GRADE_5 = "grade_5_death"


class AECausality(str, Enum):
    """Adverse event causality assessment."""
    NOT_RELATED = "not_related"
    UNLIKELY = "unlikely"
    POSSIBLY = "possibly"
    PROBABLY = "probably"
    DEFINITELY = "definitely"


class AEOutcome(str, Enum):
    """Adverse event outcome."""
    RECOVERED = "recovered"
    RECOVERING = "recovering"
    NOT_RECOVERED = "not_recovered"
    RECOVERED_WITH_SEQUELAE = "recovered_with_sequelae"
    FATAL = "fatal"
    UNKNOWN = "unknown"


class Site(BaseModel):
    """Clinical trial site."""
    site_id: str = Field(default_factory=lambda: f"SITE-{uuid4().hex[:8].upper()}")
    name: str
    country: str = "USA"
    region: str | None = None
    principal_investigator: str | None = None
    is_active: bool = True
    activation_date: date | None = None
    
    model_config = {"frozen": False}


class Protocol(BaseModel):
    """Clinical trial protocol definition."""
    protocol_id: str
    study_title: str
    phase: str = "Phase 3"  # Phase 1, 2, 3, 4
    therapeutic_area: str = "Oncology"
    indication: str | None = None
    sponsor: str | None = None
    arms: list[dict[str, Any]] = Field(default_factory=list)
    planned_enrollment: int = 100
    duration_weeks: int = 52
    visit_schedule: list[dict[str, Any]] = Field(default_factory=list)
    
    model_config = {"frozen": False}


class Subject(BaseModel):
    """Clinical trial subject."""
    subject_id: str = Field(default_factory=lambda: f"SUBJ-{uuid4().hex[:8].upper()}")
    protocol_id: str
    site_id: str
    
    # Demographics
    age: int
    sex: str = "M"
    race: str | None = None
    ethnicity: str | None = None
    
    # Enrollment
    screening_date: date | None = None
    randomization_date: date | None = None
    arm: ArmType | None = None
    status: SubjectStatus = SubjectStatus.SCREENING
    
    # Identifiers
    patient_id: str | None = None  # Link to PatientSim patient
    
    model_config = {"frozen": False}


class Visit(BaseModel):
    """Clinical trial visit record."""
    visit_id: str = Field(default_factory=lambda: f"VST-{uuid4().hex[:8].upper()}")
    subject_id: str
    protocol_id: str
    site_id: str
    
    visit_number: int
    visit_name: str  # e.g., "Screening", "Week 4", "End of Study"
    visit_type: VisitType = VisitType.SCHEDULED
    
    planned_date: date | None = None
    actual_date: date | None = None
    visit_status: str = "scheduled"  # scheduled, completed, missed
    
    # Assessments performed
    assessments: list[str] = Field(default_factory=list)
    
    model_config = {"frozen": False}


class AdverseEvent(BaseModel):
    """Adverse event record."""
    ae_id: str = Field(default_factory=lambda: f"AE-{uuid4().hex[:8].upper()}")
    subject_id: str
    protocol_id: str
    
    # Event details
    ae_term: str  # Preferred term
    ae_description: str | None = None
    system_organ_class: str | None = None  # SOC
    
    # Timing
    onset_date: date
    resolution_date: date | None = None
    duration_days: int | None = None
    
    # Severity and causality
    severity: AESeverity = AESeverity.GRADE_1
    is_serious: bool = False
    causality: AECausality = AECausality.POSSIBLY
    outcome: AEOutcome = AEOutcome.RECOVERED
    
    # Actions
    action_taken: str | None = None  # e.g., "dose_reduced", "drug_withdrawn"
    treatment_required: bool = False
    
    model_config = {"frozen": False}


class Exposure(BaseModel):
    """Drug exposure record."""
    exposure_id: str = Field(default_factory=lambda: f"EXP-{uuid4().hex[:8].upper()}")
    subject_id: str
    protocol_id: str
    
    # Drug information
    drug_name: str
    drug_code: str | None = None
    dose: float
    dose_unit: str = "mg"
    route: str = "oral"  # oral, iv, sc, im
    
    # Timing
    start_date: date
    end_date: date | None = None
    
    # Compliance
    doses_planned: int = 1
    doses_taken: int = 1
    compliance_pct: float = 100.0
    
    model_config = {"frozen": False}
