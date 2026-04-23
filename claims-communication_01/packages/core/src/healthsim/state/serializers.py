"""
Entity serialization between canonical models and database.

Handles the mapping between in-memory entity dicts (from EntityWithProvenance)
and their database representations in canonical tables.
"""

from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4
from datetime import datetime, date
import json


def _get_nested(obj: Dict, *keys, default=None) -> Any:
    """Safely get nested dictionary value."""
    for key in keys:
        if obj is None or not isinstance(obj, dict):
            return default
        obj = obj.get(key)
    return obj if obj is not None else default


def _parse_date(value: Any) -> Optional[date]:
    """Parse date from various formats."""
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00')).date()
        except ValueError:
            return None
    return None


def _parse_datetime(value: Any) -> Optional[datetime]:
    """Parse datetime from various formats."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return None
    return None


# ============================================================================
# Patient Serialization
# ============================================================================

def serialize_patient(entity: Dict[str, Any], provenance: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Prepare a patient entity for database insertion.
    
    Handles multiple input formats:
    - FHIR-like nested: {name: {given: ..., family: ...}, address: {line1: ...}}
    - Flat simple: {first_name: ..., last_name: ..., address_line1: ...}
    - Standard: {given_name: ..., family_name: ..., street_address: ...}
    """
    prov = provenance or entity.get('_provenance', {})
    
    # Handle various name formats (priority: given_name > first_name > nested)
    given_name = (
        entity.get('given_name') or 
        entity.get('first_name') or  # Flat format
        _get_nested(entity, 'name', 'given') or
        _get_nested(entity, 'name', 0, 'given', 0) or
        'Unknown'
    )
    family_name = (
        entity.get('family_name') or 
        entity.get('last_name') or  # Flat format
        _get_nested(entity, 'name', 'family') or
        _get_nested(entity, 'name', 0, 'family') or
        'Unknown'
    )
    
    # Handle various address formats (priority: standard > flat > nested)
    street_address = (
        entity.get('street_address') or
        entity.get('address_line1') or  # Flat format
        _get_nested(entity, 'address', 'line1') or 
        _get_nested(entity, 'address', 'line', 0)
    )
    street_address_2 = (
        entity.get('street_address_2') or
        entity.get('address_line2') or  # Flat format
        _get_nested(entity, 'address', 'line2')
    )
    city = (
        entity.get('city') or  # Flat format at top level
        _get_nested(entity, 'address', 'city')
    )
    state = (
        entity.get('state') or  # Flat format at top level
        _get_nested(entity, 'address', 'state')
    )
    postal_code = (
        entity.get('postal_code') or
        entity.get('zip_code') or  # Flat format
        entity.get('zip') or  # Short form
        _get_nested(entity, 'address', 'postalCode') or 
        _get_nested(entity, 'address', 'postal_code')
    )
    country = (
        entity.get('country') or
        _get_nested(entity, 'address', 'country') or
        'US'
    )
    
    # Handle various phone formats (priority: top-level > nested)
    phone = (
        entity.get('phone') or  # Flat format at top level
        _get_nested(entity, 'telecom', 'phone')
    )
    
    # Handle various date formats
    birth_date = _parse_date(
        entity.get('birth_date') or 
        entity.get('date_of_birth') or  # Flat format
        entity.get('birthDate') or  # FHIR format
        entity.get('dob')  # Short form
    )
    
    return {
        'id': entity.get('patient_id') or entity.get('id') or str(uuid4()),
        'mrn': entity.get('mrn') or str(uuid4())[:8].upper(),
        'ssn': entity.get('ssn'),
        'given_name': given_name,
        'middle_name': entity.get('middle_name') or _get_nested(entity, 'name', 'middle'),
        'family_name': family_name,
        'suffix': entity.get('suffix') or _get_nested(entity, 'name', 'suffix'),
        'prefix': entity.get('prefix') or _get_nested(entity, 'name', 'prefix'),
        'birth_date': birth_date,
        'gender': entity.get('gender') or entity.get('sex'),  # Accept 'sex' as alias
        'race': entity.get('race'),
        'ethnicity': entity.get('ethnicity'),
        'language': entity.get('language', 'en'),
        'street_address': street_address,
        'street_address_2': street_address_2,
        'city': city,
        'state': state,
        'postal_code': postal_code,
        'country': country,
        'phone': phone,
        'phone_mobile': entity.get('phone_mobile') or _get_nested(entity, 'telecom', 'mobile'),
        'email': entity.get('email') or _get_nested(entity, 'telecom', 'email'),
        'deceased': entity.get('deceased', False),
        'death_date': _parse_date(entity.get('death_date') or entity.get('deceasedDateTime')),
        'created_at': datetime.utcnow(),
        'source_type': prov.get('source_type', 'generated'),
        'source_system': prov.get('source_system', 'patientsim'),
        'skill_used': prov.get('skill_used'),
        'generation_seed': prov.get('seed') or prov.get('generation_seed'),
    }


