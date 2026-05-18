"""C-CDA transformer.

Converts PatientSim objects to C-CDA XML documents.
"""

import html
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from patientsim.core.models import (
    Diagnosis,
    Encounter,
    LabResult,
    Medication,
    Patient,
    Procedure,
    VitalSign,
)
from patientsim.formats.ccda.header import HeaderBuilder


class DocumentType(Enum):
    """C-CDA document types with template OID, LOINC code, and display name."""

    CCD = ("2.16.840.1.113883.10.20.22.1.2", "34133-9", "Continuity of Care Document")
    DISCHARGE_SUMMARY = ("2.16.840.1.113883.10.20.22.1.8", "18842-5", "Discharge Summary")
    REFERRAL_NOTE = ("2.16.840.1.113883.10.20.22.1.14", "57133-1", "Referral Note")
    TRANSFER_SUMMARY = ("2.16.840.1.113883.10.20.22.1.13", "18761-7", "Transfer Summary")

    @property
    def template_oid(self) -> str:
        """Return the template OID."""
        return self.value[0]

    @property
    def loinc_code(self) -> str:
        """Return the LOINC code."""
        return self.value[1]

    @property
    def display_name(self) -> str:
        """Return the display name."""
        return self.value[2]


@dataclass
class CCDAConfig:
    """Configuration for C-CDA document generation."""

    document_type: DocumentType
    organization_name: str
    organization_oid: str
    author_name: str | None = None
    author_npi: str | None = None
    custodian_name: str | None = field(default=None)
    custodian_oid: str | None = field(default=None)

    def __post_init__(self) -> None:
        """Set defaults for custodian if not provided."""
        if self.custodian_name is None:
            self.custodian_name = self.organization_name
        if self.custodian_oid is None:
            self.custodian_oid = self.organization_oid


