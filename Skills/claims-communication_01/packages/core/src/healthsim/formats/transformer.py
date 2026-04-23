"""Base transformer for format conversion.

Provides abstract base class for transforming generated
data into various output formats.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class Transformer(ABC, Generic[TInput, TOutput]):
    """Abstract base class for format transformers.

    Subclasses implement transformation logic for specific
    output formats (FHIR, HL7v2, X12, etc.).
    """

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Name of the output format."""
        pass

    @property
    def format_version(self) -> str | None:
        """Version of the output format, if applicable."""
        return None

    @abstractmethod
    def transform(self, input_data: TInput) -> TOutput:
        """Transform input data to output format.

        Args:
            input_data: The data to transform

        Returns:
            Transformed data in the target format
        """
        pass

    def transform_many(self, items: list[TInput]) -> list[TOutput]:
        """Transform multiple items."""
        return [self.transform(item) for item in items]

    def __call__(self, input_data: TInput) -> TOutput:
        """Allow transformer to be called directly."""
        return self.transform(input_data)


class JsonTransformer(Transformer[Any, dict[str, Any]]):
    """Base class for JSON output transformers."""

    @property
    def format_name(self) -> str:
        return "JSON"

    def to_json_string(self, input_data: Any, indent: int = 2) -> str:
        """Transform and return as JSON string."""
        return json.dumps(self.transform(input_data), indent=indent, default=str)


class CsvTransformer(Transformer[Any, list[dict[str, Any]]]):
    """Base class for CSV output transformers."""

    @property
    def format_name(self) -> str:
        return "CSV"

    @property
    @abstractmethod
    def columns(self) -> list[str]:
        """Column headers for CSV output."""
        pass

    def to_csv_string(self, items: list[Any], include_header: bool = True) -> str:
        """Transform items to CSV string."""
        import csv
        import io

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.columns)

        if include_header:
            writer.writeheader()

        rows = self.transform_many(items)
        for row_list in rows:
            for row in row_list:
                writer.writerow(row)

        return output.getvalue()
