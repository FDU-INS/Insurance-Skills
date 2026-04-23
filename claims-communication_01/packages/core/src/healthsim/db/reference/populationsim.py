"""
PopulationSim reference data importer.

Imports CDC PLACES, SVI, and ADI data from CSV to DuckDB.
Uses DuckDB's efficient CSV reader with auto-detection for schema inference.
"""

from pathlib import Path
from typing import Optional
import duckdb

# Default location of PopulationSim CSV files (relative to package root)
def get_populationsim_data_path() -> Path:
    """Get the path to PopulationSim data directory."""
    # Navigate from this file to workspace root, then to skills/populationsim/data
    module_path = Path(__file__).resolve()
    # packages/core/src/healthsim/db/reference/populationsim.py
    # -> packages/core/src/healthsim/db/reference
    # -> packages/core/src/healthsim/db
    # -> packages/core/src/healthsim
    # -> packages/core/src
    # -> packages/core
    # -> packages
    # -> workspace root
    workspace_root = module_path.parent.parent.parent.parent.parent.parent.parent
    return workspace_root / "skills" / "populationsim" / "data"


def import_places_tract(
    conn: duckdb.DuckDBPyConnection,
    csv_path: Optional[Path] = None,
    replace: bool = False
) -> int:
    """
    Import CDC PLACES tract-level data.
    
    Args:
        conn: Database connection
        csv_path: Path to CSV (uses default if not specified)
        replace: If True, drop and recreate table; if False, skip if exists
        
    Returns:
        Number of rows imported (0 if skipped)
    """
    table_name = "ref_places_tract"
    csv_path = csv_path or get_populationsim_data_path() / "tract" / "places_tract_2024.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Check if table exists and has data
    existing = conn.execute(
        f"SELECT count(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
    ).fetchone()[0]
    
    if existing and not replace:
        # Return existing count
        return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
    
    if replace and existing:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    # Create table from CSV using DuckDB's auto-detection
    conn.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_path}', header=true, normalize_names=true)
    """)
    
    # Add primary key index on tract FIPS
    conn.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_pk ON {table_name}(tractfips)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_county ON {table_name}(countyfips)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_state ON {table_name}(stateabbr)")
    
    return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]


def import_places_county(
    conn: duckdb.DuckDBPyConnection,
    csv_path: Optional[Path] = None,
    replace: bool = False
) -> int:
    """Import CDC PLACES county-level data."""
    table_name = "ref_places_county"
    csv_path = csv_path or get_populationsim_data_path() / "county" / "places_county_2024.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    existing = conn.execute(
        f"SELECT count(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
    ).fetchone()[0]
    
    if existing and not replace:
        return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
    
    if replace and existing:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    conn.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_path}', header=true, normalize_names=true)
    """)
    
    conn.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_pk ON {table_name}(countyfips)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_state ON {table_name}(stateabbr)")
    
    return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]


def import_svi_tract(
    conn: duckdb.DuckDBPyConnection,
    csv_path: Optional[Path] = None,
    replace: bool = False
) -> int:
    """Import Social Vulnerability Index tract-level data."""
    table_name = "ref_svi_tract"
    csv_path = csv_path or get_populationsim_data_path() / "tract" / "svi_tract_2022.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    existing = conn.execute(
        f"SELECT count(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
    ).fetchone()[0]
    
    if existing and not replace:
        return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
    
    if replace and existing:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    conn.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_path}', header=true, normalize_names=true)
    """)
    
    conn.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_pk ON {table_name}(fips)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_county ON {table_name}(stcnty)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_state ON {table_name}(st_abbr)")
    
    return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]


def import_svi_county(
    conn: duckdb.DuckDBPyConnection,
    csv_path: Optional[Path] = None,
    replace: bool = False
) -> int:
    """Import Social Vulnerability Index county-level data."""
    table_name = "ref_svi_county"
    csv_path = csv_path or get_populationsim_data_path() / "county" / "svi_county_2022.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    existing = conn.execute(
        f"SELECT count(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
    ).fetchone()[0]
    
    if existing and not replace:
        return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
    
    if replace and existing:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    conn.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_path}', header=true, normalize_names=true)
    """)
    
    conn.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_pk ON {table_name}(stcnty)")
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_state ON {table_name}(st_abbr)")
    
    return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]


def import_adi_blockgroup(
    conn: duckdb.DuckDBPyConnection,
    csv_path: Optional[Path] = None,
    replace: bool = False
) -> int:
    """Import Area Deprivation Index block group data."""
    table_name = "ref_adi_blockgroup"
    csv_path = csv_path or get_populationsim_data_path() / "block_group" / "adi_blockgroup_2023.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    existing = conn.execute(
        f"SELECT count(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
    ).fetchone()[0]
    
    if existing and not replace:
        return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
    
    if replace and existing:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    conn.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_path}', header=true, normalize_names=true)
    """)
    
    conn.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_pk ON {table_name}(fips)")
    
    return conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
