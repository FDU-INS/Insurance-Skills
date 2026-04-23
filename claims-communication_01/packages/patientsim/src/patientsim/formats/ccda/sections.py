"""C-CDA section builders.

Builds all standard C-CDA sections with proper template OIDs, LOINC codes,
narrative text, and machine-readable entries.
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
        Encounter,
        LabResult,
        Medication,
        Patient,
        Procedure,
        VitalSign,
    )


@dataclass
class SectionOIDs:
    """Template OIDs for C-CDA sections."""

    # Section template OIDs
    PROBLEMS = "2.16.840.1.113883.10.20.22.2.5.1"
    MEDICATIONS = "2.16.840.1.113883.10.20.22.2.1.1"
    ALLERGIES = "2.16.840.1.113883.10.20.22.2.6.1"
    RESULTS = "2.16.840.1.113883.10.20.22.2.3.1"
    VITAL_SIGNS = "2.16.840.1.113883.10.20.22.2.4.1"
    PROCEDURES = "2.16.840.1.113883.10.20.22.2.7.1"
    IMMUNIZATIONS = "2.16.840.1.113883.10.20.22.2.2.1"
    PLAN_OF_TREATMENT = "2.16.840.1.113883.10.20.22.2.10"
    ENCOUNTERS = "2.16.840.1.113883.10.20.22.2.22.1"
    SOCIAL_HISTORY = "2.16.840.1.113883.10.20.22.2.17"
    HOSPITAL_COURSE = "2.16.840.1.113883.10.20.22.2.16"
    DISCHARGE_INSTRUCTIONS = "2.16.840.1.113883.10.20.22.2.41"
    REASON_FOR_REFERRAL = "1.3.6.1.4.1.19376.1.5.3.1.3.1"


@dataclass
class EntryOIDs:
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

    # Encounter entries
    ENCOUNTER_ACTIVITY = "2.16.840.1.113883.10.20.22.4.49"

    # Plan of treatment entries
    PLANNED_PROCEDURE = "2.16.840.1.113883.10.20.22.4.41"
    PLANNED_OBSERVATION = "2.16.840.1.113883.10.20.22.4.44"
    PLANNED_MEDICATION = "2.16.840.1.113883.10.20.22.4.42"

    # Social history entries
    SMOKING_STATUS = "2.16.840.1.113883.10.20.22.4.78"
    SOCIAL_HISTORY_OBSERVATION = "2.16.840.1.113883.10.20.22.4.38"


@dataclass
class CodeSystems:
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
    ADMIN_GENDER = "2.16.840.1.113883.5.1"
    NULL_FLAVOR = "2.16.840.1.113883.5.1008"


class SectionBuilder:
    """Builds C-CDA section XML elements.

    Generates complete section elements with templateId, code, title,
    narrative text, and machine-readable entries.

    Example:
        >>> builder = SectionBuilder()
        >>> problems_xml = builder.build_problems(diagnoses)
        >>> allergies_xml = builder.build_allergies(allergies)
    """

    def __init__(self) -> None:
        """Initialize section builder."""
        self._section_oids = SectionOIDs()
        self._entry_oids = EntryOIDs()
        self._code_systems = CodeSystems()

    # =========================================================================
    # Core Clinical Sections
    # =========================================================================

    def build_problems(self, diagnoses: list[Diagnosis]) -> str | None:
        """Build Problems section with diagnoses.

        Template OID: 2.16.840.1.113883.10.20.22.2.5.1
        LOINC: 11450-4 (Problem List)

        Args:
            diagnoses: List of Diagnosis objects

        Returns:
            XML string for Problems section or None if no data
        """
        if not diagnoses:
            return None

        # Build narrative table
        rows = []
        for diag in diagnoses:
            status = "Active" if getattr(diag, "is_active", True) else "Resolved"
            onset = (
                diag.diagnosed_date.strftime("%Y-%m-%d")
                if hasattr(diag, "diagnosed_date") and diag.diagnosed_date
                else ""
            )
            rows.append(
                f"<tr><td>{self._escape_xml(diag.description)}</td>"
                f"<td>{diag.code}</td><td>{status}</td><td>{onset}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Problem</th><th>Code</th><th>Status</th><th>Onset Date</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        # Build entries
        entries = [self._build_problem_entry(diag) for diag in diagnoses]

        return self._build_section_wrapper(
            template_oid=self._section_oids.PROBLEMS,
            loinc_code="11450-4",
            title="Problems",
            display_name="Problem List",
            narrative=narrative,
            entries=entries,
        )

    def _build_problem_entry(self, diag: Diagnosis) -> str:
        """Build Problem Concern Act with Problem Observation."""
        concern_id = str(uuid.uuid4())
        obs_id = str(uuid.uuid4())
        is_active = getattr(diag, "is_active", True)
        status_code = "active" if is_active else "completed"
        onset_time = self._format_datetime(diag.diagnosed_date) if diag.diagnosed_date else ""

        # Build SNOMED translation if available
        snomed_code = getattr(diag, "snomed_code", None)
        translation = ""
        if snomed_code:
            snomed_display = getattr(diag, "snomed_display", diag.description)
            translation = f"""
          <translation code="{snomed_code}" codeSystem="{self._code_systems.SNOMED}" codeSystemName="SNOMED CT" displayName="{self._escape_xml(snomed_display)}"/>"""

        return f"""<entry typeCode="DRIV">
  <act classCode="ACT" moodCode="EVN">
    <templateId root="{self._entry_oids.PROBLEM_CONCERN_ACT}" extension="2015-08-01"/>
    <id root="{concern_id}"/>
    <code code="CONC" codeSystem="{self._code_systems.ACT_CODE}" displayName="Concern"/>
    <statusCode code="{status_code}"/>
    <effectiveTime><low value="{onset_time}"/></effectiveTime>
    <entryRelationship typeCode="SUBJ">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="{self._entry_oids.PROBLEM_OBSERVATION}" extension="2015-08-01"/>
        <id root="{obs_id}"/>
        <code code="64572001" codeSystem="{self._code_systems.SNOMED}" displayName="Condition"/>
        <statusCode code="completed"/>
        <effectiveTime><low value="{onset_time}"/></effectiveTime>
        <value xsi:type="CD" code="{diag.code}" codeSystem="{self._code_systems.ICD10}" codeSystemName="ICD-10-CM" displayName="{self._escape_xml(diag.description)}">{translation}
        </value>
      </observation>
    </entryRelationship>
  </act>
