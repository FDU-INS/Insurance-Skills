"""
Reference data loader utilities.

Provides functions to import all reference data and check loading status.
"""

from typing import Dict, Any
import duckdb

from .populationsim import (
    import_places_tract,
    import_places_county,
    import_svi_tract,
    import_svi_county,
    import_adi_blockgroup,
)


# List of all reference tables with their expected minimum row counts
REFERENCE_TABLES = {
    "ref_places_tract": {"min_rows": 80000, "description": "CDC PLACES tract-level health indicators"},
    "ref_places_county": {"min_rows": 3000, "description": "CDC PLACES county-level health indicators"},
    "ref_svi_tract": {"min_rows": 80000, "description": "Social Vulnerability Index tract-level"},
    "ref_svi_county": {"min_rows": 3000, "description": "Social Vulnerability Index county-level"},
    "ref_adi_blockgroup": {"min_rows": 200000, "description": "Area Deprivation Index block group"},
}


def import_all_reference_data(
    conn: duckdb.DuckDBPyConnection,
    replace: bool = False,
    verbose: bool = True
) -> Dict[str, int]:
    """
    Import all PopulationSim reference datasets.
    
    Args:
        conn: Database connection
        replace: If True, drop and recreate all tables; if False, skip existing
        verbose: If True, print progress messages
        
    Returns:
        Dict mapping table names to row counts
    """
    results = {}
    
    importers = [
        ("ref_places_tract", import_places_tract),
        ("ref_places_county", import_places_county),
        ("ref_svi_tract", import_svi_tract),
        ("ref_svi_county", import_svi_county),
        ("ref_adi_blockgroup", import_adi_blockgroup),
    ]
    
    for table_name, importer in importers:
        if verbose:
            print(f"  Importing {table_name}...", end=" ", flush=True)
        try:
            count = importer(conn, replace=replace)
            results[table_name] = count
            if verbose:
                print(f"{count:,} rows")
        except Exception as e:
            results[table_name] = -1
            if verbose:
                print(f"ERROR: {e}")
    
    return results


def get_reference_status(conn: duckdb.DuckDBPyConnection) -> Dict[str, Dict[str, Any]]:
    """
    Get status of all reference tables.
    
    Returns:
        Dict with table status including:
        - exists: bool
        - row_count: int (0 if not exists)
        - healthy: bool (meets minimum row count)
        - description: str
    """
    status = {}
    
    for table_name, info in REFERENCE_TABLES.items():
        exists_result = conn.execute(
            f"SELECT count(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
        ).fetchone()
        exists = exists_result[0] > 0 if exists_result else False
        
        row_count = 0
        if exists:
            row_count = conn.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
        
        status[table_name] = {
            "exists": exists,
            "row_count": row_count,
            "healthy": row_count >= info["min_rows"],
            "description": info["description"],
            "min_expected": info["min_rows"],
        }
    
    return status


def is_reference_data_loaded(conn: duckdb.DuckDBPyConnection) -> bool:
    """
    Check if all reference data is loaded and healthy.
    
    Returns:
        True if all reference tables exist and meet minimum row counts
    """
    status = get_reference_status(conn)
    return all(info["healthy"] for info in status.values())
