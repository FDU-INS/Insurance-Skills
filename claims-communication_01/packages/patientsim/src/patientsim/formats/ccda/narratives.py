"""C-CDA narrative builders.

Generates human-readable HTML narrative content for C-CDA section/text elements.
Uses content elements with ID attributes that can link to entry elements.
"""

from __future__ import annotations

import html
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from patientsim.core.models import (
        Diagnosis,
        Encounter,
        LabResult,
        Medication,
        Procedure,
        VitalSign,
    )


class NarrativeBuilder:
    """Builds HTML narrative content for C-CDA sections.

    Generates structured HTML tables with content elements that include
    ID attributes for linking to machine-readable entries.

    Example:
        >>> builder = NarrativeBuilder()
        >>> problems_html = builder.build_problems_narrative(diagnoses)
        >>> meds_html = builder.build_medications_narrative(medications)
    """

    def build_problems_narrative(self, diagnoses: list[Diagnosis]) -> str:
        """Build narrative for Problems section.

        Creates HTML table with columns: Condition, Status, Onset Date

        Args:
            diagnoses: List of Diagnosis objects

        Returns:
            HTML string for section/text element
        """
        if not diagnoses:
            return "<text><paragraph>No known problems</paragraph></text>"

        rows = []
        for idx, diag in enumerate(diagnoses):
            content_id = f"problem-{idx + 1}"
            is_active = getattr(diag, "is_active", True)
            status = "Active" if is_active else "Resolved"
            onset = (
                diag.diagnosed_date.strftime("%Y-%m-%d")
                if hasattr(diag, "diagnosed_date") and diag.diagnosed_date
                else ""
            )
            resolved = ""
            if hasattr(diag, "resolved_date") and diag.resolved_date:
                resolved = diag.resolved_date.strftime("%Y-%m-%d")

            rows.append(
                f'<tr><td><content ID="{content_id}">{self._escape(diag.description)}</content></td>'
                f"<td>{diag.code}</td>"
                f"<td>{status}</td>"
                f"<td>{onset}</td>"
                f"<td>{resolved}</td></tr>"
            )

        return f"""<text>
  <table border="1" width="100%">
    <thead>
      <tr>
        <th>Condition</th>
        <th>Code</th>
        <th>Status</th>
        <th>Onset Date</th>
        <th>Resolved Date</th>
      </tr>
    </thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
</text>"""

    def build_medications_narrative(self, medications: list[Medication]) -> str:
        """Build narrative for Medications section.

        Creates HTML table with columns: Medication, Dose, Frequency, Start Date, Status

        Args:
            medications: List of Medication objects

        Returns:
            HTML string for section/text element
        """
        if not medications:
            return "<text><paragraph>No current medications</paragraph></text>"

        rows = []
        for idx, med in enumerate(medications):
            content_id = f"medication-{idx + 1}"
            status = getattr(med, "status", "active")
            route = getattr(med, "route", "")
            start_date = med.start_date.strftime("%Y-%m-%d") if med.start_date else ""
            indication = getattr(med, "indication", "") or ""

            rows.append(
                f'<tr><td><content ID="{content_id}">{self._escape(med.name)}</content></td>'
                f"<td>{self._escape(med.dose)}</td>"
                f"<td>{route}</td>"
                f"<td>{med.frequency}</td>"
                f"<td>{start_date}</td>"
                f"<td>{status}</td>"
                f"<td>{self._escape(indication)}</td></tr>"
            )

        return f"""<text>
  <table border="1" width="100%">
    <thead>
      <tr>
        <th>Medication</th>
        <th>Dose</th>
        <th>Route</th>
        <th>Frequency</th>
        <th>Start Date</th>
        <th>Status</th>
        <th>Indication</th>
      </tr>
    </thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
</text>"""

    def build_allergies_narrative(self, allergies: list[Any]) -> str:
        """Build narrative for Allergies section.

        Creates HTML table with columns: Allergen, Reaction, Severity
        Handles "No Known Allergies" display.

        Args:
            allergies: List of allergy objects (dict or dataclass)

        Returns:
            HTML string for section/text element
        """
        if not allergies:
            return "<text><paragraph>No Known Allergies</paragraph></text>"

        rows = []
        for idx, allergy in enumerate(allergies):
            content_id = f"allergy-{idx + 1}"
            substance = self._get_attr(allergy, "substance", "Unknown")
            reaction = self._get_attr(allergy, "reaction", "")
            severity = self._get_attr(allergy, "severity", "")
            status = self._get_attr(allergy, "status", "active")
            onset = self._get_attr(allergy, "onset_date", None)
            onset_str = onset.strftime("%Y-%m-%d") if onset else ""

            rows.append(
                f'<tr><td><content ID="{content_id}">{self._escape(substance)}</content></td>'
                f"<td>{self._escape(reaction)}</td>"
                f"<td>{severity}</td>"
                f"<td>{status}</td>"
                f"<td>{onset_str}</td></tr>"
            )

        return f"""<text>
  <table border="1" width="100%">
    <thead>
      <tr>
        <th>Allergen</th>
        <th>Reaction</th>
        <th>Severity</th>
        <th>Status</th>
        <th>Onset Date</th>
      </tr>
    </thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
</text>"""

    def build_results_narrative(
        self, lab_results: list[LabResult], group_by_panel: bool = True
    ) -> str:
        """Build narrative for Results section.

        Creates HTML tables grouped by panel or as single list.
        Columns: Test, Value, Units, Reference Range, Flag, Date

        Args:
            lab_results: List of LabResult objects
            group_by_panel: Whether to group results by panel name

        Returns:
            HTML string for section/text element
        """
        if not lab_results:
            return "<text><paragraph>No laboratory results available</paragraph></text>"

        if group_by_panel:
            # Group labs by panel
            panels: dict[str, list[LabResult]] = {}
            for lab in lab_results:
                panel_name = getattr(lab, "panel_name", None) or "Individual Tests"
                if panel_name not in panels:
                    panels[panel_name] = []
                panels[panel_name].append(lab)

            tables = []
            result_idx = 0
            for panel_name, labs in panels.items():
                rows = []
                for lab in labs:
                    result_idx += 1
                    content_id = f"result-{result_idx}"
                    row = self._build_lab_row(lab, content_id)
                    rows.append(row)

                table = f"""<paragraph><content styleCode="Bold">{self._escape(panel_name)}</content></paragraph>
  <table border="1" width="100%">
    <thead>
      <tr><th>Test</th><th>Value</th><th>Units</th><th>Reference Range</th><th>Flag</th><th>Date</th></tr>
    </thead>
    <tbody>{"".join(rows)}</tbody>
  </table>"""
                tables.append(table)

            return f"<text>{''.join(tables)}</text>"
        else:
            rows = []
            for idx, lab in enumerate(lab_results):
                content_id = f"result-{idx + 1}"
                row = self._build_lab_row(lab, content_id)
                rows.append(row)

            return f"""<text>
  <table border="1" width="100%">
    <thead>
      <tr><th>Test</th><th>Value</th><th>Units</th><th>Reference Range</th><th>Flag</th><th>Date</th></tr>
    </thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

    def _build_lab_row(self, lab: LabResult, content_id: str) -> str:
        """Build a single lab result table row."""
        ref_range = getattr(lab, "reference_range", "") or ""
        flag = getattr(lab, "abnormal_flag", "") or ""
        collected = lab.collected_time.strftime("%Y-%m-%d %H:%M") if lab.collected_time else ""

        # Add styleCode for abnormal values
        style = ""
        if flag and flag.upper() in ("H", "HH", "L", "LL", "A"):
            style = ' styleCode="Bold"'

        return (
            f'<tr><td><content ID="{content_id}">{self._escape(lab.test_name)}</content></td>'
            f"<td{style}>{self._escape(lab.value)}</td>"
            f"<td>{lab.unit or ''}</td>"
            f"<td>{ref_range}</td>"
            f"<td>{flag}</td>"
            f"<td>{collected}</td></tr>"
        )

    def build_vital_signs_narrative(self, vitals: list[VitalSign]) -> str:
        """Build narrative for Vital Signs section.

        Creates HTML table with columns: Date/Time, BP, HR, Temp, RR, SpO2, Wt

        Args:
            vitals: List of VitalSign objects

        Returns:
            HTML string for section/text element
        """
        if not vitals:
            return "<text><paragraph>No vital signs recorded</paragraph></text>"

        rows = []
        for idx, vital in enumerate(vitals):
            content_id = f"vitals-{idx + 1}"
            obs_time = (
                vital.observation_time.strftime("%Y-%m-%d %H:%M") if vital.observation_time else ""
            )

            # Format values
            bp = ""
            if vital.systolic_bp is not None and vital.diastolic_bp is not None:
                bp = f"{vital.systolic_bp}/{vital.diastolic_bp}"

            hr = str(vital.heart_rate) if vital.heart_rate is not None else ""
            temp = f"{vital.temperature}" if vital.temperature is not None else ""
            rr = str(vital.respiratory_rate) if vital.respiratory_rate is not None else ""
            spo2 = f"{vital.spo2}%" if vital.spo2 is not None else ""
            weight = f"{vital.weight_kg} kg" if vital.weight_kg is not None else ""
            height = f"{vital.height_cm} cm" if vital.height_cm is not None else ""

            rows.append(
                f'<tr><td><content ID="{content_id}">{obs_time}</content></td>'
                f"<td>{bp}</td>"
                f"<td>{hr}</td>"
                f"<td>{temp}</td>"
                f"<td>{rr}</td>"
                f"<td>{spo2}</td>"
                f"<td>{weight}</td>"
                f"<td>{height}</td></tr>"
            )

        return f"""<text>
  <table border="1" width="100%">
    <thead>
      <tr>
        <th>Date/Time</th>
        <th>BP (mmHg)</th>
        <th>HR (bpm)</th>
        <th>Temp (F)</th>
        <th>RR (/min)</th>
        <th>SpO2</th>
        <th>Weight</th>
        <th>Height</th>
      </tr>
    </thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
