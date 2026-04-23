# p0-03: MotherDuck Migration Script (Small Slice)

## What to build

Create a script that migrates a small slice of reference data from the local DuckDB file to MotherDuck. This validates the MotherDuck connection and query patterns before we migrate the full dataset in Phase 1.

## Context

The local `healthsim_current.duckdb` contains reference data including ~8.9M NPPES provider records, CDC PLACES health indicators, SVI social vulnerability data, FIPS crosswalks, and reference code tables. For Phase 0, we only need a small slice to prove the connection works.

The user has already created a MotherDuck account and has their token. It should be in the `.env` file as `MOTHERDUCK_TOKEN`.

## Tasks

1. **Create `scripts/migrate_to_motherduck.py`** that does the following:

   a. Load environment variables from `.env` (use `python-dotenv` — install if needed)
   
   b. Connect to the local DuckDB file (`healthsim_current.duckdb`) as a read source
   
   c. Connect to MotherDuck using the token: `duckdb.connect('md:healthsim_ref')`
      - This creates a database called `healthsim_ref` in MotherDuck
   
   d. Create schemas in MotherDuck: `reference`, `cohort`, `runtime`
   
   e. For the Phase 0 spike, migrate only:
      - A 1,000-row sample from the NPPES providers table (SELECT * FROM ... LIMIT 1000)
      - The full FIPS crosswalk table (small)
      - One reference code table (pick the smallest one)
   
   f. Print row counts for each migrated table to verify
   
   g. Run a test query against MotherDuck to verify data is accessible:
      ```sql
      SELECT COUNT(*) as total, 
             COUNT(DISTINCT provider_state) as states
      FROM reference.nppes_sample
      ```

2. **Add a `--full` flag** to the script that will migrate ALL reference data (for Phase 1). For now, this flag should print "Full migration not yet implemented — use without --full for the Phase 0 sample." We'll implement it in Phase 1.

3. **Test the script**:
   ```bash
   source .env  # or use dotenv
   .venv/bin/python scripts/migrate_to_motherduck.py
   ```

   Verify:
   - The `healthsim_ref` database exists in MotherDuck (check via MotherDuck web UI)
   - The three tables exist with correct row counts
   - The test query returns results

4. **Important**: First read the local DuckDB to discover the actual table names and schemas. Don't assume — the table names in the local database may not match what the migration plan documents say. Run:
   ```sql
   SELECT table_schema, table_name, estimated_size 
   FROM information_schema.tables 
   WHERE table_schema != 'information_schema'
   ORDER BY table_schema, table_name
   ```

5. **Git commit**: "feat: add MotherDuck migration script (Phase 0 sample)"

## Deliverables

- `scripts/migrate_to_motherduck.py` with sample migration
- Verified: MotherDuck database created with sample data
- Verified: queries work against MotherDuck
- Committed

## Do NOT

- Migrate the full dataset yet (that's Phase 1)
- Modify the local DuckDB file in any way
- Change the MCP server's connection logic yet (that's also Phase 1)
