# Session 02: PopulationSim Migration

**Initiative**: DuckDB Unified Data Architecture  
**Phase**: 1 - Foundation  
**Estimated Duration**: 45-60 minutes  
**Prerequisites**: SESSION-01 complete

---

## Objective

Migrate PopulationSim's 148MB of embedded CSV reference data to DuckDB tables, achieving ~5-7x compression while enabling SQL queries against CDC PLACES, SVI, and ADI datasets.

---

## Context

PopulationSim currently stores reference data as CSV files:
- CDC PLACES tract-level (~85,000 rows)
- CDC PLACES county-level (~3,200 rows)
- SVI tract-level (~85,000 rows)  
- SVI county-level (~3,200 rows)
- ADI block-group level (~242,000 rows)

These will be imported into the unified `healthsim.duckdb` as read-only reference tables.

### Reference Documents

```
docs/initiatives/duckdb-architecture/MASTER-PLAN.md
skills/populationsim/data/                              # Current CSV location
skills/populationsim/SKILL.md                           # PopulationSim skill
packages/core/healthsim/db/schema.py                    # From SESSION-01
```

---

## Pre-Flight Checklist

- [ ] SESSION-01 complete and committed
- [ ] Verify git status clean: `git status`
- [ ] Database module working: `python -c "from healthsim.db import get_connection; print(get_connection())"`
- [ ] Note current CSV file sizes for comparison

---

## Deliverables

### 1. Reference Data Loader

```
packages/core/healthsim/db/reference/
├── __init__.py
├── populationsim.py         # CSV to DuckDB importer
└── loader.py                # Generic reference data loading
```

### 2. Reference Table Schemas

Add to `schema.py`:
- `ref_cdc_places_tract`
- `ref_cdc_places_county`
- `ref_svi_tract`
- `ref_svi_county`
- `ref_adi_blockgroup`

### 3. Import Script

```
scripts/import_populationsim_data.py
```

### 4. Tests

```
packages/core/tests/db/test_reference_data.py
```

---

## Implementation Steps

### Step 1: Analyze Current CSV Structure

```bash
# Check current file sizes
ls -lh skills/populationsim/data/

# Sample headers
head -1 skills/populationsim/data/cdc_places_tract_2024.csv
head -1 skills/populationsim/data/svi_tract_2022.csv
head -1 skills/populationsim/data/adi_blockgroup_2021.csv
```

Document the exact column names and types for each CSV.

### Step 2: Add Reference Table Schemas

Update `packages/core/healthsim/db/schema.py` to include reference tables:

```python
# Reference Data Tables (PopulationSim)

REF_CDC_PLACES_TRACT_DDL = """
CREATE TABLE IF NOT EXISTS ref_cdc_places_tract (
    tract_fips          VARCHAR(11) PRIMARY KEY,
    state_abbr          VARCHAR(2),
    state_fips          VARCHAR(2),
    county_fips         VARCHAR(5),
    county_name         VARCHAR(100),
    total_population    INTEGER,
    
    -- Health measures (include all 40+ indicators)
    access2_crude_prev  DECIMAL(5,2),
    arthritis_crude_prev DECIMAL(5,2),
    binge_crude_prev    DECIMAL(5,2),
    bphigh_crude_prev   DECIMAL(5,2),
    cancer_crude_prev   DECIMAL(5,2),
    casthma_crude_prev  DECIMAL(5,2),
    chd_crude_prev      DECIMAL(5,2),
    copd_crude_prev     DECIMAL(5,2),
    diabetes_crude_prev DECIMAL(5,2),
    obesity_crude_prev  DECIMAL(5,2),
    -- ... add all columns from CSV
    
    -- Metadata
    data_release        VARCHAR(20),
    geolocation         VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_places_tract_county ON ref_cdc_places_tract(county_fips);
CREATE INDEX IF NOT EXISTS idx_places_tract_state ON ref_cdc_places_tract(state_abbr);
"""

# Similar DDL for ref_cdc_places_county, ref_svi_tract, ref_svi_county, ref_adi_blockgroup
```