</text>"""

    def build_procedures_narrative(self, procedures: list[Procedure]) -> str:
        """Build narrative for Procedures section.

        Creates HTML table with columns: Procedure, Code, Date, Performer

        Args:
            procedures: List of Procedure objects

        Returns:
            HTML string for section/text element
        """
        if not procedures:
            return "<text><paragraph>No procedures documented</paragraph></text>"

        rows = []
        for idx, proc in enumerate(procedures):
            content_id = f"procedure-{idx + 1}"
            proc_date = ""
            if hasattr(proc, "performed_date") and proc.performed_date:
                proc_date = proc.performed_date.strftime("%Y-%m-%d")
            performer = getattr(proc, "performer", "") or ""
            location = getattr(proc, "location", "") or ""

            rows.append(
                f'<tr><td><content ID="{content_id}">{self._escape(proc.description)}</content></td>'
                f"<td>{proc.code}</td>"
                f"<td>{proc_date}</td>"
                f"<td>{self._escape(performer)}</td>"
                f"<td>{self._escape(location)}</td></tr>"
            )

        return f"""<text>
  <table border="1" width="100%">
    <thead>
      <tr>
        <th>Procedure</th>
        <th>Code</th>
        <th>Date</th>
        <th>Performer</th>
        <th>Location</th>
      </tr>
    </thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
