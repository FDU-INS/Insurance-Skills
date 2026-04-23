#!/usr/bin/env python3
"""
Cohort Refactoring Script - Phase 1+2: Database + State Layer

This script renames scenario -> cohort throughout:
- Database schema (schema.py, queries.py)
- State management (manager.py, auto_persist.py, etc.)

Run from project root with: python refactor_cohort.py --apply
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Files to update (in order)
FILES = [
    # Phase 1: Database
    'packages/core/src/healthsim/db/schema.py',
    'packages/core/src/healthsim/db/queries.py',
    'packages/core/src/healthsim/db/__init__.py',
    # Phase 2: State management
    'packages/core/src/healthsim/state/manager.py',
    'packages/core/src/healthsim/state/auto_persist.py',
    'packages/core/src/healthsim/state/auto_naming.py',
    'packages/core/src/healthsim/state/summary.py',
    'packages/core/src/healthsim/state/serializers.py',
    'packages/core/src/healthsim/state/workspace.py',
    'packages/core/src/healthsim/state/legacy.py',
    'packages/core/src/healthsim/state/__init__.py',
    # Tests
    'packages/core/tests/db/test_schema.py',
    'packages/core/tests/state/test_manager.py',
    'packages/core/tests/state/test_summary.py',
    'packages/core/tests/state/test_auto_persist.py',
    'packages/core/tests/state/test_auto_persist_integration.py',
    'packages/core/tests/state/test_auto_persist_phase2.py',
    'packages/core/tests/state/test_auto_naming.py',
]

# Ordered replacements (order matters!)
REPLACEMENTS = [
    # DDL constant names
    ('SCENARIO_ENTITIES_SEQ_DDL', 'COHORT_ENTITIES_SEQ_DDL'),
    ('SCENARIO_TAGS_SEQ_DDL', 'COHORT_TAGS_SEQ_DDL'),
    ('SCENARIOS_DDL', 'COHORTS_DDL'),
    ('SCENARIO_ENTITIES_DDL', 'COHORT_ENTITIES_DDL'),
    ('SCENARIO_TAGS_DDL', 'COHORT_TAGS_DDL'),
    
    # Class names
    ('ScenarioBrief', 'CohortBrief'),
    ('ScenarioSummary', 'CohortSummary'),
    ('TestScenarioSummary', 'TestCohortSummary'),
    ('TestGetScenarioByName', 'TestGetCohortByName'),
    ('TestMigrateScenario', 'TestMigrateCohort'),
    ('TestScenarioCloning', 'TestCohortCloning'),
    ('TestScenarioMerging', 'TestCohortMerging'),
    
    # Method/function names
    ('get_patients_in_scenario', 'get_patients_in_cohort'),
    ('get_scenario_summary', 'get_cohort_summary'),
    ('get_scenario_by_name', 'get_cohort_by_name'),
    ('list_scenarios', 'list_cohorts'),
    ('scenario_exists', 'cohort_exists'),
    ('query_scenario', 'query_cohort'),
    ('rename_scenario', 'rename_cohort'),
    ('save_scenario', 'save_cohort'),
    ('load_scenario', 'load_cohort'),
    ('delete_scenario', 'delete_cohort'),
    ('clone_scenario', 'clone_cohort'),
    ('merge_scenarios', 'merge_cohorts'),
    ('generate_scenario_name', 'generate_cohort_name'),
    ('export_scenario', 'export_cohort'),
    ('_create_scenario', '_create_cohort'),
    ('_get_scenario_info', '_get_cohort_info'),
    ('_update_scenario_timestamp', '_update_cohort_timestamp'),
    ('get_scenario_tags', 'get_cohort_tags'),
    ('add_scenario_tags', 'add_cohort_tags'),
    
    # SQL table/sequence names (must be after function renames)
    ('scenario_entities_seq', 'cohort_entities_seq'),
    ('scenario_tags_seq', 'cohort_tags_seq'),
    ('scenario_entities', 'cohort_entities'),
    ('scenario_tags', 'cohort_tags'),
    
    # Variable/parameter names
    ('source_scenario_id', 'source_cohort_id'),
    ('source_scenario_name', 'source_cohort_name'),
    ('target_scenario_id', 'target_cohort_id'),
    ('target_scenario_name', 'target_cohort_name'),
    ('new_scenario_id', 'new_cohort_id'),
    ('new_scenario_name', 'new_cohort_name'),
    ('is_new_scenario', 'is_new_cohort'),
    ('scenario_id', 'cohort_id'),
    ('scenario_name', 'cohort_name'),
    
    # SQL table reference patterns (FROM, INTO, JOIN, etc.)
    ('FROM scenarios', 'FROM cohorts'),
    ('INTO scenarios', 'INTO cohorts'),
    ('UPDATE scenarios', 'UPDATE cohorts'),
    ('JOIN scenarios', 'JOIN cohorts'),
    ("'scenarios'", "'cohorts'"),
    ('"scenarios"', '"cohorts"'),
    
    # Index names
    ('idx_scenario_', 'idx_cohort_'),
    ('idx_se_', 'idx_ce_'),
    ('idx_st_', 'idx_ct_'),
    
    # Docstrings and comments (general)
    ('Scenario ', 'Cohort '),
    ('scenario ', 'cohort '),
    ('scenarios ', 'cohorts '),
    ('Scenarios ', 'Cohorts '),
]

def refactor_file(filepath: Path, dry_run: bool = False) -> dict:
    """Apply replacements to a single file."""
    if not filepath.exists():
        return {'file': str(filepath), 'error': 'File not found', 'changed': False}
    
    content = filepath.read_text()
    original = content
    changes = []
    
    for old, new in REPLACEMENTS:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            changes.append(f"  {old} -> {new} ({count}x)")
    
    result = {
        'file': str(filepath.relative_to(PROJECT_ROOT)),
        'changed': content != original,
        'changes': changes,
        'change_count': len(changes)
    }
    
    if content != original and not dry_run:
        filepath.write_text(content)
        result['written'] = True
    
    return result

def main(dry_run: bool = True):
    """Run refactoring."""
    
    print(f"Cohort Refactoring - Phase 1+2 {'(DRY RUN)' if dry_run else ''}")
    print("=" * 70)
    
    total_files = 0
    total_changes = 0
    
    for rel_path in FILES:
        filepath = PROJECT_ROOT / rel_path
        result = refactor_file(filepath, dry_run)
        
        if result.get('error'):
            print(f"\n❌ {result['file']}: {result['error']}")
        elif result.get('changed'):
            total_files += 1
            total_changes += result['change_count']
            print(f"\n✓ {result['file']} ({result['change_count']} replacement types)")
            for change in result['changes'][:5]:  # Show first 5
                print(change)
            if len(result['changes']) > 5:
                print(f"  ... and {len(result['changes']) - 5} more")
        else:
            print(f"\n○ {result['file']}: No changes needed")
    
    print(f"\n{'=' * 70}")
    print(f"Files changed: {total_files}")
    print(f"Total replacement types: {total_changes}")
    
    if dry_run:
        print("\nThis was a DRY RUN. Run with --apply to make changes.")
    else:
        print("\n✅ Changes applied successfully.")

if __name__ == '__main__':
    import sys
    dry_run = '--apply' not in sys.argv
    main(dry_run)
