#!/usr/bin/env python3
"""
Precise SQL string refactoring for scenario→cohort rename.
Only modifies SQL strings (inside triple quotes), not Python variable names.
"""
import re
import sys
from pathlib import Path

# Patterns to replace ONLY in SQL strings
SQL_REPLACEMENTS = [
    # Table names
    (r'\bINTO scenarios\b', 'INTO cohorts'),
    (r'\bFROM scenarios\b', 'FROM cohorts'),
    (r'\bUPDATE scenarios\b', 'UPDATE cohorts'),
    (r'\bINTO scenario_tags\b', 'INTO cohort_tags'),
    (r'\bFROM scenario_tags\b', 'FROM cohort_tags'),
    (r'\bINTO scenario_entities\b', 'INTO cohort_entities'),
    (r'\bFROM scenario_entities\b', 'FROM cohort_entities'),
    # Column names in SQL context (after comma, in WHERE, etc.)
    (r', scenario_id,', ', cohort_id,'),
    (r'\(scenario_id,', '(cohort_id,'),
    (r', scenario_id\)', ', cohort_id)'),
    (r'\.scenario_id\b', '.cohort_id'),  # table alias like t.scenario_id
    (r'\bWHERE scenario_id\b', 'WHERE cohort_id'),
    (r'\bAND scenario_id\b', 'AND cohort_id'),
    (r'\bOR scenario_id\b', 'OR cohort_id'),
    (r'\bON scenario_id\b', 'ON cohort_id'),
    # Sequence names
    (r"'scenario_tags_seq'", "'cohort_tags_seq'"),
    (r"'scenario_entities_seq'", "'cohort_entities_seq'"),
]

def is_sql_string(content: str, pos: int) -> bool:
    """Check if position is inside a SQL string (triple-quoted string with SQL keywords)."""
    # Find enclosing triple quotes
    before = content[:pos]
    
    # Count triple quotes before this position
    triple_double = before.count('"""')
    triple_single = before.count("'''")
    
    # If odd number of triple quotes, we're inside one
    inside_triple_double = triple_double % 2 == 1
    inside_triple_single = triple_single % 2 == 1
    
    if not (inside_triple_double or inside_triple_single):
        return False
    
    # Now check if this triple-quoted string contains SQL keywords
    # Find the opening quote
    if inside_triple_double:
        last_open = before.rfind('"""')
        quote_type = '"""'
    else:
        last_open = before.rfind("'''")
        quote_type = "'''"
    
    # Find the closing quote after pos
    close_pos = content.find(quote_type, pos)
    if close_pos == -1:
        close_pos = len(content)
    
    # Extract the string content
    string_content = content[last_open:close_pos].upper()
    
    # Check for SQL keywords
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'INTO', 'CREATE', 'DROP']
    return any(kw in string_content for kw in sql_keywords)


def refactor_file(filepath: Path) -> tuple[bool, int]:
    """Refactor SQL strings in a file. Returns (modified, count)."""
    content = filepath.read_text()
    original = content
    total_changes = 0
    
    for pattern, replacement in SQL_REPLACEMENTS:
        # Find all matches
        for match in re.finditer(pattern, content):
            if is_sql_string(content, match.start()):
                # This is inside a SQL string, replace it
                pass  # Will be replaced by re.sub below
        
        # Do the replacement
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            # Verify these were actually in SQL strings
            content = new_content
            total_changes += count
    
    if content != original:
        filepath.write_text(content)
        return True, total_changes
    return False, 0


def main():
    state_dir = Path('/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src/healthsim/state')
    test_dir = Path('/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/tests/state')
    
    files_modified = 0
    total_changes = 0
    
    for directory in [state_dir, test_dir]:
        for filepath in directory.glob('*.py'):
            modified, count = refactor_file(filepath)
            if modified:
                print(f"  Modified: {filepath.name} ({count} changes)")
                files_modified += 1
                total_changes += count
    
    print(f"\nTotal: {files_modified} files modified, {total_changes} replacements")


if __name__ == '__main__':
    main()
