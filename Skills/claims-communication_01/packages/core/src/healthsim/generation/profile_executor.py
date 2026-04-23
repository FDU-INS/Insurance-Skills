"""Profile executor for generating entities from profile specifications.

This is Phase 2 of the two-phase architecture:
  Phase 1 (Building): Conversational → ProfileSpecification JSON
  Phase 2 (Execution): ProfileSpecification → Generated Data

The executor is deterministic: given the same ProfileSpecification and seed,
it produces identical output.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any

from pydantic import BaseModel

from healthsim.generation.distributions import (
    AgeBandDistribution,
    CategoricalDistribution,
    ConditionalDistribution,
    ExplicitDistribution,
    LogNormalDistribution,
    NormalDistribution,
    UniformDistribution,
    create_distribution,
)
from healthsim.generation.profile_schema import (
    DistributionSpec,
    DistributionType,
    ProfileSpecification,
)



class HierarchicalSeedManager:
    """Manages hierarchical seeds for stable subset generation.

    Master seed spawns child seeds for each entity. This enables:
    - Adding entities without changing existing ones
    - Filtering subset while maintaining reproducibility
    - Parallel generation with deterministic results
    """

    def __init__(self, master_seed: int | None = None):
        """Initialize with master seed.

        Args:
            master_seed: Root seed (None for random)
        """
        self.master_seed = master_seed or random.randint(0, 2**31 - 1)
        self._master_rng = random.Random(self.master_seed)
        self._entity_seeds: dict[int, int] = {}

    def get_entity_seed(self, entity_index: int) -> int:
        """Get deterministic seed for a specific entity.

        Args:
            entity_index: 0-based index of the entity

        Returns:
            Seed value for this entity
        """
        if entity_index not in self._entity_seeds:
            # Generate seeds sequentially to ensure determinism
            while len(self._entity_seeds) <= entity_index:
                idx = len(self._entity_seeds)
                self._entity_seeds[idx] = self._master_rng.randint(0, 2**31 - 1)
        return self._entity_seeds[entity_index]

    def get_entity_rng(self, entity_index: int) -> random.Random:
        """Get a Random instance for a specific entity.

        Args:
            entity_index: 0-based index of the entity

        Returns:
            Random instance seeded for this entity
        """
        return random.Random(self.get_entity_seed(entity_index))

    def reset(self) -> None:
        """Reset to initial state."""
        self._master_rng = random.Random(self.master_seed)
        self._entity_seeds.clear()



@dataclass
class GeneratedEntity:
    """A single generated entity with all attributes."""

    index: int
    seed: int
    # Demographics
    age: int | None = None
    gender: str | None = None
    birth_date: date | None = None
    race: str | None = None
    ethnicity: str | None = None
    # Geography
    state: str | None = None
    county_fips: str | None = None
    city: str | None = None
    zip_code: str | None = None
    # Clinical
    conditions: list[str] = field(default_factory=list)
    severity: str | None = None
    lab_values: dict[str, float] = field(default_factory=dict)
    # Coverage
    coverage_type: str | None = None
    plan_type: str | None = None
    # Identifiers (generated later by product-specific code)
    identifiers: dict[str, str] = field(default_factory=dict)
    # Raw attributes for extension
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    """Result of profile execution."""

    profile_id: str
    seed: int
    count: int
    entities: list[GeneratedEntity]
    validation: "ValidationReport"
    duration_seconds: float
    created: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ValidationMetric:
    """A single validation metric."""

    name: str
    target: float
    actual: float
    tolerance: float = 0.05
    passed: bool = False

    def __post_init__(self) -> None:
        """Check if within tolerance."""
        if self.target == 0:
            self.passed = self.actual == 0
        else:
            deviation = abs(self.actual - self.target) / abs(self.target)
            self.passed = deviation <= self.tolerance


@dataclass
class ValidationReport:
    """Validation report for generated cohort."""

    metrics: list[ValidationMetric] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Check if all validations passed."""
        return len(self.errors) == 0 and all(m.passed for m in self.metrics)



