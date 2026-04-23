# Agent
: core

## Scope
 This directory contains core components for the module. It provides 23 classes and 9 functions.

## Classes
 and Functions

### EnhancedExposureModel
 exposure model with data integration and spatial analysis.

**Methods**:
- `get_exposure_at_location(latitude: float, longitude: float, radius: float, time_scenario: str) -> Dict[str, Any]`: Get exposure within a radius of a specific location with temporal variation.
- `get_exposure_for_event(event: Dict[str, Any]) -> List[Dict[str, Any]]`: Get the exposure affected by a hazard event with features.
- `calculate_total_exposure(bounds: Optional[Dict[str, float]], time_scenario: str) -> Dict[str, Any]`: Calculate the total exposure within optional geographic bounds with temporal variation.
- `set_time_scenario(scenario: str) -> None`: Set the current time scenario for exposure analysis.
- `update_exposure_data(new_data: pd.DataFrame, merge_strategy: str) -> None`: Update exposure data with information.
- `save_exposure_data(output_file: str) -> None`: Save exposure data to a CSV file.
- `load_exposure_data(input_file: str) -> None`: Load exposure data from a CSV file.
- `get_model_status() -> Dict[str, Any]`: Get model status information.

### EnhancedPropertyExposureModel
 property exposure model with building characteristics.

**Methods**:
- `get_exposure_for_event(event: Dict[str, Any]) -> List[Dict[str, Any]]`: Get property exposure affected by a hazard event.

### EnhancedPopulationExposureModel
 population exposure model with demographic analysis.

**Methods**:
- `get_exposure_for_event(event: Dict[str, Any]) -> List[Dict[str, Any]]`: Get population exposure affected by a hazard event.

### EnhancedInfrastructureExposureModel
 infrastructure exposure model with network considerations.

**Methods**:
- `get_exposure_for_event(event: Dict[str, Any]) -> List[Dict[str, Any]]`: Get infrastructure exposure affected by a hazard event.

### EnhancedHazardModel
 hazard model with spatial, temporal, and statistical capabilities.

**Methods**:
- `generate_events(num_events: int, region: Optional[Dict], time_period: Optional[Tuple[datetime, datetime]]) -> List[Dict[str, Any]]`: Generate stochastic hazard events with features.
- `get_intensity_at_location(event: Dict[str, Any], latitude: float, longitude: float) -> float`: Calculate hazard intensity at a specific location for a given event.
- `get_return_period_map(return_period: float, region: Optional[Dict]) -> Dict[str, Any]`: Generate hazard map for a specific return period.
- `get_model_status() -> Dict[str, Any]`: Get model status information.
- `save_model(filepath: str) -> None`: Save trained model to file.
- `load_model(filepath: str) -> None`: Load trained model from file.

### EnhancedFloodModel
 flood hazard model with hydrological modeling.

### EnhancedEarthquakeModel
 earthquake hazard model with tectonic considerations.

### EnhancedHurricaneModel
 hurricane model with storm track and intensity modeling.

### EnhancedWildfireModel
 wildfire model with fuel and weather considerations.

### InsuranceConfig
 Configuration for insurance models.

### InsuranceModel
 Abstract base class for insurance models.

**Methods**:
- `fit(historical_data: pd.DataFrame) -> 'InsuranceModel'`: Fit the model to historical data.
- `calculate_premium(risk_profile: Dict[str, Any]) -> float`: Calculate insurance premium.
- `estimate_losses(risk_profile: Dict[str, Any]) -> Dict[str, float]`: Estimate potential losses.

### PropertyInsuranceModel
 Property insurance model.

**Methods**:
- `fit(historical_data: pd.DataFrame) -> 'PropertyInsuranceModel'`: Fit property insurance model to historical data.
- `calculate_premium(risk_profile: Dict[str, Any]) -> float`: Calculate property insurance premium.
- `estimate_losses(risk_profile: Dict[str, Any]) -> Dict[str, float]`: Estimate potential property losses.

### LiabilityInsuranceModel
 Liability insurance model.

**Methods**:
- `fit(historical_data: pd.DataFrame) -> 'LiabilityInsuranceModel'`: Fit liability insurance model to historical data.
- `calculate_premium(risk_profile: Dict[str, Any]) -> float`: Calculate liability insurance premium.
- `estimate_losses(risk_profile: Dict[str, Any]) -> Dict[str, float]`: Estimate potential liability losses.

### CatastropheInsuranceModel
 Catastrophe insurance model.

**Methods**:
- `fit(historical_data: pd.DataFrame) -> 'CatastropheInsuranceModel'`: Fit catastrophe insurance model to historical data.
- `calculate_premium(risk_profile: Dict[str, Any]) -> float`: Calculate catastrophe insurance premium.
- `estimate_losses(risk_profile: Dict[str, Any]) -> Dict[str, float]`: Estimate potential catastrophe losses.

### InsuranceManager
 Manager for multiple insurance models.

