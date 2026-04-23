"""
Configuration validation and data validation utilities for GEO-INFER-RISK.

This module provides comprehensive validation capabilities for configuration files,
data inputs, and model parameters using JSON Schema validation and custom validators.
"""

import json
import os
import logging
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import jsonschema
import yaml
import pandas as pd
import numpy as np
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of validation operation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    validated_data: Dict[str, Any]

class ConfigurationValidator:
    """Comprehensive configuration validator for GEO-INFER-RISK."""

    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize configuration validator.

        Args:
            schema_path: Path to JSON schema file for validation
        """
        self.schema_path = schema_path or self._get_default_schema_path()
        self.schema = self._load_schema()
        self.custom_validators = self._initialize_custom_validators()

    def _get_default_schema_path(self) -> str:
        """Get default schema path."""
        current_dir = Path(__file__).parent.parent.parent
        return str(current_dir / "config" / "schema.json")

    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON schema for validation."""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Schema file not found at {self.schema_path}. Using basic validation.")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON schema: {e}")
            return {}

    def _initialize_custom_validators(self) -> Dict[str, callable]:
        """Initialize custom validation functions."""
        return {
            'validate_return_periods': self._validate_return_periods,
            'validate_probabilities': self._validate_probabilities,
            'validate_coordinates': self._validate_coordinates,
            'validate_file_paths': self._validate_file_paths,
            'validate_currency_codes': self._validate_currency_codes,
            'validate_hazard_types': self._validate_hazard_types,
            'validate_vulnerability_schemes': self._validate_vulnerability_schemes
        }

    def validate_config(self, config: Dict[str, Any],
                       strict: bool = True) -> ValidationResult:
        """
        Validate configuration against schema and custom rules.

        Args:
            config: Configuration dictionary to validate
            strict: If True, treat warnings as errors

        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        validated_config = config.copy()

        try:
            # JSON Schema validation
            if self.schema:
                jsonschema.validate(instance=config, schema=self.schema)

            # Custom validation rules
            self._validate_general_config(validated_config, errors, warnings)
            self._validate_risk_model_config(validated_config, errors, warnings)
            self._validate_hazards_config(validated_config, errors, warnings)
            self._validate_vulnerability_config(validated_config, errors, warnings)
            self._validate_exposure_config(validated_config, errors, warnings)
            self._validate_output_config(validated_config, errors, warnings)
            self._validate_integrations_config(validated_config, errors, warnings)

            # Apply defaults and normalize values
            validated_config = self._apply_defaults_and_normalize(validated_config)

        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")

        is_valid = len(errors) == 0 and (not strict or len(warnings) == 0)

        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            validated_data=validated_config
        )

    def _validate_general_config(self, config: Dict[str, Any],
                               errors: List[str], warnings: List[str]) -> None:
        """Validate general configuration section."""
        general = config.get('general', {})

        # Validate log level
        log_level = general.get('log_level', 'INFO')
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if log_level not in valid_log_levels:
            errors.append(f"Invalid log level: {log_level}")

        # Validate directories
        output_dir = general.get('output_directory', './outputs')
        if not self._is_valid_directory_path(output_dir):
            warnings.append(f"Output directory may not be writable: {output_dir}")

        cache_dir = general.get('cache_directory', './cache')
        if not self._is_valid_directory_path(cache_dir):
            warnings.append(f"Cache directory may not be writable: {cache_dir}")

        # Validate worker count
        num_workers = general.get('num_workers', 4)
        if num_workers < 1 or num_workers > os.cpu_count():
            warnings.append(f"num_workers ({num_workers}) outside recommended range")

    def _validate_risk_model_config(self, config: Dict[str, Any],
                                  errors: List[str], warnings: List[str]) -> None:
        """Validate risk model configuration section."""
        risk_model = config.get('risk_model', {})

        # Validate confidence level
        confidence = risk_model.get('confidence_level', 0.95)
        if not 0.5 <= confidence <= 0.99:
            errors.append(f"Confidence level must be between 0.5 and 0.99, got {confidence}")

        # Validate time horizon
        time_horizon = risk_model.get('time_horizon', 50)
        if not 1 <= time_horizon <= 500:
            errors.append(f"Time horizon must be between 1 and 500 years, got {time_horizon}")

        # Validate Monte Carlo iterations
        iterations = risk_model.get('monte_carlo_iterations', 1000)
        if not 100 <= iterations <= 100000:
            warnings.append(f"Monte Carlo iterations ({iterations}) outside recommended range")

        # Validate spatial resolution
        resolution = risk_model.get('spatial_resolution', 1.0)
        if resolution <= 0:
            errors.append(f"Spatial resolution must be positive, got {resolution}")

    def _validate_hazards_config(self, config: Dict[str, Any],
                               errors: List[str], warnings: List[str]) -> None:
        """Validate hazards configuration section."""
        hazards = config.get('hazards', {})

        if not hazards:
            warnings.append("No hazard models configured")

        for hazard_name, hazard_config in hazards.items():
            if not hazard_config.get('enabled', False):
                continue

            # Validate return periods
            return_periods = hazard_config.get('return_periods', [])
            if return_periods:
                self._validate_return_periods(return_periods, errors, hazard_name)

            # Validate hazard-specific parameters
            self._validate_hazard_specific_config(hazard_name, hazard_config, errors, warnings)

    def _validate_vulnerability_config(self, config: Dict[str, Any],
                                     errors: List[str], warnings: List[str]) -> None:
        """Validate vulnerability configuration section."""
        vulnerability = config.get('vulnerability', {})

        for vuln_name, vuln_config in vulnerability.items():
            if not vuln_config.get('enabled', False):
                continue

            # Validate classification scheme
            scheme = vuln_config.get('classification_scheme', 'custom')
            self._validate_vulnerability_schemes([scheme], errors, vuln_name)

    def _validate_exposure_config(self, config: Dict[str, Any],
                                errors: List[str], warnings: List[str]) -> None:
        """Validate exposure configuration section."""
        exposure = config.get('exposure', {})

        for exp_name, exp_config in exposure.items():
            if not exp_config.get('enabled', False):
                continue

            # Validate data sources
            data_sources = exp_config.get('data_sources', [])
            if not data_sources:
                errors.append(f"No data sources specified for exposure type: {exp_name}")

            # Validate file paths if provided
            for source in data_sources:
                if source.startswith(('file://', './', '/')):
                    self._validate_file_paths([source], errors, exp_name)

    def _validate_output_config(self, config: Dict[str, Any],
                              errors: List[str], warnings: List[str]) -> None:
        """Validate output configuration section."""
        output = config.get('output', {})

        # Validate formats
        formats = output.get('formats', ['json'])
        valid_formats = ['geojson', 'csv', 'shapefile', 'netcdf', 'parquet', 'json', 'excel']
        invalid_formats = [f for f in formats if f not in valid_formats]
        if invalid_formats:
            errors.append(f"Invalid output formats: {invalid_formats}")

        # Validate exceedance probabilities
        exceedance_probs = output.get('exceedance_probabilities', [])
        if exceedance_probs:
            self._validate_probabilities(exceedance_probs, errors, 'exceedance_probabilities')

    def _validate_integrations_config(self, config: Dict[str, Any],
                                    errors: List[str], warnings: List[str]) -> None:
        """Validate integrations configuration section."""
        integrations = config.get('integrations', {})

        # Validate GEO-INFER module integrations
        for module_name, module_config in integrations.items():
            if module_config.get('enabled', False):
                self._validate_module_integration(module_name, module_config, errors, warnings)

    def _validate_hazard_specific_config(self, hazard_name: str, hazard_config: Dict[str, Any],
                                       errors: List[str], warnings: List[str]) -> None:
        """Validate hazard-specific configuration parameters."""
        hazard_type = hazard_config.get('type', '')

        if hazard_type == 'earthquake':
            self._validate_earthquake_config(hazard_config, errors, warnings)
        elif hazard_type == 'flood':
            self._validate_flood_config(hazard_config, errors, warnings)
        elif hazard_type == 'hurricane':
            self._validate_hurricane_config(hazard_config, errors, warnings)
        elif hazard_type == 'wildfire':
            self._validate_wildfire_config(hazard_config, errors, warnings)

    def _validate_earthquake_config(self, config: Dict[str, Any],
                                  errors: List[str], warnings: List[str]) -> None:
        """Validate earthquake-specific configuration."""
        eq_type = config.get('type', 'probabilistic')
        if eq_type == 'deterministic':
            if 'scenario_magnitude' not in config:
                errors.append("scenario_magnitude required for deterministic earthquake model")
            if 'scenario_location' not in config:
                errors.append("scenario_location required for deterministic earthquake model")

    def _validate_flood_config(self, config: Dict[str, Any],
                             errors: List[str], warnings: List[str]) -> None:
        """Validate flood-specific configuration."""
        flood_type = config.get('type', 'riverine')
        if flood_type in ['coastal', 'combined']:
            warnings.append(f"Coastal flood modeling may require additional data sources")

    def _validate_hurricane_config(self, config: Dict[str, Any],
                                 errors: List[str], warnings: List[str]) -> None:
        """Validate hurricane-specific configuration."""
        components = config.get('include_components', ['wind'])
        if 'storm_surge' in components and 'bathymetry_data' not in config:
            warnings.append("Storm surge modeling requires bathymetry data")

    def _validate_wildfire_config(self, config: Dict[str, Any],
                                errors: List[str], warnings: List[str]) -> None:
        """Validate wildfire-specific configuration."""
        fuel_model = config.get('fuel_model', 'standard')
        if fuel_model != 'standard' and 'fuel_data' not in config:
            errors.append("Custom fuel model requires fuel_data specification")

    def _validate_module_integration(self, module_name: str, module_config: Dict[str, Any],
                                   errors: List[str], warnings: List[str]) -> None:
        """Validate integration with other GEO-INFER modules."""
        if module_name == 'geo_infer_space':
            self._validate_space_integration(module_config, errors, warnings)
        elif module_name == 'geo_infer_time':
            self._validate_time_integration(module_config, errors, warnings)
        elif module_name == 'geo_infer_ai':
            self._validate_ai_integration(module_config, errors, warnings)
        elif module_name == 'geo_infer_math':
            self._validate_math_integration(module_config, errors, warnings)

    def _validate_space_integration(self, config: Dict[str, Any],
                                  errors: List[str], warnings: List[str]) -> None:
        """Validate GEO-INFER-SPACE integration."""
        indexing = config.get('spatial_indexing', 'h3')
        valid_indexing = ['h3', 'geohash', 'quadtree', 's2']
        if indexing not in valid_indexing:
            errors.append(f"Invalid spatial indexing method: {indexing}")

        resolution = config.get('resolution', 9)
        if not 0 <= resolution <= 15:
            errors.append(f"Invalid spatial resolution: {resolution}")

    def _validate_time_integration(self, config: Dict[str, Any],
                                 errors: List[str], warnings: List[str]) -> None:
        """Validate GEO-INFER-TIME integration."""
        temporal_resolution = config.get('temporal_resolution', 'yearly')
        valid_resolutions = ['hourly', 'daily', 'weekly', 'monthly', 'yearly', 'event']
        if temporal_resolution not in valid_resolutions:
            errors.append(f"Invalid temporal resolution: {temporal_resolution}")

    def _validate_ai_integration(self, config: Dict[str, Any],
                               errors: List[str], warnings: List[str]) -> None:
        """Validate GEO-INFER-AI integration."""
        models = config.get('models', [])
        if not models:
            errors.append("No AI models specified for AI integration")

        backend = config.get('inference_backend', 'scikit_learn')
        valid_backends = ['tensorflow', 'pytorch', 'scikit_learn', 'xgboost']
        if backend not in valid_backends:
            errors.append(f"Invalid AI backend: {backend}")

    def _validate_math_integration(self, config: Dict[str, Any],
                                 errors: List[str], warnings: List[str]) -> None:
        """Validate GEO-INFER-MATH integration."""
        methods = config.get('statistical_methods', [])
        if not methods:
            errors.append("No statistical methods specified for math integration")

        precision = config.get('numerical_precision', 'double')
        valid_precisions = ['single', 'double', 'extended']
        if precision not in valid_precisions:
            errors.append(f"Invalid numerical precision: {precision}")

    def _validate_return_periods(self, return_periods: List[int],
                               errors: List[str], context: str = '') -> None:
        """Validate return periods array."""
        if not return_periods:
            errors.append(f"No return periods specified for {context}")
            return

        if len(return_periods) < 2:
            errors.append(f"At least 2 return periods required for {context}")
            return

        if not all(isinstance(rp, int) and rp > 0 for rp in return_periods):
            errors.append(f"All return periods must be positive integers for {context}")

        if len(set(return_periods)) != len(return_periods):
            errors.append(f"Duplicate return periods found for {context}")

        # Check if return periods are reasonable
        if any(rp < 1 for rp in return_periods):
            errors.append(f"Return periods must be at least 1 year for {context}")

        if any(rp > 10000 for rp in return_periods):
            errors.append(f"Return periods over 10,000 years may not be meaningful for {context}")

    def _validate_probabilities(self, probabilities: List[float],
                              errors: List[str], context: str = '') -> None:
        """Validate probability arrays."""
        if not probabilities:
            errors.append(f"No probabilities specified for {context}")
            return

        if not all(isinstance(p, (int, float)) and 0 <= p <= 1 for p in probabilities):
            errors.append(f"All probabilities must be between 0 and 1 for {context}")

        if len(set(probabilities)) != len(probabilities):
            errors.append(f"Duplicate probabilities found for {context}")

    def _validate_coordinates(self, coordinates: List[List[float]],
                            errors: List[str], context: str = '') -> None:
        """Validate coordinate arrays."""
        for i, coord in enumerate(coordinates):
            if len(coord) != 2:
                errors.append(f"Coordinate {i} must have exactly 2 values (lat, lon) for {context}")
                continue

            lat, lon = coord
            if not (-90 <= lat <= 90):
                errors.append(f"Latitude {lat} out of range [-90, 90] for {context}")

            if not (-180 <= lon <= 180):
                errors.append(f"Longitude {lon} out of range [-180, 180] for {context}")

    def _validate_file_paths(self, file_paths: List[str],
                           errors: List[str], context: str = '') -> None:
        """Validate file paths."""
        for path in file_paths:
            if not os.path.exists(path):
                errors.append(f"File not found: {path} for {context}")

    def _validate_currency_codes(self, currency_codes: List[str],
                               errors: List[str], context: str = '') -> None:
        """Validate currency codes."""
        valid_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'INR']
        for code in currency_codes:
            if code not in valid_currencies:
                errors.append(f"Invalid currency code: {code} for {context}")

    def _validate_hazard_types(self, hazard_types: List[str],
                             errors: List[str], context: str = '') -> None:
        """Validate hazard types."""
        valid_hazards = [
            'earthquake', 'flood', 'hurricane', 'tornado', 'wildfire', 'drought',
            'landslide', 'tsunami', 'volcanic', 'storm_surge', 'winter_storm',
            'hail', 'lightning', 'wind', 'heat_wave', 'cold_wave'
        ]
        for hazard in hazard_types:
            if hazard not in valid_hazards:
                errors.append(f"Invalid hazard type: {hazard} for {context}")

    def _validate_vulnerability_schemes(self, schemes: List[str],
                                     errors: List[str], context: str = '') -> None:
        """Validate vulnerability classification schemes."""
        valid_schemes = ['hazus', 'european', 'custom', 'gem', 'fema', 'iso']
        for scheme in schemes:
            if scheme not in valid_schemes:
                errors.append(f"Invalid vulnerability scheme: {scheme} for {context}")

    def _is_valid_directory_path(self, path: str) -> bool:
        """Check if path is a valid directory or can be created."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except (OSError, PermissionError):
            return False

    def _apply_defaults_and_normalize(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply default values and normalize configuration."""
        # Apply defaults for missing sections
        defaults = {
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
            }
        }

        # Apply defaults
        for section, default_values in defaults.items():
            if section not in config:
                config[section] = {}
            for key, value in default_values.items():
                if key not in config[section]:
                    config[section][key] = value

        # Normalize numeric values
        self._normalize_numeric_values(config)

        return config

    def _normalize_numeric_values(self, config: Dict[str, Any]) -> None:
        """Normalize numeric values in configuration."""
        # Ensure return periods are integers
        for hazard_config in config.get('hazards', {}).values():
            if 'return_periods' in hazard_config:
                hazard_config['return_periods'] = [int(rp) for rp in hazard_config['return_periods']]

        # Ensure probabilities are floats
        output_config = config.get('output', {})
        if 'exceedance_probabilities' in output_config:
            output_config['exceedance_probabilities'] = [
                float(p) for p in output_config['exceedance_probabilities']
            ]

def validate_config(config: Dict[str, Any], schema_path: Optional[str] = None,
                   strict: bool = True) -> ValidationResult:
    """
    Validate configuration against schema and custom rules.

    Args:
        config: Configuration dictionary to validate
        schema_path: Path to JSON schema file
        strict: If True, treat warnings as errors

    Returns:
        ValidationResult with validation status and details
    """
    validator = ConfigurationValidator(schema_path)
    return validator.validate_config(config, strict)

def validate_data_file(file_path: str, data_type: str = 'auto') -> ValidationResult:
    """
    Validate data file format and content.

    Args:
        file_path: Path to data file
        data_type: Expected data type ('csv', 'json', 'geojson', 'shapefile', 'auto')

    Returns:
        ValidationResult with validation status and details
    """
    errors = []
    warnings = []

    if not os.path.exists(file_path):
        return ValidationResult(False, [f"File not found: {file_path}"], [], {})

    try:
        # Auto-detect file type if not specified
        if data_type == 'auto':
            ext = Path(file_path).suffix.lower()
            if ext == '.csv':
                data_type = 'csv'
            elif ext == '.json' or ext == '.geojson':
                data_type = 'json'
            elif ext in ['.shp', '.dbf', '.prj', '.shx']:
                data_type = 'shapefile'
            else:
                data_type = 'unknown'

        if data_type == 'csv':
            return validate_csv_file(file_path)
        elif data_type == 'json':
            return validate_json_file(file_path)
        elif data_type == 'shapefile':
            return validate_shapefile(file_path)
        else:
            return ValidationResult(False, [f"Unsupported data type: {data_type}"], [], {})

    except Exception as e:
        return ValidationResult(False, [f"Error validating file: {str(e)}"], [], {})

def validate_csv_file(file_path: str) -> ValidationResult:
    """Validate CSV file format and content."""
    errors = []
    warnings = []

    try:
        df = pd.read_csv(file_path)

        # Check for required columns
        if len(df.columns) == 0:
            errors.append("CSV file has no columns")
        else:
            # Check for common geospatial columns
            geospatial_columns = ['latitude', 'longitude', 'lat', 'lon', 'x', 'y']
            has_geospatial = any(col.lower() in geospatial_columns for col in df.columns)

            if not has_geospatial:
                warnings.append("No geospatial columns detected (latitude/longitude)")

            # Check for value columns
            value_columns = ['value', 'amount', 'cost', 'price', 'loss']
            has_values = any(col.lower() in value_columns for col in df.columns)

            if not has_values:
                warnings.append("No value columns detected")

        # Check data quality
        if df.empty:
            warnings.append("CSV file is empty")

        missing_data = df.isnull().sum().sum()
        if missing_data > 0:
            warnings.append(f"Found {missing_data} missing values")

        # Check for duplicate rows
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            warnings.append(f"Found {duplicates} duplicate rows")

        return ValidationResult(len(errors) == 0, errors, warnings, df.to_dict('records'))

    except Exception as e:
        return ValidationResult(False, [f"Error reading CSV file: {str(e)}"], [], {})

def validate_json_file(file_path: str) -> ValidationResult:
    """Validate JSON file format and content."""
    errors = []
    warnings = []

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Check if it's a valid JSON structure
        if not isinstance(data, (dict, list)):
            errors.append("JSON file must contain object or array at root level")

        # Check for GeoJSON structure if it has geospatial features
        if isinstance(data, dict) and data.get('type') == 'FeatureCollection':
            warnings.append("GeoJSON format detected")

        return ValidationResult(len(errors) == 0, errors, warnings, data)

    except json.JSONDecodeError as e:
        return ValidationResult(False, [f"Invalid JSON format: {str(e)}"], [], {})
    except Exception as e:
        return ValidationResult(False, [f"Error reading JSON file: {str(e)}"], [], {})

def validate_shapefile(file_path: str) -> ValidationResult:
    """Validate shapefile format and content."""
    errors = []
    warnings = []

    try:
        import geopandas as gpd

        # Check if it's a valid shapefile
        if not file_path.endswith('.shp'):
            # Try to find the .shp file
            shp_path = file_path.replace('.dbf', '.shp').replace('.prj', '.shp').replace('.shx', '.shp')
            if os.path.exists(shp_path):
                file_path = shp_path
            else:
                errors.append("No .shp file found")

        if not errors:
            gdf = gpd.read_file(file_path)

            if gdf.empty:
                warnings.append("Shapefile is empty")
            else:
                # Check for geometry column
                if 'geometry' not in gdf.columns:
                    errors.append("No geometry column found in shapefile")

                # Check coordinate reference system
                if gdf.crs is None:
                    warnings.append("No coordinate reference system defined")

                # Check for common attribute columns
                attr_columns = ['value', 'amount', 'cost', 'population', 'area']
                has_attributes = any(col.lower() in attr_columns for col in gdf.columns)

                if not has_attributes:
                    warnings.append("No common attribute columns found")

            return ValidationResult(len(errors) == 0, errors, warnings, gdf.to_dict('records'))

    except ImportError:
        return ValidationResult(False, ["geopandas not available for shapefile validation"], [], {})
    except Exception as e:
        return ValidationResult(False, [f"Error reading shapefile: {str(e)}"], [], {})

def validate_model_parameters(model_type: str, parameters: Dict[str, Any]) -> ValidationResult:
    """
    Validate model parameters for specific model types.

    Args:
        model_type: Type of model ('hazard', 'vulnerability', 'exposure', 'insurance')
        parameters: Model parameters to validate

    Returns:
        ValidationResult with validation status and details
    """
    errors = []
    warnings = []

    if model_type == 'hazard':
        return validate_hazard_parameters(parameters)
    elif model_type == 'vulnerability':
        return validate_vulnerability_parameters(parameters)
    elif model_type == 'exposure':
        return validate_exposure_parameters(parameters)
    elif model_type == 'insurance':
        return validate_insurance_parameters(parameters)
    else:
        return ValidationResult(False, [f"Unknown model type: {model_type}"], [], parameters)

def validate_hazard_parameters(parameters: Dict[str, Any]) -> ValidationResult:
    """Validate hazard model parameters."""
    errors = []
    warnings = []

    required_params = ['hazard_type', 'return_periods']
    for param in required_params:
        if param not in parameters:
            errors.append(f"Required hazard parameter missing: {param}")

    hazard_type = parameters.get('hazard_type', '')
    if hazard_type:
        valid_hazards = [
            'earthquake', 'flood', 'hurricane', 'tornado', 'wildfire', 'drought',
            'landslide', 'tsunami', 'volcanic', 'storm_surge', 'winter_storm'
        ]
        if hazard_type not in valid_hazards:
            errors.append(f"Invalid hazard type: {hazard_type}")

    return_periods = parameters.get('return_periods', [])
    if return_periods:
        if not all(isinstance(rp, int) and rp > 0 for rp in return_periods):
            errors.append("All return periods must be positive integers")

    return ValidationResult(len(errors) == 0, errors, warnings, parameters)

def validate_vulnerability_parameters(parameters: Dict[str, Any]) -> ValidationResult:
    """Validate vulnerability model parameters."""
    errors = []
    warnings = []

    required_params = ['vulnerability_type', 'classification_scheme']
    for param in required_params:
        if param not in parameters:
            errors.append(f"Required vulnerability parameter missing: {param}")

    scheme = parameters.get('classification_scheme', '')
    if scheme:
        valid_schemes = ['hazus', 'european', 'custom', 'gem', 'fema']
        if scheme not in valid_schemes:
            errors.append(f"Invalid vulnerability classification scheme: {scheme}")

    return ValidationResult(len(errors) == 0, errors, warnings, parameters)

def validate_exposure_parameters(parameters: Dict[str, Any]) -> ValidationResult:
    """Validate exposure model parameters."""
    errors = []
    warnings = []

    required_params = ['exposure_type', 'data_sources', 'value_type']
    for param in required_params:
        if param not in parameters:
            errors.append(f"Required exposure parameter missing: {param}")

    value_type = parameters.get('value_type', '')
    if value_type:
        valid_types = ['replacement_cost', 'market_value', 'depreciated_value', 'custom']
        if value_type not in valid_types:
            errors.append(f"Invalid value type: {value_type}")

    data_sources = parameters.get('data_sources', [])
    if not data_sources:
        errors.append("At least one data source must be specified")

    return ValidationResult(len(errors) == 0, errors, warnings, parameters)

def validate_insurance_parameters(parameters: Dict[str, Any]) -> ValidationResult:
    """Validate insurance model parameters."""
    errors = []
    warnings = []

    # Validate currency
    currency = parameters.get('currency', 'USD')
    valid_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'INR']
    if currency not in valid_currencies:
        errors.append(f"Invalid currency code: {currency}")

    # Validate rates and ratios
    expense_ratio = parameters.get('expense_ratio', 0.25)
    if not 0 <= expense_ratio <= 1:
        errors.append(f"Expense ratio must be between 0 and 1, got {expense_ratio}")

    profit_loading = parameters.get('profit_loading', 0.15)
    if not 0 <= profit_loading <= 1:
        errors.append(f"Profit loading must be between 0 and 1, got {profit_loading}")

    return ValidationResult(len(errors) == 0, errors, warnings, parameters)
