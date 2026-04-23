"""Base transformer classes.

Provides abstract base classes for format transformers.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")  # Input type
R = TypeVar("R")  # Output type


class BaseTransformer(ABC, Generic[T, R]):
    """Abstract base class for format transformers.

    Transformers convert data from one format to another.
    Products should extend this to create domain-specific transformers.

    Type Parameters:
        T: Input type
        R: Output type

    Example:
        >>> class PersonToDict(BaseTransformer[Person, dict]):
        ...     def transform(self, source: Person) -> dict:
        ...         return source.model_dump()
        ...
        >>> transformer = PersonToDict()
        >>> result = transformer.transform(person)
    """

    @abstractmethod
    def transform(self, source: T) -> R:
        """Transform a single source object.

        Args:
            source: Object to transform

        Returns:
            Transformed object
        """
        ...

    def transform_batch(self, sources: list[T]) -> list[R]:
        """Transform multiple source objects.

        Args:
            sources: List of objects to transform

        Returns:
            List of transformed objects
        """
        return [self.transform(s) for s in sources]

    def can_transform(self, source: T) -> bool:
        """Check if source can be transformed.

        Override this to add validation logic.

        Args:
            source: Object to check

        Returns:
            True if object can be transformed
        """
        return True


class BidirectionalTransformer(ABC, Generic[T, R]):
    """Transformer that can convert in both directions.

    Type Parameters:
        T: First type
        R: Second type

    Example:
        >>> class PersonJsonTransformer(BidirectionalTransformer[Person, str]):
        ...     def forward(self, source: Person) -> str:
        ...         return source.model_dump_json()
        ...
        ...     def reverse(self, source: str) -> Person:
        ...         return Person.model_validate_json(source)
    """

    @abstractmethod
    def forward(self, source: T) -> R:
        """Transform from T to R.

        Args:
            source: Object of type T

        Returns:
            Object of type R
        """
        ...

    @abstractmethod
    def reverse(self, source: R) -> T:
        """Transform from R to T.

        Args:
            source: Object of type R

        Returns:
            Object of type T
        """
        ...


class ChainedTransformer(BaseTransformer[T, R]):
    """Transformer that chains multiple transformers together.

    Example:
        >>> chain = ChainedTransformer([
        ...     PersonToDict(),
        ...     DictToJson()
        ... ])
        >>> json_str = chain.transform(person)
    """

    def __init__(self, transformers: list[BaseTransformer]) -> None:
        """Initialize with a list of transformers.

        Args:
            transformers: List of transformers to chain
        """
        if not transformers:
            raise ValueError("Must provide at least one transformer")
        self.transformers = transformers

    def transform(self, source: T) -> R:
        """Transform by applying each transformer in sequence.

        Args:
            source: Initial input

        Returns:
            Final transformed output
        """
        result = source
        for transformer in self.transformers:
            result = transformer.transform(result)
        return result
