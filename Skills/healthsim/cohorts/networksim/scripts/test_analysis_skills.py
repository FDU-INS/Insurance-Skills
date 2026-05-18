#!/usr/bin/env python3
"""
Test all NetworkSim network analysis skills (Session 6).
Validates query patterns from:
- npi-validation.md
- network-roster.md  
- provider-density.md
- coverage-analysis.md
"""

import duckdb
import time
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent.parent / "healthsim.duckdb"

def run_test(name: str, sql: str, expected_min: int = 1) -> dict:
    """Run a test query and return results with timing."""
    conn = duckdb.connect(str(DB_PATH))
    
    start = time.time()
    try:
        results = conn.execute(sql).fetchall()
        elapsed_ms = (time.time() - start) * 1000
        
        passed = len(results) >= expected_min
        return {
            'name': name,
            'passed': passed,
            'result_count': len(results),
            'expected_min': expected_min,
            'elapsed_ms': elapsed_ms,
            'sample': results[:2] if results else None
        }
    except Exception as e:
        return {
            'name': name,
            'passed': False,
            'error': str(e)
        }
    finally:
        conn.close()

def main():
    """Run all network analysis skill tests."""
    
    print("=" * 80)
    print("NetworkSim Network Analysis Skills Test Suite (Session 6)")
    print("=" * 80)
    
    tests = [
        # NPI VALIDATION TESTS
        {
            'name': 'NPI Validation: Lookup Valid NPI',
            'sql': """
                SELECT npi, first_name, last_name, credential, practice_state
                FROM network.providers
                WHERE npi = '1679576722'
            """,
            'expected_min': 1
        },
        {
            'name': 'NPI Validation: Batch Validation',
            'sql': """
                WITH npi_list AS (
                    SELECT UNNEST(['1679576722', '1588667471', '9999999999']) as npi_to_check
                )
                SELECT nl.npi_to_check, p.npi IS NOT NULL as found
                FROM npi_list nl
                LEFT JOIN network.providers p ON nl.npi_to_check = p.npi
            """,
            'expected_min': 3
        },
        
        # NETWORK ROSTER TESTS
        {
            'name': 'Network Roster: PCP Roster for Harris County',
            'sql': """
                SELECT npi, first_name, last_name, taxonomy_1
                FROM network.providers
                WHERE county_fips = '48201'
                  AND (taxonomy_1 LIKE '207Q%' OR taxonomy_1 LIKE '208D%')
                  AND entity_type_code = '1'
                LIMIT 50
            """,
            'expected_min': 10
        },
        {
            'name': 'Network Roster: Multi-State PCP Counts',
            'sql': """
                SELECT practice_state, COUNT(DISTINCT npi) as pcp_count
                FROM network.providers
                WHERE (taxonomy_1 LIKE '207Q%' OR taxonomy_1 LIKE '208D%' OR taxonomy_1 LIKE '207R%')
                  AND practice_state IN ('CA', 'TX', 'FL', 'NY')
                  AND entity_type_code = '1'
                GROUP BY practice_state
            """,
            'expected_min': 4
        },
        {
            'name': 'Network Roster: Specialty Distribution',
            'sql': """
                SELECT 
                    CASE 
                        WHEN taxonomy_1 LIKE '207Q%' THEN 'Family Medicine'
                        WHEN taxonomy_1 LIKE '207R%' THEN 'Internal Medicine'
                        WHEN taxonomy_1 LIKE '207RC%' THEN 'Cardiology'
                        ELSE 'Other'
                    END as specialty,
                    COUNT(DISTINCT npi) as provider_count
                FROM network.providers
                WHERE practice_state = 'CA'
                  AND entity_type_code = '1'
                  AND (taxonomy_1 LIKE '207Q%' OR taxonomy_1 LIKE '207R%' OR taxonomy_1 LIKE '207RC%')
                GROUP BY specialty
            """,
            'expected_min': 2
        },
        
        # PROVIDER DENSITY TESTS
        {
            'name': 'Provider Density: County-Level Calculation',
            'sql': """
                SELECT 
                    sv.county, sv.state, sv.e_totpop,
                    COUNT(DISTINCT p.npi) as provider_count,
                    ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) as per_100k
                FROM population.svi_county sv
                LEFT JOIN network.providers p 
                    ON sv.stcnty = p.county_fips 
                    AND p.entity_type_code = '1'
                WHERE sv.e_totpop >= 50000
                  AND sv.state = 'Texas'
                GROUP BY sv.county, sv.state, sv.e_totpop
                HAVING COUNT(DISTINCT p.npi) > 0
                LIMIT 20
            """,
            'expected_min': 15
        },
        {
            'name': 'Provider Density: Underserved Area Identification',
            'sql': """
                SELECT 
                    sv.county, sv.state,
                    COUNT(DISTINCT p.npi) as pcp_count,
                    ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) as pcps_per_100k
                FROM population.svi_county sv
                LEFT JOIN network.providers p 
                    ON sv.stcnty = p.county_fips 
                    AND (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '208D%' OR p.taxonomy_1 LIKE '207R%')
                    AND p.entity_type_code = '1'
                WHERE sv.e_totpop >= 25000
                GROUP BY sv.county, sv.state, sv.e_totpop
                HAVING ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(sv.e_totpop, 0), 2) < 60
                   AND COUNT(DISTINCT p.npi) > 0
                LIMIT 30
            """,
            'expected_min': 20
        },
        {
            'name': 'Provider Density: State-Level Specialty Comparison',
            'sql': """
                SELECT 
                    sv.state,
                    SUM(sv.e_totpop) as population,
                    COUNT(DISTINCT p.npi) as cardio_count,
                    ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(SUM(sv.e_totpop), 0), 2) as per_100k
                FROM population.svi_county sv
                LEFT JOIN network.providers p 
                    ON sv.stcnty = p.county_fips 
                    AND p.taxonomy_1 LIKE '207RC%'
                    AND p.entity_type_code = '1'
                WHERE sv.state IN ('California', 'Texas', 'Florida')
                GROUP BY sv.state
            """,
            'expected_min': 3
        },
        
        # COVERAGE ANALYSIS TESTS
        {
            'name': 'Coverage Analysis: Basic Specialty Coverage',
            'sql': """
                SELECT 
                    'Primary Care' as specialty,
                    COUNT(DISTINCT CASE 
                        WHEN taxonomy_1 LIKE '207Q%' OR taxonomy_1 LIKE '208D%' OR taxonomy_1 LIKE '207R%'
                        THEN npi 
                    END) as provider_count
                FROM network.providers
                WHERE practice_state = 'CA' AND entity_type_code = '1'
                UNION ALL
                SELECT 
                    'Cardiology',
                    COUNT(DISTINCT CASE WHEN taxonomy_1 LIKE '207RC%' THEN npi END)
                FROM network.providers
                WHERE practice_state = 'CA' AND entity_type_code = '1'
            """,
            'expected_min': 2
        },
        {
            'name': 'Coverage Analysis: Counties with Coverage Gaps',
            'sql': """
                SELECT 
                    sv.county, sv.state,
                    COUNT(DISTINCT p.npi) as pcp_count
                FROM population.svi_county sv
                LEFT JOIN network.providers p 
                    ON sv.stcnty = p.county_fips 
                    AND (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '208D%' OR p.taxonomy_1 LIKE '207R%')
                    AND p.entity_type_code = '1'
                WHERE sv.e_totpop >= 10000
                GROUP BY sv.county, sv.state
                HAVING COUNT(DISTINCT p.npi) < 5
                LIMIT 20
            """,
            'expected_min': 10
        },
        {
            'name': 'Coverage Analysis: Multi-State Adequacy Scorecard',
            'sql': """
                SELECT 
                    sv.state,
                    COUNT(DISTINCT sv.stcnty) as county_count,
                    SUM(sv.e_totpop) as total_pop,
                    COUNT(DISTINCT p.npi) as total_providers
                FROM population.svi_county sv
                LEFT JOIN network.providers p 
                    ON sv.stcnty = p.county_fips 
                    AND p.entity_type_code = '1'
                WHERE sv.state IN ('California', 'Texas', 'Florida', 'New York')
                GROUP BY sv.state
            """,
            'expected_min': 4
        },
        {
            'name': 'Coverage Analysis: High-Need Low-Access Areas',
            'sql': """
                SELECT 
                    pc.countyname, pc.stateabbr,
                    pc.diabetes_crudeprev,
                    COUNT(DISTINCT p.npi) as pcp_count,
                    ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(pc.totalpopulation, 0), 2) as pcps_per_100k
                FROM population.places_county pc
                LEFT JOIN network.providers p 
                    ON pc.countyfips = p.county_fips 
                    AND (p.taxonomy_1 LIKE '207Q%' OR p.taxonomy_1 LIKE '208D%' OR p.taxonomy_1 LIKE '207R%')
                    AND p.entity_type_code = '1'
                WHERE pc.diabetes_crudeprev >= 13.0
                  AND pc.totalpopulation >= 25000
                GROUP BY pc.countyname, pc.stateabbr, pc.diabetes_crudeprev, pc.totalpopulation
                HAVING ROUND(100000.0 * COUNT(DISTINCT p.npi) / NULLIF(pc.totalpopulation, 0), 2) < 60
                LIMIT 20
            """,
            'expected_min': 10
        },
    ]
    
    # Run all tests
    results = []
    for test in tests:
        print(f"\n{test['name']}...")
        result = run_test(test['name'], test['sql'], test['expected_min'])
        results.append(result)
        
        if result['passed']:
            print(f"  ✅ PASS: {result['result_count']} results in {result['elapsed_ms']:.1f}ms")
            if result.get('sample'):
                print(f"  Sample: {result['sample'][0][:3] if len(result['sample'][0]) > 0 else 'N/A'}")
        else:
            if 'error' in result:
                print(f"  ❌ FAIL: {result['error']}")
            else:
                print(f"  ❌ FAIL: Got {result['result_count']}, expected {result['expected_min']}+")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total} ({100*passed/total:.1f}%)")
    
    avg_time = sum(r.get('elapsed_ms', 0) for r in results if r['passed']) / max(passed, 1)
    print(f"Average Query Time: {avg_time:.1f}ms")
    
    if passed == total:
        print("\n✅ All network analysis skills validated!")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
