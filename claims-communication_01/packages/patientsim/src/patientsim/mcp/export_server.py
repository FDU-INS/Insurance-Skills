"""MCP Server for PatientSim export capabilities.

This module implements a Model Context Protocol (MCP) server that exposes
patient export tools for transforming generated patients into standard
healthcare formats (FHIR, HL7v2, MIMIC-III, JSON).

The export server integrates with the generation server's session state
to export previously generated patients.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from patientsim.formats.fhir.transformer import FHIRTransformer
from patientsim.formats.hl7v2.generator import HL7v2Generator
from patientsim.formats.mimic.transformer import MIMICTransformer
from patientsim.mcp.export_formatters import (
    format_export_error,
    format_export_formats_list,
    format_export_summary,
)
from patientsim.mcp.session import SessionManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("patientsim.mcp.export")

# Initialize MCP server
app = Server("patientsim-export")

# Initialize session manager (shared with generation server)
session_manager = SessionManager()

# Default output directory
OUTPUT_DIR = Path.cwd() / "patientsim_exports"


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP export tools."""
    return [
        Tool(
            name="export_fhir",
            description="Export patients to FHIR R4 Bundle format",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_ids": {
                        "type": "array",
                        "description": "Specific patient IDs to export (exports all if omitted)",
                        "items": {"type": "string"},
                    },
                    "resource_types": {
                        "type": "array",
                        "description": "Filter to specific resource types",
                        "items": {
                            "type": "string",
                            "enum": ["Patient", "Encounter", "Condition", "Observation", "all"],
                        },
                    },
                    "bundle_type": {
                        "type": "string",
                        "description": "FHIR Bundle type",
                        "enum": ["collection", "transaction", "document"],
                        "default": "collection",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Custom output file path (optional)",
                    },
                },
            },
        ),
        Tool(
            name="export_hl7v2",
            description="Export patients to HL7v2 message format",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_ids": {
                        "type": "array",
                        "description": "Specific patient IDs to export",
                        "items": {"type": "string"},
                    },
                    "message_types": {
                        "type": "array",
                        "description": "HL7v2 message types to generate",
                        "items": {
                            "type": "string",
                            "enum": ["ADT^A01", "ADT^A03", "ADT^A08", "ORU^R01", "all"],
                        },
                        "default": ["ADT^A01"],
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Custom output directory path (optional)",
                    },
                },
            },
        ),
        Tool(
            name="export_mimic",
            description="Export patients to MIMIC-III database format",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_ids": {
                        "type": "array",
                        "description": "Specific patient IDs to export",
                        "items": {"type": "string"},
                    },
                    "tables": {
                        "type": "array",
                        "description": "Specific MIMIC tables to export",
                        "items": {
                            "type": "string",
                            "enum": [
                                "PATIENTS",
                                "ADMISSIONS",
                                "DIAGNOSES_ICD",
                                "LABEVENTS",
                                "CHARTEVENTS",
                                "all",
                            ],
                        },
                        "default": ["all"],
                    },
                    "format": {
                        "type": "string",
                        "description": "Output file format",
                        "enum": ["csv", "parquet"],
                        "default": "csv",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Custom output directory path (optional)",
                    },
                },
            },
        ),
        Tool(
            name="export_json",
            description="Export patients to native PatientSim JSON format",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_ids": {
                        "type": "array",
                        "description": "Specific patient IDs to export",
                        "items": {"type": "string"},
                    },
                    "include_metadata": {
                        "type": "boolean",
                        "description": "Include export metadata",
                        "default": True,
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Custom output file path (optional)",
                    },
                },
            },
        ),
        Tool(
            name="list_export_formats",
            description="List available export formats with descriptions",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "export_fhir":
            return await _export_fhir_tool(arguments)
        elif name == "export_hl7v2":
            return await _export_hl7v2_tool(arguments)
        elif name == "export_mimic":
            return await _export_mimic_tool(arguments)
        elif name == "export_json":
            return await _export_json_tool(arguments)
        elif name == "list_export_formats":
            return await _list_export_formats_tool(arguments)
        else:
            error_msg = format_export_error(
                "Unknown Tool",
                f"Tool '{name}' not found",
                "Available tools: export_fhir, export_hl7v2, export_mimic, export_json, list_export_formats",
            )
            return [TextContent(type="text", text=error_msg)]
    except Exception as e:
        logger.exception(f"Error in export tool {name}")
        error_msg = format_export_error(
            name, f"{type(e).__name__}: {str(e)}", "Check the tool parameters and session state"
        )
        return [TextContent(type="text", text=error_msg)]


async def _export_fhir_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Export patients to FHIR R4 format."""
    patient_ids = arguments.get("patient_ids")
    _resource_types = arguments.get("resource_types", ["all"])  # TODO: implement filtering
    bundle_type = arguments.get("bundle_type", "collection")
    output_path = arguments.get("output_path")

    # Get patients from session
    sessions = _get_sessions_by_ids(patient_ids)

    if not sessions:
        error_msg = format_export_error(
            "FHIR",
            "No patients found in session",
            "Generate patients first using the generation server",
        )
        return [TextContent(type="text", text=error_msg)]

    # Extract data from sessions
    patients = [s.patient for s in sessions]
    encounters = [s.encounter for s in sessions if s.encounter]
    diagnoses = [d for s in sessions for d in s.diagnoses]
    labs = [lab for s in sessions for lab in s.labs]
    vitals = [v for s in sessions for v in s.vitals]

    # Transform to FHIR
    transformer = FHIRTransformer()

    try:
        bundle = transformer.create_bundle(
            patients=patients,
            encounters=encounters,
            diagnoses=diagnoses,
            labs=labs,
            vitals=vitals,
            bundle_type=bundle_type,
        )

        # Serialize bundle
        bundle_dict = bundle.model_dump(by_alias=True, exclude_none=True)

        # Write to file
        if not output_path:
            OUTPUT_DIR.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"fhir_bundle_{timestamp}.json"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(bundle_dict, f, indent=2)

        # Count resources
        resource_counts = {}
        for entry in bundle_dict.get("entry", []):
            resource_type = entry.get("resource", {}).get("resourceType", "Unknown")
            resource_counts[resource_type] = resource_counts.get(resource_type, 0) + 1

        # Format response
        response = format_export_summary(
            format_name="FHIR",
            patient_count=len(patients),
            details={"resources": resource_counts},
            file_paths=output_path,
        )

        return [TextContent(type="text", text=response)]

    except Exception as e:
        logger.exception("FHIR export failed")
        error_msg = format_export_error(
            "FHIR",
            f"Export failed: {str(e)}",
            "Ensure patients have valid data for FHIR transformation",
        )
        return [TextContent(type="text", text=error_msg)]


async def _export_hl7v2_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Export patients to HL7v2 message format."""
    patient_ids = arguments.get("patient_ids")
    message_types = arguments.get("message_types", ["ADT^A01"])
    output_dir = arguments.get("output_dir")

    # Get patients from session
    sessions = _get_sessions_by_ids(patient_ids)

    if not sessions:
        error_msg = format_export_error(
            "HL7v2",
            "No patients found in session",
            "Generate patients first using the generation server",
        )
        return [TextContent(type="text", text=error_msg)]

    # Setup output directory
    if not output_dir:
        OUTPUT_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = OUTPUT_DIR / f"hl7v2_messages_{timestamp}"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate messages
    hl7_generator = HL7v2Generator()
    message_counts = {}
    file_paths = []

    try:
        for session in sessions:
            if not session.encounter:
                continue

            # Generate requested message types
            for msg_type in message_types:
                if msg_type == "all" or msg_type == "ADT^A01":
                    # Admission message
                    message = hl7_generator.generate_adt_a01(
                        session.patient,
                        session.encounter,
                        diagnoses=session.diagnoses,
                    )

                    # Write message to file
                    filename = f"{session.patient.mrn}_ADT_A01.hl7"
                    file_path = output_dir / filename
                    with open(file_path, "w") as f:
                        f.write(message)

                    file_paths.append(file_path)
                    message_counts["ADT^A01"] = message_counts.get("ADT^A01", 0) + 1

        # Format response
        response = format_export_summary(
            format_name="HL7v2",
            patient_count=len(sessions),
            details={"messages": message_counts},
            file_paths=file_paths if len(file_paths) <= 5 else [output_dir],
        )

        return [TextContent(type="text", text=response)]

    except Exception as e:
        logger.exception("HL7v2 export failed")
        error_msg = format_export_error(
            "HL7v2",
            f"Export failed: {str(e)}",
            "Ensure patients have encounter data for HL7v2 transformation",
        )
        return [TextContent(type="text", text=error_msg)]


async def _export_mimic_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Export patients to MIMIC-III format."""
    patient_ids = arguments.get("patient_ids")
    tables = arguments.get("tables", ["all"])
    file_format = arguments.get("format", "csv")
    output_dir = arguments.get("output_dir")

    # Get patients from session
    sessions = _get_sessions_by_ids(patient_ids)

    if not sessions:
        error_msg = format_export_error(
            "MIMIC",
            "No patients found in session",
            "Generate patients first using the generation server",
        )
        return [TextContent(type="text", text=error_msg)]

    # Setup output directory
    if not output_dir:
        OUTPUT_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = OUTPUT_DIR / f"mimic_{timestamp}"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract data from sessions
    patients = [s.patient for s in sessions]
    encounters = [s.encounter for s in sessions if s.encounter]
    diagnoses = [d for s in sessions for d in s.diagnoses]
    labs = [lab for s in sessions for lab in s.labs]
    vitals = [v for s in sessions for v in s.vitals]

    # Transform to MIMIC
    transformer = MIMICTransformer()
    table_counts = {}
    file_paths = []

    try:
        # Determine which tables to export
        export_all = "all" in tables

        if export_all or "PATIENTS" in tables:
            patients_df = transformer.transform_patients(patients)
            file_path = output_dir / f"PATIENTS.{file_format}"
            if file_format == "csv":
                patients_df.to_csv(file_path, index=False)
            else:  # parquet
                patients_df.to_parquet(file_path, index=False)
            table_counts["PATIENTS"] = len(patients_df)
            file_paths.append(file_path)

        if (export_all or "ADMISSIONS" in tables) and encounters:
            admissions_df = transformer.transform_admissions(encounters)
            file_path = output_dir / f"ADMISSIONS.{file_format}"
            if file_format == "csv":
                admissions_df.to_csv(file_path, index=False)
            else:
                admissions_df.to_parquet(file_path, index=False)
            table_counts["ADMISSIONS"] = len(admissions_df)
            file_paths.append(file_path)

        if (export_all or "DIAGNOSES_ICD" in tables) and diagnoses:
            diagnoses_df = transformer.transform_diagnoses_icd(diagnoses)
            file_path = output_dir / f"DIAGNOSES_ICD.{file_format}"
            if file_format == "csv":
                diagnoses_df.to_csv(file_path, index=False)
            else:
                diagnoses_df.to_parquet(file_path, index=False)
            table_counts["DIAGNOSES_ICD"] = len(diagnoses_df)
            file_paths.append(file_path)

        if (export_all or "LABEVENTS" in tables) and labs:
            labs_df = transformer.transform_labevents(labs)
            file_path = output_dir / f"LABEVENTS.{file_format}"
            if file_format == "csv":
                labs_df.to_csv(file_path, index=False)
            else:
                labs_df.to_parquet(file_path, index=False)
            table_counts["LABEVENTS"] = len(labs_df)
            file_paths.append(file_path)

        if (export_all or "CHARTEVENTS" in tables) and vitals:
            vitals_df = transformer.transform_chartevents(vitals)
            file_path = output_dir / f"CHARTEVENTS.{file_format}"
            if file_format == "csv":
                vitals_df.to_csv(file_path, index=False)
            else:
                vitals_df.to_parquet(file_path, index=False)
            table_counts["CHARTEVENTS"] = len(vitals_df)
            file_paths.append(file_path)

        # Format response
        response = format_export_summary(
            format_name="MIMIC",
            patient_count=len(patients),
            details={"tables": table_counts},
            file_paths=file_paths if len(file_paths) <= 5 else [output_dir],
        )

        return [TextContent(type="text", text=response)]

    except Exception as e:
        logger.exception("MIMIC export failed")
        error_msg = format_export_error(
            "MIMIC",
            f"Export failed: {str(e)}",
            "Ensure patients have clinical data for MIMIC transformation",
        )
        return [TextContent(type="text", text=error_msg)]


async def _export_json_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Export patients to native JSON format."""
    patient_ids = arguments.get("patient_ids")
    include_metadata = arguments.get("include_metadata", True)
    output_path = arguments.get("output_path")

    # Get patients from session
    sessions = _get_sessions_by_ids(patient_ids)

    if not sessions:
        error_msg = format_export_error(
            "JSON",
            "No patients found in session",
            "Generate patients first using the generation server",
        )
        return [TextContent(type="text", text=error_msg)]

    # Build export data
    export_data = {
        "patients": [s.to_summary() for s in sessions],
    }

    if include_metadata:
        export_data["metadata"] = {
            "export_time": datetime.now().isoformat(),
            "patient_count": len(sessions),
            "format": "PatientSim JSON",
            "version": "1.0",
        }

    # Write to file
    if not output_path:
        OUTPUT_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUT_DIR / f"patients_{timestamp}.json"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)

        # Format response
        response = format_export_summary(
            format_name="JSON",
            patient_count=len(sessions),
            details={},
            file_paths=output_path,
        )

        return [TextContent(type="text", text=response)]

    except Exception as e:
        logger.exception("JSON export failed")
        error_msg = format_export_error(
            "JSON", f"Export failed: {str(e)}", "Check file permissions and disk space"
        )
        return [TextContent(type="text", text=error_msg)]


async def _list_export_formats_tool(_arguments: dict[str, Any]) -> list[TextContent]:
    """List available export formats."""
    response = format_export_formats_list()
    return [TextContent(type="text", text=response)]


def _get_sessions_by_ids(patient_ids: list[str] | None) -> list:
    """Get patient sessions by IDs, or all if None."""
    if not patient_ids:
        return session_manager.list_all()

    sessions = []
    for patient_id in patient_ids:
        session = session_manager.get_by_id(patient_id)
        if not session:
            # Try interpreting as position
            try:
                position = int(patient_id)
                session = session_manager.get_by_position(position)
            except (ValueError, TypeError):
                pass

        if session:
            sessions.append(session)

    return sessions


async def main() -> None:
    """Run the MCP export server."""
    logger.info("Starting PatientSim MCP Export Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
