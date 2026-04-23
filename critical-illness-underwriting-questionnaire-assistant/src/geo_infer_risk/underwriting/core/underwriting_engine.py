"""
Underwriting Engine: Core orchestrator for underwriting operations.

This module provides the main UnderwritingEngine class that coordinates all
underwriting activities including risk assessment, policy management, claims
processing, and portfolio management.
"""

import logging
import time
import json
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd

# GEO-INFER module imports with error handling
try:
    from geo_infer_risk.core.risk_engine import EnhancedRiskEngine
    RISK_ENGINE_AVAILABLE = True
except ImportError:
    RISK_ENGINE_AVAILABLE = False
    EnhancedRiskEngine = None

try:
    from geo_infer_space.core.spatial_indexing import SpatialIndexingInterface
    SPACE_AVAILABLE = True
except ImportError:
    SPACE_AVAILABLE = False
    SpatialIndexingInterface = None

# Local imports
from ..models.policy_models import Policy, Coverage
from ..models.claim_models import Claim, ClaimStatus
from ..models.underwriting_models import UnderwritingCase, Decision
from .risk_assessment import RiskAssessmentEngine
from .policy_management import PolicyManager
from .claims_processing import ClaimsProcessor
from .portfolio_management import PortfolioManager
from .underwriting_rules import UnderwritingRulesEngine
from .pricing_engine import PricingEngine
from ..utils.validation import UnderwritingValidator
from ..utils.data_integration import DataIntegrationManager

logger = logging.getLogger(__name__)

class UnderwritingStatus(Enum):
    """Underwriting case status enumeration."""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    DECLINED = "declined"
    REFERRED = "referred"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"

@dataclass
class UnderwritingConfig:
    """Configuration for underwriting operations."""
    # General settings
    processing_mode: str = "batch"  # batch, real_time, hybrid
    max_concurrent_cases: int = 10
    auto_decision_threshold: float = 0.8  # Confidence threshold for auto-decisions
    risk_tolerance: str = "moderate"  # conservative, moderate, aggressive
    compliance_framework: str = "standard"  # standard, strict, custom

    # Risk assessment settings
    risk_assessment_method: str = "comprehensive"  # basic, comprehensive, advanced
    include_climate_risk: bool = True
    include_secondary_perils: bool = True
    confidence_level: float = 0.95

    # Policy settings
    default_policy_term: int = 12  # months
    default_deductible: float = 0.02  # 2% of value
    max_policy_limit: float = 10000000  # Maximum policy limit
    min_policy_limit: float = 10000  # Minimum policy limit

    # Claims settings
    claims_processing_mode: str = "automated"  # automated, manual, hybrid
    reserve_calculation_method: str = "expected_value"  # expected_value, percentile, conservative
    payment_processing_days: int = 30

    # Integration settings
    external_data_sources: List[str] = field(default_factory=lambda: ["credit_bureau", "property_database"])
    api_endpoints: Dict[str, str] = field(default_factory=dict)
    real_time_updates: bool = False

    # Performance settings
    cache_results: bool = True
    cache_duration_hours: int = 24
    enable_parallel_processing: bool = True
    batch_size: int = 100

