"""Export utilities for JSON and CSV formats.

Provides simple export functions for PatientSim models to JSON and CSV formats.
For healthcare-specific formats (FHIR, HL7v2, C-CDA), use the dedicated transformers.
"""

import csv
import json
from datetime import date, datetime
from decimal import Decimal
from io import StringIO
from typing import Any

from pydantic import BaseModel


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for PatientSim models."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        if hasattr(obj, "value"):  # Enum
            return obj.value
        return super().default(obj)


def to_json(data: Any, pretty: bool = True) -> str:
    """Convert data to JSON string.

    Args:
        data: Model instance, list, or dict
        pretty: Use indentation for readability

    Returns:
        JSON string
    """
    indent = 2 if pretty else None

    if isinstance(data, BaseModel):
        return json.dumps(data.model_dump(), cls=JSONEncoder, indent=indent)
    elif isinstance(data, list):
        items = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
        return json.dumps(items, cls=JSONEncoder, indent=indent)
    else:
        return json.dumps(data, cls=JSONEncoder, indent=indent)


def to_csv(data: list[BaseModel], include_header: bool = True) -> str:
    """Convert list of models to CSV string.

    Args:
        data: List of Pydantic model instances
        include_header: Include column headers

    Returns:
        CSV string
    """
    if not data:
        return ""

    output = StringIO()

    # Get fields from first item
    first = data[0]
    fields = list(first.model_fields.keys())

    writer = csv.DictWriter(output, fieldnames=fields)

    if include_header:
        writer.writeheader()

    for item in data:
        row = {}
        for field in fields:
            value = getattr(item, field)
            if isinstance(value, datetime | date):
                row[field] = value.isoformat()
            elif isinstance(value, Decimal):
                row[field] = str(value)
            elif isinstance(value, list):
                row[field] = "|".join(str(v) for v in value)
            elif isinstance(value, BaseModel):
                row[field] = json.dumps(value.model_dump(), cls=JSONEncoder)
            elif hasattr(value, "value"):  # Enum
                row[field] = value.value
            else:
                row[field] = value
        writer.writerow(row)

    return output.getvalue()


