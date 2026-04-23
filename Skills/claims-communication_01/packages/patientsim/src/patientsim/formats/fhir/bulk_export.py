"""FHIR Bulk Data Export (NDJSON) functionality.

This module provides NDJSON (Newline Delimited JSON) export for FHIR R4
resources, following the FHIR Bulk Data Access specification.

NDJSON Format:
- Each line is a complete, valid JSON object (one FHIR resource)
- Lines are separated by newline characters
- No commas between lines
- Files are organized by resource type (Patient.ndjson, Observation.ndjson, etc.)

Reference:
- FHIR Bulk Data Access IG: https://hl7.org/fhir/uv/bulkdata/
- NDJSON Spec: http://ndjson.org/

Example:
    >>> from patientsim.formats.fhir import FHIRBulkExporter
    >>> exporter = FHIRBulkExporter()
    >>> exporter.export_to_directory(
    ...     patients=patients,
    ...     encounters=encounters,
    ...     output_dir="./fhir_export"
    ... )
    # Creates:
    #   ./fhir_export/Patient.ndjson
    #   ./fhir_export/Encounter.ndjson
    #   ./fhir_export/Condition.ndjson
    #   ./fhir_export/Observation.ndjson
"""

import gzip
import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import IO, Any

from patientsim.core.models import (
    Diagnosis,
    Encounter,
    LabResult,
    Medication,
    Patient,
    VitalSign,
)
from patientsim.formats.fhir.transformer import FHIRTransformer


@dataclass
class BulkExportManifest:
    """Manifest file for FHIR Bulk Data Export.

    The manifest provides metadata about the export including
    timestamps, resource counts, and file locations.

    Attributes:
        transactionTime: When the export was initiated
        request: Original export request URL (simulated)
        requiresAccessToken: Whether files require authentication
        output: List of output file descriptors
        error: List of error file descriptors
    """

    transactionTime: str
    request: str = "https://healthsim.local/$export"
    requiresAccessToken: bool = False
    output: list[dict[str, Any]] = field(default_factory=list)
    error: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "transactionTime": self.transactionTime,
            "request": self.request,
            "requiresAccessToken": self.requiresAccessToken,
            "output": self.output,
            "error": self.error,
        }


@dataclass
class ExportResult:
    """Result of a bulk export operation.

    Attributes:
        output_dir: Directory where files were written
        manifest: Export manifest with file metadata
        resource_counts: Count of resources by type
        total_resources: Total number of resources exported
        files_created: List of created file paths
    """

    output_dir: Path
    manifest: BulkExportManifest
    resource_counts: dict[str, int]
    total_resources: int
    files_created: list[Path]


