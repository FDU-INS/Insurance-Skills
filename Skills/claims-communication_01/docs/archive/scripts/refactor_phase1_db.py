#!/usr/bin/env python3
"""
Cohort Refactoring Script - Phase 1: Database Schema

Renames scenario -> cohort in database layer files.
Run from project root.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Ordered replacements (order matters for some patterns)
REPLACEMENTS = [
    # Table/sequence names (uppercase DDL constants)
    ('SCENARIO_ENTITIES_SEQ_DDL', 'COHORT_ENTITIES_SEQ_DDL'),
    ('SCENARIO_TAGS_SEQ_DDL', 'COHORT_TAGS_SEQ_DDL'),
    ('SCENARIOS_DDL', 'COHORTS_DDL'),
    ('SCENARIO_ENTITIES_DDL', 'COHORT_ENTITIES_DDL'),
    ('SCENARIO_TAGS_DDL', 'COHORT_TAGS_DDL'),
    
    # SQL table names
    ('scenario_entities_seq', 'cohort_entities_seq'),
    ('scenario_tags_seq', 'cohort_tags_seq'),
    ('scenario_entities', 'cohort_entities'),
    ('scenario_tags', 'cohort_tags'),
    ('scenarios', 'cohorts'),
    
    # Column names
    ('scenario_id', 'cohort_id'),
    
    # Index names (patterns)
    ('idx_scenario_', 'idx_cohort_'),
    ('idx_se_', 'idx_ce_'),  # scenario_entities indexes
    ('idx_st_', 'idx_ct_'),  # scenario_tags indexes
    
    # Function names in queries.py
    ('get_patients_in_scenario', 'get_patients_in_cohort'),
    ('get_scenario_summary', 'get_cohort_summary'),
    ('list_scenarios', 'list_cohorts'),
    ('scenario_exists', 'cohort_exists'),
    
    # State table references
    ("'scenarios'", "'cohorts'"),
    ('"scenarios"', '"cohorts"'),
]

def refactor_file(filepath: Path, dry_run: bool = False) -> dict:
    """Apply replacements to a single file."""
    if not filepath.exists():
        return {'file': str(filepath), 'error': 'File not found'}
    
    content = filepath.read_text()
    original = content
    changes = []
    
    for old, new in REPLACEMENTS:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            changes.append(f"  {old} -> {new} ({count}x)")
    
    result = {
        'file': str(filepath),
        'changed': content != original,
        'changes': changes
    }
    
    if content != original and not dry_run:
        filepath.write_text(content)
        result['written'] = True
    
    return result

def main(dry_run: bool = True):
    """Run Phase 1 refactoring on database files."""
    
    db_path = PROJECT_ROOT / 'packages/core/src/healthsim/db'
    
    files = [
        db_path / 'schema.py',
        db_path / 'queries.py',
        db_path / '__init__.py',
    ]
    
    print(f"Phase 1: Database Schema Refactoring {'(DRY RUN)' if dry_run else ''}")
    print("=" * 60)
    
    total_changes = 0
    for filepath in files:
        result = refactor_file(filepath, dry_run)
        if result.get('changed'):
            print(f"\n{result['file']}:")
            for change in result['changes']:
                print(change)
            total_changes += len(result['changes'])
        else:
            print(f"\n{result['file']}: No changes needed")
    
    print(f"\n{'=' * 60}")
    print(f"Total replacement types: {total_changes}")
    if dry_run:
        print("\nThis was a DRY RUN. Run with --apply to make changes.")
    else:
        print("\nChanges applied successfully.")

if __name__ == '__main__':
    import sys
    dry_run = '--apply' not in sys.argv
    main(dry_run)