def deserialize_patient(row: Tuple, columns: List[str]) -> Dict[str, Any]:
    """Convert database row back to canonical patient format."""
    data = dict(zip(columns, row))
    return {
        'patient_id': data['id'],
        'mrn': data['mrn'],
        'ssn': data['ssn'],
        'name': {
            'given': data['given_name'],
            'middle': data['middle_name'],
            'family': data['family_name'],
            'prefix': data['prefix'],
            'suffix': data['suffix'],
        },
        'birthDate': str(data['birth_date']) if data['birth_date'] else None,
        'gender': data['gender'],
        'race': data['race'],
        'ethnicity': data['ethnicity'],
        'language': data['language'],
        'address': {
            'line1': data['street_address'],
            'line2': data['street_address_2'],
            'city': data['city'],
            'state': data['state'],
            'postalCode': data['postal_code'],
            'country': data['country'],
        },
        'telecom': {
            'phone': data['phone'],
            'mobile': data['phone_mobile'],
            'email': data['email'],
        },
        'deceased': data['deceased'],
        'deceasedDateTime': str(data['death_date']) if data['death_date'] else None,
        '_provenance': {
            'source_type': data.get('source_type'),
            'source_system': data.get('source_system'),
            'skill_used': data.get('skill_used'),
            'seed': data.get('generation_seed'),
        }
    }


# ============================================================================
# Encounter Serialization
# ============================================================================

def serialize_encounter(entity: Dict[str, Any], provenance: Optional[Dict] = None) -> Dict[str, Any]:
    """Prepare an encounter entity for database insertion."""
    prov = provenance or entity.get('_provenance', {})
    
    return {
        'encounter_id': entity.get('encounter_id') or entity.get('id') or str(uuid4()),
        'patient_mrn': entity.get('patient_mrn') or entity.get('patient_id'),
        'class_code': entity.get('class_code') or entity.get('class', 'O'),
        'status': entity.get('status', 'finished'),
        'admission_time': _parse_datetime(entity.get('admission_time') or entity.get('period', {}).get('start')),
        'discharge_time': _parse_datetime(entity.get('discharge_time') or entity.get('period', {}).get('end')),
        'facility': entity.get('facility'),
        'department': entity.get('department'),
        'room': entity.get('room'),
        'bed': entity.get('bed'),
        'chief_complaint': entity.get('chief_complaint') or entity.get('reasonCode'),
        'admitting_diagnosis': entity.get('admitting_diagnosis'),
        'discharge_disposition': entity.get('discharge_disposition'),
        'attending_physician': entity.get('attending_physician'),
        'admitting_physician': entity.get('admitting_physician'),
        'created_at': datetime.utcnow(),
        'source_type': prov.get('source_type', 'generated'),
        'source_system': prov.get('source_system', 'patientsim'),
        'skill_used': prov.get('skill_used'),
        'generation_seed': prov.get('seed') or prov.get('generation_seed'),
    }


def deserialize_encounter(row: Tuple, columns: List[str]) -> Dict[str, Any]:
    """Convert database row back to canonical encounter format."""
    data = dict(zip(columns, row))
    return {
        'encounter_id': data['encounter_id'],
        'patient_mrn': data['patient_mrn'],
        'class': data['class_code'],
        'status': data['status'],
        'period': {
            'start': data['admission_time'].isoformat() if data['admission_time'] else None,
            'end': data['discharge_time'].isoformat() if data['discharge_time'] else None,
        },
        'facility': data['facility'],
        'department': data['department'],
        'room': data['room'],
        'bed': data['bed'],
        'chief_complaint': data['chief_complaint'],
        'admitting_diagnosis': data['admitting_diagnosis'],
        'discharge_disposition': data['discharge_disposition'],
        'attending_physician': data['attending_physician'],
        'admitting_physician': data['admitting_physician'],
        '_provenance': {
            'source_type': data.get('source_type'),
            'source_system': data.get('source_system'),
            'skill_used': data.get('skill_used'),
            'seed': data.get('generation_seed'),
        }
    }


