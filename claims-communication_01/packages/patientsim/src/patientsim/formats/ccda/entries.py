"""C-CDA entry-level builders.

Functions for building individual CDA entry elements with proper template OIDs,
unique IDs, and formatted values.
"""

from __future__ import annotations

import html
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from patientsim.core.models import (
        Diagnosis,
        LabResult,
        Medication,
        Procedure,
        VitalSign,
    )


@dataclass
class TemplateOIDs:
    """Template OIDs for C-CDA entry-level templates."""

    # Problem entries
    PROBLEM_CONCERN_ACT = "2.16.840.1.113883.10.20.22.4.3"
    PROBLEM_OBSERVATION = "2.16.840.1.113883.10.20.22.4.4"

    # Medication entries
    MEDICATION_ACTIVITY = "2.16.840.1.113883.10.20.22.4.16"
    MEDICATION_INFORMATION = "2.16.840.1.113883.10.20.22.4.23"

    # Allergy entries
    ALLERGY_CONCERN_ACT = "2.16.840.1.113883.10.20.22.4.30"
    ALLERGY_OBSERVATION = "2.16.840.1.113883.10.20.22.4.7"
    REACTION_OBSERVATION = "2.16.840.1.113883.10.20.22.4.9"
    SEVERITY_OBSERVATION = "2.16.840.1.113883.10.20.22.4.8"

    # Result entries
    RESULT_ORGANIZER = "2.16.840.1.113883.10.20.22.4.1"
    RESULT_OBSERVATION = "2.16.840.1.113883.10.20.22.4.2"

    # Vital signs entries
    VITAL_SIGNS_ORGANIZER = "2.16.840.1.113883.10.20.22.4.26"
    VITAL_SIGNS_OBSERVATION = "2.16.840.1.113883.10.20.22.4.27"

    # Procedure entries
    PROCEDURE_ACTIVITY = "2.16.840.1.113883.10.20.22.4.14"

    # Immunization entries
    IMMUNIZATION_ACTIVITY = "2.16.840.1.113883.10.20.22.4.52"
    IMMUNIZATION_MEDICATION = "2.16.840.1.113883.10.20.22.4.54"


@dataclass
class CodeSystemOIDs:
    """OIDs for standard code systems."""

    SNOMED = "2.16.840.1.113883.6.96"
    LOINC = "2.16.840.1.113883.6.1"
    RXNORM = "2.16.840.1.113883.6.88"
    ICD10 = "2.16.840.1.113883.6.90"
    CVX = "2.16.840.1.113883.12.292"
    CPT = "2.16.840.1.113883.6.12"
    NDC = "2.16.840.1.113883.6.69"
    UCUM = "2.16.840.1.113883.6.8"
    ACT_CODE = "2.16.840.1.113883.5.4"
    ROUTE = "2.16.840.1.113883.5.112"


TEMPLATES = TemplateOIDs()
CODE_SYSTEMS = CodeSystemOIDs()


# =============================================================================
# Problem Entries
# =============================================================================


def build_problem_concern_act(
    diagnosis: Diagnosis,
    snomed_code: str | None = None,
    snomed_display: str | None = None,
) -> str:
    """Build Problem Concern Act entry.

    classCode="ACT", moodCode="EVN"
    Template OID: 2.16.840.1.113883.10.20.22.4.3

    Args:
        diagnosis: Diagnosis object
        snomed_code: Optional SNOMED code for the condition
        snomed_display: Optional SNOMED display name

    Returns:
        XML string for Problem Concern Act
    """
    act_id = str(uuid.uuid4())
    is_active = getattr(diagnosis, "is_active", True)
    status_code = "active" if is_active else "completed"
    onset_time = _format_datetime(diagnosis.diagnosed_date) if diagnosis.diagnosed_date else ""

    # Build the contained Problem Observation
    observation = build_problem_observation(
        diagnosis=diagnosis,
        snomed_code=snomed_code,
        snomed_display=snomed_display,
        icd10_code=diagnosis.code,
        icd10_display=diagnosis.description,
    )

    return f"""<entry typeCode="DRIV">
  <act classCode="ACT" moodCode="EVN">
    <templateId root="{TEMPLATES.PROBLEM_CONCERN_ACT}" extension="2015-08-01"/>
    <id root="{act_id}"/>
    <code code="CONC" codeSystem="{CODE_SYSTEMS.ACT_CODE}" displayName="Concern"/>
    <statusCode code="{status_code}"/>
    <effectiveTime><low value="{onset_time}"/></effectiveTime>
    <entryRelationship typeCode="SUBJ">
      {observation}
    </entryRelationship>
  </act>
</entry>"""


