"""
HealthSim Reference Data Module.

Provides loaders for external reference datasets including:
- CDC PLACES health indicators (tract and county level)
- Social Vulnerability Index (tract and county level)
- Area Deprivation Index (block group level)

Usage:
    from healthsim.db.reference import import_all_reference_data, get_reference_status
    
    # Import all reference data
    results = import_all_reference_data(conn)
    
    # Check what's loaded
    status = get_reference_status(conn)
"""

from .loader import (
    import_all_reference_data,
    get_reference_status,
    is_reference_data_loaded,
    REFERENCE_TABLES,
)

from .populationsim import (
    import_places_tract,
    import_places_county,
    import_svi_tract,
    import_svi_county,
    import_adi_blockgroup,
    get_populationsim_data_path,
)

__all__ = [
    # Main functions
    "import_all_reference_data",
    "get_reference_status",
    "is_reference_data_loaded",
    "REFERENCE_TABLES",
    # Individual importers
    "import_places_tract",
    "import_places_county",
    "import_svi_tract",
    "import_svi_county",
    "import_adi_blockgroup",
    "get_populationsim_data_path",
]
