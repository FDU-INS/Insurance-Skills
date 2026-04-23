"""Cohort generation for batch synthetic data creation.

Provides infrastructure for generating groups of entities
with configurable constraints and distributions.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from healthsim.generation.reproducibility import SeedManager

T = TypeVar("T")


@dataclass
class CohortConstraints:
    """Constraints for cohort generation.

    Generic constraints that can be extended by product-specific
    constraint classes.
    """

    count: int = 100

    # Age constraints
    min_age: int | None = None
    max_age: int | None = None

    # Gender distribution (as percentages that should sum to ~100)
    gender_distribution: dict[str, float] = field(default_factory=dict)

    # Custom constraints as key-value pairs
    custom: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert constraints to dictionary for serialization."""
        return {
            "count": self.count,
            "min_age": self.min_age,
            "max_age": self.max_age,
            "gender_distribution": self.gender_distribution,
            "custom": self.custom,
        }


@dataclass
class CohortProgress:
    """Track progress of cohort generation."""

    total: int = 0
    completed: int = 0
    failed: int = 0
    current_item: int = 0

    @property
    def percent_complete(self) -> float:
        """Get percentage of items completed."""
        if self.total == 0:
            return 0.0
        return (self.completed / self.total) * 100

    @property
    def is_complete(self) -> bool:
        """Check if generation is complete."""
        return self.completed + self.failed >= self.total


class CohortGenerator(Generic[T]):
    """Generate cohorts of entities with constraints.

    This is a generic base class. Products should create specific
    subclasses (PatientCohortGenerator, MemberCohortGenerator) that
    implement the generate_one method.

    Example:
        class MemberCohortGenerator(CohortGenerator[Member]):
            def generate_one(self, index: int, constraints: CohortConstraints) -> Member:
                # Member-specific generation logic
                pass
    """

    def __init__(self, seed: int | None = None):
        """Initialize cohort generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed_manager = SeedManager(seed or 42)
        self._progress = CohortProgress()

    def generate_one(self, index: int, constraints: CohortConstraints) -> T:
        """Generate a single entity. Override in subclasses.

        Args:
            index: Index of this entity in the cohort (0-based)
            constraints: Generation constraints

        Returns:
            Generated entity

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement generate_one")

    def generate(
        self,
        constraints: CohortConstraints,
        progress_callback: Callable[[CohortProgress], None] | None = None,
    ) -> list[T]:
        """Generate a cohort of entities.

        Args:
            constraints: Generation constraints including count
            progress_callback: Optional callback for progress updates

        Returns:
            List of generated entities
        """
        self._progress = CohortProgress(total=constraints.count)
        results: list[T] = []

        for i in range(constraints.count):
            self._progress.current_item = i
            try:
                entity = self.generate_one(i, constraints)
                results.append(entity)
                self._progress.completed += 1
            except Exception:
                self._progress.failed += 1

            if progress_callback:
                progress_callback(self._progress)

        return results

    def generate_iter(self, constraints: CohortConstraints) -> Iterator[T]:
        """Generate entities as an iterator (memory efficient).

        Args:
            constraints: Generation constraints including count

        Yields:
            Generated entities one at a time
        """
        for i in range(constraints.count):
            yield self.generate_one(i, constraints)

    @property
    def progress(self) -> CohortProgress:
        """Get current generation progress."""
        return self._progress

    def reset(self) -> None:
        """Reset the generator's seed manager."""
        self.seed_manager.reset()
