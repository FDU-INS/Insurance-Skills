"""Tests for the DuckDB dimensional writer."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from healthsim.dimensional import DuckDBDimensionalWriter, generate_dim_date


class TestDuckDBWriterInit:
    """Tests for DuckDBDimensionalWriter initialization."""

    def test_init_defaults(self):
        """Test default initialization."""
        writer = DuckDBDimensionalWriter()
        assert writer.db_path == ":memory:"
        assert writer.schema == "analytics"
        assert writer.read_only is False
        writer.close()

    def test_init_custom_path(self):
        """Test initialization with custom path."""
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False) as f:
            writer = DuckDBDimensionalWriter(f.name)
            assert writer.db_path == f.name
            writer.close()

    def test_init_custom_schema(self):
        """Test initialization with custom schema."""
        writer = DuckDBDimensionalWriter(schema="custom_schema")
        assert writer.schema == "custom_schema"
        writer.close()

    def test_init_path_as_pathlib(self):
        """Test initialization with Path object."""
        with tempfile.NamedTemporaryFile(suffix=".duckdb", delete=False) as f:
            path = Path(f.name)
            writer = DuckDBDimensionalWriter(path)
            assert writer.db_path == str(path)
            writer.close()


class TestDuckDBWriterContextManager:
    """Tests for context manager behavior."""

    def test_context_manager_entry_exit(self):
        """Test context manager opens and closes connection."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            assert writer._connection is not None

        # After exit, connection should be closed
        assert writer._connection is None

    def test_context_manager_creates_schema(self):
        """Test context manager creates schema."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            # Query to check schema exists
            result = writer.query(
                """
                SELECT schema_name FROM information_schema.schemata
                WHERE schema_name = 'analytics'
                """
            )
            assert len(result) == 1

    def test_close_is_idempotent(self):
        """Test that close() can be called multiple times safely."""
        writer = DuckDBDimensionalWriter(":memory:")
        writer._ensure_connection()
        writer.close()
        writer.close()  # Should not raise


class TestDuckDBWriterWriteTable:
    """Tests for write_table method."""

    def test_write_table_basic(self):
        """Test basic table writing."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            df = pd.DataFrame({"id": [1, 2, 3], "name": ["a", "b", "c"]})
            count = writer.write_table("test_table", df)

            assert count == 3

            result = writer.query("SELECT COUNT(*) as cnt FROM analytics.test_table")
            assert result.iloc[0]["cnt"] == 3

    def test_write_table_replace_mode(self):
        """Test replace mode overwrites existing table."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            df1 = pd.DataFrame({"id": [1, 2, 3]})
            df2 = pd.DataFrame({"id": [4, 5]})

            writer.write_table("test_table", df1)
            writer.write_table("test_table", df2, if_exists="replace")

            result = writer.query("SELECT COUNT(*) as cnt FROM analytics.test_table")
            assert result.iloc[0]["cnt"] == 2

    def test_write_table_append_mode(self):
        """Test append mode adds to existing table."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            df1 = pd.DataFrame({"id": [1, 2, 3]})
            df2 = pd.DataFrame({"id": [4, 5]})

            writer.write_table("test_table", df1)
            writer.write_table("test_table", df2, if_exists="append")

            result = writer.query("SELECT COUNT(*) as cnt FROM analytics.test_table")
            assert result.iloc[0]["cnt"] == 5

    def test_write_table_append_creates_if_not_exists(self):
        """Test append mode creates table if it doesn't exist."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            df = pd.DataFrame({"id": [1, 2, 3]})
            count = writer.write_table("new_table", df, if_exists="append")

            assert count == 3

    def test_write_table_invalid_if_exists(self):
        """Test invalid if_exists raises ValueError."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            df = pd.DataFrame({"id": [1]})
            with pytest.raises(ValueError):
                writer.write_table("test_table", df, if_exists="invalid")

    def test_write_empty_dataframe(self):
        """Test writing empty DataFrame creates empty table."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            df = pd.DataFrame({"id": pd.Series([], dtype=int), "name": pd.Series([], dtype=str)})
            count = writer.write_table("empty_table", df)

            assert count == 0

            result = writer.query("SELECT COUNT(*) as cnt FROM analytics.empty_table")
            assert result.iloc[0]["cnt"] == 0


class TestDuckDBWriterWriteDimensionalModel:
    """Tests for write_dimensional_model method."""

    def test_write_dimensional_model_basic(self):
        """Test writing complete dimensional model."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            dimensions = {
                "dim_customer": pd.DataFrame({"id": [1, 2], "name": ["A", "B"]}),
                "dim_product": pd.DataFrame({"id": [1, 2, 3], "name": ["X", "Y", "Z"]}),
            }
            facts = {
                "fact_sales": pd.DataFrame(
                    {"customer_id": [1, 1, 2], "product_id": [1, 2, 3], "amount": [100, 200, 300]}
                )
            }

            result = writer.write_dimensional_model(dimensions, facts)

            assert result["dim_customer"] == 2
            assert result["dim_product"] == 3
            assert result["fact_sales"] == 3

    def test_write_dimensional_model_with_dim_date(self):
        """Test writing model with generated date dimension."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            dim_date = generate_dim_date("2024-01-01", "2024-12-31")

            dimensions = {"dim_date": dim_date}
            facts = {}

            result = writer.write_dimensional_model(dimensions, facts)

            assert result["dim_date"] == 366  # Leap year


class TestDuckDBWriterGetTableList:
    """Tests for get_table_list method."""

    def test_get_table_list_empty(self):
        """Test get_table_list with no tables."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            tables = writer.get_table_list()
            assert tables == []

    def test_get_table_list_with_tables(self):
        """Test get_table_list with multiple tables."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            writer.write_table("table_a", pd.DataFrame({"id": [1]}))
            writer.write_table("table_b", pd.DataFrame({"id": [1]}))
            writer.write_table("dim_date", pd.DataFrame({"id": [1]}))

            tables = writer.get_table_list()

            assert "table_a" in tables
            assert "table_b" in tables
            assert "dim_date" in tables
            assert len(tables) == 3


class TestDuckDBWriterGetTableStats:
    """Tests for get_table_stats method."""

    def test_get_table_stats_basic(self):
        """Test get_table_stats returns correct stats."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            writer.write_table(
                "dim_customer", pd.DataFrame({"id": [1, 2, 3], "name": ["A", "B", "C"]})
            )
            writer.write_table(
                "fact_sales",
                pd.DataFrame({"id": [1, 2], "customer_id": [1, 2], "amount": [100, 200]}),
            )

            stats = writer.get_table_stats()

            assert len(stats) == 2

            customer_stats = stats[stats["table_name"] == "dim_customer"].iloc[0]
            assert customer_stats["row_count"] == 3
            assert customer_stats["column_count"] == 2

            sales_stats = stats[stats["table_name"] == "fact_sales"].iloc[0]
            assert sales_stats["row_count"] == 2
            assert sales_stats["column_count"] == 3

    def test_get_table_stats_empty_schema(self):
        """Test get_table_stats with no tables."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            stats = writer.get_table_stats()
            assert len(stats) == 0


class TestDuckDBWriterQuery:
    """Tests for query method."""

    def test_query_select(self):
        """Test basic SELECT query."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            writer.write_table("test", pd.DataFrame({"id": [1, 2, 3], "val": [10, 20, 30]}))

            result = writer.query("SELECT * FROM analytics.test ORDER BY id")

            assert len(result) == 3
            assert list(result["id"]) == [1, 2, 3]
            assert list(result["val"]) == [10, 20, 30]

    def test_query_aggregate(self):
        """Test aggregate query."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            writer.write_table("test", pd.DataFrame({"id": [1, 2, 3], "val": [10, 20, 30]}))

            result = writer.query("SELECT SUM(val) as total FROM analytics.test")

            assert result.iloc[0]["total"] == 60

    def test_query_join(self):
        """Test JOIN query."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            writer.write_table("customers", pd.DataFrame({"id": [1, 2], "name": ["A", "B"]}))
            writer.write_table(
                "orders", pd.DataFrame({"id": [1, 2], "customer_id": [1, 1], "amount": [100, 200]})
            )

            result = writer.query(
                """
                SELECT c.name, SUM(o.amount) as total
                FROM analytics.customers c
                JOIN analytics.orders o ON c.id = o.customer_id
                GROUP BY c.name
                """
            )

            assert len(result) == 1
            assert result.iloc[0]["name"] == "A"
            assert result.iloc[0]["total"] == 300


