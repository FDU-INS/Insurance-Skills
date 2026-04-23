"""Generators for clinical trial entities.

Provides generators for creating synthetic trial data including
subjects, visits, adverse events, and drug exposures.
"""

import random
from datetime import date, timedelta
from typing import Any

from faker import Faker

from trialsim.core.models import (
    AdverseEvent,
    AECausality,
    AEOutcome,
    AESeverity,
    ArmType,
    Exposure,
    Subject,
    SubjectStatus,
    Visit,
    VisitType,
)


class TrialSubjectGenerator:
    """Generate synthetic trial subjects."""
    
    def __init__(self, seed: int | None = None):
        """Initialize generator with optional seed for reproducibility."""
        self.seed = seed
        self.random = random.Random(seed)
        self.faker = Faker()
        if seed is not None:
            Faker.seed(seed)
    
    def generate(
        self,
        protocol_id: str = "PROTO-001",
        site_id: str = "SITE-001",
        arm: ArmType | None = None,
        **kwargs: Any,
    ) -> Subject:
        """Generate a single trial subject."""
        age = kwargs.get("age", self.random.randint(18, 75))
        sex = kwargs.get("sex", self.random.choice(["M", "F"]))
        
        races = ["White", "Black", "Asian", "American Indian", "Pacific Islander", "Other"]
        ethnicities = ["Hispanic or Latino", "Not Hispanic or Latino"]
        
        return Subject(
            protocol_id=protocol_id,
            site_id=site_id,
            age=age,
            sex=sex,
            race=self.random.choice(races),
            ethnicity=self.random.choice(ethnicities),
            arm=arm,
            status=SubjectStatus.SCREENING,
        )
    
    def generate_many(
        self,
        count: int,
        protocol_id: str = "PROTO-001",
        sites: list[str] | None = None,
        arms: list[str] | None = None,
        **kwargs: Any,
    ) -> list[Subject]:
        """Generate multiple trial subjects."""
        if sites is None:
            sites = ["SITE-001"]
        
        subjects = []
        for i in range(count):
            site_id = self.random.choice(sites)
            arm = None
            if arms:
                arm_str = self.random.choice(arms)
                arm = ArmType(arm_str) if arm_str in [a.value for a in ArmType] else None
            
            subject = self.generate(
                protocol_id=protocol_id,
                site_id=site_id,
                arm=arm,
                **kwargs,
            )
            subjects.append(subject)
        
        return subjects


class VisitGenerator:
    """Generate visit records for trial subjects."""
    
    def __init__(self, seed: int | None = None):
        """Initialize generator with optional seed."""
        self.seed = seed
        self.random = random.Random(seed)
    
    def generate_schedule(
        self,
        subject: Subject,
        protocol_phase: str = "phase3",
        duration_weeks: int = 52,
        start_date: date | None = None,
    ) -> list[Visit]:
        """Generate a complete visit schedule for a subject."""
        if start_date is None:
            start_date = date.today()
        
        visits = []
        visit_num = 1
        
        # Screening visit
        visits.append(Visit(
            subject_id=subject.subject_id,
            protocol_id=subject.protocol_id,
            site_id=subject.site_id,
            visit_number=visit_num,
            visit_name="Screening",
            visit_type=VisitType.SCREENING,
            planned_date=start_date,
            actual_date=start_date,
            visit_status="completed",
        ))
        visit_num += 1
        
        # Baseline/Randomization (Day 1)
        baseline_date = start_date + timedelta(days=self.random.randint(7, 21))
        visits.append(Visit(
            subject_id=subject.subject_id,
            protocol_id=subject.protocol_id,
            site_id=subject.site_id,
            visit_number=visit_num,
            visit_name="Baseline/Randomization",
            visit_type=VisitType.RANDOMIZATION,
            planned_date=baseline_date,
            actual_date=baseline_date,
            visit_status="completed",
        ))
        visit_num += 1
        
        # Scheduled visits (typically every 4 weeks for Phase 3)
        visit_interval = 4  # weeks
        current_date = baseline_date
        week = visit_interval
        
        while week <= duration_weeks:
            current_date = baseline_date + timedelta(weeks=week)
            visit_name = f"Week {week}"
            
            # Add some date variation
            actual_offset = self.random.randint(-3, 3)
            actual = current_date + timedelta(days=actual_offset)
            
            visits.append(Visit(
                subject_id=subject.subject_id,
                protocol_id=subject.protocol_id,
                site_id=subject.site_id,
                visit_number=visit_num,
                visit_name=visit_name,
                visit_type=VisitType.SCHEDULED,
                planned_date=current_date,
                actual_date=actual,
                visit_status="completed" if week < 24 else "scheduled",
            ))
            visit_num += 1
            week += visit_interval
        
        # End of Study visit
        eos_date = baseline_date + timedelta(weeks=duration_weeks)
        visits.append(Visit(
            subject_id=subject.subject_id,
            protocol_id=subject.protocol_id,
            site_id=subject.site_id,
            visit_number=visit_num,
            visit_name="End of Study",
            visit_type=VisitType.END_OF_STUDY,
            planned_date=eos_date,
            visit_status="scheduled",
        ))
        
        return visits


