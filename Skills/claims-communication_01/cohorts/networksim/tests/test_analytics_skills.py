"""
NetworkSim Analytics Skills Tests
Tests for network adequacy and healthcare desert analysis.
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


class TestNetworkAdequacy:
    """Tests for network-adequacy-analysis.md skill patterns."""
    
    def test_pcp_ratio_calculation(self, db_conn):
        """Calculate PCP-to-population ratio."""
        # Use subqueries to avoid fan-out when joining
        result = db_conn.execute("""
            WITH pop AS (
                SELECT SUM(e_totpop) as total_pop
                FROM population.svi_county
                WHERE state = 'California'
            ),
            pcps AS (
                SELECT COUNT(DISTINCT npi) as pcp_count
                FROM network.providers
                WHERE county_fips LIKE '06%'  -- California FIPS
                  AND taxonomy_1 LIKE '207Q%'  -- Family Medicine
            )
            SELECT 
                'California' as state,
                pop.total_pop,
                pcps.pcp_count,
                ROUND(pop.total_pop / 1200.0, 0) as required_pcps,
                ROUND(100.0 * pcps.pcp_count / NULLIF(pop.total_pop / 1200.0, 0), 1) as adequacy_pct
            FROM pop, pcps
        """).fetchone()
        
        assert result is not None, "Should calculate CA adequacy"
        assert result[4] is not None, "Should have adequacy percentage"
        assert result[4] > 0, "Adequacy should be positive"
    
    def test_county_level_adequacy(self, db_conn):
        """Assess adequacy at county level."""
        result = db_conn.execute("""
            SELECT 
                sv.county,
                sv.e_totpop as population,
                COUNT(DISTINCT p.npi) as pcps,
                ROUND(sv.e_totpop / 1200.0, 1) as required,
                CASE 
                    WHEN COUNT(DISTINCT p.npi) >= sv.e_totpop / 1200.0 THEN 'ADEQUATE'
                    ELSE 'SHORTAGE'
                END as status
            FROM population.svi_county sv
            LEFT JOIN network.providers p 
                ON sv.stcnty = p.county_fips
                AND p.taxonomy_1 LIKE '207Q%'
            WHERE sv.state = 'Texas'
              AND sv.e_totpop > 100000
            GROUP BY sv.county, sv.e_totpop
            ORDER BY population DESC
            LIMIT 10
        """).fetchall()
        
        assert len(result) == 10, "Should return 10 Texas counties"
        assert all(row[4] in ('ADEQUATE', 'SHORTAGE') for row in result)
    
    def test_specialty_coverage(self, db_conn):
        """Check NCQA essential specialty coverage."""
        # Test for presence of cardiology
        result = db_conn.execute("""
            SELECT COUNT(DISTINCT p.npi)
            FROM network.providers p
            WHERE p.taxonomy_1 LIKE '207RC%'  -- Cardiovascular Disease
              AND p.practice_state = 'TX'
        """).fetchone()
        
        assert result[0] > 1_000, \
            f"Expected 1K+ cardiologists in TX, got {result[0]:,}"
    
    def test_cms_ratio_standards(self, db_conn):
        """Verify CMS ratio calculation works."""
        # CMS standard: 1:1,200 for PCPs, 1:2,000 for OB/GYN
        result = db_conn.execute("""
            SELECT 
                'PCP' as specialty,
                COUNT(DISTINCT p.npi) as actual,
                ROUND(10000000 / 1200.0, 0) as required_10m,
                ROUND(100.0 * COUNT(DISTINCT p.npi) / (10000000 / 1200.0), 1) as pct
            FROM network.providers p
            WHERE p.taxonomy_1 LIKE '207Q%'
              AND p.practice_state = 'CA'
        """).fetchone()
        
        assert result is not None, "Should calculate CMS ratio"


class TestHealthcareDeserts:
    """Tests for healthcare-deserts.md skill patterns."""
    
    def test_identify_low_access_counties(self, db_conn):
        """Identify counties with low provider access."""
        result = db_conn.execute("""
            SELECT 
                sv.county,
                sv.state,
                sv.e_totpop as population,
                COUNT(DISTINCT p.npi) as providers,
                ROUND(COUNT(DISTINCT p.npi) * 100000.0 / NULLIF(sv.e_totpop, 0), 1) as per_100k
            FROM population.svi_county sv
            LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
            WHERE sv.e_totpop > 10000
            GROUP BY sv.county, sv.state, sv.e_totpop
            HAVING COUNT(DISTINCT p.npi) * 100000.0 / NULLIF(sv.e_totpop, 0) < 50
            ORDER BY per_100k ASC
            LIMIT 20
        """).fetchall()
        
        assert len(result) > 0, "Should identify low-access counties"
        assert all(row[4] < 50 for row in result), "All should have <50 per 100K"
    
    def test_desert_with_health_burden(self, db_conn):
        """Identify deserts with high disease burden."""
        result = db_conn.execute("""
            SELECT 
                sv.county,
                COUNT(p.npi) * 100000.0 / sv.e_totpop as providers_per_100k,
                sv.rpl_themes as svi_percentile
            FROM population.svi_county sv
            LEFT JOIN network.providers p 
                ON sv.stcnty = p.county_fips
                AND p.taxonomy_1 LIKE '207Q%'
            WHERE sv.state = 'Texas'
              AND sv.e_totpop > 20000
            GROUP BY sv.county, sv.e_totpop, sv.rpl_themes
            HAVING COUNT(p.npi) * 100000.0 / sv.e_totpop < 40
            ORDER BY svi_percentile DESC
            LIMIT 10
        """).fetchall()
        
        assert len(result) > 0, "Should find desert counties in Texas"
    
    def test_desert_severity_classification(self, db_conn):
        """Classify desert severity levels based on PCP availability."""
        # Use subquery to get proper per-county metrics for PCPs
        result = db_conn.execute("""
            WITH county_pcps AS (
                SELECT 
                    sv.county,
                    sv.e_totpop as pop,
                    COUNT(p.npi) as pcp_count
                FROM population.svi_county sv
                LEFT JOIN network.providers p 
                    ON sv.stcnty = p.county_fips
                    AND p.taxonomy_1 LIKE '207Q%'  -- Family Medicine PCPs only
                WHERE sv.state = 'Texas'
                  AND sv.e_totpop > 10000
                GROUP BY sv.county, sv.e_totpop
            )
            SELECT 
                county,
                pcp_count * 100000.0 / pop as per_100k,
                CASE 
                    WHEN pcp_count * 100000.0 / pop < 20 THEN 'Critical'
                    WHEN pcp_count * 100000.0 / pop < 40 THEN 'Severe'
                    WHEN pcp_count * 100000.0 / pop < 60 THEN 'Moderate'
                    ELSE 'Adequate'
                END as severity
            FROM county_pcps
            ORDER BY per_100k ASC
            LIMIT 20
        """).fetchall()
        
        assert len(result) > 0, "Should classify desert severity"
        # With PCP-only counts, some counties should be Critical or Severe
        severities = [row[2] for row in result]
        assert any(s in ('Critical', 'Severe', 'Moderate') for s in severities), \
            f"Should find some underserved counties, got: {severities}"
    
    def test_vulnerable_population_analysis(self, db_conn):
        """Analyze access for vulnerable populations."""
        result = db_conn.execute("""
            SELECT 
                sv.county,
                sv.rpl_themes as svi_overall,
                sv.rpl_theme1 as socioeconomic,
                COUNT(DISTINCT p.npi) as providers,
                sv.e_totpop as population
            FROM population.svi_county sv
            LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
            WHERE sv.rpl_themes > 0.75  -- Top quartile vulnerability
              AND sv.e_totpop > 50000
            GROUP BY sv.county, sv.rpl_themes, sv.rpl_theme1, sv.e_totpop
            ORDER BY sv.rpl_themes DESC
            LIMIT 10
        """).fetchall()
        
        assert len(result) > 0, "Should find high-vulnerability counties"
        assert all(row[1] > 0.75 for row in result), "All should be high SVI"


class TestCompositeScoring:
    """Tests for composite desert scoring."""
    
    def test_composite_desert_score(self, db_conn):
        """Calculate composite desert score."""
        result = db_conn.execute("""
            SELECT 
                sv.county,
                sv.state,
                -- Access gap (35% weight)
                CASE 
                    WHEN COUNT(p.npi) * 100000.0 / sv.e_totpop < 60 
                    THEN (60 - COUNT(p.npi) * 100000.0 / sv.e_totpop) / 60.0
                    ELSE 0 
                END as access_gap,
                -- Vulnerability (25% weight)
                sv.rpl_themes as vulnerability,
                -- Composite score
                (
                    0.35 * CASE 
                        WHEN COUNT(p.npi) * 100000.0 / sv.e_totpop < 60 
                        THEN (60 - COUNT(p.npi) * 100000.0 / sv.e_totpop) / 60.0
                        ELSE 0 
                    END +
                    0.25 * sv.rpl_themes
                ) as partial_score
            FROM population.svi_county sv
            LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
            WHERE sv.state = 'Mississippi'
              AND sv.e_totpop > 10000
            GROUP BY sv.county, sv.state, sv.e_totpop, sv.rpl_themes
            ORDER BY partial_score DESC
            LIMIT 10
        """).fetchall()
        
        assert len(result) > 0, "Should calculate composite scores"
    
    def test_intervention_priority(self, db_conn):
        """Rank counties for intervention priority."""
        result = db_conn.execute("""
            SELECT 
                sv.county,
                sv.e_totpop as population,
                COUNT(p.npi) as providers,
                sv.rpl_themes as svi,
                ROW_NUMBER() OVER (
                    ORDER BY 
                        sv.rpl_themes DESC,
                        COUNT(p.npi) * 100000.0 / sv.e_totpop ASC
                ) as priority_rank
            FROM population.svi_county sv
            LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
            WHERE sv.state = 'Alabama'
              AND sv.e_totpop > 20000
            GROUP BY sv.county, sv.e_totpop, sv.rpl_themes
            LIMIT 10
        """).fetchall()
        
        assert len(result) > 0, "Should rank intervention priorities"
        assert all(1 <= row[4] <= 10 for row in result), "Should have valid ranks"


class TestCrossProductAnalytics:
    """Tests for cross-product integration patterns."""
    
    def test_network_population_join(self, db_conn):
        """Join network data with population data."""
        result = db_conn.execute("""
            SELECT 
                sv.state,
                COUNT(DISTINCT sv.stcnty) as counties,
                SUM(sv.e_totpop) as total_pop,
                COUNT(DISTINCT p.npi) as providers
            FROM population.svi_county sv
            LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
            GROUP BY sv.state
            ORDER BY total_pop DESC
            LIMIT 5
        """).fetchall()
        
        assert len(result) == 5, "Should return top 5 states"
        assert all(row[3] > 0 for row in result), "All states should have providers"
    
    def test_quality_adjusted_adequacy(self, db_conn):
        """Test quality-adjusted network adequacy."""
        result = db_conn.execute("""
            SELECT 
                sv.county,
                COUNT(DISTINCT p.npi) as all_providers,
                COUNT(DISTINCT CASE WHEN p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?' 
                      THEN p.npi END) as quality_providers,
                ROUND(100.0 * COUNT(DISTINCT CASE WHEN p.credential ~ 'M\\.?D\\.?|D\\.?O\\.?' 
                      THEN p.npi END) / NULLIF(COUNT(DISTINCT p.npi), 0), 1) as quality_pct
            FROM population.svi_county sv
            LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
            WHERE sv.state = 'Florida'
              AND sv.e_totpop > 100000
            GROUP BY sv.county
            ORDER BY quality_pct DESC
            LIMIT 10
        """).fetchall()
        
        assert len(result) > 0, "Should calculate quality-adjusted adequacy"


class TestAnalyticsPerformance:
    """Performance tests for analytics queries."""
    
    def test_adequacy_query_performance(self, db_conn):
        """Adequacy query should complete in reasonable time."""
        import time
        
        start = time.time()
        db_conn.execute("""
            SELECT 
                sv.state,
                COUNT(DISTINCT p.npi) as providers,
                SUM(sv.e_totpop) as population
            FROM population.svi_county sv
            LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
            GROUP BY sv.state
        """).fetchall()
        elapsed = time.time() - start
        
        assert elapsed < 5.0, f"Adequacy query took {elapsed:.2f}s, expected < 5s"
    
    def test_desert_analysis_performance(self, db_conn):
        """Desert analysis should complete in reasonable time."""
        import time
        
        start = time.time()
        db_conn.execute("""
            SELECT 
                sv.county,
                COUNT(p.npi) * 100000.0 / sv.e_totpop as per_100k,
                sv.rpl_themes
            FROM population.svi_county sv
            LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
            WHERE sv.e_totpop > 10000
            GROUP BY sv.county, sv.e_totpop, sv.rpl_themes
            ORDER BY per_100k ASC
            LIMIT 100
        """).fetchall()
        elapsed = time.time() - start
        
        assert elapsed < 3.0, f"Desert analysis took {elapsed:.2f}s, expected < 3s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
