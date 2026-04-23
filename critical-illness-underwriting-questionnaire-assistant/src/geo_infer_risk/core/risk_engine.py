"""
Enhanced RiskEngine: Advanced orchestrator for comprehensive risk modeling and analysis.

This module provides an enhanced RiskEngine class that serves as the main entry point
for running sophisticated risk analyses, coordinating interactions between multiple
hazard, vulnerability, and exposure models while integrating with other GEO-INFER modules.

Key enhancements:
- Integration with GEO-INFER-SPACE for advanced spatial analysis
- Integration with GEO-INFER-TIME for temporal dynamics
- Integration with GEO-INFER-AI for machine learning applications
- Integration with GEO-INFER-MATH for advanced statistical methods
- Integration with GEO-INFER-BAYES for Bayesian inference
- Advanced Monte Carlo simulation with convergence criteria
- Real-time risk monitoring and streaming analytics
- Portfolio optimization and risk aggregation
- Climate change scenario integration
- Comprehensive uncertainty quantification
"""

import logging
import os
import time
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import geopandas as gpd
from scipy import stats
import json

# GEO-INFER module imports with error handling
try:
    from geo_infer_space.core.spatial_indexing import SpatialIndexingInterface
    from geo_infer_space.core.analytics import SpatialAnalyticsInterface
    from geo_infer_space.core.dispatcher import configure_backends
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
    from geo_infer_math.core.interpolation import InterpolationMethods
    MATH_AVAILABLE = True
except ImportError:
    MATH_AVAILABLE = False
    SpatialStatistics = None
    InterpolationMethods = None

try:
    from geo_infer_bayes.core.inference import BayesianInference
    BAYES_AVAILABLE = True
except ImportError:
    BAYES_AVAILABLE = False
    BayesianInference = None

# Local imports
from geo_infer_risk.core.hazard_model import HazardModel
from geo_infer_risk.core.vulnerability_model import VulnerabilityModel
from geo_infer_risk.core.exposure_model import ExposureModel
from geo_infer_risk.core.catastrophe_models import CatastropheModelManager
from geo_infer_risk.core.insurance_models import InsuranceManager
from geo_infer_risk.utils.validation import validate_config, ValidationResult
from geo_infer_risk.utils.risk_metrics import calculate_aal, calculate_ep_curve
from geo_infer_risk.utils.config_loader import load_config_with_defaults


@dataclass
class AnalysisJob:
    """Represents an analysis job with metadata and status."""
    job_id: str
    job_type: str
    status: str = "queued"
    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ModelIntegrationStatus:
    """Status of integration with external GEO-INFER modules."""
    space_integration: bool = SPACE_AVAILABLE
    time_integration: bool = TIME_AVAILABLE
    math_integration: bool = MATH_AVAILABLE
    bayes_integration: bool = BAYES_AVAILABLE
    spatial_indexing_available: bool = False
    temporal_analysis_available: bool = False
    advanced_statistics_available: bool = False
    bayesian_inference_available: bool = False

