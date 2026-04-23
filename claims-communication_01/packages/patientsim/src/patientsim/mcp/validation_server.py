"""MCP Server for PatientSim validation capabilities.

This module implements a Model Context Protocol (MCP) server that exposes
patient validation tools for checking clinical plausibility and data integrity.
"""

import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from patientsim.mcp.session import SessionManager
from patientsim.mcp.validation_formatters import (
    format_export_validation_summary,
    format_fix_summary,
    format_rule_explanation,
    format_validation_error,
    format_validation_summary,
)
from patientsim.validation import (
    ValidationResult,
    ValidationSeverity,
    validate_patient_record,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("patientsim.mcp.validation")

# Initialize MCP server
app = Server("patientsim-validation")

# Shared session manager (imported from generation server)
session_manager = SessionManager()


# Validation rule documentation
VALIDATION_RULES = {
    "TEMP_001": {
        "description": "Checks that death date is not before birth date",
        "severity": "error",
        "rationale": "A patient cannot die before they are born. This indicates a data entry error.",
        "passing_example": "Birth: 1950-01-01, Death: 2020-01-01",
        "failing_example": "Birth: 1950-01-01, Death: 1940-01-01",
        "fix_guidance": "Correct the death_date or birth_date to ensure temporal consistency.",
    },
    "TEMP_002": {
        "description": "Checks that admission time is not in the future",
        "severity": "warning",
        "rationale": "Future admissions may be scheduled appointments, but typically should not be in test data.",
        "passing_example": "Admission: 2024-01-15 (today is 2024-01-20)",
        "failing_example": "Admission: 2024-02-01 (today is 2024-01-20)",
        "fix_guidance": "Set admission_time to a date in the past or present.",
    },
    "TEMP_003": {
        "description": "Checks for unusually long length of stay (> 1 year)",
        "severity": "warning",
        "rationale": "Hospital stays over 1 year are rare and may indicate incorrect discharge time.",
        "passing_example": "Admission: 2024-01-01, Discharge: 2024-01-15 (14 days)",
        "failing_example": "Admission: 2020-01-01, Discharge: 2023-01-01 (3 years)",
        "fix_guidance": "Verify discharge_time is correct or split into multiple encounters.",
    },
    "TEMP_004": {
        "description": "Checks that length of stay is positive",
        "severity": "error",
        "rationale": "Discharge cannot be before admission. This indicates a data error.",
        "passing_example": "Admission: 2024-01-01 10:00, Discharge: 2024-01-02 14:00",
        "failing_example": "Admission: 2024-01-02 10:00, Discharge: 2024-01-01 14:00",
        "fix_guidance": "Ensure discharge_time is after admission_time.",
    },
    "TEMP_005": {
        "description": "Checks that lab collection time is not before encounter admission",
        "severity": "warning",
        "rationale": "Labs collected before admission may be outpatient labs or data errors.",
        "passing_example": "Admission: 2024-01-01 10:00, Lab collected: 2024-01-01 15:00",
        "failing_example": "Admission: 2024-01-01 10:00, Lab collected: 2023-12-31 15:00",
        "fix_guidance": "Adjust lab collected_time or remove encounter association.",
    },
    "TEMP_006": {
        "description": "Checks that lab collection time is not after encounter discharge",
        "severity": "warning",
        "rationale": "Labs after discharge may be follow-up labs or data errors.",
        "passing_example": "Discharge: 2024-01-05, Lab collected: 2024-01-03",
        "failing_example": "Discharge: 2024-01-05, Lab collected: 2024-01-10",
        "fix_guidance": "Adjust lab collected_time or remove encounter association.",
    },
    "REF_001": {
        "description": "Checks that diagnosis patient_mrn matches patient MRN",
        "severity": "error",
        "rationale": "Referential integrity ensures data consistency across records.",
        "passing_example": "Patient MRN: MRN123, Diagnosis MRN: MRN123",
        "failing_example": "Patient MRN: MRN123, Diagnosis MRN: MRN456",
        "fix_guidance": "Update diagnosis.patient_mrn to match patient.mrn.",
    },
    "REF_002": {
        "description": "Checks that encounter patient_mrn matches patient MRN",
        "severity": "error",
        "rationale": "Encounter must belong to the correct patient.",
        "passing_example": "Patient MRN: MRN123, Encounter MRN: MRN123",
        "failing_example": "Patient MRN: MRN123, Encounter MRN: MRN456",
        "fix_guidance": "Update encounter.patient_mrn to match patient.mrn.",
    },
    "REF_003": {
        "description": "Checks that lab patient_mrn matches patient MRN",
        "severity": "error",
        "rationale": "Lab results must belong to the correct patient.",
        "passing_example": "Patient MRN: MRN123, Lab MRN: MRN123",
        "failing_example": "Patient MRN: MRN123, Lab MRN: MRN456",
        "fix_guidance": "Update lab.patient_mrn to match patient.mrn.",
    },
    "REF_004": {
        "description": "Checks that lab encounter_id matches encounter ID",
        "severity": "error",
        "rationale": "Lab must be associated with the correct encounter.",
        "passing_example": "Encounter ID: ENC123, Lab encounter_id: ENC123",
        "failing_example": "Encounter ID: ENC123, Lab encounter_id: ENC456",
        "fix_guidance": "Update lab.encounter_id to match encounter.encounter_id.",
    },
    "CLIN_001": {
        "description": "Checks for geriatric conditions in young patients",
        "severity": "warning",
        "rationale": "Some conditions (CAD, heart failure, CKD) are more common in older adults.",
        "passing_example": "Patient age 65 with CAD",
        "failing_example": "Patient age 25 with CAD",
        "fix_guidance": "Verify diagnosis is correct for patient's age.",
    },
    "CLIN_002": {
        "description": "Checks for female-only conditions in non-female patients",
        "severity": "error",
        "rationale": "Conditions like pregnancy can only occur in females.",
        "passing_example": "Female patient with pregnancy diagnosis",
        "failing_example": "Male patient with pregnancy diagnosis",
        "fix_guidance": "Correct the gender or remove the diagnosis.",
    },
    "CLIN_003": {
        "description": "Checks for male-only conditions in non-male patients",
        "severity": "error",
        "rationale": "Conditions like prostate disease can only occur in males.",
        "passing_example": "Male patient with prostate disease",
        "failing_example": "Female patient with prostate disease",
        "fix_guidance": "Correct the gender or remove the diagnosis.",
    },
    "CLIN_004": {
        "description": "Checks that medications have appropriate indications",
        "severity": "info",
        "rationale": "Medications should typically be prescribed for documented conditions.",
        "passing_example": "Patient with diabetes taking Metformin",
        "failing_example": "Patient without diabetes taking Metformin",
        "fix_guidance": "Add the indicated diagnosis or verify medication is correct.",
    },
    "CLIN_005": {
        "description": "Checks that appropriate labs are ordered for conditions",
        "severity": "info",
        "rationale": "Certain conditions require specific monitoring labs.",
        "passing_example": "Patient with diabetes has HbA1c and glucose labs",
        "failing_example": "Patient with diabetes has no glucose-related labs",
        "fix_guidance": "Consider adding typical labs for the condition.",
    },
    "CLIN_006": {
        "description": "Checks for critically high temperature (>106°F)",
        "severity": "warning",
        "rationale": "Temperatures above 106°F are life-threatening and rare.",
        "passing_example": "Temperature: 101.5°F",
        "failing_example": "Temperature: 108°F",
        "fix_guidance": "Verify temperature reading or adjust to realistic value.",
    },
    "CLIN_007": {
        "description": "Checks for critically low temperature (<92°F)",
        "severity": "warning",
        "rationale": "Temperatures below 92°F indicate severe hypothermia.",
        "passing_example": "Temperature: 97.5°F",
        "failing_example": "Temperature: 88°F",
        "fix_guidance": "Verify temperature reading or adjust to realistic value.",
    },
    "CLIN_008": {
        "description": "Checks for critically high heart rate (>180 bpm)",
        "severity": "warning",
        "rationale": "Heart rates above 180 are typically seen only in critical conditions.",
        "passing_example": "Heart rate: 110 bpm",
        "failing_example": "Heart rate: 220 bpm",
        "fix_guidance": "Verify heart rate or adjust to realistic value.",
    },
    "CLIN_009": {
        "description": "Checks for critically low heart rate (<40 bpm)",
        "severity": "warning",
        "rationale": "Heart rates below 40 indicate severe bradycardia.",
        "passing_example": "Heart rate: 65 bpm",
        "failing_example": "Heart rate: 30 bpm",
        "fix_guidance": "Verify heart rate or adjust to realistic value.",
    },
    "CLIN_010": {
        "description": "Checks for critically low oxygen saturation (<85%)",
        "severity": "warning",
        "rationale": "SpO2 below 85% indicates severe hypoxia.",
        "passing_example": "SpO2: 96%",
        "failing_example": "SpO2: 75%",
        "fix_guidance": "Verify oxygen saturation or adjust to realistic value.",
    },
    "CLIN_011": {
        "description": "Checks for unusually narrow pulse pressure (<20 mmHg)",
        "severity": "warning",
        "rationale": "Narrow pulse pressure may indicate cardiac tamponade or severe hypovolemia.",
        "passing_example": "BP: 120/80 (pulse pressure 40)",
        "failing_example": "BP: 100/95 (pulse pressure 5)",
        "fix_guidance": "Verify blood pressure readings.",
    },
    "CLIN_012": {
        "description": "Checks for unusually wide pulse pressure (>100 mmHg)",
        "severity": "info",
        "rationale": "Wide pulse pressure may indicate aortic regurgitation or other conditions.",
        "passing_example": "BP: 120/80 (pulse pressure 40)",
        "failing_example": "BP: 180/60 (pulse pressure 120)",
        "fix_guidance": "Wide pulse pressure may be clinically significant but not necessarily an error.",
    },
    "CLIN_013": {
        "description": "Checks for severely underweight BMI (<16)",
        "severity": "warning",
        "rationale": "BMI below 16 indicates severe malnutrition.",
        "passing_example": "BMI: 22",
        "failing_example": "BMI: 14",
        "fix_guidance": "Verify BMI calculation or adjust weight/height.",
    },
    "CLIN_014": {
        "description": "Checks for severely obese BMI (>40)",
        "severity": "info",
        "rationale": "BMI above 40 is class III obesity, clinically significant but not an error.",
        "passing_example": "BMI: 28",
        "failing_example": "BMI: 45",
        "fix_guidance": "BMI >40 is valid but clinically significant.",
    },
}


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available validation tools."""
    return [
        Tool(
            name="validate_patients",
            description="Validate patient data for clinical plausibility and structural integrity",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_ids": {
                        "type": "array",
                        "description": "Patient IDs to validate (omit for all)",
                        "items": {"type": "string"},
                    },
                    "validation_level": {
                        "type": "string",
                        "description": "Validation thoroughness",
                        "enum": ["quick", "standard", "thorough"],
                        "default": "standard",
                    },
                },
            },
        ),
        Tool(
            name="validate_for_export",
            description="Validate patients for specific export format requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_ids": {
                        "type": "array",
                        "description": "Patient IDs to validate (omit for all)",
                        "items": {"type": "string"},
                    },
                    "target_format": {
                        "type": "string",
                        "description": "Target export format",
                        "enum": ["fhir", "hl7v2", "mimic"],
                    },
                },
                "required": ["target_format"],
            },
        ),
        Tool(
            name="fix_validation_issues",
            description="Auto-fix common validation issues in patient data",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "Patient ID to fix",
                    },
                    "issue_type": {
                        "type": "string",
                        "description": "Type of issue to fix (omit for all auto-fixable)",
                        "enum": ["referential", "temporal", "all"],
                        "default": "all",
                    },
                    "fix_strategy": {
                        "type": "string",
                        "description": "How aggressive to be with fixes",
                        "enum": ["conservative", "aggressive"],
                        "default": "conservative",
                    },
                },
                "required": ["patient_id"],
            },
        ),
        Tool(
            name="explain_validation_rule",
            description="Get detailed explanation of a validation rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "rule_code": {
                        "type": "string",
                        "description": "Validation rule code (e.g., TEMP_001)",
                    },
                },
                "required": ["rule_code"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "validate_patients":
            return await _validate_patients_tool(arguments)
        elif name == "validate_for_export":
            return await _validate_for_export_tool(arguments)
        elif name == "fix_validation_issues":
            return await _fix_validation_issues_tool(arguments)
        elif name == "explain_validation_rule":
            return await _explain_validation_rule_tool(arguments)
        else:
            error_msg = format_validation_error(
                f"Unknown tool: {name}",
                "Available tools: validate_patients, validate_for_export, fix_validation_issues, explain_validation_rule",
            )
            return [TextContent(type="text", text=error_msg)]
    except Exception as e:
        logger.exception(f"Error in tool {name}")
        error_msg = format_validation_error(
            f"{type(e).__name__}: {str(e)}", "Please check the tool parameters and try again."
        )
        return [TextContent(type="text", text=error_msg)]


def _get_sessions_by_ids(patient_ids: list[str] | None) -> list[Any]:
    """Get patient sessions by IDs or all if None."""
    if not patient_ids:
        return session_manager.list_all()

    sessions = []
    for patient_id in patient_ids:
        # Try by ID first
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


async def _validate_patients_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Validate patients with configurable thoroughness."""
    patient_ids = arguments.get("patient_ids")
    validation_level = arguments.get("validation_level", "standard")

    # Get patients
    sessions = _get_sessions_by_ids(patient_ids)

    if not sessions:
        error_msg = format_validation_error(
            "No patients found to validate",
            "Generate patients first using the generation server or specify valid patient IDs.",
        )
        return [TextContent(type="text", text=error_msg)]

    # Validate each patient
    patient_results: dict[str, ValidationResult] = {}

    for session in sessions:
        # Run validation
        result = validate_patient_record(
            patient=session.patient,
            encounters=[session.encounter] if session.encounter else None,
            diagnoses=session.diagnoses if session.diagnoses else None,
            labs=session.labs if session.labs else None,
            vitals=session.vitals if session.vitals else None,
        )

        # Filter by validation level
        if validation_level == "quick":
            # Only show errors
            result.issues = [i for i in result.issues if i.severity == ValidationSeverity.ERROR]
        elif validation_level == "standard":
            # Show errors and warnings
            result.issues = [
                i
                for i in result.issues
                if i.severity in [ValidationSeverity.ERROR, ValidationSeverity.WARNING]
            ]
        # thorough: show everything

        patient_results[session.id] = result

    # Format response
    response = format_validation_summary(patient_results, validation_level)

    return [TextContent(type="text", text=response)]


async def _validate_for_export_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Validate patients for specific export format."""
    patient_ids = arguments.get("patient_ids")
    target_format = arguments["target_format"]

    # Get patients
    sessions = _get_sessions_by_ids(patient_ids)

    if not sessions:
        error_msg = format_validation_error(
            "No patients found to validate",
            "Generate patients first or specify valid patient IDs.",
        )
        return [TextContent(type="text", text=error_msg)]

    # Validate each patient
    patient_results: dict[str, ValidationResult] = {}
    format_specific_issues: list[str] = []

    for session in sessions:
        result = validate_patient_record(
            patient=session.patient,
            encounters=[session.encounter] if session.encounter else None,
            diagnoses=session.diagnoses if session.diagnoses else None,
            labs=session.labs if session.labs else None,
            vitals=session.vitals if session.vitals else None,
        )

        # Add format-specific checks
        if target_format == "fhir":
            # FHIR requires patient name and gender
            if not session.patient.given_name or not session.patient.family_name:
                result.add_issue(
                    code="FHIR_001",
                    message="FHIR requires patient name (given_name and family_name)",
                    severity=ValidationSeverity.ERROR,
                    field_path="name",
                )
        elif target_format == "hl7v2":
            # HL7v2 ADT requires encounter
            if not session.encounter:
                result.add_issue(
                    code="HL7_001",
                    message="HL7v2 ADT messages require an encounter",
                    severity=ValidationSeverity.ERROR,
                    field_path="encounter",
                )
                format_specific_issues.append(
                    f"Patient {session.id} missing encounter (required for ADT messages)"
                )
        elif target_format == "mimic":
            # MIMIC requires admission for ADMISSIONS table
            if not session.encounter:
                result.add_issue(
                    code="MIMIC_001",
                    message="MIMIC format requires encounter for ADMISSIONS table",
                    severity=ValidationSeverity.ERROR,
                    field_path="encounter",
                )
                format_specific_issues.append(
                    f"Patient {session.id} missing encounter (required for ADMISSIONS table)"
                )

            # MIMIC requires ICD codes for DIAGNOSES_ICD
            if not session.diagnoses:
                format_specific_issues.append(
                    f"Patient {session.id} has no diagnoses (DIAGNOSES_ICD table will be empty)"
                )

        patient_results[session.id] = result

    # Format response
    response = format_export_validation_summary(
        patient_results, target_format, format_specific_issues
    )

    return [TextContent(type="text", text=response)]


async def _fix_validation_issues_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Auto-fix common validation issues."""
    patient_id = arguments["patient_id"]
    issue_type = arguments.get("issue_type", "all")
    _fix_strategy = arguments.get("fix_strategy", "conservative")  # TODO: implement

    # Get patient session
    session = session_manager.get_by_id(patient_id)
    if not session:
        # Try position
        try:
            position = int(patient_id)
            session = session_manager.get_by_position(position)
        except (ValueError, TypeError):
            pass

    if not session:
        error_msg = format_validation_error(
            f"Patient '{patient_id}' not found",
            f"Current session has {session_manager.count()} patients.",
        )
        return [TextContent(type="text", text=error_msg)]

    # Validate to find issues
    result = validate_patient_record(
        patient=session.patient,
        encounters=[session.encounter] if session.encounter else None,
        diagnoses=session.diagnoses if session.diagnoses else None,
        labs=session.labs if session.labs else None,
        vitals=session.vitals if session.vitals else None,
    )

    fixes_applied: list[str] = []

    # Auto-fix referential integrity issues
    if issue_type in ["referential", "all"]:
        for issue in result.errors:
            # Fix MRN mismatches for referential issues
            if issue.code.startswith("REF") and "patient_mrn" in (issue.field_path or ""):
                if session.encounter and session.encounter.patient_mrn != session.patient.mrn:
                    session.encounter.patient_mrn = session.patient.mrn
                    fixes_applied.append(f"Updated encounter.patient_mrn to {session.patient.mrn}")

                for diagnosis in session.diagnoses:
                    if diagnosis.patient_mrn != session.patient.mrn:
                        diagnosis.patient_mrn = session.patient.mrn
                        fixes_applied.append(
                            f"Updated diagnosis {diagnosis.code} patient_mrn to {session.patient.mrn}"
                        )

                for lab in session.labs:
                    if lab.patient_mrn != session.patient.mrn:
                        lab.patient_mrn = session.patient.mrn
                        fixes_applied.append(f"Updated lab {lab.test_name} patient_mrn")

                if session.vitals and session.vitals.patient_mrn != session.patient.mrn:
                    session.vitals.patient_mrn = session.patient.mrn
                    fixes_applied.append("Updated vital signs patient_mrn")

    # Re-validate
    new_result = validate_patient_record(
        patient=session.patient,
        encounters=[session.encounter] if session.encounter else None,
        diagnoses=session.diagnoses if session.diagnoses else None,
        labs=session.labs if session.labs else None,
        vitals=session.vitals if session.vitals else None,
    )

    # Format response
    response = format_fix_summary(session.id, fixes_applied, new_result.errors)

    return [TextContent(type="text", text=response)]


async def _explain_validation_rule_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Explain a validation rule."""
    rule_code = arguments["rule_code"]

    if rule_code not in VALIDATION_RULES:
        error_msg = format_validation_error(
            f"Unknown validation rule: {rule_code}",
            f"Available rules: {', '.join(sorted(VALIDATION_RULES.keys()))}",
        )
        return [TextContent(type="text", text=error_msg)]

    rule_info = VALIDATION_RULES[rule_code]
    response = format_rule_explanation(rule_code, rule_info)

    return [TextContent(type="text", text=response)]


async def main() -> None:
    """Run the MCP validation server."""
    logger.info("Starting PatientSim MCP Validation Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
