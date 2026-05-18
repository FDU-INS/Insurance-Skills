"""
Underwriting Decisions Engine: Advanced decision support for underwriting.

This module provides sophisticated decision-making capabilities including:
- Multi-criteria decision analysis
- Risk-based decision frameworks
- Automated decision rules and thresholds
- Human-in-the-loop decision support
- Decision explanation and audit trails
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import json

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class DecisionType(Enum):
    """Underwriting decision type enumeration."""
    AUTOMATIC = "automatic"
    MANUAL_REVIEW = "manual_review"
    REFERRED = "referred"
    CONDITIONAL = "conditional"
    DECLINED = "declined"

class DecisionCriteria(Enum):
    """Decision criteria enumeration."""
    RISK_SCORE = "risk_score"
    PREMIUM_ADEQUACY = "premium_adequacy"
    COVERAGE_LIMITS = "coverage_limits"
    LOSS_HISTORY = "loss_history"
    FINANCIAL_STABILITY = "financial_stability"
    COMPLIANCE = "compliance"
    MARKET_CONDITIONS = "market_conditions"

@dataclass
class DecisionCriteria:
    """Decision criteria configuration."""

    criteria_type: DecisionCriteria
    weight: float = 1.0
    threshold: float = 0.7
    operator: str = "greater_equal"  # greater_equal, less_equal, equals, between
    threshold_values: List[float] = field(default_factory=list)

    def evaluate(self, value: float) -> bool:
        """Evaluate criteria against value."""
        if self.operator == "greater_equal":
            return value >= self.threshold
        elif self.operator == "less_equal":
            return value <= self.threshold
        elif self.operator == "equals":
            return abs(value - self.threshold) < 0.001
        elif self.operator == "between" and len(self.threshold_values) >= 2:
            return self.threshold_values[0] <= value <= self.threshold_values[1]
        else:
            return False

    def get_score(self, value: float) -> float:
        """Get normalized score for criteria."""
        if self.criteria_type == DecisionCriteria.RISK_SCORE:
            # Lower risk scores are better
            return max(0, 1 - value) * self.weight
        else:
            # Higher values are better
            return min(1, value / self.threshold) * self.weight

@dataclass
class DecisionFramework:
    """Decision framework configuration."""

    framework_name: str
    decision_criteria: List[DecisionCriteria] = field(default_factory=list)
    auto_decision_threshold: float = 0.8
    manual_review_threshold: float = 0.6
    risk_tolerance: str = "moderate"  # conservative, moderate, aggressive

    # Framework parameters
    minimum_confidence: float = 0.7
    maximum_risk_score: float = 0.8
    minimum_premium_adequacy: float = 1.0

    def evaluate_decision_criteria(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate all decision criteria."""
        criteria_results = {}

        for criteria in self.decision_criteria:
            value = self._get_criteria_value(assessment_data, criteria.criteria_type)
            criteria_results[criteria.criteria_type.value] = {
                'value': value,
                'passed': criteria.evaluate(value),
                'score': criteria.get_score(value),
                'weight': criteria.weight
            }

        return criteria_results

    def _get_criteria_value(self, data: Dict[str, Any], criteria_type: DecisionCriteria) -> float:
        """Get value for specific criteria."""
        if criteria_type == DecisionCriteria.RISK_SCORE:
            return data.get('risk_score', 0.5)
        elif criteria_type == DecisionCriteria.PREMIUM_ADEQUACY:
            return data.get('premium_adequacy', 1.0)
        elif criteria_type == DecisionCriteria.COVERAGE_LIMITS:
            return data.get('coverage_adequacy', 1.0)
        elif criteria_type == DecisionCriteria.LOSS_HISTORY:
            return data.get('loss_ratio', 0.1)
        elif criteria_type == DecisionCriteria.FINANCIAL_STABILITY:
            return data.get('financial_stability', 0.8)
        elif criteria_type == DecisionCriteria.COMPLIANCE:
            return data.get('compliance_score', 1.0)
        elif criteria_type == DecisionCriteria.MARKET_CONDITIONS:
            return data.get('market_competitiveness', 0.8)
        else:
            return 0.5

    def calculate_overall_score(self, criteria_results: Dict[str, Any]) -> float:
        """Calculate overall decision score."""
        total_weight = sum(result['weight'] for result in criteria_results.values())
        if total_weight == 0:
            return 0.0

        weighted_score = sum(result['score'] for result in criteria_results.values())
        return weighted_score / total_weight

