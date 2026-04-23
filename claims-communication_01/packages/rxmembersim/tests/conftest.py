"""Pytest configuration and fixtures for RxMemberSim tests."""
from datetime import date
from decimal import Decimal

import pytest


@pytest.fixture
def sample_member_data():
    """Sample pharmacy member data."""
    return {
        "member_id": "RX123456789",
        "person_code": "01",
        "cardholder_id": "CH987654321",
        "group_number": "GRP001",
        "bin": "610014",
        "pcn": "RXTEST",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": date(1985, 6, 15),
        "gender": "M",
    }


@pytest.fixture
def sample_drug_data():
    """Sample drug/NDC data."""
    return {
        "ndc": "00071015523",
        "drug_name": "Lipitor",
        "generic_name": "Atorvastatin Calcium",
        "gpi": "39400010000320",
        "strength": "20 MG",
        "dosage_form": "TABLET",
        "route": "ORAL",
        "dea_schedule": None,
        "brand_generic": "B",
    }


@pytest.fixture
def sample_claim_data(sample_member_data, sample_drug_data):
    """Sample pharmacy claim data."""
    return {
        "claim_id": "CLM20241128001",
        "service_date": date(2024, 11, 28),
        "member": sample_member_data,
        "drug": sample_drug_data,
        "pharmacy_npi": "1234567890",
        "prescriber_npi": "0987654321",
        "quantity_dispensed": Decimal("30"),
        "days_supply": 30,
        "daw_code": "0",
        "fill_number": 1,
        "refills_authorized": 5,
    }