**Methods**:
- `fit_model(model_type: str, historical_data: pd.DataFrame) -> bool`: Fit a specific insurance model.
- `calculate_premium(model_type: str, risk_profile: Dict[str, Any]) -> float`: Calculate insurance premium.
- `estimate_losses(model_type: str, risk_profile: Dict[str, Any]) -> Dict[str, float]`: Estimate potential losses.
- `generate_quote(risk_profile: Dict[str, Any], coverage_types: List[str]) -> Dict[str, Any]`: Generate insurance quote.

### AnalysisJob
 Represents an analysis job with metadata and status.

### ModelIntegrationStatus
 Status of integration with external GEO-INFER modules.

### EnhancedRiskEngine
 risk analysis engine with capabilities and module integration.

**Methods**:
- `get_integration_status() -> Dict[str, bool]`: Get status of all module integrations.
- `run_enhanced_analysis(analysis_type: str, **kwargs) -> Dict[str, Any]`: Run risk analysis with capabilities.
- `get_job_status(job_id: str) -> Optional[Dict[str, Any]]`: Get status of an analysis job.
- `cancel_job(job_id: str) -> bool`: Cancel a running analysis job.
- `get_model_status() -> Dict[str, Any]`: Get status of all loaded models.
- `calibrate_models(calibration_data: Dict[str, Any], method: str) -> Dict[str, Any]`: Calibrate model parameters using historical data.
- `run_monte_carlo_analysis(num_iterations: int, convergence_threshold: float) -> Dict[str, Any]`: Run Monte Carlo analysis with convergence monitoring.
- `save_enhanced_results(results: Dict[str, Any], filename: Optional[str]) -> str`: Save analysis results with metadata.
- `load_models()`: Load and initialize all models based on the configuration (legacy method).
- `run_analysis()`: Execute the risk analysis workflow (legacy method).

### RiskParameters
 Parameters for defining risk model behavior.

### RiskModel
 Base class for all geospatial risk models.

**Methods**:
- `set_hazard(hazard_model: 'HazardModel') -> None`: Set the hazard component of the risk model.
- `set_vulnerability(vulnerability_model: 'VulnerabilityModel') -> None`: Set the vulnerability component of the risk model.
- `set_exposure(exposure_model: 'ExposureModel') -> None`: Set the exposure component of the risk model.
- `calculate_risk(geometry: Union[gpd.GeoDataFrame, gpd.GeoSeries]) -> gpd.GeoDataFrame`: Calculate risk for the given geographic area.
- `run_monte_carlo(geometry: gpd.GeoDataFrame) -> Dict`: Run Monte Carlo simulations for risk assessment.

### HazardModel
 Base class for modeling hazard probability in geographic areas.

**Methods**:
- `calculate(geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame`: Calculate hazard probability for given areas.
- `sample() -> np.ndarray`: Generate a random sample from the hazard model for Monte Carlo simulation.

### VulnerabilityModel
 Base class for modeling vulnerability of assets or populations.

**Methods**:
- `calculate(geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame`: Calculate vulnerability indices for given areas.
- `sample() -> np.ndarray`: Generate a random sample from the vulnerability model for Monte Carlo simulation.

### ExposureModel
 Base class for modeling exposure (assets, population, etc.).

**Methods**:
- `calculate(geometry: gpd.GeoDataFrame) -> gpd.GeoDataFrame`: Calculate exposure values for given areas.
- `sample() -> np.ndarray`: Generate a random sample from the exposure model for Monte Carlo simulation.

### create_enhanced_property_exposure_model
 `create_enhanced_property_exposure_model(params: Dict[str, Any]) -> EnhancedPropertyExposureModel` Create an property exposure model.

### create_enhanced_population_exposure_model
 `create_enhanced_population_exposure_model(params: Dict[str, Any]) -> EnhancedPopulationExposureModel` Create an population exposure model.

### create_enhanced_infrastructure_exposure_model
 `create_enhanced_infrastructure_exposure_model(params: Dict[str, Any]) -> EnhancedInfrastructureExposureModel` Create an infrastructure exposure model.

### create_enhanced_flood_model
 `create_enhanced_flood_model(params: Dict[str, Any]) -> EnhancedFloodModel` Create an flood hazard model.

### create_enhanced_earthquake_model
 `create_enhanced_earthquake_model(params: Dict[str, Any]) -> EnhancedEarthquakeModel` Create an earthquake hazard model.

### create_enhanced_hurricane_model
 `create_enhanced_hurricane_model(params: Dict[str, Any]) -> EnhancedHurricaneModel` Create an hurricane hazard model.

### create_enhanced_wildfire_model
 `create_enhanced_wildfire_model(params: Dict[str, Any]) -> EnhancedWildfireModel` Create an wildfire hazard model.

### create_insurance_manager
 `create_insurance_manager(config: Optional[InsuranceConfig]) -> InsuranceManager` Create a insurance manager.

### calculate_property_premium
 `calculate_property_premium(property_value: float, property_type: str, location: str) -> float` Calculate property insurance premium.

## Capabilities

- **23 classes** for core functionality
- **9 functions** for utility operations

## Integration

- **Location**: `GEO-INFER-RISK/src/geo_infer_risk/core`
- **Type**: Directory Node
