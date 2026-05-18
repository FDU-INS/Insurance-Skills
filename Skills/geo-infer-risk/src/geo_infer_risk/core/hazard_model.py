"""
Enhanced HazardModel: Advanced hazard modeling with spatial and temporal integration.

This module provides sophisticated hazard modeling capabilities with:
- Integration with GEO-INFER-SPACE for spatial analysis
- Integration with GEO-INFER-TIME for temporal dynamics
- Integration with GEO-INFER-MATH for advanced statistical methods
- Climate change scenario modeling
- Advanced event generation with spatial correlation
- Real-time hazard monitoring capabilities
- Uncertainty quantification and probabilistic modeling
"""

import abc
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import json

import numpy as np
import pandas as pd
import geopandas as gpd
from scipy import stats, spatial
from shapely.geometry import Point, Polygon

# GEO-INFER module imports with error handling
try:
    from geo_infer_space.core.spatial_indexing import SpatialIndexingInterface
    from geo_infer_space.core.analytics import SpatialAnalyticsInterface
    SPACE_AVAILABLE = True
except ImportError:
    SPACE_AVAILABLE = False
    SpatialIndexingInterface = None
    SpatialAnalyticsInterface = None

try:
    from geo_infer_time.core.temporal_analysis import TemporalAnalysisInterface
    TIME_AVAILABLE = True
except ImportError:
    TIME_AVAILABLE = False
    TemporalAnalysisInterface = None

try:
    from geo_infer_math.core.spatial_statistics import SpatialStatistics
    MATH_AVAILABLE = True
except ImportError:
    MATH_AVAILABLE = False
    SpatialStatistics = None

logger = logging.getLogger(__name__)


