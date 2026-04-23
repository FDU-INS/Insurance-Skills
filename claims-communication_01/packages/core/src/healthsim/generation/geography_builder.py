"""Geography-aware profile builder.

Combines PopulationSim demographics (CDC PLACES, SVI) with NetworkSim
provider/facility data to create geographically realistic profiles.

This is the integration layer that connects:
- PopulationSim: Population demographics, health indicators, SDOH
- NetworkSim: Providers, facilities, quality metrics

Usage:
    from healthsim.generation.geography_builder import (
        GeographyAwareProfileBuilder,
        create_geography_profile,
    )
    
    # Build profile for Harris County, TX
    builder = GeographyAwareProfileBuilder(conn)
    profile = builder.build_profile(
        geography={"type": "county", "fips": "48201"},
        include_providers=True,
        specialties=["internal_medicine", "endocrinology"],
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional
import duckdb

from healthsim.generation.reference_profiles import (
    DemographicProfile,
    GeographyLevel,
    GeographyReference,
    ReferenceProfileResolver,
    merge_profile_with_reference,
    resolve_geography,
)
from healthsim.generation.networksim_reference import (
    NetworkSimResolver,
    Provider,
    Facility,
    TAXONOMY_MAP,
    get_providers_by_geography,
    get_facilities_by_geography,
)


@dataclass
class GeographyProfile:
    """Complete geography-aware profile.
    
    Combines demographic data from PopulationSim with provider/facility
    data from NetworkSim for a specific geographic area.
    """
    # Geography identification
    geography: GeographyReference
    
    # Demographics (from PopulationSim)
    demographics: DemographicProfile
    
    # Provider pool (from NetworkSim)
    primary_care_providers: list[Provider] = field(default_factory=list)
    specialty_providers: dict[str, list[Provider]] = field(default_factory=dict)
    
    # Facility pool (from NetworkSim)
    hospitals: list[Facility] = field(default_factory=list)
    snfs: list[Facility] = field(default_factory=list)
    other_facilities: list[Facility] = field(default_factory=list)
    
    # Metadata
    provider_count: int = 0
    facility_count: int = 0
    
    def get_providers_for_specialty(self, specialty: str) -> list[Provider]:
        """Get providers for a specific specialty."""
        return self.specialty_providers.get(specialty, [])
    
    def get_random_pcp(self, seed: int | None = None) -> Optional[Provider]:
        """Get a random primary care provider."""
        import random
        if seed is not None:
            random.seed(seed)
        if self.primary_care_providers:
            return random.choice(self.primary_care_providers)
        return None
    
    def get_random_specialist(
        self,
        specialty: str,
        seed: int | None = None
    ) -> Optional[Provider]:
        """Get a random specialist provider."""
        import random
        if seed is not None:
            random.seed(seed)
        providers = self.specialty_providers.get(specialty, [])
        if providers:
            return random.choice(providers)
        return None
    
    def get_random_hospital(self, seed: int | None = None) -> Optional[Facility]:
        """Get a random hospital."""
        import random
        if seed is not None:
            random.seed(seed)
        if self.hospitals:
            return random.choice(self.hospitals)
        return None
    
    def to_profile_spec(self) -> dict:
        """Convert to profile specification dict."""
        spec = {
            "profile": {
                "id": f"geo-{self.geography.code}",
                "demographics": {
                    "source": "populationsim",
                    "reference": {
                        "type": self.geography.level.value,
                        "code": self.geography.code,
                        "name": self.geography.name,
                    }
                },
                "_geography_profile": {
                    "provider_count": self.provider_count,
                    "facility_count": self.facility_count,
                    "primary_care_count": len(self.primary_care_providers),
                    "hospital_count": len(self.hospitals),
                    "specialties_available": list(self.specialty_providers.keys()),
                }
            }
        }
        return spec


class GeographyAwareProfileBuilder:
    """Builds geography-aware profiles combining PopulationSim and NetworkSim.
    
    Example:
        >>> conn = duckdb.connect("healthsim.duckdb", read_only=True)
        >>> builder = GeographyAwareProfileBuilder(conn)
        >>> 
        >>> # Simple profile for a county
        >>> profile = builder.build_profile(
        ...     geography={"type": "county", "fips": "48201"}
        ... )
        >>> 
        >>> # Profile with specific specialties
        >>> profile = builder.build_profile(
        ...     geography={"type": "county", "fips": "48201"},
        ...     specialties=["cardiology", "endocrinology", "nephrology"],
        ...     max_providers_per_specialty=50,
        ... )
        >>> 
        >>> # Use the profile
        >>> pcp = profile.get_random_pcp(seed=42)
        >>> specialist = profile.get_random_specialist("cardiology", seed=42)
    """
    
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        """Initialize builder with database connection.
        
        Args:
            conn: DuckDB connection with both PopulationSim and NetworkSim data
        """
        self.conn = conn
        self.pop_resolver = ReferenceProfileResolver(conn)
        self.net_resolver = NetworkSimResolver(conn)
    
    def build_profile(
        self,
        geography: dict,
        include_providers: bool = True,
        include_facilities: bool = True,
        specialties: list[str] | None = None,
        max_providers_per_specialty: int = 100,
        max_facilities_per_type: int = 50,
    ) -> GeographyProfile:
        """Build a complete geography-aware profile.
        
        Args:
            geography: Geography specification dict with 'type' and 'fips'/'code'
            include_providers: Whether to include provider data
            include_facilities: Whether to include facility data
            specialties: List of specialty keys (from TAXONOMY_MAP) to include
            max_providers_per_specialty: Maximum providers per specialty
            max_facilities_per_type: Maximum facilities per type
            
        Returns:
            GeographyProfile with demographics and provider/facility pools
        """
        # Resolve demographics from PopulationSim
        demographics = resolve_geography(geography, self.conn)
        
        # Create geography reference
        geo_ref = GeographyReference(
            level=demographics.geography.level,
            code=demographics.geography.code,
            name=demographics.geography.name,
        )
        
        # Get state from geography for provider/facility lookup
        state = self._get_state_from_geography(geography, demographics)
        city = self._get_city_from_geography(geography, demographics)
        
        # Build result
        profile = GeographyProfile(
            geography=geo_ref,
            demographics=demographics,
        )
        
        # Add providers if requested
        if include_providers and state:
            profile = self._add_providers(
                profile,
                state=state,
                city=city,
                specialties=specialties,
                max_per_specialty=max_providers_per_specialty,
            )
        
        # Add facilities if requested
        if include_facilities and state:
            profile = self._add_facilities(
                profile,
                state=state,
                city=city,
                max_per_type=max_facilities_per_type,
            )
        
        return profile
    
    def _get_state_from_geography(
        self,
        geography: dict,
        demographics: DemographicProfile,
    ) -> Optional[str]:
        """Extract state from geography or demographics."""
        geo_type = geography.get("type", "").lower()
        
        if geo_type == "state":
            return geography.get("code") or geography.get("state")
        
        # For county/tract, look up state from raw data
        if demographics.raw_places:
            return demographics.raw_places.get("stateabbr")
        if demographics.raw_svi:
            return demographics.raw_svi.get("st_abbr")
        
        return None
    
    def _get_city_from_geography(
        self,
        geography: dict,
        demographics: DemographicProfile,
    ) -> Optional[str]:
        """Extract city from geography if available."""
        # Cities aren't directly in SVI/PLACES, would need additional lookup
        # For now, return None and search at state level
        return None
    
    def _add_providers(
        self,
        profile: GeographyProfile,
        state: str,
        city: Optional[str],
        specialties: list[str] | None,
        max_per_specialty: int,
    ) -> GeographyProfile:
        """Add providers to profile."""
        # Primary care providers (Internal Medicine, Family Medicine)
        pcp_taxonomies = [
            TAXONOMY_MAP["internal_medicine"],
            TAXONOMY_MAP["family_medicine"],
            TAXONOMY_MAP["general_practice"],
        ]
        
        pcps = []
        for taxonomy in pcp_taxonomies:
            providers = self.net_resolver.find_providers(
                state=state,
                city=city,
                taxonomy=taxonomy,
                limit=max_per_specialty // 3,
                random_sample=True,
            )
            pcps.extend(providers)
        
        profile.primary_care_providers = pcps[:max_per_specialty]
        profile.provider_count += len(profile.primary_care_providers)
        
        # Specialty providers
        if specialties:
            for specialty in specialties:
                taxonomy = TAXONOMY_MAP.get(specialty.lower().replace(" ", "_"), specialty)
                providers = self.net_resolver.find_providers(
                    state=state,
                    city=city,
                    taxonomy=taxonomy,
                    limit=max_per_specialty,
                    random_sample=True,
                )
                if providers:
                    profile.specialty_providers[specialty] = providers
                    profile.provider_count += len(providers)
        
        return profile
    
    def _add_facilities(
        self,
        profile: GeographyProfile,
        state: str,
        city: Optional[str],
        max_per_type: int,
    ) -> GeographyProfile:
        """Add facilities to profile."""
        # Hospitals
        hospitals = self.net_resolver.find_facilities(
            state=state,
            city=city,
            facility_type="hospital",
            limit=max_per_type,
            random_sample=True,
        )
        profile.hospitals = hospitals
        profile.facility_count += len(hospitals)
        
        # SNFs
        snfs = self.net_resolver.find_facilities(
            state=state,
            city=city,
            facility_type="snf",
            limit=max_per_type,
            random_sample=True,
        )
        profile.snfs = snfs
        profile.facility_count += len(snfs)
        
        return profile
    
    def build_multi_geography_profile(
        self,
        geographies: list[dict],
        **kwargs,
    ) -> list[GeographyProfile]:
        """Build profiles for multiple geographies.
        
        Useful for building profiles across multiple counties, states, etc.
        
        Args:
            geographies: List of geography specifications
            **kwargs: Arguments passed to build_profile
            
        Returns:
            List of GeographyProfile objects
        """
        return [
            self.build_profile(geo, **kwargs)
            for geo in geographies
        ]


# =============================================================================
# Convenience Functions
# =============================================================================

def create_geography_profile(
    conn: duckdb.DuckDBPyConnection,
    geography: dict,
    **kwargs,
) -> GeographyProfile:
    """Create a geography-aware profile.
    
    Convenience function that creates builder and builds profile in one call.
    
    Args:
        conn: DuckDB connection
        geography: Geography specification
        **kwargs: Arguments passed to build_profile
        
    Returns:
        GeographyProfile
    """
    builder = GeographyAwareProfileBuilder(conn)
    return builder.build_profile(geography, **kwargs)


def build_cohort_with_geography(
    conn: duckdb.DuckDBPyConnection,
    geography: dict,
    count: int,
    specialties: list[str] | None = None,
    seed: int | None = None,
) -> dict:
    """Build a cohort specification using geography-aware profile.
    
    Creates a complete cohort specification that uses PopulationSim
    demographics and includes assigned providers/facilities.
    
    Args:
        conn: DuckDB connection
        geography: Geography specification
        count: Number of entities to generate
        specialties: Specialties needed for the cohort
        seed: Random seed for reproducibility
        
    Returns:
        Profile specification dict ready for ProfileExecutor
    """
    # Build the geography profile
    profile = create_geography_profile(
        conn,
        geography,
        specialties=specialties,
    )
    
    # Convert demographics to profile spec
    base_spec = profile.to_profile_spec()
    
    # Add generation settings
    base_spec["profile"]["generation"] = {
        "count": count,
        "seed": seed,
    }
    
    # Add provider/facility metadata
    if profile.primary_care_providers:
        base_spec["profile"]["_assigned_providers"] = {
            "primary_care": [
                {"npi": p.npi, "name": p.display_name}
                for p in profile.primary_care_providers[:10]  # Sample
            ],
        }
    
    if profile.hospitals:
        base_spec["profile"]["_assigned_facilities"] = {
            "hospitals": [
                {"ccn": f.ccn, "name": f.name}
                for f in profile.hospitals[:5]  # Sample
            ],
        }
    
    return base_spec


def get_provider_for_entity(
    geography_profile: GeographyProfile,
    specialty: str | None = None,
    entity_seed: int | None = None,
) -> Optional[Provider]:
    """Get a provider for an entity from the geography profile.
    
    Args:
        geography_profile: Pre-built geography profile with provider pools
        specialty: Specialty to match (None for PCP)
        entity_seed: Seed for reproducible selection
        
    Returns:
        Provider or None if no match
    """
    if specialty:
        return geography_profile.get_random_specialist(specialty, seed=entity_seed)
    return geography_profile.get_random_pcp(seed=entity_seed)


def get_facility_for_entity(
    geography_profile: GeographyProfile,
    facility_type: str = "hospital",
    entity_seed: int | None = None,
) -> Optional[Facility]:
    """Get a facility for an entity from the geography profile.
    
    Args:
        geography_profile: Pre-built geography profile with facility pools
        facility_type: Type of facility needed
        entity_seed: Seed for reproducible selection
        
    Returns:
        Facility or None if no match
    """
    import random
    if entity_seed is not None:
        random.seed(entity_seed)
    
    if facility_type == "hospital":
        return geography_profile.get_random_hospital(seed=entity_seed)
    elif facility_type == "snf":
        if geography_profile.snfs:
            return random.choice(geography_profile.snfs)
    
    return None


__all__ = [
    "GeographyProfile",
    "GeographyAwareProfileBuilder",
    "create_geography_profile",
    "build_cohort_with_geography",
    "get_provider_for_entity",
    "get_facility_for_entity",
]
