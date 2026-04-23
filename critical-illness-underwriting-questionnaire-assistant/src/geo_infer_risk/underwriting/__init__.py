"""
GEO-INFER-RISK Underwriting Module

Comprehensive underwriting system for risk assessment, policy management,
and insurance operations within the GEO-INFER framework.

This module provides enterprise-grade underwriting capabilities including:
- Risk assessment and pricing algorithms
- Policy management and lifecycle operations
- Claims processing and settlement
- Portfolio management and optimization
- Underwriting guidelines and compliance
- Real-time underwriting decisions
- Integration with external data sources and APIs
"""

__version__ = "1.0.0"
__author__ = "GEO-INFER-RISK Team"

# Import main underwriting components
from .core.underwriting_engine import UnderwritingEngine, UnderwritingConfig, UnderwritingMetrics
from .core.risk_assessment import RiskAssessmentEngine, RiskAssessmentConfig, RiskMetrics
from .core.policy_management import PolicyManager, PolicyLifecycle, Policy, Coverage, Endorsement, Exclusion
from .core.claims_processing import ClaimsProcessor, ClaimsEngine, Claim, ClaimStatus, Payment, Reserve
from .core.portfolio_management import PortfolioManager, PortfolioOptimizer
from .core.underwriting_rules import UnderwritingRulesEngine, RuleEvaluator, UnderwritingRule, RuleCondition, RuleType
from .core.pricing_engine import PricingEngine, PremiumCalculator, PremiumCalculation, PricingMethod
from .core.underwriting_decisions import UnderwritingDecisionEngine, DecisionFramework, DecisionCriteria

# Import utility modules
from .utils.validation import UnderwritingValidator, PolicyValidator
from .utils.data_integration import DataIntegrationManager, ExternalDataSource
from .utils.compliance import ComplianceEngine, RegulatoryFramework, ComplianceStatus
from .utils.reporting import UnderwritingReporter, ReportingEngine

# Import models and data structures
from .models.policy_models import Policy as PolicyModel, Coverage as CoverageModel, Endorsement as EndorsementModel, Exclusion as ExclusionModel
from .models.claim_models import Claim as ClaimModel, ClaimStatus as ClaimStatusModel, Payment as PaymentModel, Reserve as ReserveModel
from .models.risk_models import RiskProfile as RiskProfileModel, ExposureProfile as ExposureProfileModel, VulnerabilityProfile as VulnerabilityProfileModel
from .models.underwriting_models import UnderwritingCase as UnderwritingCaseModel, Decision as DecisionModel, Guideline as GuidelineModel

# Import enums and types
from .core.underwriting_engine import UnderwritingStatus
from .models.policy_models import CoverageType
from .models.claim_models import ClaimType, PaymentType
from .models.risk_models import RiskLevel, RiskCategory
from .core.underwriting_decisions import DecisionType, DecisionCriteria
from .core.underwriting_rules import RuleType
from .utils.compliance import ComplianceFramework, ComplianceStatus
from .core.pricing_engine import PricingMethod

# Convenience functions
def underwrite_policy(application_data: Dict[str, Any],
                     config: Optional[UnderwritingConfig] = None) -> UnderwritingCase:
    """Convenience function to underwrite a policy."""
    engine = create_underwriting_engine(config)
    return engine.underwrite_policy(application_data)

def process_claim(claim_data: Dict[str, Any],
                 config: Optional[Dict[str, Any]] = None) -> Claim:
    """Convenience function to process a claim."""
    processor = create_claims_processor(config)
    return processor.process_claim(claim_data)

def assess_risk(entity_data: Dict[str, Any],
               assessment_type: str = "comprehensive") -> Dict[str, Any]:
    """Convenience function to assess risk."""
    engine = create_risk_assessment()
    return engine.assess_risk(entity_data, assessment_type)

def calculate_premium(policy_data: Dict[str, Any],
                     risk_assessment: Dict[str, Any],
                     rule_evaluation: Dict[str, Any]) -> PremiumCalculation:
    """Convenience function to calculate premium."""
    engine = create_pricing_engine()
    return engine.calculate_premium(policy_data, risk_assessment, rule_evaluation)

def create_underwriting_engine(config: Optional[UnderwritingConfig] = None) -> UnderwritingEngine:
    """Create a new underwriting engine."""
    from .core.underwriting_engine import UnderwritingEngine
    return UnderwritingEngine(config)

def create_risk_assessment(config: Optional[RiskAssessmentConfig] = None) -> RiskAssessmentEngine:
    """Create a risk assessment engine."""
    from .core.risk_assessment import RiskAssessmentEngine
    return RiskAssessmentEngine(config)

def create_policy_manager(config: Optional[Dict[str, Any]] = None) -> PolicyManager:
    """Create a policy manager."""
    from .core.policy_management import PolicyManager
    return PolicyManager(config)

def create_claims_processor(config: Optional[Dict[str, Any]] = None) -> ClaimsProcessor:
    """Create a claims processor."""
    from .core.claims_processing import ClaimsProcessor
    return ClaimsProcessor(config)

# Package exports
__all__ = [
    # Core Engines and Config
    "UnderwritingEngine",
    "UnderwritingConfig",
    "UnderwritingMetrics",
    "RiskAssessmentEngine",
    "RiskAssessmentConfig",
    "RiskMetrics",
    "PolicyManager",
    "PolicyLifecycle",
    "ClaimsProcessor",
    "ClaimsEngine",
    "PortfolioManager",
    "PortfolioOptimizer",
    "UnderwritingRulesEngine",
    "RuleEvaluator",
    "PricingEngine",
    "PremiumCalculator",
    "UnderwritingDecisionEngine",

    # Models
    "Policy",
    "Coverage",
    "Endorsement",
    "Exclusion",
    "Claim",
    "ClaimStatus",
    "Payment",
    "Reserve",
    "RiskProfile",
    "ExposureProfile",
    "VulnerabilityProfile",
    "UnderwritingCase",
    "Decision",
    "Guideline",

    # Utilities
    "UnderwritingValidator",
    "PolicyValidator",
    "DataIntegrationManager",
    "ExternalDataSource",
    "ComplianceEngine",
    "RegulatoryFramework",
    "UnderwritingReporter",
    "ReportingEngine",

    # Enums and Types
    "UnderwritingStatus",
    "CoverageType",
    "ClaimType",
    "PaymentType",
    "RiskLevel",
    "RiskCategory",
    "DecisionType",
    "DecisionCriteria",
    "RuleType",
    "ComplianceFramework",
    "ComplianceStatus",
    "PricingMethod",

    # Convenience functions
    "create_underwriting_engine",
    "create_risk_assessment",
    "create_policy_manager",
    "create_claims_processor",
    "underwrite_policy",
    "process_claim",
    "assess_risk",
    "calculate_premium"
]