def build_problem_observation(
    diagnosis: Diagnosis,
    snomed_code: str | None = None,
    snomed_display: str | None = None,
    icd10_code: str | None = None,
    icd10_display: str | None = None,
) -> str:
    """Build Problem Observation entry.

    classCode="OBS", moodCode="EVN"
    Template OID: 2.16.840.1.113883.10.20.22.4.4

    Uses SNOMED as primary code with ICD-10 as translation.

    Args:
        diagnosis: Diagnosis object
        snomed_code: SNOMED code for the condition
        snomed_display: SNOMED display name
        icd10_code: ICD-10 code
        icd10_display: ICD-10 display name

    Returns:
        XML string for Problem Observation
    """
    obs_id = str(uuid.uuid4())
    onset_time = _format_datetime(diagnosis.diagnosed_date) if diagnosis.diagnosed_date else ""

    # Use ICD-10 as fallback if no SNOMED provided
    if snomed_code and snomed_display:
        primary_code = snomed_code
        primary_display = snomed_display
        primary_system = CODE_SYSTEMS.SNOMED
        primary_system_name = "SNOMED CT"

        # Add ICD-10 translation if available
        translation = ""
        if icd10_code:
            translation = f"""
          <translation code="{icd10_code}" codeSystem="{CODE_SYSTEMS.ICD10}" codeSystemName="ICD-10-CM" displayName="{_escape_xml(icd10_display or '')}"/>"""
    else:
        # Fall back to ICD-10 as primary
        primary_code = icd10_code or diagnosis.code
        primary_display = icd10_display or diagnosis.description
        primary_system = CODE_SYSTEMS.ICD10
        primary_system_name = "ICD-10-CM"
        translation = ""

    return f"""<observation classCode="OBS" moodCode="EVN">
    <templateId root="{TEMPLATES.PROBLEM_OBSERVATION}" extension="2015-08-01"/>
    <id root="{obs_id}"/>
    <code code="64572001" codeSystem="{CODE_SYSTEMS.SNOMED}" displayName="Condition"/>
    <statusCode code="completed"/>
    <effectiveTime><low value="{onset_time}"/></effectiveTime>
    <value xsi:type="CD" code="{primary_code}" codeSystem="{primary_system}" codeSystemName="{primary_system_name}" displayName="{_escape_xml(primary_display)}">{translation}
    </value>
  </observation>"""


# =============================================================================
# Medication Entries
# =============================================================================


