"""Reference profile resolver for PopulationSim and NetworkSim integration.

Resolves geography references to actual demographic distributions
from CDC PLACES and SVI data, and provider/facility data from NPPES.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
import duckdb


class GeographyLevel(Enum):
    """Geographic resolution levels."""
    STATE = "state"
    COUNTY = "county"
    TRACT = "tract"
    MSA = "msa"


@dataclass
class GeographyReference:
    """Reference to a geographic area."""
    level: GeographyLevel
    code: str  # FIPS code, state abbreviation, or CBSA code
    name: Optional[str] = None


@dataclass
class DemographicProfile:
    """Demographic profile extracted from reference data."""
    geography: GeographyReference
    population: int = 0
    
    # Age distribution
    pct_age_under_17: float = 0.0
    pct_age_18_64: float = 0.0
    pct_age_65_plus: float = 0.0
    
    # Gender (default US average, not in SVI)
    pct_male: float = 49.0
    pct_female: float = 51.0
    
    # Race/ethnicity
    pct_minority: float = 0.0
    pct_hispanic: float = 0.0
    pct_asian: float = 0.0
    
    # Socioeconomic
    pct_poverty: float = 0.0
    pct_uninsured: float = 0.0
    
    # Health indicators (from PLACES)
    pct_diabetes: float = 0.0
    pct_obesity: float = 0.0
    pct_hypertension: float = 0.0
    pct_asthma: float = 0.0
    pct_heart_disease: float = 0.0
    pct_copd: float = 0.0
    pct_cancer: float = 0.0
    pct_depression: float = 0.0
    
    # Raw data for custom extraction
    raw_places: dict = field(default_factory=dict)
    raw_svi: dict = field(default_factory=dict)



class ReferenceProfileResolver:
    """Resolves geography references to demographic profiles.
    
    Uses CDC PLACES and SVI data to extract real-world demographics
    that can be used to build profile specifications.
    
    Example:
        >>> resolver = ReferenceProfileResolver(conn)
        >>> profile = resolver.resolve_county("48201")  # Harris County TX
        >>> profile.pct_diabetes  # 13.2
        >>> profile.pct_age_65_plus  # 11.0
        >>> 
        >>> # Convert to profile spec
        >>> spec = resolver.to_profile_spec(profile)
    """
    
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        """Initialize resolver with database connection.
        
        Args:
            conn: DuckDB connection to healthsim.duckdb with population and network schemas
        """
        self.conn = conn
    
    def resolve_county(self, county_fips: str) -> DemographicProfile:
        """Resolve county FIPS to demographic profile.
        
        Args:
            county_fips: 5-digit county FIPS code (e.g., "48201")
            
        Returns:
            DemographicProfile with extracted demographics
        """
        # Normalize FIPS (remove leading zeros issues)
        if isinstance(county_fips, int):
            county_fips = str(county_fips).zfill(5)
        
        # Get PLACES data
        places_data = self._get_places_county(county_fips)
        
        # Get SVI data
        svi_data = self._get_svi_county(county_fips)
        
        if not places_data and not svi_data:
            raise ValueError(f"No data found for county FIPS: {county_fips}")
        
        return self._build_profile(
            geography=GeographyReference(
                level=GeographyLevel.COUNTY,
                code=county_fips,
                name=places_data.get("countyname") if places_data else None
            ),
            places_data=places_data or {},
            svi_data=svi_data or {}
        )
    
    def resolve_state(self, state_abbr: str) -> DemographicProfile:
        """Resolve state to aggregated demographic profile.
        
        Args:
            state_abbr: 2-letter state abbreviation (e.g., "TX")
            
        Returns:
            DemographicProfile with state-level averages
        """
        # Aggregate PLACES data for state
        places_query = """
            SELECT 
                stateabbr,
                SUM(totalpopulation) as total_pop,
                SUM(diabetes_crudeprev * totalpopulation) / SUM(totalpopulation) as diabetes_avg,
                SUM(obesity_crudeprev * totalpopulation) / SUM(totalpopulation) as obesity_avg,
                SUM(bphigh_crudeprev * totalpopulation) / SUM(totalpopulation) as bphigh_avg,
                SUM(casthma_crudeprev * totalpopulation) / SUM(totalpopulation) as asthma_avg,
                SUM(chd_crudeprev * totalpopulation) / SUM(totalpopulation) as chd_avg,
                SUM(copd_crudeprev * totalpopulation) / SUM(totalpopulation) as copd_avg,
                SUM(cancer_crudeprev * totalpopulation) / SUM(totalpopulation) as cancer_avg,
                SUM(depression_crudeprev * totalpopulation) / SUM(totalpopulation) as depression_avg
            FROM population.places_county
            WHERE stateabbr = ?
            GROUP BY stateabbr
        """
        places_result = self.conn.execute(places_query, [state_abbr]).fetchone()
        
        # Aggregate SVI data for state  
        svi_query = """
            SELECT
                st_abbr,
                SUM(e_totpop) as total_pop,
                SUM(ep_age65 * e_totpop) / NULLIF(SUM(e_totpop), 0) as age65_avg,
                SUM(ep_age17 * e_totpop) / NULLIF(SUM(e_totpop), 0) as age17_avg,
                SUM(ep_minrty * e_totpop) / NULLIF(SUM(e_totpop), 0) as minority_avg,
                SUM(ep_hisp * e_totpop) / NULLIF(SUM(e_totpop), 0) as hisp_avg,
                SUM(ep_pov150 * e_totpop) / NULLIF(SUM(e_totpop), 0) as poverty_avg,
                SUM(ep_uninsur * e_totpop) / NULLIF(SUM(e_totpop), 0) as uninsur_avg
            FROM population.svi_county
            WHERE st_abbr = ?
            GROUP BY st_abbr
        """
        svi_result = self.conn.execute(svi_query, [state_abbr]).fetchone()
        
        if not places_result and not svi_result:
            raise ValueError(f"No data found for state: {state_abbr}")
        
        # Build aggregated profile
        return DemographicProfile(
            geography=GeographyReference(
                level=GeographyLevel.STATE,
                code=state_abbr,
                name=state_abbr
            ),
            population=int(places_result[1]) if places_result else 0,
            pct_age_under_17=float(svi_result[3] or 0) if svi_result else 22.0,
            pct_age_65_plus=float(svi_result[2] or 0) if svi_result else 16.0,
            pct_age_18_64=100 - float(svi_result[3] or 22) - float(svi_result[2] or 16) if svi_result else 62.0,
            pct_minority=float(svi_result[4] or 0) if svi_result else 40.0,
            pct_hispanic=float(svi_result[5] or 0) if svi_result else 18.0,
            pct_poverty=float(svi_result[6] or 0) if svi_result else 12.0,
            pct_uninsured=float(svi_result[7] or 0) if svi_result else 10.0,
            pct_diabetes=float(places_result[2] or 0) if places_result else 11.0,
            pct_obesity=float(places_result[3] or 0) if places_result else 32.0,
            pct_hypertension=float(places_result[4] or 0) if places_result else 30.0,
            pct_asthma=float(places_result[5] or 0) if places_result else 9.0,
            pct_heart_disease=float(places_result[6] or 0) if places_result else 6.0,
            pct_copd=float(places_result[7] or 0) if places_result else 6.0,
            pct_cancer=float(places_result[8] or 0) if places_result else 6.0,
            pct_depression=float(places_result[9] or 0) if places_result else 20.0,
        )

    
    def _get_places_county(self, county_fips: str) -> Optional[dict]:
        """Get PLACES data for a county."""
        query = """
            SELECT * FROM population.places_county 
            WHERE countyfips = ? OR countyfips = ?
        """
        # Try with and without leading zeros
        result = self.conn.execute(query, [county_fips, county_fips.lstrip('0')]).fetchone()
        if result:
            cols = [desc[0] for desc in self.conn.description]
            return dict(zip(cols, result))
        return None
    
    def _get_svi_county(self, county_fips: str) -> Optional[dict]:
        """Get SVI data for a county."""
        query = """
            SELECT * FROM population.svi_county 
            WHERE stcnty = ? OR stcnty = ?
        """
        result = self.conn.execute(query, [county_fips, county_fips.lstrip('0')]).fetchone()
        if result:
            cols = [desc[0] for desc in self.conn.description]
            return dict(zip(cols, result))
        return None
    
    def _build_profile(
        self,
        geography: GeographyReference,
        places_data: dict,
        svi_data: dict
    ) -> DemographicProfile:
        """Build demographic profile from raw data."""
        
        # Extract population
        population = places_data.get("totalpopulation", 0) or svi_data.get("e_totpop", 0)
        
        # Extract age distribution from SVI
        pct_age_65_plus = float(svi_data.get("ep_age65", 0) or 0)
        pct_age_under_17 = float(svi_data.get("ep_age17", 0) or 0)
        pct_age_18_64 = max(0, 100 - pct_age_65_plus - pct_age_under_17)
        
        # Extract race/ethnicity
        pct_minority = float(svi_data.get("ep_minrty", 0) or 0)
        pct_hispanic = float(svi_data.get("ep_hisp", 0) or 0)
        pct_asian = float(svi_data.get("ep_asian", 0) or 0)
        
        # Extract socioeconomic
        pct_poverty = float(svi_data.get("ep_pov150", 0) or 0)
        pct_uninsured = float(svi_data.get("ep_uninsur", 0) or 0)
        
        # Extract health indicators from PLACES
        pct_diabetes = float(places_data.get("diabetes_crudeprev", 0) or 0)
        pct_obesity = float(places_data.get("obesity_crudeprev", 0) or 0)
        pct_hypertension = float(places_data.get("bphigh_crudeprev", 0) or 0)
        pct_asthma = float(places_data.get("casthma_crudeprev", 0) or 0)
        pct_heart_disease = float(places_data.get("chd_crudeprev", 0) or 0)
        pct_copd = float(places_data.get("copd_crudeprev", 0) or 0)
        pct_cancer = float(places_data.get("cancer_crudeprev", 0) or 0)
        pct_depression = float(places_data.get("depression_crudeprev", 0) or 0)
        
        return DemographicProfile(
            geography=geography,
            population=int(population),
            pct_age_under_17=pct_age_under_17,
            pct_age_18_64=pct_age_18_64,
            pct_age_65_plus=pct_age_65_plus,
            pct_minority=pct_minority,
            pct_hispanic=pct_hispanic,
            pct_asian=pct_asian,
            pct_poverty=pct_poverty,
            pct_uninsured=pct_uninsured,
            pct_diabetes=pct_diabetes,
            pct_obesity=pct_obesity,
            pct_hypertension=pct_hypertension,
            pct_asthma=pct_asthma,
            pct_heart_disease=pct_heart_disease,
            pct_copd=pct_copd,
            pct_cancer=pct_cancer,
            pct_depression=pct_depression,
            raw_places=places_data,
            raw_svi=svi_data,
        )
    
    def to_profile_spec(self, profile: DemographicProfile) -> dict:
        """Convert demographic profile to profile specification.
        
        Creates a ProfileSpecification dict that can be used with
        the profile executor.
        
        Args:
            profile: DemographicProfile from resolve_* methods
            
        Returns:
            Dict suitable for ProfileExecutor
        """
        geo_name = profile.geography.name or profile.geography.code
        
        # Build age distribution based on census-style bands
        age_bands = {}
        if profile.pct_age_under_17 > 0:
            age_bands["0-17"] = profile.pct_age_under_17 / 100
        if profile.pct_age_18_64 > 0:
            # Split 18-64 into sub-bands (rough estimate)
            age_bands["18-34"] = (profile.pct_age_18_64 * 0.35) / 100
            age_bands["35-54"] = (profile.pct_age_18_64 * 0.40) / 100
            age_bands["55-64"] = (profile.pct_age_18_64 * 0.25) / 100
        if profile.pct_age_65_plus > 0:
            age_bands["65+"] = profile.pct_age_65_plus / 100
        
        # Normalize to ensure sum = 1.0
        total = sum(age_bands.values())
        if total > 0:
            age_bands = {k: v/total for k, v in age_bands.items()}
        
        return {
            "profile": {
                "id": f"ref-{profile.geography.level.value}-{profile.geography.code}",
                "name": f"Reference Profile: {geo_name}",
                "source": "populationsim",
                "version": "1.0",
                
                "generation": {
                    "count": 100,  # Default, override as needed
                    "products": ["patientsim"],
                },
                
                "demographics": {
                    "source": "populationsim",
                    "reference": {
                        "type": profile.geography.level.value,
                        "code": profile.geography.code,
                        "name": geo_name,
                    },
                    "age": {
                        "type": "age_bands",
                        "bands": age_bands
                    },
                    "gender": {
                        "type": "categorical",
                        "weights": {
                            "M": profile.pct_male / 100,
                            "F": profile.pct_female / 100
                        }
                    },
                },
                
                "clinical": {
                    "conditions": [
                        {"code": "E11", "description": "Type 2 diabetes", 
                         "prevalence": profile.pct_diabetes / 100},
                        {"code": "E66", "description": "Obesity", 
                         "prevalence": profile.pct_obesity / 100},
                        {"code": "I10", "description": "Essential hypertension", 
                         "prevalence": profile.pct_hypertension / 100},
                        {"code": "J45", "description": "Asthma", 
                         "prevalence": profile.pct_asthma / 100},
                        {"code": "I25", "description": "Heart disease", 
                         "prevalence": profile.pct_heart_disease / 100},
                        {"code": "J44", "description": "COPD", 
                         "prevalence": profile.pct_copd / 100},
                        {"code": "C80", "description": "Cancer", 
                         "prevalence": profile.pct_cancer / 100},
                        {"code": "F32", "description": "Depression", 
                         "prevalence": profile.pct_depression / 100},
                    ]
                },
                
                "coverage": {
                    "pct_uninsured": profile.pct_uninsured
                },
                
                "socioeconomic": {
                    "pct_poverty": profile.pct_poverty,
                    "pct_minority": profile.pct_minority,
                }
            }
        }



def resolve_geography(
    geography_spec: dict,
    conn: duckdb.DuckDBPyConnection
) -> DemographicProfile:
    """Resolve a geography specification to demographic profile.
    
    Convenience function for use with profile specifications.
    
    Args:
        geography_spec: Dict with 'type' and 'code' (and optional 'fips')
        conn: DuckDB connection
        
    Returns:
        DemographicProfile
        
    Example:
        >>> spec = {"type": "county", "fips": "48201"}
        >>> profile = resolve_geography(spec, conn)
    """
    resolver = ReferenceProfileResolver(conn)
    
    geo_type = geography_spec.get("type", "").lower()
    code = geography_spec.get("code") or geography_spec.get("fips") or geography_spec.get("state")
    
    if geo_type == "county":
        return resolver.resolve_county(code)
    elif geo_type == "state":
        return resolver.resolve_state(code)
    else:
        raise ValueError(f"Unsupported geography type: {geo_type}")


def list_counties(
    conn: duckdb.DuckDBPyConnection,
    state_abbr: Optional[str] = None
) -> list[dict]:
    """List available counties in reference data.
    
    Args:
        conn: DuckDB connection
        state_abbr: Optional state filter
        
    Returns:
        List of dicts with county info
    """
    query = """
        SELECT countyfips, countyname, stateabbr, totalpopulation
        FROM population.places_county
    """
    if state_abbr:
        query += " WHERE stateabbr = ?"
        result = conn.execute(query, [state_abbr]).fetchall()
    else:
        result = conn.execute(query).fetchall()
    
    return [
        {
            "fips": r[0],
            "name": r[1],
            "state": r[2],
            "population": r[3]
        }
        for r in result
    ]


def list_states(conn: duckdb.DuckDBPyConnection) -> list[dict]:
    """List available states in reference data.
    
    Args:
        conn: DuckDB connection
        
    Returns:
        List of dicts with state info
    """
    query = """
        SELECT stateabbr, SUM(totalpopulation) as total_pop, COUNT(*) as county_count
        FROM population.places_county
        GROUP BY stateabbr
        ORDER BY stateabbr
    """
    result = conn.execute(query).fetchall()
    
    return [
        {
            "abbr": r[0],
            "population": r[1],
            "county_count": r[2]
        }
        for r in result
    ]



def merge_profile_with_reference(
    base_spec: dict,
    reference_profile: DemographicProfile,
) -> dict:
    """Merge user profile specification with reference profile data.
    
    Creates a hybrid profile where:
    - Reference demographics fill in missing values
    - User-specified values override reference data
    - Clinical prevalences come from reference if not specified
    
    Args:
        base_spec: User's profile specification (may be partial)
        reference_profile: DemographicProfile from PopulationSim
        
    Returns:
        Complete profile specification with merged values
        
    Example:
        >>> user_spec = {
        ...     "profile": {
        ...         "demographics": {
        ...             "source": "populationsim",
        ...             "reference": {"type": "county", "fips": "48201"},
        ...             "age": {"type": "normal", "mean": 72}  # Override
        ...         }
        ...     }
        ... }
        >>> merged = merge_profile_with_reference(user_spec, ref_profile)
    """
    import copy
    merged = copy.deepcopy(base_spec)
    profile = merged.get("profile", {})
    
    # Get or create sections
    demographics = profile.setdefault("demographics", {})
    clinical = profile.setdefault("clinical", {})
    
    # Build reference age distribution if not overridden
    if "age" not in demographics:
        age_bands = {}
        if reference_profile.pct_age_under_17 > 0:
            age_bands["0-17"] = reference_profile.pct_age_under_17 / 100
        if reference_profile.pct_age_18_64 > 0:
            age_bands["18-34"] = (reference_profile.pct_age_18_64 * 0.35) / 100
            age_bands["35-54"] = (reference_profile.pct_age_18_64 * 0.40) / 100
            age_bands["55-64"] = (reference_profile.pct_age_18_64 * 0.25) / 100
        if reference_profile.pct_age_65_plus > 0:
            age_bands["65+"] = reference_profile.pct_age_65_plus / 100
        
        # Normalize
        total = sum(age_bands.values())
        if total > 0:
            age_bands = {k: v/total for k, v in age_bands.items()}
            demographics["age"] = {"type": "age_bands", "bands": age_bands}
    
    # Build reference gender distribution if not overridden
    if "gender" not in demographics:
        demographics["gender"] = {
            "type": "categorical",
            "weights": {
                "M": reference_profile.pct_male / 100,
                "F": reference_profile.pct_female / 100
            }
        }
    
    # Add reference clinical conditions if none specified
    if "conditions" not in clinical and "primary_condition" not in clinical:
        conditions = []
        
        if reference_profile.pct_diabetes > 1:
            conditions.append({
                "code": "E11", 
                "description": "Type 2 diabetes",
                "prevalence": reference_profile.pct_diabetes / 100
            })
        if reference_profile.pct_obesity > 1:
            conditions.append({
                "code": "E66",
                "description": "Obesity", 
                "prevalence": reference_profile.pct_obesity / 100
            })
        if reference_profile.pct_hypertension > 1:
            conditions.append({
                "code": "I10",
                "description": "Essential hypertension",
                "prevalence": reference_profile.pct_hypertension / 100
            })
        if reference_profile.pct_asthma > 1:
            conditions.append({
                "code": "J45",
                "description": "Asthma",
                "prevalence": reference_profile.pct_asthma / 100
            })
        if reference_profile.pct_heart_disease > 1:
            conditions.append({
                "code": "I25",
                "description": "Ischemic heart disease",
                "prevalence": reference_profile.pct_heart_disease / 100
            })
        if reference_profile.pct_depression > 1:
            conditions.append({
                "code": "F32",
                "description": "Depression",
                "prevalence": reference_profile.pct_depression / 100
            })
        
        if conditions:
            clinical["conditions"] = conditions
    
    # Add reference metadata
    profile["_reference"] = {
        "geography": {
            "level": reference_profile.geography.level.value,
            "code": reference_profile.geography.code,
            "name": reference_profile.geography.name,
        },
        "population": reference_profile.population,
        "source": "populationsim"
    }
    
    merged["profile"] = profile
    return merged


def create_hybrid_profile(
    user_spec: dict,
    conn: "duckdb.DuckDBPyConnection"
) -> dict:
    """Create a hybrid profile from user spec and reference data.
    
    If the user spec references PopulationSim data, resolves the
    reference and merges it with user overrides.
    
    Args:
        user_spec: User's profile specification
        conn: DuckDB connection for PopulationSim data
        
    Returns:
        Complete profile specification
        
    Example:
        >>> spec = {
        ...     "profile": {
        ...         "id": "harris-diabetic",
        ...         "generation": {"count": 200},
        ...         "demographics": {
        ...             "source": "populationsim",
        ...             "reference": {"type": "county", "fips": "48201"},
        ...             "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65}
        ...         },
        ...         "clinical": {
        ...             "primary_condition": {"code": "E11", "prevalence": 1.0}
        ...         }
        ...     }
        ... }
        >>> hybrid = create_hybrid_profile(spec, conn)
        # Uses PopulationSim for gender, adds age override, user clinical
    """
    profile = user_spec.get("profile", {})
    demographics = profile.get("demographics", {})
    
    # Check if reference data is requested
    source = demographics.get("source", "").lower()
    reference = demographics.get("reference", {})
    
    if source == "populationsim" and reference:
        # Resolve the reference
        ref_profile = resolve_geography(reference, conn)
        
        # Merge with user spec
        return merge_profile_with_reference(user_spec, ref_profile)
    
    # No reference requested, return as-is
    return user_spec


def resolve_provider_reference(
    reference: dict,
    conn: "duckdb.DuckDBPyConnection",
    limit: int = 100
) -> list[dict]:
    """Resolve provider reference to actual provider data from NetworkSim.
    
    Args:
        reference: Provider search criteria
            - state: 2-letter state abbreviation (required)
            - city: City name (optional)
            - specialty: Specialty name or taxonomy code (optional)
            - entity_type: "individual" or "organization" (optional)
        conn: DuckDB connection with network schema
        limit: Maximum providers to return
        
    Returns:
        List of provider dictionaries with NPI, name, location, specialty
        
    Example:
        >>> ref = {"state": "TX", "specialty": "internal_medicine"}
        >>> providers = resolve_provider_reference(ref, conn)
        >>> len(providers)  # Up to 100 TX internists
    """
    from .networksim_reference import NetworkSimResolver, TAXONOMY_MAP
    
    resolver = NetworkSimResolver(conn)
    
    state = reference.get("state")
    city = reference.get("city")
    specialty = reference.get("specialty")
    entity_type = reference.get("entity_type")
    
    # Convert specialty name to taxonomy code if needed
    taxonomy = None
    if specialty:
        taxonomy = TAXONOMY_MAP.get(specialty, specialty)
    
    providers = resolver.find_providers(
        state=state,
        city=city,
        taxonomy=taxonomy,
        entity_type=entity_type,
        limit=limit
    )
    
    return [
        {
            "npi": p.npi,
            "name": p.display_name,
            "entity_type": p.entity_type.value,
            "state": p.practice_state,
            "city": p.practice_city,
            "zip": p.practice_zip,
            "specialty": p.primary_taxonomy,
        }
        for p in providers
    ]


def resolve_facility_reference(
    reference: dict,
    conn: "duckdb.DuckDBPyConnection",
    limit: int = 50
) -> list[dict]:
    """Resolve facility reference to actual facility data from NetworkSim.
    
    Args:
        reference: Facility search criteria
            - state: 2-letter state abbreviation (required)
            - city: City name (optional)
            - type: Facility type (hospital, snf, hha, etc.) (optional)
            - min_beds: Minimum bed count (optional)
        conn: DuckDB connection with network schema
        limit: Maximum facilities to return
        
    Returns:
        List of facility dictionaries with CCN, name, type, location
        
    Example:
        >>> ref = {"state": "TX", "type": "hospital", "min_beds": 100}
        >>> facilities = resolve_facility_reference(ref, conn)
    """
    from .networksim_reference import NetworkSimResolver, FacilityType
    
    resolver = NetworkSimResolver(conn)
    
    state = reference.get("state")
    city = reference.get("city")
    facility_type_str = reference.get("type")
    min_beds = reference.get("min_beds")
    
    # Convert type string to enum if provided
    facility_type = None
    if facility_type_str:
        try:
            facility_type = FacilityType(facility_type_str.lower())
        except ValueError:
            pass  # Use None if invalid type
    
    facilities = resolver.find_facilities(
        state=state,
        city=city,
        facility_type=facility_type,
        min_beds=min_beds,
        limit=limit
    )
    
    return [
        {
            "ccn": f.ccn,
            "name": f.name,
            "type": f.facility_type or "other",
            "state": f.state,
            "city": f.city,
            "zip": f.zip_code,
            "beds": f.beds,
        }
        for f in facilities
    ]


def create_hybrid_profile_with_network(
    user_spec: dict,
    conn: "duckdb.DuckDBPyConnection"
) -> dict:
    """Create a hybrid profile with PopulationSim demographics AND NetworkSim providers.
    
    Extends create_hybrid_profile() to also resolve provider and facility
    references from NetworkSim data.
    
    Args:
        user_spec: User's profile specification with optional:
            - demographics.source = "populationsim"
            - providers.source = "networksim"
            - facilities.source = "networksim"
        conn: DuckDB connection for both PopulationSim and NetworkSim data
        
    Returns:
        Complete profile specification with resolved references
        
    Example:
        >>> spec = {
        ...     "profile": {
        ...         "id": "harris-diabetic-with-pcp",
        ...         "generation": {"count": 100},
        ...         "demographics": {
        ...             "source": "populationsim",
        ...             "reference": {"type": "county", "fips": "48201"}
        ...         },
        ...         "providers": {
        ...             "source": "networksim",
        ...             "reference": {"state": "TX", "specialty": "internal_medicine"},
        ...             "assignment": "pcp"
        ...         },
        ...         "facilities": {
        ...             "source": "networksim", 
        ...             "reference": {"state": "TX", "type": "hospital"},
        ...             "assignment": "primary"
        ...         }
        ...     }
        ... }
        >>> hybrid = create_hybrid_profile_with_network(spec, conn)
    """
    # First, apply PopulationSim demographics if requested
    result = create_hybrid_profile(user_spec, conn)
    
    profile = result.get("profile", {})
    
    # Resolve provider reference if requested
    providers_config = profile.get("providers", {})
    if providers_config.get("source", "").lower() == "networksim":
        provider_ref = providers_config.get("reference", {})
        if provider_ref:
            resolved_providers = resolve_provider_reference(provider_ref, conn)
            
            # Add to profile
            profile["_providers"] = {
                "source": "networksim",
                "reference": provider_ref,
                "count": len(resolved_providers),
                "pool": resolved_providers[:20],  # Sample for context
                "assignment": providers_config.get("assignment"),
            }
    
    # Resolve facility reference if requested
    facilities_config = profile.get("facilities", {})
    if facilities_config.get("source", "").lower() == "networksim":
        facility_ref = facilities_config.get("reference", {})
        if facility_ref:
            resolved_facilities = resolve_facility_reference(facility_ref, conn)
            
            # Add to profile
            profile["_facilities"] = {
                "source": "networksim",
                "reference": facility_ref,
                "count": len(resolved_facilities),
                "pool": resolved_facilities[:10],  # Sample for context
                "assignment": facilities_config.get("assignment"),
            }
    
    result["profile"] = profile
    return result
