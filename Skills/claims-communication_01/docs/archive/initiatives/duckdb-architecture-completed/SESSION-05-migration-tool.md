# Session 05: Migration Tool

**Initiative**: DuckDB Unified Data Architecture  
**Phase**: 1 - Foundation  
**Estimated Duration**: 30-45 minutes  
**Prerequisites**: SESSION-01 through SESSION-04 complete

---

## Objective

Create a migration tool that converts existing JSON cohorts to the new DuckDB format. This enables users to upgrade without losing their saved cohorts.

---

## Context

Users with existing HealthSim installations may have cohorts saved as JSON files in `~/.healthsim/cohorts/`. This tool will:
1. Discover all existing JSON cohorts
2. Import them to the DuckDB database
3. Preserve the original files as backup
4. Report migration status

### Reference Documents

```
docs/initiatives/duckdb-architecture/MASTER-PLAN.md
packages/core/healthsim/state/legacy.py
packages/core/healthsim/state/manager.py
~/.healthsim/cohorts/                              # Existing JSON files
```

---

## Pre-Flight Checklist

- [ ] SESSION-04 complete (JSON import working)
- [ ] Note any existing JSON cohorts in `~/.healthsim/cohorts/`
- [ ] Git status clean

---

## Deliverables

### 1. Migration Script

```
scripts/migrate_json_to_duckdb.py
```

### 2. Migration Module

```
packages/core/healthsim/db/migrate/
├── __init__.py
├── json_cohorts.py        # JSON to DuckDB migration
└── validator.py             # Verify migration success
```

### 3. Tests

```
packages/core/tests/db/test_migration.py
```

---

## Implementation Steps

### Step 1: Create Migration Module

```python
# packages/core/healthsim/db/migrate/json_cohorts.py
"""
Migrate JSON cohorts to DuckDB.

This module handles the one-time migration of existing JSON-based
cohorts to the new DuckDB storage format.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import shutil
import json

from ..connection import DEFAULT_DB_PATH
from ...state.manager import StateManager
from ...state.legacy import list_legacy_cohorts, import_from_json


LEGACY_PATH = Path.home() / ".healthsim" / "cohorts"
BACKUP_PATH = Path.home() / ".healthsim" / "cohorts_backup"


class MigrationResult:
    """Result of a single cohort migration."""
    
    def __init__(self, name: str, success: bool, 
                 entity_count: int = 0, error: Optional[str] = None):
        self.name = name
        self.success = success
        self.entity_count = entity_count
        self.error = error
    
    def __repr__(self):
        status = "✓" if self.success else "✗"
        if self.success:
            return f"{status} {self.name}: {self.entity_count} entities"
        return f"{status} {self.name}: {self.error}"


def discover_json_cohorts() -> List[Dict]:
    """
    Find all JSON cohorts in the legacy location.
    
    Returns:
        List of {name, path, size, modified_at}
    """
    return list_legacy_cohorts()


def migrate_cohort(
    json_path: Path,
    manager: StateManager,
    overwrite: bool = False
) -> MigrationResult:
    """
    Migrate a single JSON cohort to DuckDB.
    
    Args:
        json_path: Path to JSON file
        manager: State manager instance
        overwrite: Replace existing cohort if name conflicts
        
    Returns:
        MigrationResult with success/failure info
    """
    name = json_path.stem
    
    try:
        cohort_id = manager.import_from_json(json_path, overwrite=overwrite)
        cohort = manager.load_cohort(cohort_id)
        entity_count = sum(len(v) for v in cohort['entities'].values())
        return MigrationResult(name, True, entity_count)
    except Exception as e:
        return MigrationResult(name, False, error=str(e))


def migrate_all_cohorts(
    dry_run: bool = False,
    overwrite: bool = False
) -> Tuple[List[MigrationResult], Path]:
    """
    Migrate all JSON cohorts to DuckDB.
    
    Args:
        dry_run: If True, report what would be done without doing it
        overwrite: Replace existing cohorts on conflict
        
    Returns:
        Tuple of (results list, backup path)
    """
    cohorts = discover_json_cohorts()
    results = []
    
    if not cohorts:
        return results, BACKUP_PATH
    
    if dry_run:
        for s in cohorts:
            results.append(MigrationResult(s['name'], True, 
                                          entity_count=-1))  # -1 = dry run
        return results, BACKUP_PATH
    
    manager = StateManager()
    
    for cohort_info in cohorts:
        result = migrate_cohort(
            cohort_info['path'],
            manager,
            overwrite=overwrite
        )
        results.append(result)
    
    # Create backup of original JSON files
    if LEGACY_PATH.exists() and any(r.success for r in results):
        backup_json_cohorts()
    
    return results, BACKUP_PATH


def backup_json_cohorts() -> Path:
    """
    Move JSON cohorts to backup location.
    
    Returns:
        Path to backup directory
    """
    if LEGACY_PATH.exists():
        BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # If backup already exists, add timestamp
        if BACKUP_PATH.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            actual_backup = BACKUP_PATH.parent / f"cohorts_backup_{timestamp}"
            shutil.move(str(LEGACY_PATH), str(actual_backup))
            return actual_backup
        
        shutil.move(str(LEGACY_PATH), str(BACKUP_PATH))
    
    return BACKUP_PATH


def verify_migration(original_count: int) -> Dict:
    """
    Verify that migration was successful.
    
    Args:
        original_count: Number of cohorts that should exist
        
    Returns:
        Verification report
    """
    manager = StateManager()
    cohorts = manager.list_cohorts()
    
    return {
        'expected': original_count,
        'found': len(cohorts),
        'match': len(cohorts) >= original_count,
        'cohorts': [s['name'] for s in cohorts]
    }
```

