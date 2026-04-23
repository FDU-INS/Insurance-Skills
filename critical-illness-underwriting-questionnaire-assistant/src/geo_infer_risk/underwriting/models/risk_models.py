"""
Risk Models: Data structures for risk assessment and profiling.

This module provides data models for risk profiles including:
- Risk profile structures for underwriting
- Exposure and vulnerability profiles
- Risk scoring and assessment models
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

class RiskLevel(Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskCategory(Enum):
    """Risk category enumeration."""
    PROPERTY = "property"
    LIABILITY = "liability"
    BUSINESS_INTERRUPTION = "business_interruption"
    CATASTROPHE = "catastrophe"
    CYBER = "cyber"
    REPUTATIONAL = "reputational"

@dataclass
class RiskProfile:
    """Comprehensive risk profile for underwriting assessment."""

    profile_id: str
    entity_id: str  # Policyholder, property, or business ID
    entity_type: str  # individual, business, property, portfolio

    # Risk scores
    overall_risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.MEDIUM
    risk_categories: Dict[RiskCategory, float] = field(default_factory=dict)

    # Risk factors
    location_risk: float = 0.0
    historical_risk: float = 0.0
    operational_risk: float = 0.0
    financial_risk: float = 0.0

    # Confidence and uncertainty
    confidence_level: float = 0.8
    uncertainty_range: float = 0.1

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    assessment_method: str = "comprehensive"
    data_sources: List[str] = field(default_factory=list)

    def calculate_weighted_risk_score(self, weights: Optional[Dict[str, float]] = None) -> float:
        """Calculate weighted risk score."""
        if weights is None:
            weights = {
                'location_risk': 0.3,
                'historical_risk': 0.25,
                'operational_risk': 0.2,
                'financial_risk': 0.15
            }

        weighted_score = (
            weights.get('location_risk', 0.3) * self.location_risk +
            weights.get('historical_risk', 0.25) * self.historical_risk +
            weights.get('operational_risk', 0.2) * self.operational_risk +
            weights.get('financial_risk', 0.15) * self.financial_risk
        )

        return min(1.0, max(0.0, weighted_score))

    def update_risk_level(self) -> None:
        """Update risk level based on overall risk score."""
        if self.overall_risk_score < 0.3:
            self.risk_level = RiskLevel.LOW
        elif self.overall_risk_score < 0.6:
            self.risk_level = RiskLevel.MEDIUM
        elif self.overall_risk_score < 0.8:
            self.risk_level = RiskLevel.HIGH
        else:
            self.risk_level = RiskLevel.CRITICAL

    def to_dict(self) -> Dict[str, Any]:
        """Convert risk profile to dictionary."""
        return {
            'profile_id': self.profile_id,
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'overall_risk_score': self.overall_risk_score,
            'risk_level': self.risk_level.value,
            'risk_categories': {k.value: v for k, v in self.risk_categories.items()},
            'location_risk': self.location_risk,
            'historical_risk': self.historical_risk,
            'operational_risk': self.operational_risk,
            'financial_risk': self.financial_risk,
            'confidence_level': self.confidence_level,
            'uncertainty_range': self.uncertainty_range,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'assessment_method': self.assessment_method,
            'data_sources': self.data_sources
        }

@dataclass
class ExposureProfile:
    """Exposure profile for risk assessment."""

    profile_id: str
    entity_id: str
    exposure_type: str

    # Exposure metrics
    total_value: float = 0.0
    replacement_cost: float = 0.0
    market_value: float = 0.0

    # Spatial information
    location: Dict[str, float] = field(default_factory=dict)
    area: float = 0.0
    elevation: float = 0.0

    # Temporal information
    time_variants: Dict[str, float] = field(default_factory=dict)
    seasonality_factors: Dict[str, float] = field(default_factory=dict)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    data_sources: List[str] = field(default_factory=list)

    def calculate_value_at_risk(self, confidence_level: float = 0.95) -> float:
        """Calculate value at risk for the exposure."""
        return self.total_value * (1 - confidence_level)

    def get_seasonal_adjustment(self, season: str) -> float:
        """Get seasonal adjustment factor."""
        return self.seasonality_factors.get(season, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exposure profile to dictionary."""
        return {
            'profile_id': self.profile_id,
            'entity_id': self.entity_id,
            'exposure_type': self.exposure_type,
            'total_value': self.total_value,
            'replacement_cost': self.replacement_cost,
            'market_value': self.market_value,
            'location': self.location,
            'area': self.area,
            'elevation': self.elevation,
            'time_variants': self.time_variants,
            'seasonality_factors': self.seasonality_factors,
            'created_at': self.created_at.isoformat(),
            'data_sources': self.data_sources
        }

@dataclass
class VulnerabilityProfile:
    """Vulnerability profile for risk assessment."""

    profile_id: str
    entity_id: str
    vulnerability_type: str

    # Vulnerability metrics
    vulnerability_score: float = 0.0
    damage_ratios: Dict[str, float] = field(default_factory=dict)
    recovery_time: float = 0.0

    # Asset characteristics
    construction_type: str = ""
    building_age: int = 0
    occupancy_type: str = ""

    # Environmental factors
    soil_type: str = ""
    flood_zone: str = ""
    seismic_zone: str = ""

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    assessment_method: str = "comprehensive"

    def get_damage_ratio(self, hazard_type: str) -> float:
        """Get damage ratio for specific hazard."""
        return self.damage_ratios.get(hazard_type, 0.0)

    def calculate_expected_loss(self, hazard_intensity: float) -> float:
        """Calculate expected loss for given hazard intensity."""
        # Simplified calculation - in practice would use vulnerability curves
        return self.vulnerability_score * hazard_intensity

    def to_dict(self) -> Dict[str, Any]:
        """Convert vulnerability profile to dictionary."""
        return {
            'profile_id': self.profile_id,
            'entity_id': self.entity_id,
            'vulnerability_type': self.vulnerability_type,
            'vulnerability_score': self.vulnerability_score,
            'damage_ratios': self.damage_ratios,
            'recovery_time': self.recovery_time,
            'construction_type': self.construction_type,
            'building_age': self.building_age,
            'occupancy_type': self.occupancy_type,
            'soil_type': self.soil_type,
            'flood_zone': self.flood_zone,
            'seismic_zone': self.seismic_zone,
            'created_at': self.created_at.isoformat(),
            'assessment_method': self.assessment_method
        }
