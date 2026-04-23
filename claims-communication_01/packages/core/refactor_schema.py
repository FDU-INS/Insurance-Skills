#!/usr/bin/env python3
"""Refactor scenario -> cohort in schema.py"""

import re

filepath = '/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src/healthsim/db/schema.py'

with open(filepath, 'r') as f:
    content = f.read()

# Track changes
original = content

# 1. Schema version
content = content.replace('SCHEMA_VERSION = "1.4"', 'SCHEMA_VERSION = "1.5"')

# 2. Provenance columns comment and field
content = content.replace('scenario_id         VARCHAR,   -- Links to scenarios table', 
                          'cohort_id           VARCHAR,   -- Links to cohorts table')

# 3. Sequence names (DDL variable names and SQL)
content = content.replace('SCENARIO_ENTITIES_SEQ_DDL', 'COHORT_ENTITIES_SEQ_DDL')
content = content.replace('SCENARIO_TAGS_SEQ_DDL', 'COHORT_TAGS_SEQ_DDL')
content = content.replace("scenario_entities_seq", "cohort_entities_seq")
content = content.replace("scenario_tags_seq", "cohort_tags_seq")

# 4. Table DDL variable names
content = content.replace('SCENARIOS_DDL', 'COHORTS_DDL')
content = content.replace('SCENARIO_ENTITIES_DDL', 'COHORT_ENTITIES_DDL')
content = content.replace('SCENARIO_TAGS_DDL', 'COHORT_TAGS_DDL')

# 5. Table names in SQL
content = content.replace('CREATE TABLE IF NOT EXISTS scenarios', 'CREATE TABLE IF NOT EXISTS cohorts')
content = content.replace('CREATE TABLE IF NOT EXISTS scenario_entities', 'CREATE TABLE IF NOT EXISTS cohort_entities')
content = content.replace('CREATE TABLE IF NOT EXISTS scenario_tags', 'CREATE TABLE IF NOT EXISTS cohort_tags')
content = content.replace('REFERENCES scenarios(id)', 'REFERENCES cohorts(id)')

# 6. Column name scenario_id -> cohort_id (in table definitions)
content = content.replace('scenario_id     VARCHAR NOT NULL REFERENCES', 'cohort_id       VARCHAR NOT NULL REFERENCES')
content = content.replace('UNIQUE(scenario_id, entity_type, entity_id)', 'UNIQUE(cohort_id, entity_type, entity_id)')
content = content.replace('UNIQUE(scenario_id, tag)', 'UNIQUE(cohort_id, tag)')

# 7. Index names - use regex for all idx_*_scenario patterns
content = re.sub(r'idx_(\w+)_scenario_', r'idx_\1_cohort_', content)
content = re.sub(r'idx_scenario_', r'idx_cohort_', content)

# 8. Comments
content = content.replace('# STATE MANAGEMENT TABLES', '# STATE MANAGEMENT TABLES (Cohorts)')
content = content.replace('-- scenario_', '-- cohort_')

# 9. get_state_tables function
content = content.replace("'scenarios'", "'cohorts'")
content = content.replace("'scenario_entities'", "'cohort_entities'")  
content = content.replace("'scenario_tags'", "'cohort_tags'")

# Write back
with open(filepath, 'w') as f:
    f.write(content)

# Report
print(f"Replacements made:")
print(f"  - SCHEMA_VERSION: 1.4 -> 1.5")
print(f"  - scenario_id -> cohort_id in provenance")
print(f"  - Sequence names updated")
print(f"  - Table DDL names updated")
print(f"  - SQL table names updated")
print(f"  - Column names updated")
print(f"  - Index names updated")
print(f"  - State table list updated")
