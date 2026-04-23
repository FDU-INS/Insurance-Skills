"""NetworkSim reference data resolver.

Resolves provider and facility references from the NetworkSim data
in the canonical healthsim.duckdb database (network schema).

Database: healthsim.duckdb (network schema)

Tables:
- network.providers: 8.9M NPPES provider records
- network.facilities: 77K hospital/facility records  
- network.hospital_quality: 5.4K hospital quality metrics
- network.physician_quality: 1.5M physician quality metrics
- network.ahrf_county: 3.2K Area Health Resource File county data

Usage:
    from healthsim.generation.networksim_reference import (
        NetworkSimResolver,
        get_providers_by_geography,
        get_facilities_by_geography,
    )
    
    resolver = NetworkSimResolver(conn)
    providers = resolver.find_providers(
        state="TX",
        city="Houston",
        specialty="Internal Medicine"
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional
import random


class EntityType(str, Enum):
    """NPPES entity type codes."""
    INDIVIDUAL = "1"
    ORGANIZATION = "2"


class FacilityType(str, Enum):
    """Facility types from CMS data."""
    HOSPITAL = "hospital"
    SNF = "snf"  # Skilled Nursing Facility
    HHA = "hha"  # Home Health Agency
    HOSPICE = "hospice"
    FQHC = "fqhc"  # Federally Qualified Health Center
    RHC = "rhc"  # Rural Health Clinic
    ASC = "asc"  # Ambulatory Surgery Center
    OTHER = "other"


@dataclass
class Provider:
    """Provider record from NPPES."""
    npi: str
    entity_type: EntityType
    
    # Individual provider fields
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    credential: Optional[str] = None
    gender: Optional[str] = None
    
    # Organization fields
    organization_name: Optional[str] = None
    
    # Location
    practice_city: Optional[str] = None
    practice_state: Optional[str] = None
    practice_zip: Optional[str] = None
    practice_address_1: Optional[str] = None
    practice_address_2: Optional[str] = None
    phone: Optional[str] = None
    
    # Taxonomy (specialty codes)
    taxonomy_1: Optional[str] = None
    taxonomy_2: Optional[str] = None
    taxonomy_3: Optional[str] = None
    
    @property
    def display_name(self) -> str:
        """Get display name for provider."""
        if self.entity_type == EntityType.ORGANIZATION:
            return self.organization_name or "Unknown Organization"
        
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        if self.credential:
            parts.append(f", {self.credential}")
        return " ".join(parts) if parts else "Unknown Provider"
    
    @property
    def primary_taxonomy(self) -> Optional[str]:
        """Get primary taxonomy code."""
        return self.taxonomy_1


@dataclass
class Facility:
    """Facility record."""
    ccn: str  # CMS Certification Number
    name: str
    facility_type: str
    
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    
    beds: Optional[int] = None
    subtype: Optional[str] = None


@dataclass
class ProviderSearchCriteria:
    """Criteria for searching providers."""
    state: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    county_fips: Optional[str] = None
    
    entity_type: Optional[EntityType] = None
    taxonomy: Optional[str] = None  # Specialty taxonomy code
    specialty_description: Optional[str] = None  # Text search
    
    limit: int = 100
    random_sample: bool = False


@dataclass
class FacilitySearchCriteria:
    """Criteria for searching facilities."""
    state: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    
    facility_type: Optional[FacilityType] = None
    min_beds: Optional[int] = None
    max_beds: Optional[int] = None
    
    limit: int = 100
    random_sample: bool = False


# Common taxonomy codes for specialties
TAXONOMY_MAP = {
    "internal_medicine": "207R00000X",
    "family_medicine": "207Q00000X", 
    "general_practice": "208D00000X",
    "cardiology": "207RC0000X",
    "endocrinology": "207RE0101X",
    "nephrology": "207RN0300X",
    "pulmonology": "207RP1001X",
    "gastroenterology": "207RG0100X",
    "neurology": "2084N0400X",
    "psychiatry": "2084P0800X",
    "orthopedics": "207X00000X",
    "dermatology": "207N00000X",
    "ophthalmology": "207W00000X",
    "emergency_medicine": "207P00000X",
    "pediatrics": "208000000X",
    "obstetrics": "207V00000X",
    "surgery_general": "208600000X",
    "anesthesiology": "207L00000X",
    "radiology": "2085R0202X",
    "pathology": "207ZP0102X",
    "nurse_practitioner": "363L00000X",
    "physician_assistant": "363A00000X",
    "pharmacy": "183500000X",
    "hospital": "282N00000X",
    "skilled_nursing": "314000000X",
}


# CMS Provider of Service (POS) facility type codes
FACILITY_TYPE_MAP = {
    "hospital": "01",               # Short-term Acute Care Hospital
    "long_term_hospital": "02",     # Long-term Care Hospital  
    "psychiatric": "03",            # Psychiatric Hospital
    "rehabilitation": "04",         # Rehabilitation Hospital
    "childrens": "05",              # Children's Hospital
    "religious_nonmedical": "06",   # Religious Nonmedical Health Care
    "snf": "07",                    # Skilled Nursing Facility
    "home_health": "08",            # Home Health Agency
    "hospice": "09",                # Hospice
    "corf": "11",                   # Comprehensive Outpatient Rehab
    "esrd": "12",                   # End-Stage Renal Disease
    "asc": "14",                    # Ambulatory Surgical Center
    "rural_health": "17",           # Rural Health Clinic
    "fqhc": "19",                   # Federally Qualified Health Center
    "cmhc": "21",                   # Community Mental Health Center
}


def get_healthsim_db_path() -> Path:
    """Get the path to canonical HealthSim DuckDB database.
    
    The canonical database is healthsim.duckdb which contains:
    - main schema: Entity tables (patients, encounters, etc.)
    - population schema: CDC PLACES and SVI reference data
    - network schema: NPPES provider and facility data
    
    Note: healthsim.duckdb is tracked in Git LFS (~1.7GB).
    """
    module_path = Path(__file__).resolve()
    workspace_root = module_path.parent.parent.parent.parent.parent.parent
    return workspace_root / "healthsim.duckdb"


def get_networksim_db_path() -> Path:
    """Get the path to HealthSim DuckDB database for NetworkSim data.
    
    Returns the canonical healthsim.duckdb path. NetworkSim data is in 
    the 'network' schema:
    - network.providers: 8.9M NPPES provider records
    - network.facilities: 77K CMS facility records
    - network.hospital_quality: Hospital quality metrics
    - network.physician_quality: Physician quality metrics
    - network.ahrf_county: Area Health Resource File data
    
    Note: This returns the same path as get_healthsim_db_path() since
    NetworkSim data is now part of the canonical database.
    """
    return get_healthsim_db_path()


class NetworkSimResolver:
    """Resolves provider and facility references from NetworkSim data.
    
    Uses the 'network' schema in the HealthSim DuckDB database which contains:
    - providers: 8.9M NPPES provider records
    - facilities: 77K hospital/facility records
    - hospital_quality: 5.4K hospital quality metrics
    - physician_quality: 1.5M physician quality metrics
    - ahrf_county: 3.2K Area Health Resource File county data
    
    Example:
        >>> import duckdb
        >>> conn = duckdb.connect(str(get_healthsim_db_path()), read_only=True)
        >>> resolver = NetworkSimResolver(conn)
        >>> 
        >>> # Find cardiologists in Houston
        >>> providers = resolver.find_providers(
        ...     state="TX",
        ...     city="HOUSTON", 
        ...     taxonomy=TAXONOMY_MAP["cardiology"]
        ... )
        >>> 
        >>> # Find hospitals in California
        >>> facilities = resolver.find_facilities(
        ...     state="CA",
        ...     facility_type=FacilityType.HOSPITAL,
        ...     min_beds=100
        ... )
    """
    
    # Schema prefix for network tables in healthsim.duckdb
    SCHEMA = "network"
    
    def __init__(self, conn):
        """Initialize resolver with database connection.
        
        Args:
            conn: DuckDB connection to NetworkSim database
        """
        self.conn = conn
    
    def find_providers(
        self,
        state: Optional[str] = None,
        city: Optional[str] = None,
        zip_code: Optional[str] = None,
        entity_type: Optional[EntityType] = None,
        taxonomy: Optional[str] = None,
        limit: int = 100,
        random_sample: bool = False,
    ) -> list[Provider]:
        """Find providers matching criteria.
        
        Args:
            state: State abbreviation (e.g., "TX")
            city: City name (case-insensitive)
            zip_code: ZIP code (5-digit)
            entity_type: Individual (1) or Organization (2)
            taxonomy: Taxonomy code for specialty
            limit: Maximum results to return
            random_sample: If True, return random sample instead of first N
            
        Returns:
            List of matching Provider objects
        """
        conditions = []
        params = []
        
        if state:
            conditions.append("practice_state = ?")
            params.append(state.upper())
        
        if city:
            conditions.append("UPPER(practice_city) = UPPER(?)")
            params.append(city)
        
        if zip_code:
            conditions.append("practice_zip LIKE ?")
            params.append(f"{zip_code[:5]}%")
        
        if entity_type:
            conditions.append("entity_type_code = ?")
            params.append(entity_type.value)
        
        if taxonomy:
            conditions.append("(taxonomy_1 = ? OR taxonomy_2 = ? OR taxonomy_3 = ?)")
            params.extend([taxonomy, taxonomy, taxonomy])
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        if random_sample:
            order_clause = "ORDER BY RANDOM()"
        else:
            order_clause = "ORDER BY npi"
        
        query = f"""
            SELECT npi, entity_type_code, last_name, first_name, middle_name,
                   credential, gender, organization_name,
                   practice_city, practice_state, practice_zip,
                   practice_address_1, practice_address_2, phone,
                   taxonomy_1, taxonomy_2, taxonomy_3
            FROM {self.SCHEMA}.providers
            WHERE {where_clause}
            {order_clause}
            LIMIT {limit}
        """
        
        results = self.conn.execute(query, params).fetchall()
        
        providers = []
        for row in results:
            providers.append(Provider(
                npi=row[0],
                entity_type=EntityType(row[1]) if row[1] else EntityType.INDIVIDUAL,
                last_name=row[2],
                first_name=row[3],
                middle_name=row[4],
                credential=row[5],
                gender=row[6],
                organization_name=row[7],
                practice_city=row[8],
                practice_state=row[9],
                practice_zip=row[10],
                practice_address_1=row[11],
                practice_address_2=row[12],
                phone=row[13],
                taxonomy_1=row[14],
                taxonomy_2=row[15],
                taxonomy_3=row[16],
            ))
        
        return providers
    
    def find_facilities(
        self,
        state: Optional[str] = None,
        city: Optional[str] = None,
        zip_code: Optional[str] = None,
        facility_type: Optional[str] = None,
        min_beds: Optional[int] = None,
        max_beds: Optional[int] = None,
        limit: int = 100,
        random_sample: bool = False,
    ) -> list[Facility]:
        """Find facilities matching criteria.
        
        Args:
            state: State abbreviation
            city: City name
            zip_code: ZIP code
            facility_type: Type of facility
            min_beds: Minimum bed count
            max_beds: Maximum bed count
            limit: Maximum results
            random_sample: Return random sample
            
        Returns:
            List of matching Facility objects
        """
        conditions = []
        params = []
        
        if state:
            conditions.append("state = ?")
            params.append(state.upper())
        
        if city:
            conditions.append("UPPER(city) = UPPER(?)")
            params.append(city)
        
        if zip_code:
            conditions.append("zip LIKE ?")
            params.append(f"{zip_code[:5]}%")
        
        if facility_type:
            # Translate facility type name to code if needed
            type_code = FACILITY_TYPE_MAP.get(facility_type.lower(), facility_type)
            conditions.append("type = ?")
            params.append(type_code)
        
        if min_beds is not None:
            conditions.append("beds >= ?")
            params.append(min_beds)
        
        if max_beds is not None:
            conditions.append("beds <= ?")
            params.append(max_beds)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        if random_sample:
            order_clause = "ORDER BY RANDOM()"
        else:
            order_clause = "ORDER BY ccn"
        
        query = f"""
            SELECT ccn, name, type, city, state, zip, phone, beds, subtype
            FROM {self.SCHEMA}.facilities
            WHERE {where_clause}
            {order_clause}
            LIMIT {limit}
        """
        
        results = self.conn.execute(query, params).fetchall()
        
        facilities = []
        for row in results:
            facilities.append(Facility(
                ccn=row[0],
                name=row[1],
                facility_type=row[2],
                city=row[3],
                state=row[4],
                zip_code=row[5],
                phone=row[6],
                beds=row[7],
                subtype=row[8],
            ))
        
        return facilities
    
    def get_provider_by_npi(self, npi: str) -> Optional[Provider]:
        """Get a specific provider by NPI."""
        providers = self.find_providers(limit=1)
        # Direct query
        query = f"""
            SELECT npi, entity_type_code, last_name, first_name, middle_name,
                   credential, gender, organization_name,
                   practice_city, practice_state, practice_zip,
                   practice_address_1, practice_address_2, phone,
                   taxonomy_1, taxonomy_2, taxonomy_3
            FROM {self.SCHEMA}.providers
            WHERE npi = ?
        """
        result = self.conn.execute(query, [npi]).fetchone()
        
        if not result:
            return None
        
        return Provider(
            npi=result[0],
            entity_type=EntityType(result[1]) if result[1] else EntityType.INDIVIDUAL,
            last_name=result[2],
            first_name=result[3],
            middle_name=result[4],
            credential=result[5],
            gender=result[6],
            organization_name=result[7],
            practice_city=result[8],
            practice_state=result[9],
            practice_zip=result[10],
            practice_address_1=result[11],
            practice_address_2=result[12],
            phone=result[13],
            taxonomy_1=result[14],
            taxonomy_2=result[15],
            taxonomy_3=result[16],
        )
    
    def get_facility_by_ccn(self, ccn: str) -> Optional[Facility]:
        """Get a specific facility by CCN."""
        query = f"""
            SELECT ccn, name, type, city, state, zip, phone, beds, subtype
            FROM {self.SCHEMA}.facilities
            WHERE ccn = ?
        """
        result = self.conn.execute(query, [ccn]).fetchone()
        
        if not result:
            return None
        
        return Facility(
            ccn=result[0],
            name=result[1],
            facility_type=result[2],
            city=result[3],
            state=result[4],
            zip_code=result[5],
            phone=result[6],
            beds=result[7],
            subtype=result[8],
        )
    
    def count_providers(
        self,
        state: Optional[str] = None,
        taxonomy: Optional[str] = None,
    ) -> int:
        """Count providers matching criteria."""
        conditions = []
        params = []
        
        if state:
            conditions.append("practice_state = ?")
            params.append(state.upper())
        
        if taxonomy:
            conditions.append("(taxonomy_1 = ? OR taxonomy_2 = ? OR taxonomy_3 = ?)")
            params.extend([taxonomy, taxonomy, taxonomy])
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f"SELECT COUNT(*) FROM {self.SCHEMA}.providers WHERE {where_clause}"
        return self.conn.execute(query, params).fetchone()[0]
    
    def count_facilities(
        self,
        state: Optional[str] = None,
        facility_type: Optional[str] = None,
    ) -> int:
        """Count facilities matching criteria."""
        conditions = []
        params = []
        
        if state:
            conditions.append("state = ?")
            params.append(state.upper())
        
        if facility_type:
            # Translate facility type name to code if needed
            type_code = FACILITY_TYPE_MAP.get(facility_type.lower(), facility_type)
            conditions.append("type = ?")
            params.append(type_code)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f"SELECT COUNT(*) FROM {self.SCHEMA}.facilities WHERE {where_clause}"
        return self.conn.execute(query, params).fetchone()[0]
    
    def list_states_with_providers(self) -> list[dict]:
        """List states with provider counts."""
        query = f"""
            SELECT practice_state, COUNT(*) as provider_count
            FROM {self.SCHEMA}.providers
            WHERE practice_state IS NOT NULL
            GROUP BY practice_state
            ORDER BY practice_state
        """
        results = self.conn.execute(query).fetchall()
        return [{"state": r[0], "count": r[1]} for r in results]
    
    def get_specialty_distribution(self, state: Optional[str] = None) -> list[dict]:
        """Get distribution of specialties."""
        where_clause = f"WHERE practice_state = '{state}'" if state else ""
        
        query = f"""
            SELECT taxonomy_1, COUNT(*) as count
            FROM {self.SCHEMA}.providers
            {where_clause}
            GROUP BY taxonomy_1
            ORDER BY count DESC
            LIMIT 50
        """
        results = self.conn.execute(query).fetchall()
        return [{"taxonomy": r[0], "count": r[1]} for r in results]


# =============================================================================
# Convenience Functions
# =============================================================================

def get_providers_by_geography(
    conn,
    state: str,
    city: Optional[str] = None,
    specialty: Optional[str] = None,
    limit: int = 100,
) -> list[Provider]:
    """Get providers by geographic location.
    
    Args:
        conn: DuckDB connection to NetworkSim database
        state: State abbreviation
        city: Optional city name
        specialty: Optional specialty key (from TAXONOMY_MAP) or taxonomy code
        limit: Maximum results
        
    Returns:
        List of Provider objects
    """
    resolver = NetworkSimResolver(conn)
    
    taxonomy = None
    if specialty:
        # Check if it's a key in TAXONOMY_MAP
        taxonomy = TAXONOMY_MAP.get(specialty.lower().replace(" ", "_"), specialty)
    
    return resolver.find_providers(
        state=state,
        city=city,
        taxonomy=taxonomy,
        limit=limit,
    )


def get_facilities_by_geography(
    conn,
    state: str,
    city: Optional[str] = None,
    facility_type: Optional[str] = None,
    limit: int = 100,
) -> list[Facility]:
    """Get facilities by geographic location.
    
    Args:
        conn: DuckDB connection to NetworkSim database
        state: State abbreviation
        city: Optional city name
        facility_type: Facility type name (from FACILITY_TYPE_MAP) or CMS code
        limit: Maximum results
        
    Returns:
        List of Facility objects
    """
    resolver = NetworkSimResolver(conn)
    
    # Resolve facility type to CMS code if needed
    resolved_type = None
    if facility_type:
        resolved_type = FACILITY_TYPE_MAP.get(
            facility_type.lower().replace(" ", "_"), 
            facility_type
        )
    
    return resolver.find_facilities(
        state=state,
        city=city,
        facility_type=resolved_type,
        limit=limit,
    )


def assign_provider_to_patient(
    conn,
    patient_state: str,
    patient_city: Optional[str] = None,
    specialty: Optional[str] = None,
    seed: Optional[int] = None,
) -> Optional[Provider]:
    """Assign a provider to a patient based on geography.
    
    Args:
        conn: DuckDB connection to NetworkSim database
        patient_state: Patient's state
        patient_city: Patient's city (optional)
        specialty: Required specialty (optional)
        seed: Random seed for reproducibility (affects Python's random.choice)
        
    Returns:
        Assigned Provider or None if no match found
    """
    if seed is not None:
        random.seed(seed)
    
    resolver = NetworkSimResolver(conn)
    
    taxonomy = None
    if specialty:
        taxonomy = TAXONOMY_MAP.get(specialty.lower().replace(" ", "_"), specialty)
    
    # Try to find in same city first (use deterministic order, then random.choice)
    if patient_city:
        providers = resolver.find_providers(
            state=patient_state,
            city=patient_city,
            taxonomy=taxonomy,
            limit=100,
            random_sample=False,  # Use deterministic NPI ordering
        )
        if providers:
            return random.choice(providers)
    
    # Fall back to state-level
    providers = resolver.find_providers(
        state=patient_state,
        taxonomy=taxonomy,
        limit=100,
        random_sample=False,  # Use deterministic NPI ordering
    )
    
    return random.choice(providers) if providers else None


def assign_facility_to_patient(
    conn,
    patient_state: str,
    patient_city: Optional[str] = None,
    facility_type: str = "hospital",
    seed: Optional[int] = None,
) -> Optional[Facility]:
    """Assign a facility to a patient based on geography.
    
    Args:
        conn: DuckDB connection to NetworkSim database
        patient_state: Patient's state
        patient_city: Patient's city (optional)
        facility_type: Type of facility (from FACILITY_TYPE_MAP) or CMS code
        seed: Random seed for reproducibility
        
    Returns:
        Assigned Facility or None if no match found
    """
    if seed is not None:
        random.seed(seed)
    
    resolver = NetworkSimResolver(conn)
    
    # Resolve facility type to CMS code
    resolved_type = FACILITY_TYPE_MAP.get(
        facility_type.lower().replace(" ", "_"),
        facility_type
    )
    
    # Try to find in same city first (use deterministic order, then random.choice)
    if patient_city:
        facilities = resolver.find_facilities(
            state=patient_state,
            city=patient_city,
            facility_type=resolved_type,
            limit=50,
            random_sample=False,  # Use deterministic CCN ordering
        )
        if facilities:
            return random.choice(facilities)
    
    # Fall back to state-level
    facilities = resolver.find_facilities(
        state=patient_state,
        facility_type=resolved_type,
        limit=50,
        random_sample=False,  # Use deterministic CCN ordering
    )
    
    return random.choice(facilities) if facilities else None


__all__ = [
    # Enums
    "EntityType",
    "FacilityType",
    # Data classes
    "Provider",
    "Facility",
    "ProviderSearchCriteria",
    "FacilitySearchCriteria",
    # Constants
    "TAXONOMY_MAP",
    "FACILITY_TYPE_MAP",
    # Resolver
    "NetworkSimResolver",
    "get_healthsim_db_path",
    "get_networksim_db_path",
    # Convenience functions
    "get_providers_by_geography",
    "get_facilities_by_geography",
    "assign_provider_to_patient",
    "assign_facility_to_patient",
]