### Step 3: Create Reference Data Loader

```python
# packages/core/healthsim/db/reference/populationsim.py
"""
PopulationSim reference data importer.

Imports CDC PLACES, SVI, and ADI data from CSV to DuckDB.
"""

from pathlib import Path
from typing import Optional
import duckdb

# Default location of PopulationSim CSV files
DEFAULT_DATA_PATH = Path(__file__).parent.parent.parent.parent.parent / "skills" / "populationsim" / "data"


def import_cdc_places_tract(
    conn: duckdb.DuckDBPyConnection,
    csv_path: Optional[Path] = None
) -> int:
    """
    Import CDC PLACES tract-level data.
    
    Args:
        conn: Database connection
        csv_path: Path to CSV (uses default if not specified)
        
    Returns:
        Number of rows imported
    """
    csv_path = csv_path or DEFAULT_DATA_PATH / "cdc_places_tract_2024.csv"
    
    # Use DuckDB's efficient CSV reader
    conn.execute(f"""
        INSERT INTO ref_cdc_places_tract
        SELECT * FROM read_csv_auto('{csv_path}', header=true)
        ON CONFLICT (tract_fips) DO UPDATE SET
            -- Update all columns with new values
            total_population = excluded.total_population,
            -- ... etc
    """)
    
    result = conn.execute("SELECT count(*) FROM ref_cdc_places_tract").fetchone()
    return result[0]


def import_all_populationsim_data(
    conn: duckdb.DuckDBPyConnection,
    data_path: Optional[Path] = None
) -> dict:
    """
    Import all PopulationSim reference datasets.
    
    Returns:
        Dict with table names and row counts
    """
    data_path = data_path or DEFAULT_DATA_PATH
    
    results = {}
    results['ref_cdc_places_tract'] = import_cdc_places_tract(conn, data_path / "cdc_places_tract_2024.csv")
    results['ref_cdc_places_county'] = import_cdc_places_county(conn, data_path / "cdc_places_county_2024.csv")
    results['ref_svi_tract'] = import_svi_tract(conn, data_path / "svi_tract_2022.csv")
    results['ref_svi_county'] = import_svi_county(conn, data_path / "svi_county_2022.csv")
    results['ref_adi_blockgroup'] = import_adi_blockgroup(conn, data_path / "adi_blockgroup_2021.csv")
    
    return results
```

### Step 4: Create Import Script

```python
#!/usr/bin/env python3
# scripts/import_populationsim_data.py
"""
Import PopulationSim reference data into HealthSim database.

Usage:
    python scripts/import_populationsim_data.py [--data-path PATH]
"""

import argparse
from pathlib import Path

from healthsim.db import get_connection
from healthsim.db.reference.populationsim import import_all_populationsim_data


def main():
    parser = argparse.ArgumentParser(description="Import PopulationSim reference data")
    parser.add_argument("--data-path", type=Path, help="Path to CSV files")
    args = parser.parse_args()
    
    print("HealthSim PopulationSim Data Import")
    print("=" * 40)
    
    conn = get_connection()
    results = import_all_populationsim_data(conn, args.data_path)
    
    print("\nImport Results:")
    for table, count in results.items():
        print(f"  {table}: {count:,} rows")
    
    # Report database size
    # DuckDB doesn't have a direct size query, so we check file size
    from healthsim.db.connection import DEFAULT_DB_PATH
    size_mb = DEFAULT_DB_PATH.stat().st_size / (1024 * 1024)
    print(f"\nDatabase size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
```

### Step 5: Write Tests