class ProfileExecutor:
    """Execute profile specifications to generate entities.

    The executor follows these principles:
    1. Deterministic: Same spec + seed = identical output
    2. Hierarchical seeds: Each entity gets its own derived seed
    3. Order-independent: Entity N is always the same regardless of count
    4. Validating: Output distributions checked against specification

    Example:
        >>> spec = ProfileSpecification.from_json(json_string)
        >>> executor = ProfileExecutor(spec)
        >>> result = executor.execute()
        >>> print(f"Generated {result.count} entities")
    """

    def __init__(
        self,
        profile: ProfileSpecification,
        seed: int | None = None,
    ):
        """Initialize executor with profile specification.

        Args:
            profile: The profile specification to execute
            seed: Override seed (defaults to profile.generation.seed)
        """
        self.profile = profile
        self.seed = seed or profile.generation.seed or random.randint(0, 2**31 - 1)
        self.seed_manager = HierarchicalSeedManager(self.seed)
        self._reference_data: dict[str, Any] = {}

    def execute(
        self,
        count_override: int | None = None,
        dry_run: bool = False,
    ) -> ExecutionResult:
        """Execute the profile to generate entities.

        Args:
            count_override: Override the count from profile
            dry_run: If True, generate sample only

        Returns:
            ExecutionResult with generated entities and validation
        """
        import time
        start_time = time.time()

        count = count_override or self.profile.generation.count
        if dry_run:
            count = min(count, 5)  # Sample only

        entities: list[GeneratedEntity] = []
        for i in range(count):
            entity = self._generate_entity(i)
            entities.append(entity)

        duration = time.time() - start_time
        validation = self._validate(entities)

        return ExecutionResult(
            profile_id=self.profile.id,
            seed=self.seed,
            count=len(entities),
            entities=entities,
            validation=validation,
            duration_seconds=duration,
        )


    def _generate_entity(self, index: int) -> GeneratedEntity:
        """Generate a single entity at the given index.

        Args:
            index: 0-based entity index

        Returns:
            Generated entity with all attributes
        """
        rng = self.seed_manager.get_entity_rng(index)
        entity = GeneratedEntity(
            index=index,
            seed=self.seed_manager.get_entity_seed(index),
        )

        # Generate demographics
        if self.profile.demographics:
            self._generate_demographics(entity, rng)

        # Generate clinical attributes
        if self.profile.clinical:
            self._generate_clinical(entity, rng)

        # Generate coverage
        if self.profile.coverage:
            self._generate_coverage(entity, rng)

        return entity

    def _generate_demographics(
        self,
        entity: GeneratedEntity,
        rng: random.Random,
    ) -> None:
        """Generate demographic attributes for an entity."""
        demo = self.profile.demographics
        if not demo:
            return

        # Age
        if demo.age:
            entity.age = self._sample_distribution(demo.age, rng, as_int=True)
            # Calculate birth date from age
            today = date.today()
            birth_year = today.year - entity.age
            entity.birth_date = date(
                birth_year,
                rng.randint(1, 12),
                rng.randint(1, 28),
            )

        # Gender
        if demo.gender:
            entity.gender = self._sample_distribution(demo.gender, rng)

        # Race
        if demo.race:
            entity.race = self._sample_distribution(demo.race, rng)

        # Ethnicity
        if demo.ethnicity:
            entity.ethnicity = self._sample_distribution(demo.ethnicity, rng)

        # Geography (from reference or explicit)
        if demo.geography or demo.reference:
            self._generate_geography(entity, rng)


    def _generate_geography(
        self,
        entity: GeneratedEntity,
        rng: random.Random,
    ) -> None:
        """Generate geographic attributes."""
        demo = self.profile.demographics
        ref = demo.geography or demo.reference if demo else None
        if not ref:
            return

        # For now, use simple state/county assignment
        # TODO: Integrate with PopulationSim reference data
        if ref.state:
            entity.state = ref.state
        if ref.fips:
            entity.county_fips = ref.fips
        elif ref.code:
            entity.county_fips = ref.code

    def _generate_clinical(
        self,
        entity: GeneratedEntity,
        rng: random.Random,
    ) -> None:
        """Generate clinical attributes for an entity."""
        clinical = self.profile.clinical
        if not clinical:
            return

        # Primary condition
        if clinical.primary_condition:
            pc = clinical.primary_condition
            if rng.random() < pc.prevalence:
                entity.conditions.append(pc.code)

        # Severity (affects lab values)
        if clinical.severity:
            entity.severity = self._sample_distribution(clinical.severity, rng)
            entity.attributes["severity"] = entity.severity

        # Comorbidities
        if clinical.comorbidities:
            for comorbidity in clinical.comorbidities:
                if rng.random() < comorbidity.prevalence:
                    entity.conditions.append(comorbidity.code)

        # Lab values (potentially conditional on severity)
        if clinical.lab_values:
            context = {"severity": entity.severity} if entity.severity else {}
            for lab_name, lab_dist in clinical.lab_values.items():
                value = self._sample_distribution(lab_dist, rng, context=context)
                entity.lab_values[lab_name] = value

    def _generate_coverage(
        self,
        entity: GeneratedEntity,
        rng: random.Random,
    ) -> None:
        """Generate coverage attributes for an entity."""
        coverage = self.profile.coverage
        if not coverage:
            return

        entity.coverage_type = coverage.type

        if coverage.plan_distribution:
            plans = list(coverage.plan_distribution.keys())
            weights = list(coverage.plan_distribution.values())
            entity.plan_type = rng.choices(plans, weights=weights, k=1)[0]
        elif coverage.plan_type:
            entity.plan_type = self._sample_distribution(coverage.plan_type, rng)


    def _sample_distribution(
        self,
        dist_spec: DistributionSpec,
        rng: random.Random,
        as_int: bool = False,
        context: dict[str, Any] | None = None,
    ) -> Any:
        """Sample a value from a distribution specification.

        Args:
            dist_spec: The distribution specification
            rng: Random number generator
            as_int: Round result to integer
            context: Context for conditional distributions

        Returns:
            Sampled value
        """
        spec_dict = dist_spec.model_dump(exclude_none=True)
        dist = create_distribution(spec_dict)

        # Handle conditional distributions
        if dist_spec.type == DistributionType.CONDITIONAL and context:
            cond_dist = ConditionalDistribution(
                rules=dist_spec.rules or [],
                default=dist_spec.default,
            )
            value = cond_dist.sample(context, rng)
        else:
            value = dist.sample(rng)

        # Apply bounds if specified
        if dist_spec.min is not None and value < dist_spec.min:
            value = dist_spec.min
        if dist_spec.max is not None and value > dist_spec.max:
            value = dist_spec.max

        if as_int:
            value = int(round(value))

        return value

    def _validate(self, entities: list[GeneratedEntity]) -> ValidationReport:
        """Validate generated entities against profile specification.

        Args:
            entities: List of generated entities

        Returns:
            Validation report with metrics and issues
        """
        report = ValidationReport()
        if not entities:
            report.warnings.append("No entities generated")
            return report

        count = len(entities)

        # Validate demographics
        if self.profile.demographics:
            self._validate_demographics(entities, report)

        # Validate clinical
        if self.profile.clinical:
            self._validate_clinical(entities, report)

        # Validate coverage
        if self.profile.coverage:
            self._validate_coverage(entities, report)

        return report


    def _validate_demographics(
        self,
        entities: list[GeneratedEntity],
        report: ValidationReport,
    ) -> None:
        """Validate demographic distributions."""
        demo = self.profile.demographics
        if not demo:
            return

        count = len(entities)

        # Validate age distribution
        if demo.age and demo.age.type == DistributionType.NORMAL:
            ages = [e.age for e in entities if e.age is not None]
            if ages:
                actual_mean = sum(ages) / len(ages)
                target_mean = demo.age.mean or 0
                report.metrics.append(ValidationMetric(
                    name="Age (mean)",
                    target=target_mean,
                    actual=actual_mean,
                    tolerance=0.05,
                ))

        # Validate gender distribution
        if demo.gender and demo.gender.type == DistributionType.CATEGORICAL:
            for gender, target_pct in (demo.gender.weights or {}).items():
                actual_count = sum(1 for e in entities if e.gender == gender)
                actual_pct = actual_count / count if count > 0 else 0
                report.metrics.append(ValidationMetric(
                    name=f"Gender {gender}",
                    target=target_pct,
                    actual=actual_pct,
                    tolerance=0.05,
                ))

    def _validate_clinical(
        self,
        entities: list[GeneratedEntity],
        report: ValidationReport,
    ) -> None:
        """Validate clinical distributions."""
        clinical = self.profile.clinical
        if not clinical:
            return

        count = len(entities)

        # Validate primary condition prevalence
        if clinical.primary_condition:
            pc = clinical.primary_condition
            actual_count = sum(
                1 for e in entities if pc.code in e.conditions
            )
            actual_pct = actual_count / count if count > 0 else 0
            report.metrics.append(ValidationMetric(
                name=f"Primary condition {pc.code}",
                target=pc.prevalence,
                actual=actual_pct,
                tolerance=0.05,
            ))

        # Validate comorbidities
        if clinical.comorbidities:
            for comorbidity in clinical.comorbidities:
                actual_count = sum(
                    1 for e in entities if comorbidity.code in e.conditions
                )
                actual_pct = actual_count / count if count > 0 else 0
                report.metrics.append(ValidationMetric(
                    name=f"Comorbidity {comorbidity.code}",
                    target=comorbidity.prevalence,
                    actual=actual_pct,
                    tolerance=0.10,  # More tolerance for comorbidities
                ))


    def _validate_coverage(
        self,
        entities: list[GeneratedEntity],
        report: ValidationReport,
    ) -> None:
        """Validate coverage distributions."""
        coverage = self.profile.coverage
        if not coverage:
            return

        count = len(entities)

        # Validate plan distribution
        if coverage.plan_distribution:
            for plan, target_pct in coverage.plan_distribution.items():
                actual_count = sum(
                    1 for e in entities if e.plan_type == plan
                )
                actual_pct = actual_count / count if count > 0 else 0
                report.metrics.append(ValidationMetric(
                    name=f"Plan {plan}",
                    target=target_pct,
                    actual=actual_pct,
                    tolerance=0.05,
                ))


def execute_profile(
    profile: ProfileSpecification | dict[str, Any] | str,
    seed: int | None = None,
    count: int | None = None,
) -> ExecutionResult:
    """Convenience function to execute a profile specification.

    Args:
        profile: ProfileSpecification, dict, or JSON string
        seed: Optional seed override
        count: Optional count override

    Returns:
        ExecutionResult with generated entities

    Example:
        >>> result = execute_profile({
        ...     "id": "test-profile",
        ...     "name": "Test",
        ...     "generation": {"count": 10},
        ...     "demographics": {
        ...         "age": {"type": "normal", "mean": 45, "std_dev": 10}
        ...     }
        ... })
        >>> print(f"Generated {result.count} entities")
    """
    if isinstance(profile, str):
        spec = ProfileSpecification.from_json(profile)
    elif isinstance(profile, dict):
        spec = ProfileSpecification.model_validate(profile)
    else:
        spec = profile

    executor = ProfileExecutor(spec, seed=seed)
    return executor.execute(count_override=count)
