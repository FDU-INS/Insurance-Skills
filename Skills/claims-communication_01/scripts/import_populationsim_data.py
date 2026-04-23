#!/usr/bin/env python3
"""
Import PopulationSim reference data into HealthSim database.

This script imports CDC PLACES, SVI, and ADI data from embedded CSV files
into the HealthSim DuckDB database for efficient SQL querying.

Usage:
    python scripts/import_populationsim_data.py
    python scripts/import_populationsim_data.py --replace  # Force reimport
    python scripts/import_populationsim_data.py --status   # Check status only
"""

import argparse
import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core" / "src"))

from healthsim.db import get_connection, DEFAULT_DB_PATH
from healthsim.db.reference import (
    import_all_reference_data,
    get_reference_status,
    is_reference_data_loaded,
)


def print_status(conn):
    """Print current reference data status."""
    print("\nReference Data Status")
    print("=" * 60)
    
    status = get_reference_status(conn)
    
    for table_name, info in status.items():
        status_icon = "✅" if info["healthy"] else ("⚠️" if info["exists"] else "❌")
        row_str = f"{info['row_count']:,}" if info["exists"] else "NOT LOADED"
        print(f"{status_icon} {table_name}: {row_str} rows")
        print(f"   {info['description']}")
    
    print()
    if is_reference_data_loaded(conn):
        print("✅ All reference data is loaded and healthy")
    else:
        print("⚠️  Some reference data is missing or incomplete")


def main():
    parser = argparse.ArgumentParser(
        description="Import PopulationSim reference data into HealthSim database"
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Force reimport of all data (drops existing tables)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current status only, don't import",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress messages",
    )
    args = parser.parse_args()

    print("HealthSim PopulationSim Data Import")
    print("=" * 60)
    print(f"Database: {DEFAULT_DB_PATH}")
    
    conn = get_connection()
    
    if args.status:
        print_status(conn)
        return
    
    # Check if already loaded
    if is_reference_data_loaded(conn) and not args.replace:
        print("\n✅ All reference data is already loaded.")
        print("   Use --replace to force reimport.")
        print_status(conn)
        return
    
    print("\nImporting reference data...")
    results = import_all_reference_data(conn, replace=args.replace, verbose=not args.quiet)
    
    # Report results
    print("\n" + "=" * 60)
    print("Import Results:")
    total_rows = 0
    for table_name, count in results.items():
        if count >= 0:
            print(f"  ✅ {table_name}: {count:,} rows")
            total_rows += count
        else:
            print(f"  ❌ {table_name}: FAILED")
    
    print(f"\nTotal: {total_rows:,} rows imported")
    
    # Report database size
    if DEFAULT_DB_PATH.exists():
        size_mb = DEFAULT_DB_PATH.stat().st_size / (1024 * 1024)
        print(f"Database size: {size_mb:.1f} MB")
    
    # Final status check
    if is_reference_data_loaded(conn):
        print("\n✅ All reference data imported successfully!")
    else:
        print("\n⚠️  Some imports may have issues. Run with --status for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
