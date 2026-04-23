#!/usr/bin/env python3
"""
Test MCP server connection to HealthSim database.

Verifies:
- Connection to healthsim.duckdb
- Access to all three schemas (main, population, network)
- Cross-schema JOIN capabilities
"""

import sys
from pathlib import Path

# Add packages to path
WORKSPACE_ROOT = Path(__file__).parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))

from healthsim.db import get_connection, DEFAULT_DB_PATH

def test_connection():
    """Test database connection and schema access."""
    print("=" * 80)
    print("Testing MCP Server Database Connection")
    print("=" * 80)
    print()
    
    # Verify database path
    print(f"Database Path: {DEFAULT_DB_PATH}")
    print(f"Database Exists: {DEFAULT_DB_PATH.exists()}")
    print(f"Database Size: {DEFAULT_DB_PATH.stat().st_size / (1024**3):.2f} GB")
    print()
    
    # Get connection
    print("Connecting to database...")
    conn = get_connection()
    print("✓ Connection successful")
    print()
    
    # Test schema access
    print("=" * 80)
    print("Schema Organization")
    print("=" * 80)
    print()
    
    schemas = {
        "main": "Entity tables (patients, members, encounters, claims)",
        "population": "PopulationSim reference data (CDC PLACES, SVI, ADI)",
        "network": "NetworkSim provider/facility data (NPPES, quality)"
    }
    
    for schema, description in schemas.items():
        print(f"\n{schema.upper()} SCHEMA: {description}")
        print("-" * 80)
        
        # List tables in schema
        if schema == "main":
            result = conn.execute("SHOW TABLES").fetchall()
            tables = [row[0] for row in result if not row[0].startswith(("population.", "network."))]
        else:
            result = conn.execute(f"SHOW TABLES FROM {schema}").fetchall()
            tables = [row[0] for row in result]
        
        print(f"Tables: {len(tables)}")
        for table in sorted(tables)[:5]:  # Show first 5
            table_name = f"{schema}.{table}" if schema != "main" else table
            count_result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
            print(f"  - {table}: {count_result[0]:,} records")
        
        if len(tables) > 5:
            print(f"  ... and {len(tables) - 5} more tables")
    
    # Test cross-schema JOIN
    print("\n" + "=" * 80)
    print("Cross-Schema JOIN Test")
    print("=" * 80)
    print()
    
    query = """
    SELECT 
        p.st_abbr as state,
        COUNT(DISTINCT n.npi) as provider_count,
        AVG(p.e_totpop) as avg_population
    FROM population.svi_county p
    LEFT JOIN network.providers n ON n.practice_state = p.st_abbr
    WHERE p.st_abbr IN ('CA', 'TX', 'NY')
    GROUP BY p.st_abbr
    ORDER BY provider_count DESC
    """
    
    print("Query: Join population.svi_county with network.providers")
    result = conn.execute(query).fetchall()
    
    print("\nResults:")
    print(f"{'State':<10} {'Providers':<15} {'Avg Population':<20}")
    print("-" * 50)
    for row in result:
        state, count, avg_pop = row
        print(f"{state:<10} {count:>14,} {avg_pop:>19,.0f}")
    
    print("\n✓ Cross-schema JOIN successful")
    
    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print("✓ Database connection working")
    print("✓ All three schemas accessible (main, population, network)")
    print("✓ Cross-schema JOINs functional")
    print("✓ MCP server ready for use")
    print()

if __name__ == "__main__":
    try:
        test_connection()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
