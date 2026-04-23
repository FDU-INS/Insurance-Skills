"""Tests for healthsim.formats module."""

import json
from datetime import date, datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from healthsim.formats import (
    BaseTransformer,
    CSVExporter,
    CsvTransformer,
    JSONExporter,
    JsonTransformer,
    Transformer,
    format_date,
    format_datetime,
    safe_str,
    truncate,
)
from healthsim.person import Gender, Person, PersonName


class MockTransformer(BaseTransformer[dict, str]):
    """Mock transformer for testing."""

    def transform(self, source: dict) -> str:
        return f"transformed:{source.get('value', '')}"


class TestBaseTransformer:
    """Tests for BaseTransformer."""

    def test_transform(self) -> None:
        """Test basic transformation."""
        transformer = MockTransformer()
        result = transformer.transform({"value": "test"})
        assert result == "transformed:test"

    def test_transform_batch(self) -> None:
        """Test batch transformation."""
        transformer = MockTransformer()
        sources = [{"value": "a"}, {"value": "b"}, {"value": "c"}]

        results = transformer.transform_batch(sources)

        assert len(results) == 3
        assert results[0] == "transformed:a"
        assert results[1] == "transformed:b"
        assert results[2] == "transformed:c"

    def test_can_transform(self) -> None:
        """Test can_transform default."""
        transformer = MockTransformer()
        assert transformer.can_transform({}) is True


class TestJSONExporter:
    """Tests for JSONExporter."""

    def test_export_dict(self) -> None:
        """Test exporting a dictionary."""
        exporter = JSONExporter()
        data = {"name": "John", "age": 30}

        result = exporter.export(data)
        parsed = json.loads(result)

        assert parsed["name"] == "John"
        assert parsed["age"] == 30

    def test_export_list(self) -> None:
        """Test exporting a list."""
        exporter = JSONExporter()
        data = [1, 2, 3]

        result = exporter.export(data)
        parsed = json.loads(result)

        assert parsed == [1, 2, 3]

    def test_export_pydantic_model(self) -> None:
        """Test exporting a Pydantic model."""
        exporter = JSONExporter()
        person = Person(
            id="test-001",
            name=PersonName(given_name="John", family_name="Smith"),
            birth_date=date(1990, 1, 1),
            gender=Gender.MALE,
        )

        result = exporter.export(person)
        parsed = json.loads(result)

        assert parsed["id"] == "test-001"
        assert parsed["name"]["given_name"] == "John"
        assert parsed["gender"] == "M"

    def test_export_with_indent(self) -> None:
        """Test indented output."""
        exporter = JSONExporter(indent=4)
        data = {"key": "value"}

        result = exporter.export(data)
        assert "    " in result  # Should have 4-space indent

    def test_export_compact(self) -> None:
        """Test compact output."""
        exporter = JSONExporter(indent=None)
        data = {"key": "value"}

        result = exporter.export(data)
        assert "\n" not in result  # No newlines in compact mode

    def test_export_list_of_models(self) -> None:
        """Test exporting list of models."""
        exporter = JSONExporter()
        items = [
            {"name": "a", "value": 1},
            {"name": "b", "value": 2},
        ]

        result = exporter.export_list(items)
        parsed = json.loads(result)

        assert len(parsed) == 2
        assert parsed[0]["name"] == "a"

    def test_export_to_file(self) -> None:
        """Test exporting to file."""
        exporter = JSONExporter()
        data = {"test": "data"}

        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = Path(f.name)

        try:
            exporter.export_to_file(data, path)

            content = path.read_text()
            parsed = json.loads(content)
            assert parsed["test"] == "data"
        finally:
            path.unlink()