</entry>"""

    def build_medications(self, medications: list[Medication]) -> str | None:
        """Build Medications section.

        Template OID: 2.16.840.1.113883.10.20.22.2.1.1
        LOINC: 10160-0 (History of Medication Use)

        Args:
            medications: List of Medication objects

        Returns:
            XML string for Medications section or None if no data
        """
        if not medications:
            return None

        # Build narrative table
        rows = []
        for med in medications:
            status = getattr(med, "status", "active")
            route = getattr(med, "route", "")
            rows.append(
                f"<tr><td>{self._escape_xml(med.name)}</td>"
                f"<td>{med.dose}</td><td>{route}</td>"
                f"<td>{med.frequency}</td><td>{status}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Medication</th><th>Dose</th><th>Route</th><th>Frequency</th><th>Status</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        entries = [self._build_medication_entry(med) for med in medications]

        return self._build_section_wrapper(
            template_oid=self._section_oids.MEDICATIONS,
            loinc_code="10160-0",
            title="Medications",
            display_name="History of Medication Use",
            narrative=narrative,
            entries=entries,
        )

    def _build_medication_entry(self, med: Medication) -> str:
        """Build Medication Activity entry."""
        entry_id = str(uuid.uuid4())
        status = getattr(med, "status", "active")
        status_code = "active" if status == "active" else "completed"

        # Build effectiveTime
        start_time = self._format_datetime(med.start_date) if med.start_date else ""
        end_time = (
            self._format_datetime(med.end_date) if hasattr(med, "end_date") and med.end_date else ""
        )

        if start_time and end_time:
            effective_time = f'<effectiveTime xsi:type="IVL_TS"><low value="{start_time}"/><high value="{end_time}"/></effectiveTime>'
        elif start_time:
            effective_time = (
                f'<effectiveTime xsi:type="IVL_TS"><low value="{start_time}"/></effectiveTime>'
            )
        else:
            effective_time = (
                '<effectiveTime xsi:type="IVL_TS"><low nullFlavor="UNK"/></effectiveTime>'
            )

        # Route code mapping
        route = getattr(med, "route", "PO")
        route_code = self._get_route_code(route)
        route_xml = f'<routeCode code="{route_code}" codeSystem="2.16.840.1.113883.5.112" codeSystemName="RouteOfAdministration" displayName="{route}"/>'

        # RxNorm code
        rxnorm_code = getattr(med, "code", "") or ""
        code_system = self._code_systems.RXNORM if rxnorm_code else ""

        # Parse dose value and unit
        dose_parts = med.dose.split() if med.dose else ["", ""]
        dose_value = dose_parts[0] if dose_parts else ""
        dose_unit = dose_parts[1] if len(dose_parts) > 1 else ""

        return f"""<entry typeCode="DRIV">
  <substanceAdministration classCode="SBADM" moodCode="EVN">
    <templateId root="{self._entry_oids.MEDICATION_ACTIVITY}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <statusCode code="{status_code}"/>
    {effective_time}
    {route_xml}
    <doseQuantity value="{dose_value}" unit="{dose_unit}"/>
    <consumable>
      <manufacturedProduct classCode="MANU">
        <templateId root="{self._entry_oids.MEDICATION_INFORMATION}" extension="2014-06-09"/>
        <manufacturedMaterial>
          <code code="{rxnorm_code}" codeSystem="{code_system}" codeSystemName="RxNorm" displayName="{self._escape_xml(med.name)}"/>
        </manufacturedMaterial>
      </manufacturedProduct>
    </consumable>
  </substanceAdministration>
</entry>"""

    def build_allergies(self, allergies: list[Any]) -> str | None:
        """Build Allergies and Intolerances section.

        Template OID: 2.16.840.1.113883.10.20.22.2.6.1
        LOINC: 48765-2 (Allergies and adverse reactions)

        Handles "No Known Allergies" with negationInd="true" pattern.

        Args:
            allergies: List of allergy objects (dict or dataclass with substance,
                      reaction, severity, status fields)

        Returns:
            XML string for Allergies section or None if no data
        """
        # Handle No Known Allergies case
        if not allergies:
            return self._build_no_known_allergies_section()

        # Build narrative table
        rows = []
        for allergy in allergies:
            substance = self._get_attr(allergy, "substance", "Unknown")
            reaction = self._get_attr(allergy, "reaction", "")
            severity = self._get_attr(allergy, "severity", "")
            status = self._get_attr(allergy, "status", "active")
            rows.append(
                f"<tr><td>{self._escape_xml(substance)}</td>"
                f"<td>{self._escape_xml(reaction)}</td>"
                f"<td>{severity}</td><td>{status}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Substance</th><th>Reaction</th><th>Severity</th><th>Status</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        entries = [self._build_allergy_entry(allergy) for allergy in allergies]

        return self._build_section_wrapper(
            template_oid=self._section_oids.ALLERGIES,
            loinc_code="48765-2",
            title="Allergies and Intolerances",
            display_name="Allergies and adverse reactions",
            narrative=narrative,
            entries=entries,
        )

    def _build_no_known_allergies_section(self) -> str:
        """Build Allergies section with No Known Allergies assertion."""
        concern_id = str(uuid.uuid4())
        obs_id = str(uuid.uuid4())
        effective_time = self._format_datetime(datetime.now())

        narrative = """<text>
  <paragraph>No Known Allergies</paragraph>