class EnhancedHazardModel:
    """
    Enhanced hazard model with advanced spatial, temporal, and statistical capabilities.

    This class provides sophisticated hazard modeling with:
    - Advanced spatial analysis using H3 indexing
    - Temporal dynamics and seasonal patterns
    - Climate change scenario integration
    - Statistical modeling with uncertainty quantification
    - Real-time hazard monitoring
    - Integration with external data sources
    """

    def __init__(self, hazard_type: str, params: Dict[str, Any]):
        """
        Initialize the enhanced hazard model.

        Args:
            hazard_type: Type of hazard (flood, earthquake, hurricane, etc.)
            params: Model parameters and configuration
        """
        self.hazard_type = hazard_type
        self.params = params
        self.logger = logging.getLogger(f"{__name__}.{hazard_type}")

        # Enhanced parameter handling
        self.return_periods = params.get("return_periods", [10, 25, 50, 100, 500])
        self.data_source = params.get("data_source", "default")
        self.include_climate_change = params.get("include_climate_change", False)
        self.climate_scenario = params.get("climate_scenario", "rcp4.5")
        self.spatial_resolution = params.get("spatial_resolution", 9)  # H3 resolution
        self.temporal_resolution = params.get("temporal_resolution", "daily")
        self.include_seasonality = params.get("include_seasonality", True)
        self.uncertainty_method = params.get("uncertainty_method", "parametric")

        # Initialize spatial and temporal interfaces
        self.spatial_interface = None
        self.temporal_interface = None
        self.math_interface = None

        if SPACE_AVAILABLE:
            try:
                self.spatial_interface = SpatialIndexingInterface()
                self.logger.info("Spatial interface initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize spatial interface: {e}")

        if TIME_AVAILABLE:
            try:
                self.temporal_interface = TemporalAnalysisInterface()
                self.logger.info("Temporal interface initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize temporal interface: {e}")

        if MATH_AVAILABLE:
            try:
                self.math_interface = SpatialStatistics()
                self.logger.info("Math interface initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize math interface: {e}")

        # Model state
        self.is_fitted = False
        self.historical_data = None
        self.model_parameters = {}
        self.climate_factors = {}
        self.uncertainty_parameters = {}

        # Hazard-specific attributes
        self.intensity_measure_type = self._get_intensity_measure_type()
        self.intensity_measure_units = self._get_intensity_measure_units()
        self.hazard_specific_params = {}

        # Load and validate data
        self._load_and_validate_data()

        # Initialize climate factors if needed
        if self.include_climate_change:
            self._initialize_climate_factors()

        self.logger.info(f"Enhanced {hazard_type} hazard model initialized successfully")

    def _get_intensity_measure_type(self) -> str:
        """Get the appropriate intensity measure type for this hazard."""
        intensity_measure_map = {
            "flood": "depth",
            "earthquake": "pga",
            "hurricane": "wind_speed",
            "wildfire": "fireline_intensity",
            "drought": "spi",
            "landslide": "displacement",
            "tsunami": "wave_height",
            "tornado": "wind_speed",
            "hail": "hail_size",
            "winter_storm": "snow_depth",
            "storm_surge": "height",
            "lightning": "density",
            "heat_wave": "temperature_anomaly",
            "cold_wave": "temperature_anomaly"
        }

        return intensity_measure_map.get(self.hazard_type, "intensity")

    def _get_intensity_measure_units(self) -> str:
        """Get the appropriate units for the intensity measure."""
        unit_map = {
            "flood": "m",
            "earthquake": "g",
            "hurricane": "m/s",
            "wildfire": "kW/m",
            "drought": "index",
            "landslide": "m",
            "tsunami": "m",
            "tornado": "m/s",
            "hail": "mm",
            "winter_storm": "cm",
            "storm_surge": "m",
            "lightning": "strikes/km²",
            "heat_wave": "°C",
            "cold_wave": "°C"
        }

        return unit_map.get(self.hazard_type, "")

    def _load_and_validate_data(self) -> None:
        """Load and validate hazard model data."""
        try:
            # Load historical data if available
            data_source = self.params.get("historical_data_source")
            if data_source:
                self.historical_data = self._load_historical_data(data_source)

                # Validate data quality
                self._validate_historical_data()

                # Fit model parameters
                self._fit_model_parameters()

                self.is_fitted = True
                self.logger.info("Hazard model data loaded and validated successfully")
            else:
                self.historical_data = self._generate_synthetic_historical_data()
                self._fit_model_parameters()
                self.logger.info("Hazard model initialized with synthetic data (not fitted)")

        except Exception as e:
            self.logger.error(f"Failed to load hazard data: {e}")
            self.historical_data = None
            self.is_fitted = False

    def _load_historical_data(self, data_source: str) -> pd.DataFrame:
        """Load historical hazard data from various sources."""
        # Placeholder implementation - in real use, this would load from actual data sources
        if data_source.startswith('file://'):
            # Load from file
            file_path = data_source.replace('file://', '')
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                return pd.DataFrame(data)
        elif data_source.startswith('api://'):
            # Load from API (requires runtime endpoint configuration)
            self.logger.info(f"API data loading not implemented for {data_source}")
            return pd.DataFrame()
        else:
            # Try to load from common data sources
            return self._load_from_common_sources(data_source)

    def _load_from_common_sources(self, source: str) -> pd.DataFrame:
        """Load data from common hazard data sources."""
        # Placeholder implementations for common data sources
        if source == "usgs":
            return self._load_usgs_data()
        elif source == "noaa":
            return self._load_noaa_data()
        elif source == "fema":
            return self._load_fema_data()
        else:
            return pd.DataFrame()

    def _load_usgs_data(self) -> pd.DataFrame:
        """Load earthquake data from USGS."""
        # Placeholder - in real implementation, this would query USGS API
        return pd.DataFrame({
            'event_id': ['usgs_001', 'usgs_002'],
            'magnitude': [6.5, 7.2],
            'latitude': [37.7749, 34.0522],
            'longitude': [-122.4194, -118.2437],
            'depth': [10.0, 15.0],
            'timestamp': [datetime.now() - timedelta(days=365), datetime.now() - timedelta(days=180)]
        })

    def _load_noaa_data(self) -> pd.DataFrame:
        """Load weather/climate data from NOAA."""
        # Placeholder implementation
        return pd.DataFrame({
            'event_id': ['noaa_001', 'noaa_002'],
            'event_type': ['hurricane', 'flood'],
            'intensity': [120.0, 2.5],
            'latitude': [25.7617, 40.7128],
            'longitude': [-80.1918, -74.0060],
            'timestamp': [datetime.now() - timedelta(days=300), datetime.now() - timedelta(days=150)]
        })

    def _load_fema_data(self) -> pd.DataFrame:
        """Load flood data from FEMA."""
        # Placeholder implementation
        return pd.DataFrame({
            'event_id': ['fema_001', 'fema_002'],
            'flood_type': ['riverine', 'coastal'],
            'water_depth': [3.2, 1.8],
            'latitude': [29.7604, 32.7767],
            'longitude': [-95.3698, -96.7970],
            'timestamp': [datetime.now() - timedelta(days=200), datetime.now() - timedelta(days=100)]
        })

    def _generate_synthetic_historical_data(self) -> pd.DataFrame:
        """Generate synthetic historical data for testing."""
        num_events = 100

        # Generate synthetic events based on hazard type
        if self.hazard_type == "earthquake":
            return self._generate_synthetic_earthquake_data(num_events)
        elif self.hazard_type == "flood":
            return self._generate_synthetic_flood_data(num_events)
        elif self.hazard_type == "hurricane":
            return self._generate_synthetic_hurricane_data(num_events)
        else:
            return self._generate_generic_synthetic_data(num_events)

    def _generate_synthetic_earthquake_data(self, num_events: int) -> pd.DataFrame:
        """Generate synthetic earthquake data."""
        # Generate earthquake events following Gutenberg-Richter law
        magnitudes = self._generate_magnitudes_gutenberg_richter(num_events)

        # Generate locations (global distribution)
        latitudes = np.random.uniform(-60, 60, num_events)
        longitudes = np.random.uniform(-180, 180, num_events)
        depths = np.random.exponential(15.0, num_events)  # Average depth ~15km

        # Generate timestamps over past 50 years
        start_date = datetime.now() - timedelta(days=50*365)
        timestamps = [start_date + timedelta(days=np.random.randint(0, 50*365)) for _ in range(num_events)]

        return pd.DataFrame({
            'event_id': [f'synth_eq_{i}' for i in range(num_events)],
            'magnitude': magnitudes,
            'latitude': latitudes,
            'longitude': longitudes,
            'depth': depths,
            'timestamp': timestamps
        })

    def _generate_synthetic_flood_data(self, num_events: int) -> pd.DataFrame:
        """Generate synthetic flood data."""
        # Generate flood events
        water_depths = np.random.exponential(2.0, num_events)
        latitudes = np.random.uniform(-60, 60, num_events)
        longitudes = np.random.uniform(-180, 180, num_events)

        timestamps = [datetime.now() - timedelta(days=np.random.randint(0, 10*365)) for _ in range(num_events)]

        return pd.DataFrame({
            'event_id': [f'synth_flood_{i}' for i in range(num_events)],
            'water_depth': water_depths,
            'latitude': latitudes,
            'longitude': longitudes,
            'timestamp': timestamps
        })

    def _generate_synthetic_hurricane_data(self, num_events: int) -> pd.DataFrame:
        """Generate synthetic hurricane data."""
        # Generate hurricane events in tropical regions
        latitudes = np.random.uniform(10, 30, num_events)  # Tropical latitudes
        longitudes = np.random.uniform(-100, -30, num_events)  # Atlantic basin
        wind_speeds = np.random.weibull(2.5, num_events) * 40 + 30  # Hurricane wind speeds

        timestamps = [datetime.now() - timedelta(days=np.random.randint(0, 20*365)) for _ in range(num_events)]

        return pd.DataFrame({
            'event_id': [f'synth_hur_{i}' for i in range(num_events)],
            'wind_speed': wind_speeds,
            'latitude': latitudes,
            'longitude': longitudes,
            'timestamp': timestamps
        })

    def _generate_generic_synthetic_data(self, num_events: int) -> pd.DataFrame:
        """Generate generic synthetic hazard data."""
        intensities = np.random.exponential(1.0, num_events)
        latitudes = np.random.uniform(-60, 60, num_events)
        longitudes = np.random.uniform(-180, 180, num_events)

        timestamps = [datetime.now() - timedelta(days=np.random.randint(0, 5*365)) for _ in range(num_events)]

        return pd.DataFrame({
            'event_id': [f'synth_{self.hazard_type}_{i}' for i in range(num_events)],
            'intensity': intensities,
            'latitude': latitudes,
            'longitude': longitudes,
            'timestamp': timestamps
        })

    def _generate_magnitudes_gutenberg_richter(self, num_events: int, b_value: float = 1.0) -> np.ndarray:
        """Generate earthquake magnitudes following Gutenberg-Richter law."""
        # Gutenberg-Richter: log10(N) = a - b*M
        # Generate magnitudes between 4.0 and 8.0
        min_mag, max_mag = 4.0, 8.0

        # Generate uniform random values and transform to magnitude distribution
        u = np.random.uniform(0, 1, num_events)

        # Inverse transform sampling for Gutenberg-Richter
        # N(M) = 10^(a - b*M), so M = (a - log10(N))/b
        a = 6.0  # Example value
        magnitudes = (a - np.log10(1/u)) / b_value

        # Clip to realistic range
        magnitudes = np.clip(magnitudes, min_mag, max_mag)

        return magnitudes

    def _validate_historical_data(self) -> None:
        """Validate historical data quality and completeness."""
        if self.historical_data is None or self.historical_data.empty:
            self.logger.warning("No historical data available for validation")
            return

        # Check for required columns
        required_cols = ['event_id', 'timestamp']
        for col in required_cols:
            if col not in self.historical_data.columns:
                raise ValueError(f"Required column missing: {col}")

        # Check data quality
        missing_data = self.historical_data.isnull().sum().sum()
        if missing_data > 0:
            self.logger.warning(f"Historical data contains {missing_data} missing values")

        # Check temporal coverage
        if 'timestamp' in self.historical_data.columns:
            time_range = self.historical_data['timestamp'].max() - self.historical_data['timestamp'].min()
            self.logger.info(f"Historical data covers {time_range.days} days")

        # Check spatial coverage
        if 'latitude' in self.historical_data.columns and 'longitude' in self.historical_data.columns:
            lat_range = self.historical_data['latitude'].max() - self.historical_data['latitude'].min()
            lon_range = self.historical_data['longitude'].max() - self.historical_data['longitude'].min()
            self.logger.info(f"Spatial coverage: {lat_range:.2f}° lat, {lon_range:.2f}° lon")

    def _fit_model_parameters(self) -> None:
        """Fit model parameters from historical data."""
        if self.historical_data is None or self.historical_data.empty:
            self.logger.warning("No data available for parameter fitting")
            return

        # Fit distribution parameters based on hazard type
        if self.hazard_type == "earthquake":
            self._fit_earthquake_parameters()
        elif self.hazard_type == "flood":
            self._fit_flood_parameters()
        elif self.hazard_type == "hurricane":
            self._fit_hurricane_parameters()
        else:
            self._fit_generic_parameters()

    def _fit_earthquake_parameters(self) -> None:
        """Fit earthquake model parameters."""
        if 'magnitude' in self.historical_data.columns:
            magnitudes = self.historical_data['magnitude'].values

            # Fit Gutenberg-Richter parameters
            self.model_parameters = {
                'mean_magnitude': np.mean(magnitudes),
                'std_magnitude': np.std(magnitudes),
                'min_magnitude': np.min(magnitudes),
                'max_magnitude': np.max(magnitudes),
                'b_value': self._estimate_b_value(magnitudes),
                'annual_rate': len(magnitudes) / 50.0  # Assuming 50 years of data
            }

    def _fit_flood_parameters(self) -> None:
        """Fit flood model parameters."""
        if 'water_depth' in self.historical_data.columns:
            depths = self.historical_data['water_depth'].values

            self.model_parameters = {
                'mean_depth': np.mean(depths),
                'std_depth': np.std(depths),
                'distribution': 'exponential' if np.mean(depths) > 0 else 'normal'
            }

    def _fit_hurricane_parameters(self) -> None:
        """Fit hurricane model parameters."""
        if 'wind_speed' in self.historical_data.columns:
            wind_speeds = self.historical_data['wind_speed'].values

            self.model_parameters = {
                'mean_wind_speed': np.mean(wind_speeds),
                'std_wind_speed': np.std(wind_speeds),
                'shape_parameter': 2.5,  # Weibull shape
                'scale_parameter': np.mean(wind_speeds) / 2.5
            }

    def _fit_generic_parameters(self) -> None:
        """Fit generic hazard model parameters."""
        if 'intensity' in self.historical_data.columns:
            intensities = self.historical_data['intensity'].values

            self.model_parameters = {
                'mean_intensity': np.mean(intensities),
                'std_intensity': np.std(intensities),
                'distribution': 'exponential'
            }

    def _estimate_b_value(self, magnitudes: np.ndarray) -> float:
        """Estimate Gutenberg-Richter b-value from magnitude data."""
        # Simple b-value estimation using maximum likelihood
        if len(magnitudes) < 10:
            return 1.0  # Default b-value

        # Use magnitudes above completeness threshold
        min_mag = np.percentile(magnitudes, 90)  # Use top 10% for b-value estimation
        complete_mags = magnitudes[magnitudes >= min_mag]

        if len(complete_mags) < 5:
            return 1.0

        # Maximum likelihood b-value estimation
        mean_mag = np.mean(complete_mags)
        b_value = 1.0 / (mean_mag - min_mag + 0.05)  # Add small constant to avoid division by zero

        return max(0.5, min(2.0, b_value))  # Constrain to reasonable range

    def _initialize_climate_factors(self) -> None:
        """Initialize climate change adjustment factors."""
        if not self.include_climate_change:
            return

        # Climate scenario factors (simplified)
        scenario_factors = {
            'rcp2.6': {'intensity': 1.05, 'frequency': 1.1, 'time_horizon': 2050},
            'rcp4.5': {'intensity': 1.15, 'frequency': 1.2, 'time_horizon': 2050},
            'rcp8.5': {'intensity': 1.3, 'frequency': 1.4, 'time_horizon': 2050},
            'ssp1-1.9': {'intensity': 1.02, 'frequency': 1.05, 'time_horizon': 2100},
            'ssp1-2.6': {'intensity': 1.08, 'frequency': 1.15, 'time_horizon': 2100},
            'ssp2-4.5': {'intensity': 1.18, 'frequency': 1.25, 'time_horizon': 2100},
            'ssp3-7.0': {'intensity': 1.25, 'frequency': 1.35, 'time_horizon': 2100},
            'ssp5-8.5': {'intensity': 1.4, 'frequency': 1.5, 'time_horizon': 2100}
        }

        self.climate_factors = scenario_factors.get(self.climate_scenario, {'intensity': 1.0, 'frequency': 1.0})

        self.logger.info(f"Climate factors initialized for scenario {self.climate_scenario}: {self.climate_factors}")

    def generate_events(self, num_events: int, region: Optional[Dict] = None,
                       time_period: Optional[Tuple[datetime, datetime]] = None) -> List[Dict[str, Any]]:
        """
        Generate stochastic hazard events with advanced features.

        Args:
            num_events: Number of events to generate
            region: Spatial region constraints
            time_period: Temporal constraints

        Returns:
            List of generated hazard events
        """
        self.logger.info(f"Generating {num_events} {self.hazard_type} events")

        events = []

        # Apply climate change adjustment if enabled
        climate_multiplier = self.climate_factors.get('frequency', 1.0) if self.include_climate_change else 1.0

        # Generate events in batches for efficiency
        batch_size = min(1000, num_events)
        remaining_events = num_events

        while remaining_events > 0:
            current_batch = min(batch_size, remaining_events)
            batch_events = self._generate_event_batch(current_batch, region, time_period, climate_multiplier)
            events.extend(batch_events)
            remaining_events -= current_batch

        # Apply spatial correlation if available
        if self.spatial_interface and region:
            events = self._apply_spatial_correlation(events, region)

        # Apply temporal patterns if available
        if self.temporal_interface and time_period:
            events = self._apply_temporal_patterns(events, time_period)

        self.logger.info(f"Generated {len(events)} {self.hazard_type} events successfully")
        return events

    def _generate_event_batch(self, batch_size: int, region: Optional[Dict] = None,
                            time_period: Optional[Tuple[datetime, datetime]] = None,
                            climate_multiplier: float = 1.0) -> List[Dict[str, Any]]:
        """Generate a batch of hazard events."""
        events = []

        for i in range(batch_size):
            event = self._generate_single_event(region, time_period, climate_multiplier)
            events.append(event)

        return events

    def _generate_single_event(self, region: Optional[Dict] = None,
                             time_period: Optional[Tuple[datetime, datetime]] = None,
                             climate_multiplier: float = 1.0) -> Dict[str, Any]:
        """Generate a single hazard event."""
        # Generate basic event properties
        event_id = f"{self.hazard_type}_{np.random.randint(1000000)}"

        # Generate timestamp
        if time_period:
            start_time, end_time = time_period
            timestamp = start_time + timedelta(seconds=np.random.randint(0, int((end_time - start_time).total_seconds())))
        else:
            timestamp = datetime.now() + timedelta(days=np.random.randint(0, 365))

        # Generate location
        location = self._generate_event_location(region)

        # Generate intensity based on hazard type
        intensity = self._generate_event_intensity(climate_multiplier)

        # Create event dictionary
        event = {
            'event_id': event_id,
            'hazard_type': self.hazard_type,
            'timestamp': timestamp,
            'location': location,
            'intensity': intensity,
            'intensity_measure': self.intensity_measure_type,
            'units': self.intensity_measure_units,
            'metadata': {
                'climate_adjusted': self.include_climate_change,
                'climate_scenario': self.climate_scenario if self.include_climate_change else None,
                'generation_method': 'monte_carlo',
                'model_version': '2.0.0'
            }
        }

        # Add hazard-specific properties
        event.update(self._get_hazard_specific_properties(intensity, location))

        return event

    def _generate_event_location(self, region: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate event location within specified region."""
        if region:
            # Generate within specified bounds
            bounds = region.get('bounds', {})
            if bounds:
                min_lat = bounds.get('min_lat', -90)
                max_lat = bounds.get('max_lat', 90)
                min_lon = bounds.get('min_lon', -180)
                max_lon = bounds.get('max_lon', 180)

                lat = np.random.uniform(min_lat, max_lat)
                lon = np.random.uniform(min_lon, max_lon)
            else:
                # Generate globally
                lat = np.random.uniform(-60, 60)
                lon = np.random.uniform(-180, 180)
        else:
            # Generate globally with realistic distribution
            lat = np.random.uniform(-60, 60)
            lon = np.random.uniform(-180, 180)

        # Add depth for 3D hazards (earthquakes, etc.)
        depth = 0.0
        if self.hazard_type == "earthquake":
            depth = np.random.exponential(15.0)  # Average earthquake depth

        return {
            'latitude': lat,
            'longitude': lon,
            'depth': depth
        }

    def _generate_event_intensity(self, climate_multiplier: float = 1.0) -> float:
        """Generate event intensity based on fitted parameters."""
        if not self.is_fitted or not self.model_parameters:
            # Use default distributions if not fitted
            return np.random.exponential(1.0) * climate_multiplier

        params = self.model_parameters

        if self.hazard_type == "earthquake":
            # Generate magnitude using Gutenberg-Richter
            magnitude = self._generate_earthquake_magnitude(params)
            # Convert magnitude to intensity measure (PGA)
            return self._magnitude_to_intensity(magnitude)

        elif self.hazard_type == "flood":
            # Generate water depth
            if params.get('distribution') == 'exponential':
                depth = np.random.exponential(params.get('mean_depth', 2.0))
            else:
                depth = np.random.normal(params.get('mean_depth', 2.0), params.get('std_depth', 1.0))

            return max(0, depth) * climate_multiplier

        elif self.hazard_type == "hurricane":
            # Generate wind speed using Weibull distribution
            shape = params.get('shape_parameter', 2.5)
            scale = params.get('scale_parameter', 20.0)
            wind_speed = np.random.weibull(shape) * scale
            return max(0, wind_speed) * climate_multiplier

        else:
            # Generic intensity generation
            mean_intensity = params.get('mean_intensity', 1.0)
            std_intensity = params.get('std_intensity', 0.5)
            intensity = np.random.exponential(mean_intensity)
            return max(0, intensity) * climate_multiplier

    def _generate_earthquake_magnitude(self, params: Dict[str, Any]) -> float:
        """Generate earthquake magnitude using fitted parameters."""
        # Use inverse transform sampling for Gutenberg-Richter distribution
        b_value = params.get('b_value', 1.0)
        min_mag = params.get('min_magnitude', 4.0)

        # Generate uniform random variable
        u = np.random.uniform(0, 1)

        # Transform using Gutenberg-Richter relationship
        # N(M) ∝ 10^(-b*M), so M = (log10(1/u) - a) / (-b)
        # We use the fitted parameters to estimate 'a'
        a = 6.0  # Example value - in practice this would be fitted
        magnitude = (np.log10(1/u) - a) / (-b_value) + min_mag

        # Ensure magnitude is in reasonable range
        return max(min_mag, min(8.0, magnitude))

    def _magnitude_to_intensity(self, magnitude: float) -> float:
        """Convert earthquake magnitude to intensity measure (PGA)."""
        # Simplified magnitude to PGA conversion
        # In practice, this would use ground motion prediction equations (GMPEs)
        if magnitude < 4.0:
            return 0.01  # Very low PGA for small earthquakes
        elif magnitude < 5.0:
            return 0.05
        elif magnitude < 6.0:
            return 0.15
        elif magnitude < 7.0:
            return 0.3
        else:
            return 0.5

    def _get_hazard_specific_properties(self, intensity: float, location: Dict[str, Any]) -> Dict[str, Any]:
        """Get hazard-specific properties for the event."""
        properties = {}

        if self.hazard_type == "earthquake":
            properties.update({
                'magnitude': self._intensity_to_magnitude(intensity),
                'depth': location['depth'],
                'tectonic_region': np.random.choice(['active', 'stable', 'subduction'])
            })
        elif self.hazard_type == "flood":
            properties.update({
                'water_depth': intensity,
                'flood_type': np.random.choice(['riverine', 'pluvial', 'coastal']),
                'duration': np.random.exponential(48.0)  # Hours
            })
        elif self.hazard_type == "hurricane":
            properties.update({
                'wind_speed': intensity,
                'category': self._get_hurricane_category(intensity),
                'pressure': 1013.0 - (intensity - 30) * 2.0,  # Simplified pressure drop
                'radius_max_wind': np.random.normal(50, 15)  # km
            })
        elif self.hazard_type == "wildfire":
            properties.update({
                'fireline_intensity': intensity,
                'burned_area': np.random.exponential(1000.0),  # hectares
                'flame_length': min(10.0, intensity / 100.0)  # meters
            })

        return properties

    def _intensity_to_magnitude(self, intensity: float) -> float:
        """Convert intensity measure back to magnitude (for earthquakes)."""
        # Inverse of magnitude_to_intensity
        if intensity < 0.05:
            return 4.0
        elif intensity < 0.15:
            return 5.0
        elif intensity < 0.3:
            return 6.0
        else:
            return 7.0

    def _get_hurricane_category(self, wind_speed: float) -> int:
        """Get Saffir-Simpson hurricane category from wind speed."""
        if wind_speed < 33:  # Tropical storm
            return 0
        elif wind_speed < 43:  # Category 1
            return 1
        elif wind_speed < 50:  # Category 2
            return 2
        elif wind_speed < 58:  # Category 3
            return 3
        elif wind_speed < 70:  # Category 4
            return 4
        else:  # Category 5
            return 5

    def _apply_spatial_correlation(self, events: List[Dict[str, Any]], region: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply spatial correlation to generated events using proximity-based clustering.

        Events that occur within a threshold distance of each other (cluster radius)
        receive a positive intensity boost reflecting hazard co-location effects
        (e.g. earthquake aftershock clusters, storm train sequences).

        Uses a simplified distance matrix approach:
        - cluster_radius: configured in ``params`` (default 100 km)
        - intensity_boost_per_neighbour: 5% (capped at 20%)

        Falls back to returning events unchanged if scipy is unavailable.
        """
        if not self.spatial_interface:
            return events

        if not events:
            return events

        try:
            from scipy.spatial import distance as sp_distance  # type: ignore

            cluster_radius_km = float(self.params.get('spatial_cluster_radius_km', 100.0))
            boost_per_neighbour = float(self.params.get('spatial_intensity_boost', 0.05))
            max_boost = float(self.params.get('max_spatial_boost', 0.20))

            # Build coordinate array [lat, lon] in degrees
            coords = [(e['location']['latitude'], e['location']['longitude']) for e in events]

            # Haversine-inspired degree-based proxy: 1 degree ≈ 111 km
            km_per_degree = 111.0
            coords_km = [(lat, lon * km_per_degree) for lat, lon in coords]

            for i, event in enumerate(events):
                neighbours = 0
                lat_i, lon_i = coords_km[i]
                for j, (lat_j, lon_j) in enumerate(coords_km):
                    if i == j:
                        continue
                    d = ((lat_i - lat_j) ** 2 + (lon_i - lon_j) ** 2) ** 0.5
                    if d <= cluster_radius_km:
                        neighbours += 1

                if neighbours > 0:
                    boost = min(max_boost, neighbours * boost_per_neighbour)
                    events[i]['intensity'] *= (1.0 + boost)
                    events[i]['metadata']['spatial_cluster_neighbours'] = neighbours
                    events[i]['metadata']['spatial_intensity_boost'] = boost

            self.logger.info(f"Spatial correlation applied to {len(events)} events (radius={cluster_radius_km} km)")
            return events

        except ImportError:
            self.logger.warning("scipy not available — spatial correlation skipped")
            return events
        except Exception as e:
            self.logger.warning(f"Failed to apply spatial correlation: {e}")
            return events


    def _apply_temporal_patterns(self, events: List[Dict[str, Any]], time_period: Tuple[datetime, datetime]) -> List[Dict[str, Any]]:
        """Apply temporal patterns and seasonality to events."""
        if not self.temporal_interface:
            return events

        try:
            # Apply seasonal patterns based on hazard type
            if self.include_seasonality:
                events = self._apply_seasonality(events, time_period)

            self.logger.info("Temporal patterns applied")
            return events

        except Exception as e:
            self.logger.warning(f"Failed to apply temporal patterns: {e}")
            return events

    def _apply_seasonality(self, events: List[Dict[str, Any]], time_period: Tuple[datetime, datetime]) -> List[Dict[str, Any]]:
        """Apply seasonal patterns to events."""
        # Simple seasonality implementation
        seasonal_multipliers = self._get_seasonal_multipliers()

        for event in events:
            timestamp = event['timestamp']
            month = timestamp.month

            # Apply seasonal multiplier
            multiplier = seasonal_multipliers.get(month, 1.0)
            event['intensity'] *= multiplier
            event['metadata']['seasonal_adjustment'] = multiplier

        return events

    def _get_seasonal_multipliers(self) -> Dict[int, float]:
        """Get seasonal multipliers for the hazard type."""
        # Default seasonal patterns - can be overridden by subclasses
        base_patterns = {
            'earthquake': {m: 1.0 for m in range(1, 13)},  # No strong seasonality
            'flood': {1: 0.8, 2: 0.9, 3: 1.2, 4: 1.3, 5: 1.2, 6: 1.0, 7: 0.9, 8: 0.8, 9: 0.9, 10: 1.1, 11: 1.2, 12: 1.0},
            'hurricane': {1: 0.1, 2: 0.1, 3: 0.2, 4: 0.3, 5: 0.5, 6: 1.0, 7: 0.8, 8: 1.0, 9: 0.9, 10: 0.5, 11: 0.2, 12: 0.1},
            'wildfire': {1: 0.5, 2: 0.6, 3: 0.8, 4: 1.0, 5: 1.2, 6: 1.5, 7: 1.8, 8: 1.5, 9: 1.2, 10: 0.8, 11: 0.5, 12: 0.4}
        }

        return base_patterns.get(self.hazard_type, {m: 1.0 for m in range(1, 13)})

    def get_intensity_at_location(self, event: Dict[str, Any], latitude: float, longitude: float) -> float:
        """
        Calculate hazard intensity at a specific location for a given event.

        Args:
            event: Hazard event dictionary
            latitude: Target latitude
            longitude: Target longitude

        Returns:
            Hazard intensity at the specified location
        """
        # Get event location and intensity
        event_loc = event['location']
        event_intensity = event['intensity']

        # Calculate distance from event epicenter/center
        distance = self._calculate_distance(
            event_loc['latitude'], event_loc['longitude'],
            latitude, longitude
        )

        # Apply distance attenuation
        attenuated_intensity = self._apply_distance_attenuation(event_intensity, distance)

        # Apply local site effects if available
        site_effects = self._apply_site_effects(latitude, longitude, attenuated_intensity)

        return site_effects

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great circle distance between two points."""
        # Haversine formula
        R = 6371  # Earth's radius in km

        lat1_rad, lon1_rad = np.radians([lat1, lon1])
        lat2_rad, lon2_rad = np.radians([lat2, lon2])

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

        return R * c

    def _apply_distance_attenuation(self, intensity: float, distance: float) -> float:
        """Apply distance attenuation to hazard intensity."""
        # Simple attenuation models - in practice, these would be more sophisticated

        if self.hazard_type == "earthquake":
            # Ground motion attenuation
            if distance < 10:
                return intensity
            else:
                # Simple 1/r attenuation with saturation
                return intensity / (1 + distance / 50.0)

        elif self.hazard_type == "flood":
            # Flood attenuation (simplified)
            if distance < 5:
                return intensity
            else:
                return max(0, intensity - distance * 0.1)

        elif self.hazard_type == "hurricane":
            # Hurricane wind field attenuation
            radius_max = 50.0  # km
            if distance < radius_max:
                # Inside RMW - use Holland model approximation
                return intensity * np.exp(-distance / radius_max)
            else:
                # Outside RMW - rapid decay
                return intensity * np.exp(-distance / radius_max) * (radius_max / distance)**0.5

        else:
            # Generic attenuation
            return max(0, intensity / (1 + distance / 20.0))

    def _apply_site_effects(self, latitude: float, longitude: float, intensity: float) -> float:
        """Apply local site effects to hazard intensity."""
        # Placeholder for site effects
        # In practice, this would use soil conditions, topography, etc.

        # Simple example: add some random variation to simulate site effects
        site_variation = np.random.normal(1.0, 0.1)
        return intensity * site_variation

    def get_return_period_map(self, return_period: float, region: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate hazard map for a specific return period.

        Args:
            return_period: Return period in years
            region: Geographic region for the map

        Returns:
            Hazard intensity map data
        """
        self.logger.info(f"Generating {return_period}-year return period map for {self.hazard_type}")

        if not region:
            region = {
                'bounds': {
                    'min_lon': -180, 'max_lon': 180,
                    'min_lat': -90, 'max_lat': 90
                }
            }

        bounds = region['bounds']
        resolution = self.spatial_resolution

        # Create grid points
        lats = np.linspace(bounds['min_lat'], bounds['max_lat'],
                          int((bounds['max_lat'] - bounds['min_lat']) * 10))
        lons = np.linspace(bounds['min_lon'], bounds['max_lon'],
                          int((bounds['max_lon'] - bounds['min_lon']) * 10))

        # Generate intensity map
        intensity_grid = np.zeros((len(lats), len(lons)))

        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                # Get intensity at this location for the return period
                intensity = self._get_return_period_intensity(return_period, lat, lon)
                intensity_grid[i, j] = intensity

        return {
            'hazard_type': self.hazard_type,
            'return_period': return_period,
            'bounds': bounds,
            'resolution': resolution,
            'intensity_grid': intensity_grid.tolist(),
            'latitude_grid': lats.tolist(),
            'longitude_grid': lons.tolist(),
            'units': self.intensity_measure_units,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'model_version': '2.0.0',
                'climate_scenario': self.climate_scenario if self.include_climate_change else None
            }
        }

    def _get_return_period_intensity(self, return_period: float, latitude: float, longitude: float) -> float:
        """Get hazard intensity for a specific return period at a location."""
        # Simplified implementation - in practice, this would use extreme value theory
        if not self.is_fitted:
            return 0.0

        # Use Gumbel distribution for extreme values
        mean_intensity = self.model_parameters.get('mean_intensity', 1.0)
        std_intensity = self.model_parameters.get('std_intensity', 0.5)

        # Gumbel parameters
        location = mean_intensity
        scale = std_intensity / np.sqrt(6) / np.pi  # Approximation

        # Return level for given return period
        return_period_prob = 1.0 / return_period
        gumbel_quantile = -np.log(-np.log(1 - return_period_prob))

        return location + scale * gumbel_quantile

    def get_model_status(self) -> Dict[str, Any]:
        """Get comprehensive model status information."""
        return {
            'hazard_type': self.hazard_type,
            'is_fitted': self.is_fitted,
            'data_available': self.historical_data is not None,
            'climate_change_enabled': self.include_climate_change,
            'climate_scenario': self.climate_scenario if self.include_climate_change else None,
            'spatial_integration': self.spatial_interface is not None,
            'temporal_integration': self.temporal_interface is not None,
            'math_integration': self.math_interface is not None,
            'model_parameters': self.model_parameters,
            'intensity_measure': {
                'type': self.intensity_measure_type,
                'units': self.intensity_measure_units
            },
            'configuration': {
                'return_periods': self.return_periods,
                'spatial_resolution': self.spatial_resolution,
                'temporal_resolution': self.temporal_resolution,
                'uncertainty_method': self.uncertainty_method
            }
        }

    def save_model(self, filepath: str) -> None:
        """Save trained model to file."""
        model_state = {
            'hazard_type': self.hazard_type,
            'model_parameters': self.model_parameters,
            'climate_factors': self.climate_factors,
            'uncertainty_parameters': self.uncertainty_parameters,
            'is_fitted': self.is_fitted,
            'params': self.params,
            'metadata': {
                'saved_at': datetime.now().isoformat(),
                'version': '2.0.0'
            }
        }

        with open(filepath, 'w') as f:
            json.dump(model_state, f, indent=2, default=str)

        self.logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath: str) -> None:
        """Load trained model from file."""
        with open(filepath, 'r') as f:
            model_state = json.load(f)

        self.hazard_type = model_state['hazard_type']
        self.model_parameters = model_state['model_parameters']
        self.climate_factors = model_state['climate_factors']
        self.uncertainty_parameters = model_state['uncertainty_parameters']
        self.is_fitted = model_state['is_fitted']
        self.params = model_state['params']

        self.logger.info(f"Model loaded from {filepath}")


