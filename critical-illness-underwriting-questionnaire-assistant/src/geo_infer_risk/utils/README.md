# utils
 ## Overview
 This directory contains utils components. It includes 3 Python modules. ## Components
 ### config_loade
r
.py Configuration loading and management utilities for GEO-INFER-RISK. **Classes**: `ConfigurationLoader` **Functions**: `load_config`, `load_config_with_defaults`, `create_example_config`, `get_default_config`, `save_config` ### risk_metric
s
.py Risk Metrics: Functions for calculating key risk metrics from event loss data. **Functions**: `calculate_aal`, `calculate_ep_curve`, `calculate_pml`, `calculate_loss_by_return_period`, `calculate_tail_value_at_risk`, `calculate_annual_occurrence_exceedance_probability`, `calculate_annual_aggregate_exceedance_probability`, `calculate_loss_frequency_curve`, `calculate_correlation_matrix` ### validatio
n
.py Configuration validation and data validation utilities for GEO-INFER-RISK. **Classes**: `ValidationResult`, `ConfigurationValidator` **Functions**: `validate_config`, `validate_data_file`, `validate_csv_file`, `validate_json_file`, `validate_shapefile`, `validate_model_parameters`, `validate_hazard_parameters`, `validate_vulnerability_parameters`, `validate_exposure_parameters`, `validate_insurance_parameters` ## Usage
 See individual component documentation for usage examples. ## Integration
 This directory integrates with other module components and may be used by higher-level modules. 