</text>"""

        entry = f"""<entry typeCode="DRIV">
  <act classCode="ACT" moodCode="EVN">
    <templateId root="{self._entry_oids.ALLERGY_CONCERN_ACT}" extension="2015-08-01"/>
    <id root="{concern_id}"/>
    <code code="CONC" codeSystem="{self._code_systems.ACT_CODE}" displayName="Concern"/>
    <statusCode code="active"/>
    <effectiveTime><low value="{effective_time}"/></effectiveTime>
    <entryRelationship typeCode="SUBJ">
      <observation classCode="OBS" moodCode="EVN" negationInd="true">
        <templateId root="{self._entry_oids.ALLERGY_OBSERVATION}" extension="2014-06-09"/>
        <id root="{obs_id}"/>
        <code code="ASSERTION" codeSystem="{self._code_systems.ACT_CODE}"/>
        <statusCode code="completed"/>
        <effectiveTime><low value="{effective_time}"/></effectiveTime>
        <value xsi:type="CD" code="419199007" codeSystem="{self._code_systems.SNOMED}" displayName="Allergy to substance"/>
        <participant typeCode="CSM">
          <participantRole classCode="MANU">
            <playingEntity classCode="MMAT">
              <code nullFlavor="NA"/>
            </playingEntity>
          </participantRole>
        </participant>
      </observation>
    </entryRelationship>
  </act>
</entry>"""

        return self._build_section_wrapper(
            template_oid=self._section_oids.ALLERGIES,
            loinc_code="48765-2",
            title="Allergies and Intolerances",
            display_name="Allergies and adverse reactions",
            narrative=narrative,
            entries=[entry],
        )

    def _build_allergy_entry(self, allergy: Any) -> str:
        """Build Allergy Concern Act with Allergy Observation."""
        concern_id = str(uuid.uuid4())
        obs_id = str(uuid.uuid4())
        reaction_id = str(uuid.uuid4())

        substance = self._get_attr(allergy, "substance", "Unknown")
        substance_code = self._get_attr(allergy, "substance_code", "")
        reaction = self._get_attr(allergy, "reaction", "")
        reaction_code = self._get_attr(allergy, "reaction_code", "")
        severity = self._get_attr(allergy, "severity", "moderate")
        status = self._get_attr(allergy, "status", "active")
        onset_date = self._get_attr(allergy, "onset_date", None)

        status_code = "active" if status == "active" else "completed"
        onset_time = self._format_datetime(onset_date) if onset_date else ""

        # Severity code mapping
        severity_codes = {
            "mild": ("255604002", "Mild"),
            "moderate": ("6736007", "Moderate"),
            "severe": ("24484000", "Severe"),
        }
        severity_code, severity_display = severity_codes.get(
            severity.lower(), ("6736007", "Moderate")
        )

        # Build reaction observation if reaction provided
        reaction_xml = ""
        if reaction:
            reaction_xml = f"""
    <entryRelationship typeCode="MFST" inversionInd="true">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="{self._entry_oids.REACTION_OBSERVATION}" extension="2014-06-09"/>
        <id root="{reaction_id}"/>
        <code code="ASSERTION" codeSystem="{self._code_systems.ACT_CODE}"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="{reaction_code}" codeSystem="{self._code_systems.SNOMED}" displayName="{self._escape_xml(reaction)}"/>
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="{self._entry_oids.SEVERITY_OBSERVATION}" extension="2014-06-09"/>
            <id root="{str(uuid.uuid4())}"/>
            <code code="SEV" codeSystem="{self._code_systems.ACT_CODE}" displayName="Severity"/>
            <statusCode code="completed"/>
            <value xsi:type="CD" code="{severity_code}" codeSystem="{self._code_systems.SNOMED}" displayName="{severity_display}"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>"""

        return f"""<entry typeCode="DRIV">
  <act classCode="ACT" moodCode="EVN">
    <templateId root="{self._entry_oids.ALLERGY_CONCERN_ACT}" extension="2015-08-01"/>
    <id root="{concern_id}"/>
    <code code="CONC" codeSystem="{self._code_systems.ACT_CODE}" displayName="Concern"/>
    <statusCode code="{status_code}"/>
    <effectiveTime><low value="{onset_time}"/></effectiveTime>
    <entryRelationship typeCode="SUBJ">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="{self._entry_oids.ALLERGY_OBSERVATION}" extension="2014-06-09"/>
        <id root="{obs_id}"/>
        <code code="ASSERTION" codeSystem="{self._code_systems.ACT_CODE}"/>
        <statusCode code="completed"/>
        <effectiveTime><low value="{onset_time}"/></effectiveTime>
        <value xsi:type="CD" code="419199007" codeSystem="{self._code_systems.SNOMED}" displayName="Allergy to substance"/>
        <participant typeCode="CSM">
          <participantRole classCode="MANU">
            <playingEntity classCode="MMAT">
              <code code="{substance_code}" codeSystem="{self._code_systems.RXNORM}" displayName="{self._escape_xml(substance)}"/>
            </playingEntity>
          </participantRole>
        </participant>{reaction_xml}
      </observation>
    </entryRelationship>
  </act>
