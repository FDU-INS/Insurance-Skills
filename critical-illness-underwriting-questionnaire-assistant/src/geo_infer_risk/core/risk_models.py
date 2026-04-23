"""
Geospatial risk modeling components for the GEO-INFER-RISK module.

This module provides classes for modeling risk across geographic areas,
including hazard identification, vulnerability assessment, and exposure calculation.
"""

import numpy as np
import geopandas as gpd
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RiskParameters:
    """Parameters for defining risk model behavior."""
    confidence_level: float = 0.95
    time_horizon: int = 50  # years
    spatial_resolution: float = 1.0  # km
    monte_carlo_iterations: int = 1000


class RiskModel:
    """Base class for all geospatial risk models."""
    
    def __init__(self, parameters: Optional[RiskParameters] = None):
        """Initialize a risk model with configurable parameters.
        
        Args:
            parameters: Model configuration parameters
        """
        self.parameters = parameters or RiskParameters()
        self.hazard = None
        self.vulnerability = None
        self.exposure = None
        logger.info("RiskModel initialized with %d-year horizon", self.parameters.time_horizon)
    
    def set_hazard(self, hazard_model: 'HazardModel') -> None:
        """Set the hazard component of the risk model.
        
        Args:
            hazard_model: A hazard model instance
        """
        self.hazard = hazard_model
        logger.info("Hazard model set: %s", type(hazard_model).__name__)
        
    def set_vulnerability(self, vulnerability_model: 'VulnerabilityModel') -> None:
        """Set the vulnerability component of the risk model.
        
        Args:
            vulnerability_model: A vulnerability model instance
        """
        self.vulnerability = vulnerability_model
        logger.info("Vulnerability model set: %s", type(vulnerability_model).__name__)
        
    def set_exposure(self, exposure_model: 'ExposureModel') -> None:
        """Set the exposure component of the risk model.
        
        Args:
            exposure_model: An exposure model instance
        """
        self.exposure = exposure_model
        logger.info("Exposure model set: %s", type(exposure_model).__name__)
    
    def calculate_risk(self, geometry: Union[gpd.GeoDataFrame, gpd.GeoSeries]) -> gpd.GeoDataFrame:
        """Calculate risk for the given geographic area.
        
        Args:
            geometry: Geographic areas to assess risk for
            
        Returns:
            GeoDataFrame with risk metrics for each area
        """
        if not all([self.hazard, self.vulnerability, self.exposure]):
            raise ValueError("Hazard, vulnerability, and exposure models must be set")
        
        logger.info("Calculating risk for %d geometries", len(geometry))
            
        # Calculate risk components
        hazard_data = self.hazard.calculate(geometry)
        vulnerability_data = self.vulnerability.calculate(geometry)
        exposure_data = self.exposure.calculate(geometry)
        
        # Combine components to produce risk
        risk_data = hazard_data.copy()
        risk_data['risk_score'] = hazard_data['hazard_probability'] * \
                                 vulnerability_data['vulnerability_index'] * \
                                 exposure_data['exposure_value']
        
        # Add uncertainty measures
        risk_data['risk_lower_bound'] = risk_data['risk_score'] * 0.8  # Simplified example
        risk_data['risk_upper_bound'] = risk_data['risk_score'] * 1.2  # Simplified example
        
        logger.info("Risk calculated: mean=%.4f", risk_data['risk_score'].mean())
        return risk_data
    
    def run_monte_carlo(self, geometry: gpd.GeoDataFrame) -> Dict:
        """Run Monte Carlo simulations for risk assessment.
        
        Args:
            geometry: Geographic areas to assess risk for
            
        Returns:
            Dictionary with simulation results
        """
        logger.info("Running %d Monte Carlo iterations", self.parameters.monte_carlo_iterations)
        results = []
        for i in range(self.parameters.monte_carlo_iterations):
            # Generate random variations in hazard, vulnerability and exposure
            hazard_variation = self.hazard.sample()
            vulnerability_variation = self.vulnerability.sample()
            exposure_variation = self.exposure.sample()
            
            # Calculate combined risk
            risk = hazard_variation * vulnerability_variation * exposure_variation
            results.append(risk)
            
        # Process results
        results_array = np.array(results)
        result = {
            'mean': np.mean(results_array, axis=0),
            'median': np.median(results_array, axis=0),
            'std_dev': np.std(results_array, axis=0),
            'percentile_95': np.percentile(results_array, 95, axis=0),
            'percentile_5': np.percentile(results_array, 5, axis=0)
        }
        logger.info("Monte Carlo complete: mean risk=%.4f", float(np.mean(result['mean'])))
        return result