class TestDuckDBWriterFullSchemaName:
    """Tests for full_schema_name property."""

    def test_full_schema_name_default(self):
        """Test default schema name."""
        writer = DuckDBDimensionalWriter()
        assert writer.full_schema_name == "analytics"
        writer.close()

    def test_full_schema_name_custom(self):
        """Test custom schema name."""
        writer = DuckDBDimensionalWriter(schema="my_schema")
        assert writer.full_schema_name == "my_schema"
        writer.close()


class TestDuckDBWriterFilePersistence:
    """Tests for file-based database persistence."""

    def test_file_persistence(self):
        """Test that data persists across connections."""
        # Create a temp directory and use a path within it
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.duckdb"

            # Write data
            with DuckDBDimensionalWriter(db_path) as writer:
                writer.write_table("test", pd.DataFrame({"id": [1, 2, 3]}))

            # Read data with new connection
            with DuckDBDimensionalWriter(db_path) as writer:
                result = writer.query("SELECT COUNT(*) as cnt FROM analytics.test")
                assert result.iloc[0]["cnt"] == 3


class TestDuckDBWriterIntegration:
    """Integration tests with generate_dim_date."""

    def test_write_and_query_dim_date(self):
        """Test writing and querying date dimension."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            dim_date = generate_dim_date("2024-01-01", "2024-12-31")
            count = writer.write_table("dim_date", dim_date)

            assert count == 366

            # Query holidays
            result = writer.query(
                """
                SELECT year, COUNT(*) as holiday_count
                FROM analytics.dim_date
                WHERE is_us_federal_holiday = TRUE
                GROUP BY year
                """
            )
            assert result.iloc[0]["holiday_count"] == 11

            # Query weekends
            result = writer.query(
                """
                SELECT COUNT(*) as weekend_count
                FROM analytics.dim_date
                WHERE is_weekend = TRUE
                """
            )
            # 2024 has 104 weekend days (52 Saturdays + 52 Sundays)
            assert result.iloc[0]["weekend_count"] == 104

    def test_acceptance_criteria_validation(self):
        """Test the acceptance criteria from the specification."""
        with DuckDBDimensionalWriter(":memory:") as writer:
            dim_date = generate_dim_date("2024-01-01", "2024-12-31")
            count = writer.write_table("dim_date", dim_date)

            assert count == 366

            result = writer.query("SELECT COUNT(*) as cnt FROM analytics.dim_date")
            assert result.iloc[0]["cnt"] == 366

            tables = writer.get_table_list()
            assert "dim_date" in tables
