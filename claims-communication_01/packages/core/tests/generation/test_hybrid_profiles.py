"""Tests for hybrid profile creation with PopulationSim and NetworkSim data.

Phase 4.4: Reference Data in Profiles
"""

import pytest
from pathlib import Path

# Check for canonical database
# Path: tests/generation/test_hybrid_profiles.py -> packages/core -> healthsim-workspace
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent.parent
DB_PATH = WORKSPACE_ROOT / "healthsim.duckdb"
db_available = DB_PATH.exists() and DB_PATH.stat().st_size > 1000000  # >1MB = real DB

if db_available:
    import duckdb


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def db_conn():
    """Provide read-only connection to canonical healthsim.duckdb."""
    if not db_available:
        pytest.skip("healthsim.duckdb not available")
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    yield conn
    conn.close()


# =============================================================================
# create_hybrid_profile() Tests
# =============================================================================

class TestCreateHybridProfile:
    """Tests for create_hybrid_profile()."""
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_hybrid_profile_with_county_reference(self, db_conn):
        """Test hybrid profile with county-level PopulationSim data."""
        from healthsim.generation.reference_profiles import create_hybrid_profile
        
        spec = {
            "profile": {
                "id": "harris-county-test",
                "generation": {"count": 50},
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"},  # Harris County TX
                },
                "clinical": {
                    "primary_condition": {"code": "E11", "prevalence": 1.0}
                }
            }
        }
        
        result = create_hybrid_profile(spec, db_conn)
        
        # Should have merged profile
        assert "profile" in result
        profile = result["profile"]
        
        # User values preserved
        assert profile["id"] == "harris-county-test"
        assert profile["generation"]["count"] == 50
        assert profile["clinical"]["primary_condition"]["code"] == "E11"
        
        # PopulationSim demographics resolved
        demographics = profile.get("demographics", {})
        assert "source" in demographics or "_reference_data" in profile
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_hybrid_profile_with_age_override(self, db_conn):
        """Test that user age override is preserved."""
        from healthsim.generation.reference_profiles import create_hybrid_profile
        
        spec = {
            "profile": {
                "id": "elderly-harris",
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"},
                    "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65}
                }
            }
        }
        
        result = create_hybrid_profile(spec, db_conn)
        profile = result["profile"]
        
        # User age override should be preserved
        assert "demographics" in profile
        age = profile["demographics"].get("age", {})
        if age:
            assert age.get("mean") == 72 or age.get("min") == 65
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_hybrid_profile_state_reference(self, db_conn):
        """Test hybrid profile with state-level reference."""
        from healthsim.generation.reference_profiles import create_hybrid_profile
        
        spec = {
            "profile": {
                "id": "texas-state",
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "state", "code": "TX"}
                }
            }
        }
        
        result = create_hybrid_profile(spec, db_conn)
        assert "profile" in result
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_hybrid_profile_no_reference_passthrough(self, db_conn):
        """Test that profiles without references pass through unchanged."""
        from healthsim.generation.reference_profiles import create_hybrid_profile
        
        spec = {
            "profile": {
                "id": "manual-profile",
                "demographics": {
                    "age": {"type": "uniform", "min": 30, "max": 50},
                    "gender": {"male": 0.5, "female": 0.5}
                }
            }
        }
        
        result = create_hybrid_profile(spec, db_conn)
        
        # Should pass through unchanged
        assert result["profile"]["id"] == "manual-profile"
        assert result["profile"]["demographics"]["age"]["min"] == 30


# =============================================================================
# create_hybrid_profile_with_network() Tests
# =============================================================================