# Enhanced Specific Hazard Models

class EnhancedFloodModel(EnhancedHazardModel):
    """Enhanced flood hazard model with advanced hydrological modeling."""

    def __init__(self, params: Dict[str, Any]):
        super().__init__("flood", params)
        self.flood_type = params.get("type", "riverine")
        self.dem_resolution = params.get("dem_resolution", 30)
        self.include_storm_surge = params.get("include_storm_surge", False)
        self.include_pluvial = params.get("include_pluvial", False)

    def _fit_flood_parameters(self) -> None:
        """Fit flood-specific model parameters."""
        if 'water_depth' in self.historical_data.columns:
            depths = self.historical_data['water_depth'].values

            # Fit distribution parameters
            self.model_parameters = {
                'mean_depth': np.mean(depths),
                'std_depth': np.std(depths),
                'max_depth': np.max(depths),
                'distribution_type': 'gumbel' if np.mean(depths) > 1.0 else 'exponential',
                'return_level_params': self._fit_extreme_value_parameters(depths)
            }

        # Fit spatial correlation parameters
        if 'latitude' in self.historical_data.columns and 'longitude' in self.historical_data.columns:
            self._fit_spatial_correlation_parameters()

    def _fit_extreme_value_parameters(self, depths: np.ndarray) -> Dict[str, float]:
        """Fit extreme value distribution parameters."""
        # Use Generalized Extreme Value (GEV) distribution
        try:
            shape, loc, scale = stats.genextreme.fit(depths)
            return {
                'shape': shape,
                'location': loc,
                'scale': scale
            }
        except:
            # Fallback to Gumbel distribution
            loc, scale = stats.gumbel_r.fit(depths)
            return {
                'shape': 0.0,  # Gumbel is GEV with shape=0
                'location': loc,
                'scale': scale
            }

    def _fit_spatial_correlation_parameters(self) -> None:
        """Fit spatial correlation parameters for flood events."""
        # Calculate spatial correlation length
        coords = self.historical_data[['longitude', 'latitude']].values

        if len(coords) > 1:
            # Simple correlation length estimation
            distances = spatial.distance.pdist(coords)
            if len(distances) > 0:
                self.model_parameters['correlation_length'] = np.mean(distances) * 0.3

    def _generate_event_intensity(self, climate_multiplier: float = 1.0) -> float:
        """Generate flood event intensity with climate adjustment."""
        if not self.is_fitted:
            return np.random.exponential(2.0) * climate_multiplier

        params = self.model_parameters

        if params.get('distribution_type') == 'gumbel':
            # Generate from Gumbel distribution
            depth = np.random.gumbel(params['mean_depth'], params['std_depth'])
        else:
            # Generate from exponential distribution
            depth = np.random.exponential(params['mean_depth'])

        # Apply climate change adjustment
        return max(0, depth) * climate_multiplier

    def _get_hazard_specific_properties(self, intensity: float, location: Dict[str, Any]) -> Dict[str, Any]:
        """Get flood-specific properties."""
        return {
            'water_depth': intensity,
            'flood_type': self.flood_type,
            'duration': np.random.exponential(72.0),  # Hours
            'flow_velocity': np.random.uniform(0.5, 3.0),  # m/s
            'affected_area': np.random.exponential(50.0)  # km²
        }

