"""Integration tests for PopulationSim + NetworkSim reference data.

These tests use REAL data from the canonical DuckDB database:
- healthsim.duckdb: Contains all reference data in separate schemas
  - population schema: CDC PLACES, SVI
  - network schema: NPPES providers, facilities

Note: healthsim.duckdb is tracked in Git LFS (~1.7GB).

Run with: pytest tests/generation/test_reference_integration.py -v
"""

import pytest
from pathlib import Path

# Check if database is available
# Path: tests/generation/test_reference_integration.py
#       -> tests/generation -> tests -> core -> packages -> healthsim-workspace
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
HEALTHSIM_DB = WORKSPACE_ROOT / "healthsim.duckdb"

# Skip all tests if database not available or is LFS pointer
def _check_db_available():
    if not HEALTHSIM_DB.exists():
        return False
    # Check if it's a real DB or LFS pointer (pointer is ~130 bytes)
    if HEALTHSIM_DB.stat().st_size < 1000:
        return False
    return True

db_available = _check_db_available()
skip_reason = "DuckDB database not available (may be Git LFS pointer only)"


@pytest.fixture
def healthsim_conn():
    """Connection to canonical HealthSim database."""
    import duckdb
    conn = duckdb.connect(str(HEALTHSIM_DB), read_only=True)
    yield conn
    conn.close()


# Backwards-compatible fixtures that use the same DB
@pytest.fixture
def populationsim_conn(healthsim_conn):
    """Connection for PopulationSim tests (same DB, population schema)."""
    return healthsim_conn


@pytest.fixture
def networksim_conn(healthsim_conn):
    """Connection for NetworkSim tests (same DB, network schema)."""
    return healthsim_conn


# =============================================================================
# PopulationSim Integration Tests
# =============================================================================

@pytest.mark.skipif(not db_available, reason=skip_reason)
class TestPopulationSimIntegration:
    """Tests using real PopulationSim data."""

    def test_resolve_harris_county(self, populationsim_conn):
        """Resolve Harris County, TX demographics."""
        from healthsim.generation.reference_profiles import ReferenceProfileResolver
        
        resolver = ReferenceProfileResolver(populationsim_conn)
        profile = resolver.resolve_county("48201")  # Harris County, TX
        
        assert profile.geography.code == "48201"
        assert profile.population > 4000000  # Harris is ~4.7M
        assert 10 < profile.pct_diabetes < 20  # Reasonable diabetes rate
        assert 20 < profile.pct_obesity < 50  # Reasonable obesity rate
        assert profile.pct_age_65_plus > 0

    def test_resolve_texas_state(self, populationsim_conn):
        """Resolve Texas state demographics."""
        from healthsim.generation.reference_profiles import ReferenceProfileResolver
        
        resolver = ReferenceProfileResolver(populationsim_conn)
        profile = resolver.resolve_state("TX")
        
        assert profile.geography.code == "TX"
        assert profile.population > 25000000  # Texas is ~30M
        assert profile.pct_diabetes > 0
        assert profile.pct_hypertension > 0

    def test_list_texas_counties(self, populationsim_conn):
        """List counties in Texas."""
        from healthsim.generation.reference_profiles import list_counties
        
        counties = list_counties(populationsim_conn, state_abbr="TX")
        
        assert len(counties) > 200  # Texas has 254 counties
        
        # Find Harris County
        harris = next((c for c in counties if c["fips"] == "48201"), None)
        assert harris is not None
        assert harris["name"] == "Harris"  # Data has "Harris" not "Harris County"

    def test_to_profile_spec(self, populationsim_conn):
        """Convert demographic profile to profile spec."""
        from healthsim.generation.reference_profiles import ReferenceProfileResolver
        
        resolver = ReferenceProfileResolver(populationsim_conn)
        profile = resolver.resolve_county("48201")
        spec = resolver.to_profile_spec(profile)
        
        assert "profile" in spec
        assert "demographics" in spec["profile"]
        assert "clinical" in spec["profile"]
        assert "age" in spec["profile"]["demographics"]
        assert "gender" in spec["profile"]["demographics"]


# =============================================================================
# NetworkSim Integration Tests
# =============================================================================

