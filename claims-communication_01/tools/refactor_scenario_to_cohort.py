#!/usr/bin/env python3
"""
Cohort Refactoring Script

Systematically renames scenario -> cohort throughout the codebase.
Run with --dry-run first to see what would change.

Usage:
    python refactor_scenario_to_cohort.py --phase 1 --dry-run
    python refactor_scenario_to_cohort.py --phase 1
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import argparse

# Base path
BASE_PATH = Path(__file__).parent.parent

# Replacement mappings by category
SQL_REPLACEMENTS = [
    # Table names in SQL
    ('FROM scenarios', 'FROM cohorts'),
    ('INTO scenarios', 'INTO cohorts'),
    ('UPDATE scenarios', 'UPDATE cohorts'),
    ('JOIN scenarios', 'JOIN cohorts'),
    ('FROM scenario_entities', 'FROM cohort_entities'),
    ('INTO scenario_entities', 'INTO cohort_entities'),
    ('FROM scenario_tags', 'FROM cohort_tags'),
    ('INTO scenario_tags', 'INTO cohort_tags'),
    # Column names
    ('scenario_id =', 'cohort_id ='),
    ('scenario_id,', 'cohort_id,'),
    ('scenario_id)', 'cohort_id)'),
    ('.scenario_id', '.cohort_id'),
    ("'scenario_id'", "'cohort_id'"),
    ('"scenario_id"', '"cohort_id"'),
]

SCHEMA_REPLACEMENTS = [
    # DDL constants
    ('SCENARIOS_DDL', 'COHORTS_DDL'),
    ('SCENARIO_ENTITIES_DDL', 'COHORT_ENTITIES_DDL'),
    ('SCENARIO_TAGS_DDL', 'COHORT_TAGS_DDL'),
    ('SCENARIO_ENTITIES_SEQ_DDL', 'COHORT_ENTITIES_SEQ_DDL'),
    ('SCENARIO_TAGS_SEQ_DDL', 'COHORT_TAGS_SEQ_DDL'),
    # Table definitions
    ('CREATE TABLE scenarios', 'CREATE TABLE cohorts'),
    ('CREATE TABLE scenario_entities', 'CREATE TABLE cohort_entities'),
    ('CREATE TABLE scenario_tags', 'CREATE TABLE cohort_tags'),
    ('CREATE SEQUENCE scenario_entities_seq', 'CREATE SEQUENCE cohort_entities_seq'),
    ('CREATE SEQUENCE scenario_tags_seq', 'CREATE SEQUENCE cohort_tags_seq'),
    # Index names
    ('idx_scenario_', 'idx_cohort_'),
    ('idx_scenarios_', 'idx_cohorts_'),
    # State tables list
    ("'scenarios'", "'cohorts'"),
    ("'scenario_entities'", "'cohort_entities'"),
    ("'scenario_tags'", "'cohort_tags'"),
]

CLASS_METHOD_REPLACEMENTS = [
    # Classes
    ('class ScenarioSummary', 'class CohortSummary'),
    ('class ScenarioBrief', 'class CohortBrief'),
    ('ScenarioSummary', 'CohortSummary'),
    ('ScenarioBrief', 'CohortBrief'),
    # Method names
    ('def list_scenarios', 'def list_cohorts'),
    ('def get_scenario_summary', 'def get_cohort_summary'),
    ('def query_scenario', 'def query_cohort'),
    ('def rename_scenario', 'def rename_cohort'),
    ('def clone_scenario', 'def clone_cohort'),
    ('def merge_scenarios', 'def merge_cohorts'),
    ('def delete_scenario', 'def delete_cohort'),
    ('def save_scenario', 'def save_cohort'),
    ('def load_scenario', 'def load_cohort'),
    ('def _create_scenario', 'def _create_cohort'),
    ('def _get_scenario_info', 'def _get_cohort_info'),
    ('def _update_scenario_timestamp', 'def _update_cohort_timestamp'),
    ('def export_scenario', 'def export_cohort'),
    ('def get_scenario_tags', 'def get_cohort_tags'),
    ('def add_scenario_tags', 'def add_cohort_tags'),
    ('def scenario_exists', 'def cohort_exists'),
    ('def generate_scenario_name', 'def generate_cohort_name'),
    ('def get_scenario_by_name', 'def get_cohort_by_name'),
    # Function calls
    ('list_scenarios(', 'list_cohorts('),
    ('get_scenario_summary(', 'get_cohort_summary('),
    ('query_scenario(', 'query_cohort('),
    ('rename_scenario(', 'rename_cohort('),
    ('clone_scenario(', 'clone_cohort('),
    ('merge_scenarios(', 'merge_cohorts('),
    ('delete_scenario(', 'delete_cohort('),
    ('_create_scenario(', '_create_cohort('),
    ('_get_scenario_info(', '_get_cohort_info('),
    ('_update_scenario_timestamp(', '_update_cohort_timestamp('),
    ('export_scenario(', 'export_cohort('),
    ('get_scenario_tags(', 'get_cohort_tags('),
    ('add_scenario_tags(', 'add_cohort_tags('),
    ('scenario_exists(', 'cohort_exists('),
    ('generate_scenario_name(', 'generate_cohort_name('),
    ('get_scenario_by_name(', 'get_cohort_by_name('),
]

VARIABLE_REPLACEMENTS = [
    # Dataclass fields and variables
    ('scenario_id:', 'cohort_id:'),
    ('scenario_name:', 'cohort_name:'),
    ('source_scenario_id:', 'source_cohort_id:'),
    ('source_scenario_name:', 'source_cohort_name:'),
    ('new_scenario_id:', 'new_cohort_id:'),
    ('new_scenario_name:', 'new_cohort_name:'),
    ('target_scenario_id:', 'target_cohort_id:'),
    ('target_scenario_name:', 'target_cohort_name:'),
    ('is_new_scenario:', 'is_new_cohort:'),
    # Parameter names
    ('scenario_id=', 'cohort_id='),
    ('scenario_name=', 'cohort_name='),
    ('scenario_id,', 'cohort_id,'),
    ('scenario_name,', 'cohort_name,'),
    ('scenario_id)', 'cohort_id)'),
    ('scenario_name)', 'cohort_name)'),
    # Variable assignments
    ('scenario_id =', 'cohort_id ='),
    ('scenario_name =', 'cohort_name ='),
    # Dictionary keys
    ("'scenario_id':", "'cohort_id':"),
    ("'scenario_name':", "'cohort_name':"),
    ("'is_new_scenario':", "'is_new_cohort':"),
    ("'source_scenario_id':", "'source_cohort_id':"),
    ("'source_scenario_name':", "'source_cohort_name':"),
    ("'new_scenario_id':", "'new_cohort_id':"),
    ("'new_scenario_name':", "'new_cohort_name':"),
    ("'target_scenario_id':", "'target_cohort_id':"),
    ("'target_scenario_name':", "'target_cohort_name':"),
    # f-string and format references
    ('{scenario_id}', '{cohort_id}'),
    ('{scenario_name}', '{cohort_name}'),
]

QUERY_FUNCTION_REPLACEMENTS = [
    ('def get_patients_in_scenario', 'def get_patients_in_cohort'),
    ('def get_scenario_summary', 'def get_cohort_summary'),
    ('def list_scenarios', 'def list_cohorts'),
    ('def scenario_exists', 'def cohort_exists'),
    ('get_patients_in_scenario', 'get_patients_in_cohort'),
]


def apply_replacements(content: str, replacements: List[Tuple[str, str]]) -> Tuple[str, List[str]]:
    """Apply replacements and return new content + list of changes made."""
    changes = []
    for old, new in replacements:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            changes.append(f"  {old} -> {new} ({count}x)")
    return content, changes


def process_file(filepath: Path, replacements: List[Tuple[str, str]], dry_run: bool = True) -> Dict:
    """Process a single file with the given replacements."""
    result = {
        'file': str(filepath),
        'changes': [],
        'error': None
    }
    
    try:
        content = filepath.read_text()
        new_content, changes = apply_replacements(content, replacements)
        
        if changes:
            result['changes'] = changes
            if not dry_run:
                filepath.write_text(new_content)
                
    except Exception as e:
        result['error'] = str(e)
    
    return result


def phase1_database_schema(dry_run: bool = True) -> List[Dict]:
    """Phase 1: Database schema changes."""
    results = []
    
    # schema.py - DDL and table definitions
    schema_file = BASE_PATH / 'packages/core/src/healthsim/db/schema.py'
    results.append(process_file(
        schema_file,
        SCHEMA_REPLACEMENTS + SQL_REPLACEMENTS,
        dry_run
    ))
    
    # queries.py - Query functions
    queries_file = BASE_PATH / 'packages/core/src/healthsim/db/queries.py'
    results.append(process_file(
        queries_file,
        SQL_REPLACEMENTS + QUERY_FUNCTION_REPLACEMENTS + VARIABLE_REPLACEMENTS,
        dry_run
    ))
    
    # __init__.py - exports
    init_file = BASE_PATH / 'packages/core/src/healthsim/db/__init__.py'
    results.append(process_file(
        init_file,
        QUERY_FUNCTION_REPLACEMENTS,
        dry_run
    ))
    
    return results


def phase2_core_python(dry_run: bool = True) -> List[Dict]:
    """Phase 2: Core Python state management."""
    results = []
    
    state_files = [
        'manager.py',
        'auto_persist.py', 
        'auto_naming.py',
        'summary.py',
        'serializers.py',
        'workspace.py',
        'legacy.py',
        '__init__.py',
    ]
    
    all_replacements = (
        SQL_REPLACEMENTS + 
        CLASS_METHOD_REPLACEMENTS + 
        VARIABLE_REPLACEMENTS +
        SCHEMA_REPLACEMENTS
    )
    
    for filename in state_files:
        filepath = BASE_PATH / f'packages/core/src/healthsim/state/{filename}'
        if filepath.exists():
            results.append(process_file(filepath, all_replacements, dry_run))
    
    return results


def print_results(results: List[Dict], phase_name: str):
    """Print results in a readable format."""
    print(f"\n{'='*60}")
    print(f"Phase: {phase_name}")
    print('='*60)
    
    total_changes = 0
    for result in results:
        if result['error']:
            print(f"\n❌ {result['file']}")
            print(f"   Error: {result['error']}")
        elif result['changes']:
            print(f"\n✅ {result['file']}")
            for change in result['changes']:
                print(change)
            total_changes += len(result['changes'])
        else:
            print(f"\n⬜ {result['file']} (no changes needed)")
    
    print(f"\n{'='*60}")
    print(f"Total changes: {total_changes}")
    print('='*60)


def main():
    parser = argparse.ArgumentParser(description='Refactor scenario to cohort')
    parser.add_argument('--phase', type=int, required=True, choices=[1, 2, 3],
                        help='Phase to execute (1=schema, 2=core python, 3=mcp)')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='Show what would change without making changes')
    args = parser.parse_args()
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made\n")
    else:
        print("\n⚠️  LIVE MODE - Changes will be written to files\n")
    
    if args.phase == 1:
        results = phase1_database_schema(args.dry_run)
        print_results(results, "Database Schema")
    elif args.phase == 2:
        results = phase2_core_python(args.dry_run)
        print_results(results, "Core Python")
    else:
        print("Phase 3 not yet implemented")
        sys.exit(1)


if __name__ == '__main__':
    main()