def build_medication_activity(medication: Medication) -> str:
    """Build Medication Activity entry.

    classCode="SBADM", moodCode="EVN"
    Template OID: 2.16.840.1.113883.10.20.22.4.16

    Args:
        medication: Medication object

    Returns:
        XML string for Medication Activity
    """
    entry_id = str(uuid.uuid4())
    status = getattr(medication, "status", "active")
    status_code = "active" if status == "active" else "completed"

    # Build effectiveTime for duration
    start_time = _format_datetime(medication.start_date) if medication.start_date else ""
    end_time = ""
    if hasattr(medication, "end_date") and medication.end_date:
        end_time = _format_datetime(medication.end_date)

    if start_time and end_time:
        duration_time = f'<effectiveTime xsi:type="IVL_TS"><low value="{start_time}"/><high value="{end_time}"/></effectiveTime>'
    elif start_time:
        duration_time = (
            f'<effectiveTime xsi:type="IVL_TS"><low value="{start_time}"/></effectiveTime>'
        )
    else:
        duration_time = '<effectiveTime xsi:type="IVL_TS"><low nullFlavor="UNK"/></effectiveTime>'

    # Build effectiveTime for frequency (PIVL_TS)
    frequency = getattr(medication, "frequency", "")
    frequency_time = _build_frequency_time(frequency)

    # Route code
    route = getattr(medication, "route", "PO")
    route_code = _get_route_code(route)
    route_xml = f'<routeCode code="{route_code}" codeSystem="{CODE_SYSTEMS.ROUTE}" codeSystemName="RouteOfAdministration" displayName="{route}"/>'

    # Parse dose
    dose_parts = medication.dose.split() if medication.dose else ["", ""]
    dose_value = dose_parts[0] if dose_parts else ""
    dose_unit = dose_parts[1] if len(dose_parts) > 1 else ""

    # RxNorm code
    rxnorm_code = getattr(medication, "code", "") or ""
    code_system = CODE_SYSTEMS.RXNORM if rxnorm_code else ""

    return f"""<entry typeCode="DRIV">
  <substanceAdministration classCode="SBADM" moodCode="EVN">
    <templateId root="{TEMPLATES.MEDICATION_ACTIVITY}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <statusCode code="{status_code}"/>
    {duration_time}
    {frequency_time}
    {route_xml}
    <doseQuantity value="{dose_value}" unit="{dose_unit}"/>
    <consumable>
      <manufacturedProduct classCode="MANU">
        <templateId root="{TEMPLATES.MEDICATION_INFORMATION}" extension="2014-06-09"/>
        <manufacturedMaterial>
          <code code="{rxnorm_code}" codeSystem="{code_system}" codeSystemName="RxNorm" displayName="{_escape_xml(medication.name)}"/>
        </manufacturedMaterial>
      </manufacturedProduct>
    </consumable>
  </substanceAdministration>
</entry>"""


def _build_frequency_time(frequency: str) -> str:
    """Build PIVL_TS element for medication frequency.

    Args:
        frequency: Frequency string (QD, BID, TID, etc.)

    Returns:
        XML string for effectiveTime with PIVL_TS
    """
    # Map common frequencies to period values (in hours)
    frequency_map = {
        "QD": ("24", "h"),
        "BID": ("12", "h"),
        "TID": ("8", "h"),
        "QID": ("6", "h"),
        "Q4H": ("4", "h"),
        "Q6H": ("6", "h"),
        "Q8H": ("8", "h"),
        "Q12H": ("12", "h"),
        "QHS": ("24", "h"),
        "QAM": ("24", "h"),
        "QPM": ("24", "h"),
        "WEEKLY": ("1", "wk"),
        "MONTHLY": ("1", "mo"),
    }

    freq_upper = frequency.upper() if frequency else ""
    if freq_upper in frequency_map:
        period_value, period_unit = frequency_map[freq_upper]
        return f'<effectiveTime xsi:type="PIVL_TS" institutionSpecified="true" operator="A"><period value="{period_value}" unit="{period_unit}"/></effectiveTime>'
    elif freq_upper == "PRN":
        return '<effectiveTime xsi:type="PIVL_TS" institutionSpecified="true" operator="A"><period nullFlavor="NI"/></effectiveTime>'
    else:
        return ""


# =============================================================================
# Allergy Entries
# =============================================================================


