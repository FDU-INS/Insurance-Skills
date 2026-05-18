#!/usr/bin/env python3
"""
Geographic Enrichment Script for NetworkSim
Adds county FIPS codes to providers table using Census ZIP-County crosswalk
"""

import duckdb
import time
import sys

def main():
    # Connect to database
    conn = duckdb.connect('/Users/markoswald/Developer/projects/healthsim-workspace/healthsim.duckdb')
    
    print("📊 Geographic Enrichment Process")
    print("=" * 60)
    
    # Step 1: Load crosswalk data
    print("\n1️⃣  Loading ZIP→County crosswalk...")
    start = time.time()
    
    # Create temp table from Census data
    conn.execute("""
        CREATE TEMP TABLE zip_county_xwalk AS
        SELECT 
            ZCTA5 as zip,
            GEOID as county_fips,
            ZPOPPCT as allocation_ratio
        FROM read_csv_auto(
            '/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/raw/zcta_county_rel_10.txt',
            delim=',',
            header=true
        )
        WHERE ZPOPPCT > 0  -- Only keep allocations with population
    """)
    
    xwalk_count = conn.execute("SELECT COUNT(*) FROM zip_county_xwalk").fetchone()[0]
    print(f"   ✓ Loaded {xwalk_count:,} ZIP→County mappings ({time.time()-start:.1f}s)")
    
    # Step 2: Update providers table
    print("\n2️⃣  Updating providers with county FIPS codes...")
    start = time.time()
    
    # For ZIPs that span multiple counties, use the one with highest population allocation
    conn.execute("""
        UPDATE network.providers p
        SET county_fips = (
            SELECT x.county_fips
            FROM zip_county_xwalk x
            WHERE x.zip = SUBSTR(p.practice_zip, 1, 5)
            ORDER BY x.allocation_ratio DESC
            LIMIT 1
        )
        WHERE county_fips IS NULL
    """)
    
    print(f"   ✓ Updated providers ({time.time()-start:.1f}s)")
    
    # Step 3: Validation
    print("\n3️⃣  Validation Results:")
    print("   " + "-" * 56)
    
    # Count coverage
    result = conn.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(county_fips) as with_fips,
            ROUND(100.0 * COUNT(county_fips) / COUNT(*), 2) as pct_coverage
        FROM network.providers
    """).fetchone()
    
    total, with_fips, pct = result
    print(f"   Total providers:      {total:>12,}")
    print(f"   With county FIPS:     {with_fips:>12,}")
    print(f"   Coverage:             {pct:>11.2f}%")
    print(f"   Missing FIPS:         {total-with_fips:>12,}")
    
    # Check if meets target
    target_met = pct > 95.0
    status = "PASS" if target_met else "FAIL"
    print(f"   Target (>95%):        {status:>12}")
    
    if not target_met:
        print("\n   ⚠️  WARNING: Target not met. Checking missing ZIPs...")
        missing = conn.execute("""
            SELECT DISTINCT SUBSTR(practice_zip, 1, 5) as zip, COUNT(*) as count
            FROM network.providers
            WHERE county_fips IS NULL AND practice_zip IS NOT NULL
            GROUP BY zip
            ORDER BY count DESC
            LIMIT 10
        """).fetchall()
        print("\n   Top 10 ZIPs missing from crosswalk:")
        for zip_code, count in missing:
            print(f"     {zip_code}: {count:,} providers")
    
    # Geographic spread
    geo_stats = conn.execute("""
        SELECT 
            COUNT(DISTINCT practice_state) as states,
            COUNT(DISTINCT county_fips) as counties
        FROM network.providers
        WHERE county_fips IS NOT NULL
    """).fetchone()
    
    print(f"\n   States covered:       {geo_stats[0]:>12}")
    print(f"   Counties covered:     {geo_stats[1]:>12,}")
    
    # Top states by provider count
    print("\n4️⃣  Top 10 States by Provider Count:")
    print("   " + "-" * 56)
    top_states = conn.execute("""
        SELECT 
            practice_state,
            COUNT(*) as provider_count,
            COUNT(county_fips) as with_fips,
            ROUND(100.0 * COUNT(county_fips) / COUNT(*), 1) as pct
        FROM network.providers
        GROUP BY practice_state
        ORDER BY provider_count DESC
        LIMIT 10
    """).fetchall()
    
    for state, count, fips, pct_cov in top_states:
        print(f"   {state:5} {count:>10,} providers  ({pct_cov:>5.1f}% with FIPS)")
    
    conn.close()
    print("\n" + "=" * 60)
    print("✅ Geographic enrichment complete!\n")
    
    # Return exit code based on success
    sys.exit(0 if target_met else 1)

if __name__ == "__main__":
    main()
