"""Tests for entity serialization functions."""

import pytest
from datetime import date, datetime
from uuid import uuid4

from healthsim.state.serializers import (
    serialize_patient,
    deserialize_patient,
    serialize_encounter,
    deserialize_encounter,
    serialize_member,
    serialize_claim,
    serialize_prescription,
    serialize_subject,
    get_serializer,
    get_table_info,
    ENTITY_TABLE_MAP,
)


class TestPatientSerialization:
    """Tests for patient serialization."""
    
    def test_serialize_basic_patient(self):
        """Can serialize a basic patient."""
        patient = {
            'patient_id': '123',
            'mrn': 'MRN001',
            'given_name': 'John',
            'family_name': 'Doe',
            'birth_date': '1980-01-15',
            'gender': 'male',
        }
        
        result = serialize_patient(patient)
        
        assert result['id'] == '123'
        assert result['mrn'] == 'MRN001'
        assert result['given_name'] == 'John'
        assert result['family_name'] == 'Doe'
        assert result['gender'] == 'male'
        assert result['birth_date'] == date(1980, 1, 15)
    
    def test_serialize_with_nested_name(self):
        """Can serialize patient with FHIR-style nested name."""
        patient = {
            'id': '456',
            'mrn': 'MRN002',
            'name': {
                'given': 'Jane',
                'family': 'Smith',
            },
            'birthDate': '1985-06-20',
            'gender': 'female',
        }
        
        result = serialize_patient(patient)
        
        assert result['given_name'] == 'Jane'
        assert result['family_name'] == 'Smith'
    
    def test_serialize_with_address(self):
        """Can serialize patient with address."""
        patient = {
            'given_name': 'Test',
            'family_name': 'User',
            'birth_date': '1990-01-01',
            'gender': 'male',
            'address': {
                'line1': '123 Main St',
                'line2': 'Apt 4',
                'city': 'Anytown',
                'state': 'CA',
                'postalCode': '90210',
            },
        }
        
        result = serialize_patient(patient)
        
        assert result['street_address'] == '123 Main St'
        assert result['street_address_2'] == 'Apt 4'
        assert result['city'] == 'Anytown'
        assert result['state'] == 'CA'
        assert result['postal_code'] == '90210'
    
    def test_serialize_with_provenance(self):
        """Can serialize patient with provenance."""
        patient = {
            'given_name': 'Test',
            'family_name': 'User',
            'birth_date': '1990-01-01',
            'gender': 'male',
        }
        provenance = {
            'source_type': 'generated',
            'source_system': 'patientsim',
            'skill_used': 'diabetes-management',
            'seed': 42,
        }
        
        result = serialize_patient(patient, provenance)
        
        assert result['source_type'] == 'generated'
        assert result['source_system'] == 'patientsim'
        assert result['skill_used'] == 'diabetes-management'
        assert result['generation_seed'] == 42
    
    def test_generates_uuid_if_missing(self):
        """Generates UUID if patient_id missing."""
        patient = {
            'given_name': 'Test',
            'family_name': 'User',
            'birth_date': '1990-01-01',
            'gender': 'male',
        }
        
        result = serialize_patient(patient)
        
        assert result['id'] is not None
        assert len(result['id']) == 36  # UUID format
    
    def test_deserialize_patient(self):
        """Can deserialize patient row back to dict."""
        columns = ['id', 'mrn', 'ssn', 'given_name', 'middle_name', 'family_name',
                   'suffix', 'prefix', 'birth_date', 'gender', 'race', 'ethnicity',
                   'language', 'street_address', 'street_address_2', 'city', 'state',
                   'postal_code', 'country', 'phone', 'phone_mobile', 'email',
                   'deceased', 'death_date', 'created_at', 'source_type', 
                   'source_system', 'skill_used', 'generation_seed']
        
        row = ('123', 'MRN001', None, 'John', None, 'Doe', None, None,
               date(1980, 1, 15), 'male', 'white', 'non-hispanic', 'en',
               '123 Main St', None, 'Anytown', 'CA', '90210', 'US',
               '555-1234', None, 'john@example.com', False, None,
               datetime.now(), 'generated', 'patientsim', None, None)
        
        result = deserialize_patient(row, columns)
        
        assert result['patient_id'] == '123'
        assert result['mrn'] == 'MRN001'
        assert result['name']['given'] == 'John'
        assert result['name']['family'] == 'Doe'
        assert result['gender'] == 'male'
        assert result['address']['city'] == 'Anytown'