class UnderwritingMetrics:
    """Metrics and KPIs for underwriting operations."""

    def __init__(self):
        self.total_cases_processed = 0
        self.approved_cases = 0
        self.declined_cases = 0
        self.referred_cases = 0
        self.average_processing_time = 0.0
        self.average_premium = 0.0
        self.loss_ratio = 0.0
        self.claims_frequency = 0.0
        self.claims_severity = 0.0
        self.portfolio_concentration = 0.0

        # Track processing times
        self.processing_times = []
        self.premium_amounts = []

    def update_metrics(self, case: UnderwritingCase, processing_time: float) -> None:
        """Update metrics with a completed underwriting case."""
        self.total_cases_processed += 1
        self.processing_times.append(processing_time)

        if case.status == UnderwritingStatus.APPROVED:
            self.approved_cases += 1
            self.premium_amounts.append(case.premium)
        elif case.status == UnderwritingStatus.DECLINED:
            self.declined_cases += 1
        elif case.status == UnderwritingStatus.REFERRED:
            self.referred_cases += 1

        # Recalculate averages
        if self.processing_times:
            self.average_processing_time = np.mean(self.processing_times)

        if self.premium_amounts:
            self.average_premium = np.mean(self.premium_amounts)

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of underwriting metrics."""
        return {
            'total_cases': self.total_cases_processed,
            'approval_rate': self.approved_cases / max(1, self.total_cases_processed),
            'decline_rate': self.declined_cases / max(1, self.total_cases_processed),
            'referral_rate': self.referred_cases / max(1, self.total_cases_processed),
            'average_processing_time_hours': self.average_processing_time,
            'average_premium': self.average_premium,
            'loss_ratio': self.loss_ratio,
            'claims_frequency': self.claims_frequency,
            'claims_severity': self.claims_severity,
            'portfolio_concentration': self.portfolio_concentration,
            'last_updated': datetime.now().isoformat()
        }

class UnderwritingEngine:
    """
    Main underwriting engine that orchestrates all underwriting operations.

    The UnderwritingEngine provides:
    - Comprehensive risk assessment for underwriting decisions
    - Automated and manual policy underwriting
    - Claims processing and management
    - Portfolio management and optimization
    - Compliance and regulatory framework adherence
    - Real-time underwriting capabilities
    - Integration with external data sources
    """

    def __init__(self, config: Optional[UnderwritingConfig] = None):
        """
        Initialize the underwriting engine.

        Args:
            config: Underwriting configuration. If None, uses default configuration.
        """
        self.config = config or UnderwritingConfig()
        self.logger = self._setup_logging()

        # Initialize core components
        self.risk_assessment = RiskAssessmentEngine(self.config)
        self.policy_manager = PolicyManager(self.config)
        self.claims_processor = ClaimsProcessor(self.config)
        self.portfolio_manager = PortfolioManager(self.config)
        self.rules_engine = UnderwritingRulesEngine(self.config)
        self.pricing_engine = PricingEngine(self.config)

        # Initialize external integrations
        self.data_integration = DataIntegrationManager(self.config.external_data_sources)
        self.validator = UnderwritingValidator()

        # Initialize state management
        self.active_cases: Dict[str, UnderwritingCase] = {}
        self.case_counter = 0
        self.metrics = UnderwritingMetrics()

        # Initialize risk engine if available
        self.risk_engine = None
        if RISK_ENGINE_AVAILABLE:
            try:
                self.risk_engine = EnhancedRiskEngine()
                self.logger.info("Risk engine initialized for underwriting")
            except Exception as e:
                self.logger.warning(f"Failed to initialize risk engine: {e}")

        # Initialize threading for concurrent processing
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_cases)
        self.processing_queue = asyncio.Queue()

        self.logger.info(f"UnderwritingEngine initialized with {self.config.processing_mode} mode")

    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the underwriting engine."""
        logger = logging.getLogger("geo_infer_risk.underwriting")
        logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def underwrite_policy(self, application_data: Dict[str, Any],
                         auto_decide: bool = True) -> UnderwritingCase:
        """
        Underwrite a new insurance policy application.

        Args:
            application_data: Policy application data including property details,
                            applicant information, and coverage requirements
            auto_decide: Whether to make automatic underwriting decisions

        Returns:
            UnderwritingCase with decision and rationale
        """
        start_time = time.time()

        # Create underwriting case
        case_id = self._generate_case_id()
        case = UnderwritingCase(
            case_id=case_id,
            application_data=application_data,
            status=UnderwritingStatus.PENDING,
            created_at=datetime.now()
        )

        self.active_cases[case_id] = case

        try:
            # Step 1: Validate application
            validation_result = self.validator.validate_application(application_data)
            if not validation_result.is_valid:
                case.status = UnderwritingStatus.DECLINED
                case.decision = Decision(
                    approved=False,
                    reason="Application validation failed",
                    confidence=1.0,
                    conditions=validation_result.errors
                )
                case.completed_at = datetime.now()
                return case

            # Step 2: Perform risk assessment
            risk_assessment = self._perform_risk_assessment(application_data)
            case.risk_assessment = risk_assessment

            # Step 3: Evaluate underwriting rules
            rule_evaluation = self.rules_engine.evaluate_rules(application_data, risk_assessment)
            case.rule_evaluation = rule_evaluation

            # Step 4: Calculate premium
            premium_calculation = self.pricing_engine.calculate_premium(
                application_data, risk_assessment, rule_evaluation
            )
            case.premium = premium_calculation['total_premium']

            # Step 5: Make underwriting decision
            decision = self._make_underwriting_decision(
                application_data, risk_assessment, rule_evaluation, auto_decide
            )
            case.decision = decision

            # Step 6: Create policy if approved
            if decision.approved:
                policy = self.policy_manager.create_policy(
                    application_data, premium_calculation, decision
                )
                case.policy = policy
                case.status = UnderwritingStatus.APPROVED
            else:
                case.status = UnderwritingStatus.DECLINED

            case.completed_at = datetime.now()

            # Update metrics
            processing_time = time.time() - start_time
            self.metrics.update_metrics(case, processing_time)

            self.logger.info(f"Underwriting case {case_id} completed in {processing_time:.2f}s")
            return case

        except Exception as e:
            self.logger.error(f"Underwriting failed for case {case_id}: {e}")
            case.status = UnderwritingStatus.EXPIRED
            case.error_message = str(e)
            case.completed_at = datetime.now()
            return case

    def _generate_case_id(self) -> str:
        """Generate unique case ID."""
        self.case_counter += 1
        timestamp = int(time.time())
        return f"UW_{timestamp}_{self.case_counter}"

    def _perform_risk_assessment(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive risk assessment for underwriting."""
        try:
            # Use risk engine if available
            if self.risk_engine:
                # Convert application data to risk analysis format
                risk_data = self._convert_to_risk_format(application_data)
                risk_results = self.risk_engine.run_enhanced_analysis("comprehensive", **risk_data)
                return risk_results
            else:
                # Fallback to internal risk assessment
                return self.risk_assessment.assess_risk(application_data)

        except Exception as e:
            self.logger.error(f"Risk assessment failed: {e}")
            # Return basic risk assessment
            return {
                'risk_score': 0.5,
                'risk_level': 'medium',
                'confidence': 0.7,
                'assessment_method': 'fallback'
            }

    def _convert_to_risk_format(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert underwriting application to risk analysis format."""
        # Extract property information
        property_info = application_data.get('property', {})

        # Create risk analysis input
        risk_input = {
            'region': {
                'bounds': {
                    'min_lon': property_info.get('longitude', -74.1) - 0.1,
                    'max_lon': property_info.get('longitude', -73.9) + 0.1,
                    'min_lat': property_info.get('latitude', 40.7) - 0.1,
                    'max_lat': property_info.get('latitude', 40.9) + 0.1
                }
            },
            'hazards': ['flood', 'earthquake', 'hurricane'],  # Default hazards
            'exposure_types': ['property'],
            'analysis_parameters': {
                'confidence_level': self.config.confidence_level,
                'time_horizon': self.config.default_policy_term // 12  # Convert months to years
            }
        }

        return risk_input

    def _make_underwriting_decision(self, application_data: Dict[str, Any],
                                  risk_assessment: Dict[str, Any],
                                  rule_evaluation: Dict[str, Any],
                                  auto_decide: bool) -> Decision:
        """Make underwriting decision based on risk assessment and rules."""
        try:
            # Calculate decision confidence
            risk_score = risk_assessment.get('risk_score', 0.5)
            rule_score = rule_evaluation.get('compliance_score', 1.0)

            # Combine scores
            combined_score = (risk_score + rule_score) / 2.0

            # Determine if auto-decision is appropriate
            confidence_threshold = self.config.auto_decision_threshold

            if auto_decide and combined_score >= confidence_threshold:
                # Auto-decision
                approved = combined_score >= 0.6  # Threshold for approval
                confidence = min(1.0, combined_score + 0.1)  # Add some confidence buffer

                reason = "Auto-approved based on risk assessment" if approved else "Auto-declined based on risk assessment"

                return Decision(
                    approved=approved,
                    reason=reason,
                    confidence=confidence,
                    risk_score=risk_score,
                    rule_score=rule_score,
                    conditions=rule_evaluation.get('conditions', []),
                    requirements=rule_evaluation.get('requirements', [])
                )
            else:
                # Refer for manual review
                return Decision(
                    approved=False,  # Will be reviewed manually
                    reason="Referred for manual review",
                    confidence=0.8,
                    risk_score=risk_score,
                    rule_score=rule_score,
                    conditions=['manual_review_required'],
                    requirements=['human_underwriter_review']
                )

        except Exception as e:
            self.logger.error(f"Decision making failed: {e}")
            return Decision(
                approved=False,
                reason=f"Decision error: {str(e)}",
                confidence=0.0,
                conditions=['system_error']
            )

    def process_claim(self, claim_data: Dict[str, Any]) -> Claim:
        """
        Process an insurance claim.

        Args:
            claim_data: Claim information including policy details, damage description, etc.

        Returns:
            Processed claim with status and settlement information
        """
        try:
            # Validate claim
            validation_result = self.validator.validate_claim(claim_data)
            if not validation_result.is_valid:
                return Claim(
                    claim_id="INVALID",
                    policy_id=claim_data.get('policy_id', 'UNKNOWN'),
                    status=ClaimStatus.INVALID,
                    description="Claim validation failed",
                    errors=validation_result.errors
                )

            # Process claim through claims engine
            claim = self.claims_processor.process_claim(claim_data)

            # Update portfolio metrics
            self.portfolio_manager.update_portfolio_metrics(claim)

            self.logger.info(f"Claim {claim.claim_id} processed with status {claim.status}")
            return claim

        except Exception as e:
            self.logger.error(f"Claim processing failed: {e}")
            return Claim(
                claim_id="ERROR",
                policy_id=claim_data.get('policy_id', 'UNKNOWN'),
                status=ClaimStatus.ERROR,
                description=f"Processing error: {str(e)}"
            )

    def get_portfolio_summary(self, portfolio_id: str = None) -> Dict[str, Any]:
        """
        Get portfolio summary and performance metrics.

        Args:
            portfolio_id: Specific portfolio ID. If None, returns aggregate summary.

        Returns:
            Portfolio summary with key metrics and statistics
        """
        return self.portfolio_manager.get_portfolio_summary(portfolio_id)

    def get_underwriting_metrics(self) -> Dict[str, Any]:
        """Get comprehensive underwriting performance metrics."""
        return self.metrics.get_metrics_summary()

    def get_case_status(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific underwriting case."""
        if case_id not in self.active_cases:
            return None

        case = self.active_cases[case_id]
        return {
            'case_id': case.case_id,
            'status': case.status.value,
            'created_at': case.created_at.isoformat(),
            'completed_at': case.completed_at.isoformat() if case.completed_at else None,
            'premium': case.premium,
            'risk_score': case.risk_assessment.get('risk_score') if case.risk_assessment else None,
            'decision_confidence': case.decision.confidence if case.decision else None,
            'error_message': case.error_message
        }

    def cancel_case(self, case_id: str) -> bool:
        """Cancel a pending underwriting case."""
        if case_id not in self.active_cases:
            return False

        case = self.active_cases[case_id]
        if case.status == UnderwritingStatus.PENDING:
            case.status = UnderwritingStatus.WITHDRAWN
            case.completed_at = datetime.now()
            return True

        return False

    def get_active_cases(self) -> List[Dict[str, Any]]:
        """Get list of all active underwriting cases."""
        return [
            {
                'case_id': case.case_id,
                'status': case.status.value,
                'created_at': case.created_at.isoformat(),
                'premium': case.premium
            }
            for case in self.active_cases.values()
            if case.status in [UnderwritingStatus.PENDING, UnderwritingStatus.IN_REVIEW]
        ]

    def update_configuration(self, config_updates: Dict[str, Any]) -> None:
        """Update underwriting configuration."""
        # Update config attributes
        for key, value in config_updates.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        # Reinitialize components that depend on configuration
        self.rules_engine = UnderwritingRulesEngine(self.config)
        self.pricing_engine = PricingEngine(self.config)

        self.logger.info("Underwriting configuration updated")

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on underwriting system."""
        health_status = {
            'overall_status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }

        # Check core components
        components_to_check = [
            ('risk_assessment', self.risk_assessment),
            ('policy_manager', self.policy_manager),
            ('claims_processor', self.claims_processor),
            ('portfolio_manager', self.portfolio_manager),
            ('rules_engine', self.rules_engine),
            ('pricing_engine', self.pricing_engine),
            ('data_integration', self.data_integration),
            ('validator', self.validator)
        ]

        all_healthy = True
        for component_name, component in components_to_check:
            try:
                if hasattr(component, 'health_check'):
                    component_health = component.health_check()
                else:
                    component_health = {'status': 'operational'}

                health_status['components'][component_name] = component_health

                if component_health.get('status') != 'operational':
                    all_healthy = False

            except Exception as e:
                health_status['components'][component_name] = {
                    'status': 'error',
                    'error': str(e)
                }
                all_healthy = False

        # Check external integrations
        integrations_status = {
            'risk_engine': RISK_ENGINE_AVAILABLE,
            'spatial_indexing': SPACE_AVAILABLE
        }

        health_status['integrations'] = integrations_status

        # Determine overall status
        if not all_healthy:
            health_status['overall_status'] = 'degraded'
        elif not all(integrations_status.values()):
            health_status['overall_status'] = 'degraded'

        return health_status

    def shutdown(self) -> None:
        """Shutdown the underwriting engine and cleanup resources."""
        self.logger.info("Shutting down underwriting engine")

        # Shutdown thread pool
        self.executor.shutdown(wait=True)

        # Close any open connections
        if hasattr(self.data_integration, 'close_connections'):
            self.data_integration.close_connections()

        self.logger.info("Underwriting engine shutdown complete")


# Convenience functions
def create_underwriting_engine(config: Optional[UnderwritingConfig] = None) -> UnderwritingEngine:
    """Create a new underwriting engine instance."""
    return UnderwritingEngine(config)

def create_risk_assessment(config: Optional[UnderwritingConfig] = None) -> RiskAssessmentEngine:
    """Create a risk assessment engine."""
    return RiskAssessmentEngine(config or UnderwritingConfig())

def create_policy_manager(config: Optional[UnderwritingConfig] = None) -> PolicyManager:
    """Create a policy manager."""
    from .policy_management import PolicyManager
    return PolicyManager(config or UnderwritingConfig())

def create_claims_processor(config: Optional[UnderwritingConfig] = None) -> ClaimsProcessor:
    """Create a claims processor."""
    from .claims_processing import ClaimsProcessor
    return ClaimsProcessor(config or UnderwritingConfig())
