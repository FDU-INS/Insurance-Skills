"""
Response formatters for MCP export server.

Formats export results as human-readable summaries with file information
and next steps.
"""

from pathlib import Path
from typing import Any


def format_export_summary(
    format_name: str,
    patient_count: int,
    details: dict[str, Any],
    file_paths: list[Path] | Path,
    validation_warnings: list[str] | None = None,
) -> str:
    """
    Format an export summary.

    Args:
        format_name: Name of the export format (FHIR, HL7v2, MIMIC, JSON)
        patient_count: Number of patients exported
        details: Format-specific details (resource counts, message types, etc.)
        file_paths: Path(s) to exported file(s)
        validation_warnings: Optional validation warnings

    Returns:
        Markdown-formatted export summary
    """
    lines = [
        f"## {format_name} Export Complete",
        "",
        f"**Patients Exported**: {patient_count}",
        "",
    ]

    # Add format-specific details
    if "resources" in details:
        lines.extend(
            [
                "### FHIR Resources Generated",
                "",
            ]
        )
        for resource_type, count in details["resources"].items():
            lines.append(f"- **{resource_type}**: {count}")
        lines.append("")

    if "messages" in details:
        lines.extend(
            [
                "### HL7v2 Messages Generated",
                "",
            ]
        )
        for message_type, count in details["messages"].items():
            lines.append(f"- **{message_type}**: {count}")
        lines.append("")

    if "tables" in details:
        lines.extend(
            [
                "### MIMIC-III Tables",
                "",
            ]
        )
        for table_name, row_count in details["tables"].items():
            lines.append(f"- **{table_name}**: {row_count} rows")
        lines.append("")

    # File information
    if isinstance(file_paths, list):
        if len(file_paths) == 1:
            lines.extend(
                [
                    "### Output File",
                    "",
                    f"```\n{file_paths[0]}\n```",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    "### Output Files",
                    "",
                ]
            )
            for file_path in file_paths:
                lines.append(f"- `{file_path}`")
            lines.append("")
    else:
        lines.extend(
            [
                "### Output File",
                "",
                f"```\n{file_paths}\n```",
                "",
            ]
        )

    # Validation warnings
    if validation_warnings:
        lines.extend(
            [
                "### ⚠️ Validation Warnings",
                "",
            ]
        )
        for warning in validation_warnings:
            lines.append(f"- {warning}")
        lines.append("")

    # Next steps based on format
    next_steps = _get_next_steps(format_name)
    if next_steps:
        lines.extend(
            [
                "### Next Steps",
                "",
            ]
        )
        for step in next_steps:
            lines.append(f"- {step}")

    return "\n".join(lines)


def format_export_formats_list() -> str:
    """
    Format the list of available export formats.

    Returns:
        Markdown-formatted list of export formats
    """
    formats = {
        "FHIR R4": {
            "description": "HL7 FHIR R4 resources in JSON format",
            "use_cases": [
                "Testing FHIR servers and APIs",
                "Healthcare interoperability",
                "Modern EMR integration",
            ],
            "output": "Bundle resource with Patient, Encounter, Condition, Observation, etc.",
        },
        "HL7v2": {
            "description": "HL7 Version 2 messages (pipe-delimited)",
            "use_cases": [
                "Interface engine testing",
                "Legacy system integration",
                "ADT message workflows",
            ],
            "output": "Individual message files (ADT^A01, ADT^A03, ORU^R01, etc.)",
        },
        "MIMIC-III": {
            "description": "MIMIC-III critical care database format",
            "use_cases": [
                "Research database population",
                "Analytics and data science",
                "ML model training",
            ],
            "output": "CSV/Parquet tables (PATIENTS, ADMISSIONS, DIAGNOSES_ICD, etc.)",
        },
        "JSON": {
            "description": "Native PatientSim JSON format",
            "use_cases": [
                "Custom data processing",
                "Debugging and inspection",
                "Programmatic access",
            ],
            "output": "Structured JSON with full patient data",
        },
    }

    lines = [
        "## Available Export Formats",
        "",
    ]

    for format_name, info in formats.items():
        lines.extend(
            [
                f"### {format_name}",
                "",
                f"**Description**: {info['description']}",
                "",
                "**Use Cases**:",
            ]
        )
        for use_case in info["use_cases"]:
            lines.append(f"- {use_case}")

        lines.extend(
            [
                "",
                f"**Output**: {info['output']}",
                "",
            ]
        )

    return "\n".join(lines)


def _get_next_steps(format_name: str) -> list[str]:
    """Get format-specific next steps."""
    steps = {
        "FHIR": [
            "Load the Bundle into a FHIR server using POST /",
            "Validate resources with the FHIR validator",
            "Test FHIR API search and read operations",
        ],
        "HL7v2": [
            "Send messages to your interface engine for processing",
            "Verify message parsing and routing",
            "Test downstream system integration",
        ],
        "MIMIC": [
            "Import CSV files into your research database",
            "Run analytics queries on the data",
            "Train ML models with the synthetic dataset",
        ],
        "JSON": [
            "Process the data with custom scripts",
            "Inspect patient details for debugging",
            "Transform to other formats as needed",
        ],
    }

    return steps.get(format_name, [])


def format_export_error(
    format_name: str,
    error_message: str,
    suggestion: str | None = None,
) -> str:
    """
    Format an export error message.

    Args:
        format_name: Name of the export format
        error_message: Error description
        suggestion: Optional suggestion for fixing the error

    Returns:
        Formatted error message
    """
    lines = [
        f"## ❌ {format_name} Export Failed",
        "",
        f"**Error**: {error_message}",
    ]

    if suggestion:
        lines.extend(
            [
                "",
                f"**Suggestion**: {suggestion}",
            ]
        )

    return "\n".join(lines)
