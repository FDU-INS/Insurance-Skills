"""
Migrate JSON cohorts to DuckDB.

This module handles the one-time migration of existing JSON-based
cohorts to the new DuckDB storage format.

Usage:
    from healthsim.db.migrate import migrate_all_cohorts
    
    # Dry run - see what would be migrated
    results, backup = migrate_all_cohorts(dry_run=True)
    
    # Actual migration
    results, backup = migrate_all_cohorts()
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import shutil
import json
import logging

logger = logging.getLogger(__name__)


# Legacy storage locations
LEGACY_PATH = Path.home() / ".healthsim" / "cohorts"
BACKUP_PATH = Path.home() / ".healthsim" / "cohorts_backup"


@dataclass
class MigrationResult:
    """Result of a single cohort migration."""
    
    name: str
    success: bool
    entity_count: int = 0
    error: Optional[str] = None
    source_path: Optional[Path] = None
    
    def __repr__(self):
        status = "✓" if self.success else "✗"
        if self.success:
            if self.entity_count == -1:
                return f"{status} {self.name}: [dry run]"
            return f"{status} {self.name}: {self.entity_count} entities"
        return f"{status} {self.name}: {self.error}"


def discover_json_cohorts(legacy_path: Optional[Path] = None) -> List[Dict]:
    """
    Find all JSON cohorts in the legacy location.
    
    Args:
        legacy_path: Override default legacy path (for testing)
    
    Returns:
        List of dicts with keys: name, path, size_bytes, modified_at
    """
    path = legacy_path or LEGACY_PATH
    
    if not path.exists():
        return []
    
    cohorts = []
    for json_file in path.glob("*.json"):
        try:
            stat = json_file.stat()
            cohorts.append({
                'name': json_file.stem,
                'path': json_file,
                'size_bytes': stat.st_size,
                'modified_at': datetime.fromtimestamp(stat.st_mtime),
            })
        except Exception as e:
            logger.warning(f"Could not stat {json_file}: {e}")
    
    # Sort by name for consistent ordering
    cohorts.sort(key=lambda s: s['name'])
    
    return cohorts


def migrate_cohort(
    json_path: Path,
    manager: 'StateManager',
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
        
        logger.info(f"Migrated {name}: {entity_count} entities")
        return MigrationResult(
            name=name,
            success=True,
            entity_count=entity_count,
            source_path=json_path
        )
    except Exception as e:
        logger.error(f"Failed to migrate {name}: {e}")
        return MigrationResult(
            name=name,
            success=False,
            error=str(e),
            source_path=json_path
        )


def migrate_all_cohorts(
    dry_run: bool = False,
    overwrite: bool = False,
    legacy_path: Optional[Path] = None,
    backup_path: Optional[Path] = None,
) -> Tuple[List[MigrationResult], Optional[Path]]:
    """
    Migrate all JSON cohorts to DuckDB.
    
    Args:
        dry_run: If True, report what would be done without doing it
        overwrite: Replace existing cohorts on conflict
        legacy_path: Override default legacy path (for testing)
        backup_path: Override default backup path (for testing)
        
    Returns:
        Tuple of (results list, backup path or None)
    """
    from ...state.manager import StateManager
    
    source_path = legacy_path or LEGACY_PATH
    target_backup = backup_path or BACKUP_PATH
    
    cohorts = discover_json_cohorts(source_path)
    results = []
    
    if not cohorts:
        logger.info("No JSON cohorts found to migrate")
        return results, None
    
    logger.info(f"Found {len(cohorts)} JSON cohort(s) to migrate")
    
    if dry_run:
        for s in cohorts:
            results.append(MigrationResult(
                name=s['name'],
                success=True,
                entity_count=-1,  # -1 indicates dry run
                source_path=s['path']
            ))
        return results, target_backup
    
    # Create state manager for migration
    manager = StateManager()
    
    # Migrate each cohort
    for cohort_info in cohorts:
        result = migrate_cohort(
            cohort_info['path'],
            manager,
            overwrite=overwrite
        )
        results.append(result)
    
    # Backup original files if any migrations succeeded
    actual_backup = None
    if any(r.success for r in results):
        actual_backup = backup_json_cohorts(source_path, target_backup)
    
    return results, actual_backup


def backup_json_cohorts(
    source_path: Optional[Path] = None,
    backup_path: Optional[Path] = None
) -> Optional[Path]:
    """
    Move JSON cohorts to backup location.
    
    Args:
        source_path: Path to cohorts directory
        backup_path: Path for backup
    
    Returns:
        Path to backup directory, or None if no backup created
    """
    source = source_path or LEGACY_PATH
    target = backup_path or BACKUP_PATH
    
    if not source.exists():
        return None
    
    # Ensure parent directory exists
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # If backup already exists, add timestamp to avoid overwrite
    if target.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = target.parent / f"cohorts_backup_{timestamp}"
    
    try:
        shutil.move(str(source), str(target))
        logger.info(f"Backed up cohorts to {target}")
        return target
    except Exception as e:
        logger.error(f"Failed to backup cohorts: {e}")
        return None


def verify_migration(
    expected_count: int,
    expected_names: Optional[List[str]] = None,
    manager: Optional['StateManager'] = None,
) -> Dict:
    """
    Verify that migration was successful.
    
    Args:
        expected_count: Number of cohorts that should exist
        expected_names: Optional list of expected cohort names
        manager: Optional StateManager instance (for testing)
        
    Returns:
        Verification report dict
    """
    if manager is None:
        from ...state.manager import StateManager
        manager = StateManager()
    
    cohorts = manager.list_cohorts()
    
    found_names = [s['name'] for s in cohorts]
    
    report = {
        'expected_count': expected_count,
        'found_count': len(cohorts),
        'count_match': len(cohorts) >= expected_count,
        'found_names': found_names,
        'success': True,
        'missing': [],
    }
    
    if expected_names:
        missing = [n for n in expected_names if n not in found_names]
        report['missing'] = missing
        report['success'] = len(missing) == 0
    
    return report


def get_migration_status(manager: Optional['StateManager'] = None) -> Dict:
    """
    Get current migration status.
    
    Args:
        manager: Optional StateManager instance (for testing)
    
    Returns:
        Dict with legacy_exists, backup_exists, cohort_count
    """
    if manager is None:
        from ...state.manager import StateManager
        manager = StateManager()
    
    cohorts = manager.list_cohorts()
    
    return {
        'legacy_exists': LEGACY_PATH.exists(),
        'legacy_count': len(list(LEGACY_PATH.glob("*.json"))) if LEGACY_PATH.exists() else 0,
        'backup_exists': BACKUP_PATH.exists(),
        'database_cohort_count': len(cohorts),
    }
