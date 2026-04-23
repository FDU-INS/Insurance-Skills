"""HL7v2 segment builders.

Functions to build individual HL7v2 segments following the specification.
Uses pipe-delimited format with proper field encoding.
"""

from datetime import datetime

from patientsim.core.models import Encounter, Patient

# HL7v2 field delimiters
FIELD_SEP = "|"
COMPONENT_SEP = "^"
REPETITION_SEP = "~"
ESCAPE_CHAR = "\\"
SUBCOMPONENT_SEP = "&"

# Encoding characters after field separator
ENCODING_CHARS = f"{COMPONENT_SEP}{REPETITION_SEP}{ESCAPE_CHAR}{SUBCOMPONENT_SEP}"


def escape_hl7(text: str) -> str:
    """Escape special characters for HL7v2.

    Args:
        text: Text to escape

    Returns:
        Escaped text
    """
    if not text:
        return ""
    # Basic escaping - only escape the delimiters, not the escape character itself
    # to avoid double-escaping in typical use
    return (
        text.replace("|", "\\F\\").replace("^", "\\S\\").replace("~", "\\R\\").replace("&", "\\T\\")
    )


def format_hl7_datetime(dt: datetime) -> str:
    """Format datetime for HL7v2.

    Args:
        dt: Datetime to format

    Returns:
        HL7 datetime string (YYYYMMDDHHmmss)
    """
    return dt.strftime("%Y%m%d%H%M%S")


def format_hl7_date(dt: datetime | None) -> str:
    """Format date for HL7v2.

    Args:
        dt: Date to format

    Returns:
        HL7 date string (YYYYMMDD)
    """
    if not dt:
        return ""
    if hasattr(dt, "strftime"):
        return dt.strftime("%Y%m%d")
    return ""


def build_msh_segment(
    message_type: str,
    trigger_event: str,
    message_control_id: str,
    timestamp: datetime,
    sending_application: str = "PATIENTSIM",
    sending_facility: str = "HOSPITAL",
    receiving_application: str = "EMR",
    receiving_facility: str = "HOSPITAL",
) -> str:
    """Build MSH (Message Header) segment.

    Args:
        message_type: Message type (e.g., "ADT")
        trigger_event: Trigger event (e.g., "A01")
        message_control_id: Unique message control ID
        timestamp: Message timestamp
        sending_application: Sending application name
        sending_facility: Sending facility name
        receiving_application: Receiving application name
        receiving_facility: Receiving facility name

    Returns:
        MSH segment string
    """
    fields = [
        "MSH",
        ENCODING_CHARS,  # MSH-2: Encoding characters
        sending_application,  # MSH-3: Sending application
        sending_facility,  # MSH-4: Sending facility
        receiving_application,  # MSH-5: Receiving application
        receiving_facility,  # MSH-6: Receiving facility
        format_hl7_datetime(timestamp),  # MSH-7: Date/Time of message
        "",  # MSH-8: Security
        f"{message_type}{COMPONENT_SEP}{trigger_event}",  # MSH-9: Message type
        message_control_id,  # MSH-10: Message control ID
        "P",  # MSH-11: Processing ID (P=Production, T=Test, D=Debug)
        "2.5",  # MSH-12: Version ID
    ]

    return FIELD_SEP.join(fields)


def build_evn_segment(
    event_type: str,
    event_timestamp: datetime,
    event_reason_code: str | None = None,
) -> str:
    """Build EVN (Event Type) segment.

    Args:
        event_type: Event type code (e.g., "A01")
        event_timestamp: When the event occurred
        event_reason_code: Reason code for the event

    Returns:
        EVN segment string
    """
    fields = [
        "EVN",
        event_type,  # EVN-1: Event type code
        format_hl7_datetime(event_timestamp),  # EVN-2: Recorded date/time
        "",  # EVN-3: Date/time planned event
        event_reason_code or "",  # EVN-4: Event reason code
    ]

    return FIELD_SEP.join(fields)


def build_pid_segment(patient: Patient) -> str:
    """Build PID (Patient Identification) segment.

    Args:
        patient: Patient object

    Returns:
        PID segment string
    """
    # Build patient name (Last^First^Middle)
    patient_name = (
        f"{escape_hl7(patient.family_name)}{COMPONENT_SEP}{escape_hl7(patient.given_name)}"
    )

    # Format birth date
    birth_date = format_hl7_date(patient.birth_date) if patient.birth_date else ""

    # Map gender
    gender = patient.gender  # Already "M", "F", "O", or "U"

    # Handle deceased indicator
    deceased_indicator = "Y" if patient.deceased else "N"
    deceased_datetime = (
        format_hl7_datetime(patient.death_date) if patient.death_date and patient.deceased else ""
    )

    fields = [
        "PID",
        "1",  # PID-1: Set ID
        "",  # PID-2: Patient ID (deprecated)
        patient.mrn,  # PID-3: Patient identifier list
        "",  # PID-4: Alternate patient ID
        patient_name,  # PID-5: Patient name
        "",  # PID-6: Mother's maiden name
        birth_date,  # PID-7: Date/time of birth
        gender,  # PID-8: Administrative sex
        "",  # PID-9: Patient alias
        "",  # PID-10: Race
        "",  # PID-11: Patient address
        "",  # PID-12: County code
        "",  # PID-13: Phone number - home
        "",  # PID-14: Phone number - business
        "",  # PID-15: Primary language
        "",  # PID-16: Marital status
        "",  # PID-17: Religion
        "",  # PID-18: Patient account number
        "",  # PID-19: SSN
        "",  # PID-20: Driver's license number
        "",  # PID-21: Mother's identifier
        "",  # PID-22: Ethnic group
        "",  # PID-23: Birth place
        "",  # PID-24: Multiple birth indicator
        "",  # PID-25: Birth order
        "",  # PID-26: Citizenship
        "",  # PID-27: Veterans military status
        "",  # PID-28: Nationality
        "",  # PID-29: Patient death date and time
        deceased_indicator if deceased_datetime else "",  # PID-30: Patient death indicator
    ]

    # Add death datetime if deceased
    if deceased_datetime:
        fields[29] = deceased_datetime  # PID-29

    return FIELD_SEP.join(fields)