</text>"""

    def build_immunizations_narrative(self, immunizations: list[Any]) -> str:
        """Build narrative for Immunizations section.

        Creates HTML table with columns: Vaccine, Date, Status, Lot Number

        Args:
            immunizations: List of immunization objects

        Returns:
            HTML string for section/text element
        """
        if not immunizations:
            return "<text><paragraph>No immunizations recorded</paragraph></text>"

        rows = []
        for idx, imm in enumerate(immunizations):
            content_id = f"immunization-{idx + 1}"
            vaccine = self._get_attr(imm, "vaccine_name", "Unknown")
            admin_date = self._get_attr(imm, "administered_date", None)
            date_str = admin_date.strftime("%Y-%m-%d") if admin_date else ""
            status = self._get_attr(imm, "status", "completed")
            lot = self._get_attr(imm, "lot_number", "") or ""

            rows.append(
                f'<tr><td><content ID="{content_id}">{self._escape(vaccine)}</content></td>'
                f"<td>{date_str}</td>"
                f"<td>{status}</td>"
                f"<td>{lot}</td></tr>"
            )

        return f"""<text>
  <table border="1" width="100%">
    <thead>
      <tr>
        <th>Vaccine</th>
        <th>Date</th>
        <th>Status</th>
        <th>Lot Number</th>
      </tr>
    </thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
