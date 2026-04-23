"""FHIR R4 format export functionality.

This module provides transformers to convert PatientSim objects
into FHIR R4 compatible resources and bundles.

Features:
    - FHIRTransformer: Convert to FHIR R4 Bundle format
    - FHIRBulkExporter: NDJSON export for FHIR Bulk Data Access

Example - Bundle Export:
    >>> from patientsim.formats.fhir import FHIRTransformer
    >>> transformer = FHIRTransformer()
    >>> bundle = transformer.create_bundle(patients=patients)

Example - Bulk NDJSON Export:
    >>> from patientsim.formats.fhir import FHIRBulkExporter
    >>> exporter = FHIRBulkExporter()
    >>> result = exporter.export_to_directory(
    ...     patients=patients,
    ...     output_dir="./fhir_export"
    ... )
    >>> print(f"Exported {result.total_resources} resources")
"""

from patientsim.formats.fhir.bulk_export import (
    BulkExportManifest,
    ExportResult,
    FHIRBulkExporter,
)
from patientsim.formats.fhir.transformer import FHIRTransformer

__all__ = [
    "FHIRTransformer",
    "FHIRBulkExporter",
    "BulkExportManifest",
    "ExportResult",
]