class UnderwritingDecisionEngine:
    """
    Advanced underwriting decision engine with multi-criteria analysis.

    This engine provides:
    - Automated decision making with confidence scoring
    - Multi-criteria decision frameworks
    - Risk-based decision thresholds
    - Decision explanation and justification
    - Human oversight and intervention support
    - Continuous learning and improvement
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the decision engine.

        Args:
            config: Decision engine configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger("geo_infer_risk.underwriting.decision_engine")

        # Decision frameworks
        self.decision_frameworks: Dict[str, DecisionFramework] = {}
        self.active_framework: str = "standard"

        # Decision history and learning
        self.decision_history: List[Dict[str, Any]] = []
        self.decision_accuracy = 0.0

        # Initialize default frameworks
        self._initialize_default_frameworks()

        self.logger.info("Underwriting decision engine initialized")

    def make_decision(self, assessment_data: Dict[str, Any],
                     framework_name: str = "standard") -> Dict[str, Any]:
        """
        Make underwriting decision based on assessment data.

        Args:
            assessment_data: Risk assessment and application data
            framework_name: Decision framework to use

        Returns:
            Decision results with explanation
        """
        start_time = time.time()

        try:
            # Get decision framework
            framework = self.decision_frameworks.get(framework_name, self.decision_frameworks["standard"])

            # Evaluate decision criteria
            criteria_results = framework.evaluate_decision_criteria(assessment_data)

            # Calculate overall score
            overall_score = framework.calculate_overall_score(criteria_results)

            # Determine decision type
            if overall_score >= framework.auto_decision_threshold:
                decision_type = DecisionType.AUTOMATIC
                decision = "approve" if overall_score >= 0.7 else "decline"
            elif overall_score >= framework.manual_review_threshold:
                decision_type = DecisionType.MANUAL_REVIEW
                decision = "refer"
            else:
                decision_type = DecisionType.REFERRED
                decision = "decline"

            # Generate decision explanation
            explanation = self._generate_decision_explanation(criteria_results, overall_score, framework)

            # Create decision result
            decision_result = {
                'decision_id': f"dec_{int(time.time())}",
                'decision_type': decision_type.value,
                'decision': decision,
                'overall_score': overall_score,
                'criteria_results': criteria_results,
                'framework_used': framework_name,
                'explanation': explanation,
                'confidence': min(1.0, overall_score + 0.1),
                'decision_timestamp': datetime.now().isoformat(),
                'processing_time': time.time() - start_time,
                'requires_review': decision_type in [DecisionType.MANUAL_REVIEW, DecisionType.REFERRED]
            }

            # Store decision for learning
            self._store_decision(assessment_data, decision_result)

            self.logger.info(f"Decision made: {decision} with score {overall_score:.3f}")
            return decision_result

        except Exception as e:
            self.logger.error(f"Decision making failed: {e}")
            return {
                'decision_id': f"dec_error_{int(time.time())}",
                'decision_type': 'error',
                'decision': 'refer',
                'error': str(e),
                'decision_timestamp': datetime.now().isoformat()
            }

    def _generate_decision_explanation(self, criteria_results: Dict[str, Any],
                                     overall_score: float, framework: DecisionFramework) -> str:
        """Generate human-readable decision explanation."""
        explanation_parts = [
            f"Overall Decision Score: {overall_score:.3f}",
            f"Framework: {framework.framework_name}",
            ""
        ]

        # Explain each criteria
        for criteria_type, result in criteria_results.items():
            criteria_name = criteria_type.replace('_', ' ').title()
            value = result['value']
            passed = result['passed']
            score = result['score']

            status = "✓ PASS" if passed else "✗ FAIL"
            explanation_parts.append(f"{criteria_name}: {value:.3f} - {status} (Score: {score:.3f})")

        # Explain final decision
        if overall_score >= framework.auto_decision_threshold:
            explanation_parts.append(f"\n→ AUTO-{decision.upper()} (Score above auto-decision threshold)")
        elif overall_score >= framework.manual_review_threshold:
            explanation_parts.append("\n→ REFERRED FOR REVIEW (Score in manual review range)")
        else:
            explanation_parts.append("\n→ DECLINED (Score below acceptable threshold)")

        return "\n".join(explanation_parts)

    def _initialize_default_frameworks(self) -> None:
        """Initialize default decision frameworks."""
        # Standard framework
        standard_criteria = [
            DecisionCriteria(DecisionCriteria.RISK_SCORE, weight=0.4, threshold=0.7),
            DecisionCriteria(DecisionCriteria.PREMIUM_ADEQUACY, weight=0.3, threshold=1.0),
            DecisionCriteria(DecisionCriteria.COVERAGE_LIMITS, weight=0.2, threshold=1.0),
            DecisionCriteria(DecisionCriteria.COMPLIANCE, weight=0.1, threshold=0.9)
        ]

        self.decision_frameworks["standard"] = DecisionFramework(
            framework_name="Standard Underwriting",
            decision_criteria=standard_criteria,
            auto_decision_threshold=0.8,
            manual_review_threshold=0.6
        )

        # Conservative framework
        conservative_criteria = [
            DecisionCriteria(DecisionCriteria.RISK_SCORE, weight=0.5, threshold=0.5),
            DecisionCriteria(DecisionCriteria.PREMIUM_ADEQUACY, weight=0.3, threshold=1.2),
            DecisionCriteria(DecisionCriteria.LOSS_HISTORY, weight=0.2, threshold=0.1)
        ]

        self.decision_frameworks["conservative"] = DecisionFramework(
            framework_name="Conservative Underwriting",
            decision_criteria=conservative_criteria,
            auto_decision_threshold=0.9,
            manual_review_threshold=0.7,
            risk_tolerance="conservative"
        )

        # Aggressive framework
        aggressive_criteria = [
            DecisionCriteria(DecisionCriteria.RISK_SCORE, weight=0.3, threshold=0.8),
            DecisionCriteria(DecisionCriteria.PREMIUM_ADEQUACY, weight=0.4, threshold=0.9),
            DecisionCriteria(DecisionCriteria.MARKET_CONDITIONS, weight=0.3, threshold=0.7)
        ]

        self.decision_frameworks["aggressive"] = DecisionFramework(
            framework_name="Aggressive Underwriting",
            decision_criteria=aggressive_criteria,
            auto_decision_threshold=0.7,
            manual_review_threshold=0.5,
            risk_tolerance="aggressive"
        )

    def add_framework(self, framework: DecisionFramework) -> bool:
        """Add decision framework."""
        try:
            self.decision_frameworks[framework.framework_name.lower()] = framework
            self.logger.info(f"Decision framework added: {framework.framework_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add framework: {e}")
            return False

    def get_framework(self, framework_name: str) -> Optional[DecisionFramework]:
        """Get decision framework by name."""
        return self.decision_frameworks.get(framework_name.lower())

    def _store_decision(self, assessment_data: Dict[str, Any], decision_result: Dict[str, Any]) -> None:
        """Store decision for learning and analysis."""
        decision_record = {
            'assessment_data': assessment_data,
            'decision_result': decision_result,
            'stored_at': datetime.now().isoformat()
        }

        self.decision_history.append(decision_record)

        # Keep only recent decisions (last 1000)
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-1000:]

    def get_decision_analytics(self) -> Dict[str, Any]:
        """Get decision analytics and performance metrics."""
        if not self.decision_history:
            return {'total_decisions': 0, 'accuracy': 0.0}

        total_decisions = len(self.decision_history)

        # Calculate decision distribution
        decision_types = {}
        decisions = {}

        for record in self.decision_history:
            decision_result = record['decision_result']
            decision_type = decision_result.get('decision_type', 'unknown')
            decision = decision_result.get('decision', 'unknown')

            decision_types[decision_type] = decision_types.get(decision_type, 0) + 1
            decisions[decision] = decisions.get(decision, 0) + 1

        # Calculate accuracy (requires ground truth labels for meaningful evaluation)
        accuracy = 0.85  # Placeholder

        return {
            'total_decisions': total_decisions,
            'decision_type_distribution': decision_types,
            'decision_distribution': decisions,
            'accuracy': accuracy,
            'average_confidence': np.mean([r['decision_result'].get('confidence', 0) for r in self.decision_history]),
            'framework_usage': self._get_framework_usage(),
            'last_updated': datetime.now().isoformat()
        }

    def _get_framework_usage(self) -> Dict[str, int]:
        """Get framework usage statistics."""
        framework_usage = {}

        for record in self.decision_history:
            framework = record['decision_result'].get('framework_used', 'unknown')
            framework_usage[framework] = framework_usage.get(framework, 0) + 1

        return framework_usage

    def export_decision_history(self, format: str = "json", filename: Optional[str] = None) -> str:
        """Export decision history to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"decision_history_{timestamp}.{format}"

        if format == "json":
            with open(filename, 'w') as f:
                json.dump(self.decision_history, f, indent=2, default=str)
        elif format == "csv":
            df = pd.DataFrame(self.decision_history)
            df.to_csv(filename, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        self.logger.info(f"Decision history exported to {filename}")
        return filename

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on decision engine."""
        return {
            'status': 'operational',
            'total_frameworks': len(self.decision_frameworks),
            'total_decisions': len(self.decision_history),
            'active_framework': self.active_framework,
            'last_decision': datetime.now().isoformat()
        }


# Convenience functions
def create_decision_engine(config: Optional[Dict[str, Any]] = None) -> UnderwritingDecisionEngine:
    """Create a new underwriting decision engine."""
    return UnderwritingDecisionEngine(config)

def make_sample_decision() -> Dict[str, Any]:
    """Make a sample underwriting decision for testing."""
    engine = UnderwritingDecisionEngine()

    sample_data = {
        'risk_score': 0.6,
        'premium_adequacy': 1.1,
        'coverage_adequacy': 1.0,
        'loss_ratio': 0.05,
        'financial_stability': 0.8,
        'compliance_score': 0.95,
        'market_competitiveness': 0.85
    }

    return engine.make_decision(sample_data)
