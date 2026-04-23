"""Member cohort generation using healthsim-core infrastructure.

Extends core CohortGenerator for health plan member-specific generation.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from healthsim.generation import CohortConstraints as BaseCohortConstraints
from healthsim.generation import CohortGenerator as BaseCohortGenerator
from healthsim.generation import CohortProgress, WeightedChoice

if TYPE_CHECKING:
    from membersim.core.member import Member


@dataclass
class MemberCohortConstraints(BaseCohortConstraints):
    """Constraints for member cohort generation.

    Extends base constraints with health plan specific options.
    """

    count: int = 100  # Must re-declare to satisfy dataclass inheritance
    gender_distribution: dict[str, float] = field(
        default_factory=lambda: {"M": 0.49, "F": 0.51}
    )
    age_distribution: dict[str, float] = field(
        default_factory=lambda: {
            "0-17": 0.10,
            "18-34": 0.20,
            "35-54": 0.35,
            "55-64": 0.20,
            "65+": 0.15,
        }
    )
    plan_distribution: dict[str, float] = field(
        default_factory=lambda: {
            "HMO": 0.35,
            "PPO": 0.40,
            "HDHP": 0.25,
        }
    )
    state_distribution: dict[str, float] | None = None

    def validate(self) -> list[str]:
        """Validate constraints sum to ~1.0."""
        errors = []
        for name, dist in [
            ("gender", self.gender_distribution),
            ("age", self.age_distribution),
            ("plan", self.plan_distribution),
        ]:
            total = sum(dist.values())
            if abs(total - 1.0) > 0.01:
                errors.append(f"{name} distribution sums to {total}, should be 1.0")
        return errors

    def to_dict(self) -> dict[str, Any]:
        """Convert constraints to dictionary."""
        base = super().to_dict()
        base.update({
            "gender_distribution": self.gender_distribution,
            "age_distribution": self.age_distribution,
            "plan_distribution": self.plan_distribution,
            "state_distribution": self.state_distribution,
        })
        return base


class MemberCohortGenerator(BaseCohortGenerator["Member"]):
    """Generate cohorts of health plan members with demographic constraints.

    Example:
        constraints = MemberCohortConstraints(
            count=1000,
            gender_distribution={"M": 0.45, "F": 0.55},
            plan_distribution={"PPO": 0.6, "HMO": 0.4},
        )

        generator = MemberCohortGenerator(seed=42)
        members = generator.generate(constraints)
    """

    def __init__(self, seed: int | None = None):
        """Initialize member cohort generator.

        Args:
            seed: Random seed for reproducibility
        """
        super().__init__(seed=seed)
        # Late import to avoid circular dependency
        from membersim.core.member import MemberGenerator

        self._member_generator = MemberGenerator(seed=seed)
        self._gender_choice: WeightedChoice[str] | None = None
        self._plan_choice: WeightedChoice[str] | None = None
        self._age_choice: WeightedChoice[str] | None = None

    def _setup_distributions(self, constraints: MemberCohortConstraints) -> None:
        """Setup weighted choice distributions from constraints."""
        self._gender_choice = WeightedChoice(
            options=list(constraints.gender_distribution.items()),
        )
        self._plan_choice = WeightedChoice(
            options=list(constraints.plan_distribution.items()),
        )
        self._age_choice = WeightedChoice(
            options=list(constraints.age_distribution.items()),
        )

    def _select_age_band(self, age_band: str) -> tuple[int, int]:
        """Convert age band string to (min, max) tuple."""
        age_bands = {
            "0-17": (0, 17),
            "18-34": (18, 34),
            "35-54": (35, 54),
            "55-64": (55, 64),
            "65+": (65, 90),
        }
        if age_band not in age_bands:
            raise ValueError(f"Unknown age band: {age_band}")
        return age_bands[age_band]

    def generate_one(
        self,
        _index: int,
        constraints: BaseCohortConstraints,
    ) -> Member:
        """Generate a single member.

        Args:
            index: Index of this member in the cohort
            constraints: Generation constraints

        Returns:
            Generated Member instance
        """
        if not isinstance(constraints, MemberCohortConstraints):
            constraints = MemberCohortConstraints(count=constraints.count)

        # Setup distributions on first call
        if self._gender_choice is None:
            self._setup_distributions(constraints)

        # Select attributes from distributions using seed_manager's rng
        gender = self._gender_choice.select(rng=self.seed_manager.rng)  # type: ignore
        plan_type = self._plan_choice.select(rng=self.seed_manager.rng)  # type: ignore
        age_band = self._age_choice.select(rng=self.seed_manager.rng)  # type: ignore
        min_age, max_age = self._select_age_band(age_band)

        # Get deterministic seed for this member
        member_seed = self.seed_manager.get_child_seed()

        return self._member_generator.generate_one(
            seed=member_seed,
            gender=gender,
            plan_type=plan_type,
            min_age=min_age,
            max_age=max_age,
        )

    def generate(
        self,
        constraints: BaseCohortConstraints,
        progress_callback: Callable[[CohortProgress], None] | None = None,
    ) -> list[Member]:
        """Generate a cohort of members.

        Args:
            constraints: Generation constraints
            progress_callback: Optional callback for progress updates

        Returns:
            List of generated members
        """
        # Reset distributions for new cohort
        self._gender_choice = None
        self._plan_choice = None
        self._age_choice = None

        return super().generate(constraints, progress_callback)


# Aliases for backward compatibility
CohortConstraints = MemberCohortConstraints
CohortGenerator = MemberCohortGenerator
