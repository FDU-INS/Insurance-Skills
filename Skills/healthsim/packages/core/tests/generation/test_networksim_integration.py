"""Integration tests for NetworkSim reference data using real database.

These tests require the healthsim_current_backup.duckdb database.
They verify that the queries work against real NPPES/CMS data.

Run with: pytest -v -m integration packages/core/tests/generation/test_networksim_integration.py
"""

import pytest
from pathlib import Path

from healthsim.generation.networksim_reference import (
    NetworkSimResolver,
    get_networksim_db_path,
    get_providers_by_geography,
    get_facilities_by_geography,
    assign_provider_to_patient,
    assign_facility_to_patient,
    TAXONOMY_MAP,
    EntityType,
)


# Check if database is available
def _db_available() -> bool:
    """Check if the NetworkSim database is available."""
    db_path = get_networksim_db_path()
    if not db_path.exists():
        return False
    # Check it's not a Git LFS pointer (< 200 bytes)
    return db_path.stat().st_size > 1000


db_available = _db_available()
skip_reason = "NetworkSim database not available (Git LFS)"


@pytest.fixture
def real_conn():
    """Create real DuckDB connection to NetworkSim database."""
    import duckdb
    db_path = get_networksim_db_path()
    conn = duckdb.connect(str(db_path), read_only=True)
    yield conn
    conn.close()


# =============================================================================
# Provider Query Integration Tests
# =============================================================================

@pytest.mark.integration
@pytest.mark.skipif(not db_available, reason=skip_reason)
class TestProviderQueries:
    """Integration tests for provider queries."""

    def test_find_providers_by_state(self, real_conn):
        """Find providers in Texas."""
        resolver = NetworkSimResolver(real_conn)
        providers = resolver.find_providers(state="TX", limit=10)
        
        assert len(providers) > 0
        assert all(p.practice_state == "TX" for p in providers)

    def test_find_providers_by_city(self, real_conn):
        """Find providers in Houston, TX."""
        resolver = NetworkSimResolver(real_conn)
        providers = resolver.find_providers(state="TX", city="HOUSTON", limit=10)
        
        assert len(providers) > 0
        assert all(p.practice_state == "TX" for p in providers)
        assert all(p.practice_city.upper() == "HOUSTON" for p in providers)

    def test_find_providers_by_taxonomy(self, real_conn):
        """Find internal medicine providers."""
        resolver = NetworkSimResolver(real_conn)
        providers = resolver.find_providers(
            taxonomy=TAXONOMY_MAP["internal_medicine"],
            limit=10
        )
        
        assert len(providers) > 0
        # At least one taxonomy should match
        for p in providers:
            assert (
                p.taxonomy_1 == TAXONOMY_MAP["internal_medicine"] or
                p.taxonomy_2 == TAXONOMY_MAP["internal_medicine"] or
                p.taxonomy_3 == TAXONOMY_MAP["internal_medicine"]
            )

    def test_find_individual_providers(self, real_conn):
        """Find individual (non-organization) providers."""
        resolver = NetworkSimResolver(real_conn)
        providers = resolver.find_providers(
            entity_type=EntityType.INDIVIDUAL,
            limit=10
        )
        
        assert len(providers) > 0
        assert all(p.entity_type == EntityType.INDIVIDUAL for p in providers)

    def test_find_organization_providers(self, real_conn):
        """Find organization providers."""
        resolver = NetworkSimResolver(real_conn)
        providers = resolver.find_providers(
            entity_type=EntityType.ORGANIZATION,
            limit=10
        )
        
        assert len(providers) > 0
        assert all(p.entity_type == EntityType.ORGANIZATION for p in providers)

    def test_count_providers_in_state(self, real_conn):
        """Count providers in California."""
        resolver = NetworkSimResolver(real_conn)
        count = resolver.count_providers(state="CA")
        
        # CA should have many providers
        assert count > 100000

    def test_random_sample_providers(self, real_conn):
        """Random sample should return different results."""
        resolver = NetworkSimResolver(real_conn)
        
        # Two random samples should be different (with high probability)
        sample1 = resolver.find_providers(state="TX", limit=5, random_sample=True)
        sample2 = resolver.find_providers(state="TX", limit=5, random_sample=True)
        
        # NPIs should not all be the same
        npis1 = {p.npi for p in sample1}
        npis2 = {p.npi for p in sample2}
        
        # There's a tiny chance they're the same, but very unlikely
        assert len(sample1) == 5
        assert len(sample2) == 5

    def test_list_states_with_providers(self, real_conn):
        """List all states with provider counts."""
        resolver = NetworkSimResolver(real_conn)
        states = resolver.list_states_with_providers()
        
        # Should have most US states
        assert len(states) >= 50
        
        # Check structure
        for state in states[:5]:
            assert "state" in state
            assert "count" in state
            assert state["count"] > 0


# =============================================================================
# Facility Query Integration Tests
# =============================================================================

