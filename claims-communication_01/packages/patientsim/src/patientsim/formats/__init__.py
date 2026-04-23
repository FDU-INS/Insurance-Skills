"""Healthcare data format handlers (HL7v2, FHIR, CDA, etc.).

This module provides format transformers for generating healthcare
data in standard interchange formats.

Available formats:
- C-CDA: Consolidated Clinical Document Architecture (XML)
- FHIR R4: Fast Healthcare Interoperability Resources (JSON/NDJSON)
- JSON/CSV: Simple export utilities

Example - C-CDA:
    >>> from patientsim.formats.ccda import CCDATransformer, CCDAConfig, DocumentType
    >>> config = CCDAConfig(
    ...     document_type=DocumentType.CCD,
    ...     organization_name="Example Hospital",
    ...     organization_oid="2.16.840.1.113883.3.1234",
    ... )
    >>> transformer = CCDATransformer(config)
    >>> xml = transformer.transform(patient, encounters, diagnoses)

Example - FHIR Bundle:
    >>> from patientsim.formats.fhir import FHIRTransformer
    >>> transformer = FHIRTransformer()
    >>> bundle = transformer.create_bundle(patients=patients)

Example - FHIR Bulk Export (NDJSON):
    >>> from patientsim.formats.fhir import FHIRBulkExporter
    >>> exporter = FHIRBulkExporter()
    >>> result = exporter.export_to_directory(
    ...     patients=patients,
    ...     output_dir="./fhir_export"
    ... )

Example - JSON/CSV Export:
    >>> from patientsim.formats import to_json, patients_to_csv
    >>> json_str = to_json(patient)
    >>> csv_str = patients_to_csv([patient1, patient2])
"""

from patientsim.formats.ccda import (
    CCDAConfig,
    CCDATransformer,
    CCDAValidator,
    DocumentType,
    ValidationResult,
)
from patientsim.formats.export import (
    JSONEncoder,
    diagnoses_to_csv,
    encounters_to_csv,
    labs_to_csv,
    medications_to_csv,
    patients_to_csv,
    to_csv,
    to_json,
    vitals_to_csv,
)
from patientsim.formats.fhir import (
    BulkExportManifest,
    ExportResult,
    FHIRBulkExporter,
    FHIRTransformer,
)

__all__ = [
    # C-CDA
    "CCDAConfig",
    "CCDATransformer",
    "CCDAValidator",
    "DocumentType",
    "ValidationResult",
    # FHIR
    "FHIRTransformer",
    "FHIRBulkExporter",
    "BulkExportManifest",
    "ExportResult",
    # JSON/CSV Export
    "JSONEncoder",
    "to_json",
    "to_csv",
    "patients_to_csv",
    "encounters_to_csv",
    "diagnoses_to_csv",
    "medications_to_csv",
    "labs_to_csv",
    "vitals_to_csv",
]