# ============================================================================
# Diagnosis Serialization  
# ============================================================================

def serialize_diagnosis(entity: Dict[str, Any], provenance: Optional[Dict] = None) -> Dict[str, Any]:
    """Prepare a diagnosis entity for database insertion."""
    prov = provenance or entity.get('_provenance', {})
    
    return {
        'id': entity.get('id') or str(uuid4()),
        'code': entity.get('code'),
        'description': entity.get('description') or entity.get('display'),
        'type': entity.get('type', 'final'),
        'patient_mrn': entity.get('patient_mrn') or entity.get('patient_id'),
        'encounter_id': entity.get('encounter_id'),
        'diagnosed_date': _parse_date(entity.get('diagnosed_date') or entity.get('onsetDateTime')),
        'resolved_date': _parse_date(entity.get('resolved_date') or entity.get('abatementDateTime')),
        'created_at': datetime.utcnow(),
        'source_type': prov.get('source_type', 'generated'),
        'source_system': prov.get('source_system', 'patientsim'),
        'skill_used': prov.get('skill_used'),
        'generation_seed': prov.get('seed') or prov.get('generation_seed'),
    }


# ============================================================================
# Member Serialization (MemberSim)
# ============================================================================

# X12 270/271 Subscriber Relationship Codes (INS03)
RELATIONSHIP_CODE_MAP = {
    'self': '18',
    'subscriber': '18',
    'spouse': '01',
    'child': '19',
    'dependent': '19',  # Generic dependent → child
    'parent': '32',
    'grandparent': '04',
    'grandchild': '05',
    'nephew_niece': '07',
    'foster_child': '10',
    'ward': '15',
    'stepchild': '17',
    'employee': '20',
    'other': '21',
    'life_partner': '53',
    'domestic_partner': '53',
}


def _resolve_relationship_code(entity: Dict[str, Any]) -> str:
    """
    Resolve relationship code from various input formats.
    
    Accepts:
    - relationship_code: Direct X12 code ("18", "01", "19")
    - relationship: Friendly text ("SELF", "spouse", "Child")
    
    Returns X12 relationship code, defaulting to "18" (Self).
    """
    # Try direct code first
    code = entity.get('relationship_code')
    if code:
        return str(code)
    
    # Try friendly text and map to code
    relationship = entity.get('relationship')
    if relationship:
        # Normalize: lowercase, strip whitespace, replace spaces/underscores
        normalized = relationship.lower().strip().replace(' ', '_').replace('-', '_')
        if normalized in RELATIONSHIP_CODE_MAP:
            return RELATIONSHIP_CODE_MAP[normalized]
        # If it looks like a code already (numeric), use it
        if relationship.isdigit():
            return relationship
    
    # Default to Self
    return '18'