</entry>"""

    def build_results(self, lab_results: list[LabResult]) -> str | None:
        """Build Results section with laboratory results.

        Template OID: 2.16.840.1.113883.10.20.22.2.3.1
        LOINC: 30954-2 (Relevant diagnostic tests/laboratory data)

        Groups labs by panel using Result Organizer.

        Args:
            lab_results: List of LabResult objects

        Returns:
            XML string for Results section or None if no data
        """
        if not lab_results:
            return None

        # Build narrative table
        rows = []
        for lab in lab_results:
            collected = lab.collected_time.strftime("%Y-%m-%d %H:%M") if lab.collected_time else ""
            ref_range = getattr(lab, "reference_range", "") or ""
            flag = getattr(lab, "abnormal_flag", "") or ""
            rows.append(
                f"<tr><td>{self._escape_xml(lab.test_name)}</td>"
                f"<td>{lab.value} {lab.unit or ''}</td>"
                f"<td>{ref_range}</td><td>{flag}</td><td>{collected}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Test</th><th>Result</th><th>Reference Range</th><th>Flag</th><th>Date</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        # Group labs by panel (if panel_name attribute exists)
        panels = self._group_labs_by_panel(lab_results)
        entries = []
        for panel_name, labs in panels.items():
            entry = self._build_result_organizer(panel_name, labs)
            entries.append(entry)

        return self._build_section_wrapper(
            template_oid=self._section_oids.RESULTS,
            loinc_code="30954-2",
            title="Results",
            display_name="Relevant diagnostic tests/laboratory data",
            narrative=narrative,
            entries=entries,
        )

    def _group_labs_by_panel(self, labs: list[LabResult]) -> dict[str, list[LabResult]]:
        """Group lab results by panel name."""
        panels: dict[str, list[LabResult]] = {}
        for lab in labs:
            panel_name = getattr(lab, "panel_name", None) or "Individual Tests"
            if panel_name not in panels:
                panels[panel_name] = []
            panels[panel_name].append(lab)
        return panels

    def _build_result_organizer(self, panel_name: str, labs: list[LabResult]) -> str:
        """Build Result Organizer with Result Observations."""
        organizer_id = str(uuid.uuid4())

        # Use first lab's LOINC as panel code, or generic
        panel_loinc = ""
        if labs:
            first_lab = labs[0]
            panel_loinc = (
                getattr(first_lab, "panel_loinc", "") or getattr(first_lab, "loinc_code", "") or ""
            )

        collected_time = ""
        if labs and labs[0].collected_time:
            collected_time = self._format_datetime(labs[0].collected_time)

        # Build component observations
        observations = []
        for lab in labs:
            obs = self._build_result_observation(lab)
            observations.append(obs)

        return f"""<entry typeCode="DRIV">
  <organizer classCode="CLUSTER" moodCode="EVN">
    <templateId root="{self._entry_oids.RESULT_ORGANIZER}" extension="2015-08-01"/>
    <id root="{organizer_id}"/>
    <code code="{panel_loinc}" codeSystem="{self._code_systems.LOINC}" codeSystemName="LOINC" displayName="{self._escape_xml(panel_name)}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{collected_time}"/>
    {"".join(observations)}
  </organizer>
</entry>"""

    def _build_result_observation(self, lab: LabResult) -> str:
        """Build single Result Observation."""
        obs_id = str(uuid.uuid4())
        loinc_code = getattr(lab, "loinc_code", "") or ""
        collected_time = self._format_datetime(lab.collected_time) if lab.collected_time else ""

        # Build reference range if available
        ref_range = getattr(lab, "reference_range", None)
        ref_range_xml = ""
        if ref_range:
            ref_range_xml = f"<referenceRange><observationRange><text>{self._escape_xml(ref_range)}</text></observationRange></referenceRange>"

        # Determine value type (PQ for numeric, ST for string)
        try:
            float(lab.value)
            value_xml = f'<value xsi:type="PQ" value="{lab.value}" unit="{lab.unit or ""}"/>'
        except (ValueError, TypeError):
            value_xml = f'<value xsi:type="ST">{self._escape_xml(lab.value)}</value>'

        return f"""<component>
  <observation classCode="OBS" moodCode="EVN">
    <templateId root="{self._entry_oids.RESULT_OBSERVATION}" extension="2015-08-01"/>
    <id root="{obs_id}"/>
    <code code="{loinc_code}" codeSystem="{self._code_systems.LOINC}" codeSystemName="LOINC" displayName="{self._escape_xml(lab.test_name)}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{collected_time}"/>
    {value_xml}
    {ref_range_xml}
  </observation>
