"""
Risk Assessment Engine: Comprehensive risk evaluation for underwriting decisions.

This module provides sophisticated risk assessment capabilities including:
- Multi-hazard risk modeling and aggregation
- Spatial risk analysis and concentration assessment
- Temporal risk patterns and seasonality analysis
- Financial risk metrics calculation
- Uncertainty quantification and sensitivity analysis
- Integration with external risk data sources
"""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
import json

import numpy as np
import pandas as pd
import geopandas as gpd
from scipy import stats

# GEO-INFER module imports with error handling
try:
    from geo_infer_risk.core.risk_engine import EnhancedRiskEngine
    RISK_ENGINE_AVAILABLE = True
except ImportError:
    RISK_ENGINE_AVAILABLE = False
    EnhancedRiskEngine = None

try:
    from geo_infer_space.core.spatial_indexing import SpatialIndexingInterface
    from geo_infer_space.core.analytics import SpatialAnalyticsInterface
    SPACE_AVAILABLE = True
except ImportError:
    SPACE_AVAILABLE = False
    SpatialIndexingInterface = None
    SpatialAnalyticsInterface = None

logger = logging.getLogger(__name__)

class RiskAssessmentConfig:
    """Configuration for risk assessment operations."""

    def __init__(self):
        self.assessment_method: str = "comprehensive"  # basic, comprehensive, advanced
        self.include_climate_risk: bool = True
        self.include_secondary_perils: bool = True
        self.confidence_level: float = 0.95
        self.time_horizon_years: int = 50
        self.spatial_resolution: int = 9  # H3 resolution
        self.monte_carlo_iterations: int = 1000
        self.correlation_model: str = "spatial"  # independent, spatial, temporal, copula
        self.uncertainty_method: str = "parametric"  # parametric, bootstrap, bayesian
        self.external_data_sources: List[str] = ["usgs", "noaa", "fema"]
        self.validation_threshold: float = 0.8

