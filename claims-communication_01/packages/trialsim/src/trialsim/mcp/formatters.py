"""Formatters for TrialSim MCP server output.

This module provides human-readable formatting for TrialSim entities and operations.
"""

from typing import Any


def format_subject_summary(subject: Any) -> str:
    """Format a single subject summary for display."""
    lines = [
        f"**Subject: {subject.subject_id}**",
        "",
        f"- Protocol: {subject.protocol_id}",
        f"- Site: {subject.site_id}",
        f"- Age: {subject.age} years",
        f"- Sex: {subject.sex}",
        f"- Race: {subject.race or 'Not specified'}",
        f"- Status: {subject.status.value}",
    ]
    
    if subject.arm:
        lines.append(f"- Treatment Arm: {subject.arm.value}")
    
    if subject.screening_date:
        lines.append(f"- Screened: {subject.screening_date}")
    
    if subject.randomization_date:
        lines.append(f"- Randomized: {subject.randomization_date}")
    
    return "\n".join(lines)


def format_cohort_summary(subjects: list, skill: str | None = None) -> str:
    """Format a cohort summary with statistics."""
    if not subjects:
        return "No subjects generated."
    
    count = len(subjects)
    
    # Calculate demographics
    ages = [s.age for s in subjects]
    avg_age = sum(ages) / len(ages)
    
    male_count = sum(1 for s in subjects if s.sex == "M")
    female_count = sum(1 for s in subjects if s.sex == "F")
    
    # Status breakdown
    status_counts = {}
    for s in subjects:
        status = s.status.value
        status_counts[status] = status_counts.get(status, 0) + 1
    
    lines = [
        f"**Generated {count} Subjects**",
        "",
        "**Demographics:**",
        f"- Average age: {avg_age:.1f} years",
        f"- Age range: {min(ages)}-{max(ages)} years",
        f"- Sex: {male_count} male, {female_count} female",
    ]
    
    if skill:
        lines.insert(2, f"- Skill: {skill}")
    
    lines.extend(["", "**Status Distribution:**"])
    for status, cnt in sorted(status_counts.items()):
        lines.append(f"- {status}: {cnt}")
    
    # Sample subjects
    sample_size = min(3, count)
    lines.extend(["", f"**Sample Subjects ({sample_size} of {count}):**"])
    for s in subjects[:sample_size]:
        lines.append(f"- {s.subject_id}: {s.age}y {s.sex}, {s.status.value}")
    
    return "\n".join(lines)


def format_visit_schedule(visits: list) -> str:
    """Format a visit schedule for display."""
    if not visits:
        return "No visits scheduled."
    
    lines = [
        f"**Visit Schedule ({len(visits)} visits)**",
        "",
    ]
    
    for visit in visits:
        status_icon = "✓" if visit.visit_status == "completed" else "○"
        date_str = visit.planned_date.isoformat() if visit.planned_date else "TBD"
        lines.append(f"{status_icon} **{visit.visit_name}** ({visit.visit_type.value})")
        lines.append(f"  - Planned: {date_str}")
        if visit.actual_date:
            lines.append(f"  - Actual: {visit.actual_date.isoformat()}")
        lines.append("")
    
    return "\n".join(lines)


def format_adverse_events(adverse_events: list) -> str:
    """Format adverse events for display."""
    if not adverse_events:
        return "No adverse events recorded."
    
    lines = [
        f"**Adverse Events ({len(adverse_events)})**",
        "",
    ]
    
    for ae in adverse_events:
        severity_icon = "⚠️" if ae.is_serious else "•"
        lines.append(f"{severity_icon} **{ae.ae_term}** (Grade {ae.severity.value[-1]})")
        lines.append(f"  - Onset: {ae.onset_date}")
        if ae.resolution_date:
            lines.append(f"  - Resolved: {ae.resolution_date}")
        if ae.causality:
            lines.append(f"  - Causality: {ae.causality.value}")
        lines.append("")
    
    return "\n".join(lines)


def format_exposures(exposures: list) -> str:
    """Format drug exposures for display."""
    if not exposures:
        return "No exposures recorded."
    
    lines = [
        f"**Drug Exposures ({len(exposures)})**",
        "",
    ]
    
    for exp in exposures:
        lines.append(f"• **{exp.drug_name}** {exp.dose} {exp.dose_unit}")
        lines.append(f"  - Start: {exp.start_date}")
        if exp.end_date:
            lines.append(f"  - End: {exp.end_date}")
        lines.append(f"  - Compliance: {exp.compliance_pct:.1f}%")
        lines.append("")
    
    return "\n".join(lines)


def format_skill_list(skills: list[dict]) -> str:
    """Format list of available skills."""
    if not skills:
        return "No skills available."
    
    lines = ["**Available TrialSim Skills:**", ""]
    
    for skill in skills:
        lines.append(f"- **{skill['name']}**: {skill['description']}")
    
    return "\n".join(lines)


def format_skill_details(skill: dict) -> str:
    """Format detailed skill information."""
    lines = [
        f"**Skill: {skill['name']}**",
        "",
        f"_{skill['description']}_",
        "",
    ]
    
    if skill.get("parameters"):
        lines.append("**Parameters:**")
        for param, info in skill["parameters"].items():
            lines.append(f"- `{param}`: {info.get('description', 'No description')}")
    
    if skill.get("examples"):
        lines.append("")
        lines.append("**Examples:**")
        for example in skill["examples"]:
            lines.append(f"- {example}")
    
    return "\n".join(lines)


def format_success(message: str) -> str:
    """Format a success message."""
    return f"✓ {message}"


def format_error(message: str) -> str:
    """Format an error message."""
    return f"**Error:** {message}"