def patients_to_csv(patients: list) -> str:
    """Export patients to CSV with flattened demographics.

    Args:
        patients: List of Patient instances

    Returns:
        CSV string with patient data
    """
    output = StringIO()

    fields = [
        "mrn",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "street",
        "city",
        "state",
        "zip_code",
        "race",
        "language",
        "ssn",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for patient in patients:
        # Handle Person-based Patient
        addr = patient.address if hasattr(patient, "address") else None

        row = {
            "mrn": patient.mrn,
            "first_name": patient.name.given_name if hasattr(patient, "name") else "",
            "last_name": patient.name.family_name if hasattr(patient, "name") else "",
            "date_of_birth": patient.birth_date.isoformat() if patient.birth_date else "",
            "gender": (
                patient.gender.value if hasattr(patient.gender, "value") else str(patient.gender)
            ),
            "street": addr.street if addr else "",
            "city": addr.city if addr else "",
            "state": addr.state if addr else "",
            "zip_code": addr.zip_code if addr else "",
            "race": getattr(patient, "race", "") or "",
            "language": getattr(patient, "language", "en"),
            "ssn": getattr(patient, "ssn", "") or "",
        }
        writer.writerow(row)

    return output.getvalue()


def encounters_to_csv(encounters: list) -> str:
    """Export encounters to CSV.

    Args:
        encounters: List of Encounter instances

    Returns:
        CSV string with encounter data
    """
    output = StringIO()

    fields = [
        "encounter_id",
        "patient_mrn",
        "class_code",
        "status",
        "admission_time",
        "discharge_time",
        "facility",
        "department",
        "chief_complaint",
        "discharge_disposition",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for encounter in encounters:
        row = {
            "encounter_id": encounter.encounter_id,
            "patient_mrn": encounter.patient_mrn,
            "class_code": (
                encounter.class_code.value
                if hasattr(encounter.class_code, "value")
                else str(encounter.class_code)
            ),
            "status": (
                encounter.status.value
                if hasattr(encounter.status, "value")
                else str(encounter.status)
            ),
            "admission_time": (
                encounter.admission_time.isoformat() if encounter.admission_time else ""
            ),
            "discharge_time": (
                encounter.discharge_time.isoformat() if encounter.discharge_time else ""
            ),
            "facility": encounter.facility or "",
            "department": encounter.department or "",
            "chief_complaint": encounter.chief_complaint or "",
            "discharge_disposition": encounter.discharge_disposition or "",
        }
        writer.writerow(row)

    return output.getvalue()


def diagnoses_to_csv(diagnoses: list) -> str:
    """Export diagnoses to CSV.

    Args:
        diagnoses: List of Diagnosis instances

    Returns:
        CSV string with diagnosis data
    """
    output = StringIO()

    fields = [
        "diagnosis_id",
        "patient_mrn",
        "encounter_id",
        "code",
        "code_system",
        "description",
        "type",
        "onset_date",
        "resolved_date",
        "is_principal",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for dx in diagnoses:
        row = {
            "diagnosis_id": getattr(dx, "diagnosis_id", ""),
            "patient_mrn": getattr(dx, "patient_mrn", ""),
            "encounter_id": getattr(dx, "encounter_id", ""),
            "code": dx.code,
            "code_system": getattr(dx, "code_system", "ICD-10-CM"),
            "description": dx.description,
            "type": dx.type.value if hasattr(dx.type, "value") else str(dx.type),
            "onset_date": (
                dx.onset_date.isoformat() if hasattr(dx, "onset_date") and dx.onset_date else ""
            ),
            "resolved_date": (
                dx.resolved_date.isoformat()
                if hasattr(dx, "resolved_date") and dx.resolved_date
                else ""
            ),
            "is_principal": getattr(dx, "is_principal", False),
        }
        writer.writerow(row)

    return output.getvalue()


def medications_to_csv(medications: list) -> str:
    """Export medications to CSV.

    Args:
        medications: List of Medication instances

    Returns:
        CSV string with medication data
    """
    output = StringIO()

    fields = [
        "medication_id",
        "patient_mrn",
        "name",
        "code",
        "code_system",
        "dose",
        "dose_unit",
        "route",
        "frequency",
        "start_date",
        "end_date",
        "status",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for med in medications:
        row = {
            "medication_id": getattr(med, "medication_id", ""),
            "patient_mrn": getattr(med, "patient_mrn", ""),
            "name": med.name,
            "code": getattr(med, "code", ""),
            "code_system": getattr(med, "code_system", "RxNorm"),
            "dose": getattr(med, "dose", ""),
            "dose_unit": getattr(med, "dose_unit", ""),
            "route": getattr(med, "route", ""),
            "frequency": getattr(med, "frequency", ""),
            "start_date": (
                med.start_date.isoformat() if hasattr(med, "start_date") and med.start_date else ""
            ),
            "end_date": (
                med.end_date.isoformat() if hasattr(med, "end_date") and med.end_date else ""
            ),
            "status": med.status.value if hasattr(med.status, "value") else str(med.status),
        }
        writer.writerow(row)

    return output.getvalue()


def labs_to_csv(labs: list) -> str:
    """Export lab results to CSV.

    Args:
        labs: List of LabResult instances

    Returns:
        CSV string with lab result data
    """
    output = StringIO()

    fields = [
        "result_id",
        "patient_mrn",
        "encounter_id",
        "test_code",
        "test_name",
        "value",
        "units",
        "reference_range",
        "abnormal_flag",
        "result_time",
        "status",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for lab in labs:
        row = {
            "result_id": getattr(lab, "result_id", ""),
            "patient_mrn": getattr(lab, "patient_mrn", ""),
            "encounter_id": getattr(lab, "encounter_id", ""),
            "test_code": lab.test_code,
            "test_name": lab.test_name,
            "value": str(lab.value) if lab.value is not None else "",
            "units": getattr(lab, "units", ""),
            "reference_range": getattr(lab, "reference_range", ""),
            "abnormal_flag": getattr(lab, "abnormal_flag", ""),
            "result_time": (
                lab.result_time.isoformat()
                if hasattr(lab, "result_time") and lab.result_time
                else ""
            ),
            "status": getattr(lab, "status", ""),
        }
        writer.writerow(row)

    return output.getvalue()


def vitals_to_csv(vitals: list) -> str:
    """Export vital signs to CSV.

    Args:
        vitals: List of VitalSign instances

    Returns:
        CSV string with vital signs data
    """
    output = StringIO()

    fields = [
        "vital_id",
        "patient_mrn",
        "encounter_id",
        "observation_time",
        "temperature",
        "heart_rate",
        "respiratory_rate",
        "systolic_bp",
        "diastolic_bp",
        "spo2",
        "weight_kg",
        "height_cm",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for vital in vitals:
        row = {
            "vital_id": getattr(vital, "vital_id", ""),
            "patient_mrn": getattr(vital, "patient_mrn", ""),
            "encounter_id": getattr(vital, "encounter_id", ""),
            "observation_time": (
                vital.observation_time.isoformat()
                if hasattr(vital, "observation_time") and vital.observation_time
                else ""
            ),
            "temperature": getattr(vital, "temperature", "") or "",
            "heart_rate": getattr(vital, "heart_rate", "") or "",
            "respiratory_rate": getattr(vital, "respiratory_rate", "") or "",
            "systolic_bp": getattr(vital, "systolic_bp", "") or "",
            "diastolic_bp": getattr(vital, "diastolic_bp", "") or "",
            "spo2": getattr(vital, "spo2", "") or "",
            "weight_kg": getattr(vital, "weight_kg", "") or "",
            "height_cm": getattr(vital, "height_cm", "") or "",
        }
        writer.writerow(row)

    return output.getvalue()