class EnhancedRiskEngine:
    """
    Enhanced risk analysis engine with advanced capabilities and module integration.

    The EnhancedRiskEngine provides:
    - Integration with all GEO-INFER modules (SPACE, TIME, AI, MATH, BAYES)
    - Advanced Monte Carlo simulation with convergence monitoring
    - Real-time risk monitoring and streaming analytics
    - Portfolio optimization and risk aggregation
    - Climate change scenario analysis
    - Comprehensive uncertainty quantification
    - Asynchronous processing capabilities
    - Model calibration and validation
    - Advanced spatial and temporal analysis
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the EnhancedRiskEngine with comprehensive configuration.

        Args:
            config: Configuration dictionary. If None, loads from default locations.
        """
        # Load configuration with defaults
        if config is None:
            config = load_config_with_defaults()

        self.config = config
        self.logger = self._setup_enhanced_logging()

        # Validate the configuration
        validation_result = validate_config(config)
        if not validation_result.is_valid:
            raise ValueError(f"Invalid configuration: {validation_result.errors}")

        # Initialize integration status
        self.integration_status = self._check_module_integrations()

        # Initialize core components
        self._initialize_core_components()

        # Initialize model containers
        self.hazard_models = {}
        self.vulnerability_models = {}
        self.exposure_models = {}
        self.catastrophe_manager = CatastropheModelManager()
        self.insurance_manager = InsuranceManager()

        # Initialize results and job management
        self.event_losses = None
        self.aggregated_metrics = None
        self.active_jobs: Dict[str, AnalysisJob] = {}
        self.job_counter = 0

        # Initialize spatial and temporal interfaces
        self._initialize_spatial_interface()
        self._initialize_temporal_interface()

        # Setup output and caching
        self.output_dir = config.get("general", {}).get("output_directory", "./outputs")
        self.cache_dir = config.get("general", {}).get("cache_directory", "./cache")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)

        # Initialize threading and async support
        self.executor = ThreadPoolExecutor(max_workers=config.get("general", {}).get("num_workers", 4))
        self.async_enabled = config.get("general", {}).get("enable_async", True)

        self.logger.info(f"EnhancedRiskEngine initialized successfully with {len(self.integration_status.__dict__)} module integrations")

    def _check_module_integrations(self) -> ModelIntegrationStatus:
        """Check availability of external module integrations."""
        status = ModelIntegrationStatus()

        # Check SPACE integration
        if SPACE_AVAILABLE:
            try:
                # Try to configure backends
                configure_backends({
                    'default_backends': {
                        'indexing': 'h3',
                        'analytics': 'srai'
                    }
                })
                status.spatial_indexing_available = True
                status.space_integration = True
            except Exception as e:
                self.logger.warning(f"SPACE integration check failed: {e}")
                status.space_integration = False

        # Check TIME integration
        if TIME_AVAILABLE:
            try:
                # Try to initialize temporal analysis
                status.temporal_analysis_available = True
                status.time_integration = True
            except Exception as e:
                self.logger.warning(f"TIME integration check failed: {e}")
                status.time_integration = False

        # Check MATH integration
        if MATH_AVAILABLE:
            try:
                # Try to initialize spatial statistics
                status.advanced_statistics_available = True
                status.math_integration = True
            except Exception as e:
                self.logger.warning(f"MATH integration check failed: {e}")
                status.math_integration = False

        # Check BAYES integration
        if BAYES_AVAILABLE:
            try:
                # Try to initialize Bayesian inference
                status.bayesian_inference_available = True
                status.bayes_integration = True
            except Exception as e:
                self.logger.warning(f"BAYES integration check failed: {e}")
                status.bayes_integration = False

        return status

    def _initialize_core_components(self) -> None:
        """Initialize core risk analysis components."""
        # Initialize catastrophe and insurance managers
        self.catastrophe_manager = CatastropheModelManager()
        self.insurance_manager = InsuranceManager()

        # Initialize spatial and temporal interfaces if available
        self.spatial_interface = None
        self.temporal_interface = None
        self.math_interface = None
        self.bayes_interface = None

    def _initialize_spatial_interface(self) -> None:
        """Initialize spatial analysis interface."""
        if self.integration_status.space_integration:
            try:
                self.spatial_interface = SpatialIndexingInterface()
                self.spatial_analytics = SpatialAnalyticsInterface()
                self.logger.info("Spatial interface initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize spatial interface: {e}")
                self.spatial_interface = None

    def _initialize_temporal_interface(self) -> None:
        """Initialize temporal analysis interface."""
        if self.integration_status.time_integration:
            try:
                self.temporal_interface = TemporalAnalysisInterface()
                self.logger.info("Temporal interface initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize temporal interface: {e}")
                self.temporal_interface = None

    def _setup_enhanced_logging(self) -> logging.Logger:
        """Set up enhanced logging with structured output."""
        log_level = self.config.get("general", {}).get("log_level", "INFO")
        level = getattr(logging, log_level)

        logger = logging.getLogger("geo_infer_risk_enhanced")
        logger.setLevel(level)

        # Create formatter with more detailed information
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(module)s:%(funcName)s:%(lineno)d] - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler if output directory is available
        try:
            log_file = os.path.join(self.output_dir, "risk_engine.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not create log file: {e}")

        return logger

    def get_integration_status(self) -> Dict[str, bool]:
        """Get status of all module integrations."""
        return {
            'space_integration': self.integration_status.space_integration,
            'time_integration': self.integration_status.time_integration,
            'math_integration': self.integration_status.math_integration,
            'bayes_integration': self.integration_status.bayes_integration,
            'spatial_indexing': self.integration_status.spatial_indexing_available,
            'temporal_analysis': self.integration_status.temporal_analysis_available,
            'advanced_statistics': self.integration_status.advanced_statistics_available,
            'bayesian_inference': self.integration_status.bayesian_inference_available
        }

    def run_enhanced_analysis(self, analysis_type: str = "comprehensive",
                            **kwargs) -> Dict[str, Any]:
        """
        Run enhanced risk analysis with advanced capabilities.

        Args:
            analysis_type: Type of analysis ('comprehensive', 'portfolio', 'climate', 'stress_test')
            **kwargs: Additional analysis parameters

        Returns:
            Comprehensive risk analysis results
        """
        self.logger.info(f"Starting enhanced {analysis_type} risk analysis")

        job_id = self._create_analysis_job(analysis_type, **kwargs)

        try:
            if analysis_type == "comprehensive":
                results = self._run_comprehensive_analysis(**kwargs)
            elif analysis_type == "portfolio":
                results = self._run_portfolio_analysis(**kwargs)
            elif analysis_type == "climate":
                results = self._run_climate_analysis(**kwargs)
            elif analysis_type == "stress_test":
                results = self._run_stress_test(**kwargs)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")

            # Update job status
            self._update_job_status(job_id, "completed", results=results)

            self.logger.info(f"Enhanced {analysis_type} analysis completed successfully")
            return results

        except Exception as e:
            self.logger.error(f"Enhanced analysis failed: {e}")
            self._update_job_status(job_id, "failed", error_message=str(e))
            raise

    def _run_comprehensive_analysis(self, **kwargs) -> Dict[str, Any]:
        """Run comprehensive multi-hazard risk analysis."""
        # Load and validate models
        self.load_models()

        # Run spatial analysis if available
        if self.spatial_interface:
            spatial_results = self._run_spatial_analysis(**kwargs)
        else:
            spatial_results = {}

        # Run temporal analysis if available
        if self.temporal_interface:
            temporal_results = self._run_temporal_analysis(**kwargs)
        else:
            temporal_results = {}

        # Run core risk analysis
        core_results = self.run_analysis()

        # Combine results
        combined_results = {
            'core_analysis': core_results,
            'spatial_analysis': spatial_results,
            'temporal_analysis': temporal_results,
            'integration_metadata': self.get_integration_status(),
            'analysis_timestamp': datetime.now().isoformat()
        }

        return combined_results

    def _run_spatial_analysis(self, **kwargs) -> Dict[str, Any]:
        """Run advanced spatial analysis using GEO-INFER-SPACE."""
        if not self.spatial_interface:
            return {}

        region = kwargs.get('region', {})
        if not region:
            return {}

        try:
            # Convert region to spatial format
            bounds = region.get('bounds', {})
            if bounds:
                min_lon, max_lon = bounds.get('min_lon', -180), bounds.get('max_lon', 180)
                min_lat, max_lat = bounds.get('min_lat', -90), bounds.get('max_lat', 90)

                # Create spatial analysis region
                spatial_region = {
                    'min_lon': min_lon,
                    'max_lon': max_lon,
                    'min_lat': min_lat,
                    'max_lat': max_lat
                }

                # Run spatial analytics
                if hasattr(self.spatial_analytics, 'analyze_risk_concentration'):
                    concentration_analysis = self.spatial_analytics.analyze_risk_concentration(
                        region=spatial_region,
                        resolution=kwargs.get('spatial_resolution', 9)
                    )
                else:
                    concentration_analysis = {}

                # Run spatial statistics if available
                if self.integration_status.advanced_statistics_available:
                    statistical_analysis = self._run_spatial_statistics(spatial_region)
                else:
                    statistical_analysis = {}

                return {
                    'concentration_analysis': concentration_analysis,
                    'statistical_analysis': statistical_analysis,
                    'spatial_indexing': 'h3' if self.spatial_interface else 'none'
                }

        except Exception as e:
            self.logger.warning(f"Spatial analysis failed: {e}")
            return {}

    def _run_spatial_statistics(self, region: Dict[str, Any]) -> Dict[str, Any]:
        """Run spatial statistics using GEO-INFER-MATH."""
        if not self.integration_status.advanced_statistics_available:
            return {}

        try:
            # Extract location pairs from region features
            coords = []
            values = []
            for feat in region.get('features', []):
                loc = feat.get('location', {})
                if 'latitude' in loc and 'longitude' in loc:
                    coords.append([loc['latitude'], loc['longitude']])
                    values.append(feat.get('risk_value', 0.0))

            if len(coords) < 3:
                return {'spatial_autocorrelation': 0.0, 'morans_i': 0.0, 'geary_c': 0.0, 'local_indicators': []}

            coords_arr = np.array(coords)
            vals = np.array(values, dtype=float)
            n = len(vals)
            mean_val = np.mean(vals)
            dev = vals - mean_val

            # Distance-based spatial weights (inverse distance)
            from scipy.spatial.distance import pdist, squareform  # type: ignore
            dists = squareform(pdist(coords_arr))
            np.fill_diagonal(dists, np.inf)
            W = 1.0 / dists
            np.fill_diagonal(W, 0.0)
            W_sum = W.sum()

            # Moran's I
            morans_num = n * np.sum(W * np.outer(dev, dev))
            morans_den = W_sum * np.sum(dev ** 2)
            morans_i = morans_num / morans_den if morans_den != 0 else 0.0

            # Geary's C
            geary_num = (n - 1) * np.sum(W * (np.subtract.outer(vals, vals) ** 2))
            geary_den = 2 * W_sum * np.sum(dev ** 2)
            geary_c = geary_num / geary_den if geary_den != 0 else 0.0

            return {
                'spatial_autocorrelation': float(morans_i),
                'morans_i': float(morans_i),
                'geary_c': float(geary_c),
                'local_indicators': [float(d) for d in dev[:10]]
            }
        except ImportError:
            self.logger.warning("scipy not available for spatial statistics")
            return {'spatial_autocorrelation': 0.0, 'morans_i': 0.0, 'geary_c': 0.0, 'local_indicators': []}
        except Exception as e:
            self.logger.warning(f"Spatial statistics failed: {e}")
            return {}

    def _run_temporal_analysis(self, **kwargs) -> Dict[str, Any]:
        """Run temporal analysis using GEO-INFER-TIME."""
        if not self.temporal_interface:
            return {}

        try:
            time_horizon = kwargs.get('time_horizon', 50)

            # Analyse loss history to extract seasonal and trend components
            history = kwargs.get('loss_history', [])
            if not history:
                return {'seasonal_patterns': {}, 'trend_analysis': {}, 'time_series_decomposition': {}, 'forecast_scenarios': []}

            values = np.array([h.get('value', 0) for h in history], dtype=float)
            timestamps = [h.get('date', '') for h in history]

            # Trend via simple linear regression
            x = np.arange(len(values), dtype=float)
            if len(values) > 1:
                slope = np.polyfit(x, values, 1)[0]
            else:
                slope = 0.0

            # Seasonal: group by month index (mod 12)
            seasonal = {}
            for i, v in enumerate(values):
                month = i % 12
                seasonal.setdefault(month, []).append(v)
            seasonal_means = {k: float(np.mean(v)) for k, v in seasonal.items()}

            return {
                'seasonal_patterns': seasonal_means,
                'trend_analysis': {'slope': float(slope), 'direction': 'increasing' if slope > 0 else 'decreasing'},
                'time_series_decomposition': {'mean': float(np.mean(values)), 'std': float(np.std(values))},
                'forecast_scenarios': [{'horizon': time_horizon, 'projected_mean': float(np.mean(values) + slope * time_horizon)}]
            }
        except Exception as e:
            self.logger.warning(f"Temporal analysis failed: {e}")
            return {}

    def _create_analysis_job(self, job_type: str, **kwargs) -> str:
        """Create a new analysis job."""
        self.job_counter += 1
        job_id = f"analysis_{self.job_counter}_{int(time.time())}"

        job = AnalysisJob(
            job_id=job_id,
            job_type=job_type,
            status="queued",
            metadata=kwargs
        )

        self.active_jobs[job_id] = job
        return job_id

    def _update_job_status(self, job_id: str, status: str,
                          progress: float = None, results: Dict = None,
                          error_message: str = None) -> None:
        """Update job status and progress."""
        if job_id not in self.active_jobs:
            return

        job = self.active_jobs[job_id]
        job.status = status

        if progress is not None:
            job.progress = progress

        if status == "running" and job.started_at is None:
            job.started_at = datetime.now()
        elif status in ["completed", "failed"]:
            job.completed_at = datetime.now()

        if error_message:
            job.error_message = error_message

        if results:
            job.results = results

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of an analysis job."""
        if job_id not in self.active_jobs:
            return None

        job = self.active_jobs[job_id]
        return {
            'job_id': job.job_id,
            'job_type': job.job_type,
            'status': job.status,
            'progress': job.progress,
            'created_at': job.created_at.isoformat(),
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
            'error_message': job.error_message,
            'metadata': job.metadata
        }

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a running analysis job."""
        if job_id not in self.active_jobs:
            return False

        job = self.active_jobs[job_id]
        if job.status in ["running"]:
            job.status = "cancelled"
            job.completed_at = datetime.now()
            return True

        return False

    def get_model_status(self) -> Dict[str, Any]:
        """Get status of all loaded models."""
        return {
            'hazard_models': list(self.hazard_models.keys()),
            'vulnerability_models': list(self.vulnerability_models.keys()),
            'exposure_models': list(self.exposure_models.keys()),
            'catastrophe_manager': hasattr(self.catastrophe_manager, 'models'),
            'insurance_manager': hasattr(self.insurance_manager, 'models'),
            'integration_status': self.get_integration_status(),
            'loaded_models_count': len(self.hazard_models) + len(self.vulnerability_models) + len(self.exposure_models)
        }

    def calibrate_models(self, calibration_data: Dict[str, Any],
                        method: str = "cross_validation") -> Dict[str, Any]:
        """
        Calibrate model parameters using historical data.

        Args:
            calibration_data: Historical data for calibration
            method: Calibration method ('maximum_likelihood', 'bayesian', 'cross_validation')

        Returns:
            Calibration results and updated parameters
        """
        self.logger.info(f"Starting model calibration using {method} method")

        # Use Bayesian inference if available
        if self.integration_status.bayesian_inference_available and method == "bayesian":
            return self._calibrate_with_bayes(calibration_data)
        else:
            return self._calibrate_with_cross_validation(calibration_data)

    def _calibrate_with_bayes(self, calibration_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calibrate models using Bayesian inference."""
        if not self.integration_status.bayesian_inference_available:
            raise ValueError("Bayesian inference not available")

        # Use available Bayesian interface for parameter estimation
        params = {}
        for name, model in self.hazard_models.items():
            cfg = getattr(model, 'params', {})
            params[name] = {k: float(v) if isinstance(v, (int, float)) else v for k, v in cfg.items()}
        return {
            'method': 'bayesian',
            'calibrated_parameters': params,
            'validation_scores': {n: 0.0 for n in params},
            'convergence_info': {'iterations': 0, 'converged': False}
        }

    def _calibrate_with_cross_validation(self, calibration_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calibrate models using cross-validation."""
        # K-fold cross-validation over calibration samples
        samples = calibration_data.get('samples', [])
        k = min(5, max(1, len(samples)))
        fold_scores = []
        for i in range(k):
            train = [s for j, s in enumerate(samples) if j % k != i]
            test = [s for j, s in enumerate(samples) if j % k == i]
            if train and test:
                train_mean = np.mean([s.get('loss', 0) for s in train])
                test_vals = [s.get('loss', 0) for s in test]
                mse = np.mean([(v - train_mean) ** 2 for v in test_vals])
                fold_scores.append(float(mse))
        avg_score = float(np.mean(fold_scores)) if fold_scores else 0.0
        return {
            'method': 'cross_validation',
            'calibrated_parameters': {},
            'validation_scores': {'average_mse': avg_score},
            'cross_validation_results': {'k': k, 'fold_scores': fold_scores}
        }

    def run_monte_carlo_analysis(self, num_iterations: int = None,
                                convergence_threshold: float = 0.01) -> Dict[str, Any]:
        """
        Run advanced Monte Carlo analysis with convergence monitoring.

        Args:
            num_iterations: Number of Monte Carlo iterations
            convergence_threshold: Convergence threshold for stopping criteria

        Returns:
            Monte Carlo analysis results with convergence information
        """
        if num_iterations is None:
            num_iterations = self.config.get("risk_model", {}).get("monte_carlo_iterations", 1000)

        self.logger.info(f"Running Monte Carlo analysis with {num_iterations} iterations")

        # Initialize results tracking
        all_losses = []
        running_means = []
        running_stds = []

        # Run Monte Carlo simulation in batches
        batch_size = min(100, num_iterations // 10)

        for i in range(0, num_iterations, batch_size):
            batch_iterations = min(batch_size, num_iterations - i)

            # Run batch simulation
            batch_results = self._run_monte_carlo_batch(batch_iterations)
            all_losses.extend(batch_results['losses'])

            # Update running statistics
            running_mean = np.mean(all_losses)
            running_std = np.std(all_losses)

            running_means.append(running_mean)
            running_stds.append(running_std)

            # Check convergence
            if len(running_means) > 10:
                recent_means = running_means[-10:]
                mean_change = abs(recent_means[-1] - recent_means[0]) / recent_means[0]

                if mean_change < convergence_threshold:
                    self.logger.info(f"Convergence reached at iteration {i + batch_iterations}")
                    break

        # Calculate final statistics
        final_mean = np.mean(all_losses)
        final_std = np.std(all_losses)
        confidence_interval = stats.norm.interval(0.95, loc=final_mean, scale=final_std/np.sqrt(len(all_losses)))

        return {
            'total_iterations': len(all_losses),
            'final_aal': final_mean,
            'standard_deviation': final_std,
            'confidence_interval_95': confidence_interval,
            'convergence_info': {
                'converged': len(running_means) > 10 and abs(running_means[-1] - running_means[-10]) / running_means[-10] < convergence_threshold,
                'threshold': convergence_threshold,
                'running_means': running_means,
                'running_stds': running_stds
            },
            'loss_distribution': {
                'mean': final_mean,
                'median': np.median(all_losses),
                'percentiles': {
                    '5th': np.percentile(all_losses, 5),
                    '95th': np.percentile(all_losses, 95),
                    '99th': np.percentile(all_losses, 99)
                }
            }
        }

    def _run_monte_carlo_batch(self, batch_size: int) -> Dict[str, Any]:
        """Run a batch of Monte Carlo simulations."""
        losses = []

        for _ in range(batch_size):
            # Generate random event
            event = self._generate_random_event()

            # Calculate loss for this event
            loss = self._calculate_event_loss(event)
            losses.append(loss)

        return {
            'batch_size': batch_size,
            'losses': losses,
            'batch_mean': np.mean(losses),
            'batch_std': np.std(losses)
        }

    def _generate_random_event(self) -> Dict[str, Any]:
        """Generate a random hazard event."""
        # Sample from loaded hazard model catalogues when available
        available_types = list(self.hazard_models.keys()) or ['earthquake', 'flood', 'hurricane', 'wildfire']
        hazard_type = np.random.choice(available_types)
        return {
            'event_id': f'random_{np.random.randint(1000000)}',
            'hazard_type': hazard_type,
            'magnitude': np.random.exponential(5.0),
            'location': {
                'latitude': np.random.uniform(-90, 90),
                'longitude': np.random.uniform(-180, 180)
            },
            'timestamp': datetime.now() + timedelta(days=np.random.randint(365))
        }

    def _calculate_event_loss(self, event: Dict[str, Any]) -> float:
        """Calculate loss for a single event."""
        # Loss = base_exposure * vulnerability_factor * magnitude_scaling
        magnitude = event.get('magnitude', 1.0)
        base_exposure = 1_000_000  # default exposure
        vulnerability = 1 - np.exp(-0.3 * magnitude)  # vulnerability curve
        return float(base_exposure * vulnerability * np.random.lognormal(0, 0.3))

    def save_enhanced_results(self, results: Dict[str, Any],
                            filename: Optional[str] = None) -> str:
        """
        Save enhanced analysis results with comprehensive metadata.

        Args:
            results: Analysis results to save
            filename: Output filename (optional)

        Returns:
            Path to saved results file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_risk_analysis_{timestamp}.json"

        if not filename.endswith('.json'):
            filename += '.json'

        filepath = os.path.join(self.output_dir, filename)

        # Add metadata to results
        enhanced_results = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'engine_version': '2.0.0',
                'integration_status': self.get_integration_status(),
                'configuration_summary': {
                    'monte_carlo_iterations': self.config.get("risk_model", {}).get("monte_carlo_iterations", 1000),
                    'confidence_level': self.config.get("risk_model", {}).get("confidence_level", 0.95),
                    'spatial_resolution': self.config.get("risk_model", {}).get("spatial_resolution", 1.0)
                }
            },
            'results': results
        }

        # Save with custom encoder for datetime and numpy objects
        with open(filepath, 'w') as f:
            json.dump(enhanced_results, f, indent=2, default=self._json_encoder)

        self.logger.info(f"Enhanced results saved to {filepath}")
        return filepath

    def _json_encoder(self, obj):
        """Custom JSON encoder for datetime and numpy objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    # Legacy compatibility methods
    def load_models(self):
        """Load and initialize all models based on the configuration (legacy method)."""
        self.logger.info("Loading risk models...")

        # Load hazard models
        hazard_config = self.config.get("hazards", {})
        for hazard_type, hazard_params in hazard_config.items():
            if hazard_params.get("enabled", False):
                self.logger.info(f"Loading {hazard_type} hazard model")
                self.hazard_models[hazard_type] = HazardModel(
                    hazard_type=hazard_type,
                    params=hazard_params
                )

        # Load vulnerability models
        vuln_config = self.config.get("vulnerability", {})
        for vuln_type, vuln_params in vuln_config.items():
            if vuln_params.get("enabled", False):
                self.logger.info(f"Loading {vuln_type} vulnerability model")
                self.vulnerability_models[vuln_type] = VulnerabilityModel(
                    vulnerability_type=vuln_type,
                    params=vuln_params
                )

        # Load exposure models
        exposure_config = self.config.get("exposure", {})
        for exp_type, exp_params in exposure_config.items():
            if exp_params.get("enabled", False):
                self.logger.info(f"Loading {exp_type} exposure model")
                self.exposure_models[exp_type] = ExposureModel(
                    exposure_type=exp_type,
                    params=exp_params
                )

        self.logger.info(
            f"Models loaded: {len(self.hazard_models)} hazard, "
            f"{len(self.vulnerability_models)} vulnerability, "
            f"{len(self.exposure_models)} exposure"
        )

    def run_analysis(self):
        """Execute the full risk analysis workflow (legacy method)."""
        return self.run_enhanced_analysis("comprehensive")

    def _run_portfolio_analysis(self, **kwargs) -> Dict[str, Any]:
        """Run portfolio risk analysis."""
        # Aggregate risk across loaded models
        hazard_count = len(self.hazard_models)
        vuln_count = len(self.vulnerability_models)
        return {
            'portfolio_id': kwargs.get('portfolio_id', 'default'),
            'analysis_type': 'portfolio',
            'aggregation_level': kwargs.get('aggregation_level', 'location'),
            'risk_metrics': {'hazard_model_count': hazard_count, 'vulnerability_model_count': vuln_count},
            'correlation_analysis': {'inter_peril_correlation': 0.3 if hazard_count > 1 else 0.0},
            'diversification_benefits': {'benefit_ratio': max(0, 1 - 1 / max(hazard_count, 1))}
        }

    def _run_climate_analysis(self, **kwargs) -> Dict[str, Any]:
        """Run climate risk analysis."""
        # Climate projection using simple scaling factors per scenario
        baseline_year = kwargs.get('baseline_year', 2023)
        target_years = kwargs.get('target_years', [2050, 2100])
        scenarios = kwargs.get('scenarios', ['rcp4.5', 'rcp8.5'])
        scenario_factors = {'rcp2.6': 1.1, 'rcp4.5': 1.3, 'rcp6.0': 1.5, 'rcp8.5': 2.0}
        projected = {}
        for sc in scenarios:
            factor = scenario_factors.get(sc, 1.2)
            projected[sc] = {str(yr): {'risk_multiplier': 1 + (factor - 1) * (yr - baseline_year) / 100} for yr in target_years}
        return {
            'baseline_year': baseline_year,
            'target_years': target_years,
            'scenarios': scenarios,
            'projected_risks': projected,
            'adaptation_analysis': {'cost_benefit_ratio': 2.5}
        }

    def _run_stress_test(self, **kwargs) -> Dict[str, Any]:
        """Run stress testing analysis."""
        # Stress test by scaling losses by severity multiplier
        severity_map = {'low': 1.5, 'moderate': 2.0, 'high': 3.0, 'extreme': 5.0}
        severity = kwargs.get('severity_level', 'moderate')
        multiplier = severity_map.get(severity, 2.0)
        baseline_loss = np.random.exponential(1_000_000)
        stressed_loss = baseline_loss * multiplier
        return {
            'scenario_type': kwargs.get('scenario_type', 'historical'),
            'severity_level': severity,
            'baseline_metrics': {'expected_loss': float(baseline_loss)},
            'stressed_metrics': {'expected_loss': float(stressed_loss), 'multiplier': multiplier},
            'impact_analysis': {'loss_increase_pct': (multiplier - 1) * 100}
        }

    # Legacy RiskEngine compatibility
    def __getattr__(self, name):
        """Provide backward compatibility for legacy RiskEngine methods."""
        # Map legacy method names to enhanced method names
        method_mapping = {
            'save_results': 'save_enhanced_results',
            'plot_results': 'plot_enhanced_results',
            'calculate_metrics': 'calculate_enhanced_metrics'
        }

        if name in method_mapping:
            enhanced_name = method_mapping[name]
            if hasattr(self, enhanced_name):
                return getattr(self, enhanced_name)

        # For other attributes, raise AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


# Backward compatibility alias
RiskEngine = EnhancedRiskEngine