class CCDATransformer:
    """Transforms PatientSim objects to C-CDA XML documents.

    Example:
        >>> config = CCDAConfig(
        ...     document_type=DocumentType.CCD,
        ...     organization_name="Example Hospital",
        ...     organization_oid="2.16.840.1.113883.3.1234",
        ... )
        >>> transformer = CCDATransformer(config)
        >>> xml = transformer.transform(patient, encounters, diagnoses)
    """

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"
    LOINC_OID = "2.16.840.1.113883.6.1"
    RXNORM_OID = "2.16.840.1.113883.6.88"
    ICD10_OID = "2.16.840.1.113883.6.90"
    CVX_OID = "2.16.840.1.113883.12.292"

    # Section template OIDs
    PROBLEMS_SECTION_OID = "2.16.840.1.113883.10.20.22.2.5.1"
    MEDICATIONS_SECTION_OID = "2.16.840.1.113883.10.20.22.2.1.1"
    RESULTS_SECTION_OID = "2.16.840.1.113883.10.20.22.2.3.1"
    VITAL_SIGNS_SECTION_OID = "2.16.840.1.113883.10.20.22.2.4.1"
    PROCEDURES_SECTION_OID = "2.16.840.1.113883.10.20.22.2.7.1"

    # Entry template OIDs
    PROBLEM_CONCERN_OID = "2.16.840.1.113883.10.20.22.4.3"
    PROBLEM_OBSERVATION_OID = "2.16.840.1.113883.10.20.22.4.4"
    MEDICATION_ACTIVITY_OID = "2.16.840.1.113883.10.20.22.4.16"
    RESULT_ORGANIZER_OID = "2.16.840.1.113883.10.20.22.4.1"
    RESULT_OBSERVATION_OID = "2.16.840.1.113883.10.20.22.4.2"
    VITAL_SIGNS_ORGANIZER_OID = "2.16.840.1.113883.10.20.22.4.26"
    VITAL_SIGNS_OBSERVATION_OID = "2.16.840.1.113883.10.20.22.4.27"
    PROCEDURE_ACTIVITY_OID = "2.16.840.1.113883.10.20.22.4.14"

    def __init__(self, config: CCDAConfig) -> None:
        """Initialize transformer with configuration.

        Args:
            config: C-CDA configuration settings
        """
        self.config = config
        self._header_builder = HeaderBuilder(config)

    def transform(
        self,
        patient: Patient,
        encounters: list[Encounter] | None = None,
        diagnoses: list[Diagnosis] | None = None,
        medications: list[Medication] | None = None,
        labs: list[LabResult] | None = None,
        vitals: list[VitalSign] | None = None,
        procedures: list[Procedure] | None = None,
    ) -> str:
        """Transform PatientSim data to C-CDA XML document.

        Args:
            patient: Patient object
            encounters: List of encounters (first used for encompassingEncounter)
            diagnoses: List of diagnoses for Problems section
            medications: List of medications for Medications section
            labs: List of lab results for Results section
            vitals: List of vital signs for Vital Signs section
            procedures: List of procedures for Procedures section

        Returns:
            C-CDA XML document as string
        """
        # Get primary encounter for header
        primary_encounter = encounters[0] if encounters else None

        # Build document parts
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            self._build_clinical_document_open(),
            self._header_builder.build_header(patient, primary_encounter),
            "<component>",
            "<structuredBody>",
        ]

        # Add sections based on available data
        if diagnoses:
            xml_parts.append(self._build_problems_section(diagnoses))

        if medications:
            xml_parts.append(self._build_medications_section(medications))

        if labs:
            xml_parts.append(self._build_results_section(labs))

        if vitals:
            xml_parts.append(self._build_vital_signs_section(vitals))

        if procedures:
            xml_parts.append(self._build_procedures_section(procedures))

        # Close document
        xml_parts.extend(
            [
                "</structuredBody>",
                "</component>",
                "</ClinicalDocument>",
            ]
        )

        return "\n".join(xml_parts)

    def _build_clinical_document_open(self) -> str:
        """Build opening ClinicalDocument element with namespaces and type info."""
        doc_type = self.config.document_type
        doc_id = self._generate_document_id()
        effective_time = self._format_datetime(datetime.now())

        return f"""<ClinicalDocument xmlns="urn:hl7-org:v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:sdtc="urn:hl7-org:sdtc">
  <realmCode code="US"/>
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <templateId root="{doc_type.template_oid}" extension="2015-08-01"/>
  <id root="{self.config.organization_oid}" extension="{doc_id}"/>
  <code code="{doc_type.loinc_code}" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="{doc_type.display_name}"/>
  <title>{doc_type.display_name}</title>
  <effectiveTime value="{effective_time}"/>
  <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25" displayName="Normal"/>
  <languageCode code="en-US"/>"""

    def _build_problems_section(self, diagnoses: list[Diagnosis]) -> str:
        """Build Problems section with diagnoses.

        Args:
            diagnoses: List of Diagnosis objects

        Returns:
            XML string for Problems section
        """
        # Build narrative table
        rows = []
        for diag in diagnoses:
            status = "Active" if diag.is_active else "Resolved"
            rows.append(
                f"<tr><td>{self._escape_xml(diag.description)}</td>"
                f"<td>{diag.code}</td><td>{status}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Problem</th><th>Code</th><th>Status</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        # Build entries
        entries = []
        for diag in diagnoses:
            entry = self._build_problem_entry(diag)
            entries.append(entry)

        return f"""<component>
  <section>
    <templateId root="{self.PROBLEMS_SECTION_OID}" extension="2015-08-01"/>
    <code code="11450-4" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="Problem List"/>
    <title>Problems</title>
    {narrative}
    {"".join(entries)}
  </section>
</component>"""

    def _build_problem_entry(self, diag: Diagnosis) -> str:
        """Build a Problem Concern Act entry for a diagnosis.

        Args:
            diag: Diagnosis object

        Returns:
            XML string for problem entry
        """
        entry_id = str(uuid.uuid4())
        obs_id = str(uuid.uuid4())
        status_code = "active" if diag.is_active else "completed"
        onset_time = self._format_datetime(diag.diagnosed_date) if diag.diagnosed_date else ""

        return f"""<entry typeCode="DRIV">
  <act classCode="ACT" moodCode="EVN">
    <templateId root="{self.PROBLEM_CONCERN_OID}" extension="2015-08-01"/>
    <id root="{entry_id}"/>
    <code code="CONC" codeSystem="2.16.840.1.113883.5.6" displayName="Concern"/>
    <statusCode code="{status_code}"/>
    <effectiveTime><low value="{onset_time}"/></effectiveTime>
    <entryRelationship typeCode="SUBJ">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="{self.PROBLEM_OBSERVATION_OID}" extension="2015-08-01"/>
        <id root="{obs_id}"/>
        <code code="64572001" codeSystem="{self.SNOMED_OID}" displayName="Condition"/>
        <statusCode code="completed"/>
        <effectiveTime><low value="{onset_time}"/></effectiveTime>
        <value xsi:type="CD" code="{diag.code}" codeSystem="{self.ICD10_OID}" codeSystemName="ICD-10-CM" displayName="{self._escape_xml(diag.description)}"/>
      </observation>
    </entryRelationship>
  </act>
</entry>"""

    def _build_medications_section(self, medications: list[Medication]) -> str:
        """Build Medications section.

        Args:
            medications: List of Medication objects

        Returns:
            XML string for Medications section
        """
        # Build narrative table
        rows = []
        for med in medications:
            status = med.status if hasattr(med, "status") else "active"
            rows.append(
                f"<tr><td>{self._escape_xml(med.drug_name)}</td>"
                f"<td>{med.dose} {med.unit}</td>"
                f"<td>{med.frequency}</td><td>{status}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Medication</th><th>Dose</th><th>Frequency</th><th>Status</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        # Build entries
        entries = []
        for med in medications:
            entry = self._build_medication_entry(med)
            entries.append(entry)

        return f"""<component>
  <section>
    <templateId root="{self.MEDICATIONS_SECTION_OID}" extension="2014-06-09"/>
    <code code="10160-0" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="History of Medication Use"/>
    <title>Medications</title>
    {narrative}
    {"".join(entries)}
  </section>
</component>"""

    def _build_medication_entry(self, med: Medication) -> str:
        """Build a Medication Activity entry.

        Args:
            med: Medication object

        Returns:
            XML string for medication entry
        """
        entry_id = str(uuid.uuid4())
        status_code = "active" if med.status == "active" else "completed"
        start_time = self._format_datetime(med.start_date) if med.start_date else ""
        end_time = self._format_datetime(med.end_date) if med.end_date else ""

        # Build effectiveTime based on available dates
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

        # RxNorm code if available
        rxnorm_code = med.rxnorm_code if hasattr(med, "rxnorm_code") and med.rxnorm_code else ""
        code_system = self.RXNORM_OID if rxnorm_code else ""

        return f"""<entry typeCode="DRIV">
  <substanceAdministration classCode="SBADM" moodCode="EVN">
    <templateId root="{self.MEDICATION_ACTIVITY_OID}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <statusCode code="{status_code}"/>
    {effective_time}
    <doseQuantity value="{med.dose}" unit="{med.unit}"/>
    <consumable>
      <manufacturedProduct classCode="MANU">
        <templateId root="2.16.840.1.113883.10.20.22.4.23" extension="2014-06-09"/>
        <manufacturedMaterial>
          <code code="{rxnorm_code}" codeSystem="{code_system}" codeSystemName="RxNorm" displayName="{self._escape_xml(med.drug_name)}"/>
        </manufacturedMaterial>
      </manufacturedProduct>
    </consumable>
  </substanceAdministration>
</entry>"""

    def _build_results_section(self, labs: list[LabResult]) -> str:
        """Build Results section with lab results.

        Args:
            labs: List of LabResult objects

        Returns:
            XML string for Results section
        """
        # Build narrative table
        rows = []
        for lab in labs:
            collected = lab.collected_time.strftime("%Y-%m-%d") if lab.collected_time else ""
            rows.append(
                f"<tr><td>{self._escape_xml(lab.test_name)}</td>"
                f"<td>{lab.value} {lab.unit}</td>"
                f"<td>{collected}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Test</th><th>Result</th><th>Date</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        # Build entries - group by panel if applicable
        entries = []
        for lab in labs:
            entry = self._build_result_entry(lab)
            entries.append(entry)

        return f"""<component>
  <section>
    <templateId root="{self.RESULTS_SECTION_OID}" extension="2015-08-01"/>
    <code code="30954-2" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="Relevant diagnostic tests/laboratory data"/>
    <title>Results</title>
    {narrative}
    {"".join(entries)}
  </section>
</component>"""

    def _build_result_entry(self, lab: LabResult) -> str:
        """Build a Result Organizer entry for a lab result.

        Args:
            lab: LabResult object

        Returns:
            XML string for result entry
        """
        organizer_id = str(uuid.uuid4())
        obs_id = str(uuid.uuid4())
        collected_time = self._format_datetime(lab.collected_time) if lab.collected_time else ""

        # Get LOINC code if available
        loinc_code = lab.loinc_code if hasattr(lab, "loinc_code") and lab.loinc_code else ""

        return f"""<entry typeCode="DRIV">
  <organizer classCode="CLUSTER" moodCode="EVN">
    <templateId root="{self.RESULT_ORGANIZER_OID}" extension="2015-08-01"/>
    <id root="{organizer_id}"/>
    <code code="{loinc_code}" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="{self._escape_xml(lab.test_name)}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{collected_time}"/>
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="{self.RESULT_OBSERVATION_OID}" extension="2015-08-01"/>
        <id root="{obs_id}"/>
        <code code="{loinc_code}" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="{self._escape_xml(lab.test_name)}"/>
        <statusCode code="completed"/>
        <effectiveTime value="{collected_time}"/>
        <value xsi:type="PQ" value="{lab.value}" unit="{lab.unit}"/>
      </observation>
    </component>
  </organizer>
</entry>"""

    def _build_vital_signs_section(self, vitals: list[VitalSign]) -> str:
        """Build Vital Signs section.

        Args:
            vitals: List of VitalSign objects

        Returns:
            XML string for Vital Signs section
        """
        # Build narrative table
        rows = []
        for vital in vitals:
            obs_time = (
                vital.observation_time.strftime("%Y-%m-%d %H:%M") if vital.observation_time else ""
            )
            bp = f"{vital.systolic_bp}/{vital.diastolic_bp}" if vital.systolic_bp else ""
            rows.append(
                f"<tr><td>{obs_time}</td>"
                f"<td>{bp}</td>"
                f"<td>{vital.heart_rate or ''}</td>"
                f"<td>{vital.respiratory_rate or ''}</td>"
                f"<td>{vital.temperature or ''}</td>"
                f"<td>{vital.spo2 or ''}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Date/Time</th><th>BP</th><th>HR</th><th>RR</th><th>Temp</th><th>SpO2</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        # Build entries
        entries = []
        for vital in vitals:
            entry = self._build_vital_signs_entry(vital)
            entries.append(entry)

        return f"""<component>
  <section>
    <templateId root="{self.VITAL_SIGNS_SECTION_OID}" extension="2015-08-01"/>
    <code code="8716-3" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="Vital Signs"/>
    <title>Vital Signs</title>
    {narrative}
    {"".join(entries)}
  </section>
</component>"""

    def _build_vital_signs_entry(self, vital: VitalSign) -> str:
        """Build a Vital Signs Organizer entry.

        Args:
            vital: VitalSign object

        Returns:
            XML string for vital signs entry
        """
        organizer_id = str(uuid.uuid4())
        obs_time = self._format_datetime(vital.observation_time) if vital.observation_time else ""

        # Build individual observations
        observations = []

        # LOINC codes for vital signs
        vital_mappings = [
            ("systolic_bp", vital.systolic_bp, "8480-6", "Systolic blood pressure", "mm[Hg]"),
            ("diastolic_bp", vital.diastolic_bp, "8462-4", "Diastolic blood pressure", "mm[Hg]"),
            ("heart_rate", vital.heart_rate, "8867-4", "Heart rate", "/min"),
            ("respiratory_rate", vital.respiratory_rate, "9279-1", "Respiratory rate", "/min"),
            ("temperature", vital.temperature, "8310-5", "Body temperature", "[degF]"),
            ("spo2", vital.spo2, "2708-6", "Oxygen saturation", "%"),
            ("height_cm", vital.height_cm, "8302-2", "Body height", "cm"),
            ("weight_kg", vital.weight_kg, "29463-7", "Body weight", "kg"),
        ]

        for _, value, loinc_code, display, unit in vital_mappings:
            if value is not None:
                obs_id = str(uuid.uuid4())
                observations.append(
                    f"""<component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="{self.VITAL_SIGNS_OBSERVATION_OID}" extension="2014-06-09"/>
        <id root="{obs_id}"/>
        <code code="{loinc_code}" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="{display}"/>
        <statusCode code="completed"/>
        <effectiveTime value="{obs_time}"/>
        <value xsi:type="PQ" value="{value}" unit="{unit}"/>
      </observation>
    </component>"""
                )

        return f"""<entry typeCode="DRIV">
  <organizer classCode="CLUSTER" moodCode="EVN">
    <templateId root="{self.VITAL_SIGNS_ORGANIZER_OID}" extension="2014-06-09"/>
    <id root="{organizer_id}"/>
    <code code="46680005" codeSystem="{self.SNOMED_OID}" codeSystemName="SNOMED CT" displayName="Vital signs"/>
    <statusCode code="completed"/>
    <effectiveTime value="{obs_time}"/>
    {"".join(observations)}
  </organizer>
</entry>"""

    def _build_procedures_section(self, procedures: list[Procedure]) -> str:
        """Build Procedures section.

        Args:
            procedures: List of Procedure objects

        Returns:
            XML string for Procedures section
        """
        # Build narrative table
        rows = []
        for proc in procedures:
            proc_date = proc.procedure_date.strftime("%Y-%m-%d") if proc.procedure_date else ""
            rows.append(
                f"<tr><td>{self._escape_xml(proc.description)}</td>"
                f"<td>{proc.code}</td><td>{proc_date}</td></tr>"
            )

        narrative = f"""<text>
  <table border="1" width="100%">
    <thead><tr><th>Procedure</th><th>Code</th><th>Date</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</text>"""

        # Build entries
        entries = []
        for proc in procedures:
            entry = self._build_procedure_entry(proc)
            entries.append(entry)

        return f"""<component>
  <section>
    <templateId root="{self.PROCEDURES_SECTION_OID}" extension="2014-06-09"/>
    <code code="47519-4" codeSystem="{self.LOINC_OID}" codeSystemName="LOINC" displayName="History of Procedures"/>
    <title>Procedures</title>
    {narrative}
    {"".join(entries)}
  </section>
</component>"""

    def _build_procedure_entry(self, proc: Procedure) -> str:
        """Build a Procedure Activity entry.

        Args:
            proc: Procedure object

        Returns:
            XML string for procedure entry
        """
        entry_id = str(uuid.uuid4())
        proc_time = self._format_datetime(proc.procedure_date) if proc.procedure_date else ""

        # Determine code system (CPT vs SNOMED)
        code_system = self.SNOMED_OID
        code_system_name = "SNOMED CT"
        if hasattr(proc, "code_system") and proc.code_system and "cpt" in proc.code_system.lower():
            code_system = "2.16.840.1.113883.6.12"
            code_system_name = "CPT"

        return f"""<entry typeCode="DRIV">
  <procedure classCode="PROC" moodCode="EVN">
    <templateId root="{self.PROCEDURE_ACTIVITY_OID}" extension="2014-06-09"/>
    <id root="{entry_id}"/>
    <code code="{proc.code}" codeSystem="{code_system}" codeSystemName="{code_system_name}" displayName="{self._escape_xml(proc.description)}"/>
    <statusCode code="completed"/>
    <effectiveTime value="{proc_time}"/>
  </procedure>
</entry>"""

    def _generate_document_id(self) -> str:
        """Generate a unique document ID.

        Returns:
            UUID string for document identification
        """
        return str(uuid.uuid4())

    def _format_datetime(self, dt: datetime | None) -> str:
        """Format datetime for CDA (YYYYMMDDHHMMSS format).

        Args:
            dt: Datetime object or None

        Returns:
            Formatted datetime string or empty string
        """
        if dt is None:
            return ""
        return dt.strftime("%Y%m%d%H%M%S")

    def _escape_xml(self, text: str | None) -> str:
        """Escape text for XML content.

        Args:
            text: Text to escape

        Returns:
            XML-escaped text
        """
        if text is None:
            return ""
        return html.escape(text)
