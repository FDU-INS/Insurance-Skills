"""Profile executor for TrialSim.

Extends core ProfileExecutor with clinical trial subject generation.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any
from uuid import uuid4

from healthsim.generation.distributions import create_distribution
from healthsim.generation.profile_executor import (
    ExecutionResult,
    ProfileExecutor,
    ValidationReport,
)
from healthsim.generation.reproducibility import SeedManager
from healthsim.generation.profile_schema import ProfileSpecification

from trialsim.generation.profiles import TrialSimProfileSpecification


@dataclass
class TrialSimValidationResult:
    """Simple validation result for TrialSim generation."""
    
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class GeneratedSite:
    """A generated trial site."""

    site_id: str
    name: str
    country: str = "USA"
    region: str = "North America"
    principal_investigator: str = ""
    is_active: bool = True
    activation_date: date | None = None
    target_enrollment: int = 10
    
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratedSubject:
    """A generated clinical trial subject."""

    subject_id: str
    protocol_id: str
    site_id: str
    
    # Demographics
    first_name: str = ""
    last_name: str = ""
    age: int = 0
    sex: str = "M"
    race: str | None = None
    ethnicity: str | None = None
    date_of_birth: date | None = None
    
    # Enrollment
    screening_date: date | None = None
    screening_status: str = "passed"
    screening_failure_reason: str | None = None
    randomization_date: date | None = None
    arm: str | None = None
    status: str = "screening"
    enrollment_date: date | None = None
    
    # Compliance
    visit_compliance: float = 0.90
    treatment_compliance: float = 0.85
    
    # Adverse events probability
    ae_probability: float = 0.30
    
    # Links
    patient_id: str | None = None
    
    # Raw data
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class TrialSimExecutionResult(ExecutionResult):
    """Result from TrialSim profile execution."""

    subjects: list[GeneratedSubject] = field(default_factory=list)
    sites: list[GeneratedSite] = field(default_factory=list)
    protocol_id: str = ""
    
    @property
    def enrolled_count(self) -> int:
        return len([s for s in self.subjects if s.status != "screen_failed"])
    
    @property
    def screen_failure_count(self) -> int:
        return len([s for s in self.subjects if s.status == "screen_failed"])
    
    @property
    def arm_counts(self) -> dict[str, int]:
        """Count subjects by arm."""
        counts = {}
        for s in self.subjects:
            if s.arm:
                counts[s.arm] = counts.get(s.arm, 0) + 1
        return counts


class TrialSimProfileExecutor(ProfileExecutor):
    """Executor for clinical trial profile specifications.

    Generates clinical trial subjects based on profile specifications,
    with trial-specific attributes like arm randomization, visit
    compliance, and adverse event probability.
    """

    def __init__(
        self,
        spec: TrialSimProfileSpecification | ProfileSpecification | dict[str, Any],
        seed: int | None = None,
    ):
        """Initialize executor with profile specification.

        Args:
            spec: Profile specification (TrialSim-specific, core, or dict)
            seed: Random seed for reproducibility (overrides spec)
        """
        # Convert to TrialSimProfileSpecification if needed
        if isinstance(spec, dict):
            self.trial_spec = TrialSimProfileSpecification.model_validate(spec)
        elif isinstance(spec, ProfileSpecification):
            self.trial_spec = TrialSimProfileSpecification.from_core_profile(spec)
        else:
            self.trial_spec = spec

        # Initialize parent with core spec
        core_spec = self.trial_spec.to_core_profile()
        super().__init__(core_spec, seed=seed)

        # Override seed if provided
        if seed is not None:
            self.trial_spec.generation.seed = seed

    def execute(
        self,
        count_override: int | None = None,
        dry_run: bool = False,
    ) -> TrialSimExecutionResult:
        """Execute profile specification to generate trial subjects.

        Args:
            count_override: Override the count from profile
            dry_run: If True, generate small sample only (max 5)

        Returns:
            TrialSimExecutionResult with generated subjects, sites, and validation
        """
        start_time = time.time()
        
        # Determine count
        count = count_override or self.trial_spec.generation.count
        if dry_run:
            count = min(count, 5)

        # Setup seed manager
        seed = self.trial_spec.generation.seed or 42

        # Generate protocol ID
        protocol = self.trial_spec.protocol
        protocol_id = protocol.protocol_id or f"PROT-{uuid4().hex[:8].upper()}"

        # Generate sites
        sites = self._generate_sites(seed)

        # Generate subjects
        subjects = []
        for i in range(count):
            rng = self.seed_manager.get_entity_rng(i)
            site = sites[i % len(sites)] if sites else GeneratedSite(
                site_id="SITE-001", name="Default Site"
            )
            subject = self._generate_subject(i, protocol_id, site, rng)
            subjects.append(subject)

        # Validate
        validation = self._validate_results(subjects, sites)
        duration = time.time() - start_time

        return TrialSimExecutionResult(
            entities=[s.raw for s in subjects],
            subjects=subjects,
            sites=sites,
            protocol_id=protocol_id,
            validation=validation,
            profile_id=self.trial_spec.id,
            seed=seed,
            count=len(subjects),
            duration_seconds=duration,
        )

    def _generate_sites(self, seed: int) -> list[GeneratedSite]:
        """Generate trial sites."""
        from faker import Faker

        fake = Faker()
        Faker.seed(seed)

        sites_spec = self.trial_spec.sites
        num_sites = sites_spec.num_sites

        # Region distribution
        region_dist = create_distribution(sites_spec.region_distribution.model_dump())

        sites = []
        for i in range(num_sites):
            rng = random.Random(seed + i + 1000)
            region = region_dist.sample(rng=rng)
            
            # Map region to country
            region_countries = {
                "North America": ["USA", "Canada"],
                "Europe": ["UK", "Germany", "France", "Spain", "Italy"],
                "Asia Pacific": ["Japan", "Australia", "South Korea", "China"],
                "Latin America": ["Brazil", "Mexico", "Argentina"],
            }
            countries = region_countries.get(region, ["USA"])
            country = fake.random_element(countries)

            site = GeneratedSite(
                site_id=f"SITE-{i + 1:03d}",
                name=f"{fake.city()} Clinical Research Center",
                country=country,
                region=region,
                principal_investigator=f"Dr. {fake.last_name()}",
                is_active=True,
                activation_date=date.today() - timedelta(days=fake.random_int(30, 180)),
                target_enrollment=int(sites_spec.subjects_per_site.mean or 10),
                raw={"index": i},
            )
            sites.append(site)

        return sites

    def _generate_subject(
        self,
        index: int,
        protocol_id: str,
        site: GeneratedSite,
        rng: random.Random,
    ) -> GeneratedSubject:
        """Generate a single trial subject."""
        from faker import Faker

        fake = Faker()
        fake.seed_instance(rng.randint(0, 2**31 - 1))

        # Generate demographics
        demographics = self._generate_demographics(rng, fake)

        # Screening
        enrollment_spec = self.trial_spec.enrollment
        screening_date = date.today() - timedelta(days=fake.random_int(7, 90))
        
        # Check screen failure
        screen_failed = rng.random() < enrollment_spec.screening_failure_rate
        
        screening_status = "failed" if screen_failed else "passed"
        screening_failure_reason = None
        randomization_date = None
        enrollment_date = None
        arm = None
        status = "screen_failed" if screen_failed else "enrolled"
        
        if screen_failed:
            failure_dist = create_distribution(
                enrollment_spec.screening_failure_reasons.model_dump()
            )
            screening_failure_reason = failure_dist.sample(rng=rng)
        else:
            # Randomize
            enrollment_date = screening_date + timedelta(days=rng.randint(1, 7))
            randomization_date = enrollment_date + timedelta(days=rng.randint(1, 7))
            
            arm_dist = create_distribution(self.trial_spec.arm_distribution.model_dump())
            arm = arm_dist.sample(rng=rng)
            status = "randomized"

        # Compliance values
        visit_comp_dist = create_distribution(
            self.trial_spec.visit_compliance.attendance_rate.model_dump()
        )
        visit_compliance = min(1.0, max(0.0, visit_comp_dist.sample(rng=rng)))

        exp_comp_dist = create_distribution(
            self.trial_spec.exposure_compliance.compliance_rate.model_dump()
        )
        treatment_compliance = min(1.0, max(0.0, exp_comp_dist.sample(rng=rng)))

        # AE probability
        ae_prob = self.trial_spec.adverse_events.ae_probability
        if arm == "placebo":
            ae_prob *= 0.6

        return GeneratedSubject(
            subject_id=f"SUBJ-{index + 1:05d}",
            protocol_id=protocol_id,
            site_id=site.site_id,
            first_name=demographics["first_name"],
            last_name=demographics["last_name"],
            age=demographics["age"],
            sex=demographics["sex"],
            race=demographics.get("race"),
            ethnicity=demographics.get("ethnicity"),
            date_of_birth=demographics["date_of_birth"],
            screening_date=screening_date,
            screening_status=screening_status,
            screening_failure_reason=screening_failure_reason,
            randomization_date=randomization_date,
            enrollment_date=enrollment_date,
            arm=arm,
            status=status,
            visit_compliance=round(visit_compliance, 3),
            treatment_compliance=round(treatment_compliance, 3),
            ae_probability=round(ae_prob, 3),
            raw={
                "protocol": self.trial_spec.protocol.model_dump(),
                "site_region": site.region,
            },
        )

    def _generate_demographics(
        self,
        rng: random.Random,
        fake: Any,
    ) -> dict[str, Any]:
        """Generate demographic attributes from profile spec."""
        result = {}

        # Sex
        sex_weights = {"M": 0.50, "F": 0.50}
        if self.trial_spec.demographics and self.trial_spec.demographics.gender:
            sex_weights = self.trial_spec.demographics.gender.weights
        
        sex_dist = create_distribution({"type": "categorical", "weights": sex_weights})
        result["sex"] = sex_dist.sample(rng=rng)

        # Name based on sex
        if result["sex"] == "M":
            result["first_name"] = fake.first_name_male()
        else:
            result["first_name"] = fake.first_name_female()
        result["last_name"] = fake.last_name()

        # Age
        if self.trial_spec.demographics and self.trial_spec.demographics.age:
            age_dist = create_distribution(self.trial_spec.demographics.age.model_dump())
            result["age"] = int(age_dist.sample(rng=rng))
        else:
            result["age"] = rng.randint(18, 75)
        
        result["date_of_birth"] = date.today() - timedelta(
            days=result["age"] * 365 + rng.randint(0, 364)
        )

        # Race/ethnicity
        race_dist = create_distribution({
            "type": "categorical",
            "weights": {
                "White": 0.60, "Black or African American": 0.15,
                "Asian": 0.12, "American Indian or Alaska Native": 0.02,
                "Native Hawaiian or Other Pacific Islander": 0.01,
                "Multiple": 0.05, "Unknown": 0.05,
            }
        })
        result["race"] = race_dist.sample(rng=rng)

        ethnicity_dist = create_distribution({
            "type": "categorical",
            "weights": {"Not Hispanic or Latino": 0.85, "Hispanic or Latino": 0.15}
        })
        result["ethnicity"] = ethnicity_dist.sample(rng=rng)

        return result

    def _validate_results(
        self,
        subjects: list[GeneratedSubject],
        sites: list[GeneratedSite],
    ) -> TrialSimValidationResult:
        """Validate generated subjects and sites."""
        errors = []
        warnings = []

        if not sites:
            errors.append("No sites generated")

        for subject in subjects:
            if not subject.subject_id:
                errors.append("Subject missing subject_id")
            if not subject.site_id:
                errors.append(f"Subject {subject.subject_id} missing site_id")

        # Check arm distribution
        enrolled = [s for s in subjects if s.arm is not None]
        if enrolled:
            arm_counts = {}
            for s in enrolled:
                arm_counts[s.arm] = arm_counts.get(s.arm, 0) + 1
            
            expected = self.trial_spec.arm_distribution.weights
            for arm, expected_pct in expected.items():
                actual_pct = arm_counts.get(arm, 0) / len(enrolled)
                if abs(actual_pct - expected_pct) > 0.15:
                    warnings.append(
                        f"Arm '{arm}' distribution off: expected {expected_pct:.1%}, got {actual_pct:.1%}"
                    )

        return TrialSimValidationResult(
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )
