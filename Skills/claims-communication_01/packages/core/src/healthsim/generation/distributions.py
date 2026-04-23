"""Statistical distributions for data generation.

Provides distribution classes for generating values according
to various statistical distributions.
"""

import random
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class WeightedChoice(BaseModel, Generic[T]):
    """Weighted random selection from options.

    Allows selecting from a list of options where each option
    has an associated weight/probability.

    Attributes:
        options: List of (option, weight) tuples

    Example:
        >>> choices = WeightedChoice(options=[
        ...     ("common", 0.7),
        ...     ("uncommon", 0.2),
        ...     ("rare", 0.1)
        ... ])
        >>> # "common" will be selected ~70% of the time
        >>> choices.select()
        'common'
    """

    options: list[tuple[Any, float]]

    def select(self, rng: random.Random | None = None) -> Any:
        """Select an option based on weights.

        Args:
            rng: Random number generator (for reproducibility)

        Returns:
            Selected option
        """
        if not self.options:
            raise ValueError("No options to select from")

        if rng is None:
            rng = random.Random()

        items = [opt[0] for opt in self.options]
        weights = [opt[1] for opt in self.options]

        return rng.choices(items, weights=weights, k=1)[0]

    def select_multiple(
        self,
        count: int,
        rng: random.Random | None = None,
        unique: bool = False,
    ) -> list[Any]:
        """Select multiple options.

        Args:
            count: Number of options to select
            rng: Random number generator
            unique: If True, each option can only be selected once

        Returns:
            List of selected options
        """
        if not self.options:
            raise ValueError("No options to select from")

        if rng is None:
            rng = random.Random()

        items = [opt[0] for opt in self.options]
        weights = [opt[1] for opt in self.options]

        if unique:
            if count > len(items):
                raise ValueError(f"Cannot select {count} unique items from {len(items)} options")

            selected = []
            remaining_items = list(items)
            remaining_weights = list(weights)

            for _ in range(count):
                choice = rng.choices(remaining_items, weights=remaining_weights, k=1)[0]
                selected.append(choice)
                idx = remaining_items.index(choice)
                remaining_items.pop(idx)
                remaining_weights.pop(idx)

            return selected
        else:
            return rng.choices(items, weights=weights, k=count)


class Distribution(ABC):
    """Abstract base class for statistical distributions."""

    @abstractmethod
    def sample(self, rng: random.Random | None = None) -> float:
        """Sample a value from the distribution.

        Args:
            rng: Random number generator

        Returns:
            Sampled value
        """
        ...


class NormalDistribution(Distribution, BaseModel):
    """Normal (Gaussian) distribution.

    Attributes:
        mean: Mean of the distribution
        std_dev: Standard deviation

    Example:
        >>> dist = NormalDistribution(mean=100, std_dev=15)
        >>> value = dist.sample()  # ~100 +/- 15
    """

    mean: float
    std_dev: float

    def sample(self, rng: random.Random | None = None) -> float:
        """Sample from the normal distribution.

        Args:
            rng: Random number generator

        Returns:
            Sampled value
        """
        if rng is None:
            rng = random.Random()
        return rng.gauss(self.mean, self.std_dev)

    def sample_int(self, rng: random.Random | None = None) -> int:
        """Sample and round to integer.

        Args:
            rng: Random number generator

        Returns:
            Sampled integer value
        """
        return round(self.sample(rng))

    def sample_bounded(
        self,
        min_val: float | None = None,
        max_val: float | None = None,
        rng: random.Random | None = None,
    ) -> float:
        """Sample with bounds, re-sampling if outside range.

        Args:
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            rng: Random number generator

        Returns:
            Sampled value within bounds
        """
        max_attempts = 1000
        for _ in range(max_attempts):
            value = self.sample(rng)
            if min_val is not None and value < min_val:
                continue
            if max_val is not None and value > max_val:
                continue
            return value

        # Fallback: clamp to bounds
        value = self.sample(rng)
        if min_val is not None and value < min_val:
            return min_val
        if max_val is not None and value > max_val:
            return max_val
        return value


class UniformDistribution(Distribution, BaseModel):
    """Uniform distribution between min and max.

    Attributes:
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)

    Example:
        >>> dist = UniformDistribution(min_val=0, max_val=100)
        >>> value = dist.sample()  # 0 to 100 with equal probability
    """

    min_val: float
    max_val: float

    def sample(self, rng: random.Random | None = None) -> float:
        """Sample from the uniform distribution.

        Args:
            rng: Random number generator

        Returns:
            Sampled value
        """
        if rng is None:
            rng = random.Random()
        return rng.uniform(self.min_val, self.max_val)

    def sample_int(self, rng: random.Random | None = None) -> int:
        """Sample and return integer.

        Args:
            rng: Random number generator

        Returns:
            Sampled integer value
        """
        if rng is None:
            rng = random.Random()
        return rng.randint(int(self.min_val), int(self.max_val))


class AgeDistribution:
    """Age distribution for population generation.

    Provides weighted random age selection based on
    configurable age bands.
    """

    def __init__(self, bands: list[tuple[int, int, float]] | None = None):
        """Initialize age distribution.

        Args:
            bands: List of (min_age, max_age, weight) tuples
        """
        if bands is None:
            # Default adult distribution
            self.bands = [
                (18, 30, 0.20),
                (31, 45, 0.25),
                (46, 60, 0.25),
                (61, 75, 0.20),
                (76, 90, 0.10),
            ]
        else:
            self.bands = bands
        self._rng = random.Random()

    def seed(self, seed: int) -> None:
        """Set random seed for reproducibility."""
        self._rng = random.Random(seed)

    def sample(self) -> int:
        """Sample an age from the distribution."""
        # Weighted selection of band
        weights = [band[2] for band in self.bands]
        band = self._rng.choices(self.bands, weights=weights, k=1)[0]

        # Random age within band
        return self._rng.randint(band[0], band[1])

    def sample_many(self, count: int) -> list[int]:
        """Sample multiple ages."""
        return [self.sample() for _ in range(count)]

    @classmethod
    def pediatric(cls) -> "AgeDistribution":
        """Create pediatric age distribution (0-17)."""
        return cls(
            bands=[
                (0, 2, 0.15),
                (3, 5, 0.15),
                (6, 12, 0.35),
                (13, 17, 0.35),
            ]
        )

    @classmethod
    def adult(cls) -> "AgeDistribution":
        """Create adult age distribution (18-90)."""
        return cls()  # Uses default

    @classmethod
    def senior(cls) -> "AgeDistribution":
        """Create senior age distribution (65+)."""
        return cls(
            bands=[
                (65, 70, 0.30),
                (71, 75, 0.25),
                (76, 80, 0.20),
                (81, 85, 0.15),
                (86, 95, 0.10),
            ]
        )



class LogNormalDistribution(Distribution, BaseModel):
    """Log-normal distribution for right-skewed positive values.

    Common in healthcare for costs, lengths of stay, and other
    values that can't be negative and have a long tail.

    Attributes:
        mean: Target mean of the distribution
        std_dev: Target standard deviation
        min_val: Optional minimum value (clamp)

    Example:
        >>> dist = LogNormalDistribution(mean=5000, std_dev=8000)
        >>> value = dist.sample()  # Typically small, occasionally large
    """

    mean: float
    std_dev: float
    min_val: float = 0.0

    def sample(self, rng: random.Random | None = None) -> float:
        """Sample from the log-normal distribution.

        Args:
            rng: Random number generator

        Returns:
            Sampled value (always positive)
        """
        import math

        if rng is None:
            rng = random.Random()

        # Convert mean/std_dev to log-space parameters
        # Using method of moments
        if self.mean <= 0:
            return self.min_val

        variance = self.std_dev**2
        mu = math.log(self.mean**2 / math.sqrt(variance + self.mean**2))
        sigma = math.sqrt(math.log(1 + variance / self.mean**2))

        value = rng.lognormvariate(mu, sigma)
        return max(value, self.min_val)

    def sample_bounded(
        self,
        max_val: float | None = None,
        rng: random.Random | None = None,
    ) -> float:
        """Sample with optional upper bound.

        Args:
            max_val: Maximum allowed value
            rng: Random number generator

        Returns:
            Sampled value within bounds
        """
        value = self.sample(rng)
        if max_val is not None and value > max_val:
            return max_val
        return value