def build_allergy_concern_act(allergy: Any) -> str:
    """Build Allergy Concern Act entry.

    Template OID: 2.16.840.1.113883.10.20.22.4.30

    Args:
        allergy: Allergy object (dict or dataclass)

    Returns:
        XML string for Allergy Concern Act
    """
    act_id = str(uuid.uuid4())
    status = _get_attr(allergy, "status", "active")
    status_code = "active" if status == "active" else "completed"
    onset_date = _get_attr(allergy, "onset_date", None)
    onset_time = _format_datetime(onset_date) if onset_date else ""

    # Build contained Allergy Observation
    observation = build_allergy_observation(allergy)

    return f"""<entry typeCode="DRIV">
  <act classCode="ACT" moodCode="EVN">
    <templateId root="{TEMPLATES.ALLERGY_CONCERN_ACT}" extension="2015-08-01"/>
    <id root="{act_id}"/>
    <code code="CONC" codeSystem="{CODE_SYSTEMS.ACT_CODE}" displayName="Concern"/>
    <statusCode code="{status_code}"/>
    <effectiveTime><low value="{onset_time}"/></effectiveTime>
    <entryRelationship typeCode="SUBJ">
      {observation}
    </entryRelationship>
  </act>
</entry>"""


def build_allergy_observation(allergy: Any) -> str:
    """Build Allergy Observation entry.

    Template OID: 2.16.840.1.113883.10.20.22.4.7

    Args:
        allergy: Allergy object (dict or dataclass)

    Returns:
        XML string for Allergy Observation
    """
    obs_id = str(uuid.uuid4())
    onset_date = _get_attr(allergy, "onset_date", None)
    onset_time = _format_datetime(onset_date) if onset_date else ""

    # Substance info
    substance = _get_attr(allergy, "substance", "Unknown")
    substance_code = _get_attr(allergy, "substance_code", "")
    substance_system = _get_attr(allergy, "substance_code_system", CODE_SYSTEMS.RXNORM)

    # Reaction info
    reaction = _get_attr(allergy, "reaction", "")
    reaction_code = _get_attr(allergy, "reaction_code", "")
    severity = _get_attr(allergy, "severity", "moderate")

    # Build participant for allergen
    participant_xml = f"""<participant typeCode="CSM">
      <participantRole classCode="MANU">
        <playingEntity classCode="MMAT">
          <code code="{substance_code}" codeSystem="{substance_system}" displayName="{_escape_xml(substance)}"/>
        </playingEntity>
      </participantRole>
    </participant>"""

    # Build reaction observation if provided
    reaction_xml = ""
    if reaction:
        reaction_xml = _build_reaction_observation(reaction, reaction_code, severity)

    return f"""<observation classCode="OBS" moodCode="EVN">
    <templateId root="{TEMPLATES.ALLERGY_OBSERVATION}" extension="2014-06-09"/>
    <id root="{obs_id}"/>
    <code code="ASSERTION" codeSystem="{CODE_SYSTEMS.ACT_CODE}"/>
    <statusCode code="completed"/>
    <effectiveTime><low value="{onset_time}"/></effectiveTime>
    <value xsi:type="CD" code="419199007" codeSystem="{CODE_SYSTEMS.SNOMED}" displayName="Allergy to substance"/>
    {participant_xml}
    {reaction_xml}
  </observation>"""


def _build_reaction_observation(reaction: str, reaction_code: str, severity: str) -> str:
    """Build Reaction Observation with Severity.

    Args:
        reaction: Reaction description
        reaction_code: SNOMED code for reaction
        severity: Severity level (mild, moderate, severe)

    Returns:
        XML string for reaction entryRelationship
    """
    reaction_id = str(uuid.uuid4())
    severity_id = str(uuid.uuid4())

    # Map severity to SNOMED codes
    severity_codes = {
        "mild": ("255604002", "Mild"),
        "moderate": ("6736007", "Moderate"),
        "severe": ("24484000", "Severe"),
    }
    sev_code, sev_display = severity_codes.get(severity.lower(), ("6736007", "Moderate"))

    return f"""<entryRelationship typeCode="MFST" inversionInd="true">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="{TEMPLATES.REACTION_OBSERVATION}" extension="2014-06-09"/>
        <id root="{reaction_id}"/>
        <code code="ASSERTION" codeSystem="{CODE_SYSTEMS.ACT_CODE}"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="{reaction_code}" codeSystem="{CODE_SYSTEMS.SNOMED}" displayName="{_escape_xml(reaction)}"/>
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="{TEMPLATES.SEVERITY_OBSERVATION}" extension="2014-06-09"/>
            <id root="{severity_id}"/>
            <code code="SEV" codeSystem="{CODE_SYSTEMS.ACT_CODE}" displayName="Severity"/>
            <statusCode code="completed"/>
            <value xsi:type="CD" code="{sev_code}" codeSystem="{CODE_SYSTEMS.SNOMED}" displayName="{sev_display}"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>"""


