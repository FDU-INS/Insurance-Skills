#!/usr/bin/env python3
"""
NetworkSim v2.0 - DuckDB Data Import Script
Imports all processed data into healthsim.duckdb using healthsim-mcp
"""

import sys
import time
from pathlib import Path

# Note: This script will be executed by Claude using the healthsim_query MCP tool
# It generates the SQL commands needed for import

def generate_import_sql(base_dir):
    """
    Generate SQL commands to import all NetworkSim data
    """
    processed_dir = base_dir / "data/processed"
    
    # Make paths absolute and properly formatted for DuckDB
    nppes_file = str(processed_dir / "nppes_filtered.csv").replace("'", "''")
    facilities_file = str(processed_dir / "facilities.csv").replace("'", "''")
    hospital_file = str(processed_dir / "hospital_quality.csv").replace("'", "''")
    physician_file = str(processed_dir / "physician_quality.csv").replace("'", "''")
    ahrf_file = str(processed_dir / "ahrf_county.csv").replace("'", "''")
    
    import_sql = f"""
-- ============================================================================
-- NetworkSim v2.0 Data Import
-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
-- ============================================================================

-- Import providers (~8.9M records)
COPY providers (
    npi, entity_type_code, last_name, first_name, middle_name,
    name_prefix, name_suffix, credential, gender, organization_name,
    mailing_address_1, mailing_city, mailing_state, mailing_zip,
    practice_address_1, practice_address_2, practice_city,
    practice_state, practice_zip, phone,
    taxonomy_1, taxonomy_2, taxonomy_3, taxonomy_4, primary_taxonomy_switch,
    enumeration_date, last_update_date, deactivation_date, reactivation_date
)
FROM '{nppes_file}'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- Import facilities (~77K records)  
COPY facilities (ccn, name, city, state, zip, phone, type, subtype, beds)
FROM '{facilities_file}'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- Import hospital quality (~5K records)
COPY hospital_quality (
    facility_id, facility_name, city_town, state,
    hospital_overall_rating, hospital_overall_rating_footnote
)
FROM '{hospital_file}'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- Import physician quality (~2.8M records)
COPY physician_quality (
    npi, provider_last_name, provider_first_name, provider_middle_name
)
FROM '{physician_file}'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- Import AHRF county (~3K records)
COPY ahrf_county (county_fips)
FROM '{ahrf_file}'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- ============================================================================
-- Import Validation Queries
-- ============================================================================

-- Check record counts
SELECT 'providers' as table_name, COUNT(*) as record_count FROM providers
UNION ALL
SELECT 'facilities', COUNT(*) FROM facilities
UNION ALL
SELECT 'hospital_quality', COUNT(*) FROM hospital_quality
UNION ALL
SELECT 'physician_quality', COUNT(*) FROM physician_quality
UNION ALL
SELECT 'ahrf_county', COUNT(*) FROM ahrf_county;

-- Check for NULLs in primary keys
SELECT 'providers_null_npi' as check_name, COUNT(*) as null_count 
FROM providers WHERE npi IS NULL
UNION ALL
SELECT 'facilities_null_ccn', COUNT(*) FROM facilities WHERE ccn IS NULL
UNION ALL
SELECT 'hospital_quality_null_id', COUNT(*) FROM hospital_quality WHERE facility_id IS NULL
UNION ALL
SELECT 'physician_quality_null_npi', COUNT(*) FROM physician_quality WHERE npi IS NULL
UNION ALL
SELECT 'ahrf_county_null_fips', COUNT(*) FROM ahrf_county WHERE county_fips IS NULL;

-- Sample data verification
SELECT 'Sample providers' as description, npi, last_name, first_name, practice_state, taxonomy_1
FROM providers LIMIT 5;

SELECT 'Sample facilities' as description, ccn, name, state, type, beds
FROM facilities LIMIT 5;

-- ============================================================================
-- End of import script
-- ============================================================================
"""
    
    return import_sql

def main():
    base_dir = Path(__file__).parent.parent
    
    print("=" * 80)
    print("NETWORKSIM v2.0 - DuckDB IMPORT SCRIPT GENERATOR")
    print("=" * 80)
    print(f"\nBase directory: {base_dir}")
    print(f"Processed data: {base_dir / 'data/processed'}")
    print()
    
    # Generate import SQL
    import_sql = generate_import_sql(base_dir)
    
    # Save to file
    output_file = base_dir / "scripts/import_data.sql"
    with open(output_file, 'w') as f:
        f.write(import_sql)
    
    print(f"✓ Generated import SQL: {output_file}")
    print()
    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print()
    print("1. Execute schema creation:")
    print("   Use healthsim_query with scripts/create_schema.sql")
    print()
    print("2. Execute data import:")
    print("   Use healthsim_query with scripts/import_data.sql")
    print()
    print("3. Verify imports:")
    print("   Check record counts and sample data")
    print()
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
