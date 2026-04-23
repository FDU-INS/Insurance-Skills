# p1-01: Full MotherDuck Data Migration

## What to build

Extend `scripts/migrate_to_motherduck.py` to migrate ALL reference data from the local DuckDB to MotherDuck. This replaces the Phase 0 sample with the complete dataset.

## Context

In Phase 0 we migrated 1,000 NPPES rows and a couple of small tables. Now we need the full dataset: ~8.9M NPPES providers, CDC PLACES, SVI, FIPS crosswalks, all reference code tables, and the cohort schema.

## Tasks

1. **Read the local DuckDB schema** to get the complete inventory:
   ```sql
   SELECT table_schema, table_name, 
          estimated_size as est_rows
   FROM information_schema.tables 
   WHERE table_schema != 'information_schema'
   ORDER BY table_schema, table_name
   ```

2. **Implement the `--full` flag** in `scripts/migrate_to_motherduck.py`. When `--full` is passed:

   a. Drop and recreate the Phase 0 sample tables (replace them with full data)
   
   b. Migrate all reference data tables. For the NPPES table (~8.9M rows), migrate in batches of 500K rows to avoid memory issues:
   ```python
   batch_size = 500_000
   offset = 0
   while True:
       batch = local_conn.execute(
           f"SELECT * FROM {table} LIMIT {batch_size} OFFSET {offset}"
       ).fetchdf()
       if len(batch) == 0:
           break
       # Insert batch into MotherDuck
       md_conn.execute(f"INSERT INTO {target_table} SELECT * FROM batch")
       offset += batch_size
       print(f"  Migrated {offset} rows...")
   ```
   
   c. Create the cohort schema tables (empty — these are populated at runtime by the generation engine):
      - `cohort.cohorts`
      - `cohort.cohort_entities`
      - `cohort.cohort_metadata`
      Match the schemas from the local DuckDB exactly.
   
   d. Create the runtime schema for session tracking (empty).
   
   e. Print a summary: table name, local row count, MotherDuck row count, match status.

3. **Add a `--verify` flag** that only checks row counts between local and MotherDuck without migrating. Useful for spot-checking after migration.

4. **Run the full migration**:
   ```bash
   .venv/bin/python scripts/migrate_to_motherduck.py --full
   ```
   This may take 10-30 minutes depending on network speed (the NPPES table is large).

5. **Verify via MotherDuck UI**: Log into app.motherduck.com and confirm all tables exist with correct row counts.

6. **Run the verify check**:
   ```bash
   .venv/bin/python scripts/migrate_to_motherduck.py --verify
   ```

7. **Git commit**: "feat: full MotherDuck data migration with batch loading"

## Deliverables

- Updated `scripts/migrate_to_motherduck.py` with `--full` and `--verify` flags
- All reference data migrated to MotherDuck
- Row counts verified matching
- Committed