class FHIRBulkExporter:
    """Export FHIR resources in NDJSON format for Bulk Data Access.

    This class implements the FHIR Bulk Data Export specification,
    generating NDJSON files organized by resource type.

    Features:
    - Exports Patient, Encounter, Condition, Observation resources
    - Optional gzip compression
    - Generates export manifest
    - Streaming export for large datasets
    - Consistent with FHIR Bulk Data Access IG

    Example:
        >>> exporter = FHIRBulkExporter()
        >>> result = exporter.export_to_directory(
        ...     patients=patients,
        ...     encounters=encounters,
        ...     diagnoses=diagnoses,
        ...     output_dir="./export"
        ... )
        >>> print(f"Exported {result.total_resources} resources")
    """

    # Resource type to file name mapping
    RESOURCE_FILES = {
        "Patient": "Patient.ndjson",
        "Encounter": "Encounter.ndjson",
        "Condition": "Condition.ndjson",
        "Observation": "Observation.ndjson",
        "MedicationRequest": "MedicationRequest.ndjson",
    }

    def __init__(self, compress: bool = False) -> None:
        """Initialize bulk exporter.

        Args:
            compress: Whether to gzip compress output files
        """
        self.compress = compress
        self._transformer = FHIRTransformer()

    def _open_file(self, path: Path) -> IO[str]:
        """Open file for writing, with optional compression.

        Args:
            path: File path to open

        Returns:
            File handle for writing
        """
        if self.compress:
            path = path.with_suffix(path.suffix + ".gz")
            return gzip.open(path, "wt", encoding="utf-8")
        return open(path, "w", encoding="utf-8")

    def _write_resource(self, file: IO[str], resource: Any) -> None:
        """Write a single resource as NDJSON line.

        Args:
            file: File handle to write to
            resource: Pydantic model or dict to serialize
        """
        if hasattr(resource, "model_dump"):
            data = resource.model_dump(by_alias=True, exclude_none=True)
        else:
            data = resource
        json_line = json.dumps(data, separators=(",", ":"))
        file.write(json_line + "\n")

    def export_patients(
        self,
        patients: list[Patient],
        output_file: Path,
    ) -> int:
        """Export Patient resources to NDJSON file.

        Args:
            patients: List of Patient objects to export
            output_file: Path to output NDJSON file

        Returns:
            Number of resources exported
        """
        count = 0
        with self._open_file(output_file) as f:
            for patient in patients:
                resource = self._transformer.transform_patient(patient)
                self._write_resource(f, resource)
                count += 1
        return count

    def export_encounters(
        self,
        encounters: list[Encounter],
        output_file: Path,
    ) -> int:
        """Export Encounter resources to NDJSON file.

        Args:
            encounters: List of Encounter objects to export
            output_file: Path to output NDJSON file

        Returns:
            Number of resources exported
        """
        count = 0
        with self._open_file(output_file) as f:
            for encounter in encounters:
                resource = self._transformer.transform_encounter(encounter)
                self._write_resource(f, resource)
                count += 1
        return count

    def export_conditions(
        self,
        diagnoses: list[Diagnosis],
        output_file: Path,
    ) -> int:
        """Export Condition resources to NDJSON file.

        Args:
            diagnoses: List of Diagnosis objects to export
            output_file: Path to output NDJSON file

        Returns:
            Number of resources exported
        """
        count = 0
        with self._open_file(output_file) as f:
            for diagnosis in diagnoses:
                resource = self._transformer.transform_condition(diagnosis)
                self._write_resource(f, resource)
                count += 1
        return count

    def export_observations(
        self,
        labs: list[LabResult] | None = None,
        vitals: list[VitalSign] | None = None,
        output_file: Path | None = None,
    ) -> int:
        """Export Observation resources to NDJSON file.

        Combines lab results and vital signs into Observation resources.

        Args:
            labs: List of LabResult objects
            vitals: List of VitalSign objects
            output_file: Path to output NDJSON file

        Returns:
            Number of resources exported
        """
        if output_file is None:
            raise ValueError("output_file is required")

        count = 0
        with self._open_file(output_file) as f:
            # Export lab observations
            if labs:
                for lab in labs:
                    resource = self._transformer.transform_lab_observation(lab)
                    if resource:  # Skip if no LOINC mapping
                        self._write_resource(f, resource)
                        count += 1

            # Export vital sign observations
            if vitals:
                for vital in vitals:
                    vital_obs = self._transformer.transform_vital_observations(vital)
                    for resource in vital_obs:
                        self._write_resource(f, resource)
                        count += 1

        return count

    def export_to_directory(
        self,
        output_dir: str | Path,
        patients: list[Patient] | None = None,
        encounters: list[Encounter] | None = None,
        diagnoses: list[Diagnosis] | None = None,
        labs: list[LabResult] | None = None,
        vitals: list[VitalSign] | None = None,
        _medications: list[Medication] | None = None,  # Reserved for future use
        create_manifest: bool = True,
    ) -> ExportResult:
        """Export all resources to NDJSON files in a directory.

        Creates one file per resource type following FHIR Bulk Data
        naming conventions.

        Args:
            output_dir: Directory to write NDJSON files
            patients: List of Patient objects
            encounters: List of Encounter objects
            diagnoses: List of Diagnosis objects
            labs: List of LabResult objects
            vitals: List of VitalSign objects
            medications: List of Medication objects (for future use)
            create_manifest: Whether to create export manifest file

        Returns:
            ExportResult with counts and file locations
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        resource_counts: dict[str, int] = {}
        files_created: list[Path] = []
        manifest_output: list[dict[str, Any]] = []

        # Export patients
        if patients:
            file_path = output_path / self.RESOURCE_FILES["Patient"]
            count = self.export_patients(patients, file_path)
            resource_counts["Patient"] = count
            files_created.append(file_path)
            manifest_output.append(
                {
                    "type": "Patient",
                    "url": str(file_path),
                    "count": count,
                }
            )

        # Export encounters
        if encounters:
            file_path = output_path / self.RESOURCE_FILES["Encounter"]
            count = self.export_encounters(encounters, file_path)
            resource_counts["Encounter"] = count
            files_created.append(file_path)
            manifest_output.append(
                {
                    "type": "Encounter",
                    "url": str(file_path),
                    "count": count,
                }
            )

        # Export conditions
        if diagnoses:
            file_path = output_path / self.RESOURCE_FILES["Condition"]
            count = self.export_conditions(diagnoses, file_path)
            resource_counts["Condition"] = count
            files_created.append(file_path)
            manifest_output.append(
                {
                    "type": "Condition",
                    "url": str(file_path),
                    "count": count,
                }
            )

        # Export observations (labs + vitals)
        if labs or vitals:
            file_path = output_path / self.RESOURCE_FILES["Observation"]
            count = self.export_observations(labs, vitals, file_path)
            resource_counts["Observation"] = count
            files_created.append(file_path)
            manifest_output.append(
                {
                    "type": "Observation",
                    "url": str(file_path),
                    "count": count,
                }
            )

        # Create manifest
        manifest = BulkExportManifest(
            transactionTime=datetime.now().isoformat(),
            output=manifest_output,
        )

        if create_manifest:
            manifest_path = output_path / "manifest.json"
            with open(manifest_path, "w") as f:
                json.dump(manifest.to_dict(), f, indent=2)
            files_created.append(manifest_path)

        return ExportResult(
            output_dir=output_path,
            manifest=manifest,
            resource_counts=resource_counts,
            total_resources=sum(resource_counts.values()),
            files_created=files_created,
        )

    def stream_resources(
        self,
        resource_type: str,
        patients: list[Patient] | None = None,
        encounters: list[Encounter] | None = None,
        diagnoses: list[Diagnosis] | None = None,
        labs: list[LabResult] | None = None,
        vitals: list[VitalSign] | None = None,
    ) -> Iterator[str]:
        """Stream NDJSON lines for a specific resource type.

        Useful for large exports or when writing to custom destinations.

        Args:
            resource_type: FHIR resource type to stream
            patients: List of Patient objects
            encounters: List of Encounter objects
            diagnoses: List of Diagnosis objects
            labs: List of LabResult objects
            vitals: List of VitalSign objects

        Yields:
            NDJSON lines (JSON string + newline)
        """
        if resource_type == "Patient" and patients:
            for patient in patients:
                resource = self._transformer.transform_patient(patient)
                data = resource.model_dump(by_alias=True, exclude_none=True)
                yield json.dumps(data, separators=(",", ":")) + "\n"

        elif resource_type == "Encounter" and encounters:
            for encounter in encounters:
                resource = self._transformer.transform_encounter(encounter)
                data = resource.model_dump(by_alias=True, exclude_none=True)
                yield json.dumps(data, separators=(",", ":")) + "\n"

        elif resource_type == "Condition" and diagnoses:
            for diagnosis in diagnoses:
                resource = self._transformer.transform_condition(diagnosis)
                data = resource.model_dump(by_alias=True, exclude_none=True)
                yield json.dumps(data, separators=(",", ":")) + "\n"

        elif resource_type == "Observation":
            if labs:
                for lab in labs:
                    resource = self._transformer.transform_lab_observation(lab)
                    if resource:
                        data = resource.model_dump(by_alias=True, exclude_none=True)
                        yield json.dumps(data, separators=(",", ":")) + "\n"

            if vitals:
                for vital in vitals:
                    vital_obs = self._transformer.transform_vital_observations(vital)
                    for resource in vital_obs:
                        data = resource.model_dump(by_alias=True, exclude_none=True)
                        yield json.dumps(data, separators=(",", ":")) + "\n"

    def to_ndjson_string(
        self,
        patients: list[Patient] | None = None,
        encounters: list[Encounter] | None = None,
        diagnoses: list[Diagnosis] | None = None,
        labs: list[LabResult] | None = None,
        vitals: list[VitalSign] | None = None,
    ) -> dict[str, str]:
        """Export all resources to NDJSON strings by resource type.

        Useful when you need the NDJSON content without writing to disk.

        Args:
            patients: List of Patient objects
            encounters: List of Encounter objects
            diagnoses: List of Diagnosis objects
            labs: List of LabResult objects
            vitals: List of VitalSign objects

        Returns:
            Dictionary mapping resource type to NDJSON string content
        """
        result: dict[str, str] = {}

        if patients:
            lines = list(self.stream_resources("Patient", patients=patients))
            result["Patient"] = "".join(lines)

        if encounters:
            lines = list(self.stream_resources("Encounter", encounters=encounters))
            result["Encounter"] = "".join(lines)

        if diagnoses:
            lines = list(self.stream_resources("Condition", diagnoses=diagnoses))
            result["Condition"] = "".join(lines)

        if labs or vitals:
            lines = list(self.stream_resources("Observation", labs=labs, vitals=vitals))
            result["Observation"] = "".join(lines)

        return result