```python
# packages/core/tests/db/test_reference_data.py
"""Tests for PopulationSim reference data import."""

import pytest
from pathlib import Path
import tempfile

from healthsim.db import DatabaseConnection
from healthsim.db.reference.populationsim import (
    import_cdc_places_tract,
    import_all_populationsim_data,
)


@pytest.fixture
def test_db():
    """Create a temporary test database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.duckdb"
        conn = DatabaseConnection(db_path)
        yield conn.connect()
        conn.close()


def test_cdc_places_tract_import(test_db):
    """Test CDC PLACES tract data imports correctly."""
    count = import_cdc_places_tract(test_db)
    assert count > 80000  # Should have ~85,000 tracts
    
    # Verify data structure
    result = test_db.execute("""
        SELECT tract_fips, state_abbr, diabetes_crude_prev
        FROM ref_cdc_places_tract
        WHERE state_abbr = 'CA'
        LIMIT 1
    """).fetchone()
    
    assert result is not None
    assert len(result[0]) == 11  # FIPS is 11 characters


def test_all_data_import(test_db):
    """Test all PopulationSim data imports."""
    results = import_all_populationsim_data(test_db)
    
    assert results['ref_cdc_places_tract'] > 80000
    assert results['ref_cdc_places_county'] > 3000
    assert results['ref_svi_tract'] > 80000
    assert results['ref_svi_county'] > 3000
    assert results['ref_adi_blockgroup'] > 200000


def test_query_by_location(test_db):
    """Test querying reference data by geographic location."""
    import_all_populationsim_data(test_db)
    
    # Query San Diego County diabetes rates
    result = test_db.execute("""
        SELECT AVG(diabetes_crude_prev) as avg_diabetes
        FROM ref_cdc_places_tract
        WHERE county_fips = '06073'  -- San Diego
    """).fetchone()
    
    assert result[0] is not None
    assert 5.0 < result[0] < 20.0  # Reasonable diabetes prevalence range
```

### Step 6: Update PopulationSim Skills

Update `skills/populationsim/SKILL.md` to note that data is now in DuckDB:

```markdown
## Data Sources

PopulationSim uses embedded reference data from:
- CDC PLACES 2024 (tract and county level health indicators)
- Social Vulnerability Index 2022 (tract and county)
- Area Deprivation Index 2021 (block group)

**Storage**: Data is stored in the HealthSim database (`~/.healthsim/healthsim.duckdb`)
in `ref_*` tables. On first use, data is automatically imported from the embedded CSV files.

**Querying**: You can query reference data directly:
```sql
SELECT * FROM ref_cdc_places_tract WHERE county_fips = '06073' LIMIT 10;
```
```

### Step 7: Verify Compression

```bash
# Before: Check CSV sizes
du -sh skills/populationsim/data/

# After: Check DuckDB size
ls -lh ~/.healthsim/healthsim.duckdb
```

Expected: ~148MB CSV → ~20-30MB DuckDB (5-7x compression)

### Step 8: Run Tests

```bash
cd packages/core
source .venv/bin/activate
pytest tests/db/test_reference_data.py -v
pytest tests/ -v  # All tests
```

---

## Post-Flight Checklist

- [ ] All reference tables created in schema
- [ ] CSV import works correctly
- [ ] Row counts match expected (85K tract, 3K county, etc.)
- [ ] Query performance acceptable (<1s for county lookups)
- [ ] Database size ~20-30MB (vs 148MB CSV)
- [ ] PopulationSim skill documentation updated
- [ ] All tests pass

---

## Commit

```bash
git add -A
git commit -m "[Database] Add PopulationSim reference data to DuckDB

- Add reference table schemas (cdc_places, svi, adi)
- Create reference data import module
- Add import script for PopulationSim data
- Update PopulationSim skill documentation
- Achieve ~5-7x compression (148MB CSV → ~25MB DuckDB)

Part of: DuckDB Unified Data Architecture initiative"

git push
```

---

## Update MASTER-PLAN.md

Mark SESSION-02 as complete with commit hash.

---

## Success Criteria

✅ Session complete when:
1. All 5 reference tables exist with data
2. Row counts match source CSVs
3. Geographic queries work (by county, state, tract)
4. Database size is significantly smaller than CSVs
5. Skills documentation updated
6. All tests pass
7. Committed and pushed

---

## Next Session

Proceed to [SESSION-03: State Management](SESSION-03-state-management.md)