# =============================================================================
# Result Entries
# =============================================================================


def build_result_organizer(
    panel_code: str,
    panel_display: str,
    observations: list[str],
    effective_time: str = "",
) -> str:
    """Build Result Organizer entry.

    classCode="CLUSTER", moodCode="EVN"
    Template OID: 2.16.840.1.113883.10.20.22.4.1

    Args:
        panel_code: LOINC code for the panel
        panel_display: Display name for the panel
        observations: List of Result Observation XML strings
        effective_time: Formatted datetime string

    Returns:
        XML string for Result Organizer
    """
    organizer_id = str(uuid.uuid4())

    components = "\n".join(f"<component>{obs}</component>" for obs in observations)

    return f"""<entry typeCode="DRIV">
  <organizer classCode="CLUSTER" moodCode="EVN">
    <templateId root="{TEMPLATES.RESULT_ORGANIZER}" extension="2015-08-01"/>
    <id root="{organizer_id}"/>
    <code code="{panel_code}" codeSystem="{CODE_SYSTEMS.LOINC}" codeSystemName="LOINC" displayName="{_escape_xml(panel_display)}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{effective_time}"/>
    {components}
  </organizer>
</entry>"""


def build_result_observation(lab: LabResult) -> str:
    """Build Result Observation entry.

    classCode="OBS", moodCode="EVN"
    Template OID: 2.16.840.1.113883.10.20.22.4.2

    Args:
        lab: LabResult object

    Returns:
        XML string for Result Observation
    """
    obs_id = str(uuid.uuid4())
    loinc_code = getattr(lab, "loinc_code", "") or ""
    collected_time = _format_datetime(lab.collected_time) if lab.collected_time else ""

    # Build reference range if available
    ref_range = getattr(lab, "reference_range", None)
    ref_range_xml = ""
    if ref_range:
        ref_range_xml = f"""<referenceRange>
      <observationRange>
        <text>{_escape_xml(ref_range)}</text>
      </observationRange>
    </referenceRange>"""

    # Interpretation code if abnormal
    abnormal_flag = getattr(lab, "abnormal_flag", None)
    interpretation_xml = ""
    if abnormal_flag:
        interp_codes = {
            "H": ("H", "High"),
            "L": ("L", "Low"),
            "HH": ("HH", "Critical High"),
            "LL": ("LL", "Critical Low"),
            "A": ("A", "Abnormal"),
            "N": ("N", "Normal"),
        }
        code, display = interp_codes.get(abnormal_flag.upper(), ("A", "Abnormal"))
        interpretation_xml = f'<interpretationCode code="{code}" codeSystem="2.16.840.1.113883.5.83" displayName="{display}"/>'

    # Determine value type
    try:
        float(lab.value)
        value_xml = f'<value xsi:type="PQ" value="{lab.value}" unit="{lab.unit or ""}"/>'
    except (ValueError, TypeError):
        value_xml = f'<value xsi:type="ST">{_escape_xml(lab.value)}</value>'

    return f"""<observation classCode="OBS" moodCode="EVN">
    <templateId root="{TEMPLATES.RESULT_OBSERVATION}" extension="2015-08-01"/>
    <id root="{obs_id}"/>
    <code code="{loinc_code}" codeSystem="{CODE_SYSTEMS.LOINC}" codeSystemName="LOINC" displayName="{_escape_xml(lab.test_name)}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{collected_time}"/>
    {value_xml}
    {interpretation_xml}
    {ref_range_xml}
  </observation>"""


# =============================================================================
# Vital Signs Entries
# =============================================================================


