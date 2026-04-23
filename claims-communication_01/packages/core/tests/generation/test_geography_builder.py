"""Tests for geography-aware profile builder."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import date

from healthsim.generation.geography_builder import (
    GeographyProfile,
    GeographyAwareProfileBuilder,
    create_geography_profile,
    build_cohort_with_geography,
    get_provider_for_entity,
    get_facility_for_entity,
)
from healthsim.generation.reference_profiles import (
    GeographyLevel,
    GeographyReference,
    DemographicProfile,
)
from healthsim.generation.networksim_reference import (
    Provider,
    Facility,
    EntityType,
    get_networksim_db_path,
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
def sample_demographic_profile():
    """Create a sample demographic profile."""
    return DemographicProfile(
        geography=GeographyReference(
            level=GeographyLevel.COUNTY,
            code="48201",
            name="Harris County"
        ),
        population=4700000,
        pct_age_under_17=25.3,
        pct_age_18_64=63.5,
        pct_age_65_plus=11.2,
        pct_diabetes=12.5,
        pct_obesity=34.2,
        pct_hypertension=30.1,
        raw_places={"stateabbr": "TX", "countyname": "Harris County"},
        raw_svi={"st_abbr": "TX"},
    )


@pytest.fixture
def sample_provider():
    """Create a sample provider."""
    return Provider(
        npi="1234567890",
        entity_type=EntityType.INDIVIDUAL,
        last_name="SMITH",
        first_name="JOHN",
        credential="MD",
        practice_state="TX",
        practice_city="HOUSTON",
        taxonomy_1="207R00000X",
    )


@pytest.fixture
def sample_facility():
    """Create a sample facility."""
    return Facility(
        ccn="450001",
        name="MEMORIAL HERMANN",
        facility_type="hospital",
        state="TX",
        city="HOUSTON",
        beds=500,
    )


@pytest.fixture
def sample_geography_profile(sample_demographic_profile, sample_provider, sample_facility):
    """Create a sample geography profile."""
    return GeographyProfile(
        geography=GeographyReference(
            level=GeographyLevel.COUNTY,
            code="48201",
            name="Harris County"
        ),
        demographics=sample_demographic_profile,
        primary_care_providers=[sample_provider],
        specialty_providers={"cardiology": [sample_provider]},
        hospitals=[sample_facility],
        provider_count=2,
        facility_count=1,
    )


# =============================================================================
# GeographyProfile Tests
# =============================================================================

class TestGeographyProfile:
    """Tests for GeographyProfile data class."""
    
    def test_basic_creation(self, sample_demographic_profile):
        """Test basic profile creation."""
        profile = GeographyProfile(
            geography=GeographyReference(
                level=GeographyLevel.COUNTY,
                code="48201",
                name="Harris County"
            ),
            demographics=sample_demographic_profile,
        )
        
        assert profile.geography.code == "48201"
        assert profile.demographics.population == 4700000
        assert profile.provider_count == 0
    
    def test_get_providers_for_specialty(self, sample_geography_profile):
        """Test getting providers for a specialty."""
        providers = sample_geography_profile.get_providers_for_specialty("cardiology")
        assert len(providers) == 1
        
        # Non-existent specialty
        providers = sample_geography_profile.get_providers_for_specialty("dermatology")
        assert len(providers) == 0
    
    def test_get_random_pcp(self, sample_geography_profile):
        """Test getting random PCP."""
        pcp = sample_geography_profile.get_random_pcp(seed=42)
        assert pcp is not None
        assert pcp.npi == "1234567890"
    
    def test_get_random_pcp_empty(self, sample_demographic_profile):
        """Test getting PCP when none available."""
        profile = GeographyProfile(
            geography=GeographyReference(
                level=GeographyLevel.COUNTY,
                code="48201",
            ),
            demographics=sample_demographic_profile,
        )
        
        pcp = profile.get_random_pcp()
        assert pcp is None
    
    def test_get_random_specialist(self, sample_geography_profile):
        """Test getting random specialist."""
        specialist = sample_geography_profile.get_random_specialist("cardiology", seed=42)
        assert specialist is not None
    
    def test_get_random_hospital(self, sample_geography_profile):
        """Test getting random hospital."""
        hospital = sample_geography_profile.get_random_hospital(seed=42)
        assert hospital is not None
        assert hospital.ccn == "450001"
    
    def test_to_profile_spec(self, sample_geography_profile):
        """Test converting to profile spec."""
        spec = sample_geography_profile.to_profile_spec()
        
        assert "profile" in spec
        assert spec["profile"]["id"] == "geo-48201"
        assert spec["profile"]["demographics"]["source"] == "populationsim"
        assert spec["profile"]["demographics"]["reference"]["code"] == "48201"
        assert "_geography_profile" in spec["profile"]


# =============================================================================
# GeographyAwareProfileBuilder Tests
# =============================================================================

class TestGeographyAwareProfileBuilder:
    """Tests for GeographyAwareProfileBuilder."""
    
    def test_initialization(self, mock_conn):
        """Test builder initialization."""
        builder = GeographyAwareProfileBuilder(mock_conn)
        assert builder.conn == mock_conn
    
    @patch("healthsim.generation.geography_builder.resolve_geography")
    @patch("healthsim.generation.geography_builder.NetworkSimResolver")
    def test_build_profile_county(
        self,
        mock_net_resolver_class,
        mock_resolve_geo,
        mock_conn,
        sample_demographic_profile,
        sample_provider,
        sample_facility,
    ):
        """Test building profile for a county."""
        # Setup mocks
        mock_resolve_geo.return_value = sample_demographic_profile
        
        mock_net_resolver = MagicMock()
        mock_net_resolver.find_providers.return_value = [sample_provider]
        mock_net_resolver.find_facilities.return_value = [sample_facility]
        mock_net_resolver_class.return_value = mock_net_resolver
        
        # Build profile
        builder = GeographyAwareProfileBuilder(mock_conn)
        profile = builder.build_profile(
            geography={"type": "county", "fips": "48201"}
        )
        
        assert profile.geography.code == "48201"
        assert profile.demographics.population == 4700000
        assert len(profile.primary_care_providers) > 0
    
    @patch("healthsim.generation.geography_builder.resolve_geography")
    def test_build_profile_without_providers(
        self,
        mock_resolve_geo,
        mock_conn,
        sample_demographic_profile,
    ):
        """Test building profile without providers."""
        mock_resolve_geo.return_value = sample_demographic_profile
        
        builder = GeographyAwareProfileBuilder(mock_conn)
        profile = builder.build_profile(
            geography={"type": "county", "fips": "48201"},
            include_providers=False,
            include_facilities=False,
        )
        
        assert profile.provider_count == 0
        assert profile.facility_count == 0
    
    @patch("healthsim.generation.geography_builder.resolve_geography")
    @patch("healthsim.generation.geography_builder.NetworkSimResolver")
    def test_build_profile_with_specialties(
        self,
        mock_net_resolver_class,
        mock_resolve_geo,
        mock_conn,
        sample_demographic_profile,
        sample_provider,
        sample_facility,
    ):
        """Test building profile with specific specialties."""
        mock_resolve_geo.return_value = sample_demographic_profile
        
        mock_net_resolver = MagicMock()
        mock_net_resolver.find_providers.return_value = [sample_provider]
        mock_net_resolver.find_facilities.return_value = [sample_facility]
        mock_net_resolver_class.return_value = mock_net_resolver
        
        builder = GeographyAwareProfileBuilder(mock_conn)
        profile = builder.build_profile(
            geography={"type": "county", "fips": "48201"},
            specialties=["cardiology", "endocrinology"],
        )
        
        # Should have called find_providers for PCPs + each specialty
        assert mock_net_resolver.find_providers.call_count >= 3


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    @patch("healthsim.generation.geography_builder.GeographyAwareProfileBuilder")
    def test_create_geography_profile(self, mock_builder_class, mock_conn):
        """Test create_geography_profile function."""
        mock_builder = MagicMock()
        mock_builder.build_profile.return_value = MagicMock()
        mock_builder_class.return_value = mock_builder
        
        profile = create_geography_profile(
            mock_conn,
            geography={"type": "county", "fips": "48201"},
        )
        
        mock_builder.build_profile.assert_called_once()
    
    def test_get_provider_for_entity(self, sample_geography_profile):
        """Test getting provider for an entity."""
        # PCP
        provider = get_provider_for_entity(
            sample_geography_profile,
            specialty=None,
            entity_seed=42,
        )
        assert provider is not None
        
        # Specialist
        provider = get_provider_for_entity(
            sample_geography_profile,
            specialty="cardiology",
            entity_seed=42,
        )
        assert provider is not None
    
    def test_get_facility_for_entity(self, sample_geography_profile):
        """Test getting facility for an entity."""
        facility = get_facility_for_entity(
            sample_geography_profile,
            facility_type="hospital",
            entity_seed=42,
        )
        assert facility is not None


# =============================================================================
# Integration Tests (require real database)
# =============================================================================

class TestIntegration:
    """Integration tests with real database."""
    
    @pytest.fixture
    def real_conn(self):
        """Get connection to real database if available."""
        import duckdb
        
        db_path = get_networksim_db_path()
        if not db_path.exists():
            pytest.skip(f"HealthSim database not found: {db_path}")
        
        conn = duckdb.connect(str(db_path), read_only=True)
        yield conn
        conn.close()
    
    def test_real_county_profile(self, real_conn):
        """Test building real county profile."""
        builder = GeographyAwareProfileBuilder(real_conn)
        profile = builder.build_profile(
            geography={"type": "county", "fips": "48201"},  # Harris County TX
            specialties=["cardiology"],
            max_providers_per_specialty=10,
        )
        
        # Should have demographics
        assert profile.demographics.population > 0
        assert profile.demographics.pct_diabetes > 0
        
        # Should have providers
        assert len(profile.primary_care_providers) > 0
        
        # Should have facilities
        assert len(profile.hospitals) > 0
    
    def test_real_state_profile(self, real_conn):
        """Test building state-level profile."""
        builder = GeographyAwareProfileBuilder(real_conn)
        profile = builder.build_profile(
            geography={"type": "state", "code": "TX"},
            max_providers_per_specialty=20,
        )
        
        assert profile.demographics.population > 0
    
    def test_real_cohort_builder(self, real_conn):
        """Test building cohort with geography."""
        spec = build_cohort_with_geography(
            real_conn,
            geography={"type": "county", "fips": "48201"},
            count=100,
            specialties=["endocrinology"],
            seed=42,
        )
        
        assert spec["profile"]["generation"]["count"] == 100
        assert spec["profile"]["generation"]["seed"] == 42
        assert "demographics" in spec["profile"]
    
    def test_reproducible_provider_assignment(self, real_conn):
        """Test that provider assignment is reproducible with seed."""
        builder = GeographyAwareProfileBuilder(real_conn)
        profile = builder.build_profile(
            geography={"type": "county", "fips": "48201"},
            max_providers_per_specialty=50,
        )
        
        # Same seed should give same provider
        pcp1 = profile.get_random_pcp(seed=42)
        pcp2 = profile.get_random_pcp(seed=42)
        
        assert pcp1.npi == pcp2.npi
        
        # Different seed may give different provider
        pcp3 = profile.get_random_pcp(seed=99)
        # Note: Could be same if pool is small, so we just verify it works
        assert pcp3 is not None
