# Session 07: Testing & Polish

**Initiative**: DuckDB Unified Data Architecture  
**Phase**: 1 - Foundation (Final Session)  
**Estimated Duration**: 60-90 minutes  
**Prerequisites**: SESSION-01 through SESSION-06 complete

---

## Objective

Perform comprehensive integration testing, fix any issues discovered, ensure all tests pass, and prepare for Phase 1 completion. This is the final quality gate before declaring Phase 1 complete.

---

## Context

All code and documentation changes are complete. This session focuses on:
1. End-to-end integration testing
2. Running the full test suite
3. Fixing any discovered issues
4. Performance validation
5. Final cleanup and polish

---

## Pre-Flight Checklist

- [ ] All previous sessions (01-06) complete
- [ ] All code changes committed
- [ ] Documentation updated
- [ ] Git status clean

---

## Deliverables

### 1. Passing Test Suite

All 476+ existing tests plus new tests pass.

### 2. Integration Test Results

End-to-end workflows validated.

### 3. Performance Benchmarks

Database operations meet performance targets.

### 4. Issue Resolution

All discovered issues fixed.

### 5. Clean Git History

Final commit with Phase 1 complete.

---

## Implementation Steps

### Step 1: Run Full Test Suite

```bash
cd packages/core
source .venv/bin/activate

# Run all tests with verbose output
pytest tests/ -v --tb=short

# If any fail, note them and continue to categorize
```

**Expected Results:**
- All existing tests pass (476+)
- All new database tests pass
- All new state management tests pass
- All new migration tests pass

### Step 2: Integration Test Cohorts

Test complete workflows end-to-end:

#### Cohort A: Fresh Installation

```bash
# Remove existing database
rm -f ~/.healthsim/healthsim.duckdb

# Start Python, trigger database creation
python -c "from healthsim.db import get_connection; c = get_connection(); print('DB created')"

# Verify database exists and has tables
python -c "
from healthsim.db import get_connection
conn = get_connection()
tables = conn.execute(\"\"\"
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'main'
\"\"\").fetchall()
print(f'Tables created: {len(tables)}')
for t in tables[:10]:
    print(f'  - {t[0]}')
"
```

#### Cohort B: Save/Load Cycle

```python
# test_integration_save_load.py
from healthsim.state import save_cohort, load_cohort, list_cohorts

# Create test data
test_entities = {
    'patient': [{
        'patient_id': '11111111-1111-1111-1111-111111111111',
        'given_name': 'Integration',
        'family_name': 'Test',
        'date_of_birth': '1985-06-15',
        'gender': 'male'
    }],
    'encounter': [{
        'encounter_id': '22222222-2222-2222-2222-222222222222',
        'patient_id': '11111111-1111-1111-1111-111111111111',
        'encounter_type': 'outpatient',
        'admit_datetime': '2024-01-15T09:00:00'
    }]
}

# Save
cohort_id = save_cohort(
    'integration-test',
    test_entities,
    description='Integration test cohort',
    tags=['test', 'integration']
)
print(f"Saved cohort: {cohort_id}")

# List
cohorts = list_cohorts()
print(f"Found {len(cohorts)} cohorts")
assert any(s['name'] == 'integration-test' for s in cohorts)

# Load
loaded = load_cohort('integration-test')
assert loaded['name'] == 'integration-test'
assert len(loaded['entities']['patient']) == 1
assert loaded['entities']['patient'][0]['given_name'] == 'Integration'
print("✓ Save/Load cycle passed")
```

#### Cohort C: JSON Export/Import

```python
# test_integration_json.py
from pathlib import Path
from healthsim.state.manager import StateManager

manager = StateManager()

# Create cohort
manager.save_cohort('export-test', {
    'patient': [{'given_name': 'Export', 'family_name': 'Test'}]
})

# Export
export_path = Path('/tmp/export-test.json')
result_path = manager.export_to_json('export-test', export_path)
assert result_path.exists()
print(f"✓ Exported to {result_path}")

# Delete from database
manager.delete_cohort('export-test')

# Import
manager.import_from_json(export_path, name='reimported-test')

# Verify
loaded = manager.load_cohort('reimported-test')
assert loaded['entities']['patient'][0]['given_name'] == 'Export'
print("✓ JSON Export/Import passed")

# Cleanup
export_path.unlink()
manager.delete_cohort('reimported-test')
```