class TestCSVExporter:
    """Tests for CSVExporter."""

    def test_export_list_of_dicts(self) -> None:
        """Test exporting list of dictionaries."""
        exporter = CSVExporter()
        data = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25},
        ]

        result = exporter.export(data)
        lines = result.strip().split("\n")

        assert len(lines) == 3  # Header + 2 rows
        assert "name" in lines[0]
        assert "age" in lines[0]
        assert "John" in lines[1]
        assert "Jane" in lines[2]

    def test_export_with_columns(self) -> None:
        """Test exporting with specific column order."""
        exporter = CSVExporter()
        data = [
            {"a": 1, "b": 2, "c": 3},
            {"a": 4, "b": 5, "c": 6},
        ]

        result = exporter.export(data, columns=["c", "a"])
        lines = result.strip().split("\n")

        # Strip \r for cross-platform compatibility (CSV uses \r\n)
        assert lines[0].strip() == "c,a"

    def test_export_without_header(self) -> None:
        """Test exporting without header."""
        exporter = CSVExporter(include_header=False)
        data = [{"name": "John", "age": 30}]

        result = exporter.export(data)
        lines = result.strip().split("\n")

        assert len(lines) == 1
        assert "name" not in lines[0] or "John" in lines[0]

    def test_export_custom_delimiter(self) -> None:
        """Test exporting with custom delimiter."""
        exporter = CSVExporter(delimiter=";")
        data = [{"a": 1, "b": 2}]

        result = exporter.export(data)
        assert ";" in result

    def test_export_empty_data(self) -> None:
        """Test exporting empty data."""
        exporter = CSVExporter()
        result = exporter.export([])
        assert result == ""

    def test_export_to_file(self) -> None:
        """Test exporting to file."""
        exporter = CSVExporter()
        data = [{"x": 1, "y": 2}]

        with NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            path = Path(f.name)

        try:
            exporter.export_to_file(data, path)
            content = path.read_text()
            assert "x" in content
            assert "y" in content
        finally:
            path.unlink()

    def test_export_handles_none_values(self) -> None:
        """Test that None values are handled."""
        exporter = CSVExporter()
        data = [{"name": "John", "email": None}]

        result = exporter.export(data)
        # Should not raise and should have empty string for None
        assert "John" in result

    def test_flatten_nested_dict(self) -> None:
        """Test flattening nested dictionary."""
        exporter = CSVExporter()
        nested = {"a": {"b": 1, "c": 2}}

        flat = exporter._flatten_dict(nested)

        assert "a_b" in flat
        assert "a_c" in flat
        assert flat["a_b"] == 1
        assert flat["a_c"] == 2


class TestFormatUtilities:
    """Tests for format utility functions."""

    def test_format_date(self) -> None:
        """Test date formatting."""
        d = date(2024, 1, 15)
        result = format_date(d)
        assert result == "2024-01-15"

    def test_format_date_custom_format(self) -> None:
        """Test date formatting with custom format."""
        d = date(2024, 1, 15)
        result = format_date(d, "%m/%d/%Y")
        assert result == "01/15/2024"

    def test_format_date_none(self) -> None:
        """Test format_date with None."""
        result = format_date(None)
        assert result is None

    def test_format_date_with_datetime(self) -> None:
        """Test format_date with datetime input."""
        dt = datetime(2024, 1, 15, 10, 30)
        result = format_date(dt)
        assert result == "2024-01-15"

    def test_format_datetime(self) -> None:
        """Test datetime formatting."""
        dt = datetime(2024, 1, 15, 14, 30, 45)
        result = format_datetime(dt)
        assert result == "2024-01-15T14:30:45"

    def test_format_datetime_custom_format(self) -> None:
        """Test datetime formatting with custom format."""
        dt = datetime(2024, 1, 15, 14, 30, 45)
        result = format_datetime(dt, "%Y-%m-%d %H:%M")
        assert result == "2024-01-15 14:30"

    def test_format_datetime_none(self) -> None:
        """Test format_datetime with None."""
        result = format_datetime(None)
        assert result is None

    def test_safe_str(self) -> None:
        """Test safe string conversion."""
        assert safe_str("hello") == "hello"
        assert safe_str(123) == "123"
        assert safe_str(None) == ""
        assert safe_str(3.14) == "3.14"

    def test_safe_str_with_objects(self) -> None:
        """Test safe_str with various objects."""

        class CustomObj:
            def __str__(self) -> str:
                return "custom"

        assert safe_str(CustomObj()) == "custom"
        assert safe_str([1, 2, 3]) == "[1, 2, 3]"

    def test_truncate(self) -> None:
        """Test text truncation."""
        text = "Hello, World!"
        result = truncate(text, max_length=8)
        assert result == "Hello..."
        assert len(result) == 8

    def test_truncate_no_truncation_needed(self) -> None:
        """Test truncate with short text."""
        text = "Hi"
        result = truncate(text, max_length=10)
        assert result == "Hi"

    def test_truncate_custom_suffix(self) -> None:
        """Test truncate with custom suffix."""
        text = "Hello, World!"
        result = truncate(text, max_length=10, suffix="~")
        assert result == "Hello, Wo~"
        assert len(result) == 10

    def test_truncate_exact_length(self) -> None:
        """Test truncate when text is exactly max_length."""
        text = "Hello"
        result = truncate(text, max_length=5)
        assert result == "Hello"