class ExplicitDistribution(Distribution, BaseModel):
    """Distribution with explicit values and weights.

    Use when you need to select from a specific list of values
    with defined probabilities.

    Attributes:
        values: List of (value, weight) tuples

    Example:
        >>> dist = ExplicitDistribution(values=[
        ...     ("48201", 0.40),  # Harris County
        ...     ("48113", 0.35),  # Dallas County
        ...     ("48029", 0.25),  # Bexar County
        ... ])
        >>> value = dist.sample()  # Returns one of the county codes
    """

    values: list[tuple[Any, float]]

    def sample(self, rng: random.Random | None = None) -> Any:
        """Sample a value from the distribution.

        Args:
            rng: Random number generator

        Returns:
            Selected value
        """
        if not self.values:
            raise ValueError("No values to select from")

        if rng is None:
            rng = random.Random()

        items = [v[0] for v in self.values]
        weights = [v[1] for v in self.values]

        return rng.choices(items, weights=weights, k=1)[0]

    def sample_multiple(
        self,
        count: int,
        rng: random.Random | None = None,
        unique: bool = False,
    ) -> list[Any]:
        """Sample multiple values.

        Args:
            count: Number of values to sample
            rng: Random number generator
            unique: If True, don't repeat values

        Returns:
            List of sampled values
        """
        if not self.values:
            raise ValueError("No values to select from")

        if rng is None:
            rng = random.Random()

        items = [v[0] for v in self.values]
        weights = [v[1] for v in self.values]

        if unique:
            if count > len(items):
                raise ValueError(f"Cannot select {count} unique from {len(items)}")
            selected = []
            remaining = list(zip(items, weights))
            for _ in range(count):
                vals, wts = zip(*remaining)
                choice = rng.choices(vals, weights=wts, k=1)[0]
                selected.append(choice)
                remaining = [(v, w) for v, w in remaining if v != choice]
            return selected
        else:
            return rng.choices(items, weights=weights, k=count)



