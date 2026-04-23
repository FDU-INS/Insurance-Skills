"""
GEO-INFER-RISK: Geospatial Risk Analysis and Catastrophe Modeling Framework

A framework for modeling, analyzing, and visualizing geospatial risk
across multiple hazards, vulnerabilities, and exposure types.
"""

__version__ = "0.1.0"
__author__ = "GEO-INFER Team"
__license__ = "MIT"

# Import core components for easier access
try:
    from geo_infer_risk.core import (
        RiskEngine,
        RiskModel,
        HazardModel,
        VulnerabilityModel,
        ExposureModel,
    )
except ImportError:
    RiskEngine = None
    RiskModel = None
    HazardModel = None
    VulnerabilityModel = None
    ExposureModel = None

# Import specialized risk models (optional)
try:
    from geo_infer_risk.models import (
        FloodModel,
        EarthquakeModel,
        HurricaneModel,
        WildfireModel,
        DroughtModel,
        MultiHazardModel,
    )
except ImportError:
    FloodModel = None
    EarthquakeModel = None
    HurricaneModel = None
    WildfireModel = None
    DroughtModel = None
    MultiHazardModel = None

# Import utility functions (optional)
try:
    from geo_infer_risk.utils import (
        config_loader,
        risk_metrics,
        spatial_utils,
        validation,
    )
except ImportError:
    config_loader = None
    risk_metrics = None
    spatial_utils = None
    validation = None

# Import API components (optional)
try:
    from geo_infer_risk.api import (
        RiskAPI,
        ModelRegistry,
        ResultsFormatter,
    )
except ImportError:
    RiskAPI = None
    ModelRegistry = None
    ResultsFormatter = None

# Import underwriting module (optional)
try:
    from geo_infer_risk.underwriting import (
        UnderwritingEngine,
        UnderwritingConfig,
        RiskAssessmentEngine,
        PolicyManager,
        ClaimsProcessor,
        PortfolioManager,
        UnderwritingRulesEngine,
        PricingEngine,
        UnderwritingDecisionEngine,
        Policy,
        Claim,
        UnderwritingCase,
        Decision,
        create_underwriting_engine,
        underwrite_policy,
        process_claim,
        assess_risk,
        calculate_premium,
    )
    UNDERWRITING_AVAILABLE = True
except ImportError:
    UNDERWRITING_AVAILABLE = False

# Import enhanced core components (optional)
try:
    from geo_infer_risk.core import (
        EnhancedRiskEngine,
        EnhancedHazardModel,
        EnhancedVulnerabilityModel,
        EnhancedCatastropheModel,
        CatastropheConfig,
    )
    ENHANCED_CORE_AVAILABLE = True
except ImportError:
    ENHANCED_CORE_AVAILABLE = False

# Define module level constants
DEFAULT_CONFIDENCE_LEVEL = 0.95
DEFAULT_RETURN_PERIODS = [10, 25, 50, 100, 250, 500, 1000]


def create_risk_analysis(config_path=None, **kwargs):
    """
    Create a new risk analysis engine with the specified configuration.

    Args:
        config_path: Path to configuration file. If not provided,
                     default configuration will be used.
        **kwargs: Additional configuration parameters that override file settings.

    Returns:
        RiskEngine: Configured risk analysis engine instance.
    """
    from geo_infer_risk.utils.config_loader import load_config

    if config_path:
        config = load_config(config_path)
    else:
        config = {}

    for key, value in kwargs.items():
        config[key] = value

    return RiskEngine(config)


def create_underwriting_system(config=None):
    """
    Create an underwriting system.

    Args:
        config: Underwriting configuration. If None, uses defaults.

    Returns:
        UnderwritingEngine: Configured underwriting engine.
    """
    if not UNDERWRITING_AVAILABLE:
        raise ImportError("Underwriting module not available")

    return create_underwriting_engine(config)


def underwrite_insurance_policy(application_data, config=None):
    """
    Underwrite an insurance policy application.

    Args:
        application_data: Policy application data
        config: Underwriting configuration

    Returns:
        UnderwritingCase: Completed underwriting case
    """
    if not UNDERWRITING_AVAILABLE:
        raise ImportError("Underwriting module not available")

    return underwrite_policy(application_data, config)


def process_insurance_claim(claim_data, config=None):
    """
    Process an insurance claim.

    Args:
        claim_data: Claim information
        config: Claims processing configuration

    Returns:
        Claim: Processed claim
    """
    if not UNDERWRITING_AVAILABLE:
        raise ImportError("Underwriting module not available")

    return process_claim(claim_data, config)
