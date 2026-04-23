"""
Response formatters for MCP validation server.

Formats validation results as human-readable summaries with actionable guidance.
"""

from typing import Any

from patientsim.validation.base import ValidationIssue, ValidationResult


def format_validation_summary(
    patient_results: dict[str, ValidationResult],
    validation_level: str = "standard",
) -> str:
    """
    Format validation results for multiple patients.

    Args:
        patient_results: Dict mapping patient ID to validation result
        validation_level: Validation thoroughness level

    Returns:
        Markdown-formatted validation summary
    """
    total_patients = len(patient_results)
    passed_patients = sum(1 for r in patient_results.values() if r.valid)
    failed_patients = total_patients - passed_patients

    # Count issues by severity
    total_errors = sum(len(r.errors) for r in patient_results.values())
    total_warnings = sum(len(r.warnings) for r in patient_results.values())
    total_infos = sum(len(r.infos) for r in patient_results.values())

    lines = [
        f"## Validation Results ({validation_level.title()} Level)",
        "",
        f"**Patients Validated**: {total_patients}",
        f"**✅ Passed**: {passed_patients}",
        f"**❌ Failed**: {failed_patients}",
        "",
    ]

    # Summary of issues
    if total_errors + total_warnings + total_infos > 0:
        lines.extend(
            [
                "### Issues Found",
                "",
                f"- **Errors**: {total_errors} (must fix)",
                f"- **Warnings**: {total_warnings} (recommended)",
                f"- **Info**: {total_infos} (informational)",
                "",
            ]
        )

    # Details per patient
    if failed_patients > 0 or total_warnings > 0:
        lines.extend(
            [
                "### Patient Details",
                "",
            ]
        )

        for patient_id, result in patient_results.items():
            if not result.valid or result.warnings:
                status = "❌ FAILED" if not result.valid else "⚠️  HAS WARNINGS"
                lines.append(f"#### Patient {patient_id} - {status}")
                lines.append("")

                # Group issues by severity
                if result.errors:
                    lines.append("**Errors** (must fix):")
                    for issue in result.errors:
                        lines.append(f"- [{issue.code}] {issue.message}")
                        if issue.field_path:
                            lines.append(f"  *Field: {issue.field_path}*")
                    lines.append("")

                if result.warnings:
                    lines.append("**Warnings** (recommended):")
                    for issue in result.warnings:
                        lines.append(f"- [{issue.code}] {issue.message}")
                    lines.append("")

                if result.infos and validation_level == "thorough":
                    lines.append("**Info** (for reference):")
                    for issue in result.infos:
                        lines.append(f"- [{issue.code}] {issue.message}")
                    lines.append("")

    # Next steps
    if failed_patients > 0:
        lines.extend(
            [
                "### Next Steps",
                "",
                "- Use `fix_validation_issues()` to auto-fix common problems",
                "- Use `explain_validation_rule()` to understand specific issues",
                "- Manually correct issues in the patient data",
                "- Re-validate after making changes",
            ]
        )
    elif total_warnings > 0:
        lines.extend(
            [
                "### Next Steps",
                "",
                "- Review warnings and decide if action is needed",
                "- Use `explain_validation_rule()` for more context",
                "- Warnings won't prevent export, but may indicate data quality issues",
            ]
        )
    else:
        lines.extend(
            [
                "### ✅ All Clear!",
                "",
                "All patients passed validation. The data is ready for export.",
            ]
        )

    return "\n".join(lines)


def format_export_validation_summary(
    patient_results: dict[str, ValidationResult],
    target_format: str,
    format_specific_issues: list[str] | None = None,
) -> str:
    """
    Format validation results for a specific export format.

    Args:
        patient_results: Dict mapping patient ID to validation result
        target_format: Target export format (fhir, hl7v2, mimic)
        format_specific_issues: Additional format-specific issues

    Returns:
        Markdown-formatted validation summary
    """
    total_patients = len(patient_results)
    passed_patients = sum(1 for r in patient_results.values() if r.valid)
    failed_patients = total_patients - passed_patients

    lines = [
        f"## {target_format.upper()} Export Validation",
        "",
        f"**Patients Checked**: {total_patients}",
        f"**✅ Export Ready**: {passed_patients}",
        f"**❌ Export Blocked**: {failed_patients}",
        "",
    ]

    # Format-specific requirements
    format_requirements = {
        "fhir": [
            "All required FHIR resources must have valid references",
            "Patient resource must have at least name and gender",
            "Temporal consistency is critical for FHIR bundles",
        ],
        "hl7v2": [
            "Patient demographics must be complete (name, MRN, DOB)",
            "Encounter must exist for ADT messages",
            "All required segments must have valid data",
        ],
        "mimic": [
            "Patient must have admission for ADMISSIONS table",
            "ICD codes required for DIAGNOSES_ICD table",
            "Temporal consistency required for time-based tables",
        ],
    }

    if target_format.lower() in format_requirements:
        lines.extend(
            [
                f"### {target_format.upper()} Requirements",
                "",
            ]
        )
        for req in format_requirements[target_format.lower()]:
            lines.append(f"- {req}")
        lines.append("")

    # Format-specific issues
    if format_specific_issues:
        lines.extend(
            [
                "### Format-Specific Issues",
                "",
            ]
        )
        for issue in format_specific_issues:
            lines.append(f"- {issue}")
        lines.append("")

    # Failed patients
    if failed_patients > 0:
        lines.extend(
            [
                "### Patients with Issues",
                "",
            ]
        )

        for patient_id, result in patient_results.items():
            if not result.valid:
                lines.append(f"**Patient {patient_id}**:")
                for error in result.errors:
                    lines.append(f"  - {error.message}")
                lines.append("")

        lines.extend(
            [
                "### Recommendation",
                "",
                f"Fix validation errors before exporting to {target_format.upper()}. ",
                "Use `fix_validation_issues()` for auto-fixes or manually correct the data.",
            ]
        )
    else:
        lines.extend(
            [
                f"### ✅ Ready for {target_format.upper()} Export",
                "",
                f"All patients meet {target_format.upper()} requirements and can be exported safely.",
            ]
        )

    return "\n".join(lines)


