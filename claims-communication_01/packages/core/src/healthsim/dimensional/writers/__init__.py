"""Writers for persisting dimensional model data.

This module provides pluggable writers for various target platforms.
Writers are registered automatically when their required packages
are available.

Available Writers:
    - DuckDBDimensionalWriter: Write to local DuckDB databases (always available)
    - DatabricksDimensionalWriter: Write to Databricks Unity Catalog
      (requires databricks-sql-connector)

Usage:
    >>> from healthsim.dimensional.writers import WriterRegistry, DuckDBDimensionalWriter
    >>>
    >>> # Direct instantiation
    >>> with DuckDBDimensionalWriter('analytics.duckdb') as writer:
    ...     writer.write_table('dim_date', df)
    >>>
    >>> # Via registry
    >>> writer = WriterRegistry.create('duckdb', db_path='analytics.duckdb')
    >>>
    >>> # Check available writers
    >>> WriterRegistry.list_available()
    ['duckdb', 'databricks']
"""

from __future__ import annotations

from healthsim.dimensional.writers.base import BaseDimensionalWriter
from healthsim.dimensional.writers.duckdb_writer import DuckDBDimensionalWriter
from healthsim.dimensional.writers.registry import WriterRegistry

__all__ = [
    "BaseDimensionalWriter",
    "DuckDBDimensionalWriter",
    "WriterRegistry",
]

# Conditionally export Databricks writer
try:
    from healthsim.dimensional.writers.databricks_writer import (
        DatabricksDimensionalWriter,
    )

    __all__.append("DatabricksDimensionalWriter")
except ImportError:
    DatabricksDimensionalWriter = None  # type: ignore