</component>"""

    def build_vital_signs(self, observations: list[VitalSign]) -> str | None:
        """Build Vital Signs section.

        Template OID: 2.16.840.1.113883.10.20.22.2.4.1
        LOINC: 8716-3 (Vital Signs)

        Groups vitals by datetime into Vital Signs Organizer.
        Handles BP as compound observation with systolic + diastolic.

        Args:
            observations: List of VitalSign objects

        Returns:
            XML string for Vital Signs section or None if no data
        """
        if not observations:
            return None

        # Build narrative table
        rows = []
        for vital in observations:
            obs_time = (
                vital.observation_time.strftime("%Y-%m-%d %H:%M") if vital.observation_time else ""
            )
            bp = (
                f"{vital.systolic_bp}/{vital.diastolic_bp}"
                if vital.systolic_bp and vital.diastolic_bp
                else ""
            )
            hr = str(vital.heart_rate) if vital.heart_rate else ""
            rr = str(vital.respiratory_rate) if vital.respiratory_rate else ""
            temp = str(vital.temperature) if vital.temperature else ""
            spo2 = str(vital.spo2) if vital.spo2 else ""
            rows.append(
                f"<tr><td>{obs_time}</td><td>{bp}</td>"
                f"<td>{hr}</td><td>{rr}</td><td>{temp}</td><td>{spo2}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Date/Time</th><th>BP (mmHg)</th><th>HR (bpm)</th><th>RR (/min)</th><th>Temp (F)</th><th>SpO2 (%)</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        entries = [self._build_vital_signs_organizer(vital) for vital in observations]

        return self._build_section_wrapper(
            template_oid=self._section_oids.VITAL_SIGNS,
            loinc_code="8716-3",
            title="Vital Signs",
            display_name="Vital Signs",
            narrative=narrative,
            entries=entries,
        )

    def _build_vital_signs_organizer(self, vital: VitalSign) -> str:
        """Build Vital Signs Organizer with individual observations."""
        organizer_id = str(uuid.uuid4())
        obs_time = self._format_datetime(vital.observation_time) if vital.observation_time else ""

        # LOINC codes and units for each vital
        vital_mappings = [
            ("systolic_bp", vital.systolic_bp, "8480-6", "Systolic blood pressure", "mm[Hg]"),
            (
                "diastolic_bp",
                vital.diastolic_bp,
                "8462-4",
                "Diastolic blood pressure",
                "mm[Hg]",
            ),
            ("heart_rate", vital.heart_rate, "8867-4", "Heart rate", "/min"),
            ("respiratory_rate", vital.respiratory_rate, "9279-1", "Respiratory rate", "/min"),
            ("temperature", vital.temperature, "8310-5", "Body temperature", "[degF]"),
            ("spo2", vital.spo2, "2708-6", "Oxygen saturation", "%"),
            ("height_cm", vital.height_cm, "8302-2", "Body height", "cm"),
            ("weight_kg", vital.weight_kg, "29463-7", "Body weight", "kg"),
        ]

        components = []
        for _, value, loinc_code, display, unit in vital_mappings:
            if value is not None:
                obs_id = str(uuid.uuid4())
                components.append(
                    f"""<component>
  <observation classCode="OBS" moodCode="EVN">
    <templateId root="{self._entry_oids.VITAL_SIGNS_OBSERVATION}" extension="2014-06-09"/>
    <id root="{obs_id}"/>
    <code code="{loinc_code}" codeSystem="{self._code_systems.LOINC}" codeSystemName="LOINC" displayName="{display}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{obs_time}"/>
    <value xsi:type="PQ" value="{value}" unit="{unit}"/>
  </observation>
</component>"""
                )

        return f"""<entry typeCode="DRIV">
  <organizer classCode="CLUSTER" moodCode="EVN">
    <templateId root="{self._entry_oids.VITAL_SIGNS_ORGANIZER}" extension="2014-06-09"/>
    <id root="{organizer_id}"/>
    <code code="46680005" codeSystem="{self._code_systems.SNOMED}" codeSystemName="SNOMED CT" displayName="Vital signs"/>
    <statusCode code="completed"/>
    <effectiveTime value="{obs_time}"/>
    {"".join(components)}
  </organizer>
</entry>"""

    def build_procedures(self, procedures: list[Procedure]) -> str | None:
        """Build Procedures section.

        Template OID: 2.16.840.1.113883.10.20.22.2.7.1
        LOINC: 47519-4 (History of Procedures)

        Args:
            procedures: List of Procedure objects

        Returns:
            XML string for Procedures section or None if no data
        """
        if not procedures:
            return None

        # Build narrative table
        rows = []
        for proc in procedures:
            proc_date = (
                proc.performed_date.strftime("%Y-%m-%d")
                if hasattr(proc, "performed_date") and proc.performed_date
                else ""
            )
            performer = getattr(proc, "performer", "") or ""
            rows.append(
                f"<tr><td>{self._escape_xml(proc.description)}</td>"
                f"<td>{proc.code}</td><td>{proc_date}</td><td>{performer}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Procedure</th><th>Code</th><th>Date</th><th>Performer</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        entries = [self._build_procedure_entry(proc) for proc in procedures]

        return self._build_section_wrapper(
            template_oid=self._section_oids.PROCEDURES,
            loinc_code="47519-4",
            title="Procedures",
            display_name="History of Procedures",
            narrative=narrative,
            entries=entries,
        )

    def _build_procedure_entry(self, proc: Procedure) -> str:
        """Build Procedure Activity Procedure entry."""
        entry_id = str(uuid.uuid4())
        proc_time = (
            self._format_datetime(proc.performed_date)
            if hasattr(proc, "performed_date") and proc.performed_date
            else ""
        )

        # Determine code system
        code_system = self._code_systems.SNOMED
        code_system_name = "SNOMED CT"
        if hasattr(proc, "code_system") and proc.code_system and "cpt" in proc.code_system.lower():
            code_system = self._code_systems.CPT
            code_system_name = "CPT"

        return f"""<entry typeCode="DRIV">
  <procedure classCode="PROC" moodCode="EVN">
    <templateId root="{self._entry_oids.PROCEDURE_ACTIVITY}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <code code="{proc.code}" codeSystem="{code_system}" codeSystemName="{code_system_name}" displayName="{self._escape_xml(proc.description)}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{proc_time}"/>
  </procedure>
