# core
 ## Overview
 This directory contains core components. It includes 5 Python modules. ## Components
 ### exposure_mode
l
.py ExposureModel: asset exposure modeling with real data integration. **Classes**: `EnhancedExposureModel`, `EnhancedPropertyExposureModel`, `EnhancedPopulationExposureModel`, `EnhancedInfrastructureExposureModel` **Functions**: `create_enhanced_property_exposure_model`, `create_enhanced_population_exposure_model`, `create_enhanced_infrastructure_exposure_model` ### hazard_mode
l
.py HazardModel: hazard modeling with spatial and temporal integration. **Classes**: `EnhancedHazardModel`, `EnhancedFloodModel`, `EnhancedEarthquakeModel`, `EnhancedHurricaneModel`, `EnhancedWildfireModel` **Functions**: `create_enhanced_flood_model`, `create_enhanced_earthquake_model`, `create_enhanced_hurricane_model`, `create_enhanced_wildfire_model` ### insurance_model
s
.py Insurance Models for Risk Assessment **Classes**: `InsuranceConfig`, `InsuranceModel`, `PropertyInsuranceModel`, `LiabilityInsuranceModel`, `CatastropheInsuranceModel`, `InsuranceManager` **Functions**: `create_insurance_manager`, `calculate_property_premium` ### risk_engin
e
.py RiskEngine: orchestrator for risk modeling and analysis. **Classes**: `AnalysisJob`, `ModelIntegrationStatus`, `EnhancedRiskEngine` ### risk_model
s
.py Geospatial risk modeling components for the GEO-INFER-RISK module. **Classes**: `RiskParameters`, `RiskModel`, `HazardModel`, `VulnerabilityModel`, `ExposureModel` ## Usage
 See individual component documentation for usage examples. ## Integration
 This directory integrates with other module components and may be used by higher-level modules. 