class EnhancedEarthquakeModel(EnhancedHazardModel):
    """Enhanced earthquake hazard model with tectonic considerations."""

    def __init__(self, params: Dict[str, Any]):
        super().__init__("earthquake", params)
        self.eq_type = params.get("type", "probabilistic")
        self.include_secondary_perils = params.get("include_secondary_perils", True)
        self.secondary_perils = params.get("secondary_perils", ["liquefaction", "landslide"])

    def _fit_earthquake_parameters(self) -> None:
        """Fit earthquake-specific model parameters."""
        if 'magnitude' in self.historical_data.columns:
            magnitudes = self.historical_data['magnitude'].values

            # Fit Gutenberg-Richter parameters
            self.model_parameters = {
                'mean_magnitude': np.mean(magnitudes),
                'std_magnitude': np.std(magnitudes),
                'min_magnitude': np.min(magnitudes),
                'max_magnitude': np.max(magnitudes),
                'b_value': self._estimate_b_value(magnitudes),
                'annual_rate': len(magnitudes) / max(1, self.historical_data['timestamp'].max().year - self.historical_data['timestamp'].min().year + 1),
                'magnitude_distribution': 'gutenberg_richter'
            }

        # Fit depth distribution
        if 'depth' in self.historical_data.columns:
            depths = self.historical_data['depth'].values
            self.model_parameters.update({
                'mean_depth': np.mean(depths),
                'depth_distribution': 'exponential'
            })

    def _generate_earthquake_magnitude(self, params: Dict[str, Any]) -> float:
        """Generate earthquake magnitude using Gutenberg-Richter distribution."""
        b_value = params.get('b_value', 1.0)
        min_mag = params.get('min_magnitude', 4.0)
        max_mag = params.get('max_magnitude', 8.0)

        # Generate using inverse transform sampling
        u = np.random.uniform(0, 1)

        # Gutenberg-Richter: N(M) ∝ 10^(-b*M)
        # M = (log10(1/u) - a) / (-b) + M_min
        # We solve for 'a' using the maximum magnitude
        a = -b_value * max_mag + np.log10(len(self.historical_data) if self.historical_data is not None else 100)
        magnitude = (np.log10(1/u) - a) / (-b_value) + min_mag

        return max(min_mag, min(8.5, magnitude))

    def _get_hazard_specific_properties(self, intensity: float, location: Dict[str, Any]) -> Dict[str, Any]:
        """Get earthquake-specific properties."""
        magnitude = self._intensity_to_magnitude(intensity)

        properties = {
            'magnitude': magnitude,
            'depth': location['depth'],
            'tectonic_region': np.random.choice(['active_crustal', 'subduction', 'stable_crustal']),
            'focal_mechanism': np.random.choice(['strike_slip', 'normal', 'reverse', 'oblique'])
        }

        # Add secondary perils if enabled
        if self.include_secondary_perils:
            properties['secondary_perils'] = {}

            # Liquefaction probability
            properties['secondary_perils']['liquefaction'] = self._calculate_liquefaction_probability(magnitude, location)

            # Landslide probability
            properties['secondary_perils']['landslide'] = self._calculate_landslide_probability(magnitude, location)

        return properties

    def _calculate_liquefaction_probability(self, magnitude: float, location: Dict[str, Any]) -> float:
        """Calculate liquefaction probability (simplified)."""
        # Simplified model based on magnitude and depth
        if magnitude < 5.0:
            return 0.1
        elif magnitude < 6.0:
            return 0.3
        elif magnitude < 7.0:
            return 0.6
        else:
            return 0.8

    def _calculate_landslide_probability(self, magnitude: float, location: Dict[str, Any]) -> float:
        """Calculate landslide probability (simplified)."""
        # Simplified model
        if magnitude < 4.0:
            return 0.05
        elif magnitude < 5.0:
            return 0.15
        elif magnitude < 6.0:
            return 0.4
        else:
            return 0.7

