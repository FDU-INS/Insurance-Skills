#!/usr/bin/env python3
"""
Migrate HealthSim JSON scenarios to DuckDB.

This script migrates existing JSON-based scenarios from ~/.healthsim/scenarios/
to the new DuckDB database at ~/.healthsim/healthsim.duckdb.

Usage:
    python scripts/migrate_json_to_duckdb.py [options]

Options:
    --dry-run       Show what would be migrated without doing it
    --overwrite     Replace existing scenarios on name conflict
    --no-backup     Don't backup original JSON files (not recommended)
    --quiet         Minimal output
    --verbose       Detailed output

Examples:
    # Preview what would be migrated
    python scripts/migrate_json_to_duckdb.py --dry-run
    
    # Migrate all scenarios
    python scripts/migrate_json_to_duckdb.py
    
    # Migrate and overwrite existing
    python scripts/migrate_json_to_duckdb.py --overwrite
"""

import argparse
import sys
from pathlib import Path

# Add packages to path for standalone execution
SCRIPT_DIR = Path(__file__).parent.resolve()
PACKAGES_DIR = SCRIPT_DIR.parent / "packages" / "core" / "src"
if PACKAGES_DIR.exists():
    sys.path.insert(0, str(PACKAGES_DIR))

from healthsim.db.migrate.json_scenarios import (
    discover_json_scenarios,
    migrate_all_scenarios,
    verify_migration,
    get_migration_status,
    LEGACY_PATH,
    BACKUP_PATH,
)


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def main():
    parser = argparse.ArgumentParser(
        description="Migrate HealthSim JSON scenarios to DuckDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be migrated without doing it"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true", 
        help="Replace existing scenarios on name conflict"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't backup original JSON files (not recommended)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Minimal output"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Detailed output"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show migration status and exit"
    )
    args = parser.parse_args()
    
    # Status mode
    if args.status:
        status = get_migration_status()
        print("HealthSim Migration Status")
        print("=" * 40)
        print(f"Legacy scenarios exist: {status['legacy_exists']}")
        if status['legacy_exists']:
            print(f"  Count: {status['legacy_count']}")
        print(f"Backup exists: {status['backup_exists']}")
        print(f"Database scenarios: {status['database_scenario_count']}")
        return 0
    
    if not args.quiet:
        print("HealthSim JSON to DuckDB Migration")
        print("=" * 40)
    
    # Discover scenarios
    scenarios = discover_json_scenarios()
    
    if not scenarios:
        if not args.quiet:
            print(f"\nNo JSON scenarios found in {LEGACY_PATH}")
            print("Nothing to migrate.")
        return 0
    
    if not args.quiet:
        print(f"\nFound {len(scenarios)} JSON scenario(s):")
        for s in scenarios:
            size = format_size(s['size_bytes'])
            print(f"  - {s['name']} ({size})")
    
    if args.dry_run:
        if not args.quiet:
            print("\n[DRY RUN] Would migrate the above scenarios.")
            if not args.no_backup:
                print(f"[DRY RUN] Original files would be backed up to {BACKUP_PATH}")
        return 0
    
    # Confirm (unless quiet mode)
    if not args.quiet:
        print("\nThis will:")
        print("  1. Import all JSON scenarios to DuckDB")
        if not args.no_backup:
            print(f"  2. Move original JSON files to {BACKUP_PATH}")
        response = input("\nProceed? [y/N] ")
        
        if response.lower() != 'y':
            print("Aborted.")
            return 1
    
    # Migrate
    if not args.quiet:
        print("\nMigrating...")
    
    results, backup_path = migrate_all_scenarios(
        overwrite=args.overwrite
    )
    
    # Report results
    success_count = sum(1 for r in results if r.success)
    
    if not args.quiet:
        print("\nMigration Results:")
        for result in results:
            print(f"  {result}")
        
        print(f"\nSummary: {success_count}/{len(results)} scenarios migrated successfully")
        
        if backup_path and backup_path.exists():
            print(f"Original files backed up to: {backup_path}")
    
    # Verify
    if success_count > 0:
        expected_names = [r.name for r in results if r.success]
        verification = verify_migration(success_count, expected_names)
        
        if not args.quiet:
            if verification['success']:
                print("\n✓ Verification passed")
            else:
                print(f"\n⚠ Verification warning:")
                if verification['missing']:
                    print(f"  Missing scenarios: {verification['missing']}")
    
    return 0 if success_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
