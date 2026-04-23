#!/usr/bin/env python3
"""Refactor scenario -> cohort in queries.py"""

filepath = '/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src/healthsim/db/queries.py'

with open(filepath, 'r') as f:
    content = f.read()

# Function names
content = content.replace('def get_patients_in_scenario', 'def get_patients_in_cohort')
content = content.replace('def get_scenario_summary', 'def get_cohort_summary')
content = content.replace('def list_scenarios', 'def list_cohorts')
content = content.replace('def scenario_exists', 'def cohort_exists')

# Parameters
content = content.replace('scenario_id: str', 'cohort_id: str')
content = content.replace('scenario_id: Optional[str]', 'cohort_id: Optional[str]')
content = content.replace('[scenario_id]', '[cohort_id]')
content = content.replace('if scenario_id:', 'if cohort_id:')

# SQL table/column references
content = content.replace('JOIN scenario_entities', 'JOIN cohort_entities')
content = content.replace('FROM scenario_entities', 'FROM cohort_entities')
content = content.replace('WHERE se.scenario_id', 'WHERE se.cohort_id')
content = content.replace('WHERE scenario_id', 'WHERE cohort_id')
content = content.replace('FROM scenarios', 'FROM cohorts')
content = content.replace('ON s.scenario_id', 'ON s.id')  # fix join - cohorts uses 'id' not 'scenario_id'
content = content.replace('= t.scenario_id', '= t.cohort_id')
content = content.replace('FROM scenario_tags', 'FROM cohort_tags')

# Docstrings
content = content.replace('scenario identifier', 'cohort identifier')
content = content.replace('scenario to filter', 'cohort to filter')
content = content.replace('associated with a scenario', 'associated with a cohort')
content = content.replace('Get a summary of a scenario', 'Get a summary of a cohort')
content = content.replace('scenario not found', 'cohort not found')
content = content.replace('List all scenarios', 'List all cohorts')
content = content.replace('scenario summary', 'cohort summary')
content = content.replace('if a scenario', 'if a cohort')
content = content.replace('Scenario name', 'Cohort name')
content = content.replace('scenario exists', 'cohort exists')
content = content.replace('optionally filtered by scenario', 'optionally filtered by cohort')

# Variable names in code
content = content.replace('# Get scenario metadata', '# Get cohort metadata')
content = content.replace('scenario = conn.execute', 'cohort = conn.execute')
content = content.replace('if not scenario:', 'if not cohort:')
content = content.replace('columns, scenario', 'columns, cohort')

with open(filepath, 'w') as f:
    f.write(content)

print("queries.py refactored")