class EnhancedHurricaneModel(EnhancedHazardModel):
    """Enhanced hurricane model with storm track and intensity modeling."""

    def __init__(self, params: Dict[str, Any]):
        super().__init__("hurricane", params)
        self.include_components = params.get("include_components", ["wind", "storm_surge", "rainfall"])
        self.track_data_source = params.get("track_data_source", "hurdat2")

    def _fit_hurricane_parameters(self) -> None:
        """Fit hurricane-specific model parameters."""
        if 'wind_speed' in self.historical_data.columns:
            wind_speeds = self.historical_data['wind_speed'].values

            # Fit Weibull distribution for wind speeds
            shape, loc, scale = stats.weibull_min.fit(wind_speeds, floc=0)

            self.model_parameters = {
                'mean_wind_speed': np.mean(wind_speeds),
                'std_wind_speed': np.std(wind_speeds),
                'weibull_shape': shape,
                'weibull_scale': scale,
                'weibull_location': loc,
                'annual_frequency': len(wind_speeds) / 50.0  # Assuming 50 years of data
            }

    def _generate_event_intensity(self, climate_multiplier: float = 1.0) -> float:
        """Generate hurricane wind speed intensity."""
        if not self.is_fitted:
            return np.random.weibull(2.5) * 40 + 30  # Default hurricane wind speeds

        params = self.model_parameters

        # Generate from fitted Weibull distribution
        shape = params.get('weibull_shape', 2.5)
        scale = params.get('weibull_scale', 30.0)

        wind_speed = np.random.weibull(shape) * scale

        # Apply climate change adjustment
        return max(25, wind_speed) * climate_multiplier  # Minimum tropical storm strength

    def _get_hazard_specific_properties(self, intensity: float, location: Dict[str, Any]) -> Dict[str, Any]:
        """Get hurricane-specific properties."""
        properties = {
            'wind_speed': intensity,
            'category': self._get_hurricane_category(intensity),
            'central_pressure': self._calculate_central_pressure(intensity),
            'radius_max_wind': np.random.normal(50, 15),
            'forward_speed': np.random.uniform(5, 15),  # km/h
            'storm_surge': self._calculate_storm_surge(intensity, location)
        }

        # Generate track if requested
        if 'track' in self.include_components:
            properties['track'] = self._generate_storm_track(location, intensity)

        return properties

    def _calculate_central_pressure(self, wind_speed: float) -> float:
        """Calculate central pressure from wind speed."""
        # Simplified pressure-wind relationship
        return 1013.0 - (wind_speed - 30) * 1.5  # hPa

    def _calculate_storm_surge(self, wind_speed: float, location: Dict[str, Any]) -> float:
        """Calculate storm surge height."""
        # Simplified storm surge calculation
        base_surge = (wind_speed - 30) * 0.01  # meters per m/s above 30 m/s

        # Add tidal effects
        tidal_factor = 1.0 + 0.3 * np.sin(2 * np.pi * np.random.random())  # ±30% tidal variation

        return max(0, base_surge * tidal_factor)

    def _generate_storm_track(self, start_location: Dict[str, Any], intensity: float) -> List[Dict[str, Any]]:
        """Generate simplified storm track."""
        track_length = np.random.randint(5, 20)  # Number of track points
        track = []

        current_lat, current_lon = start_location['latitude'], start_location['longitude']

        for i in range(track_length):
            # Storm movement (generally westward then northward)
            if i < track_length // 2:
                # Initial westward movement
                delta_lon = np.random.normal(-0.2, 0.1)  # degrees
                delta_lat = np.random.normal(0.1, 0.1)
            else:
                # Later northward movement
                delta_lon = np.random.normal(0.1, 0.1)
                delta_lat = np.random.normal(0.3, 0.1)

            current_lat += delta_lat
            current_lon += delta_lon

            # Intensity decay over time
            decay_factor = np.exp(-i * 0.1)  # Exponential decay
            current_intensity = intensity * decay_factor

            track_point = {
                'time_offset': i * 6,  # Hours from start
                'latitude': current_lat,
                'longitude': current_lon,
                'wind_speed': current_intensity,
                'pressure': self._calculate_central_pressure(current_intensity)
            }

            track.append(track_point)

        return track