class CategoricalDistribution(Distribution, BaseModel):
    """Categorical distribution for discrete choices with weights.

    A cleaner interface for profile specifications.

    Attributes:
        weights: Dictionary mapping category names to probabilities

    Example:
        >>> dist = CategoricalDistribution(weights={"M": 0.48, "F": 0.52})
        >>> gender = dist.sample()  # "M" or "F"
    """

    weights: dict[str, float]

    def model_post_init(self, __context: Any) -> None:
        """Validate weights sum to approximately 1.0."""
        total = sum(self.weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def sample(self, rng: random.Random | None = None) -> str:
        """Sample a category from the distribution.

        Args:
            rng: Random number generator

        Returns:
            Selected category name
        """
        if not self.weights:
            raise ValueError("No categories defined")

        if rng is None:
            rng = random.Random()

        categories = list(self.weights.keys())
        probs = list(self.weights.values())

        return rng.choices(categories, weights=probs, k=1)[0]

    def sample_multiple(self, count: int, rng: random.Random | None = None) -> list[str]:
        """Sample multiple categories.

        Args:
            count: Number of samples
            rng: Random number generator

        Returns:
            List of selected categories
        """
        if rng is None:
            rng = random.Random()

        categories = list(self.weights.keys())
        probs = list(self.weights.values())

        return rng.choices(categories, weights=probs, k=count)


class AgeBandDistribution(Distribution, BaseModel):
    """Age distribution using census-style age bands.

    Attributes:
        bands: Dictionary mapping band labels to weights

    Example:
        >>> dist = AgeBandDistribution(bands={
        ...     "0-17": 0.10,
        ...     "18-34": 0.20,
        ...     "35-54": 0.35,
        ...     "55-64": 0.20,
        ...     "65+": 0.15,
        ... })
        >>> age = dist.sample()  # Age within selected band
    """

    bands: dict[str, float]

    def _parse_band(self, band_label: str) -> tuple[int, int]:
        """Parse a band label into min/max ages."""
        if band_label.endswith("+"):
            min_age = int(band_label[:-1])
            max_age = 95  # Reasonable upper bound
        elif "-" in band_label:
            parts = band_label.split("-")
            min_age = int(parts[0])
            max_age = int(parts[1])
        else:
            # Single value
            min_age = max_age = int(band_label)
        return min_age, max_age

    def sample(self, rng: random.Random | None = None) -> int:
        """Sample an age from the distribution.

        Args:
            rng: Random number generator

        Returns:
            Sampled age (integer)
        """
        if not self.bands:
            raise ValueError("No age bands defined")

        if rng is None:
            rng = random.Random()

        # Select a band based on weights
        band_labels = list(self.bands.keys())
        weights = list(self.bands.values())
        selected_band = rng.choices(band_labels, weights=weights, k=1)[0]

        # Sample uniformly within the band
        min_age, max_age = self._parse_band(selected_band)
        return rng.randint(min_age, max_age)

    def sample_multiple(self, count: int, rng: random.Random | None = None) -> list[int]:
        """Sample multiple ages."""
        if rng is None:
            rng = random.Random()
        return [self.sample(rng) for _ in range(count)]



class ConditionalRule(BaseModel):
    """A single conditional rule for conditional distributions."""

    condition: str  # e.g., "severity == 'controlled'"
    distribution: dict[str, Any]  # Distribution spec to use when condition matches


class ConditionalDistribution:
    """Distribution that varies based on entity attributes.

    Evaluates conditions against a context dictionary and selects
    the appropriate distribution.

    Example:
        >>> dist = ConditionalDistribution(rules=[
        ...     {"condition": "severity == 'controlled'",
        ...      "distribution": {"type": "normal", "mean": 6.5, "std_dev": 0.3}},
        ...     {"condition": "severity == 'uncontrolled'",
        ...      "distribution": {"type": "normal", "mean": 8.5, "std_dev": 1.0}},
        ... ])
        >>> value = dist.sample(context={"severity": "controlled"})  # ~6.5
    """

    def __init__(self, rules: list[dict[str, Any]], default: dict[str, Any] | None = None):
        """Initialize conditional distribution.

        Args:
            rules: List of {condition, distribution} dicts
            default: Default distribution if no condition matches
        """
        self.rules = rules
        self.default = default

    def _evaluate_condition(self, condition: str, context: dict[str, Any]) -> bool:
        """Evaluate a simple condition string against context.

        Supports: ==, !=, >=, <=, >, <, and, or
        """
        # Simple eval with restricted namespace
        # For safety, only allow certain operations
        try:
            # Replace attribute access with dict access
            expr = condition
            for key in context:
                # Handle string values
                if isinstance(context[key], str):
                    expr = expr.replace(f"{key}", f"context['{key}']")
                else:
                    expr = expr.replace(f"{key}", f"context['{key}']")

            return eval(expr, {"context": context, "__builtins__": {}})
        except Exception:
            return False

    def sample(
        self,
        context: dict[str, Any],
        rng: random.Random | None = None,
    ) -> Any:
        """Sample from the appropriate distribution based on context.

        Args:
            context: Dictionary of entity attributes for condition evaluation
            rng: Random number generator

        Returns:
            Sampled value from matching distribution
        """
        for rule in self.rules:
            condition = rule.get("condition", "")
            if self._evaluate_condition(condition, context):
                dist = create_distribution(rule["distribution"])
                return dist.sample(rng)

        # No condition matched, use default
        if self.default:
            dist = create_distribution(self.default)
            return dist.sample(rng)

        raise ValueError("No condition matched and no default distribution")


def create_distribution(spec: dict[str, Any]) -> Distribution:
    """Factory function to create a distribution from a specification.

    Args:
        spec: Dictionary with 'type' and type-specific parameters

    Returns:
        Appropriate Distribution instance

    Example:
        >>> dist = create_distribution({"type": "normal", "mean": 72, "std_dev": 8})
        >>> value = dist.sample()
    """
    dist_type = spec.get("type", "").lower()

    if dist_type == "categorical":
        return CategoricalDistribution(weights=spec.get("weights", {}))

    elif dist_type == "normal":
        return NormalDistribution(
            mean=spec.get("mean", 0),
            std_dev=spec.get("std_dev", 1),
        )

    elif dist_type in ("log_normal", "lognormal"):
        return LogNormalDistribution(
            mean=spec.get("mean", 100),
            std_dev=spec.get("std_dev", 50),
            min_val=spec.get("min", 0),
        )

    elif dist_type == "uniform":
        return UniformDistribution(
            min_val=spec.get("min", 0),
            max_val=spec.get("max", 1),
        )

    elif dist_type == "age_bands":
        return AgeBandDistribution(bands=spec.get("bands", {}))

    elif dist_type == "explicit":
        # Convert from various formats
        values = spec.get("values", [])
        if isinstance(values, dict):
            # {"value1": 0.5, "value2": 0.5} format
            values = [(k, v) for k, v in values.items()]
        elif values and isinstance(values[0], dict):
            # [{"value": "x", "weight": 0.5}] format
            values = [(v["value"], v["weight"]) for v in values]
        return ExplicitDistribution(values=values)

    else:
        raise ValueError(f"Unknown distribution type: {dist_type}")