#### Cohort D: PopulationSim Reference Data

```python
# test_integration_populationsim.py
from healthsim.db import get_connection

conn = get_connection()

# Check reference tables exist
tables = conn.execute("""
    SELECT table_name FROM information_schema.tables
    WHERE table_name LIKE 'ref_%'
""").fetchall()
print(f"Reference tables: {[t[0] for t in tables]}")

# Query CDC PLACES data
result = conn.execute("""
    SELECT state_abbr, COUNT(*) as tract_count
    FROM ref_cdc_places_tract
    GROUP BY state_abbr
    ORDER BY tract_count DESC
    LIMIT 5
""").fetchall()
print("Top 5 states by tract count:")
for row in result:
    print(f"  {row[0]}: {row[1]:,}")

# Query by specific location
sd_diabetes = conn.execute("""
    SELECT AVG(diabetes_crude_prev) as avg_diabetes
    FROM ref_cdc_places_tract
    WHERE county_fips = '06073'
""").fetchone()
print(f"San Diego County avg diabetes prevalence: {sd_diabetes[0]:.1f}%")

print("✓ PopulationSim reference data passed")
```

#### Cohort E: Migration Tool

```bash
# Test migration dry run (if you have legacy JSON cohorts)
python scripts/migrate_json_to_duckdb.py --dry-run
```

### Step 3: Performance Testing

```python
# test_performance.py
import time
from healthsim.state.manager import StateManager
from healthsim.db import get_connection

manager = StateManager()
conn = get_connection()

# Test: Save 100 patients
print("Performance: Saving 100 patients...")
patients = [
    {'patient_id': f'perf-{i}', 'given_name': f'Patient{i}', 'family_name': 'Test'}
    for i in range(100)
]

start = time.time()
manager.save_cohort('perf-test', {'patient': patients}, overwrite=True)
save_time = time.time() - start
print(f"  Save time: {save_time:.2f}s ({100/save_time:.0f} patients/sec)")

# Test: Load cohort
start = time.time()
loaded = manager.load_cohort('perf-test')
load_time = time.time() - start
print(f"  Load time: {load_time:.2f}s")

# Test: List cohorts
start = time.time()
for _ in range(100):
    manager.list_cohorts()
list_time = time.time() - start
print(f"  List 100x: {list_time:.2f}s ({list_time/100*1000:.1f}ms/call)")

# Test: Reference data query
start = time.time()
for _ in range(100):
    conn.execute("SELECT * FROM ref_cdc_places_tract WHERE county_fips = '06073'").fetchall()
query_time = time.time() - start
print(f"  Reference query 100x: {query_time:.2f}s ({query_time/100*1000:.1f}ms/call)")

# Cleanup
manager.delete_cohort('perf-test')

# Performance targets
assert save_time < 5.0, "Save too slow"
assert load_time < 2.0, "Load too slow"
assert list_time < 1.0, "List too slow"
assert query_time < 1.0, "Query too slow"
print("✓ All performance targets met")
```

### Step 4: Fix Discovered Issues

For each issue found:

1. **Document the issue**
   ```markdown
   ## Issue: [Description]
   - Found in: [Test/Cohort]
   - Symptom: [What went wrong]
   - Root cause: [Why]
   - Fix: [What to change]
   ```

2. **Implement the fix**

3. **Add a regression test**

4. **Re-run affected tests**

### Step 5: Database Size Verification

```bash
# Check database size
ls -lh ~/.healthsim/healthsim.duckdb

# Should be approximately:
# - Empty (no cohorts): ~25-30 MB (reference data only)
# - With cohorts: grows based on entity count
```

Compare to previous CSV size:
```bash
# If CSVs still exist
du -sh skills/populationsim/data/
# Expected: ~148 MB

# DuckDB should be ~5-7x smaller for reference data
```