def serialize_member(entity: Dict[str, Any], provenance: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Prepare a member entity for database insertion.
    
    Handles multiple input formats:
    - Flat simple: {first_name, last_name, address_line1, enrollment_start_date, plan_id...}
    - Standard: {given_name, family_name, street_address, coverage_start, group_id...}
    - Nested FHIR-like: {name: {given: ...}, address: {line1: ...}}
    
    Relationship codes can be provided as:
    - relationship_code: X12 code ("18", "01", "19")
    - relationship: Friendly text ("self", "spouse", "child")
    """
    prov = provenance or entity.get('_provenance', {})
    
    # Primary key: use 'id' if present, otherwise generate from member_id or uuid
    member_id = entity.get('member_id') or entity.get('id') or str(uuid4())
    
    # Handle various name formats
    given_name = (
        entity.get('given_name') or 
        entity.get('first_name') or  # Flat format
        _get_nested(entity, 'name', 'given')
    )
    family_name = (
        entity.get('family_name') or 
        entity.get('last_name') or  # Flat format
        _get_nested(entity, 'name', 'family')
    )
    
    # Handle various address formats
    street_address = (
        entity.get('street_address') or
        entity.get('address_line1') or  # Flat format
        _get_nested(entity, 'address', 'line1') or 
        _get_nested(entity, 'address', 'line', 0)
    )
    city = (
        entity.get('city') or
        _get_nested(entity, 'address', 'city')
    )
    state = (
        entity.get('state') or
        _get_nested(entity, 'address', 'state')
    )
    postal_code = (
        entity.get('postal_code') or
        entity.get('zip_code') or
        entity.get('zip') or
        _get_nested(entity, 'address', 'postalCode') or 
        _get_nested(entity, 'address', 'postal_code')
    )
    
    # Handle phone (top-level or nested)
    phone = (
        entity.get('phone') or
        _get_nested(entity, 'telecom', 'phone')
    )
    
    # Handle coverage dates (map from various formats)
    coverage_start = _parse_date(
        entity.get('coverage_start') or 
        entity.get('enrollment_start_date') or  # Flat format
        entity.get('effective_date') or
        entity.get('start_date')
    )
    coverage_end = _parse_date(
        entity.get('coverage_end') or
        entity.get('enrollment_end_date') or  # Flat format
        entity.get('termination_date') or
        entity.get('end_date')
    )
    
    # Handle plan identifiers (map from various formats)
    group_id = (
        entity.get('group_id') or 
        entity.get('group_number') or
        entity.get('contract_id') or  # Medicare contract
        entity.get('employer_name')  # Fallback to employer
    )
    plan_code = (
        entity.get('plan_code') or
        entity.get('plan_id') or
        entity.get('pbp_id')  # Medicare plan benefit package
    )
    
    return {
        'id': entity.get('id') or member_id,  # PK matches table schema
        'member_id': member_id,
        'subscriber_id': entity.get('subscriber_id') or entity.get('patient_id'),  # Link to patient
        'relationship_code': _resolve_relationship_code(entity),
        'ssn': entity.get('ssn'),
        'given_name': given_name,
        'middle_name': entity.get('middle_name') or _get_nested(entity, 'name', 'middle'),
        'family_name': family_name,
        'birth_date': _parse_date(entity.get('birth_date') or entity.get('date_of_birth') or entity.get('birthDate')),
        'gender': entity.get('gender') or entity.get('sex'),
        'street_address': street_address,
        'city': city,
        'state': state,
        'postal_code': postal_code,
        'phone': phone,
        'email': entity.get('email') or _get_nested(entity, 'telecom', 'email'),
        'group_id': group_id,
        'plan_code': plan_code,
        'coverage_start': coverage_start,
        'coverage_end': coverage_end,
        'pcp_npi': entity.get('pcp_npi'),
        'created_at': datetime.utcnow(),
        'source_type': prov.get('source_type', 'generated'),
        'source_system': prov.get('source_system', 'membersim'),
        'skill_used': prov.get('skill_used'),
        'generation_seed': prov.get('seed') or prov.get('generation_seed'),
    }


# ============================================================================
# Claim Serialization (MemberSim)
# ============================================================================

def serialize_claim(entity: Dict[str, Any], provenance: Optional[Dict] = None) -> Dict[str, Any]:
    """Prepare a claim entity for database insertion."""
    prov = provenance or entity.get('_provenance', {})
    
    return {
        'claim_id': entity.get('claim_id') or entity.get('id') or str(uuid4()),
        'member_id': entity.get('member_id'),
        'claim_type': entity.get('claim_type', 'professional'),
        'service_date': _parse_date(entity.get('service_date')),
        'admission_date': _parse_date(entity.get('admission_date')),
        'discharge_date': _parse_date(entity.get('discharge_date')),
        'provider_npi': entity.get('provider_npi'),
        'facility_npi': entity.get('facility_npi'),
        'total_charge': entity.get('total_charge'),
        'total_paid': entity.get('total_paid'),
        'patient_responsibility': entity.get('patient_responsibility'),
        'status': entity.get('status', 'paid'),
        'created_at': datetime.utcnow(),
        'source_type': prov.get('source_type', 'generated'),
        'source_system': prov.get('source_system', 'membersim'),
        'skill_used': prov.get('skill_used'),
        'generation_seed': prov.get('seed') or prov.get('generation_seed'),
    }


# ============================================================================
# Prescription Serialization (RxMemberSim)
# ============================================================================

def serialize_prescription(entity: Dict[str, Any], provenance: Optional[Dict] = None) -> Dict[str, Any]:
    """Prepare a prescription entity for database insertion."""
    prov = provenance or entity.get('_provenance', {})
    
    return {
        'prescription_id': entity.get('prescription_id') or entity.get('id') or str(uuid4()),
        'rx_member_id': entity.get('rx_member_id') or entity.get('member_id'),
        'drug_ndc': entity.get('drug_ndc') or entity.get('ndc'),
        'drug_name': entity.get('drug_name'),
        'quantity': entity.get('quantity'),
        'days_supply': entity.get('days_supply'),
        'refills_authorized': entity.get('refills_authorized'),
        'refills_remaining': entity.get('refills_remaining'),
        'prescriber_npi': entity.get('prescriber_npi'),
        'written_date': _parse_date(entity.get('written_date')),
        'expiration_date': _parse_date(entity.get('expiration_date')),
        'status': entity.get('status', 'active'),
        'created_at': datetime.utcnow(),
        'source_type': prov.get('source_type', 'generated'),
        'source_system': prov.get('source_system', 'rxmembersim'),
        'skill_used': prov.get('skill_used'),
        'generation_seed': prov.get('seed') or prov.get('generation_seed'),
    }


# ============================================================================
# Subject Serialization (TrialSim)
# ============================================================================

def serialize_subject(entity: Dict[str, Any], provenance: Optional[Dict] = None) -> Dict[str, Any]:
    """Prepare a trial subject entity for database insertion."""
    prov = provenance or entity.get('_provenance', {})
    
    return {
        'subject_id': entity.get('subject_id') or entity.get('id') or str(uuid4()),
        'study_id': entity.get('study_id'),
        'site_id': entity.get('site_id'),
        'ssn': entity.get('ssn'),
        'screening_id': entity.get('screening_id'),
        'randomization_id': entity.get('randomization_id'),
        'arm': entity.get('arm'),
        'cohort': entity.get('cohort'),
        'consent_date': _parse_date(entity.get('consent_date')),
        'randomization_date': _parse_date(entity.get('randomization_date')),
        'status': entity.get('status', 'screening'),
        'created_at': datetime.utcnow(),
        'source_type': prov.get('source_type', 'generated'),
        'source_system': prov.get('source_system', 'trialsim'),
        'skill_used': prov.get('skill_used'),
        'generation_seed': prov.get('seed') or prov.get('generation_seed'),
    }


# ============================================================================
# Serializer Registry
# ============================================================================

SERIALIZERS = {
    'patient': serialize_patient,
    'patients': serialize_patient,
    'encounter': serialize_encounter,
    'encounters': serialize_encounter,
    'diagnosis': serialize_diagnosis,
    'diagnoses': serialize_diagnosis,
    'member': serialize_member,
    'members': serialize_member,
    'claim': serialize_claim,
    'claims': serialize_claim,
    'prescription': serialize_prescription,
    'prescriptions': serialize_prescription,
    'subject': serialize_subject,
    'subjects': serialize_subject,
    # pcp_assignments: stored in cohort_entities JSON only, no canonical table
}

DESERIALIZERS = {
    'patient': deserialize_patient,
    'patients': deserialize_patient,
    'encounter': deserialize_encounter,
    'encounters': deserialize_encounter,
}

# Mapping from entity type to table name and ID column (must match actual table PKs)
ENTITY_TABLE_MAP = {
    'patient': ('patients', 'id'),
    'patients': ('patients', 'id'),
    'encounter': ('encounters', 'encounter_id'),
    'encounters': ('encounters', 'encounter_id'),
    'diagnosis': ('diagnoses', 'id'),
    'diagnoses': ('diagnoses', 'id'),
    'medication': ('medications', 'id'),
    'medications': ('medications', 'id'),
    'lab_result': ('lab_results', 'id'),
    'lab_results': ('lab_results', 'id'),
    'vital_sign': ('vital_signs', 'id'),
    'vital_signs': ('vital_signs', 'id'),
    'member': ('members', 'id'),  # PK is 'id', not 'member_id'
    'members': ('members', 'id'),  # PK is 'id', not 'member_id'
    'claim': ('claims', 'claim_id'),
    'claims': ('claims', 'claim_id'),
    'claim_line': ('claim_lines', 'id'),
    'claim_lines': ('claim_lines', 'id'),
    'prescription': ('prescriptions', 'prescription_id'),
    'prescriptions': ('prescriptions', 'prescription_id'),
    'subject': ('subjects', 'subject_id'),
    'subjects': ('subjects', 'subject_id'),
    # pcp_assignments: no canonical table - stored in cohort_entities JSON only
}


def get_serializer(entity_type: str):
    """Get serializer function for entity type."""
    return SERIALIZERS.get(entity_type)


def get_deserializer(entity_type: str):
    """Get deserializer function for entity type."""
    return DESERIALIZERS.get(entity_type)


def get_table_info(entity_type: str) -> Tuple[str, str]:
    """Get table name and ID column for entity type."""
    return ENTITY_TABLE_MAP.get(entity_type, (f'{entity_type}s', 'id'))
