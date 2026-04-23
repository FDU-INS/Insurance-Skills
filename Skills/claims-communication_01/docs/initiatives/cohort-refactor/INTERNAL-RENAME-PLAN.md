# Cohort Refactoring - Complete Internal Rename Plan

## Overview
Change ALL internal references from "scenario" to "cohort" for consistency.

## Files to Update (in order)

### 1. serializers.py (2 refs)
- [ ] Comments/docstrings only

### 2. auto_naming.py (16 refs)  
- [ ] Function: generate_scenario_name → generate_cohort_name
- [ ] Function: ensure_unique_name (check params)
- [ ] Variables/docstrings

### 3. summary.py (37 refs)
- [ ] Class: ScenarioSummary → CohortSummary
- [ ] Function: _get_entity_counts (scenario_id param)
- [ ] Function: _calculate_patient_statistics (scenario_id param)
- [ ] All variables named scenario*

### 4. auto_persist.py (241 refs) - MAJOR
- [ ] Class: ScenarioBrief → CohortBrief
- [ ] Class: PersistResult (scenario_id, scenario_name fields)
- [ ] Class: DeleteResult (scenario_id field)
- [ ] Class: CloneResult (source_scenario_id, new_scenario_id fields)
- [ ] Class: MergeResult (source_scenario_ids, target_scenario_id fields)
- [ ] Class: ExportResult (scenario_id field)
- [ ] Method: _create_scenario → _create_cohort
- [ ] Method: _update_scenario_timestamp → _update_cohort_timestamp
- [ ] Method: _get_scenario_info → _get_cohort_info
- [ ] Method: get_scenario_summary → get_cohort_summary
- [ ] Method: query_scenario → query_cohort
- [ ] Method: list_scenarios → list_cohorts
- [ ] Method: rename_scenario → rename_cohort
- [ ] Method: delete_scenario → delete_cohort
- [ ] Method: clone_scenario → clone_cohort
- [ ] Method: merge_scenarios → merge_cohorts
- [ ] Method: export_scenario → export_cohort
- [ ] Method: scenarios_by_tag → cohorts_by_tag
- [ ] All parameter names: scenario_id → cohort_id, scenario_name → cohort_name
- [ ] All variable names

### 5. manager.py (171 refs) - MAJOR
- [ ] Method: save_scenario → save_cohort
- [ ] Method: load_scenario → load_cohort
- [ ] Method: list_scenarios → list_cohorts
- [ ] Method: delete_scenario → delete_cohort
- [ ] Method: rename_scenario → rename_cohort
- [ ] Method: scenario_exists → cohort_exists
- [ ] Method: get_scenario_tags → get_cohort_tags
- [ ] Method: add_scenario_tags → add_cohort_tags
- [ ] Method: _get_scenario_by_name → _get_cohort_by_name
- [ ] Method: _get_scenario_by_id → _get_cohort_by_id
- [ ] Method: _load_scenario_entities → _load_cohort_entities
- [ ] Method: _delete_scenario_entities → _delete_cohort_entities
- [ ] Convenience functions at module level
- [ ] All parameters and variables

### 6. legacy.py (39 refs)
- [ ] Function: list_legacy_scenarios → list_legacy_cohorts
- [ ] Function: migrate_legacy_scenario → migrate_legacy_cohort
- [ ] Function: migrate_all_legacy_scenarios → migrate_all_legacy_cohorts
- [ ] Function: export_scenario_for_sharing → export_cohort_for_sharing
- [ ] All parameters and variables

### 7. __init__.py (32 refs)
- [ ] Update all exports to match new names
- [ ] Update __all__ list

### 8. db/migrate/json_cohorts.py
- [ ] Check for any remaining scenario references

### 9. MCP Server (healthsim_mcp.py)
- [ ] Update internal variable names
- [ ] Update AddEntitiesInput field names

### 10. Tests
- [ ] Update all test files for new method/class names

### 11. Skills Documentation
- [ ] Update any remaining scenario references

## Execution Strategy
1. Update each file completely
2. Run tests after each file
3. Commit after each successful file update
4. Push after all files complete
