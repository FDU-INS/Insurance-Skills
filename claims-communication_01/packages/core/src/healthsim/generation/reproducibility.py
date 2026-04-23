"""Seed management for reproducible generation.

Provides utilities for managing random seeds to ensure reproducibility
across generation runs.
"""

import random
from typing import Any

from faker import Faker


class SeedManager:
    """Manages random seeds for reproducible data generation.

    Provides a centralized way to set and manage seeds for both
    Python's random module and Faker.

    Attributes:
        seed: The master seed value
        rng: Random number generator instance

    Example:
        >>> manager = SeedManager(seed=42)
        >>> manager.get_random_int(1, 100)
        82
        >>> manager2 = SeedManager(seed=42)
        >>> manager2.get_random_int(1, 100)
        82  # Same result with same seed
    """

    def __init__(self, seed: int | None = None, locale: str = "en_US") -> None:
        """Initialize the seed manager.

        Args:
            seed: Master seed value (None for random)
            locale: Locale for Faker
        """
        self.seed = seed
        self.locale = locale
        self.rng = random.Random(seed)
        self.faker = Faker(locale)

        if seed is not None:
            Faker.seed(seed)
            self.faker.seed_instance(seed)

    def reset(self) -> None:
        """Reset the random state to the original seed."""
        if self.seed is not None:
            self.rng = random.Random(self.seed)
            Faker.seed(self.seed)
            self.faker = Faker(self.locale)
            self.faker.seed_instance(self.seed)

    def get_child_seed(self) -> int:
        """Get a deterministic child seed for sub-generators.

        Returns:
            A seed derived from the current state
        """
        return self.rng.randint(0, 2**31 - 1)

    def get_random_int(self, min_val: int, max_val: int) -> int:
        """Get a random integer in range.

        Args:
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)

        Returns:
            Random integer in range
        """
        return self.rng.randint(min_val, max_val)

    def get_random_float(self, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Get a random float in range.

        Args:
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Random float in range
        """
        return self.rng.uniform(min_val, max_val)

    def get_random_choice(self, options: list[Any]) -> Any:
        """Get a random choice from a list.

        Args:
            options: List of options to choose from

        Returns:
            Randomly selected item
        """
        return self.rng.choice(options)

    def get_random_sample(self, options: list[Any], k: int) -> list[Any]:
        """Get a random sample from a list.

        Args:
            options: List of options to sample from
            k: Number of items to sample

        Returns:
            List of k randomly selected items
        """
        return self.rng.sample(options, min(k, len(options)))

    def shuffle(self, items: list[Any]) -> list[Any]:
        """Shuffle a list in place and return it.

        Args:
            items: List to shuffle

        Returns:
            The shuffled list
        """
        self.rng.shuffle(items)
        return items

    def get_random_bool(self, probability: float = 0.5) -> bool:
        """Get a random boolean with given probability of True.

        Args:
            probability: Probability of returning True (0.0 to 1.0)

        Returns:
            Random boolean
        """
        return self.rng.random() < probability