</entry>"""

    def build_immunizations(self, immunizations: list[Any]) -> str | None:
        """Build Immunizations section.

        Template OID: 2.16.840.1.113883.10.20.22.2.2.1
        LOINC: 11369-6 (History of Immunization)

        Args:
            immunizations: List of immunization objects (dict or dataclass with
                          vaccine_name, cvx_code, administered_date fields)

        Returns:
            XML string for Immunizations section or None if no data
        """
        if not immunizations:
            return None

        # Build narrative table
        rows = []
        for imm in immunizations:
            vaccine = self._get_attr(imm, "vaccine_name", "Unknown")
            admin_date = self._get_attr(imm, "administered_date", None)
            date_str = admin_date.strftime("%Y-%m-%d") if admin_date else ""
            status = self._get_attr(imm, "status", "completed")
            rows.append(
                f"<tr><td>{self._escape_xml(vaccine)}</td>"
                f"<td>{date_str}</td><td>{status}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Vaccine</th><th>Date</th><th>Status</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        entries = [self._build_immunization_entry(imm) for imm in immunizations]

        return self._build_section_wrapper(
            template_oid=self._section_oids.IMMUNIZATIONS,
            loinc_code="11369-6",
            title="Immunizations",
            display_name="History of Immunization",
            narrative=narrative,
            entries=entries,
        )

    def _build_immunization_entry(self, imm: Any) -> str:
        """Build Immunization Activity entry."""
        entry_id = str(uuid.uuid4())

        vaccine = self._get_attr(imm, "vaccine_name", "Unknown")
        cvx_code = self._get_attr(imm, "cvx_code", "")
        admin_date = self._get_attr(imm, "administered_date", None)
        status = self._get_attr(imm, "status", "completed")
        lot_number = self._get_attr(imm, "lot_number", "")

        admin_time = self._format_datetime(admin_date) if admin_date else ""
        status_code = "completed" if status == "completed" else "active"
        negation = 'negationInd="true" ' if status == "refused" else ""

        return f"""<entry typeCode="DRIV">
  <substanceAdministration classCode="SBADM" moodCode="EVN" {negation}>
    <templateId root="{self._entry_oids.IMMUNIZATION_ACTIVITY}" extension="2015-08-01"/>
    <id root="{entry_id}"/>
    <statusCode code="{status_code}"/>
    <effectiveTime value="{admin_time}"/>
    <consumable>
      <manufacturedProduct classCode="MANU">
        <templateId root="2.16.840.1.113883.10.20.22.4.54" extension="2014-06-09"/>
        <manufacturedMaterial>
          <code code="{cvx_code}" codeSystem="{self._code_systems.CVX}" codeSystemName="CVX" displayName="{self._escape_xml(vaccine)}"/>
          <lotNumberText>{lot_number}</lotNumberText>
        </manufacturedMaterial>
      </manufacturedProduct>
    </consumable>
  </substanceAdministration>
</entry>"""

    def build_plan_of_treatment(self, care_plan: Any) -> str | None:
        """Build Plan of Treatment section.

        Template OID: 2.16.840.1.113883.10.20.22.2.10
        LOINC: 18776-5 (Plan of care note)

        Args:
            care_plan: Care plan object with planned_procedures, planned_observations,
                      planned_medications, goals attributes (lists or single items)

        Returns:
            XML string for Plan of Treatment section or None if no data
        """
        if not care_plan:
            return None

        planned_procedures = self._get_attr(care_plan, "planned_procedures", []) or []
        planned_observations = self._get_attr(care_plan, "planned_observations", []) or []
        planned_medications = self._get_attr(care_plan, "planned_medications", []) or []
        goals = self._get_attr(care_plan, "goals", []) or []

        if not any([planned_procedures, planned_observations, planned_medications, goals]):
            return None

        # Build narrative
        narrative_parts = []

        if goals:
            goal_items = [f"<item>{self._escape_xml(g)}</item>" for g in goals]
            narrative_parts.append(
                f'<paragraph><content styleCode="Bold">Goals:</content></paragraph>'
                f"<list>{''.join(goal_items)}</list>"
            )

        if planned_procedures:
            proc_items = []
            for proc in planned_procedures:
                name = self._get_attr(proc, "name", str(proc))
                proc_items.append(f"<item>{self._escape_xml(name)}</item>")
            narrative_parts.append(
                f'<paragraph><content styleCode="Bold">Planned Procedures:</content></paragraph>'
                f"<list>{''.join(proc_items)}</list>"
            )

        if planned_medications:
            med_items = []
            for med in planned_medications:
                name = self._get_attr(med, "name", str(med))
                med_items.append(f"<item>{self._escape_xml(name)}</item>")
            narrative_parts.append(
                f'<paragraph><content styleCode="Bold">Planned Medications:</content></paragraph>'
                f"<list>{''.join(med_items)}</list>"
            )

        narrative = f"<text>{''.join(narrative_parts)}</text>"

        # Build entries
        entries = []
        for proc in planned_procedures:
            entries.append(self._build_planned_procedure_entry(proc))
        for obs in planned_observations:
            entries.append(self._build_planned_observation_entry(obs))
        for med in planned_medications:
            entries.append(self._build_planned_medication_entry(med))

        return self._build_section_wrapper(
            template_oid=self._section_oids.PLAN_OF_TREATMENT,
            loinc_code="18776-5",
            title="Plan of Treatment",
            display_name="Plan of care note",
            narrative=narrative,
            entries=entries,
            extension="2014-06-09",
        )

    def _build_planned_procedure_entry(self, proc: Any) -> str:
        """Build Planned Procedure entry."""
        entry_id = str(uuid.uuid4())
        name = self._get_attr(proc, "name", str(proc))
        code = self._get_attr(proc, "code", "")
        planned_date = self._get_attr(proc, "planned_date", None)
        planned_time = self._format_datetime(planned_date) if planned_date else ""

        return f"""<entry typeCode="DRIV">
  <procedure classCode="PROC" moodCode="INT">
    <templateId root="{self._entry_oids.PLANNED_PROCEDURE}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <code code="{code}" codeSystem="{self._code_systems.SNOMED}" displayName="{self._escape_xml(name)}"/>
    <statusCode code="active"/>
    <effectiveTime value="{planned_time}"/>
  </procedure>