### Step 2: Create Migration Script

```python
#!/usr/bin/env python3
# scripts/migrate_json_to_duckdb.py
"""
Migrate HealthSim JSON cohorts to DuckDB.

Usage:
    python scripts/migrate_json_to_duckdb.py [options]

Options:
    --dry-run       Show what would be migrated without doing it
    --overwrite     Replace existing cohorts on name conflict
    --no-backup     Don't backup original JSON files (not recommended)
"""

import argparse
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core"))

from healthsim.db.migrate.json_cohorts import (
    discover_json_cohorts,
    migrate_all_cohorts,
    verify_migration,
    LEGACY_PATH,
    BACKUP_PATH,
)


def main():
    parser = argparse.ArgumentParser(
        description="Migrate HealthSim JSON cohorts to DuckDB"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be migrated without doing it"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true", 
        help="Replace existing cohorts on name conflict"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't backup original JSON files"
    )
    args = parser.parse_args()
    
    print("HealthSim JSON to DuckDB Migration")
    print("=" * 40)
    
    # Discover cohorts
    cohorts = discover_json_cohorts()
    
    if not cohorts:
        print(f"\nNo JSON cohorts found in {LEGACY_PATH}")
        print("Nothing to migrate.")
        return 0
    
    print(f"\nFound {len(cohorts)} JSON cohort(s):")
    for s in cohorts:
        size_kb = s['path'].stat().st_size / 1024
        print(f"  - {s['name']} ({size_kb:.1f} KB)")
    
    if args.dry_run:
        print("\n[DRY RUN] Would migrate the above cohorts.")
        print(f"[DRY RUN] Original files would be backed up to {BACKUP_PATH}")
        return 0
    
    # Confirm
    print("\nThis will:")
    print("  1. Import all JSON cohorts to DuckDB")
    print(f"  2. Move original JSON files to {BACKUP_PATH}")
    response = input("\nProceed? [y/N] ")
    
    if response.lower() != 'y':
        print("Aborted.")
        return 1
    
    # Migrate
    print("\nMigrating...")
    results, backup_path = migrate_all_cohorts(overwrite=args.overwrite)
    
    # Report results
    print("\nMigration Results:")
    success_count = 0
    for result in results:
        print(f"  {result}")
        if result.success:
            success_count += 1
    
    print(f"\nSummary: {success_count}/{len(results)} cohorts migrated successfully")
    
    if backup_path.exists():
        print(f"Original files backed up to: {backup_path}")
    
    # Verify
    if success_count > 0:
        verification = verify_migration(success_count)
        if verification['match']:
            print("\n✓ Verification passed")
        else:
            print(f"\n⚠ Verification warning: Expected {verification['expected']}, found {verification['found']}")
    
    return 0 if success_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
```

