"""Tests for reference profile resolver (PopulationSim integration)."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import date

from healthsim.generation.reference_profiles import (
    GeographyLevel,
    GeographyReference,
    DemographicProfile,
    ReferenceProfileResolver,
    resolve_geography,
    list_counties,
    list_states,
    merge_profile_with_reference,
    create_hybrid_profile,
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
def sample_places_data():
    """Sample PLACES county data."""
    return {
        "countyfips": "48201",
        "countyname": "Harris County",
        "stateabbr": "TX",
        "totalpopulation": 4700000,
        "diabetes_crudeprev": 12.5,
        "obesity_crudeprev": 34.2,
        "bphigh_crudeprev": 30.1,
        "casthma_crudeprev": 9.5,
        "chd_crudeprev": 5.8,
        "copd_crudeprev": 5.2,
        "cancer_crudeprev": 5.5,
        "depression_crudeprev": 18.3,
    }


@pytest.fixture
def sample_svi_data():
    """Sample SVI county data."""
    return {
        "stcnty": "48201",
        "county": "Harris",
        "st_abbr": "TX",
        "e_totpop": 4700000,
        "ep_age65": 11.2,
        "ep_age17": 25.3,
        "ep_minrty": 71.5,
        "ep_hisp": 43.2,
        "ep_asian": 7.8,
        "ep_pov150": 18.5,
        "ep_uninsur": 21.3,
    }


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
        pct_male=49.5,
        pct_female=50.5,
        pct_minority=71.5,
        pct_hispanic=43.2,
        pct_asian=7.8,
        pct_poverty=18.5,
        pct_uninsured=21.3,
        pct_diabetes=12.5,
        pct_obesity=34.2,
        pct_hypertension=30.1,
        pct_asthma=9.5,
        pct_heart_disease=5.8,
        pct_copd=5.2,
        pct_cancer=5.5,
        pct_depression=18.3,
    )


# =============================================================================
# Geography Reference Tests
# =============================================================================

class TestGeographyReference:
    """Tests for GeographyReference."""

    def test_county_reference(self):
        """Test creating a county reference."""
        ref = GeographyReference(
            level=GeographyLevel.COUNTY,
            code="48201",
            name="Harris County"
        )
        
        assert ref.level == GeographyLevel.COUNTY
        assert ref.code == "48201"
        assert ref.name == "Harris County"

    def test_state_reference(self):
        """Test creating a state reference."""
        ref = GeographyReference(
            level=GeographyLevel.STATE,
            code="TX",
            name="Texas"
        )
        
        assert ref.level == GeographyLevel.STATE
        assert ref.code == "TX"

    def test_reference_without_name(self):
        """Test reference without name."""
        ref = GeographyReference(
            level=GeographyLevel.COUNTY,
            code="12345"
        )
        
        assert ref.name is None


# =============================================================================
# Demographic Profile Tests
# =============================================================================

class TestDemographicProfile:
    """Tests for DemographicProfile."""

    def test_default_values(self):
        """Test default profile values."""
        profile = DemographicProfile(
            geography=GeographyReference(
                level=GeographyLevel.STATE,
                code="CA"
            )
        )
        
        assert profile.population == 0
        assert profile.pct_male == 49.0
        assert profile.pct_female == 51.0

    def test_profile_with_values(self, sample_demographic_profile):
        """Test profile with actual values."""
        profile = sample_demographic_profile
        
        assert profile.population == 4700000
        assert profile.pct_diabetes == 12.5
        assert profile.pct_minority == 71.5

    def test_age_distribution_sums(self, sample_demographic_profile):
        """Test that age distribution approximately sums to 100."""
        profile = sample_demographic_profile
        total = (
            profile.pct_age_under_17 + 
            profile.pct_age_18_64 + 
            profile.pct_age_65_plus
        )
        assert 99.0 <= total <= 101.0

    def test_raw_data_storage(self):
        """Test raw data can be stored."""
        profile = DemographicProfile(
            geography=GeographyReference(level=GeographyLevel.COUNTY, code="00000"),
            raw_places={"diabetes_crudeprev": 12.5},
            raw_svi={"ep_age65": 15.0}
        )
        
        assert profile.raw_places["diabetes_crudeprev"] == 12.5
        assert profile.raw_svi["ep_age65"] == 15.0


# =============================================================================
# Reference Profile Resolver Tests
# =============================================================================

class TestReferenceProfileResolver:
    """Tests for ReferenceProfileResolver."""

    def test_resolve_county(self, mock_conn, sample_places_data, sample_svi_data):
        """Test resolving a county to demographic profile."""
        # Setup mock
        def mock_execute(query, params=None):
            result = MagicMock()
            if "population.places_county" in query:
                cols = list(sample_places_data.keys())
                values = list(sample_places_data.values())
                mock_conn.description = [(c,) for c in cols]
                result.fetchone.return_value = values
            elif "population.svi_county" in query:
                cols = list(sample_svi_data.keys())
                values = list(sample_svi_data.values())
                mock_conn.description = [(c,) for c in cols]
                result.fetchone.return_value = values
            return result
        
        mock_conn.execute = mock_execute
        
        resolver = ReferenceProfileResolver(mock_conn)
        profile = resolver.resolve_county("48201")
        
        assert profile.geography.code == "48201"
        assert profile.geography.level == GeographyLevel.COUNTY
        assert profile.pct_diabetes == 12.5
        assert profile.pct_age_65_plus == 11.2

    def test_resolve_county_not_found(self, mock_conn):
        """Test error when county not found."""
        mock_conn.execute.return_value.fetchone.return_value = None
        
        resolver = ReferenceProfileResolver(mock_conn)
        
        with pytest.raises(ValueError, match="No data found"):
            resolver.resolve_county("99999")

    def test_resolve_county_normalizes_fips(self, mock_conn, sample_places_data, sample_svi_data):
        """Test that FIPS codes are normalized."""
        call_args = []
        
        def mock_execute(query, params=None):
            call_args.append(params)
            result = MagicMock()
            result.fetchone.return_value = None
            return result
        
        mock_conn.execute = mock_execute
        
        resolver = ReferenceProfileResolver(mock_conn)
        try:
            resolver.resolve_county(48201)  # int instead of string
        except ValueError:
            pass
        
        # Should have converted to string with zero padding
        assert "48201" in str(call_args)

    def test_to_profile_spec(self, mock_conn, sample_demographic_profile):
        """Test converting profile to spec format."""
        resolver = ReferenceProfileResolver(mock_conn)
        spec = resolver.to_profile_spec(sample_demographic_profile)
        
        assert "profile" in spec
        profile = spec["profile"]
        
        assert profile["source"] == "populationsim"
        assert "demographics" in profile
        assert "clinical" in profile
        
        # Check age bands
        age = profile["demographics"]["age"]
        assert age["type"] == "age_bands"
        assert "bands" in age

    def test_to_profile_spec_conditions(self, mock_conn, sample_demographic_profile):
        """Test that clinical conditions are included in spec."""
        resolver = ReferenceProfileResolver(mock_conn)
        spec = resolver.to_profile_spec(sample_demographic_profile)
        
        conditions = spec["profile"]["clinical"]["conditions"]
        
        # Check diabetes is included
        diabetes = next((c for c in conditions if c["code"] == "E11"), None)
        assert diabetes is not None
        assert diabetes["prevalence"] == pytest.approx(0.125, rel=0.01)


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestResolveGeography:
    """Tests for resolve_geography convenience function."""

    def test_resolve_county_spec(self, mock_conn, sample_places_data, sample_svi_data):
        """Test resolving county specification."""
        def mock_execute(query, params=None):
            result = MagicMock()
            if "population.places_county" in query:
                cols = list(sample_places_data.keys())
                values = list(sample_places_data.values())
                mock_conn.description = [(c,) for c in cols]
                result.fetchone.return_value = values
            elif "population.svi_county" in query:
                cols = list(sample_svi_data.keys())
                values = list(sample_svi_data.values())
                mock_conn.description = [(c,) for c in cols]
                result.fetchone.return_value = values
            return result
        
        mock_conn.execute = mock_execute
        
        spec = {"type": "county", "fips": "48201"}
        profile = resolve_geography(spec, mock_conn)
        
        assert profile.geography.level == GeographyLevel.COUNTY

    def test_resolve_state_spec(self, mock_conn):
        """Test resolving state specification."""
        result_mock = MagicMock()
        result_mock.fetchone.return_value = (
            "TX", 29000000, 12.0, 33.0, 29.0, 9.0, 5.5, 5.0, 5.5, 18.0
        )
        mock_conn.execute.return_value = result_mock
        
        spec = {"type": "state", "code": "TX"}
        profile = resolve_geography(spec, mock_conn)
        
        assert profile.geography.level == GeographyLevel.STATE

    def test_resolve_unsupported_type(self, mock_conn):
        """Test error for unsupported geography type."""
        spec = {"type": "tract", "code": "123456789"}
        
        with pytest.raises(ValueError, match="Unsupported geography type"):
            resolve_geography(spec, mock_conn)


class TestListCounties:
    """Tests for list_counties function."""

    def test_list_all_counties(self, mock_conn):
        """Test listing all counties."""
        mock_conn.execute.return_value.fetchall.return_value = [
            ("48201", "Harris County", "TX", 4700000),
            ("06037", "Los Angeles County", "CA", 10000000),
        ]
        
        counties = list_counties(mock_conn)
        
        assert len(counties) == 2
        assert counties[0]["fips"] == "48201"
        assert counties[0]["name"] == "Harris County"

    def test_list_counties_by_state(self, mock_conn):
        """Test filtering counties by state."""
        mock_conn.execute.return_value.fetchall.return_value = [
            ("48201", "Harris County", "TX", 4700000),
            ("48113", "Dallas County", "TX", 2600000),
        ]
        
        counties = list_counties(mock_conn, state_abbr="TX")
        
        assert len(counties) == 2
        assert all(c["state"] == "TX" for c in counties)


class TestListStates:
    """Tests for list_states function."""

    def test_list_states(self, mock_conn):
        """Test listing all states."""
        mock_conn.execute.return_value.fetchall.return_value = [
            ("CA", 39000000, 58),
            ("TX", 29000000, 254),
        ]
        
        states = list_states(mock_conn)
        
        assert len(states) == 2
        assert states[0]["abbr"] == "CA"
        assert states[1]["county_count"] == 254


# =============================================================================
# Profile Merging Tests
# =============================================================================

class TestMergeProfileWithReference:
    """Tests for merge_profile_with_reference function."""

    def test_merge_adds_missing_demographics(self, sample_demographic_profile):
        """Test that missing demographics are added from reference."""
        user_spec = {
            "profile": {
                "generation": {"count": 100}
            }
        }
        
        merged = merge_profile_with_reference(user_spec, sample_demographic_profile)
        
        assert "demographics" in merged["profile"]
        assert "age" in merged["profile"]["demographics"]
        assert "gender" in merged["profile"]["demographics"]

    def test_merge_preserves_user_age(self, sample_demographic_profile):
        """Test that user-specified age is preserved."""
        user_spec = {
            "profile": {
                "demographics": {
                    "age": {"type": "normal", "mean": 72, "std_dev": 5}
                }
            }
        }
        
        merged = merge_profile_with_reference(user_spec, sample_demographic_profile)
        
        # User's age spec should be preserved
        assert merged["profile"]["demographics"]["age"]["type"] == "normal"
        assert merged["profile"]["demographics"]["age"]["mean"] == 72

    def test_merge_adds_clinical_conditions(self, sample_demographic_profile):
        """Test that clinical conditions are added from reference."""
        user_spec = {
            "profile": {
                "generation": {"count": 50}
            }
        }
        
        merged = merge_profile_with_reference(user_spec, sample_demographic_profile)
        
        assert "clinical" in merged["profile"]
        assert "conditions" in merged["profile"]["clinical"]
        
        # Should have diabetes condition
        conditions = merged["profile"]["clinical"]["conditions"]
        has_diabetes = any(c["code"] == "E11" for c in conditions)
        assert has_diabetes

    def test_merge_preserves_user_clinical(self, sample_demographic_profile):
        """Test that user-specified clinical is preserved."""
        user_spec = {
            "profile": {
                "clinical": {
                    "primary_condition": {"code": "C34", "prevalence": 1.0}
                }
            }
        }
        
        merged = merge_profile_with_reference(user_spec, sample_demographic_profile)
        
        # User's clinical spec should be preserved
        assert "primary_condition" in merged["profile"]["clinical"]
        assert merged["profile"]["clinical"]["primary_condition"]["code"] == "C34"

    def test_merge_adds_reference_metadata(self, sample_demographic_profile):
        """Test that reference metadata is added."""
        user_spec = {"profile": {}}
        
        merged = merge_profile_with_reference(user_spec, sample_demographic_profile)
        
        assert "_reference" in merged["profile"]
        ref_meta = merged["profile"]["_reference"]
        assert ref_meta["geography"]["code"] == "48201"
        assert ref_meta["population"] == 4700000


class TestCreateHybridProfile:
    """Tests for create_hybrid_profile function."""

    def test_hybrid_with_populationsim_source(self, mock_conn, sample_places_data, sample_svi_data):
        """Test creating hybrid profile with PopulationSim source."""
        def mock_execute(query, params=None):
            result = MagicMock()
            if "population.places_county" in query:
                cols = list(sample_places_data.keys())
                values = list(sample_places_data.values())
                mock_conn.description = [(c,) for c in cols]
                result.fetchone.return_value = values
            elif "population.svi_county" in query:
                cols = list(sample_svi_data.keys())
                values = list(sample_svi_data.values())
                mock_conn.description = [(c,) for c in cols]
                result.fetchone.return_value = values
            return result
        
        mock_conn.execute = mock_execute
        
        user_spec = {
            "profile": {
                "id": "test-hybrid",
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"}
                }
            }
        }
        
        hybrid = create_hybrid_profile(user_spec, mock_conn)
        
        # Should have merged reference data
        assert "_reference" in hybrid["profile"]

    def test_hybrid_without_reference(self, mock_conn):
        """Test that specs without reference are returned as-is."""
        user_spec = {
            "profile": {
                "id": "test-no-ref",
                "demographics": {
                    "age": {"type": "uniform", "min": 18, "max": 65}
                }
            }
        }
        
        result = create_hybrid_profile(user_spec, mock_conn)
        
        # Should be unchanged
        assert result == user_spec

    def test_hybrid_with_overrides(self, mock_conn, sample_places_data, sample_svi_data):
        """Test hybrid profile respects user overrides."""
        def mock_execute(query, params=None):
            result = MagicMock()
            if "population.places_county" in query:
                cols = list(sample_places_data.keys())
                values = list(sample_places_data.values())
                mock_conn.description = [(c,) for c in cols]
                result.fetchone.return_value = values
            elif "population.svi_county" in query:
                cols = list(sample_svi_data.keys())
                values = list(sample_svi_data.values())
                mock_conn.description = [(c,) for c in cols]
                result.fetchone.return_value = values
            return result
        
        mock_conn.execute = mock_execute
        
        user_spec = {
            "profile": {
                "id": "elderly-diabetic",
                "demographics": {
                    "source": "populationsim",
                    "reference": {"type": "county", "fips": "48201"},
                    "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65}
                },
                "clinical": {
                    "primary_condition": {"code": "E11", "prevalence": 1.0}
                }
            }
        }
        
        hybrid = create_hybrid_profile(user_spec, mock_conn)
        
        # User's age override should be preserved
        assert hybrid["profile"]["demographics"]["age"]["mean"] == 72
        
        # User's clinical override should be preserved
        assert hybrid["profile"]["clinical"]["primary_condition"]["code"] == "E11"
