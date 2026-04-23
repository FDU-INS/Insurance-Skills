"""Profile executor for RxMemberSim.

Extends core ProfileExecutor with pharmacy member-specific entity generation.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

from healthsim.generation.distributions import create_distribution
from healthsim.generation.profile_executor import (
    ExecutionResult,
    HierarchicalSeedManager,
    ProfileExecutor,
    ValidationReport,
)
from healthsim.generation.profile_schema import ProfileSpecification

from rxmembersim.generation.profiles import RxMemberProfileSpecification


@dataclass
class RxMemberValidationResult:
    """Simple validation result for RxMember generation."""
    
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class GeneratedRxMember:
    """A generated pharmacy benefit member."""

    rx_member_id: str
    member_id: str | None = None  # Link to MemberSim if applicable
    
    # Demographics
    first_name: str = ""
    last_name: str = ""
    date_of_birth: date | None = None
    gender: str = ""
    
    # Pharmacy benefit enrollment
    bin_number: str = ""
    pcn: str = ""
    group_id: str = ""
    cardholder_id: str = ""
    person_code: str = "01"
    
    # Coverage details
    coverage_type: str = "Commercial"
    effective_date: date | None = None
    term_date: date | None = None
    
    # Pharmacy preferences
    preferred_pharmacy_type: str = "retail"
    mail_order_eligible: bool = True
    specialty_eligible: bool = False
    
    # Therapy profile
    active_therapies: list[dict[str, Any]] = field(default_factory=list)
    adherence_score: float = 0.75
    
    # Formulary
    formulary_id: str = ""
    
    # Raw data for extensibility
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class RxMemberExecutionResult(ExecutionResult):
    """Result from RxMember profile execution."""

    rx_members: list[GeneratedRxMember] = field(default_factory=list)


class RxMemberProfileExecutor(ProfileExecutor):
    """Executor for pharmacy member profile specifications.

    Generates pharmacy benefit members based on profile specifications,
    with pharmacy-specific attributes like formulary tiers, therapy
    patterns, and pharmacy preferences.

    Example:
        >>> from rxmembersim.generation import RxMemberProfileExecutor
        >>> from rxmembersim.generation.templates import get_template
        >>> 
        >>> spec = get_template("medicare-partd-polypharmacy")
        >>> executor = RxMemberProfileExecutor(spec)
        >>> result = executor.execute()
        >>> print(f"Generated {result.count} pharmacy members")
    """

    def __init__(
        self,
        spec: RxMemberProfileSpecification | ProfileSpecification | dict[str, Any],
        seed: int | None = None,
    ):
        """Initialize executor with profile specification.

        Args:
            spec: Profile specification (RxMember-specific, core, or dict)
            seed: Random seed for reproducibility (overrides spec)
        """
        # Convert to RxMemberProfileSpecification if needed
        if isinstance(spec, dict):
            self.rx_spec = RxMemberProfileSpecification.model_validate(spec)
        elif isinstance(spec, ProfileSpecification):
            self.rx_spec = RxMemberProfileSpecification.from_core_profile(spec)
        else:
            self.rx_spec = spec

        # Initialize parent with core spec
        core_spec = self.rx_spec.to_core_profile()
        super().__init__(core_spec, seed=seed)

        # Override seed if provided
        if seed is not None:
            self.rx_spec.generation.seed = seed

    def execute(self) -> RxMemberExecutionResult:
        """Execute profile specification to generate pharmacy members.

        Returns:
            RxMemberExecutionResult with generated members and validation
        """
        import time
        start_time = time.time()
        
        # Get count from spec
        count = self.rx_spec.generation.count

        # Setup seed manager
        seed = self.rx_spec.generation.seed or 42
        self.seed_manager = HierarchicalSeedManager(seed)

        # Generate members
        rx_members = []
        for i in range(count):
            rng = self.seed_manager.get_entity_rng(i)
            rx_member = self._generate_rx_member(i, rng)
            rx_members.append(rx_member)

        # Basic validation
        validation = self._validate_results(rx_members)
        
        duration = time.time() - start_time

        return RxMemberExecutionResult(
            entities=[m.raw for m in rx_members],
            rx_members=rx_members,
            validation=validation,
            profile_id=self.rx_spec.id,
            seed=seed,
            count=count,
            duration_seconds=duration,
        )

    def _generate_rx_member(
        self,
        index: int,
        rng: "random.Random",
    ) -> GeneratedRxMember:
        """Generate a single pharmacy member."""
        import random
        from faker import Faker

        fake = Faker()
        Faker.seed(rng.randint(0, 2**31))

        # Generate demographics
        demographics = self._generate_demographics(rng, fake)

        # Generate pharmacy-specific attributes
        coverage = self.rx_spec.coverage
        
        # Pharmacy channel preference
        pharmacy_dist = create_distribution({
            "type": "categorical",
            "weights": coverage.pharmacy_preference.weights,
        })
        preferred_pharmacy = pharmacy_dist.sample(rng=rng)

        # Formulary tier tendency (affects which drugs they get)
        tier_dist = create_distribution({
            "type": "categorical",
            "weights": coverage.formulary_tier_distribution.weights,
        })

        # Adherence score
        adherence_dist = create_distribution(
            coverage.therapy_pattern.adherence_rate.model_dump()
        )
        adherence = min(1.0, max(0.0, adherence_dist.sample(rng=rng)))

        # Number of active therapies
        therapy_count_dist = create_distribution(
            coverage.therapy_pattern.avg_therapies_per_member.model_dump()
        )
        therapy_count = int(therapy_count_dist.sample(rng=rng))

        # Generate BIN/PCN/Group
        bin_number = coverage.enrollment.bin_number if coverage.enrollment else None
        if not bin_number:
            bin_number = f"{fake.random_int(100000, 999999)}"
        
        pcn = coverage.enrollment.pcn if coverage.enrollment else None
        if not pcn:
            pcn = fake.lexify("???").upper()

        group_id = coverage.group_id or f"GRP{fake.random_int(10000, 99999)}"

        # Effective dates
        effective_date = date.today() - timedelta(days=fake.random_int(30, 365))
        if coverage.enrollment and coverage.enrollment.effective_date:
            effective_date = coverage.enrollment.effective_date

        rx_member = GeneratedRxMember(
            rx_member_id=f"RXMBR{index + 1:06d}",
            first_name=demographics["first_name"],
            last_name=demographics["last_name"],
            date_of_birth=demographics["date_of_birth"],
            gender=demographics["gender"],
            bin_number=bin_number,
            pcn=pcn,
            group_id=group_id,
            cardholder_id=f"CH{fake.random_int(100000000, 999999999)}",
            person_code="01",
            coverage_type=coverage.coverage_type,
            effective_date=effective_date,
            preferred_pharmacy_type=preferred_pharmacy,
            mail_order_eligible=preferred_pharmacy != "ltc",
            specialty_eligible=self.rx_spec.generation.include_specialty_rx,
            adherence_score=round(adherence, 3),
            formulary_id=coverage.enrollment.formulary_id if coverage.enrollment else f"FORM{fake.random_int(1000, 9999)}",
            raw={
                "therapy_count": therapy_count,
                "tier_preference": tier_dist.sample(rng=rng),
                "refill_pattern": coverage.therapy_pattern.refill_pattern,
            },
        )

        return rx_member

    def _generate_demographics(
        self,
        rng: "random.Random",
        fake: Any,
    ) -> dict[str, Any]:
        """Generate demographic attributes from profile spec."""
        result = {}

        # Gender
        gender_weights = {"M": 0.48, "F": 0.52}
        if self.rx_spec.demographics and self.rx_spec.demographics.gender:
            gender_weights = self.rx_spec.demographics.gender.weights
        
        gender_dist = create_distribution({"type": "categorical", "weights": gender_weights})
        result["gender"] = gender_dist.sample(rng=rng)

        # Name based on gender
        if result["gender"] == "M":
            result["first_name"] = fake.first_name_male()
        else:
            result["first_name"] = fake.first_name_female()
        result["last_name"] = fake.last_name()

        # Age/DOB
        if self.rx_spec.demographics and self.rx_spec.demographics.age:
            age_dist = create_distribution(self.rx_spec.demographics.age.model_dump())
            age = int(age_dist.sample(rng=rng))
        else:
            age = fake.random_int(18, 85)
        
        result["date_of_birth"] = date.today() - timedelta(days=age * 365 + fake.random_int(0, 364))

        return result

    def _validate_results(
        self,
        rx_members: list[GeneratedRxMember],
    ) -> RxMemberValidationResult:
        """Validate generated members."""
        errors = []
        warnings = []

        # Check for required fields
        for member in rx_members:
            if not member.rx_member_id:
                errors.append(f"Member missing rx_member_id")
            if not member.bin_number:
                warnings.append(f"Member {member.rx_member_id} missing BIN")
            if member.adherence_score < 0 or member.adherence_score > 1:
                errors.append(
                    f"Member {member.rx_member_id} has invalid adherence: {member.adherence_score}"
                )

        return RxMemberValidationResult(
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )
