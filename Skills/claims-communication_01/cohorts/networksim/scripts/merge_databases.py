#!/usr/bin/env python3
"""
Merge HealthSim databases with schema organization.

This script:
1. Copies MCP database (PopulationSim + Entity + State tables)
2. Adds NetworkSim tables from standalone database
3. Organizes into schemas:
   - population: PopulationSim reference data
   - network: NetworkSim provider/facility data
   - main: Entity and state management tables

Usage:
    python3 merge_databases.py
"""

import duckdb
import os
from pathlib import Path

# Database paths
MCP_DB = Path.home() / '.healthsim/healthsim.duckdb'
NETWORK_DB = Path.home() / 'Developer/projects/healthsim-workspace/healthsim.duckdb'
OUTPUT_DB = Path.home() / 'Developer/projects/healthsim-workspace/healthsim.duckdb'

def main():
    print("=" * 80)
    print("HEALTHSIM DATABASE CONSOLIDATION")
    print("=" * 80)
    print()
    
    # Check source databases exist
    if not MCP_DB.exists():
        print(f"❌ MCP database not found: {MCP_DB}")
        return
    
    if not NETWORK_DB.exists():
        print(f"❌ NetworkSim database not found: {NETWORK_DB}")
        return
    
    print(f"Source databases found:")
    print(f"  MCP DB: {MCP_DB} ({MCP_DB.stat().st_size / (1024**2):.1f} MB)")
    print(f"  Network DB: {NETWORK_DB} ({NETWORK_DB.stat().st_size / (1024**2):.1f} MB)")
    print()
    
    # Remove old output database if exists
    if OUTPUT_DB.exists():
        print(f"Removing old output database...")
        os.remove(OUTPUT_DB)
    
    print("=" * 80)
    print("STEP 1: COPY MCP DATABASE")
    print("=" * 80)
    print()
    
    # Copy MCP database to output location
    import shutil
    shutil.copy2(MCP_DB, OUTPUT_DB)
    print(f"✓ Copied MCP database to {OUTPUT_DB}")
    print()
    
    print("=" * 80)
    print("STEP 2: CREATE SCHEMAS")
    print("=" * 80)
    print()
    
    # Connect to output database
    con = duckdb.connect(str(OUTPUT_DB))
    
    # Create schemas
    con.execute("CREATE SCHEMA IF NOT EXISTS population")
    print("✓ Created 'population' schema")
    
    con.execute("CREATE SCHEMA IF NOT EXISTS network")
    print("✓ Created 'network' schema")
    print()
    
    print("=" * 80)
    print("STEP 3: MIGRATE POPULATIONSIM TABLES TO SCHEMA")
    print("=" * 80)
    print()
    
    # Get all ref_* tables
    ref_tables = con.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'main' 
        AND table_name LIKE 'ref_%'
        ORDER BY table_name
    """).fetchall()
    
    for (table_name,) in ref_tables:
        # New name without ref_ prefix
        new_name = table_name.replace('ref_', '')
        
        # Move to population schema
        con.execute(f"CREATE TABLE population.{new_name} AS SELECT * FROM main.{table_name}")
        con.execute(f"DROP TABLE main.{table_name}")
        
        count = con.execute(f"SELECT COUNT(*) FROM population.{new_name}").fetchone()[0]
        print(f"  ✓ {table_name} → population.{new_name} ({count:,} records)")
    
    print()
    print("=" * 80)
    print("STEP 4: ATTACH AND COPY NETWORKSIM TABLES")
    print("=" * 80)
    print()
    
    # Attach NetworkSim database
    con.execute(f"ATTACH '{NETWORK_DB}' AS network_source (READ_ONLY)")
    
    # Get NetworkSim tables
    network_tables = con.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_catalog = 'network_source'
        AND table_schema = 'main'
        ORDER BY table_name
    """).fetchall()
    
    for (table_name,) in network_tables:
        # Copy to network schema
        con.execute(f"CREATE TABLE network.{table_name} AS SELECT * FROM network_source.main.{table_name}")
        
        count = con.execute(f"SELECT COUNT(*) FROM network.{table_name}").fetchone()[0]
        print(f"  ✓ {table_name} → network.{table_name} ({count:,} records)")
    
    # Detach NetworkSim database
    con.execute("DETACH network_source")
    
    print()
    print("=" * 80)
    print("STEP 5: COPY INDEXES FROM NETWORKSIM")
    print("=" * 80)
    print()
    
    # Recreate indexes for network schema
    indexes = [
        ("idx_providers_state", "providers", "state"),
        ("idx_providers_zip", "providers", "zip"),
        ("idx_providers_taxonomy", "providers", "taxonomy_1"),
        ("idx_providers_type", "providers", "entity_type"),
        ("idx_providers_name", "providers", "last_name, first_name"),
        ("idx_facilities_state", "facilities", "state"),
        ("idx_facilities_type", "facilities", "facility_type"),
        ("idx_hospital_quality_state", "hospital_quality", "state"),
    ]
    
    for idx_name, table, columns in indexes:
        try:
            con.execute(f"CREATE INDEX {idx_name} ON network.{table}({columns})")
            print(f"  ✓ Created {idx_name}")
        except Exception as e:
            print(f"  ⚠️  {idx_name}: {e}")
    
    print()
    print("=" * 80)
    print("STEP 6: VALIDATION")
    print("=" * 80)
    print()
    
    # Count tables in each schema
    schemas_summary = con.execute("""
        SELECT 
            table_schema,
            COUNT(*) as table_count
        FROM information_schema.tables
        WHERE table_schema IN ('main', 'population', 'network')
        GROUP BY table_schema
        ORDER BY table_schema
    """).fetchall()
    
    print("Schema Summary:")
    total_tables = 0
    for schema, count in schemas_summary:
        print(f"  {schema}: {count} tables")
        total_tables += count
    print(f"  TOTAL: {total_tables} tables")
    print()
    
    # List all tables in each schema
    print("Detailed Table Listing:")
    print()
    
    for schema in ['main', 'population', 'network']:
        tables = con.execute(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '{schema}'
            ORDER BY table_name
        """).fetchall()
        
        if tables:
            print(f"  {schema.upper()} SCHEMA:")
            for (table_name,) in tables:
                count = con.execute(f"SELECT COUNT(*) FROM {schema}.{table_name}").fetchone()[0]
                print(f"    - {table_name}: {count:,} records")
            print()
    
    # Get database size
    db_size_mb = OUTPUT_DB.stat().st_size / (1024**2)
    
    print("=" * 80)
    print("MERGE COMPLETE!")
    print("=" * 80)
    print()
    print(f"Output database: {OUTPUT_DB}")
    print(f"Database size: {db_size_mb:.1f} MB")
    print(f"Total tables: {total_tables}")
    print()
    print("Next steps:")
    print("1. Test database with MCP server")
    print("2. Update MCP configuration to use healthsim.duckdb")
    print("3. Commit with Git LFS")
    
    con.close()

if __name__ == '__main__':
    main()