@pytest.mark.skipif(not db_available, reason=skip_reason)
class TestNetworkSimIntegration:
    """Tests using real NetworkSim data."""

    def test_find_texas_providers(self, networksim_conn):
        """Find providers in Texas."""
        from healthsim.generation.networksim_reference import NetworkSimResolver
        
        resolver = NetworkSimResolver(networksim_conn)
        providers = resolver.find_providers(state="TX", limit=10)
        
        assert len(providers) == 10
        for p in providers:
            assert p.practice_state == "TX"

    def test_find_houston_cardiologists(self, networksim_conn):
        """Find cardiologists in Houston."""
        from healthsim.generation.networksim_reference import (
            NetworkSimResolver, TAXONOMY_MAP
        )
        
        resolver = NetworkSimResolver(networksim_conn)
        providers = resolver.find_providers(
            state="TX",
            city="HOUSTON",
            taxonomy=TAXONOMY_MAP["cardiology"],
            limit=20,
        )
        
        # Houston should have cardiologists
        assert len(providers) > 0
        for p in providers:
            assert p.practice_state == "TX"
            assert "HOUSTON" in (p.practice_city or "").upper()

    def test_find_texas_hospitals(self, networksim_conn):
        """Find hospitals in Texas."""
        from healthsim.generation.networksim_reference import NetworkSimResolver
        
        resolver = NetworkSimResolver(networksim_conn)
        facilities = resolver.find_facilities(
            state="TX",
            facility_type="hospital",
            limit=20,
        )
        
        assert len(facilities) > 0
        for f in facilities:
            assert f.state == "TX"
            assert f.facility_type == "01"  # CMS type code for hospital

    def test_find_large_hospitals(self, networksim_conn):
        """Find large hospitals (500+ beds)."""
        from healthsim.generation.networksim_reference import NetworkSimResolver
        
        resolver = NetworkSimResolver(networksim_conn)
        facilities = resolver.find_facilities(
            min_beds=500,
            limit=20,
        )
        
        assert len(facilities) > 0
        for f in facilities:
            assert f.beds is not None
            assert f.beds >= 500

    def test_count_texas_providers(self, networksim_conn):
        """Count providers in Texas."""
        from healthsim.generation.networksim_reference import NetworkSimResolver
        
        resolver = NetworkSimResolver(networksim_conn)
        count = resolver.count_providers(state="TX")
        
        # Texas should have hundreds of thousands of providers
        assert count > 100000

    def test_provider_by_npi(self, networksim_conn):
        """Look up specific provider by NPI."""
        from healthsim.generation.networksim_reference import NetworkSimResolver
        
        resolver = NetworkSimResolver(networksim_conn)
        
        # First find any provider
        providers = resolver.find_providers(state="TX", limit=1)
        assert len(providers) == 1
        
        npi = providers[0].npi
        
        # Now look up by NPI
        provider = resolver.get_provider_by_npi(npi)
        assert provider is not None
        assert provider.npi == npi

    def test_assign_provider_to_patient(self, networksim_conn):
        """Assign provider to patient based on geography."""
        from healthsim.generation.networksim_reference import assign_provider_to_patient
        
        provider = assign_provider_to_patient(
            networksim_conn,
            patient_state="TX",
            patient_city="HOUSTON",
            specialty="internal_medicine",
            seed=42,
        )
        
        assert provider is not None
        assert provider.practice_state == "TX"

    def test_assign_facility_to_patient(self, networksim_conn):
        """Assign facility to patient based on geography."""
        from healthsim.generation.networksim_reference import assign_facility_to_patient
        
        facility = assign_facility_to_patient(
            networksim_conn,
            patient_state="TX",
            facility_type="hospital",
            seed=42,
        )
        
        assert facility is not None
        assert facility.state == "TX"


# =============================================================================
# Combined Integration Tests
# =============================================================================

