"""DuckDB writer for dimensional model data.

Provides a writer class for persisting dimensional model tables to DuckDB,
which is ideal for local analytics workloads and fast SQL queries.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import duckdb
import pandas as pd

from healthsim.dimensional.writers.base import BaseDimensionalWriter

if TYPE_CHECKING:
    from healthsim.config.dimensional import TargetConfig


class DuckDBDimensionalWriter(BaseDimensionalWriter):
    """Write dimensional model to DuckDB database.

    DuckDB is an embedded analytical database that provides fast OLAP
    queries without requiring a separate server process. This writer
    handles creating schemas, writing dimension and fact tables, and
    querying the results.

    The writer supports both in-memory databases (for testing and
    temporary analytics) and persistent file-based databases.

    Class Attributes:
        TARGET_NAME: 'duckdb'
        REQUIRED_PACKAGES: ['duckdb']

    Example:
        >>> from healthsim.dimensional import DuckDBDimensionalWriter, generate_dim_date
        >>>
        >>> with DuckDBDimensionalWriter(':memory:') as writer:
        ...     dim_date = generate_dim_date('2024-01-01', '2024-12-31')
        ...     writer.write_table('dim_date', dim_date)
        ...     result = writer.query('SELECT COUNT(*) as cnt FROM analytics.dim_date')
        ...     print(result.iloc[0]['cnt'])
        366

    Attributes:
        db_path: Path to the database file or ':memory:'.
        schema: Schema name for dimensional tables (default: 'analytics').
        read_only: Whether the database is opened in read-only mode.
    """

    TARGET_NAME = "duckdb"
    REQUIRED_PACKAGES = ["duckdb"]

    def __init__(
        self,
        db_path: str | Path = ":memory:",
        schema: str = "analytics",
        read_only: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize DuckDB writer.

        The connection is lazy - it's not opened until the first
        operation is performed or connect() is called.

        Args:
            db_path: Path to database file or ':memory:' for in-memory.
                Defaults to ':memory:'.
            schema: Schema name for dimensional tables. Defaults to 'analytics'.
            read_only: Open in read-only mode. Defaults to False.
            **kwargs: Additional arguments (ignored, for compatibility).
        """
        super().__init__(schema=schema, **kwargs)
        self.db_path = str(db_path)
        self.read_only = read_only
        self._connection: duckdb.DuckDBPyConnection | None = None
        self._schema_created = False

        # Ensure directory exists for file-based databases
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_config(cls, config: TargetConfig) -> DuckDBDimensionalWriter:
        """Create from configuration object.

        Args:
            config: Target configuration with connection settings.

        Returns:
            Configured DuckDBDimensionalWriter instance.
        """
        settings = config.settings
        return cls(
            db_path=settings.get("db_path", ":memory:"),
            schema=settings.get("schema", "analytics"),
            read_only=settings.get("read_only", False),
        )

    def _ensure_connection(self) -> duckdb.DuckDBPyConnection:
        """Ensure database connection is open and schema exists.

        Returns:
            Active DuckDB connection.
        """
        if self._connection is None:
            self._connection = duckdb.connect(self.db_path, read_only=self.read_only)

        if not self._schema_created and not self.read_only:
            self._connection.execute(f"CREATE SCHEMA IF NOT EXISTS {self.schema}")
            self._schema_created = True

        return self._connection

    def connect(self) -> None:
        """Establish connection to DuckDB."""
        self._ensure_connection()

    def close(self) -> None:
        """Close the database connection.

        Safe to call multiple times - will only close if connection is open.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            self._schema_created = False

    def write_table(
        self,
        table_name: str,
        df: pd.DataFrame,
        if_exists: str = "replace",
    ) -> int:
        """Write a single DataFrame to a table.

        The table will be created in the configured schema (default: 'analytics').
        Empty DataFrames will create empty tables with the correct schema.

        Args:
            table_name: Name of the table (without schema prefix).
            df: DataFrame to write.
            if_exists: How to handle existing tables:
                - 'replace': Drop and recreate the table (default)
                - 'append': Add rows to existing table

        Returns:
            Number of rows written.

        Raises:
            ValueError: If if_exists is not 'replace' or 'append'.
        """
        if if_exists not in ("replace", "append"):
            raise ValueError(f"if_exists must be 'replace' or 'append', got '{if_exists}'")

        conn = self._ensure_connection()
        full_table_name = f"{self.schema}.{table_name}"

        if if_exists == "replace":
            conn.execute(f"DROP TABLE IF EXISTS {full_table_name}")

        # Register the DataFrame temporarily
        conn.register("_temp_df", df)

        if if_exists == "replace":
            conn.execute(f"CREATE TABLE {full_table_name} AS SELECT * FROM _temp_df")
        else:  # append
            # Check if table exists
            if self.table_exists(table_name):
                conn.execute(f"INSERT INTO {full_table_name} SELECT * FROM _temp_df")
            else:
                conn.execute(f"CREATE TABLE {full_table_name} AS SELECT * FROM _temp_df")

        conn.unregister("_temp_df")

        return len(df)

    def get_table_list(self) -> list[str]:
        """Get list of tables in the schema.

        Returns:
            List of table names (without schema prefix).
        """
        conn = self._ensure_connection()

        result = conn.execute(
            f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{self.schema}'
            ORDER BY table_name
            """
        ).fetchall()

        return [row[0] for row in result]

    def get_table_stats(self) -> pd.DataFrame:
        """Get statistics for all tables in schema.

        Returns:
            DataFrame with columns:
                - table_name: Name of the table
                - row_count: Number of rows in the table
                - column_count: Number of columns in the table
        """
        conn = self._ensure_connection()
        tables = self.get_table_list()

        stats = []
        for table_name in tables:
            full_name = f"{self.schema}.{table_name}"

            # Get row count
            row_count = conn.execute(f"SELECT COUNT(*) FROM {full_name}").fetchone()[0]

            # Get column count
            col_result = conn.execute(
                f"""
                SELECT COUNT(*) FROM information_schema.columns
                WHERE table_schema = '{self.schema}' AND table_name = '{table_name}'
                """
            ).fetchone()
            col_count = col_result[0] if col_result else 0

            stats.append(
                {
                    "table_name": table_name,
                    "row_count": row_count,
                    "column_count": col_count,
                }
            )

        return pd.DataFrame(stats)

    def query(self, sql: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame.

        This is useful for running analytical queries against the
        dimensional model after data has been loaded.

        Args:
            sql: SQL query string. Can reference tables using the
                full schema.table_name format (e.g., 'analytics.dim_date').

        Returns:
            Query results as DataFrame.

        Example:
            >>> df = writer.query('''
            ...     SELECT year, COUNT(*) as holiday_count
            ...     FROM analytics.dim_date
            ...     WHERE is_us_federal_holiday = TRUE
            ...     GROUP BY year
            ... ''')
        """
        conn = self._ensure_connection()
        return conn.execute(sql).df()

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the schema.

        Args:
            table_name: Name of the table.

        Returns:
            True if table exists.
        """
        conn = self._ensure_connection()
        result = conn.execute(
            f"""
            SELECT COUNT(*) as cnt FROM information_schema.tables
            WHERE table_schema = '{self.schema}' AND table_name = '{table_name}'
            """
        ).fetchone()
        return result is not None and result[0] > 0

    @property
    def full_table_prefix(self) -> str:
        """Return fully qualified schema name.

        Returns:
            The schema name (e.g., 'analytics').
        """
        return self.schema

    def drop_table(self, table_name: str) -> bool:
        """Drop a table if it exists.

        Args:
            table_name: Name of the table to drop.

        Returns:
            True if dropped, False if table didn't exist.
        """
        if not self.table_exists(table_name):
            return False
        conn = self._ensure_connection()
        full_name = f"{self.schema}.{table_name}"
        conn.execute(f"DROP TABLE {full_name}")
        return True

    # Legacy property for backward compatibility
    @property
    def full_schema_name(self) -> str:
        """Return fully qualified schema name.

        Deprecated: Use full_table_prefix instead.

        Returns:
            The schema name (e.g., 'analytics').
        """
        return self.schema
