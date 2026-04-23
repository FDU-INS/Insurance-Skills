"""HealthSim Dimensional Output Layer.

Provides analytics-ready star schema output from canonical entities.
This module transforms HealthSim canonical models into dimensional
tables (facts and dimensions) optimized for BI tools, SQL queries,
and data analysis.

The dimensional model is an OUTPUT FORMAT, not a parallel to the
canonical model. Canonical entities remain the source of truth;
dimensional is one of many serialization options alongside FHIR,
HL7v2, X12, etc.

Components:
    - generate_dim_date: Create a comprehensive date dimension with
      US federal holidays for time-based analytics.
    - BaseDimensionalTransformer: Abstract base class for product-specific
      transformers (PatientSim, MemberSim, RxMemberSim).
    - BaseDimensionalWriter: Abstract base class for target writers.
    - DuckDBDimensionalWriter: Write dimensional tables to DuckDB for
      fast local analytics.
    - WriterRegistry: Plugin registry for discovering and creating writers.

Quick Start:
    >>> from healthsim.dimensional import (
    ...     generate_dim_date,
    ...     DuckDBDimensionalWriter,
    ...     WriterRegistry,
    ... )
    >>>
    >>> # Generate date dimension
    >>> dim_date = generate_dim_date('2024-01-01', '2024-12-31')
    >>>
    >>> # Write to DuckDB (direct)
    >>> with DuckDBDimensionalWriter(':memory:') as writer:
    ...     writer.write_table('dim_date', dim_date)
    ...     result = writer.query('SELECT COUNT(*) FROM analytics.dim_date')
    >>>
    >>> # Write via registry (pluggable)
    >>> writer = WriterRegistry.create('duckdb', db_path=':memory:')

For product-specific transformers, see:
    - patientsim.dimensional.PatientDimensionalTransformer
    - membersim.dimensional.MemberSimDimensionalTransformer
    - rxmembersim.dimensional.RxMemberSimDimensionalTransformer
"""

from __future__ import annotations

from healthsim.dimensional.generators.dim_date import generate_dim_date
from healthsim.dimensional.transformers.base import BaseDimensionalTransformer
from healthsim.dimensional.writers.base import BaseDimensionalWriter
from healthsim.dimensional.writers.duckdb_writer import DuckDBDimensionalWriter
from healthsim.dimensional.writers.registry import WriterRegistry

__all__ = [
    # Generators
    "generate_dim_date",
    # Transformers
    "BaseDimensionalTransformer",
    # Writers
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