### Step 6: Run Linting/Code Quality

```bash
# If using ruff or similar
ruff check packages/core/healthsim/

# If using mypy
mypy packages/core/healthsim/
```

### Step 7: Final Test Run

```bash
# Clean run of all tests
cd packages/core
pytest tests/ -v --tb=short 2>&1 | tee test_results.txt

# Count results
grep -E "passed|failed|error" test_results.txt | tail -1
```

### Step 8: Git Status Check

```bash
# Ensure everything is committed
git status

# Should show:
# On branch main (or feature branch)
# nothing to commit, working tree clean
```

### Step 9: Create Phase 1 Summary

Update MASTER-PLAN.md with completion summary:

```markdown
## Phase 1: Foundation - COMPLETE ✅

**Completed**: [Date]

### Summary

Phase 1 successfully migrated HealthSim to DuckDB-based storage:

- **Database Module**: `packages/core/healthsim/db/`
- **State Management**: DuckDB backend with same MCP interface
- **Reference Data**: 148 MB CSV → ~25 MB DuckDB
- **JSON Support**: Export/import preserved for sharing
- **Migration Tool**: Converts legacy JSON cohorts
- **Documentation**: Fully updated

### Metrics

- Tests: XXX passed, 0 failed
- Database size: XX MB (vs 148 MB CSV)
- Performance: Meets all targets

### Sessions Completed

| Session | Commit | Date |
|---------|--------|------|
| 01 - Foundation | XXXXXX | YYYY-MM-DD |
| 02 - PopulationSim | XXXXXX | YYYY-MM-DD |
| 03 - State Management | XXXXXX | YYYY-MM-DD |
| 04 - JSON Compatibility | XXXXXX | YYYY-MM-DD |
| 05 - Migration Tool | XXXXXX | YYYY-MM-DD |
| 06 - Documentation | XXXXXX | YYYY-MM-DD |
| 07 - Testing & Polish | XXXXXX | YYYY-MM-DD |
```

---

## Post-Flight Checklist

- [ ] All tests pass (including new tests)
- [ ] Integration cohorts all pass
- [ ] Performance meets targets
- [ ] No known issues remaining
- [ ] Database size as expected
- [ ] Code quality checks pass
- [ ] Git history clean
- [ ] MASTER-PLAN.md updated with completion
- [ ] CHANGELOG.md finalized
- [ ] CURRENT-WORK.md updated

---

## Final Commit

```bash
git add -A
git commit -m "[Phase1] Complete DuckDB Unified Data Architecture - Phase 1

Phase 1 Summary:
- DuckDB-based state management (replacing JSON files)
- PopulationSim reference data in DuckDB (~5x compression)
- JSON export/import for cohort sharing
- Migration tool for existing cohorts
- Full documentation update

All tests passing. Ready for Phase 2 (Analytics Layer).

Part of: DuckDB Unified Data Architecture initiative"

git push

# Tag the release
git tag -a v0.X.0-duckdb-phase1 -m "DuckDB Architecture Phase 1 Complete"
git push origin v0.X.0-duckdb-phase1
```

---

## Update MASTER-PLAN.md

Mark SESSION-07 and entire Phase 1 as complete.

---

## Success Criteria

✅ Phase 1 complete when:
1. All tests pass (476+ existing + new tests)
2. All integration cohorts pass
3. Performance targets met
4. Database size ~5-7x smaller than CSV
5. Documentation complete and accurate
6. No known issues
7. Tagged and pushed

---

## Phase 2 Preview

With Phase 1 complete, Phase 2 will add:
- Star schema analytics layer
- Canonical → Star transformation
- Batch generation mode
- Analytics MCP tools

See MASTER-PLAN.md for Phase 2 session outlines.

---

## Celebration 🎉

Phase 1 represents a significant architectural improvement:
- **Scalable**: Ready for 10,000+ entity cohorts
- **Queryable**: SQL access to all data
- **Efficient**: 5-7x storage reduction
- **Cloud-Ready**: MotherDuck path established
- **Maintainable**: Single database vs scattered files

Great work completing this initiative!