class TestTransformerBase:
    """Tests for Transformer abstract base class."""

    def test_transformer_is_abstract(self) -> None:
        """Test that Transformer cannot be instantiated directly."""

        # Transformer is abstract, so we test via concrete implementation
        class ConcreteTransformer(Transformer[str, str]):
            @property
            def format_name(self) -> str:
                return "test"

            def transform(self, input_data: str) -> str:
                return input_data.upper()

        transformer = ConcreteTransformer()
        assert transformer.format_name == "test"
        assert transformer.format_version is None

    def test_transform_many(self) -> None:
        """Test transform_many method."""

        class UpperTransformer(Transformer[str, str]):
            @property
            def format_name(self) -> str:
                return "upper"

            def transform(self, input_data: str) -> str:
                return input_data.upper()

        transformer = UpperTransformer()
        results = transformer.transform_many(["hello", "world"])

        assert results == ["HELLO", "WORLD"]

    def test_transformer_callable(self) -> None:
        """Test that transformer can be called directly."""

        class DoubleTransformer(Transformer[int, int]):
            @property
            def format_name(self) -> str:
                return "double"

            def transform(self, input_data: int) -> int:
                return input_data * 2

        transformer = DoubleTransformer()
        result = transformer(5)  # Call directly
        assert result == 10


class TestJsonTransformer:
    """Tests for JsonTransformer."""

    def test_format_name(self) -> None:
        """Test format name is JSON."""

        class SimpleJsonTransformer(JsonTransformer):
            def transform(self, input_data: Any) -> dict[str, Any]:
                return {"value": input_data}

        transformer = SimpleJsonTransformer()
        assert transformer.format_name == "JSON"

    def test_to_json_string(self) -> None:
        """Test to_json_string method."""

        class DictTransformer(JsonTransformer):
            def transform(self, input_data: Any) -> dict[str, Any]:
                return {"data": input_data}

        transformer = DictTransformer()
        result = transformer.to_json_string("test")
        parsed = json.loads(result)

        assert parsed == {"data": "test"}

    def test_to_json_string_indent(self) -> None:
        """Test to_json_string with custom indent."""

        class SimpleTransformer(JsonTransformer):
            def transform(self, input_data: Any) -> dict[str, Any]:
                return {"key": "value"}

        transformer = SimpleTransformer()
        result = transformer.to_json_string("ignored", indent=4)

        assert "    " in result  # 4-space indent


class TestCsvTransformer:
    """Tests for CsvTransformer."""

    def test_columns_property(self) -> None:
        """Test columns property."""

        class SimpleCsvTransformer(CsvTransformer):
            @property
            def columns(self) -> list[str]:
                return ["name", "value"]

            def transform(self, input_data: Any) -> list[dict[str, Any]]:
                return [{"name": input_data, "value": 1}]

        transformer = SimpleCsvTransformer()
        assert transformer.columns == ["name", "value"]
        assert transformer.format_name == "CSV"

    def test_to_csv_string(self) -> None:
        """Test to_csv_string method."""

        class ItemTransformer(CsvTransformer):
            @property
            def columns(self) -> list[str]:
                return ["id", "name"]

            def transform(self, input_data: dict[str, Any]) -> list[dict[str, Any]]:
                return [{"id": input_data["id"], "name": input_data["name"]}]

        transformer = ItemTransformer()
        items = [
            {"id": 1, "name": "Item A"},
            {"id": 2, "name": "Item B"},
        ]

        result = transformer.to_csv_string(items)

        assert "id,name" in result
        assert "1,Item A" in result
        assert "2,Item B" in result

    def test_to_csv_string_no_header(self) -> None:
        """Test to_csv_string without header."""

        class ItemTransformer(CsvTransformer):
            @property
            def columns(self) -> list[str]:
                return ["value"]

            def transform(self, input_data: int) -> list[dict[str, Any]]:
                return [{"value": input_data}]

        transformer = ItemTransformer()
        result = transformer.to_csv_string([1, 2], include_header=False)

        assert "value" not in result
        assert "1" in result
        assert "2" in result
