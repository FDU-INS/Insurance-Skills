"""Base class for dimensional model writers.

All writers implement this interface, enabling pluggable target support.
Writers only need to be installed if they're used.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from healthsim.config.dimensional import TargetConfig


class BaseDimensionalWriter(ABC):
    """Abstract base class for all dimensional writers.

    This class defines the interface that all dimensional writers must implement.
    Subclasses provide target-specific implementations for DuckDB, Databricks,
    Snowflake, etc.

    Class Attributes:
        TARGET_NAME: Identifier for this writer type (e.g., 'duckdb', 'databricks').
        REQUIRED_PACKAGES: List of package names required for this writer.

    Example:
        >>> class MyWriter(BaseDimensionalWriter):
        ...     TARGET_NAME = 'mydb'
        ...     REQUIRED_PACKAGES = ['mydb-connector']
        ...     # ... implement abstract methods
    """

    # Subclasses must define these
    TARGET_NAME: str = ""  # e.g., "duckdb", "databricks"
    REQUIRED_PACKAGES: list[str] = []  # e.g., ["duckdb"]

    def __init__(self, schema: str = "analytics", **kwargs: Any) -> None:
        """Initialize writer with target schema.

        Args:
            schema: Schema/database name for dimensional tables.
            **kwargs: Target-specific configuration.
        """
        self.schema = schema
        self._config = kwargs

    @classmethod
    def from_config(cls, config: TargetConfig) -> BaseDimensionalWriter:
        """Create writer from configuration object.

        Args:
            config: Target configuration with connection settings.

        Returns:
            Configured writer instance.
        """
        return cls(**config.settings)

    @classmethod
    def is_available(cls) -> bool:
        """Check if required packages are installed.

        Returns:
            True if all required packages are available.
        """
        for package in cls.REQUIRED_PACKAGES:
            try:
                __import__(package)
            except ImportError:
                return False
        return True

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the target database."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""
        pass

    def __enter__(self) -> BaseDimensionalWriter:
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit."""
        self.close()

    @abstractmethod
    def write_table(
        self,
        table_name: str,
        df: pd.DataFrame,
        if_exists: str = "replace",
    ) -> int:
        """Write a single DataFrame to a table.

        Args:
            table_name: Name of the table (without schema/catalog prefix).
            df: DataFrame to write.
            if_exists: 'replace' to overwrite, 'append' to add rows.

        Returns:
            Number of rows written.
        """
        pass

    def write_dimensional_model(
        self,
        dimensions: dict[str, pd.DataFrame],
        facts: dict[str, pd.DataFrame],
    ) -> dict[str, int]:
        """Write complete dimensional model (dimensions and facts).

        Args:
            dimensions: Dict of dimension_name -> DataFrame.
            facts: Dict of fact_name -> DataFrame.

        Returns:
            Dict of table_name -> row_count.
        """
        results: dict[str, int] = {}

        # Write dimensions first (facts depend on them)
        for name, df in dimensions.items():
            results[name] = self.write_table(name, df)

        # Write facts
        for name, df in facts.items():
            results[name] = self.write_table(name, df)

        return results

    @abstractmethod
    def get_table_list(self) -> list[str]:
        """Get list of tables in the schema.

        Returns:
            List of table names.
        """
        pass

    @abstractmethod
    def get_table_stats(self) -> pd.DataFrame:
        """Get statistics for all tables in schema.

        Returns:
            DataFrame with columns: table_name, row_count, column_count.
        """
        pass

    @abstractmethod
    def query(self, sql: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame.

        Args:
            sql: SQL query string.

        Returns:
            Query results as DataFrame.
        """
        pass

    @abstractmethod
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the schema.

        Args:
            table_name: Name of the table.

        Returns:
            True if table exists.
        """
        pass

    @property
    @abstractmethod
    def full_table_prefix(self) -> str:
        """Return the fully qualified table name prefix.

        Examples:
            DuckDB: 'analytics'
            Databricks: 'healthsim.gold'

        Returns:
            Table prefix string.
        """
        pass

    @abstractmethod
    def drop_table(self, table_name: str) -> bool:
        """Drop a table if it exists.

        Args:
            table_name: Name of the table to drop.

        Returns:
            True if dropped, False if table didn't exist.
        """
        pass

    def drop_all_tables(self) -> int:
        """Drop all tables in schema.

        Returns:
            Count of tables dropped.
        """
        tables = self.get_table_list()
        for table in tables:
            self.drop_table(table)
        return len(tables)

    def health_check(self) -> dict[str, Any]:
        """Verify connection and return status.

        Returns:
            Dict with 'healthy', 'message', and target-specific info.
        """
        try:
            self.connect()
            tables = self.get_table_list()
            return {
                "healthy": True,
                "message": "Connected successfully",
                "target": self.TARGET_NAME,
                "table_count": len(tables),
            }
        except Exception as e:
            return {
                "healthy": False,
                "message": str(e),
                "target": self.TARGET_NAME,
            }
        finally:
            self.close()
