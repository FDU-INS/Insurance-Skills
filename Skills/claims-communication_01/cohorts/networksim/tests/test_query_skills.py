"""
NetworkSim Query Skills Tests
Tests for provider search, facility search, and related query functionality.
"""

import pytest
import duckdb
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent.parent.parent / "healthsim.duckdb"


@pytest.fixture(scope="module")
def db_conn():
    """Create read-only database connection for tests."""
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    yield conn
    conn.close()


class TestProviderSearch:
    """Tests for provider-search.md skill patterns."""
    
    def test_search_by_specialty(self, db_conn):
        """Search providers by taxonomy code."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.providers
            WHERE taxonomy_1 LIKE '207R%'  -- Internal Medicine
        """).fetchone()
        
        assert result[0] > 100_000, \
            f"Expected 100K+ internal medicine providers, got {result[0]:,}"
    
    def test_search_by_state(self, db_conn):
        """Search providers by state."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.providers
            WHERE practice_state = 'CA'
        """).fetchone()
        
        assert result[0] > 500_000, \
            f"Expected 500K+ California providers, got {result[0]:,}"
    
    def test_search_by_county(self, db_conn):
        """Search providers by county FIPS."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.providers
            WHERE county_fips = '48201'  -- Harris County, TX
        """).fetchone()
        
        assert result[0] > 50_000, \
            f"Expected 50K+ Harris County providers, got {result[0]:,}"
    
    def test_search_by_credential(self, db_conn):
        """Search providers by credential."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.providers
            WHERE credential LIKE '%MD%'
        """).fetchone()
        
        assert result[0] > 500_000, \
            f"Expected 500K+ MDs, got {result[0]:,}"
    
    def test_search_combined_filters(self, db_conn):
        """Search with multiple filters (specialty + location)."""
        result = db_conn.execute("""
            SELECT npi, first_name, last_name, practice_city
            FROM network.providers
            WHERE taxonomy_1 LIKE '207RC%'  -- Cardiovascular
              AND practice_state = 'TX'
            LIMIT 10
        """).fetchall()
        
        assert len(result) == 10, "Should return 10 cardiologists in TX"
        assert all(row[0] is not None for row in result), "All should have NPI"


class TestFacilitySearch:
    """Tests for facility-search.md skill patterns."""
    
    def test_search_hospitals(self, db_conn):
        """Search for hospitals."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.facilities
            WHERE type LIKE '%Hospital%' OR type LIKE '%01%'
        """).fetchone()
        
        assert result[0] > 5_000, \
            f"Expected 5K+ hospitals, got {result[0]:,}"
    
    def test_search_facilities_by_state(self, db_conn):
        """Search facilities by state."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.facilities
            WHERE state = 'CA'
        """).fetchone()
        
        assert result[0] > 5_000, \
            f"Expected 5K+ California facilities, got {result[0]:,}"
    
    def test_facility_has_beds(self, db_conn):
        """Verify bed count data exists."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.facilities
            WHERE beds IS NOT NULL AND beds > 0
        """).fetchone()
        
        assert result[0] > 1_000, \
            f"Expected 1K+ facilities with bed counts, got {result[0]:,}"


class TestNPIValidation:
    """Tests for npi-validation.md skill patterns."""
    
    def test_npi_lookup(self, db_conn):
        """Look up provider by NPI."""
        # Get a valid NPI first
        valid_npi = db_conn.execute("""
            SELECT npi FROM network.providers LIMIT 1
        """).fetchone()[0]
        
        result = db_conn.execute(f"""
            SELECT npi, first_name, last_name 
            FROM network.providers 
            WHERE npi = '{valid_npi}'
        """).fetchone()
        
        assert result is not None, "Should find provider by NPI"
        assert result[0] == valid_npi, "NPI should match"
    
    def test_npi_format_validation(self, db_conn):
        """Verify NPI format checking works."""
        result = db_conn.execute("""
            SELECT npi FROM network.providers
            WHERE LENGTH(npi) = 10
              AND npi ~ '^[0-9]+$'
            LIMIT 5
        """).fetchall()
        
        assert len(result) == 5, "Should find 5 valid NPIs"