def build_vital_signs_organizer(vitals: VitalSign, observation_time: datetime | None = None) -> str:
    """Build Vital Signs Organizer entry.

    Template OID: 2.16.840.1.113883.10.20.22.4.26

    Args:
        vitals: VitalSign object with measurements
        observation_time: Override datetime (uses vitals.observation_time if not provided)

    Returns:
        XML string for Vital Signs Organizer
    """
    organizer_id = str(uuid.uuid4())
    obs_time = observation_time or vitals.observation_time
    formatted_time = _format_datetime(obs_time) if obs_time else ""

    # Build individual vital sign observations
    vital_mappings = [
        ("systolic_bp", vitals.systolic_bp, "8480-6", "Systolic blood pressure", "mm[Hg]"),
        ("diastolic_bp", vitals.diastolic_bp, "8462-4", "Diastolic blood pressure", "mm[Hg]"),
        ("heart_rate", vitals.heart_rate, "8867-4", "Heart rate", "/min"),
        ("respiratory_rate", vitals.respiratory_rate, "9279-1", "Respiratory rate", "/min"),
        ("temperature", vitals.temperature, "8310-5", "Body temperature", "[degF]"),
        ("spo2", vitals.spo2, "2708-6", "Oxygen saturation", "%"),
        ("height_cm", vitals.height_cm, "8302-2", "Body height", "cm"),
        ("weight_kg", vitals.weight_kg, "29463-7", "Body weight", "kg"),
    ]

    components = []
    for _, value, loinc_code, display, unit in vital_mappings:
        if value is not None:
            obs_xml = _build_vital_observation(loinc_code, display, value, unit, formatted_time)
            components.append(f"<component>{obs_xml}</component>")

    return f"""<entry typeCode="DRIV">
  <organizer classCode="CLUSTER" moodCode="EVN">
    <templateId root="{TEMPLATES.VITAL_SIGNS_ORGANIZER}" extension="2014-06-09"/>
    <id root="{organizer_id}"/>
    <code code="46680005" codeSystem="{CODE_SYSTEMS.SNOMED}" codeSystemName="SNOMED CT" displayName="Vital signs"/>
    <statusCode code="completed"/>
    <effectiveTime value="{formatted_time}"/>
    {"".join(components)}
  </organizer>
</entry>"""


def _build_vital_observation(
    loinc_code: str,
    display: str,
    value: float | int,
    unit: str,
    effective_time: str,
) -> str:
    """Build single vital sign observation."""
    obs_id = str(uuid.uuid4())

    return f"""<observation classCode="OBS" moodCode="EVN">
    <templateId root="{TEMPLATES.VITAL_SIGNS_OBSERVATION}" extension="2014-06-09"/>
    <id root="{obs_id}"/>
    <code code="{loinc_code}" codeSystem="{CODE_SYSTEMS.LOINC}" codeSystemName="LOINC" displayName="{display}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{effective_time}"/>
    <value xsi:type="PQ" value="{value}" unit="{unit}"/>
  </observation>"""


# =============================================================================
# Procedure Entries
# =============================================================================


def build_procedure_activity(procedure: Procedure) -> str:
    """Build Procedure Activity Procedure entry.

    classCode="PROC", moodCode="EVN"
    Template OID: 2.16.840.1.113883.10.20.22.4.14

    Args:
        procedure: Procedure object

    Returns:
        XML string for Procedure Activity
    """
    entry_id = str(uuid.uuid4())
    proc_time = ""
    if hasattr(procedure, "performed_date") and procedure.performed_date:
        proc_time = _format_datetime(procedure.performed_date)

    # Determine code system (CPT vs SNOMED)
    code_system = CODE_SYSTEMS.SNOMED
    code_system_name = "SNOMED CT"
    if (
        hasattr(procedure, "code_system")
        and procedure.code_system
        and "cpt" in procedure.code_system.lower()
    ):
        code_system = CODE_SYSTEMS.CPT
        code_system_name = "CPT"

    # Performer info
    performer_xml = ""
    if hasattr(procedure, "performer") and procedure.performer:
        performer_xml = f"""<performer>
      <assignedEntity>
        <id nullFlavor="UNK"/>
        <assignedPerson>
          <name>{_escape_xml(procedure.performer)}</name>
        </assignedPerson>
      </assignedEntity>
    </performer>"""

    return f"""<entry typeCode="DRIV">
  <procedure classCode="PROC" moodCode="EVN">
    <templateId root="{TEMPLATES.PROCEDURE_ACTIVITY}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <code code="{procedure.code}" codeSystem="{code_system}" codeSystemName="{code_system_name}" displayName="{_escape_xml(procedure.description)}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{proc_time}"/>
    {performer_xml}
  </procedure>
</entry>"""