class AdverseEventGenerator:
    """Generate adverse events for trial subjects."""
    
    COMMON_AES = [
        ("Headache", "Nervous system disorders"),
        ("Nausea", "Gastrointestinal disorders"),
        ("Fatigue", "General disorders"),
        ("Diarrhea", "Gastrointestinal disorders"),
        ("Rash", "Skin and subcutaneous tissue disorders"),
        ("Arthralgia", "Musculoskeletal disorders"),
        ("Dizziness", "Nervous system disorders"),
        ("Cough", "Respiratory disorders"),
        ("Insomnia", "Psychiatric disorders"),
        ("Back pain", "Musculoskeletal disorders"),
    ]
    
    def __init__(self, seed: int | None = None):
        """Initialize generator with optional seed."""
        self.seed = seed
        self.random = random.Random(seed)
    
    def generate_for_subject(
        self,
        subject: Subject,
        visit_count: int = 10,
        ae_probability: float = 0.3,
    ) -> list[AdverseEvent]:
        """Generate adverse events for a subject based on visits."""
        aes = []
        
        for i in range(visit_count):
            if self.random.random() < ae_probability:
                ae_term, soc = self.random.choice(self.COMMON_AES)
                
                # Determine severity (weighted toward mild)
                severity_weights = [0.5, 0.3, 0.15, 0.04, 0.01]
                severity = self.random.choices(
                    list(AESeverity),
                    weights=severity_weights,
                )[0]
                
                # Serious if Grade 3+
                is_serious = severity in [AESeverity.GRADE_3, AESeverity.GRADE_4, AESeverity.GRADE_5]
                
                onset = date.today() + timedelta(days=i * 28)
                duration = self.random.randint(1, 14)
                
                ae = AdverseEvent(
                    subject_id=subject.subject_id,
                    protocol_id=subject.protocol_id,
                    ae_term=ae_term,
                    system_organ_class=soc,
                    onset_date=onset,
                    resolution_date=onset + timedelta(days=duration),
                    duration_days=duration,
                    severity=severity,
                    is_serious=is_serious,
                    causality=self.random.choice(list(AECausality)),
                    outcome=AEOutcome.RECOVERED if not is_serious else self.random.choice(list(AEOutcome)),
                )
                aes.append(ae)
        
        return aes


class ExposureGenerator:
    """Generate drug exposure records."""
    
    def __init__(self, seed: int | None = None):
        """Initialize generator with optional seed."""
        self.seed = seed
        self.random = random.Random(seed)
    
    def generate_for_subject(
        self,
        subject: Subject,
        drug_name: str = "Study Drug",
        dose: float = 100.0,
        dose_unit: str = "mg",
        duration_weeks: int = 52,
        start_date: date | None = None,
    ) -> list[Exposure]:
        """Generate exposure records for a subject."""
        if start_date is None:
            start_date = date.today()
        
        exposures = []
        current_date = start_date
        
        # Generate weekly/monthly exposure records
        while current_date < start_date + timedelta(weeks=duration_weeks):
            # Some compliance variation
            doses_planned = 7
            compliance = self.random.uniform(0.8, 1.0)
            doses_taken = int(doses_planned * compliance)
            
            exposure = Exposure(
                subject_id=subject.subject_id,
                protocol_id=subject.protocol_id,
                drug_name=drug_name,
                dose=dose,
                dose_unit=dose_unit,
                start_date=current_date,
                end_date=current_date + timedelta(days=6),
                doses_planned=doses_planned,
                doses_taken=doses_taken,
                compliance_pct=round(compliance * 100, 1),
            )
            exposures.append(exposure)
            current_date += timedelta(weeks=1)
        
        return exposures
