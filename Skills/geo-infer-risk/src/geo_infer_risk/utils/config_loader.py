"""
Configuration loading and management utilities for GEO-INFER-RISK.

This module provides utilities for loading, validating, and managing
configuration files for the GEO-INFER-RISK module.
"""

import json
import os
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path
import yaml

from .validation import validate_config, ValidationResult

logger = logging.getLogger(__name__)

class ConfigurationLoader:
    """Configuration loader with validation and caching."""

    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize configuration loader.

        Args:
            schema_path: Path to JSON schema for validation
        """
        self.schema_path = schema_path
        self._config_cache = {}
        self._validation_cache = {}

    def load_config(self, config_path: Union[str, Path, Dict[str, Any]],
                   validate: bool = True, strict: bool = False,
                   use_cache: bool = True) -> Dict[str, Any]:
        """
        Load configuration from file or dictionary.

        Args:
            config_path: Path to configuration file or configuration dictionary
            validate: Whether to validate configuration
            strict: If True, treat warnings as errors during validation
            use_cache: Whether to use cached configurations

        Returns:
            Validated and normalized configuration dictionary

        Raises:
            FileNotFoundError: If config file not found
            ValidationError: If configuration validation fails
            ValueError: If configuration format is invalid
        """
        # Handle dictionary input
        if isinstance(config_path, dict):
            config = config_path
            cache_key = json.dumps(config, sort_keys=True)
        else:
            # Handle file path input
            config_path = Path(config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")

            cache_key = str(config_path.absolute())

            # Check cache
            if use_cache and cache_key in self._config_cache:
                return self._config_cache[cache_key]

            # Load from file
            config = self._load_config_file(config_path)

        # Validate if requested
        if validate:
            config = self._validate_and_process_config(config, strict)

        # Cache result
        if use_cache:
            self._config_cache[cache_key] = config

        return config

    def _load_config_file(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from file."""
        suffix = config_path.suffix.lower()

        try:
            if suffix in ['.yaml', '.yml']:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            elif suffix == '.json':
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                raise ValueError(f"Unsupported configuration file format: {suffix}")

        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ValueError(f"Error parsing configuration file {config_path}: {e}")

    def _validate_and_process_config(self, config: Dict[str, Any],
                                   strict: bool = False) -> Dict[str, Any]:
        """Validate and process configuration."""
        # Check validation cache
        config_hash = json.dumps(config, sort_keys=True)
        if config_hash in self._validation_cache:
            cached_result = self._validation_cache[config_hash]
            if cached_result.is_valid or not strict:
                return cached_result.validated_data
            else:
                raise ValueError(f"Configuration validation failed: {cached_result.errors}")

        # Validate configuration
        validation_result = validate_config(config, self.schema_path, strict)

        # Cache validation result
        self._validation_cache[config_hash] = validation_result

        if not validation_result.is_valid:
            error_msg = "Configuration validation failed:\n" + "\n".join(validation_result.errors)
            if validation_result.warnings:
                error_msg += "\nWarnings:\n" + "\n".join(validation_result.warnings)
            raise ValueError(error_msg)

        if validation_result.warnings and strict:
            warning_msg = "Configuration validation warnings treated as errors:\n" + \
                         "\n".join(validation_result.warnings)
            raise ValueError(warning_msg)

        # Log warnings if any
        if validation_result.warnings:
            logger.warning("Configuration validation warnings: %s",
                          ", ".join(validation_result.warnings))

        return validation_result.validated_data

    def load_config_with_defaults(self, config_path: Optional[Union[str, Path, Dict[str, Any]]] = None,
                                **overrides) -> Dict[str, Any]:
        """
        Load configuration with default values and optional overrides.

        Args:
            config_path: Path to configuration file or configuration dictionary
            **overrides: Configuration parameters to override

        Returns:
            Configuration with defaults applied and overrides merged
        """
        # Start with default configuration
        config = self.get_default_config()

        # Load from file or dictionary if provided
        if config_path is not None:
            loaded_config = self.load_config(config_path, validate=False)
            config = self._merge_configs(config, loaded_config)

        # Apply overrides
        config = self._merge_configs(config, overrides)

        # Validate final configuration
        return self._validate_and_process_config(config, strict=False)

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'general': {
                'log_level': 'INFO',
                'output_directory': './outputs',
                'cache_directory': './cache',
                'enable_caching': True,
                'parallel_processing': True,
                'num_workers': min(4, os.cpu_count() or 1),
                'random_seed': 42
            },
            'risk_model': {
                'confidence_level': 0.95,
                'time_horizon': 50,
                'spatial_resolution': 1.0,
                'monte_carlo_iterations': 1000,
                'include_secondary_perils': True,
                'correlation_model': 'spatial'
            },
            'hazards': {
                'flood': {
                    'enabled': False,
                    'type': 'riverine',
                    'return_periods': [10, 25, 50, 100, 500],
                    'data_source': 'noaa_nws',
                    'include_climate_change': False,
                    'climate_scenario': 'rcp4.5'
                },
                'earthquake': {
                    'enabled': False,
                    'type': 'probabilistic',
                    'return_periods': [100, 250, 500, 1000, 2500],
                    'include_secondary_perils': True,
                    'secondary_perils': ['liquefaction', 'landslide'],
                    'data_source': 'usgs'
                },
                'hurricane': {
                    'enabled': False,
                    'include_components': ['wind', 'storm_surge', 'rainfall'],
                    'track_data_source': 'hurdat2',
                    'return_periods': [10, 25, 50, 100],
                    'data_source': 'noaa_hurricane'
                },
                'wildfire': {
                    'enabled': False,
                    'fuel_model': 'standard',
                    'include_climate_factors': True,
                    'climate_scenario': 'rcp4.5',
                    'data_source': 'usfs'
                }
            },
            'vulnerability': {
                'building': {
                    'enabled': True,
                    'classification_scheme': 'hazus',
                    'include_factors': ['construction_type', 'year_built', 'stories', 'foundation_type'],
                    'uncertainty_method': 'none',
                    'data_source': 'hazus'
                },
                'infrastructure': {
                    'enabled': True,
                    'classification_scheme': 'custom',
                    'types': ['roads', 'bridges', 'power_lines', 'water_supply'],
                    'uncertainty_method': 'none',
                    'data_source': 'custom'
                },
                'population': {
                    'enabled': True,
                    'demographic_factors': ['age', 'income', 'mobility', 'housing_quality'],
                    'social_vulnerability_index': True,
                    'uncertainty_method': 'none',
                    'data_source': 'census'
                }
            },
            'exposure': {
                'property': {
                    'enabled': True,
                    'data_sources': ['openstreetmap', 'custom_property_db'],
                    'value_type': 'replacement_cost',
                    'include_contents': True,
                    'aggregation_level': 'building'
                },
                'population': {
                    'enabled': True,
                    'data_sources': ['census', 'worldpop'],
                    'time_of_day_scenarios': ['day', 'night', 'commute'],
                    'aggregation_level': 'census_block'
                },
                'infrastructure': {
                    'enabled': True,
                    'data_sources': ['openstreetmap', 'custom_lifeline_db'],
                    'types': ['transportation', 'utilities', 'communications'],
                    'valuation_method': 'replacement_cost'
                }
            },
            'output': {
                'formats': ['geojson', 'csv', 'json'],
                'metrics': ['aal', 'oep', 'ep_curve', 'return_period_losses'],
                'exceedance_probabilities': [0.5, 0.2, 0.1, 0.04, 0.02, 0.01, 0.004, 0.002],
                'include_uncertainty': True,
                'uncertainty_metrics': ['mean', 'median', 'stdev', 'percentile_5', 'percentile_95']
            },
            'integrations': {
                'geo_infer_space': {
                    'enabled': True,
                    'spatial_indexing': 'h3',
                    'resolution': 9,
                    'analytics_backend': 'srai'
                },
                'geo_infer_time': {
                    'enabled': True,
                    'temporal_resolution': 'daily',
                    'include_seasonality': True,
                    'time_series_analysis': False
                },
                'geo_infer_ai': {
                    'enabled': False,
                    'models': ['damage_classification', 'claims_prediction'],
                    'inference_backend': 'scikit_learn'
                },
                'geo_infer_math': {
                    'enabled': True,
                    'statistical_methods': ['extreme_value_theory', 'monte_carlo', 'bootstrap'],
                    'numerical_precision': 'double',
                    'optimization_method': 'gradient_descent'
                }
            }
        }

    def _merge_configs(self, base_config: Dict[str, Any],
                      override_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two configuration dictionaries recursively."""
        merged = base_config.copy()

        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value

        return merged

    def save_config(self, config: Dict[str, Any], output_path: Union[str, Path],
                   format: str = 'auto') -> str:
        """
        Save configuration to file.

        Args:
            config: Configuration to save
            output_path: Path to save configuration
            format: Output format ('yaml', 'json', 'auto')

        Returns:
            Path to saved configuration file
        """
        output_path = Path(output_path)

        # Auto-detect format
        if format == 'auto':
            if output_path.suffix.lower() in ['.yaml', '.yml']:
                format = 'yaml'
            else:
                format = 'json'

        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save in specified format
        if format == 'yaml':
            with open(output_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        elif format == 'json':
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=2)
        else:
            raise ValueError(f"Unsupported output format: {format}")

        logger.info(f"Configuration saved to {output_path}")
        return str(output_path)

    def create_example_config(self, output_path: Union[str, Path],
                            hazard_types: Optional[list] = None,
                            include_comments: bool = True) -> str:
        """
        Create an example configuration file.

        Args:
            output_path: Path to save example configuration
            hazard_types: List of hazard types to include
            include_comments: Whether to include explanatory comments

        Returns:
            Path to created example configuration file
        """
        config = self.get_default_config()

        # Filter to specific hazard types if requested
        if hazard_types:
            config['hazards'] = {
                k: v for k, v in config['hazards'].items()
                if k in hazard_types
            }

        # Add comments if requested
        if include_comments:
            config = self._add_config_comments(config)

        return self.save_config(config, output_path, 'yaml')

    def _add_config_comments(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Add explanatory comments to configuration."""
        # This is a simplified implementation
        # In a real implementation, this would use a more sophisticated approach
        # to add comments to YAML output

        commented_config = {
            '_comment_general': 'General settings for logging, output, and processing',
            'general': config['general'],
            '_comment_risk_model': 'Core risk model parameters',
            'risk_model': config['risk_model'],
            '_comment_hazards': 'Hazard model configurations',
            'hazards': config['hazards'],
            '_comment_vulnerability': 'Vulnerability model configurations',
            'vulnerability': config['vulnerability'],
            '_comment_exposure': 'Exposure model configurations',
            'exposure': config['exposure'],
            '_comment_output': 'Output format and metrics configuration',
            'output': config['output'],
            '_comment_integrations': 'Integration with other GEO-INFER modules',
            'integrations': config['integrations']
        }

        return commented_config

    def clear_cache(self) -> None:
        """Clear configuration and validation caches."""
        self._config_cache.clear()
        self._validation_cache.clear()
        logger.info("Configuration caches cleared")

# Global configuration loader instance
_config_loader = ConfigurationLoader()

def load_config(config_path: Union[str, Path, Dict[str, Any]],
               validate: bool = True, strict: bool = False) -> Dict[str, Any]:
    """
    Load configuration from file or dictionary.

    Args:
        config_path: Path to configuration file or configuration dictionary
        validate: Whether to validate configuration
        strict: If True, treat warnings as errors during validation

    Returns:
        Validated and normalized configuration dictionary
    """
    return _config_loader.load_config(config_path, validate, strict)

def load_config_with_defaults(config_path: Optional[Union[str, Path, Dict[str, Any]]] = None,
                            **overrides) -> Dict[str, Any]:
    """
    Load configuration with default values and optional overrides.

    Args:
        config_path: Path to configuration file or configuration dictionary
        **overrides: Configuration parameters to override

    Returns:
        Configuration with defaults applied and overrides merged
    """
    return _config_loader.load_config_with_defaults(config_path, **overrides)

def create_example_config(output_path: Union[str, Path],
                         hazard_types: Optional[list] = None) -> str:
    """
    Create an example configuration file.

    Args:
        output_path: Path to save example configuration
        hazard_types: List of hazard types to include

    Returns:
        Path to created example configuration file
    """
    return _config_loader.create_example_config(output_path, hazard_types)

def get_default_config() -> Dict[str, Any]:
    """Get default configuration."""
    return _config_loader.get_default_config()

def save_config(config: Dict[str, Any], output_path: Union[str, Path],
               format: str = 'auto') -> str:
    """
    Save configuration to file.

    Args:
        config: Configuration to save
        output_path: Path to save configuration
        format: Output format ('yaml', 'json', 'auto')

    Returns:
        Path to saved configuration file
    """
    return _config_loader.save_config(config, output_path, format)