class TestProviderDensity:
    """Tests for provider-density.md skill patterns."""
    
    def test_density_by_county(self, db_conn):
        """Calculate provider density by county."""
        result = db_conn.execute("""
            SELECT 
                p.county_fips,
                COUNT(DISTINCT p.npi) as providers,
                sv.e_totpop as population,
                ROUND(COUNT(DISTINCT p.npi) * 100000.0 / NULLIF(sv.e_totpop, 0), 1) as per_100k
            FROM network.providers p
            JOIN population.svi_county sv ON p.county_fips = sv.stcnty
            WHERE p.practice_state = 'CA'
            GROUP BY p.county_fips, sv.e_totpop
            HAVING sv.e_totpop > 100000
            ORDER BY per_100k DESC
            LIMIT 5
        """).fetchall()
        
        assert len(result) == 5, "Should return 5 California counties"
        assert all(row[3] > 0 for row in result), "All should have positive density"
    
    def test_density_vs_hrsa_benchmark(self, db_conn):
        """Compare density to HRSA benchmarks."""
        result = db_conn.execute("""
            SELECT 
                sv.county,
                COUNT(p.npi) * 100000.0 / sv.e_totpop as density,
                CASE 
                    WHEN COUNT(p.npi) * 100000.0 / sv.e_totpop >= 80 THEN 'Well-served'
                    WHEN COUNT(p.npi) * 100000.0 / sv.e_totpop >= 60 THEN 'Adequate'
                    ELSE 'Shortage'
                END as hrsa_status
            FROM population.svi_county sv
            LEFT JOIN network.providers p 
                ON sv.stcnty = p.county_fips
                AND p.taxonomy_1 LIKE '207Q%'  -- Family Medicine
            WHERE sv.state = 'Texas'
              AND sv.e_totpop > 50000
            GROUP BY sv.county, sv.e_totpop
            ORDER BY density
            LIMIT 10
        """).fetchall()
        
        assert len(result) > 0, "Should return Texas counties"


class TestHospitalQuality:
    """Tests for hospital-quality-search.md skill patterns."""
    
    def test_filter_by_star_rating(self, db_conn):
        """Filter hospitals by star rating."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.hospital_quality
            WHERE hospital_overall_rating IN ('4', '5')
        """).fetchone()
        
        assert result[0] > 1_000, \
            f"Expected 1K+ 4-5 star hospitals, got {result[0]:,}"
    
    def test_join_facility_quality(self, db_conn):
        """Join facilities with quality ratings."""
        result = db_conn.execute("""
            SELECT 
                f.name,
                f.state,
                hq.hospital_overall_rating
            FROM network.facilities f
            JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
            WHERE hq.hospital_overall_rating = '5'
            LIMIT 10
        """).fetchall()
        
        assert len(result) > 0, "Should find 5-star hospitals"


class TestNetworkRoster:
    """Tests for network-roster.md skill patterns."""
    
    def test_generate_roster(self, db_conn):
        """Generate a provider roster."""
        result = db_conn.execute("""
            SELECT 
                npi,
                first_name,
                last_name,
                credential,
                taxonomy_1,
                practice_city,
                practice_state,
                practice_zip
            FROM network.providers
            WHERE taxonomy_1 LIKE '207Q%'  -- Family Medicine
              AND practice_state = 'TX'
              AND county_fips = '48201'  -- Harris County
            ORDER BY last_name, first_name
            LIMIT 100
        """).fetchall()
        
        assert len(result) > 0, "Should generate roster"
        assert all(row[0] is not None for row in result), "All should have NPI"
    
    def test_roster_with_quality(self, db_conn):
        """Generate roster with quality filtering."""
        result = db_conn.execute("""
            SELECT 
                p.npi,
                p.first_name,
                p.last_name,
                p.credential
            FROM network.providers p
            WHERE p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?'  -- MD or DO
              AND p.practice_state = 'CA'
            LIMIT 50
        """).fetchall()
        
        assert len(result) > 0, "Should find MD/DO providers"


class TestPerformance:
    """Performance tests for query patterns."""
    
    def test_provider_search_performance(self, db_conn):
        """Provider search should complete quickly."""
        import time
        
        start = time.time()
        db_conn.execute("""
            SELECT npi, first_name, last_name
            FROM network.providers
            WHERE practice_state = 'TX'
              AND taxonomy_1 LIKE '207R%'
            LIMIT 100
        """).fetchall()
        elapsed = time.time() - start
        
        assert elapsed < 1.0, f"Search took {elapsed:.2f}s, expected < 1s"
    
    def test_density_query_performance(self, db_conn):
        """Density query should complete in reasonable time."""
        import time
        
        start = time.time()
        db_conn.execute("""
            SELECT 
                p.practice_state,
                COUNT(DISTINCT p.npi) as providers
            FROM network.providers p
            GROUP BY p.practice_state
        """).fetchall()
        elapsed = time.time() - start
        
        assert elapsed < 2.0, f"Density query took {elapsed:.2f}s, expected < 2s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
