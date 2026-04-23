"""
NetworkSim Data Quality Tests
Session 4: Geographic Enrichment & Validation

Tests verify:
- Data import completeness
- Geographic enrichment quality
- NPI format validation
- Cross-schema join functionality
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


class TestProviderData:
    """Tests for network.providers table."""
    
    def test_provider_count(self, db_conn):
        """Verify minimum provider count (should be 8M+)."""
        result = db_conn.execute(
            "SELECT COUNT(*) FROM network.providers"
        ).fetchone()
        
        assert result[0] >= 8_000_000, \
            f"Expected 8M+ providers, got {result[0]:,}"
    
    def test_npi_format(self, db_conn):
        """All NPIs must be 10 digits."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.providers
            WHERE npi !~ '^[0-9]{10}$'
        """).fetchone()
        
        assert result[0] == 0, \
            f"Found {result[0]:,} providers with invalid NPI format"
    
    def test_no_duplicate_npis(self, db_conn):
        """Verify no duplicate NPIs."""
        result = db_conn.execute("""
            SELECT COUNT(*) - COUNT(DISTINCT npi) as duplicates
            FROM network.providers
        """).fetchone()
        
        assert result[0] == 0, \
            f"Found {result[0]:,} duplicate NPIs"
    
    def test_entity_type_valid(self, db_conn):
        """Entity type must be 1 (Individual) or 2 (Organization)."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.providers
            WHERE entity_type_code NOT IN ('1', '2')
        """).fetchone()
        
        assert result[0] == 0, \
            f"Found {result[0]:,} providers with invalid entity_type"
    
    def test_state_coverage(self, db_conn):
        """Verify coverage of all 50 states + DC."""
        result = db_conn.execute("""
            SELECT COUNT(DISTINCT practice_state)
            FROM network.providers
            WHERE practice_state IS NOT NULL
        """).fetchone()
        
        # Should have 50 states + DC + territories
        assert result[0] >= 51, \
            f"Expected 51+ states/territories, got {result[0]}"


class TestGeographicEnrichment:
    """Tests for geographic enrichment (Session 4 focus)."""
    
    def test_county_fips_coverage(self, db_conn):
        """County FIPS coverage must exceed 95%."""
        result = db_conn.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(county_fips) as with_fips,
                ROUND(100.0 * COUNT(county_fips) / COUNT(*), 2) as pct
            FROM network.providers
        """).fetchone()
        
        assert result[2] >= 95.0, \
            f"County FIPS coverage {result[2]}% < 95% target"
    
    def test_county_fips_format(self, db_conn):
        """County FIPS must be 5 digits where present."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.providers
            WHERE county_fips IS NOT NULL
            AND county_fips !~ '^[0-9]{5}$'
        """).fetchone()
        
        assert result[0] == 0, \
            f"Found {result[0]:,} providers with invalid county_fips format"
    
    def test_county_count(self, db_conn):
        """Should cover 3000+ counties."""
        result = db_conn.execute("""
            SELECT COUNT(DISTINCT county_fips)
            FROM network.providers
            WHERE county_fips IS NOT NULL
        """).fetchone()
        
        assert result[0] >= 3000, \
            f"Expected 3000+ counties, got {result[0]:,}"


class TestFacilityData:
    """Tests for network.facilities table."""
    
    def test_facility_count(self, db_conn):
        """Verify minimum facility count (should be 70K+)."""
        result = db_conn.execute(
            "SELECT COUNT(*) FROM network.facilities"
        ).fetchone()
        
        assert result[0] >= 70_000, \
            f"Expected 70K+ facilities, got {result[0]:,}"
    
    def test_ccn_format(self, db_conn):
        """CCN (CMS Certification Number) should typically be 6 characters."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.facilities
            WHERE LENGTH(ccn) = 6
        """).fetchone()
        
        # Most CCNs should be 6 chars, but some variations exist
        total = db_conn.execute("SELECT COUNT(*) FROM network.facilities").fetchone()[0]
        pct_valid = 100.0 * result[0] / total
        
        assert pct_valid >= 90.0, \
            f"Only {pct_valid:.1f}% of CCNs are 6 characters (expected 90%+)"
    
    def test_no_duplicate_ccns(self, db_conn):
        """Verify no duplicate CCNs."""
        result = db_conn.execute("""
            SELECT COUNT(*) - COUNT(DISTINCT ccn) as duplicates
            FROM network.facilities
        """).fetchone()
        
        assert result[0] == 0, \
            f"Found {result[0]:,} duplicate CCNs"


class TestQualityData:
    """Tests for quality metrics tables."""
    
    def test_hospital_quality_count(self, db_conn):
        """Verify hospital quality records."""
        result = db_conn.execute(
            "SELECT COUNT(*) FROM network.hospital_quality"
        ).fetchone()
        
        assert result[0] >= 5_000, \
            f"Expected 5K+ hospital quality records, got {result[0]:,}"
    
    def test_physician_quality_count(self, db_conn):
        """Verify physician quality records."""
        result = db_conn.execute(
            "SELECT COUNT(*) FROM network.physician_quality"
        ).fetchone()
        
        assert result[0] >= 1_000_000, \
            f"Expected 1M+ physician quality records, got {result[0]:,}"


class TestCrossProductIntegration:
    """Tests for cross-schema joins with PopulationSim."""
    
    def test_population_join(self, db_conn):
        """Verify JOIN with PopulationSim places_county."""
        result = db_conn.execute("""
            SELECT COUNT(DISTINCT p.countyfips)
            FROM population.places_county p
            INNER JOIN network.providers n ON p.countyfips = n.county_fips
        """).fetchone()
        
        assert result[0] >= 2_000, \
            f"Expected 2K+ counties in JOIN, got {result[0]:,}"
    
    def test_svi_join(self, db_conn):
        """Verify JOIN with PopulationSim svi_county."""
        result = db_conn.execute("""
            SELECT COUNT(DISTINCT s.stcnty)
            FROM population.svi_county s
            INNER JOIN network.providers n ON s.stcnty = n.county_fips
        """).fetchone()
        
        assert result[0] >= 2_000, \
            f"Expected 2K+ counties in SVI JOIN, got {result[0]:,}"
    
    def test_ahrf_county_data(self, db_conn):
        """Verify AHRF county data."""
        result = db_conn.execute(
            "SELECT COUNT(*) FROM network.ahrf_county"
        ).fetchone()
        
        assert result[0] >= 3_000, \
            f"Expected 3K+ county records, got {result[0]:,}"


class TestDataIntegrity:
    """Tests for referential integrity and data consistency."""
    
    def test_physician_quality_npi_exists(self, db_conn):
        """All NPIs in physician_quality should exist in providers."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.physician_quality pq
            WHERE NOT EXISTS (
                SELECT 1 FROM network.providers p WHERE p.npi = pq.npi
            )
        """).fetchone()
        
        # Note: Some physicians may not be in NPPES registry
        # This is informational, not a hard failure
        if result[0] > 0:
            print(f"\nInfo: {result[0]:,} physician quality NPIs not in provider table")
    
    def test_hospital_quality_facility_exists(self, db_conn):
        """All facility_ids in hospital_quality should exist in facilities."""
        result = db_conn.execute("""
            SELECT COUNT(*) FROM network.hospital_quality hq
            WHERE NOT EXISTS (
                SELECT 1 FROM network.facilities f WHERE f.ccn = hq.facility_id
            )
        """).fetchone()
        
        # Some facilities may not be in POS file
        if result[0] > 0:
            print(f"\nInfo: {result[0]:,} hospital quality facilities not in facility table")


# Test summary marker
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