### Step 3: Write Tests

```python
# packages/core/tests/db/test_migration.py
"""Tests for JSON to DuckDB migration."""

import pytest
import json
from pathlib import Path
import tempfile
import shutil

from healthsim.db.migrate.json_cohorts import (
    discover_json_cohorts,
    migrate_cohort,
    migrate_all_cohorts,
    MigrationResult,
)
from healthsim.state.manager import StateManager


@pytest.fixture
def mock_legacy_path(tmp_path, monkeypatch):
    """Create mock legacy cohorts directory."""
    legacy_dir = tmp_path / "cohorts"
    legacy_dir.mkdir()
    
    # Create sample JSON cohorts
    cohort1 = {
        'name': 'test-cohort-1',
        'entities': {
            'patient': [{'given_name': 'Test1'}]
        }
    }
    cohort2 = {
        'name': 'test-cohort-2',
        'entities': {
            'patient': [{'given_name': 'Test2'}, {'given_name': 'Test2b'}]
        }
    }
    
    (legacy_dir / "test-cohort-1.json").write_text(json.dumps(cohort1))
    (legacy_dir / "test-cohort-2.json").write_text(json.dumps(cohort2))
    
    # Patch the legacy path
    import healthsim.db.migrate.json_cohorts as migrate_module
    monkeypatch.setattr(migrate_module, 'LEGACY_PATH', legacy_dir)
    monkeypatch.setattr(migrate_module, 'BACKUP_PATH', tmp_path / "backup")
    
    return legacy_dir


def test_discover_cohorts(mock_legacy_path):
    """Test discovering JSON cohorts."""
    cohorts = discover_json_cohorts()
    
    assert len(cohorts) == 2
    names = [s['name'] for s in cohorts]
    assert 'test-cohort-1' in names
    assert 'test-cohort-2' in names


def test_migrate_single_cohort(mock_legacy_path, tmp_path):
    """Test migrating a single cohort."""
    # Setup test database
    db_path = tmp_path / "test.duckdb"
    # ... database setup
    
    manager = StateManager()
    json_path = mock_legacy_path / "test-cohort-1.json"
    
    result = migrate_cohort(json_path, manager)
    
    assert result.success
    assert result.name == "test-cohort-1"
    assert result.entity_count == 1


def test_migrate_all_dry_run(mock_legacy_path):
    """Test dry run mode."""
    results, backup_path = migrate_all_cohorts(dry_run=True)
    
    assert len(results) == 2
    # Dry run should not actually migrate
    # Original files should still exist
    assert (mock_legacy_path / "test-cohort-1.json").exists()


def test_migrate_all_with_backup(mock_legacy_path, tmp_path, monkeypatch):
    """Test full migration with backup."""
    # ... full migration test
    pass
```

### Step 4: Run Tests

```bash
cd packages/core
source .venv/bin/activate
pytest tests/db/test_migration.py -v
pytest tests/ -v
```

---

## Post-Flight Checklist

- [ ] Migration script runs without errors
- [ ] Discovers all JSON cohorts
- [ ] Imports cohorts correctly
- [ ] Creates backup of original files
- [ ] Verification passes
- [ ] Dry run works
- [ ] Error handling for corrupt JSON
- [ ] All tests pass

---

## Commit

```bash
git add -A
git commit -m "[Database] Add JSON to DuckDB migration tool

- Create migration module for JSON cohorts
- Add migrate_json_to_duckdb.py script
- Support dry-run mode for preview
- Backup original JSON files to cohorts_backup/
- Add migration verification
- Add migration tests

Part of: DuckDB Unified Data Architecture initiative"

git push
```

---

## Update MASTER-PLAN.md

Mark SESSION-05 as complete with commit hash.

---

## Success Criteria

✅ Session complete when:
1. Migration script discovers all JSON cohorts
2. Cohorts are imported to DuckDB correctly
3. Original files backed up safely
4. Dry run shows what would happen
5. Verification confirms migration success
6. All tests pass
7. Committed and pushed

---

## Next Session

Proceed to [SESSION-06: Documentation](SESSION-06-documentation.md)
