#!/usr/bin/env python3
"""
NetworkSim v2.0 - Direct DuckDB Schema Creation and Data Import
Uses DuckDB Python library to create tables and import data
"""

import sys
import duckdb
from pathlib import Path
import time

def create_schema(con):
    """
    Create NetworkSim tables in DuckDB
    """
    print("\n" + "=" * 80)
    print("CREATING NETWORKSIM SCHEMA")
    print("=" * 80)
    
    # Create providers table
    print("\n1. Creating 'providers' table...")
    con.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            npi VARCHAR(10) PRIMARY KEY,
            entity_type_code VARCHAR(1) NOT NULL,
            last_name VARCHAR(100),
            first_name VARCHAR(100),
            middle_name VARCHAR(50),
            name_prefix VARCHAR(10),
            name_suffix VARCHAR(10),
            credential VARCHAR(50),
            gender VARCHAR(1),
            organization_name VARCHAR(255),
            mailing_address_1 VARCHAR(255),
            mailing_city VARCHAR(100),
            mailing_state VARCHAR(2),
            mailing_zip VARCHAR(10),
            practice_address_1 VARCHAR(255),
            practice_address_2 VARCHAR(100),
            practice_city VARCHAR(100),
            practice_state VARCHAR(2),
            practice_zip VARCHAR(10),
            phone VARCHAR(20),
            taxonomy_1 VARCHAR(10),
            taxonomy_2 VARCHAR(10),
            taxonomy_3 VARCHAR(10),
            taxonomy_4 VARCHAR(10),
            primary_taxonomy_switch VARCHAR(1),
            enumeration_date DATE,
            last_update_date DATE,
            deactivation_date DATE,
            reactivation_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✓ 'providers' table created")
    
    # Create facilities table
    print("\n2. Creating 'facilities' table...")
    con.execute("""
        CREATE TABLE IF NOT EXISTS facilities (
            ccn VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255),
            city VARCHAR(100),
            state VARCHAR(2),
            zip VARCHAR(10),
            phone VARCHAR(20),
            type VARCHAR(50),
            subtype VARCHAR(50),
            beds INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✓ 'facilities' table created")
    
    # Create hospital_quality table
    print("\n3. Creating 'hospital_quality' table...")
    con.execute("""
        CREATE TABLE IF NOT EXISTS hospital_quality (
            facility_id VARCHAR(10) PRIMARY KEY,
            facility_name VARCHAR(255),
            city_town VARCHAR(100),
            state VARCHAR(2),
            hospital_overall_rating VARCHAR(10),
            hospital_overall_rating_footnote VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✓ 'hospital_quality' table created")
    
    # Create physician_quality table
    print("\n4. Creating 'physician_quality' table...")
    con.execute("""
        CREATE TABLE IF NOT EXISTS physician_quality (
            npi VARCHAR(10) PRIMARY KEY,
            provider_last_name VARCHAR(100),
            provider_first_name VARCHAR(100),
            provider_middle_name VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✓ 'physician_quality' table created")
    
    # Create ahrf_county table
    print("\n5. Creating 'ahrf_county' table...")
    con.execute("""
        CREATE TABLE IF NOT EXISTS ahrf_county (
            county_fips VARCHAR(5) PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("   ✓ 'ahrf_county' table created")
    
    print("\n✓ All tables created successfully!")

def import_data(con, base_dir):
    """
    Import CSV data into DuckDB tables
    """
    print("\n" + "=" * 80)
    print("IMPORTING DATA")
    print("=" * 80)
    
    processed_dir = base_dir / "data/processed"
    
    # Import providers (largest file)
    print("\n1. Importing providers (~8.9M records, this will take 2-3 minutes)...")
    start_time = time.time()
    nppes_file = processed_dir / "nppes_filtered.csv"
    
    con.execute(f"""
        COPY providers (
            npi, entity_type_code, last_name, first_name, middle_name,
            name_prefix, name_suffix, credential, organization_name,
            mailing_address_1, mailing_city, mailing_state, mailing_zip,
            practice_address_1, practice_address_2, practice_city,
            practice_state, practice_zip, phone,
            taxonomy_1, taxonomy_2, taxonomy_3, taxonomy_4, primary_taxonomy_switch,
            enumeration_date, last_update_date, deactivation_date, reactivation_date
        )
        FROM '{str(nppes_file)}'
        WITH (HEADER TRUE, DELIMITER ',', QUOTE '"')
    """)
    
    count = con.execute("SELECT COUNT(*) FROM providers").fetchone()[0]
    elapsed = time.time() - start_time
    print(f"   ✓ Imported {count:,} providers in {elapsed:.1f} seconds")
    
    # Import facilities
    print("\n2. Importing facilities...")
    start_time = time.time()
    facilities_file = processed_dir / "facilities.csv"
    
    con.execute(f"""
        COPY facilities (ccn, name, city, state, zip, phone, type, subtype, beds)
        FROM '{str(facilities_file)}'
        WITH (HEADER TRUE, DELIMITER ',', QUOTE '"')
    """)
    
    count = con.execute("SELECT COUNT(*) FROM facilities").fetchone()[0]
    elapsed = time.time() - start_time
    print(f"   ✓ Imported {count:,} facilities in {elapsed:.1f} seconds")
    
    # Import hospital quality
    print("\n3. Importing hospital quality...")
    start_time = time.time()
    hospital_file = processed_dir / "hospital_quality.csv"
    
    con.execute(f"""
        COPY hospital_quality (
            facility_id, facility_name, city_town, state,
            hospital_overall_rating, hospital_overall_rating_footnote
        )
        FROM '{str(hospital_file)}'
        WITH (HEADER TRUE, DELIMITER ',', QUOTE '"')
    """)
    
    count = con.execute("SELECT COUNT(*) FROM hospital_quality").fetchone()[0]
    elapsed = time.time() - start_time
    print(f"   ✓ Imported {count:,} hospital quality records in {elapsed:.1f} seconds")
    
    # Import physician quality (large file)
    print("\n4. Importing physician quality (~2.8M records, this will take 1-2 minutes)...")
    start_time = time.time()
    physician_file = processed_dir / "physician_quality.csv"
    
    con.execute(f"""
        COPY physician_quality (
            npi, provider_last_name, provider_first_name, provider_middle_name
        )
        FROM '{str(physician_file)}'
        WITH (HEADER TRUE, DELIMITER ',', QUOTE '"')
    """)
    
    count = con.execute("SELECT COUNT(*) FROM physician_quality").fetchone()[0]
    elapsed = time.time() - start_time
    print(f"   ✓ Imported {count:,} physician quality records in {elapsed:.1f} seconds")
    
    # Import AHRF county
    print("\n5. Importing AHRF county...")
    start_time = time.time()
    ahrf_file = processed_dir / "ahrf_county.csv"
    
    con.execute(f"""
        COPY ahrf_county (county_fips)
        FROM '{str(ahrf_file)}'
        WITH (HEADER TRUE, DELIMITER ',', QUOTE '"')
    """)
    
    count = con.execute("SELECT COUNT(*) FROM ahrf_county").fetchone()[0]
    elapsed = time.time() - start_time
    print(f"   ✓ Imported {count:,} counties in {elapsed:.1f} seconds")
    
    print("\n✓ All data imported successfully!")

def create_indexes(con):
    """
    Create indexes for query performance
    """
    print("\n" + "=" * 80)
    print("CREATING INDEXES")
    print("=" * 80)
    
    indexes = [
        ("idx_providers_state", "providers(practice_state)"),
        ("idx_providers_zip", "providers(practice_zip)"),
        ("idx_providers_taxonomy", "providers(taxonomy_1)"),
        ("idx_providers_type", "providers(entity_type_code)"),
        ("idx_providers_name", "providers(last_name, first_name)"),
        ("idx_facilities_state", "facilities(state)"),
        ("idx_facilities_type", "facilities(type)"),
        ("idx_hospital_quality_state", "hospital_quality(state)"),
    ]
    
    for idx_name, idx_def in indexes:
        print(f"\nCreating {idx_name}...")
        con.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_def}")
        print(f"   ✓ {idx_name} created")
    
    print("\n✓ All indexes created successfully!")

def validate_import(con):
    """
    Validate the imported data
    """
    print("\n" + "=" * 80)
    print("VALIDATION")
    print("=" * 80)
    
    # Record counts
    print("\nRecord Counts:")
    tables = ['providers', 'facilities', 'hospital_quality', 'physician_quality', 'ahrf_county']
    
    for table in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:.<30} {count:>12,}")
    
    # Sample data
    print("\nSample Providers (first 5):")
    results = con.execute("""
        SELECT npi, last_name, first_name, practice_state, taxonomy_1
        FROM providers
        LIMIT 5
    """).fetchall()
    
    for row in results:
        print(f"  NPI: {row[0]}, Name: {row[1]}, {row[2]}, State: {row[3]}, Taxonomy: {row[4]}")
    
    # Check for NULLs in primary keys
    print("\nPrimary Key Validation:")
    null_checks = [
        ("providers", "npi"),
        ("facilities", "ccn"),
        ("hospital_quality", "facility_id"),
        ("physician_quality", "npi"),
        ("ahrf_county", "county_fips")
    ]
    
    all_valid = True
    for table, pk_col in null_checks:
        null_count = con.execute(f"SELECT COUNT(*) FROM {table} WHERE {pk_col} IS NULL").fetchone()[0]
        status = "✓" if null_count == 0 else "✗"
        print(f"  {status} {table}.{pk_col}: {null_count} NULLs")
        if null_count > 0:
            all_valid = False
    
    return all_valid

def main():
    base_dir = Path(__file__).parent.parent
    
    # Find or create healthsim.duckdb in workspace root
    workspace_root = base_dir.parent.parent  # scenarios/networksim -> scenarios -> workspace
    db_path = workspace_root / "healthsim.duckdb"
    
    if db_path.exists():
        print(f"Found existing database: {db_path}")
    else:
        print(f"Creating new database: {db_path}")
        # DuckDB will create the file when we connect
    
    print("=" * 80)
    print("NETWORKSIM v2.0 - DuckDB SCHEMA AND DATA IMPORT")
    print("=" * 80)
    print(f"\nDatabase: {db_path}")
    print(f"Base directory: {base_dir}")
    print()
    
    # Connect to database
    con = duckdb.connect(str(db_path))
    
    try:
        # Create schema
        create_schema(con)
        
        # Import data
        import_data(con, base_dir)
        
        # Create indexes
        create_indexes(con)
        
        # Validate
        valid = validate_import(con)
        
        # Final summary
        print("\n" + "=" * 80)
        print("IMPORT COMPLETE")
        print("=" * 80)
        
        if valid:
            print("\n✓ All validation checks passed!")
            print(f"✓ NetworkSim tables successfully added to {db_path}")
            return 0
        else:
            print("\n✗ Some validation checks failed - review above")
            return 1
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        con.close()

if __name__ == "__main__":
    sys.exit(main())