</text>"""

    def build_encounters_narrative(self, encounters: list[Encounter]) -> str:
        """Build narrative for Encounters section.

        Creates HTML table with columns: Type, Admission, Discharge, Location, Reason

        Args:
            encounters: List of Encounter objects

        Returns:
            HTML string for section/text element
        """
        if not encounters:
            return "<text><paragraph>No encounters documented</paragraph></text>"

        rows = []
        for idx, enc in enumerate(encounters):
            content_id = f"encounter-{idx + 1}"

            # Get encounter type
            class_code = getattr(enc, "class_code", "")
            enc_type = class_code.value if hasattr(class_code, "value") else str(class_code)
            type_names = {
                "I": "Inpatient",
                "O": "Outpatient",
                "E": "Emergency",
                "U": "Urgent Care",
            }
            enc_type_display = type_names.get(enc_type, enc_type)

            admit_date = enc.admission_time.strftime("%Y-%m-%d %H:%M") if enc.admission_time else ""
            discharge_date = (
                enc.discharge_time.strftime("%Y-%m-%d %H:%M") if enc.discharge_time else ""
            )
            location = getattr(enc, "facility", "") or ""
            reason = (
                getattr(enc, "chief_complaint", "") or getattr(enc, "admitting_diagnosis", "") or ""
            )

            rows.append(
                f'<tr><td><content ID="{content_id}">{enc_type_display}</content></td>'
                f"<td>{admit_date}</td>"
                f"<td>{discharge_date}</td>"
                f"<td>{self._escape(location)}</td>"
                f"<td>{self._escape(reason)}</td></tr>"
            )

        return f"""<text>
  <table border="1" width="100%">
    <thead>
      <tr>
        <th>Type</th>
        <th>Admission</th>
        <th>Discharge</th>
        <th>Facility</th>
        <th>Reason</th>
      </tr>
    </thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
</text>"""

    def build_social_history_narrative(
        self,
        smoking_status: str | None = None,
        occupation: str | None = None,
        alcohol_use: str | None = None,
        other_factors: dict[str, str] | None = None,
    ) -> str:
        """Build narrative for Social History section.

        Creates list of social history items.

        Args:
            smoking_status: Smoking status description
            occupation: Patient's occupation
            alcohol_use: Alcohol use description
            other_factors: Additional social history factors

        Returns:
            HTML string for section/text element
        """
        items = []

        if smoking_status:
            items.append(
                f'<item><content styleCode="Bold">Smoking Status:</content> {self._escape(smoking_status)}</item>'
            )

        if occupation:
            items.append(
                f'<item><content styleCode="Bold">Occupation:</content> {self._escape(occupation)}</item>'
            )

        if alcohol_use:
            items.append(
                f'<item><content styleCode="Bold">Alcohol Use:</content> {self._escape(alcohol_use)}</item>'
            )

        if other_factors:
            for factor_name, factor_value in other_factors.items():
                items.append(
                    f'<item><content styleCode="Bold">{self._escape(factor_name)}:</content> {self._escape(factor_value)}</item>'
                )

        if not items:
            return "<text><paragraph>No social history documented</paragraph></text>"

        return f"""<text>
  <list listType="unordered">
    {"".join(items)}
  </list>
