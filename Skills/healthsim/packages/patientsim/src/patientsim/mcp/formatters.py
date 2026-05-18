"""
Response formatters for MCP server.

Formats responses as human-readable summaries suitable for Claude to relay
to users, rather than raw data dumps.
"""

from typing import Any

from patientsim.mcp.session import PatientSession


def format_patient_summary(session: PatientSession) -> str:
    """
    Format a patient session as a human-readable summary.

    Args:
        session: Patient session to format

    Returns:
        Markdown-formatted summary
    """
    lines = [
        f"## Patient: {session.patient.full_name}",
        "",
        f"**ID**: {session.id}",
        f"**MRN**: {session.patient.mrn}",
        f"**Age**: {session.patient.age} years",
        f"**Gender**: {session.patient.gender}",
        "",
    ]

    # Demographics
    if session.patient.birth_date:
        lines.append(f"**Date of Birth**: {session.patient.birth_date}")

    if session.patient.address and session.patient.address.street_address:
        lines.append(
            f"**Address**: {session.patient.address.street_address}, {session.patient.address.city}, {session.patient.address.state} {session.patient.address.postal_code}"
        )

    # Encounter information
    if session.encounter:
        lines.extend(
            [
                "",
                "### Encounter",
                f"**Class**: {session.encounter.class_code}",
            ]
        )

        if session.encounter.admission_time:
            lines.append(
                f"**Admission**: {session.encounter.admission_time.strftime('%Y-%m-%d %H:%M')}"
            )

        if session.encounter.discharge_time:
            lines.append(
                f"**Discharge**: {session.encounter.discharge_time.strftime('%Y-%m-%d %H:%M')}"
            )

    # Diagnoses
    if session.diagnoses:
        lines.extend(["", "### Diagnoses"])
        for i, diagnosis in enumerate(session.diagnoses, 1):
            lines.append(f"{i}. **{diagnosis.description}** (ICD-10: {diagnosis.code})")

    # Vital signs (show most recent)
    if session.vitals:
        vitals = session.vitals[-1]  # Most recent vitals
        lines.extend(
            [
                "",
                "### Vital Signs",
                f"- **Heart Rate**: {vitals.heart_rate} bpm",
                f"- **Blood Pressure**: {vitals.systolic_bp}/{vitals.diastolic_bp} mmHg",
                f"- **Temperature**: {vitals.temperature}°F",
                f"- **Respiratory Rate**: {vitals.respiratory_rate} /min",
                f"- **SpO2**: {vitals.spo2}%",
            ]
        )

    # Lab results
    if session.labs:
        lines.extend(["", "### Lab Results"])
        for lab in session.labs:
            lines.append(f"- **{lab.test_name}**: {lab.value} {lab.unit} (LOINC: {lab.loinc_code})")

    return "\n".join(lines)


def format_cohort_summary(
    sessions: list[PatientSession],
    scenario: str | None = None,
) -> str:
    """
    Format a cohort of patients as a summary.

    Args:
        sessions: List of patient sessions
        scenario: Optional scenario name used

    Returns:
        Markdown-formatted cohort summary
    """
    if not sessions:
        return "No patients generated."

    lines = [
        f"## Generated Cohort: {len(sessions)} Patients",
        "",
    ]

    if scenario:
        lines.extend(
            [
                f"**Skill**: {scenario}",
                "",
            ]
        )

    # Demographics summary
    gender_counts = {"M": 0, "F": 0, "O": 0, "U": 0}
    ages = []

    for session in sessions:
        gender = session.patient.gender
        if gender in gender_counts:
            gender_counts[gender] += 1
        ages.append(session.patient.age)

    avg_age = sum(ages) / len(ages)
    min_age = min(ages)
    max_age = max(ages)

    lines.extend(
        [
            "### Demographics",
            f"- **Total Patients**: {len(sessions)}",
            f"- **Male**: {gender_counts['M']} ({gender_counts['M']/len(sessions)*100:.1f}%)",
            f"- **Female**: {gender_counts['F']} ({gender_counts['F']/len(sessions)*100:.1f}%)",
            f"- **Age Range**: {min_age} - {max_age} years (avg: {avg_age:.1f})",
            "",
        ]
    )

    # Patient list (first 10)
    lines.extend(
        [
            "### Patients",
            "",
        ]
    )

    for i, session in enumerate(sessions[:10], 1):
        diagnoses_text = ""
        if session.diagnoses:
            diagnoses_text = f" - {session.diagnoses[0].description}"

        lines.append(
            f"{i}. **{session.patient.full_name}** (ID: {session.id}) - "
            f"{session.patient.age}y {session.patient.gender}{diagnoses_text}"
        )

    if len(sessions) > 10:
        lines.append(f"... and {len(sessions) - 10} more patients")

    return "\n".join(lines)


def format_skill_list(scenarios: dict[str, dict[str, Any]]) -> str:
    """
    Format available scenarios as a list.

    Args:
        scenarios: Dict of scenario name to metadata

    Returns:
        Markdown-formatted scenario list
    """
    if not scenarios:
        return "No skills available."

    lines = [
        "## Available Skills",
        "",
    ]

    for name, metadata in sorted(scenarios.items()):
        description = metadata.get("description", "No description available")
        lines.extend(
            [
                f"### {name}",
                description,
                "",
            ]
        )

    return "\n".join(lines)


def format_skill_details(
    name: str,
    metadata: dict[str, Any],
) -> str:
    """
    Format detailed scenario information.

    Args:
        name: Scenario name
        metadata: Scenario metadata

    Returns:
        Markdown-formatted scenario details
    """
    lines = [
        f"## Skill: {name}",
        "",
    ]

    # Description
    if "description" in metadata:
        lines.extend(
            [
                metadata["description"],
                "",
            ]
        )

    # Parameters
    if "parameters" in metadata:
        lines.extend(
            [
                "### Parameters",
                "",
            ]
        )
        for param_name, param_info in metadata["parameters"].items():
            param_type = param_info.get("type", "any")
            param_desc = param_info.get("description", "")
            lines.append(f"- **{param_name}** ({param_type}): {param_desc}")
        lines.append("")

    # Example usage
    if "example" in metadata:
        lines.extend(
            [
                "### Example Usage",
                "",
                "```python",
                metadata["example"],
                "```",
                "",
            ]
        )

    return "\n".join(lines)


def format_error(
    message: str,
    suggestion: str | None = None,
) -> str:
    """
    Format an error message with optional suggestion.

    Args:
        message: Error message
        suggestion: Optional suggestion for fixing the error

    Returns:
        Formatted error message
    """
    lines = [
        f"❌ **Error**: {message}",
    ]

    if suggestion:
        lines.extend(
            [
                "",
                f"💡 **Suggestion**: {suggestion}",
            ]
        )

    return "\n".join(lines)


def format_success(
    message: str,
    next_steps: list[str] | None = None,
) -> str:
    """
    Format a success message with optional next steps.

    Args:
        message: Success message
        next_steps: Optional list of suggested next actions

    Returns:
        Formatted success message
    """
    lines = [
        f"✅ {message}",
    ]

    if next_steps:
        lines.extend(
            [
                "",
                "**Next steps**:",
            ]
        )
        for step in next_steps:
            lines.append(f"- {step}")

    return "\n".join(lines)