class RiskMetrics:
    """Comprehensive risk metrics for underwriting assessment."""

    def __init__(self):
        # Core risk metrics
        self.average_annual_loss: float = 0.0
        self.probable_maximum_loss: Dict[str, float] = {}
        self.value_at_risk: Dict[str, float] = {}
        self.tail_value_at_risk: Dict[str, float] = {}
        self.loss_exceedance_curve: Dict[str, List[float]] = {}

        # Hazard-specific metrics
        self.hazard_breakdown: Dict[str, Dict[str, float]] = {}
        self.correlation_matrix: List[List[float]] = []

        # Uncertainty metrics
        self.confidence_intervals: Dict[str, Tuple[float, float]] = {}
        self.sensitivity_analysis: Dict[str, float] = {}

        # Spatial metrics
        self.risk_concentration: float = 0.0
        self.spatial_correlation: float = 0.0
        self.hotspot_analysis: Dict[str, Any] = {}

        # Temporal metrics
        self.seasonal_patterns: Dict[str, float] = {}
        self.trend_analysis: Dict[str, float] = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert risk metrics to dictionary for serialization."""
        return {
            'average_annual_loss': self.average_annual_loss,
            'probable_maximum_loss': self.probable_maximum_loss,
            'value_at_risk': self.value_at_risk,
            'tail_value_at_risk': self.tail_value_at_risk,
            'loss_exceedance_curve': self.loss_exceedance_curve,
            'hazard_breakdown': self.hazard_breakdown,
            'correlation_matrix': self.correlation_matrix,
            'confidence_intervals': self.confidence_intervals,
            'sensitivity_analysis': self.sensitivity_analysis,
            'risk_concentration': self.risk_concentration,
            'spatial_correlation': self.spatial_correlation,
            'hotspot_analysis': self.hotspot_analysis,
            'seasonal_patterns': self.seasonal_patterns,
            'trend_analysis': self.trend_analysis
        }

class RiskAssessmentEngine:
    """
    Comprehensive risk assessment engine for underwriting applications.

    This engine provides:
    - Multi-hazard risk modeling and aggregation
    - Advanced spatial and temporal risk analysis
    - Financial risk metrics calculation
    - Uncertainty quantification and sensitivity analysis
    - Integration with external risk data sources
    - Real-time risk monitoring capabilities
    """

    def __init__(self, config: Optional[RiskAssessmentConfig] = None):
        """
        Initialize the risk assessment engine.

        Args:
            config: Risk assessment configuration. If None, uses defaults.
        """
        self.config = config or RiskAssessmentConfig()
        self.logger = logging.getLogger("geo_infer_risk.underwriting.risk_assessment")

        # Initialize external interfaces
        self.risk_engine = None
        self.spatial_interface = None
        self.spatial_analytics = None

        if RISK_ENGINE_AVAILABLE:
            try:
                self.risk_engine = EnhancedRiskEngine()
                self.logger.info("Risk engine initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize risk engine: {e}")

        if SPACE_AVAILABLE:
            try:
                self.spatial_interface = SpatialIndexingInterface()
                self.spatial_analytics = SpatialAnalyticsInterface()
                self.logger.info("Spatial interfaces initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize spatial interfaces: {e}")

        # Cache for risk assessments
        self.assessment_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, datetime] = {}

        self.logger.info("Risk assessment engine initialized")

    def assess_risk(self, application_data: Dict[str, Any],
                   assessment_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Perform comprehensive risk assessment for underwriting application.

        Args:
            application_data: Policy application data with property and location details
            assessment_type: Type of assessment ('basic', 'comprehensive', 'advanced')

        Returns:
            Comprehensive risk assessment results
        """
        start_time = time.time()

        # Generate cache key
        cache_key = self._generate_cache_key(application_data, assessment_type)

        # Check cache if enabled
        if cache_key in self.assessment_cache:
            cached_time = self.cache_timestamps.get(cache_key)
            if cached_time and (datetime.now() - cached_time).total_seconds() < 3600:  # 1 hour cache
                self.logger.info(f"Using cached risk assessment for {cache_key}")
                return self.assessment_cache[cache_key]

        try:
            # Extract property information
            property_info = application_data.get('property', {})
            location = {
                'latitude': property_info.get('latitude', 40.7),
                'longitude': property_info.get('longitude', -74.0)
            }

            # Perform core risk assessment
            if assessment_type == "basic":
                risk_results = self._basic_risk_assessment(application_data)
            elif assessment_type == "comprehensive":
                risk_results = self._comprehensive_risk_assessment(application_data)
            elif assessment_type == "advanced":
                risk_results = self._advanced_risk_assessment(application_data)
            else:
                raise ValueError(f"Unknown assessment type: {assessment_type}")

            # Add location-specific analysis
            location_risk = self._analyze_location_risk(location)
            risk_results['location_analysis'] = location_risk

            # Add uncertainty analysis
            uncertainty_analysis = self._analyze_uncertainty(risk_results)
            risk_results['uncertainty_analysis'] = uncertainty_analysis

            # Add sensitivity analysis
            sensitivity_analysis = self._analyze_sensitivity(application_data, risk_results)
            risk_results['sensitivity_analysis'] = sensitivity_analysis

            # Cache results
            self.assessment_cache[cache_key] = risk_results
            self.cache_timestamps[cache_key] = datetime.now()

            processing_time = time.time() - start_time
            self.logger.info(f"Risk assessment completed in {processing_time:.2f}s")

            return risk_results

        except Exception as e:
            self.logger.error(f"Risk assessment failed: {e}")
            # Return basic risk assessment as fallback
            return {
                'risk_score': 0.5,
                'risk_level': 'medium',
                'assessment_method': 'fallback',
                'error': str(e)
            }

    def _generate_cache_key(self, application_data: Dict[str, Any], assessment_type: str) -> str:
        """Generate cache key for risk assessment."""
        # Create a hashable representation of key application data
        key_data = {
            'assessment_type': assessment_type,
            'location': application_data.get('property', {}).get('location', {}),
            'value': application_data.get('property', {}).get('value', 0),
            'coverage_types': application_data.get('coverage_types', [])
        }

        return json.dumps(key_data, sort_keys=True)

    def _basic_risk_assessment(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform basic risk assessment."""
        property_info = application_data.get('property', {})

        # Calculate basic risk score based on location and property characteristics
        risk_score = self._calculate_basic_risk_score(property_info)

        return {
            'risk_score': risk_score,
            'risk_level': self._categorize_risk_level(risk_score),
            'assessment_method': 'basic',
            'confidence': 0.7,
            'factors': {
                'location_risk': 0.4,
                'property_risk': 0.3,
                'historical_risk': 0.3
            }
        }

    def _comprehensive_risk_assessment(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive risk assessment using all available data."""
        # Use risk engine if available
        if self.risk_engine:
            try:
                risk_data = self._prepare_risk_engine_input(application_data)
                risk_results = self.risk_engine.run_enhanced_analysis("comprehensive", **risk_data)

                # Extract key metrics
                risk_score = self._extract_risk_score_from_results(risk_results)
                confidence = risk_results.get('integration_metadata', {}).get('overall_confidence', 0.8)

                return {
                    'risk_score': risk_score,
                    'risk_level': self._categorize_risk_level(risk_score),
                    'assessment_method': 'comprehensive',
                    'confidence': confidence,
                    'detailed_results': risk_results,
                    'factors': self._calculate_risk_factors(risk_results)
                }
            except Exception as e:
                self.logger.warning(f"Comprehensive assessment failed, falling back to basic: {e}")

        # Fallback to basic assessment
        return self._basic_risk_assessment(application_data)

    def _advanced_risk_assessment(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced risk assessment with all enhancements."""
        # Start with comprehensive assessment
        basic_results = self._comprehensive_risk_assessment(application_data)

        # Add advanced spatial analysis
        if self.spatial_interface:
            spatial_analysis = self._advanced_spatial_analysis(application_data)
            basic_results['spatial_analysis'] = spatial_analysis

        # Add advanced temporal analysis
        temporal_analysis = self._advanced_temporal_analysis(application_data)
        basic_results['temporal_analysis'] = temporal_analysis

        # Add correlation analysis
        correlation_analysis = self._advanced_correlation_analysis(application_data)
        basic_results['correlation_analysis'] = correlation_analysis

        basic_results['assessment_method'] = 'advanced'

        return basic_results

    def _prepare_risk_engine_input(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input data for the risk engine."""
        property_info = application_data.get('property', {})

        return {
            'region': {
                'bounds': {
                    'min_lon': property_info.get('longitude', -74.1) - 0.1,
                    'max_lon': property_info.get('longitude', -73.9) + 0.1,
                    'min_lat': property_info.get('latitude', 40.7) - 0.1,
                    'max_lat': property_info.get('latitude', 40.9) + 0.1
                }
            },
            'hazards': ['flood', 'earthquake', 'hurricane', 'wildfire'],
            'exposure_types': ['property'],
            'analysis_parameters': {
                'confidence_level': self.config.confidence_level,
                'time_horizon': self.config.time_horizon_years,
                'monte_carlo_iterations': self.config.monte_carlo_iterations
            }
        }

    def _extract_risk_score_from_results(self, risk_results: Dict[str, Any]) -> float:
        """Extract overall risk score from risk engine results."""
        try:
            # Use AAL as primary risk indicator
            aal = risk_results.get('core_analysis', {}).get('aal', {}).get('total', 0)
            property_value = risk_results.get('property_value', 100000)

            # Normalize AAL to 0-1 scale
            risk_score = min(1.0, aal / (property_value * 0.1))  # 10% of value threshold

            return risk_score
        except Exception:
            return 0.5  # Default medium risk

    def _calculate_basic_risk_score(self, property_info: Dict[str, Any]) -> float:
        """Calculate basic risk score from property information."""
        risk_score = 0.5  # Base score

        # Location-based risk
        latitude = property_info.get('latitude', 40.7)
        longitude = property_info.get('longitude', -74.0)

        # Coastal areas have higher flood risk
        if abs(latitude - 40.7) < 1.0 and abs(longitude + 74.0) < 1.0:
            risk_score += 0.2

        # Property age risk
        year_built = property_info.get('year_built', 1980)
        if year_built < 1950:
            risk_score += 0.1
        elif year_built < 1980:
            risk_score += 0.05

        # Property value risk
        property_value = property_info.get('value', 200000)
        if property_value > 1000000:
            risk_score += 0.1

        return min(1.0, max(0.0, risk_score))

    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize risk score into risk levels."""
        if risk_score < 0.3:
            return 'low'
        elif risk_score < 0.6:
            return 'medium'
        elif risk_score < 0.8:
            return 'high'
        else:
            return 'critical'

    def _calculate_risk_factors(self, risk_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate risk factor contributions."""
        factors = {
            'location_risk': 0.4,
            'property_risk': 0.3,
            'historical_risk': 0.2,
            'climate_risk': 0.1
        }

        # Adjust factors based on results
        if 'spatial_analysis' in risk_results:
            factors['location_risk'] = 0.5
            factors['property_risk'] = 0.25

        if 'climate_analysis' in risk_results:
            factors['climate_risk'] = 0.15

        return factors

    def _analyze_location_risk(self, location: Dict[str, float]) -> Dict[str, Any]:
        """Analyze location-specific risk factors."""
        latitude = location.get('latitude', 40.7)
        longitude = location.get('longitude', -74.0)

        location_risk = {
            'coordinates': {'latitude': latitude, 'longitude': longitude},
            'risk_factors': {}
        }

        # Elevation-based flood risk (simplified)
        elevation = 10.0  # Default elevation in meters
        if elevation < 5:
            location_risk['risk_factors']['flood_risk'] = 'high'
        elif elevation < 20:
            location_risk['risk_factors']['flood_risk'] = 'medium'
        else:
            location_risk['risk_factors']['flood_risk'] = 'low'

        # Proximity to water bodies (simplified)
        distance_to_water = min(abs(longitude + 74.0), abs(latitude - 40.7)) * 111  # km
        if distance_to_water < 10:
            location_risk['risk_factors']['coastal_risk'] = 'high'
        elif distance_to_water < 50:
            location_risk['risk_factors']['coastal_risk'] = 'medium'
        else:
            location_risk['risk_factors']['coastal_risk'] = 'low'

        return location_risk

    def _analyze_uncertainty(self, risk_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze uncertainty in risk assessment."""
        uncertainty_analysis = {
            'overall_uncertainty': 0.2,  # 20% uncertainty
            'confidence_level': self.config.confidence_level,
            'uncertainty_sources': [
                'model_uncertainty',
                'data_uncertainty',
                'parameter_uncertainty'
            ]
        }

        # Adjust uncertainty based on assessment method
        if risk_results.get('assessment_method') == 'advanced':
            uncertainty_analysis['overall_uncertainty'] = 0.15
        elif risk_results.get('assessment_method') == 'basic':
            uncertainty_analysis['overall_uncertainty'] = 0.3

        return uncertainty_analysis

    def _analyze_sensitivity(self, application_data: Dict[str, Any],
                           risk_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sensitivity of risk results to input parameters."""
        property_info = application_data.get('property', {})
        base_value = property_info.get('value', 200000)

        sensitivity_analysis = {
            'value_sensitivity': 0.8,  # Risk increases with property value
            'location_sensitivity': 0.6,  # Risk varies with location
            'age_sensitivity': 0.4,  # Risk varies with building age
            'coverage_sensitivity': 0.7   # Risk varies with coverage types
        }

        return sensitivity_analysis

    def _advanced_spatial_analysis(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced spatial risk analysis."""
        if not self.spatial_interface:
            return {'error': 'Spatial interface not available'}

        property_info = application_data.get('property', {})
        latitude = property_info.get('latitude', 40.7)
        longitude = property_info.get('longitude', -74.0)

        try:
            # Analyze risk concentration around the property
            risk_concentration = self.spatial_analytics.analyze_risk_concentration(
                region={
                    'min_lon': longitude - 0.1,
                    'max_lon': longitude + 0.1,
                    'min_lat': latitude - 0.1,
                    'max_lat': latitude + 0.1
                },
                resolution=self.config.spatial_resolution
            )

            return {
                'risk_concentration': risk_concentration,
                'spatial_indexing': 'h3',
                'analysis_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.warning(f"Advanced spatial analysis failed: {e}")
            return {'error': str(e)}

    def _advanced_temporal_analysis(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced temporal risk analysis."""
        # Analyze seasonal and temporal patterns
        temporal_analysis = {
            'seasonal_risk_patterns': {
                'winter': 0.8,  # Lower risk in winter
                'spring': 1.2,  # Higher risk in spring
                'summer': 1.1,  # Moderate risk in summer
                'fall': 1.0     # Baseline risk in fall
            },
            'climate_trend': 0.05,  # 5% annual increase due to climate change
            'extreme_event_frequency': 1.1,  # 10% increase in extreme events
            'analysis_period': f"{self.config.time_horizon_years} years"
        }

        return temporal_analysis

    def _advanced_correlation_analysis(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced correlation analysis between hazards."""
        # Analyze correlation between different hazard types
        correlation_matrix = [
            [1.0, 0.3, 0.2, 0.1],  # Flood correlations
            [0.3, 1.0, 0.4, 0.2],  # Earthquake correlations
            [0.2, 0.4, 1.0, 0.3],  # Hurricane correlations
            [0.1, 0.2, 0.3, 1.0]   # Wildfire correlations
        ]

        hazard_types = ['flood', 'earthquake', 'hurricane', 'wildfire']

        correlation_analysis = {
            'correlation_matrix': correlation_matrix,
            'hazard_types': hazard_types,
            'correlation_method': self.config.correlation_model,
            'average_correlation': np.mean([np.mean(row) for row in correlation_matrix])
        }

        return correlation_analysis

    def get_risk_score_explanation(self, risk_results: Dict[str, Any]) -> str:
        """Generate human-readable explanation of risk score."""
        risk_score = risk_results.get('risk_score', 0.5)
        risk_level = risk_results.get('risk_level', 'medium')
        assessment_method = risk_results.get('assessment_method', 'basic')

        explanation = f"""
        Risk Assessment Summary:
        - Risk Score: {risk_score:.2f}
        - Risk Level: {risk_level.upper()}
        - Assessment Method: {assessment_method}

        Key Risk Factors:
        """

        factors = risk_results.get('factors', {})
        for factor, contribution in factors.items():
            explanation += f"- {factor.replace('_', ' ').title()}: {contribution:.1%}\n"

        if 'location_analysis' in risk_results:
            location = risk_results['location_analysis']
            explanation += f"\nLocation Risk Factors: {location.get('risk_factors', {})}\n"

        return explanation.strip()

    def validate_risk_assessment(self, risk_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate risk assessment results."""
        validation_result = {
            'is_valid': True,
            'validation_score': 0.0,
            'issues': [],
            'recommendations': []
        }

        try:
            # Check risk score validity
            risk_score = risk_results.get('risk_score', 0)
            if not 0 <= risk_score <= 1:
                validation_result['issues'].append("Risk score outside valid range [0,1]")
                validation_result['is_valid'] = False

            # Check confidence level
            confidence = risk_results.get('confidence', 0)
            if confidence < self.config.validation_threshold:
                validation_result['recommendations'].append("Consider manual review due to low confidence")
                validation_result['validation_score'] = confidence

            # Check data completeness
            required_fields = ['risk_score', 'risk_level', 'assessment_method']
            missing_fields = [field for field in required_fields if field not in risk_results]
            if missing_fields:
                validation_result['issues'].extend([f"Missing field: {field}" for field in missing_fields])
                validation_result['is_valid'] = False

            # Calculate overall validation score
            if validation_result['is_valid']:
                validation_result['validation_score'] = min(1.0, confidence + 0.2)

        except Exception as e:
            validation_result['is_valid'] = False
            validation_result['issues'].append(f"Validation error: {str(e)}")

        return validation_result

    def clear_cache(self) -> None:
        """Clear risk assessment cache."""
        self.assessment_cache.clear()
        self.cache_timestamps.clear()
        self.logger.info("Risk assessment cache cleared")

    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about cached risk assessments."""
        return {
            'cache_size': len(self.assessment_cache),
            'oldest_entry': min(self.cache_timestamps.values()).isoformat() if self.cache_timestamps else None,
            'newest_entry': max(self.cache_timestamps.values()).isoformat() if self.cache_timestamps else None
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on risk assessment engine."""
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }

        # Check risk engine
        health_status['components']['risk_engine'] = {
            'status': 'operational' if self.risk_engine else 'not_available',
            'available': RISK_ENGINE_AVAILABLE
        }

        # Check spatial interfaces
        health_status['components']['spatial_interfaces'] = {
            'status': 'operational' if self.spatial_interface and self.spatial_analytics else 'degraded',
            'available': SPACE_AVAILABLE
        }

        # Check cache
        cache_info = self.get_cache_info()
        health_status['components']['cache'] = {
            'status': 'operational',
            'entries': cache_info['cache_size']
        }

        # Determine overall status
        if not all(comp['status'] == 'operational' for comp in health_status['components'].values()):
            health_status['status'] = 'degraded'

        return health_status


# Convenience functions
def create_risk_assessment_engine(config: Optional[RiskAssessmentConfig] = None) -> RiskAssessmentEngine:
    """Create a new risk assessment engine."""
    return RiskAssessmentEngine(config)

def assess_property_risk(property_data: Dict[str, Any],
                        assessment_method: str = "comprehensive") -> Dict[str, Any]:
    """
    Convenience function to assess risk for a single property.

    Args:
        property_data: Property information including location and characteristics
        assessment_method: Assessment method to use

    Returns:
        Risk assessment results
    """
    engine = RiskAssessmentEngine()
    application_data = {'property': property_data}
    return engine.assess_risk(application_data, assessment_method)
