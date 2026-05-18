"""Tests for NetworkSim reference data resolver.

Tests provider and facility lookup from NPPES and CMS data.
Uses real data from healthsim_networksim_standalone.duckdb via osascript.
"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from healthsim.generation.networksim_reference import (
    EntityType,
    FacilityType,
    Provider,
    Facility,
    ProviderSearchCriteria,
    FacilitySearchCriteria,
    TAXONOMY_MAP,
    NetworkSimResolver,
    get_networksim_db_path,
    get_providers_by_geography,
    get_facilities_by_geography,
    assign_provider_to_patient,
    assign_facility_to_patient,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_conn():
    """Create a mock DuckDB connection."""
    conn = MagicMock()
    return conn


@pytest.fixture
def sample_provider_row():
    """Sample provider row from database."""
    return (
        "1234567890",  # npi
        "1",           # entity_type_code
        "SMITH",       # last_name
        "JOHN",        # first_name
        "A",           # middle_name
        "MD",          # credential
        "M",           # gender
        None,          # organization_name
        "HOUSTON",     # practice_city
        "TX",          # practice_state
        "77001",       # practice_zip
        "123 Main St", # practice_address_1
        "Suite 100",   # practice_address_2
        "713-555-1234",# phone
        "207R00000X",  # taxonomy_1 (Internal Medicine)
        None,          # taxonomy_2
        None,          # taxonomy_3
    )


@pytest.fixture
def sample_org_provider_row():
    """Sample organization provider row."""
    return (
        "9876543210",
        "2",           # Organization
        None, None, None, None, None,
        "HOUSTON MEDICAL CENTER",
        "HOUSTON", "TX", "77002",
        "456 Hospital Blvd", None, "713-555-5678",
        "282N00000X",  # Hospital taxonomy
        None, None,
    )


@pytest.fixture
def sample_facility_row():
    """Sample facility row from database."""
    return (
        "450358",      # ccn
        "MEMORIAL HERMANN HOSPITAL",
        "hospital",    # type
        "HOUSTON",     # city
        "TX",          # state
        "77024",       # zip
        "713-555-9999",# phone
        500,           # beds
        "acute",       # subtype
    )


# =============================================================================
# Entity Type Tests
# =============================================================================

class TestEntityType:
    """Tests for EntityType enum."""

    def test_individual_value(self):
        """Individual entity type is '1'."""
        assert EntityType.INDIVIDUAL.value == "1"

    def test_organization_value(self):
        """Organization entity type is '2'."""
        assert EntityType.ORGANIZATION.value == "2"

    def test_from_string(self):
        """Can create from string value."""
        assert EntityType("1") == EntityType.INDIVIDUAL
        assert EntityType("2") == EntityType.ORGANIZATION


# =============================================================================
# Provider Tests
# =============================================================================

class TestProvider:
    """Tests for Provider dataclass."""

    def test_individual_provider(self, sample_provider_row):
        """Test creating individual provider."""
        provider = Provider(
            npi=sample_provider_row[0],
            entity_type=EntityType(sample_provider_row[1]),
            last_name=sample_provider_row[2],
            first_name=sample_provider_row[3],
            credential=sample_provider_row[5],
            practice_city=sample_provider_row[8],
            practice_state=sample_provider_row[9],
            taxonomy_1=sample_provider_row[14],
        )
        
        assert provider.npi == "1234567890"
        assert provider.entity_type == EntityType.INDIVIDUAL
        assert provider.last_name == "SMITH"
        assert provider.first_name == "JOHN"

    def test_display_name_individual(self):
        """Display name for individual provider."""
        provider = Provider(
            npi="1234567890",
            entity_type=EntityType.INDIVIDUAL,
            first_name="JOHN",
            last_name="SMITH",
            credential="MD",
        )
        
        assert provider.display_name == "JOHN SMITH , MD"

    def test_display_name_organization(self):
        """Display name for organization provider."""
        provider = Provider(
            npi="9876543210",
            entity_type=EntityType.ORGANIZATION,
            organization_name="HOUSTON MEDICAL CENTER",
        )
        
        assert provider.display_name == "HOUSTON MEDICAL CENTER"

    def test_display_name_unknown(self):
        """Display name when no name available."""
        provider = Provider(
            npi="0000000000",
            entity_type=EntityType.INDIVIDUAL,
        )
        
        assert provider.display_name == "Unknown Provider"

    def test_primary_taxonomy(self):
        """Primary taxonomy returns taxonomy_1."""
        provider = Provider(
            npi="1234567890",
            entity_type=EntityType.INDIVIDUAL,
            taxonomy_1="207R00000X",
            taxonomy_2="207RC0000X",
        )
        
        assert provider.primary_taxonomy == "207R00000X"


# =============================================================================
# Facility Tests
# =============================================================================

class TestFacility:
    """Tests for Facility dataclass."""

    def test_create_facility(self, sample_facility_row):
        """Test creating facility."""
        facility = Facility(
            ccn=sample_facility_row[0],
            name=sample_facility_row[1],
            facility_type=sample_facility_row[2],
            city=sample_facility_row[3],
            state=sample_facility_row[4],
            zip_code=sample_facility_row[5],
            beds=sample_facility_row[7],
        )
        
        assert facility.ccn == "450358"
        assert facility.name == "MEMORIAL HERMANN HOSPITAL"
        assert facility.facility_type == "hospital"
        assert facility.state == "TX"
        assert facility.beds == 500


# =============================================================================
# Taxonomy Map Tests
# =============================================================================

class TestTaxonomyMap:
    """Tests for TAXONOMY_MAP constant."""

    def test_common_specialties_present(self):
        """Common specialties are in the map."""
        assert "internal_medicine" in TAXONOMY_MAP
        assert "cardiology" in TAXONOMY_MAP
        assert "family_medicine" in TAXONOMY_MAP
        assert "pediatrics" in TAXONOMY_MAP

    def test_taxonomy_codes_format(self):
        """Taxonomy codes follow expected format."""
        for specialty, code in TAXONOMY_MAP.items():
            assert len(code) == 10, f"{specialty} code length wrong"
            assert code.endswith("X"), f"{specialty} code should end with X"

    def test_internal_medicine_code(self):
        """Internal medicine has correct code."""
        assert TAXONOMY_MAP["internal_medicine"] == "207R00000X"

    def test_cardiology_code(self):
        """Cardiology has correct code."""
        assert TAXONOMY_MAP["cardiology"] == "207RC0000X"


# =============================================================================
# NetworkSimResolver Tests (with mocks)
# =============================================================================

class TestNetworkSimResolver:
    """Tests for NetworkSimResolver class."""

    def test_find_providers_by_state(self, mock_conn, sample_provider_row):
        """Find providers by state."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(state="TX")
        
        assert len(providers) == 1
        assert providers[0].practice_state == "TX"
        
        # Verify query included state filter
        call_args = mock_conn.execute.call_args
        assert "practice_state = ?" in call_args[0][0]
        assert "TX" in call_args[0][1]

    def test_find_providers_by_city(self, mock_conn, sample_provider_row):
        """Find providers by city."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(state="TX", city="Houston")
        
        assert len(providers) == 1
        
        call_args = mock_conn.execute.call_args
        assert "UPPER(practice_city) = UPPER(?)" in call_args[0][0]

    def test_find_providers_by_taxonomy(self, mock_conn, sample_provider_row):
        """Find providers by specialty taxonomy."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(
            state="TX",
            taxonomy="207R00000X"
        )
        
        assert len(providers) == 1
        
        call_args = mock_conn.execute.call_args
        assert "taxonomy_1 = ?" in call_args[0][0]

    def test_find_providers_entity_type(self, mock_conn, sample_provider_row):
        """Find providers by entity type."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(
            state="TX",
            entity_type=EntityType.INDIVIDUAL
        )
        
        assert len(providers) == 1
        
        call_args = mock_conn.execute.call_args
        assert "entity_type_code = ?" in call_args[0][0]

    def test_find_providers_random_sample(self, mock_conn, sample_provider_row):
        """Random sample uses ORDER BY RANDOM()."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        resolver = NetworkSimResolver(mock_conn)
        providers = resolver.find_providers(state="TX", random_sample=True)
        
        call_args = mock_conn.execute.call_args
        assert "ORDER BY RANDOM()" in call_args[0][0]

    def test_find_facilities_by_state(self, mock_conn, sample_facility_row):
        """Find facilities by state."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        resolver = NetworkSimResolver(mock_conn)
        facilities = resolver.find_facilities(state="TX")
        
        assert len(facilities) == 1
        assert facilities[0].state == "TX"

    def test_find_facilities_by_type(self, mock_conn, sample_facility_row):
        """Find facilities by type."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        resolver = NetworkSimResolver(mock_conn)
        facilities = resolver.find_facilities(
            state="TX",
            facility_type="hospital"
        )
        
        assert len(facilities) == 1
        
        call_args = mock_conn.execute.call_args
        assert "type = ?" in call_args[0][0]

    def test_find_facilities_by_beds(self, mock_conn, sample_facility_row):
        """Find facilities by bed count range."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        resolver = NetworkSimResolver(mock_conn)
        facilities = resolver.find_facilities(
            state="TX",
            min_beds=100,
            max_beds=600
        )
        
        assert len(facilities) == 1
        
        call_args = mock_conn.execute.call_args
        assert "beds >= ?" in call_args[0][0]
        assert "beds <= ?" in call_args[0][0]

    def test_get_provider_by_npi(self, mock_conn, sample_provider_row):
        """Get specific provider by NPI."""
        mock_conn.execute.return_value.fetchone.return_value = sample_provider_row
        
        resolver = NetworkSimResolver(mock_conn)
        provider = resolver.get_provider_by_npi("1234567890")
        
        assert provider is not None
        assert provider.npi == "1234567890"

    def test_get_provider_by_npi_not_found(self, mock_conn):
        """Get provider by NPI returns None when not found."""
        mock_conn.execute.return_value.fetchone.return_value = None
        
        resolver = NetworkSimResolver(mock_conn)
        provider = resolver.get_provider_by_npi("0000000000")
        
        assert provider is None

    def test_get_facility_by_ccn(self, mock_conn, sample_facility_row):
        """Get specific facility by CCN."""
        mock_conn.execute.return_value.fetchone.return_value = sample_facility_row
        
        resolver = NetworkSimResolver(mock_conn)
        facility = resolver.get_facility_by_ccn("450358")
        
        assert facility is not None
        assert facility.ccn == "450358"

    def test_count_providers(self, mock_conn):
        """Count providers with filters."""
        mock_conn.execute.return_value.fetchone.return_value = (1500,)
        
        resolver = NetworkSimResolver(mock_conn)
        count = resolver.count_providers(state="TX")
        
        assert count == 1500

    def test_count_facilities(self, mock_conn):
        """Count facilities with filters."""
        mock_conn.execute.return_value.fetchone.return_value = (250,)
        
        resolver = NetworkSimResolver(mock_conn)
        count = resolver.count_facilities(state="TX", facility_type="hospital")
        
        assert count == 250

    def test_list_states_with_providers(self, mock_conn):
        """List states with provider counts."""
        mock_conn.execute.return_value.fetchall.return_value = [
            ("TX", 500000),
            ("CA", 600000),
            ("FL", 400000),
        ]
        
        resolver = NetworkSimResolver(mock_conn)
        states = resolver.list_states_with_providers()
        
        assert len(states) == 3
        assert states[0]["state"] == "TX"
        assert states[0]["count"] == 500000


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_get_providers_by_geography(self, mock_conn, sample_provider_row):
        """get_providers_by_geography wraps resolver."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        providers = get_providers_by_geography(
            mock_conn,
            state="TX",
            city="Houston",
            specialty="internal_medicine",
        )
        
        assert len(providers) == 1

    def test_get_providers_by_geography_with_taxonomy_code(self, mock_conn, sample_provider_row):
        """Accepts raw taxonomy code."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        providers = get_providers_by_geography(
            mock_conn,
            state="TX",
            specialty="207R00000X",
        )
        
        assert len(providers) == 1

    def test_get_facilities_by_geography(self, mock_conn, sample_facility_row):
        """get_facilities_by_geography wraps resolver."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        facilities = get_facilities_by_geography(
            mock_conn,
            state="TX",
            facility_type="hospital",
        )
        
        assert len(facilities) == 1

    def test_assign_provider_to_patient_city_match(self, mock_conn, sample_provider_row):
        """Assign provider tries city first."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_provider_row]
        
        provider = assign_provider_to_patient(
            mock_conn,
            patient_state="TX",
            patient_city="Houston",
            seed=42,
        )
        
        assert provider is not None
        assert provider.practice_state == "TX"

    def test_assign_provider_to_patient_state_fallback(self, mock_conn, sample_provider_row):
        """Falls back to state when city has no matches."""
        # First call (city) returns empty, second call (state) returns provider
        mock_conn.execute.return_value.fetchall.side_effect = [
            [],  # No city match
            [sample_provider_row],  # State match
        ]
        
        provider = assign_provider_to_patient(
            mock_conn,
            patient_state="TX",
            patient_city="SmallTown",
            seed=42,
        )
        
        assert provider is not None

    def test_assign_facility_to_patient(self, mock_conn, sample_facility_row):
        """Assign facility to patient."""
        mock_conn.execute.return_value.fetchall.return_value = [sample_facility_row]
        
        facility = assign_facility_to_patient(
            mock_conn,
            patient_state="TX",
            facility_type="hospital",
            seed=42,
        )
        
        assert facility is not None
        assert facility.state == "TX"


# =============================================================================
# Database Path Tests
# =============================================================================

class TestDatabasePath:
    """Tests for database path discovery."""

    def test_get_networksim_db_path_returns_path(self):
        """Returns a Path object."""
        path = get_networksim_db_path()
        assert isinstance(path, Path)

    def test_get_networksim_db_path_correct_name(self):
        """Path ends with correct database name (canonical healthsim.duckdb)."""
        path = get_networksim_db_path()
        assert path.name == "healthsim.duckdb"

    def test_get_networksim_db_path_in_workspace(self):
        """Path is in workspace root."""
        path = get_networksim_db_path()
        assert "healthsim-workspace" in str(path)