class TestEncounterSerialization:
    """Tests for encounter serialization."""
    
    def test_serialize_encounter(self):
        """Can serialize an encounter."""
        encounter = {
            'encounter_id': 'enc-001',
            'patient_mrn': 'MRN001',
            'class_code': 'I',
            'status': 'in-progress',
            'admission_time': '2024-01-15T10:30:00',
            'facility': 'General Hospital',
            'department': 'Cardiology',
        }
        
        result = serialize_encounter(encounter)
        
        assert result['encounter_id'] == 'enc-001'
        assert result['patient_mrn'] == 'MRN001'
        assert result['class_code'] == 'I'
        assert result['status'] == 'in-progress'
        assert result['facility'] == 'General Hospital'
    
    def test_deserialize_encounter(self):
        """Can deserialize encounter row."""
        columns = ['encounter_id', 'patient_mrn', 'class_code', 'status',
                   'admission_time', 'discharge_time', 'facility', 'department',
                   'room', 'bed', 'chief_complaint', 'admitting_diagnosis',
                   'discharge_disposition', 'attending_physician', 'admitting_physician',
                   'created_at', 'source_type', 'source_system', 'skill_used', 'generation_seed']
        
        row = ('enc-001', 'MRN001', 'O', 'finished',
               datetime(2024, 1, 15, 10, 30), datetime(2024, 1, 15, 15, 0),
               'Clinic A', 'Primary Care', None, None, 'Annual checkup', None,
               None, 'Dr. Smith', None, datetime.now(), 'generated', 'patientsim', None, None)
        
        result = deserialize_encounter(row, columns)
        
        assert result['encounter_id'] == 'enc-001'
        assert result['patient_mrn'] == 'MRN001'
        assert result['class'] == 'O'
        assert result['facility'] == 'Clinic A'


class TestMemberSerialization:
    """Tests for member serialization (MemberSim)."""
    
    def test_serialize_member(self):
        """Can serialize a member."""
        member = {
            'member_id': 'mem-001',
            'given_name': 'John',
            'family_name': 'Doe',
            'birth_date': '1980-01-15',
            'gender': 'male',
            'subscriber_id': 'SUB001',
            'group_number': 'GRP100',
            'plan_code': 'GOLD',
            'coverage_start': '2024-01-01',
        }
        
        result = serialize_member(member)
        
        assert result['member_id'] == 'mem-001'
        assert result['given_name'] == 'John'
        assert result['subscriber_id'] == 'SUB001'
        assert result['coverage_start'] == date(2024, 1, 1)


class TestClaimSerialization:
    """Tests for claim serialization (MemberSim)."""
    
    def test_serialize_claim(self):
        """Can serialize a claim."""
        claim = {
            'claim_id': 'clm-001',
            'member_id': 'mem-001',
            'claim_type': 'professional',
            'service_date': '2024-06-15',
            'provider_npi': '1234567890',
            'total_charge': 250.00,
            'total_paid': 200.00,
            'status': 'paid',
        }
        
        result = serialize_claim(claim)
        
        assert result['claim_id'] == 'clm-001'
        assert result['member_id'] == 'mem-001'
        assert result['total_charge'] == 250.00
        assert result['service_date'] == date(2024, 6, 15)


class TestPrescriptionSerialization:
    """Tests for prescription serialization (RxMemberSim)."""
    
    def test_serialize_prescription(self):
        """Can serialize a prescription."""
        rx = {
            'prescription_id': 'rx-001',
            'rx_member_id': 'mem-001',
            'drug_ndc': '12345-6789-01',
            'drug_name': 'Metformin 500mg',
            'quantity': 60,
            'days_supply': 30,
            'prescriber_npi': '1234567890',
            'written_date': '2024-06-01',
        }
        
        result = serialize_prescription(rx)
        
        assert result['prescription_id'] == 'rx-001'
        assert result['drug_ndc'] == '12345-6789-01'
        assert result['quantity'] == 60
        assert result['written_date'] == date(2024, 6, 1)


class TestSubjectSerialization:
    """Tests for subject serialization (TrialSim)."""
    
    def test_serialize_subject(self):
        """Can serialize a trial subject."""
        subject = {
            'subject_id': 'subj-001',
            'study_id': 'STUDY-123',
            'site_id': 'SITE-001',
            'screening_id': 'SCR-001',
            'arm': 'treatment',
            'consent_date': '2024-06-01',
            'status': 'enrolled',
        }
        
        result = serialize_subject(subject)
        
        assert result['subject_id'] == 'subj-001'
        assert result['study_id'] == 'STUDY-123'
        assert result['arm'] == 'treatment'
        assert result['consent_date'] == date(2024, 6, 1)


class TestSerializerRegistry:
    """Tests for serializer registry functions."""
    
    def test_get_serializer_patient(self):
        """Can get patient serializer."""
        serializer = get_serializer('patient')
        assert serializer is serialize_patient
        
        # Also works with plural
        serializer = get_serializer('patients')
        assert serializer is serialize_patient
    
    def test_get_serializer_unknown(self):
        """Unknown entity type returns None."""
        serializer = get_serializer('unknown_type')
        assert serializer is None
    
    def test_get_table_info(self):
        """Can get table info for entity types."""
        table, id_col = get_table_info('patient')
        assert table == 'patients'
        assert id_col == 'id'
        
        table, id_col = get_table_info('encounter')
        assert table == 'encounters'
        assert id_col == 'encounter_id'
    
    def test_entity_table_map_coverage(self):
        """All expected entity types are in the map."""
        expected_types = [
            'patient', 'patients',
            'encounter', 'encounters',
            'diagnosis', 'diagnoses',
            'member', 'members',
            'claim', 'claims',
            'prescription', 'prescriptions',
            'subject', 'subjects',
        ]
        
        for entity_type in expected_types:
            assert entity_type in ENTITY_TABLE_MAP, f"Missing: {entity_type}"