# =============================================================================
# Immunization Entries
# =============================================================================


def build_immunization_activity(immunization: Any) -> str:
    """Build Immunization Activity entry.

    classCode="SBADM", moodCode="EVN"
    Template OID: 2.16.840.1.113883.10.20.22.4.52

    Args:
        immunization: Immunization object (dict or dataclass)

    Returns:
        XML string for Immunization Activity
    """
    entry_id = str(uuid.uuid4())

    vaccine = _get_attr(immunization, "vaccine_name", "Unknown")
    cvx_code = _get_attr(immunization, "cvx_code", "")
    admin_date = _get_attr(immunization, "administered_date", None)
    status = _get_attr(immunization, "status", "completed")
    lot_number = _get_attr(immunization, "lot_number", "")
    route = _get_attr(immunization, "route", "IM")

    admin_time = _format_datetime(admin_date) if admin_date else ""
    status_code = "completed" if status == "completed" else "active"
    negation = 'negationInd="true" ' if status == "refused" else ""

    # Route code
    route_code = _get_route_code(route)
    route_xml = (
        f'<routeCode code="{route_code}" codeSystem="{CODE_SYSTEMS.ROUTE}" displayName="{route}"/>'
    )

    # Lot number
    lot_xml = f"<lotNumberText>{_escape_xml(lot_number)}</lotNumberText>" if lot_number else ""

    return f"""<entry typeCode="DRIV">
  <substanceAdministration classCode="SBADM" moodCode="EVN" {negation}>
    <templateId root="{TEMPLATES.IMMUNIZATION_ACTIVITY}" extension="2015-08-01"/>
    <id root="{entry_id}"/>
    <statusCode code="{status_code}"/>
    <effectiveTime value="{admin_time}"/>
    {route_xml}
    <consumable>
      <manufacturedProduct classCode="MANU">
        <templateId root="{TEMPLATES.IMMUNIZATION_MEDICATION}" extension="2014-06-09"/>
        <manufacturedMaterial>
          <code code="{cvx_code}" codeSystem="{CODE_SYSTEMS.CVX}" codeSystemName="CVX" displayName="{_escape_xml(vaccine)}"/>
          {lot_xml}
        </manufacturedMaterial>
      </manufacturedProduct>
    </consumable>
  </substanceAdministration>
</entry>"""


# =============================================================================
# Helper Functions
# =============================================================================


def _format_datetime(dt: datetime | Any | None) -> str:
    """Format datetime for CDA (YYYYMMDDHHMMSS format)."""
    if dt is None:
        return ""
    if hasattr(dt, "strftime"):
        return dt.strftime("%Y%m%d%H%M%S")
    return ""


def _escape_xml(text: str | None) -> str:
    """Escape text for XML content."""
    if text is None:
        return ""
    return html.escape(str(text))


def _get_attr(obj: Any, attr: str, default: Any = None) -> Any:
    """Get attribute from object, dict, or return default."""
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)


def _get_route_code(route: str) -> str:
    """Map route abbreviation to standard code."""
    route_codes = {
        "PO": "PO",
        "IV": "IV",
        "IM": "IM",
        "SC": "SC",
        "SQ": "SC",
        "SL": "SL",
        "TOP": "TOP",
        "INH": "IPINHL",
        "PR": "PR",
        "TD": "TRNSDERM",
        "NASAL": "NASINHL",
    }
    return route_codes.get(route.upper(), route)