def format_fix_summary(
    patient_id: str,
    fixes_applied: list[str],
    remaining_issues: list[ValidationIssue],
) -> str:
    """
    Format summary of auto-fixes applied.

    Args:
        patient_id: Patient ID that was fixed
        fixes_applied: List of fixes that were applied
        remaining_issues: Issues that couldn't be auto-fixed

    Returns:
        Markdown-formatted fix summary
    """
    lines = [
        f"## Auto-Fix Results for Patient {patient_id}",
        "",
    ]

    if fixes_applied:
        lines.extend(
            [
                f"### ✅ Fixes Applied ({len(fixes_applied)})",
                "",
            ]
        )
        for fix in fixes_applied:
            lines.append(f"- {fix}")
        lines.append("")

    if remaining_issues:
        lines.extend(
            [
                f"### ⚠️  Remaining Issues ({len(remaining_issues)})",
                "",
                "*These issues require manual correction:*",
                "",
            ]
        )
        for issue in remaining_issues:
            lines.append(f"- [{issue.code}] {issue.message}")
        lines.append("")

        lines.extend(
            [
                "### Next Steps",
                "",
                "- Manually correct the remaining issues",
                "- Use `explain_validation_rule()` to understand specific issues",
                "- Re-validate after making changes",
            ]
        )
    else:
        lines.extend(
            [
                "### ✅ All Issues Resolved!",
                "",
                "Patient data now passes all validation checks.",
            ]
        )

    return "\n".join(lines)


def format_rule_explanation(
    rule_code: str,
    rule_info: dict[str, Any],
) -> str:
    """
    Format explanation of a validation rule.

    Args:
        rule_code: Validation rule code (e.g., "TEMP_001")
        rule_info: Dict with rule details

    Returns:
        Markdown-formatted rule explanation
    """
    lines = [
        f"## Validation Rule: {rule_code}",
        "",
    ]

    # Rule description
    if "description" in rule_info:
        lines.extend(
            [
                "### What This Checks",
                "",
                rule_info["description"],
                "",
            ]
        )

    # Clinical/technical rationale
    if "rationale" in rule_info:
        lines.extend(
            [
                "### Why This Matters",
                "",
                rule_info["rationale"],
                "",
            ]
        )

    # Severity
    if "severity" in rule_info:
        severity_emoji = {
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
        }
        emoji = severity_emoji.get(rule_info["severity"].lower(), "")
        lines.extend(
            [
                f"### Severity: {emoji} {rule_info['severity'].upper()}",
                "",
            ]
        )

    # Examples
    if "passing_example" in rule_info or "failing_example" in rule_info:
        lines.extend(
            [
                "### Examples",
                "",
            ]
        )

        if "passing_example" in rule_info:
            lines.extend(
                [
                    "**✅ Passing:**",
                    f"```\n{rule_info['passing_example']}\n```",
                    "",
                ]
            )

        if "failing_example" in rule_info:
            lines.extend(
                [
                    "**❌ Failing:**",
                    f"```\n{rule_info['failing_example']}\n```",
                    "",
                ]
            )

    # How to fix
    if "fix_guidance" in rule_info:
        lines.extend(
            [
                "### How to Fix",
                "",
                rule_info["fix_guidance"],
            ]
        )

    return "\n".join(lines)


def format_validation_error(
    message: str,
    suggestion: str | None = None,
) -> str:
    """
    Format a validation error message.

    Args:
        message: Error message
        suggestion: Optional suggestion for fixing

    Returns:
        Formatted error message
    """
    lines = [
        "## ❌ Validation Error",
        "",
        f"**Error**: {message}",
    ]

    if suggestion:
        lines.extend(
            [
                "",
                f"**Suggestion**: {suggestion}",
            ]
        )

    return "\n".join(lines)
