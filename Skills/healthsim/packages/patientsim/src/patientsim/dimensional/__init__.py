"""PatientSim Dimensional Output Layer.

Provides dimensional (star schema) output from PatientSim canonical models
for analytics, BI tools, and data warehousing.

This module transforms PatientSim entities (Patient, Encounter, Diagnosis,
Procedure, Medication, LabResult, VitalSign) into dimension and fact tables
optimized for analytical queries.

Example:
    >>> from patientsim.core import PatientGenerator
    >>> from patientsim.dimensional import PatientDimensionalTransformer
    >>> from healthsim.dimensional import DuckDBDimensionalWriter, generate_dim_date
    >>>
    >>> # Generate sample data
    >>> gen = PatientGenerator(seed=42)
    >>> patient = gen.generate_patient()
    >>> encounter = gen.generate_encounter(patient)
    >>> diagnosis = gen.generate_diagnosis(patient, encounter)
    >>>
    >>> # Transform to dimensional format
    >>> transformer = PatientDimensionalTransformer(
    ...     patients=[patient],
    ...     encounters=[encounter],
    ...     diagnoses=[diagnosis],
    ... )
    >>> dimensions, facts = transformer.transform()
    >>>
    >>> # Write to DuckDB
    >>> with DuckDBDimensionalWriter(':memory:') as writer:
    ...     dim_date = generate_dim_date('2024-01-01', '2024-12-31')
    ...     writer.write_dimensional_model(
    ...         {'dim_date': dim_date, **dimensions},
    ...         facts
    ...     )

See Also:
    - healthsim.dimensional.generate_dim_date: Date dimension generator
    - healthsim.dimensional.DuckDBDimensionalWriter: DuckDB output writer
    - healthsim.dimensional.BaseDimensionalTransformer: Base transformer class
"""

from __future__ import annotations

from .transformer import PatientDimensionalTransformer

__all__ = [
    "PatientDimensionalTransformer",
]