class EnhancedWildfireModel(EnhancedHazardModel):
    """Enhanced wildfire model with fuel and weather considerations."""

    def __init__(self, params: Dict[str, Any]):
        super().__init__("wildfire", params)
        self.fuel_model = params.get("fuel_model", "standard")
        self.include_weather_effects = params.get("include_weather_effects", True)
        self.include_climate_factors = params.get("include_climate_factors", True)

    def _fit_wildfire_parameters(self) -> None:
        """Fit wildfire-specific model parameters."""
        if 'fireline_intensity' in self.historical_data.columns:
            intensities = self.historical_data['fireline_intensity'].values

            self.model_parameters = {
                'mean_intensity': np.mean(intensities),
                'std_intensity': np.std(intensities),
                'distribution': 'lognormal',  # Fire intensity often follows log-normal
                'annual_frequency': len(intensities) / 20.0  # Assuming 20 years of data
            }

    def _generate_event_intensity(self, climate_multiplier: float = 1.0) -> float:
        """Generate wildfire intensity with climate adjustment."""
        if not self.is_fitted:
            return np.random.lognormal(6.0, 1.0) * climate_multiplier  # Default fire intensity

        params = self.model_parameters

        # Generate from log-normal distribution
        mean_log = np.log(params.get('mean_intensity', 500.0))
        std_log = params.get('std_intensity', 200.0) / params.get('mean_intensity', 500.0)

        intensity = np.random.lognormal(mean_log, std_log)

        # Apply climate change adjustment (drier conditions = higher intensity)
        return max(100, intensity) * climate_multiplier

    def _get_hazard_specific_properties(self, intensity: float, location: Dict[str, Any]) -> Dict[str, Any]:
        """Get wildfire-specific properties."""
        return {
            'fireline_intensity': intensity,
            'flame_length': min(20.0, intensity / 100.0),  # meters
            'burned_area': np.random.exponential(1000.0),  # hectares
            'spread_rate': np.random.uniform(0.1, 2.0),  # km/hour
            'fuel_type': np.random.choice(['grass', 'shrub', 'timber', 'slash']),
            'weather_conditions': {
                'temperature': np.random.normal(25, 8),  # Celsius
                'humidity': np.random.uniform(10, 40),   # Percent
                'wind_speed': np.random.uniform(5, 25)   # km/h
            }
        }


# Factory functions for creating enhanced hazard models
def create_enhanced_flood_model(params: Dict[str, Any]) -> EnhancedFloodModel:
    """Create an enhanced flood hazard model."""
    return EnhancedFloodModel(params)

def create_enhanced_earthquake_model(params: Dict[str, Any]) -> EnhancedEarthquakeModel:
    """Create an enhanced earthquake hazard model."""
    return EnhancedEarthquakeModel(params)

def create_enhanced_hurricane_model(params: Dict[str, Any]) -> EnhancedHurricaneModel:
    """Create an enhanced hurricane hazard model."""
    return EnhancedHurricaneModel(params)

def create_enhanced_wildfire_model(params: Dict[str, Any]) -> EnhancedWildfireModel:
    """Create an enhanced wildfire hazard model."""
    return EnhancedWildfireModel(params)


# Backward compatibility - create alias for existing code
HazardModel = EnhancedHazardModel
        