class TestCreateHybridProfileWithNetwork:
    """Tests for create_hybrid_profile_with_network()."""
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_hybrid_with_providers(self, db_conn):
        """Test hybrid profile with NetworkSim provider resolution."""
        from healthsim.generation.reference_profiles import create_hybrid_profile_with_network
        
        spec = {
            "profile": {
                "id": "with-pcp",
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"}
                },
                "providers": {
                    "source": "networksim",
                    "reference": {"state": "TX", "specialty": "internal_medicine"},
                    "assignment": "pcp"
                }
            }
        }
        
        result = create_hybrid_profile_with_network(spec, db_conn)
        profile = result["profile"]
        
        # Should have resolved providers
        assert "_providers" in profile
        providers_info = profile["_providers"]
        assert providers_info["source"] == "networksim"
        assert providers_info["count"] > 0
        assert "pool" in providers_info
        assert len(providers_info["pool"]) > 0
        
        # Check provider data structure
        provider = providers_info["pool"][0]
        assert "npi" in provider
        assert "name" in provider
        assert "state" in provider
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_hybrid_with_facilities(self, db_conn):
        """Test hybrid profile with NetworkSim facility resolution."""
        from healthsim.generation.reference_profiles import create_hybrid_profile_with_network
        
        spec = {
            "profile": {
                "id": "with-hospital",
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"}
                },
                "facilities": {
                    "source": "networksim",
                    "reference": {"state": "TX", "type": "hospital"},
                    "assignment": "primary"
                }
            }
        }
        
        result = create_hybrid_profile_with_network(spec, db_conn)
        profile = result["profile"]
        
        # Should have resolved facilities
        assert "_facilities" in profile
        facilities_info = profile["_facilities"]
        assert facilities_info["source"] == "networksim"
        assert facilities_info["count"] > 0
        assert "pool" in facilities_info
        
        # Check facility data structure
        facility = facilities_info["pool"][0]
        assert "ccn" in facility
        assert "name" in facility
        assert "type" in facility
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_hybrid_with_providers_and_facilities(self, db_conn):
        """Test hybrid profile with both providers and facilities."""
        from healthsim.generation.reference_profiles import create_hybrid_profile_with_network
        
        spec = {
            "profile": {
                "id": "full-network",
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"}
                },
                "providers": {
                    "source": "networksim",
                    "reference": {"state": "TX", "specialty": "cardiology"},
                    "assignment": "specialist"
                },
                "facilities": {
                    "source": "networksim",
                    "reference": {"state": "TX", "type": "hospital", "min_beds": 200},
                    "assignment": "primary"
                }
            }
        }
        
        result = create_hybrid_profile_with_network(spec, db_conn)
        profile = result["profile"]
        
        # Both should be resolved
        assert "_providers" in profile
        assert "_facilities" in profile
        
        # Providers should be cardiologists
        providers = profile["_providers"]
        assert providers["reference"]["specialty"] == "cardiology"
        
        # Facilities should be larger hospitals
        facilities = profile["_facilities"]
        assert facilities["reference"]["min_beds"] == 200


# =============================================================================
# resolve_provider_reference() Tests
# =============================================================================

class TestResolveProviderReference:
    """Tests for provider reference resolution."""
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_resolve_providers_by_state(self, db_conn):
        """Test provider resolution by state."""
        from healthsim.generation.reference_profiles import resolve_provider_reference
        
        ref = {"state": "TX"}
        providers = resolve_provider_reference(ref, db_conn, limit=10)
        
        assert len(providers) == 10
        for p in providers:
            assert p["state"] == "TX"
            assert "npi" in p
            assert len(p["npi"]) == 10  # NPI is 10 digits
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_resolve_providers_by_specialty(self, db_conn):
        """Test provider resolution by specialty name."""
        from healthsim.generation.reference_profiles import resolve_provider_reference
        
        ref = {"state": "TX", "specialty": "internal_medicine"}
        providers = resolve_provider_reference(ref, db_conn, limit=20)
        
        assert len(providers) > 0
        # All should be in TX
        for p in providers:
            assert p["state"] == "TX"
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_resolve_providers_by_city(self, db_conn):
        """Test provider resolution by city."""
        from healthsim.generation.reference_profiles import resolve_provider_reference
        
        ref = {"state": "TX", "city": "HOUSTON"}
        providers = resolve_provider_reference(ref, db_conn, limit=10)
        
        assert len(providers) > 0
        for p in providers:
            assert p["state"] == "TX"
            # City might vary in case
            assert p["city"].upper() == "HOUSTON"


