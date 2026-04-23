"""Databricks Dimensional Writer.

Writes dimensional models to Databricks Unity Catalog as Delta tables.

Authentication via environment variables (recommended):
    DATABRICKS_HOST: Workspace URL
    DATABRICKS_HTTP_PATH: SQL Warehouse HTTP path
    DATABRICKS_TOKEN: Personal access token

Or pass explicitly to constructor.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import pandas as pd

try:
    from databricks import sql as databricks_sql
    from databricks.sql.client import Connection
except ImportError:
    databricks_sql = None
    Connection = None

from healthsim.dimensional.writers.base import BaseDimensionalWriter

if TYPE_CHECKING:
    from healthsim.config.dimensional import TargetConfig


class DatabricksDimensionalWriter(BaseDimensionalWriter):
    """Write dimensional model to Databricks Unity Catalog.

    This writer persists dimensional tables as Delta tables in
    Databricks Unity Catalog, enabling enterprise-scale analytics
    and governance.

    Class Attributes:
        TARGET_NAME: 'databricks'
        REQUIRED_PACKAGES: ['databricks.sql']

    Authentication:
        Connection credentials can be provided via:
        1. Constructor arguments
        2. Environment variables (DATABRICKS_HOST, DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN)

    Example:
        >>> # Using environment variables for credentials
        >>> with DatabricksDimensionalWriter(catalog='healthsim', schema='gold') as writer:
        ...     writer.write_table('dim_date', dim_date_df)
        ...     stats = writer.get_table_stats()

    Attributes:
        catalog: Unity Catalog name.
        schema: Schema within catalog.
        host: Databricks workspace URL.
        http_path: SQL Warehouse HTTP path.
    """

    TARGET_NAME = "databricks"
    REQUIRED_PACKAGES = ["databricks.sql"]

    def __init__(
        self,
        catalog: str = "healthsim",
        schema: str = "gold",
        host: str | None = None,
        http_path: str | None = None,
        access_token: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize Databricks writer.

        Args:
            catalog: Unity Catalog name.
            schema: Schema within catalog.
            host: Databricks workspace URL (or DATABRICKS_HOST env var).
            http_path: SQL Warehouse HTTP path (or DATABRICKS_HTTP_PATH env var).
            access_token: Personal access token (or DATABRICKS_TOKEN env var).
            **kwargs: Additional arguments (ignored, for compatibility).

        Raises:
            ValueError: If required configuration is missing.
        """
        super().__init__(schema=schema, **kwargs)
        self.catalog = catalog

        # Resolve from args or environment
        self.host = host or os.environ.get("DATABRICKS_HOST")
        self.http_path = http_path or os.environ.get("DATABRICKS_HTTP_PATH")
        self.access_token = access_token or os.environ.get("DATABRICKS_TOKEN")

        self._validate_config()
        self._conn: Connection | None = None

    def _validate_config(self) -> None:
        """Validate required configuration is present.

        Raises:
            ValueError: If required configuration is missing.
        """
        missing = []
        if not self.host:
            missing.append("host (or DATABRICKS_HOST)")
        if not self.http_path:
            missing.append("http_path (or DATABRICKS_HTTP_PATH)")
        if not self.access_token:
            missing.append("access_token (or DATABRICKS_TOKEN)")

        if missing:
            raise ValueError(f"Missing required Databricks configuration: {', '.join(missing)}")

        # Normalize host URL
        self.host = self.host.rstrip("/")
        if not self.host.startswith("https://"):
            self.host = f"https://{self.host}"

    @classmethod
    def from_config(cls, config: TargetConfig) -> DatabricksDimensionalWriter:
        """Create from configuration object.

        Args:
            config: Target configuration with connection settings.

        Returns:
            Configured DatabricksDimensionalWriter instance.
        """
        settings = config.settings
        return cls(
            catalog=settings.get("catalog", "healthsim"),
            schema=settings.get("schema", "gold"),
            host=settings.get("host"),
            http_path=settings.get("http_path"),
            access_token=settings.get("access_token"),
        )

    def connect(self) -> None:
        """Establish connection to Databricks."""
        if self._conn is None:
            self._conn = databricks_sql.connect(
                server_hostname=self.host.replace("https://", ""),
                http_path=self.http_path,
                access_token=self.access_token,
            )
            self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create schema if it doesn't exist."""
        with self._conn.cursor() as cursor:
            cursor.execute(f"USE CATALOG {self.catalog}")
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {self.schema}")
            cursor.execute(f"USE SCHEMA {self.schema}")

    def close(self) -> None:
        """Close the database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    @property
    def connection(self) -> Connection:
        """Get active connection.

        Returns:
            Active Databricks connection.
        """
        if self._conn is None:
            self.connect()
        return self._conn

    def write_table(
        self,
        table_name: str,
        df: pd.DataFrame,
        if_exists: str = "replace",
    ) -> int:
        """Write DataFrame to Databricks Delta table.

        Args:
            table_name: Name of the table (without catalog/schema prefix).
            df: DataFrame to write.
            if_exists: 'replace' to overwrite, 'append' to add rows.

        Returns:
            Number of rows written.

        Raises:
            ValueError: If if_exists is not 'replace' or 'append'.
        """
        full_name = f"{self.catalog}.{self.schema}.{table_name}"

        if df.empty:
            return self._create_empty_table(table_name, df)

        with self.connection.cursor() as cursor:
            if if_exists == "replace":
                columns_sql = self._column_definitions(df)
                cursor.execute(
                    f"""
                    CREATE OR REPLACE TABLE {full_name} (
                        {columns_sql}
                    ) USING DELTA
                """
                )
                self._insert_data(cursor, full_name, df)
            elif if_exists == "append":
                if not self.table_exists(table_name):
                    columns_sql = self._column_definitions(df)
                    cursor.execute(
                        f"""
                        CREATE TABLE {full_name} (
                            {columns_sql}
                        ) USING DELTA
                    """
                    )
                self._insert_data(cursor, full_name, df)
            else:
                raise ValueError("if_exists must be 'replace' or 'append'")

        return len(df)

    def _column_definitions(self, df: pd.DataFrame) -> str:
        """Generate SQL column definitions from DataFrame.

        Args:
            df: DataFrame to analyze.

        Returns:
            SQL column definition string.
        """
        type_map = {
            "int64": "BIGINT",
            "int32": "INT",
            "float64": "DOUBLE",
            "float32": "FLOAT",
            "bool": "BOOLEAN",
            "object": "STRING",
            "string": "STRING",
            "datetime64[ns]": "TIMESTAMP",
        }
        cols = []
        for name, dtype in df.dtypes.items():
            sql_type = type_map.get(str(dtype), "STRING")
            cols.append(f"`{name}` {sql_type}")
        return ", ".join(cols)

    def _insert_data(
        self,
        cursor: Any,
        full_name: str,
        df: pd.DataFrame,
        batch_size: int = 1000,
    ) -> None:
        """Insert DataFrame rows in batches.

        Args:
            cursor: Database cursor.
            full_name: Fully qualified table name.
            df: DataFrame to insert.
            batch_size: Rows per batch.
        """
        if df.empty:
            return

        columns = ", ".join(f"`{c}`" for c in df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO {full_name} ({columns}) VALUES ({placeholders})"

        rows = [tuple(None if pd.isna(v) else v for v in row) for row in df.values]

        for i in range(0, len(rows), batch_size):
            cursor.executemany(sql, rows[i : i + batch_size])

    def _create_empty_table(self, table_name: str, df: pd.DataFrame) -> int:
        """Create empty table with schema.

        Args:
            table_name: Name of the table.
            df: DataFrame with schema.

        Returns:
            0 (no rows written).
        """
        full_name = f"{self.catalog}.{self.schema}.{table_name}"
        columns_sql = self._column_definitions(df)
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE OR REPLACE TABLE {full_name} (
                    {columns_sql}
                ) USING DELTA
            """
            )
        return 0

    def get_table_list(self) -> list[str]:
        """Get list of tables in schema.

        Returns:
            List of table names.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"SHOW TABLES IN {self.catalog}.{self.schema}")
            return [row.tableName for row in cursor.fetchall()]

    def get_table_stats(self) -> pd.DataFrame:
        """Get statistics for all tables.

        Returns:
            DataFrame with table_name, row_count, column_count.
        """
        tables = self.get_table_list()
        stats = []
        with self.connection.cursor() as cursor:
            for table in tables:
                full_name = f"{self.catalog}.{self.schema}.{table}"
                cursor.execute(f"SELECT COUNT(*) as cnt FROM {full_name}")
                row_count = cursor.fetchone().cnt
                cursor.execute(f"DESCRIBE TABLE {full_name}")
                col_count = len(cursor.fetchall())
                stats.append(
                    {
                        "table_name": table,
                        "row_count": row_count,
                        "column_count": col_count,
                    }
                )
        return pd.DataFrame(stats)

    def query(self, sql: str) -> pd.DataFrame:
        """Execute SQL query and return results.

        Args:
            sql: SQL query string.

        Returns:
            Query results as DataFrame.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                columns = [d[0] for d in cursor.description] if cursor.description else []
                return pd.DataFrame(columns=columns)
            columns = [d[0] for d in cursor.description]
            return pd.DataFrame([list(r) for r in results], columns=columns)

    def table_exists(self, table_name: str) -> bool:
        """Check if table exists.

        Args:
            table_name: Name of the table.

        Returns:
            True if table exists.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT 1 FROM {self.catalog}.information_schema.tables
                    WHERE table_catalog = '{self.catalog}'
                    AND table_schema = '{self.schema}'
                    AND table_name = '{table_name}'
                """
                )
                return cursor.fetchone() is not None
        except Exception:
            return False

    @property
    def full_table_prefix(self) -> str:
        """Return catalog.schema prefix.

        Returns:
            Fully qualified prefix (e.g., 'healthsim.gold').
        """
        return f"{self.catalog}.{self.schema}"

    def drop_table(self, table_name: str) -> bool:
        """Drop a table if it exists.

        Args:
            table_name: Name of the table to drop.

        Returns:
            True if dropped, False if table didn't exist.
        """
        if not self.table_exists(table_name):
            return False
        full_name = f"{self.catalog}.{self.schema}.{table_name}"
        with self.connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {full_name}")
        return True