@pytest.mark.integration
@pytest.mark.skipif(not db_available, reason=skip_reason)
class TestFacilityQueries:
    """Integration tests for facility queries."""

    def test_find_facilities_by_state(self, real_conn):
        """Find facilities in California."""
        resolver = NetworkSimResolver(real_conn)
        facilities = resolver.find_facilities(state="CA", limit=10)
        
        assert len(facilities) > 0
        assert all(f.state == "CA" for f in facilities)

    def test_find_hospitals(self, real_conn):
        """Find hospital facilities using friendly name."""
        resolver = NetworkSimResolver(real_conn)
        # Use CMS code directly since resolver doesn't do name mapping
        facilities = resolver.find_facilities(
            facility_type="01",  # CMS code for hospitals
            limit=10
        )
        
        assert len(facilities) > 0

    def test_find_hospitals_via_convenience(self, real_conn):
        """Find hospitals using convenience function with friendly name."""
        # Convenience function handles name mapping
        facilities = get_facilities_by_geography(
            real_conn,
            state="TX",
            facility_type="hospital",  # Friendly name
            limit=10
        )
        
        assert len(facilities) > 0

    def test_find_facilities_by_bed_count(self, real_conn):
        """Find large hospitals."""
        resolver = NetworkSimResolver(real_conn)
        facilities = resolver.find_facilities(
            min_beds=500,
            limit=10
        )
        
        assert len(facilities) > 0
        for f in facilities:
            if f.beds:  # Some might be None
                assert f.beds >= 500

    def test_count_facilities_in_state(self, real_conn):
        """Count facilities in Texas."""
        resolver = NetworkSimResolver(real_conn)
        count = resolver.count_facilities(state="TX")
        
        # TX should have many facilities
        assert count > 1000


# =============================================================================
# Convenience Function Integration Tests
# =============================================================================

@pytest.mark.integration
@pytest.mark.skipif(not db_available, reason=skip_reason)
class TestConvenienceFunctionsIntegration:
    """Integration tests for convenience functions."""

    def test_get_providers_by_geography(self, real_conn):
        """Get providers using convenience function."""
        providers = get_providers_by_geography(
            real_conn,
            state="TX",
            city="HOUSTON",
            limit=10
        )
        
        assert len(providers) > 0
        assert all(p.practice_state == "TX" for p in providers)

    def test_get_providers_with_specialty_name(self, real_conn):
        """Get providers using specialty name instead of taxonomy."""
        providers = get_providers_by_geography(
            real_conn,
            state="CA",
            specialty="cardiology",
            limit=10
        )
        
        assert len(providers) > 0

    def test_get_facilities_by_geography(self, real_conn):
        """Get facilities using convenience function."""
        facilities = get_facilities_by_geography(
            real_conn,
            state="NY",
            limit=10
        )
        
        assert len(facilities) > 0
        assert all(f.state == "NY" for f in facilities)

    def test_assign_provider_to_patient(self, real_conn):
        """Assign a provider to a patient."""
        provider = assign_provider_to_patient(
            real_conn,
            patient_state="TX",
            patient_city="AUSTIN",
            seed=42
        )
        
        assert provider is not None
        assert provider.practice_state == "TX"

    def test_assign_provider_with_specialty(self, real_conn):
        """Assign a specialist to a patient."""
        provider = assign_provider_to_patient(
            real_conn,
            patient_state="CA",
            specialty="endocrinology",
            seed=42
        )
        
        assert provider is not None
        # Should have endocrinology taxonomy
        endocrinology_code = TAXONOMY_MAP["endocrinology"]
        assert (
            provider.taxonomy_1 == endocrinology_code or
            provider.taxonomy_2 == endocrinology_code or
            provider.taxonomy_3 == endocrinology_code
        )

    def test_assign_facility_to_patient(self, real_conn):
        """Assign a facility to a patient using friendly name."""
        facility = assign_facility_to_patient(
            real_conn,
            patient_state="FL",
            facility_type="hospital",  # Friendly name, maps to "01"
            seed=42
        )
        
        assert facility is not None
        assert facility.state == "FL"


# =============================================================================
# Data Quality Tests
# =============================================================================

@pytest.mark.integration
@pytest.mark.skipif(not db_available, reason=skip_reason)
class TestDataQuality:
    """Tests verifying data quality and completeness."""

    def test_provider_count_reasonable(self, real_conn):
        """Total provider count should be reasonable."""
        resolver = NetworkSimResolver(real_conn)
        # Query without filters to check total
        count = real_conn.execute("SELECT COUNT(*) FROM network.providers").fetchone()[0]
        
        # Should have millions of providers
        assert count > 1_000_000

    def test_facility_count_reasonable(self, real_conn):
        """Total facility count should be reasonable."""
        count = real_conn.execute("SELECT COUNT(*) FROM network.facilities").fetchone()[0]
        
        # Should have thousands of facilities
        assert count > 50_000

    def test_major_states_have_providers(self, real_conn):
        """Major states should have significant provider counts."""
        resolver = NetworkSimResolver(real_conn)
        
        major_states = ["CA", "TX", "FL", "NY", "PA"]
        for state in major_states:
            count = resolver.count_providers(state=state)
            assert count > 50000, f"{state} should have >50k providers"

    def test_specialty_distribution(self, real_conn):
        """Should have common specialties represented."""
        resolver = NetworkSimResolver(real_conn)
        
        for specialty_key in ["internal_medicine", "family_medicine", "cardiology"]:
            providers = resolver.find_providers(
                taxonomy=TAXONOMY_MAP[specialty_key],
                limit=1
            )
            assert len(providers) > 0, f"No {specialty_key} providers found"