class HazardModel(ABC):
    """Base class for modeling hazard probability in geographic areas."""

    def __init__(self, hazard_type: str, return_period: int = 100):
        """Initialize a hazard model.

        Args:
            hazard_type: Type of hazard (flood, earthquake, wildfire, etc.)
            return_period: Return period in years for hazard probability
        """
        self.hazard_type = hazard_type
        self.return_period = return_period
        logger.info("HazardModel initialized: type=%s, return_period=%d", hazard_type, return_period)

    @abstractmethod
    def calculate(self, geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Calculate hazard probability for given areas.

        Args:
            geometry: Geographic areas to assess

        Returns:
            GeoDataFrame with hazard probabilities
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def sample(self) -> np.ndarray:
        """Generate a random sample from the hazard model for Monte Carlo simulation.

        Returns:
            Array of sampled hazard values
        """
        raise NotImplementedError("Subclasses must implement this method")


class VulnerabilityModel(ABC):
    """Base class for modeling vulnerability of assets or populations."""

    def __init__(self, vulnerability_factors: List[str]):
        """Initialize a vulnerability model.

        Args:
            vulnerability_factors: List of factors that contribute to vulnerability
        """
        self.vulnerability_factors = vulnerability_factors
        logger.info("VulnerabilityModel initialized: %d factors", len(vulnerability_factors))

    @abstractmethod
    def calculate(self, geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Calculate vulnerability indices for given areas.

        Args:
            geometry: Geographic areas to assess

        Returns:
            GeoDataFrame with vulnerability indices
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def sample(self) -> np.ndarray:
        """Generate a random sample from the vulnerability model for Monte Carlo simulation.

        Returns:
            Array of sampled vulnerability values
        """
        raise NotImplementedError("Subclasses must implement this method")


class ExposureModel(ABC):
    """Base class for modeling exposure (assets, population, etc.)."""

    def __init__(self, exposure_type: str):
        """Initialize an exposure model.

        Args:
            exposure_type: Type of exposure (buildings, population, infrastructure, etc.)
        """
        self.exposure_type = exposure_type
        logger.info("ExposureModel initialized: type=%s", exposure_type)

    @abstractmethod
    def calculate(self, geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Calculate exposure values for given areas.

        Args:
            geometry: Geographic areas to assess

        Returns:
            GeoDataFrame with exposure values
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def sample(self) -> np.ndarray:
        """Generate a random sample from the exposure model for Monte Carlo simulation.

        Returns:
            Array of sampled exposure values
        """
        raise NotImplementedError("Subclasses must implement this method")


# ==================== Concrete Implementations ====================


class FloodHazardModel(HazardModel):
    """Flood hazard model using depth-frequency analysis.

    Estimates flood probability and depth based on return period,
    elevation, and proximity to water bodies. Uses the Gumbel
    extreme value distribution for flood frequency analysis.
    """

    def __init__(self, return_period: int = 100, base_depth_m: float = 2.0):
        """Initialize flood hazard model.

        Args:
            return_period: Return period in years
            base_depth_m: Reference flood depth in meters for the base return period
        """
        super().__init__("flood", return_period)
        self.base_depth_m = base_depth_m
        self._n_samples = 1  # Updated after first calculate call

    def calculate(self, geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Calculate flood hazard probability per geometry.

        Uses annual exceedance probability P = 1 / return_period and
        assigns a depth estimate based on centroid elevation (lower → deeper).

        Args:
            geometry: GeoDataFrame of areas to assess

        Returns:
            GeoDataFrame with hazard_probability & estimated_depth columns
        """
        result = geometry.copy()
        n = len(result)
        self._n_samples = n

        # Annual exceedance probability
        annual_prob = 1.0 / self.return_period

        # Simple elevation proxy: use centroid Y coordinate normalized
        centroids = result.geometry.centroid
        y_vals = centroids.y.values
        y_range = max(y_vals.max() - y_vals.min(), 1e-6)
        # Lower elevation → higher flood probability
        elevation_factor = 1.0 - (y_vals - y_vals.min()) / y_range

        result['hazard_probability'] = annual_prob * (0.5 + 0.5 * elevation_factor)
        result['estimated_depth_m'] = self.base_depth_m * elevation_factor

        logger.info(
            "FloodHazardModel: %d areas, mean P=%.4f",
            n, result['hazard_probability'].mean(),
        )
        return result

    def sample(self) -> np.ndarray:
        """Sample flood hazard values from Gumbel distribution."""
        mu = 1.0 / self.return_period
        beta = mu * 0.3  # Scale parameter
        return np.random.gumbel(loc=mu, scale=beta, size=self._n_samples).clip(0, 1)


class BuildingVulnerabilityModel(VulnerabilityModel):
    """Building vulnerability model based on structural factors.

    Models vulnerability as a composite index of building age,
    construction material, stories, and maintenance condition.
    """

    # Default fragility curve parameters by material type
    MATERIAL_FACTORS = {
        "reinforced_concrete": 0.2,
        "steel_frame": 0.25,
        "masonry": 0.5,
        "wood": 0.6,
        "adobe": 0.8,
        "informal": 0.9,
    }

    def __init__(self, factors: Optional[List[str]] = None):
        """Initialize building vulnerability model.

        Args:
            factors: Vulnerability factors to consider
        """
        super().__init__(factors or ["age", "material", "stories", "condition"])
        self._n_samples = 1

    def calculate(self, geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Calculate vulnerability index for each area.

        If the GeoDataFrame contains 'building_material', 'building_age',
        'building_stories', or 'building_condition' columns, those are used.
        Otherwise sensible defaults are applied.

        Returns:
            GeoDataFrame with vulnerability_index (0-1) column
        """
        result = geometry.copy()
        n = len(result)
        self._n_samples = n

        # Material factor
        if 'building_material' in result.columns:
            mat_scores = result['building_material'].map(
                self.MATERIAL_FACTORS
            ).fillna(0.5)
        else:
            mat_scores = 0.5

        # Age factor (older → more vulnerable)
        if 'building_age' in result.columns:
            age_scores = (result['building_age'].clip(0, 100) / 100.0)
        else:
            age_scores = 0.4

        # Condition factor (1 = good, 5 = poor)
        if 'building_condition' in result.columns:
            cond_scores = (result['building_condition'].clip(1, 5) - 1) / 4.0
        else:
            cond_scores = 0.3

        result['vulnerability_index'] = (
            0.4 * np.array(mat_scores) +
            0.3 * np.array(age_scores) +
            0.3 * np.array(cond_scores)
        ).clip(0, 1)

        logger.info(
            "BuildingVulnerability: %d areas, mean V=%.4f",
            n, result['vulnerability_index'].mean(),
        )
        return result

    def sample(self) -> np.ndarray:
        """Sample vulnerability values from Beta distribution."""
        return np.random.beta(2, 5, size=self._n_samples)


class PopulationExposureModel(ExposureModel):
    """Population exposure model based on density and demographics.

    Estimates exposure value as a function of population density,
    per-capita income, and critical infrastructure presence.
    """

    def __init__(self, income_per_capita: float = 30000.0):
        """Initialize population exposure model.

        Args:
            income_per_capita: Regional per-capita income (USD)
        """
        super().__init__("population")
        self.income_per_capita = income_per_capita
        self._n_samples = 1

    def calculate(self, geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Calculate exposure values for each area.

        If the GeoDataFrame has 'population' and/or 'area_km2' columns,
        those are used. Otherwise uniform defaults are applied.

        Returns:
            GeoDataFrame with exposure_value column (monetary estimate)
        """
        result = geometry.copy()
        n = len(result)
        self._n_samples = n

        if 'population' in result.columns:
            pop = result['population'].values.astype(float)
        else:
            pop = np.full(n, 1000.0)

        # Exposure = population × per-capita income (simplified)
        result['exposure_value'] = pop * self.income_per_capita

        # Normalize to 0-1 for multiplicative risk model
        max_exp = result['exposure_value'].max()
        if max_exp > 0:
            result['exposure_value'] = result['exposure_value'] / max_exp

        logger.info(
            "PopulationExposure: %d areas, mean E=%.4f",
            n, result['exposure_value'].mean(),
        )
        return result

    def sample(self) -> np.ndarray:
        """Sample exposure values from log-normal distribution."""
        return np.random.lognormal(mean=0, sigma=0.3, size=self._n_samples).clip(0, 1) 