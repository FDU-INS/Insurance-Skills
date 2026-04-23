"""
Core functionality for the GEO-INFER-RISK module.

This submodule contains the essential components for risk modeling, catastrophe 
assessment, and insurance analytics with geospatial dimensions.
"""

# Import core components with explicit imports
from .risk_models import (
    RiskParameters,
    RiskModel,
    HazardModel,
    VulnerabilityModel,
    ExposureModel,
)

from .catastrophe_models import (
    CatastropheConfig,
    EnhancedCatastropheModel,
    EnhancedEarthquakeModel,
    EnhancedHurricaneModel,
    EnhancedFloodModel,
    create_enhanced_earthquake_model,
    create_enhanced_hurricane_model,
    create_enhanced_flood_model,
    CatastropheModel,  # Base class (alias for EnhancedCatastropheModel)
)

from .insurance_models import (
    InsuranceConfig,
    InsuranceModel,
    PropertyInsuranceModel,
    LiabilityInsuranceModel,
    CatastropheInsuranceModel,
    InsuranceManager,
    create_insurance_manager,
    calculate_property_premium,
)

from .risk_engine import EnhancedRiskEngine, RiskEngine, AnalysisJob, ModelIntegrationStatus
from .hazard_model import (
    EnhancedHazardModel, HazardModel,
    EnhancedFloodModel, EnhancedEarthquakeModel,
    EnhancedHurricaneModel, EnhancedWildfireModel,
    create_enhanced_flood_model, create_enhanced_earthquake_model,
    create_enhanced_hurricane_model, create_enhanced_wildfire_model
)
from .catastrophe_models import (
    EnhancedCatastropheModel, CatastropheModel,
    CatastropheConfig,
    EnhancedEarthquakeModel as EnhancedEarthquakeCatModel,
    EnhancedHurricaneModel as EnhancedHurricaneCatModel,
    EnhancedFloodModel as EnhancedFloodCatModel,
    create_enhanced_earthquake_model as create_enhanced_earthquake_cat_model,
    create_enhanced_hurricane_model as create_enhanced_hurricane_cat_model,
    create_enhanced_flood_model as create_enhanced_flood_cat_model
)
from .vulnerability_model import (
    EnhancedVulnerabilityModel, VulnerabilityModel,
    EnhancedBuildingVulnerabilityModel, EnhancedInfrastructureVulnerabilityModel,
    EnhancedPopulationVulnerabilityModel,
    create_enhanced_building_vulnerability_model,
    create_enhanced_infrastructure_vulnerability_model,
    create_enhanced_population_vulnerability_model
)

# Package exports
__all__ = [
    # Enhanced Risk Engine (primary)
    "EnhancedRiskEngine",
    "RiskEngine",  # Backward compatibility alias

    # Enhanced Hazard Models
    "EnhancedHazardModel",
    "HazardModel",  # Backward compatibility alias
    "EnhancedFloodModel",
    "EnhancedEarthquakeModel",
    "EnhancedHurricaneModel",
    "EnhancedWildfireModel",

    # Hazard model factory functions
    "create_enhanced_flood_model",
    "create_enhanced_earthquake_model",
    "create_enhanced_hurricane_model",
    "create_enhanced_wildfire_model",

    # Enhanced Vulnerability Models
    "EnhancedVulnerabilityModel",
    "VulnerabilityModel",  # Backward compatibility alias
    "EnhancedBuildingVulnerabilityModel",
    "EnhancedInfrastructureVulnerabilityModel",
    "EnhancedPopulationVulnerabilityModel",

    # Vulnerability model factory functions
    "create_enhanced_building_vulnerability_model",
    "create_enhanced_infrastructure_vulnerability_model",
    "create_enhanced_population_vulnerability_model",

    # Risk modeling components
    "RiskModel",
    "ExposureModel",

    # Enhanced Catastrophe modeling
    "EnhancedCatastropheModel",
    "CatastropheModel",  # Backward compatibility alias
    "CatastropheConfig",
    "EnhancedEarthquakeCatModel",
    "EnhancedHurricaneCatModel",
    "EnhancedFloodCatModel",
    "create_enhanced_earthquake_cat_model",
    "create_enhanced_hurricane_cat_model",
    "create_enhanced_flood_cat_model",

    # Insurance modeling
    "InsuranceConfig",
    "InsuranceModel",
    "PropertyInsuranceModel",
    "LiabilityInsuranceModel",
    "CatastropheInsuranceModel",
    "InsuranceManager",
    "create_insurance_manager",
    "calculate_property_premium",

    # Analysis job management
    "AnalysisJob",
    "ModelIntegrationStatus"
] 