</entry>"""

    def _build_planned_observation_entry(self, obs: Any) -> str:
        """Build Planned Observation entry."""
        entry_id = str(uuid.uuid4())
        name = self._get_attr(obs, "name", str(obs))
        code = self._get_attr(obs, "loinc_code", "")

        return f"""<entry typeCode="DRIV">
  <observation classCode="OBS" moodCode="INT">
    <templateId root="{self._entry_oids.PLANNED_OBSERVATION}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <code code="{code}" codeSystem="{self._code_systems.LOINC}" displayName="{self._escape_xml(name)}"/>
    <statusCode code="active"/>
  </observation>
</entry>"""

    def _build_planned_medication_entry(self, med: Any) -> str:
        """Build Planned Medication Activity entry."""
        entry_id = str(uuid.uuid4())
        name = self._get_attr(med, "name", str(med))
        rxnorm_code = self._get_attr(med, "rxnorm_code", "")

        return f"""<entry typeCode="DRIV">
  <substanceAdministration classCode="SBADM" moodCode="INT">
    <templateId root="{self._entry_oids.PLANNED_MEDICATION}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <statusCode code="active"/>
    <consumable>
      <manufacturedProduct classCode="MANU">
        <manufacturedMaterial>
          <code code="{rxnorm_code}" codeSystem="{self._code_systems.RXNORM}" displayName="{self._escape_xml(name)}"/>
        </manufacturedMaterial>
      </manufacturedProduct>
    </consumable>
  </substanceAdministration>
</entry>"""

    def build_encounters(self, encounters: list[Encounter]) -> str | None:
        """Build Encounters section.

        Template OID: 2.16.840.1.113883.10.20.22.2.22.1
        LOINC: 46240-8 (History of encounters)

        Args:
            encounters: List of Encounter objects

        Returns:
            XML string for Encounters section or None if no data
        """
        if not encounters:
            return None

        # Build narrative table
        rows = []
        for enc in encounters:
            enc_type = (
                getattr(enc, "class_code", "").value
                if hasattr(enc.class_code, "value")
                else str(enc.class_code)
            )
            admit_date = enc.admission_time.strftime("%Y-%m-%d") if enc.admission_time else ""
            discharge_date = enc.discharge_time.strftime("%Y-%m-%d") if enc.discharge_time else ""
            location = getattr(enc, "facility", "") or ""
            rows.append(
                f"<tr><td>{enc_type}</td><td>{admit_date}</td>"
                f"<td>{discharge_date}</td><td>{location}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Type</th><th>Admission</th><th>Discharge</th><th>Location</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        entries = [self._build_encounter_entry(enc) for enc in encounters]

        return self._build_section_wrapper(
            template_oid=self._section_oids.ENCOUNTERS,
            loinc_code="46240-8",
            title="Encounters",
            display_name="History of encounters",
            narrative=narrative,
            entries=entries,
        )

    def _build_encounter_entry(self, enc: Encounter) -> str:
        """Build Encounter Activity entry."""
        entry_id = str(uuid.uuid4())

        # Map encounter class to CPT codes
        class_code = getattr(enc, "class_code", "")
        class_value = class_code.value if hasattr(class_code, "value") else str(class_code)
        cpt_codes = {
            "I": ("99223", "Inpatient visit"),
            "O": ("99214", "Office/outpatient visit"),
            "E": ("99285", "Emergency department visit"),
            "U": ("99215", "Urgent care visit"),
        }
        cpt_code, cpt_display = cpt_codes.get(class_value, ("99214", "Office visit"))

        start_time = self._format_datetime(enc.admission_time) if enc.admission_time else ""
        end_time = self._format_datetime(enc.discharge_time) if enc.discharge_time else ""

        # Build effectiveTime
        if start_time and end_time:
            effective_time = f'<effectiveTime><low value="{start_time}"/><high value="{end_time}"/></effectiveTime>'
        elif start_time:
            effective_time = f'<effectiveTime><low value="{start_time}"/></effectiveTime>'
        else:
            effective_time = '<effectiveTime nullFlavor="UNK"/>'

        return f"""<entry typeCode="DRIV">
  <encounter classCode="ENC" moodCode="EVN">
    <templateId root="{self._entry_oids.ENCOUNTER_ACTIVITY}" extension="2015-08-01"/>
    <id root="{entry_id}"/>
    <code code="{cpt_code}" codeSystem="{self._code_systems.CPT}" codeSystemName="CPT" displayName="{cpt_display}"/>
    {effective_time}
  </encounter>