def build_pv1_segment(encounter: Encounter, patient_class: str | None = None) -> str:
    """Build PV1 (Patient Visit) segment.

    Args:
        encounter: Encounter object
        patient_class: Patient class override (I=Inpatient, O=Outpatient, E=Emergency)

    Returns:
        PV1 segment string
    """
    # Map encounter class to HL7 patient class
    class_map = {
        "I": "I",  # Inpatient
        "O": "O",  # Outpatient
        "E": "E",  # Emergency
        "U": "O",  # Urgent -> Outpatient
    }
    patient_class = patient_class or class_map.get(encounter.class_code, "O")

    # Format admission time
    admit_datetime = (
        format_hl7_datetime(encounter.admission_time) if encounter.admission_time else ""
    )

    # Format discharge time
    discharge_datetime = (
        format_hl7_datetime(encounter.discharge_time) if encounter.discharge_time else ""
    )

    # Admission type
    admission_type_map = {
        "I": "1",  # Emergency
        "E": "1",  # Emergency
        "O": "2",  # Urgent
        "U": "2",  # Urgent
    }
    admission_type = admission_type_map.get(encounter.class_code, "3")  # 3=Elective

    # Discharge disposition
    discharge_disposition = ""
    if encounter.discharge_disposition:
        disp = encounter.discharge_disposition.upper()
        if "HOME" in disp:
            discharge_disposition = "01"  # Home
        elif "SNF" in disp or "NURSING" in disp:
            discharge_disposition = "03"  # SNF
        elif "REHAB" in disp:
            discharge_disposition = "02"  # Rehab
        elif "DEAD" in disp or "EXPIRED" in disp or "DECEASED" in disp:
            discharge_disposition = "20"  # Expired
        else:
            discharge_disposition = "01"  # Default to home

    fields = [
        "PV1",
        "1",  # PV1-1: Set ID
        patient_class,  # PV1-2: Patient class
        "",  # PV1-3: Assigned patient location
        admission_type,  # PV1-4: Admission type
        "",  # PV1-5: Preadmit number
        "",  # PV1-6: Prior patient location
        "",  # PV1-7: Attending doctor
        "",  # PV1-8: Referring doctor
        "",  # PV1-9: Consulting doctor
        "",  # PV1-10: Hospital service
        "",  # PV1-11: Temporary location
        "",  # PV1-12: Preadmit test indicator
        "",  # PV1-13: Re-admission indicator
        "",  # PV1-14: Admit source
        "",  # PV1-15: Ambulatory status
        "",  # PV1-16: VIP indicator
        "",  # PV1-17: Admitting doctor
        "",  # PV1-18: Patient type
        encounter.encounter_id,  # PV1-19: Visit number
        "",  # PV1-20: Financial class
        "",  # PV1-21: Charge price indicator
        "",  # PV1-22: Courtesy code
        "",  # PV1-23: Credit rating
        "",  # PV1-24: Contract code
        "",  # PV1-25: Contract effective date
        "",  # PV1-26: Contract amount
        "",  # PV1-27: Contract period
        "",  # PV1-28: Interest code
        "",  # PV1-29: Transfer to bad debt code
        "",  # PV1-30: Transfer to bad debt date
        "",  # PV1-31: Bad debt agency code
        "",  # PV1-32: Bad debt transfer amount
        "",  # PV1-33: Bad debt recovery amount
        "",  # PV1-34: Delete account indicator
        "",  # PV1-35: Delete account date
        discharge_disposition,  # PV1-36: Discharge disposition
        "",  # PV1-37: Discharged to location
        "",  # PV1-38: Diet type
        "",  # PV1-39: Servicing facility
        "",  # PV1-40: Bed status
        "",  # PV1-41: Account status
        "",  # PV1-42: Pending location
        "",  # PV1-43: Prior temporary location
        admit_datetime,  # PV1-44: Admit date/time
        discharge_datetime if discharge_datetime else "",  # PV1-45: Discharge date/time
    ]

    return FIELD_SEP.join(fields)


def build_dg1_segment(
    diagnosis_code: str,
    diagnosis_text: str,
    set_id: int = 1,
    diagnosis_type: str = "F",
) -> str:
    """Build DG1 (Diagnosis) segment.

    Args:
        diagnosis_code: ICD diagnosis code
        diagnosis_text: Diagnosis description
        set_id: Sequence number
        diagnosis_type: Type (A=Admitting, W=Working, F=Final)

    Returns:
        DG1 segment string
    """
    fields = [
        "DG1",
        str(set_id),  # DG1-1: Set ID
        "",  # DG1-2: Diagnosis coding method (deprecated)
        f"{diagnosis_code}{COMPONENT_SEP}{escape_hl7(diagnosis_text)}{COMPONENT_SEP}I10",  # DG1-3: Diagnosis code
        "",  # DG1-4: Diagnosis description (deprecated)
        "",  # DG1-5: Diagnosis date/time
        diagnosis_type,  # DG1-6: Diagnosis type
    ]

    return FIELD_SEP.join(fields)