# =============================================================================
# resolve_facility_reference() Tests
# =============================================================================

class TestResolveFacilityReference:
    """Tests for facility reference resolution."""
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_resolve_facilities_by_state(self, db_conn):
        """Test facility resolution by state."""
        from healthsim.generation.reference_profiles import resolve_facility_reference
        
        ref = {"state": "TX"}
        facilities = resolve_facility_reference(ref, db_conn, limit=10)
        
        assert len(facilities) > 0
        for f in facilities:
            assert f["state"] == "TX"
            assert "ccn" in f
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_resolve_facilities_by_type(self, db_conn):
        """Test facility resolution by type."""
        from healthsim.generation.reference_profiles import resolve_facility_reference
        
        ref = {"state": "TX", "type": "hospital"}
        facilities = resolve_facility_reference(ref, db_conn, limit=10)
        
        assert len(facilities) > 0
        for f in facilities:
            assert f["state"] == "TX"
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_resolve_facilities_with_min_beds(self, db_conn):
        """Test facility resolution with minimum bed count."""
        from healthsim.generation.reference_profiles import resolve_facility_reference
        
        ref = {"state": "TX", "type": "hospital", "min_beds": 300}
        facilities = resolve_facility_reference(ref, db_conn, limit=10)
        
        assert len(facilities) > 0
        for f in facilities:
            # Beds might be None for some facilities
            if f["beds"] is not None:
                assert f["beds"] >= 300


# =============================================================================
# End-to-End Integration Tests
# =============================================================================

class TestHybridProfileIntegration:
    """End-to-end integration tests for hybrid profiles."""
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_complete_patient_profile_with_references(self, db_conn):
        """Test creating a complete patient profile with all references."""
        from healthsim.generation.reference_profiles import create_hybrid_profile_with_network
        
        # Comprehensive profile spec
        spec = {
            "profile": {
                "id": "comprehensive-diabetic",
                "generation": {"count": 100, "seed": 42},
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"},
                    "age": {"type": "normal", "mean": 65, "std_dev": 10, "min": 40}
                },
                "clinical": {
                    "primary_condition": {
                        "code": "E11",
                        "description": "Type 2 diabetes mellitus",
                        "prevalence": 1.0
                    },
                    "comorbidities": [
                        {"code": "I10", "prevalence": 0.7},
                        {"code": "E78", "prevalence": 0.5}
                    ]
                },
                "providers": {
                    "source": "networksim",
                    "reference": {"state": "TX", "specialty": "endocrinology"},
                    "assignment": "pcp"
                },
                "facilities": {
                    "source": "networksim",
                    "reference": {"state": "TX", "type": "hospital"},
                    "assignment": "primary"
                }
            }
        }
        
        result = create_hybrid_profile_with_network(spec, db_conn)
        profile = result["profile"]
        
        # Verify all components present
        assert profile["id"] == "comprehensive-diabetic"
        assert profile["generation"]["count"] == 100
        assert profile["clinical"]["primary_condition"]["code"] == "E11"
        
        # Verify reference data resolved
        assert "_providers" in profile
        assert profile["_providers"]["count"] > 0
        
        assert "_facilities" in profile
        assert profile["_facilities"]["count"] > 0
    
    @pytest.mark.skipif(not db_available, reason="Database not available")
    def test_profile_demographics_have_real_rates(self, db_conn):
        """Test that PopulationSim provides real health indicator rates."""
        from healthsim.generation.reference_profiles import (
            ReferenceProfileResolver,
            create_hybrid_profile
        )
        
        # First get raw demographics for Harris County
        resolver = ReferenceProfileResolver(db_conn)
        demo_profile = resolver.resolve_county("48201")
        
        # Harris County should have realistic diabetes rate (around 12-15%)
        assert demo_profile.pct_diabetes > 5
        assert demo_profile.pct_diabetes < 30
        
        # Should have realistic obesity rate
        assert demo_profile.pct_obesity > 20
        assert demo_profile.pct_obesity < 50
        
        # Population should be significant
        assert demo_profile.population > 1000000  # Harris is ~4.7M