</entry>"""

    def build_social_history(self, patient: Patient) -> str | None:
        """Build Social History section.

        Template OID: 2.16.840.1.113883.10.20.22.2.17
        LOINC: 29762-2 (Social history)

        Includes smoking status and other social factors.

        Args:
            patient: Patient object with social history attributes

        Returns:
            XML string for Social History section or None if no data
        """
        smoking_status = getattr(patient, "smoking_status", None)
        occupation = getattr(patient, "occupation", None)
        alcohol_use = getattr(patient, "alcohol_use", None)

        if not any([smoking_status, occupation, alcohol_use]):
            return None

        # Build narrative
        narrative_parts = []
        if smoking_status:
            narrative_parts.append(
                f'<paragraph><content styleCode="Bold">Smoking Status:</content> {self._escape_xml(smoking_status)}</paragraph>'
            )
        if occupation:
            narrative_parts.append(
                f'<paragraph><content styleCode="Bold">Occupation:</content> {self._escape_xml(occupation)}</paragraph>'
            )
        if alcohol_use:
            narrative_parts.append(
                f'<paragraph><content styleCode="Bold">Alcohol Use:</content> {self._escape_xml(alcohol_use)}</paragraph>'
            )

        narrative = f"<text>{''.join(narrative_parts)}</text>"

        entries = []
        if smoking_status:
            entries.append(self._build_smoking_status_entry(smoking_status))

        return self._build_section_wrapper(
            template_oid=self._section_oids.SOCIAL_HISTORY,
            loinc_code="29762-2",
            title="Social History",
            display_name="Social history",
            narrative=narrative,
            entries=entries,
        )

    def _build_smoking_status_entry(self, smoking_status: str) -> str:
        """Build Smoking Status Observation entry."""
        entry_id = str(uuid.uuid4())
        effective_time = self._format_datetime(datetime.now())

        # Map smoking status to SNOMED codes
        smoking_codes = {
            "current": ("449868002", "Current every day smoker"),
            "former": ("8517006", "Former smoker"),
            "never": ("266919005", "Never smoker"),
            "unknown": ("266927001", "Tobacco smoking consumption unknown"),
        }
        status_lower = smoking_status.lower()
        snomed_code, snomed_display = smoking_codes.get(
            status_lower, ("266927001", "Tobacco smoking consumption unknown")
        )

        return f"""<entry typeCode="DRIV">
  <observation classCode="OBS" moodCode="EVN">
    <templateId root="{self._entry_oids.SMOKING_STATUS}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <code code="72166-2" codeSystem="{self._code_systems.LOINC}" displayName="Tobacco smoking status"/>
    <statusCode code="completed"/>
    <effectiveTime value="{effective_time}"/>
    <value xsi:type="CD" code="{snomed_code}" codeSystem="{self._code_systems.SNOMED}" displayName="{snomed_display}"/>
  </observation>
</entry>"""

    # =========================================================================
    # Document-Specific Sections
    # =========================================================================

    def build_hospital_course(self, course_narrative: str) -> str | None:
        """Build Hospital Course section (Discharge Summary specific).

        Template OID: 2.16.840.1.113883.10.20.22.2.16
        LOINC: 8648-8 (Hospital course)

        Args:
            course_narrative: Free-text narrative of hospital stay

        Returns:
            XML string for Hospital Course section or None if no data
        """
        if not course_narrative:
            return None

        narrative = f"<text>{self._escape_xml(course_narrative)}</text>"

        return self._build_section_wrapper(
            template_oid=self._section_oids.HOSPITAL_COURSE,
            loinc_code="8648-8",
            title="Hospital Course",
            display_name="Hospital course",
            narrative=narrative,
            entries=[],
        )

    def build_discharge_instructions(self, instructions: str) -> str | None:
        """Build Discharge Instructions section (Discharge Summary specific).

        Template OID: 2.16.840.1.113883.10.20.22.2.41
        LOINC: 8653-8 (Hospital discharge instructions)

        Args:
            instructions: Patient discharge instructions text

        Returns:
            XML string for Discharge Instructions section or None if no data
        """
        if not instructions:
            return None

        narrative = f"<text>{self._escape_xml(instructions)}</text>"

        return self._build_section_wrapper(
            template_oid=self._section_oids.DISCHARGE_INSTRUCTIONS,
            loinc_code="8653-8",
            title="Discharge Instructions",
            display_name="Hospital discharge instructions",
            narrative=narrative,
            entries=[],
        )

    def build_reason_for_referral(self, reason: str, details: str | None = None) -> str | None:
        """Build Reason for Referral section (Referral Note specific).

        Template OID: 1.3.6.1.4.1.19376.1.5.3.1.3.1
        LOINC: 42349-1 (Reason for referral)

        Args:
            reason: Primary reason for specialist referral
            details: Additional details or context

        Returns:
            XML string for Reason for Referral section or None if no data
        """
        if not reason:
            return None

        narrative_text = self._escape_xml(reason)
        if details:
            narrative_text += f"\n\n{self._escape_xml(details)}"

        narrative = f"<text><paragraph>{narrative_text}</paragraph></text>"

        return self._build_section_wrapper(
            template_oid=self._section_oids.REASON_FOR_REFERRAL,
            loinc_code="42349-1",
            title="Reason for Referral",
            display_name="Reason for referral",
            narrative=narrative,
            entries=[],
            extension="2014-06-09",
        )

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _build_section_wrapper(
        self,
        template_oid: str,
        loinc_code: str,
        title: str,
        display_name: str,
        narrative: str,
        entries: list[str],
        extension: str = "2015-08-01",
    ) -> str:
        """Build consistent section structure wrapper.

        Args:
            template_oid: Section template OID
            loinc_code: LOINC code for section
            title: Human-readable section title
            display_name: LOINC display name
            narrative: Narrative text block (with <text> tags)
            entries: List of entry XML strings
            extension: Template version extension

        Returns:
            Complete section XML string
        """
        entries_xml = "".join(entries) if entries else ""

        return f"""<component>
  <section>
    <templateId root="{template_oid}" extension="{extension}"/>
    <code code="{loinc_code}" codeSystem="{self._code_systems.LOINC}" codeSystemName="LOINC" displayName="{display_name}"/>
    <title>{title}</title>
    {narrative}
    {entries_xml}
  </section>
</component>"""

    def _format_datetime(self, dt: datetime | Any | None) -> str:
        """Format datetime for CDA (YYYYMMDDHHMMSS format)."""
        if dt is None:
            return ""
        if hasattr(dt, "strftime"):
            return dt.strftime("%Y%m%d%H%M%S")
        return ""

    def _escape_xml(self, text: str | None) -> str:
        """Escape text for XML content."""
        if text is None:
            return ""
        return html.escape(str(text))

    def _get_attr(self, obj: Any, attr: str, default: Any = None) -> Any:
        """Get attribute from object, dict, or return default."""
        if isinstance(obj, dict):
            return obj.get(attr, default)
        return getattr(obj, attr, default)

    def _get_route_code(self, route: str) -> str:
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
        }
        return route_codes.get(route.upper(), route)
