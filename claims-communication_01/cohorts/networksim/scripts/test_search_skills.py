#!/usr/bin/env python3
"""
Test all NetworkSim search skills with real queries.
Validates query patterns from provider-search, facility-search, and pharmacy-search skills.
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
            'sample': results[:3] if results else None
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
    """Run all search skill tests."""
    
    print("=" * 80)
    print("NetworkSim Search Skills Test Suite")
    print("=" * 80)
    
    tests = [
        # PROVIDER SEARCH TESTS
        {
            'name': 'Provider Search: PCPs in Harris County, TX',
            'sql': """
                SELECT npi, first_name, last_name, credential, practice_city
                FROM network.providers
                WHERE county_fips = '48201'
                  AND (taxonomy_1 LIKE '207Q%' OR taxonomy_1 LIKE '208D%')
                  AND entity_type_code = '1'
                LIMIT 50
            """,
            'expected_min': 10
        },
        {
            'name': 'Provider Search: Cardiologists in California',
            'sql': """
                SELECT npi, first_name, last_name, taxonomy_1, practice_city
                FROM network.providers
                WHERE practice_state = 'CA'
                  AND taxonomy_1 LIKE '207RC%'
                  AND entity_type_code = '1'
                LIMIT 50
            """,
            'expected_min': 10
        },
        {
            'name': 'Provider Search: MDs in New York City',
            'sql': """
                SELECT npi, first_name, last_name, credential, practice_city
                FROM network.providers
                WHERE practice_state = 'NY'
                  AND practice_city IN ('NEW YORK', 'BROOKLYN', 'QUEENS', 'BRONX')
                  AND credential IN ('MD', 'M.D.')
                  AND entity_type_code = '1'
                LIMIT 100
            """,
            'expected_min': 20
        },
        {
            'name': 'Provider Search: Healthcare Organizations in Texas',
            'sql': """
                SELECT npi, organization_name, practice_city, taxonomy_1
                FROM network.providers
                WHERE practice_state = 'TX'
                  AND entity_type_code = '2'
                LIMIT 100
            """,
            'expected_min': 50
        },
        
        # FACILITY SEARCH TESTS
        {
            'name': 'Facility Search: Hospitals in Massachusetts (Type 01)',
            'sql': """
                SELECT ccn, name, city, beds, type
                FROM network.facilities
                WHERE state = 'MA'
                  AND type = '01'
                LIMIT 50
            """,
            'expected_min': 5
        },
        {
            'name': 'Facility Search: Large Facilities (500+ beds)',
            'sql': """
                SELECT ccn, name, city, state, beds
                FROM network.facilities
                WHERE beds >= 500
                  AND type = '01'
                ORDER BY beds DESC
                LIMIT 25
            """,
            'expected_min': 10
        },
        {
            'name': 'Facility Search: Facilities with Quality Ratings',
            'sql': """
                SELECT f.ccn, f.name, f.city, f.state, hq.hospital_overall_rating
                FROM network.facilities f
                INNER JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
                WHERE hq.hospital_overall_rating IS NOT NULL
                LIMIT 100
            """,
            'expected_min': 50
        },
        
        # PHARMACY SEARCH TESTS
        {
            'name': 'Pharmacy Search: Retail Pharmacies in Cook County, IL',
            'sql': """
                SELECT npi, organization_name, practice_city, practice_zip, taxonomy_1
                FROM network.providers
                WHERE county_fips = '17031'
                  AND taxonomy_1 LIKE '332%'
                  AND entity_type_code = '2'
                LIMIT 50
            """,
            'expected_min': 10
        },
        {
            'name': 'Pharmacy Search: Specialty Pharmacies in California',
            'sql': """
                SELECT npi, organization_name, practice_city, taxonomy_1
                FROM network.providers
                WHERE practice_state = 'CA'
                  AND taxonomy_1 = '3336S0011X'
                  AND entity_type_code = '2'
                LIMIT 50
            """,
            'expected_min': 5
        },
        {
            'name': 'Pharmacy Search: All Pharmacy Types Count',
            'sql': """
                SELECT COUNT(*) as pharmacy_count
                FROM network.providers
                WHERE taxonomy_1 LIKE '332%'
                  AND entity_type_code = '2'
            """,
            'expected_min': 1
        },
        
        # CROSS-PRODUCT TESTS
        {
            'name': 'Cross-Product: Providers in High-Diabetes Counties',
            'sql': """
                SELECT 
                    pc.countyname,
                    pc.stateabbr,
                    pc.diabetes_crudeprev,
                    COUNT(p.npi) as provider_count
                FROM population.places_county pc
                LEFT JOIN network.providers p ON pc.countyfips = p.county_fips
                WHERE pc.diabetes_crudeprev > 13.0
                  AND p.entity_type_code = '1'
                GROUP BY pc.countyname, pc.stateabbr, pc.diabetes_crudeprev
                HAVING COUNT(p.npi) > 0
                LIMIT 20
            """,
            'expected_min': 10
        },
        {
            'name': 'Cross-Product: Pharmacy Density by County',
            'sql': """
                SELECT 
                    sv.county,
                    sv.state,
                    sv.e_totpop,
                    COUNT(p.npi) as pharmacy_count,
                    ROUND(100000.0 * COUNT(p.npi) / NULLIF(sv.e_totpop, 0), 2) as per_100k
                FROM population.svi_county sv
                LEFT JOIN network.providers p ON sv.stcnty = p.county_fips 
                    AND p.taxonomy_1 LIKE '332%'
                WHERE sv.e_totpop > 100000
                GROUP BY sv.county, sv.state, sv.e_totpop
                HAVING COUNT(p.npi) > 0
                ORDER BY per_100k DESC
                LIMIT 20
            """,
            'expected_min': 15
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
                print(f"  Sample: {result['sample'][0][:3] if result['sample'][0] else 'No data'}")
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
        print("\n✅ All search skills validated!")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