@pytest.mark.skipif(not db_available, reason=skip_reason)
class TestCombinedIntegration:
    """Tests combining PopulationSim and NetworkSim data."""

    def test_demographics_to_provider_assignment(
        self, populationsim_conn, networksim_conn
    ):
        """
        End-to-end test:
        1. Get demographics from PopulationSim (Harris County)
        2. Assign provider from NetworkSim based on geography
        """
        from healthsim.generation.reference_profiles import ReferenceProfileResolver
        from healthsim.generation.networksim_reference import assign_provider_to_patient
        
        # Step 1: Get Harris County demographics
        resolver = ReferenceProfileResolver(populationsim_conn)
        demographics = resolver.resolve_county("48201")
        
        assert demographics.geography.code == "48201"
        assert demographics.population > 4000000
        
        # Step 2: Assign a provider in Texas (where Harris County is)
        provider = assign_provider_to_patient(
            networksim_conn,
            patient_state="TX",
            specialty="internal_medicine",
            seed=12345,
        )
        
        assert provider is not None
        assert provider.practice_state == "TX"

    def test_create_patient_with_provider_and_facility(
        self, populationsim_conn, networksim_conn
    ):
        """
        Simulate creating a patient with assigned provider and facility.
        """
        from healthsim.generation.reference_profiles import ReferenceProfileResolver
        from healthsim.generation.networksim_reference import (
            assign_provider_to_patient,
            assign_facility_to_patient,
        )
        
        # Get county demographics
        resolver = ReferenceProfileResolver(populationsim_conn)
        demographics = resolver.resolve_county("48201")
        
        # Simulate patient data based on demographics
        patient = {
            "id": "P001",
            "county_fips": demographics.geography.code,
            "state": "TX",
            "city": "HOUSTON",
            "demographics_source": {
                "pct_diabetes": demographics.pct_diabetes,
                "pct_hypertension": demographics.pct_hypertension,
            }
        }
        
        # Assign PCP
        pcp = assign_provider_to_patient(
            networksim_conn,
            patient_state=patient["state"],
            patient_city=patient["city"],
            specialty="internal_medicine",
            seed=100,
        )
        
        # Assign hospital
        hospital = assign_facility_to_patient(
            networksim_conn,
            patient_state=patient["state"],
            patient_city=patient["city"],
            facility_type="hospital",
            seed=100,
        )
        
        assert pcp is not None
        assert hospital is not None
        
        # Build complete patient record
        patient["pcp"] = {
            "npi": pcp.npi,
            "name": pcp.display_name,
            "city": pcp.practice_city,
            "state": pcp.practice_state,
        }
        patient["hospital"] = {
            "ccn": hospital.ccn,
            "name": hospital.name,
            "city": hospital.city,
            "state": hospital.state,
        }
        
        assert patient["pcp"]["npi"] is not None
        assert patient["hospital"]["ccn"] is not None

    def test_specialty_distribution_matches_population(
        self, populationsim_conn, networksim_conn
    ):
        """
        Verify we can match specialty needs based on condition prevalence.
        
        Harris County has ~12.5% diabetes prevalence.
        We should be able to find endocrinologists there.
        """
        from healthsim.generation.reference_profiles import ReferenceProfileResolver
        from healthsim.generation.networksim_reference import (
            NetworkSimResolver, TAXONOMY_MAP
        )
        
        # Get diabetes prevalence
        pop_resolver = ReferenceProfileResolver(populationsim_conn)
        demographics = pop_resolver.resolve_county("48201")
        
        assert demographics.pct_diabetes > 10  # Known high diabetes area
        
        # Find endocrinologists in the area
        net_resolver = NetworkSimResolver(networksim_conn)
        endocrinologists = net_resolver.find_providers(
            state="TX",
            taxonomy=TAXONOMY_MAP["endocrinology"],
            limit=50,
        )
        
        # Should have endocrinologists available
        assert len(endocrinologists) > 0


# =============================================================================
# Data Quality Tests
# =============================================================================

@pytest.mark.skipif(not db_available, reason=skip_reason)
class TestDataQuality:
    """Verify data quality in reference databases."""

    def test_populationsim_county_coverage(self, populationsim_conn):
        """All US counties should be present."""
        from healthsim.generation.reference_profiles import list_states
        
        states = list_states(populationsim_conn)
        
        # Should have all 50 states + DC
        state_abbrs = {s["abbr"] for s in states}
        assert "TX" in state_abbrs
        assert "CA" in state_abbrs
        assert "NY" in state_abbrs
        assert "FL" in state_abbrs
        assert len(state_abbrs) >= 50

    def test_networksim_provider_coverage(self, networksim_conn):
        """Verify provider coverage across states."""
        from healthsim.generation.networksim_reference import NetworkSimResolver
        
        resolver = NetworkSimResolver(networksim_conn)
        states = resolver.list_states_with_providers()
        
        # Should have providers in most states
        state_abbrs = {s["state"] for s in states if s["state"]}
        assert "TX" in state_abbrs
        assert "CA" in state_abbrs
        assert "NY" in state_abbrs
        assert len(state_abbrs) >= 45  # At least 45 states

    def test_provider_npi_format(self, networksim_conn):
        """NPI should be 10 digits."""
        from healthsim.generation.networksim_reference import NetworkSimResolver
        
        resolver = NetworkSimResolver(networksim_conn)
        providers = resolver.find_providers(limit=100)
        
        for p in providers:
            assert len(p.npi) == 10
            assert p.npi.isdigit()

    def test_facility_ccn_format(self, networksim_conn):
        """CCN should be 6 characters."""
        from healthsim.generation.networksim_reference import NetworkSimResolver
        
        resolver = NetworkSimResolver(networksim_conn)
        facilities = resolver.find_facilities(limit=100)
        
        for f in facilities:
            assert len(f.ccn) == 6