</text>"""

    def build_plan_of_treatment_narrative(
        self,
        goals: list[str] | None = None,
        planned_procedures: list[Any] | None = None,
        planned_medications: list[Any] | None = None,
        planned_observations: list[Any] | None = None,
        instructions: str | None = None,
    ) -> str:
        """Build narrative for Plan of Treatment section.

        Args:
            goals: List of treatment goals
            planned_procedures: List of planned procedures
            planned_medications: List of planned medications
            planned_observations: List of planned observations/tests
            instructions: Free-text instructions

        Returns:
            HTML string for section/text element
        """
        parts = []

        if goals:
            goal_items = [f"<item>{self._escape(g)}</item>" for g in goals]
            parts.append(
                f'<paragraph><content styleCode="Bold">Goals:</content></paragraph>'
                f'<list listType="unordered">{"".join(goal_items)}</list>'
            )

        if planned_procedures:
            proc_items = []
            for proc in planned_procedures:
                name = self._get_attr(proc, "name", str(proc))
                proc_items.append(f"<item>{self._escape(name)}</item>")
            parts.append(
                f'<paragraph><content styleCode="Bold">Planned Procedures:</content></paragraph>'
                f'<list listType="unordered">{"".join(proc_items)}</list>'
            )

        if planned_medications:
            med_items = []
            for med in planned_medications:
                name = self._get_attr(med, "name", str(med))
                med_items.append(f"<item>{self._escape(name)}</item>")
            parts.append(
                f'<paragraph><content styleCode="Bold">Planned Medications:</content></paragraph>'
                f'<list listType="unordered">{"".join(med_items)}</list>'
            )

        if planned_observations:
            obs_items = []
            for obs in planned_observations:
                name = self._get_attr(obs, "name", str(obs))
                obs_items.append(f"<item>{self._escape(name)}</item>")
            parts.append(
                f'<paragraph><content styleCode="Bold">Planned Tests/Observations:</content></paragraph>'
                f'<list listType="unordered">{"".join(obs_items)}</list>'
            )

        if instructions:
            parts.append(
                f'<paragraph><content styleCode="Bold">Instructions:</content></paragraph>'
                f"<paragraph>{self._escape(instructions)}</paragraph>"
            )

        if not parts:
            return "<text><paragraph>No plan of treatment documented</paragraph></text>"

        return f"<text>{''.join(parts)}</text>"

    def build_hospital_course_narrative(self, course_text: str) -> str:
        """Build narrative for Hospital Course section.

        Args:
            course_text: Free-text description of hospital course

        Returns:
            HTML string for section/text element
        """
        if not course_text:
            return "<text><paragraph>Hospital course not documented</paragraph></text>"

        # Split into paragraphs if there are line breaks
        paragraphs = course_text.split("\n\n")
        para_xml = "".join(
            f"<paragraph>{self._escape(p.strip())}</paragraph>" for p in paragraphs if p.strip()
        )

        return f"<text>{para_xml}</text>"

    def build_discharge_instructions_narrative(self, instructions: str) -> str:
        """Build narrative for Discharge Instructions section.

        Args:
            instructions: Discharge instructions text

        Returns:
            HTML string for section/text element
        """
        if not instructions:
            return "<text><paragraph>No discharge instructions provided</paragraph></text>"

        paragraphs = instructions.split("\n\n")
        para_xml = "".join(
            f"<paragraph>{self._escape(p.strip())}</paragraph>" for p in paragraphs if p.strip()
        )

        return f"<text>{para_xml}</text>"

    def build_reason_for_referral_narrative(self, reason: str, details: str | None = None) -> str:
        """Build narrative for Reason for Referral section.

        Args:
            reason: Primary reason for referral
            details: Additional details

        Returns:
            HTML string for section/text element
        """
        if not reason:
            return "<text><paragraph>Reason for referral not specified</paragraph></text>"

        parts = [f"<paragraph>{self._escape(reason)}</paragraph>"]

        if details:
            parts.append(f"<paragraph>{self._escape(details)}</paragraph>")

        return f"<text>{''.join(parts)}</text>"

    def _escape(self, text: str | None) -> str:
        """Escape text for HTML/XML content."""
        if text is None:
            return ""
        return html.escape(str(text))

    def _get_attr(self, obj: Any, attr: str, default: Any = None) -> Any:
        """Get attribute from object, dict, or return default."""
        if isinstance(obj, dict):
            return obj.get(attr, default)
        return getattr(obj, attr, default)
