"""
Pricing Engine: Advanced insurance pricing and premium calculation.

This module provides sophisticated pricing capabilities including:
- Risk-based premium calculation
- Multi-factor pricing models
- Market-based pricing adjustments
- Reinsurance cost allocation
- Profit and expense loading
- Regulatory compliance pricing
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class PricingMethod(Enum):
    """Insurance pricing method enumeration."""
    TECHNICAL = "technical"
    RISK_LOADED = "risk_loaded"
    MARKET_ADJUSTED = "market_adjusted"
    EXPERIENCE_RATED = "experience_rated"
    CATASTROPHE_LOADED = "catastrophe_loaded"

class PremiumComponent(Enum):
    """Premium component enumeration."""
    PURE_PREMIUM = "pure_premium"
    EXPENSE_LOADING = "expense_loading"
    PROFIT_LOADING = "profit_loading"
    RISK_LOADING = "risk_loading"
    CATASTROPHE_LOADING = "catastrophe_loading"
    REINSURANCE_COST = "reinsurance_cost"

@dataclass
class PremiumCalculation:
    """Premium calculation result structure."""

    total_premium: float
    base_premium: float
    component_breakdown: Dict[PremiumComponent, float] = field(default_factory=dict)
    calculation_method: PricingMethod = PricingMethod.TECHNICAL
    confidence_level: float = 0.95
    calculation_timestamp: datetime = field(default_factory=datetime.now)

    # Coverage breakdown
    coverage_breakdown: Dict[str, float] = field(default_factory=dict)

    # Risk factors
    risk_factors: Dict[str, float] = field(default_factory=dict)

    # Metadata
    calculation_parameters: Dict[str, Any] = field(default_factory=dict)

    def get_component_percentage(self, component: PremiumComponent) -> float:
        """Get percentage of total premium for a component."""
        if self.total_premium > 0:
            return self.component_breakdown.get(component, 0.0) / self.total_premium
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert calculation to dictionary."""
        return {
            'total_premium': self.total_premium,
            'base_premium': self.base_premium,
            'component_breakdown': {k.value: v for k, v in self.component_breakdown.items()},
            'calculation_method': self.calculation_method.value,
            'confidence_level': self.confidence_level,
            'calculation_timestamp': self.calculation_timestamp.isoformat(),
            'coverage_breakdown': self.coverage_breakdown,
            'risk_factors': self.risk_factors,
            'calculation_parameters': self.calculation_parameters
        }

class PricingEngine:
    """
    Advanced insurance pricing engine with multiple calculation methods.

    This engine provides:
    - Technical pricing based on actuarial principles
    - Risk-loaded pricing with uncertainty quantification
    - Market-adjusted pricing with competitive analysis
    - Experience-rated pricing with claims history
    - Catastrophe-loaded pricing for extreme events
    - Regulatory compliance and rate filing support
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the pricing engine.

        Args:
            config: Pricing engine configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger("geo_infer_risk.underwriting.pricing_engine")

        # Pricing parameters
        self.expense_ratio = self.config.get('expense_ratio', 0.25)
        self.profit_margin = self.config.get('profit_margin', 0.15)
        self.risk_loading_factor = self.config.get('risk_loading_factor', 1.2)
        self.catastrophe_loading_factor = self.config.get('catastrophe_loading_factor', 1.1)

        # Rate tables and factors
        self.base_rates = self._load_base_rates()
        self.territory_factors = self._load_territory_factors()
        self.construction_factors = self._load_construction_factors()
        self.protection_factors = self._load_protection_factors()

        # Market data
        self.market_rates = self._load_market_rates()

        # Performance tracking
        self.pricing_metrics = {
            'total_calculations': 0,
            'average_premium': 0.0,
            'premium_distribution': {},
            'calculation_times': []
        }

        self.logger.info("Pricing engine initialized")

    def calculate_premium(self, application_data: Dict[str, Any],
                         risk_assessment: Dict[str, Any],
                         rule_evaluation: Dict[str, Any]) -> PremiumCalculation:
        """
        Calculate comprehensive insurance premium.

        Args:
            application_data: Policy application data
            risk_assessment: Risk assessment results
            rule_evaluation: Rule evaluation results

        Returns:
            Complete premium calculation with breakdown
        """
        start_time = time.time()

        try:
            # Extract key information
            property_info = application_data.get('property', {})
            coverage_requests = application_data.get('coverage_requests', [])

            # Calculate base premium
            base_premium = self._calculate_base_premium(property_info, risk_assessment)

            # Calculate component breakdown
            component_breakdown = self._calculate_component_breakdown(base_premium, risk_assessment)

            # Calculate coverage-specific premiums
            coverage_breakdown = self._calculate_coverage_breakdown(coverage_requests, base_premium)

            # Apply rule-based adjustments
            rule_adjustments = self._apply_rule_adjustments(base_premium, rule_evaluation)
            adjusted_base = base_premium + rule_adjustments

            # Calculate total premium
            total_premium = sum(component_breakdown.values()) + rule_adjustments

            # Create calculation result
            calculation = PremiumCalculation(
                total_premium=total_premium,
                base_premium=adjusted_base,
                component_breakdown=component_breakdown,
                calculation_method=PricingMethod.TECHNICAL,
                confidence_level=risk_assessment.get('confidence', 0.8),
                coverage_breakdown=coverage_breakdown,
                risk_factors=self._extract_risk_factors(risk_assessment),
                calculation_parameters={
                    'property_value': property_info.get('value', 0),
                    'risk_score': risk_assessment.get('risk_score', 0.5),
                    'coverage_count': len(coverage_requests)
                }
            )

            # Update metrics
            self._update_pricing_metrics(calculation)

            processing_time = time.time() - start_time
            self.logger.info(f"Premium calculated: ${total_premium:,.2f} in {processing_time:.3f}s")

            return calculation

        except Exception as e:
            self.logger.error(f"Premium calculation failed: {e}")
            # Return minimum premium as fallback
            return PremiumCalculation(
                total_premium=100.0,
                base_premium=100.0,
                calculation_method=PricingMethod.TECHNICAL,
                confidence_level=0.5
            )

    def _calculate_base_premium(self, property_info: Dict[str, Any],
                               risk_assessment: Dict[str, Any]) -> float:
        """Calculate base premium using technical pricing."""
        property_value = property_info.get('value', 200000)
        risk_score = risk_assessment.get('risk_score', 0.5)

        # Get base rate based on property type
        property_type = property_info.get('type', 'residential')
        base_rate = self.base_rates.get(property_type, 0.005)  # 0.5% default

        # Apply risk loading
        risk_adjusted_rate = base_rate * (1 + risk_score * self.risk_loading_factor)

        # Calculate base premium
        base_premium = property_value * risk_adjusted_rate

        return base_premium

    def _calculate_component_breakdown(self, base_premium: float,
                                     risk_assessment: Dict[str, Any]) -> Dict[PremiumComponent, float]:
        """Calculate premium component breakdown."""
        components = {}

        # Pure premium (base risk cost)
        components[PremiumComponent.PURE_PREMIUM] = base_premium * 0.7  # 70% of base

        # Expense loading
        components[PremiumComponent.EXPENSE_LOADING] = base_premium * self.expense_ratio

        # Profit loading
        components[PremiumComponent.PROFIT_LOADING] = base_premium * self.profit_margin

        # Risk loading
        risk_score = risk_assessment.get('risk_score', 0.5)
        components[PremiumComponent.RISK_LOADING] = base_premium * risk_score * 0.2

        # Catastrophe loading
        cat_risk = risk_assessment.get('catastrophe_risk', 0.1)
        components[PremiumComponent.CATASTROPHE_LOADING] = base_premium * cat_risk * 0.1

        # Reinsurance cost (simplified)
        components[PremiumComponent.REINSURANCE_COST] = base_premium * 0.05

        return components

    def _calculate_coverage_breakdown(self, coverage_requests: List[Dict[str, Any]],
                                    base_premium: float) -> Dict[str, float]:
        """Calculate premium breakdown by coverage type."""
        breakdown = {}

        if not coverage_requests:
            breakdown['property'] = base_premium
            return breakdown

        # Distribute premium based on coverage limits
        total_limit = sum(coverage.get('limit', 0) for coverage in coverage_requests)

        for coverage in coverage_requests:
            coverage_type = coverage.get('coverage_type', 'property')
            limit = coverage.get('limit', 0)

            if total_limit > 0:
                proportion = limit / total_limit
                breakdown[coverage_type] = base_premium * proportion
            else:
                breakdown[coverage_type] = base_premium / len(coverage_requests)

        return breakdown

    def _apply_rule_adjustments(self, base_premium: float,
                               rule_evaluation: Dict[str, Any]) -> float:
        """Apply rule-based premium adjustments."""
        adjustments = 0.0

        # Get rule actions that affect pricing
        rule_results = rule_evaluation.get('rule_results', [])

        for rule_result in rule_results:
            if rule_result.get('passed', False):
                action_params = rule_result.get('action_parameters', {})

                if 'premium_adjustment' in action_params:
                    adjustments += action_params['premium_adjustment']
                elif 'multiplier' in action_params:
                    adjustments += base_premium * (action_params['multiplier'] - 1.0)

        return adjustments

    def _extract_risk_factors(self, risk_assessment: Dict[str, Any]) -> Dict[str, float]:
        """Extract key risk factors for premium calculation."""
        return {
            'location_risk': risk_assessment.get('location_risk', 0.5),
            'property_risk': risk_assessment.get('property_risk', 0.5),
            'historical_risk': risk_assessment.get('historical_risk', 0.5),
            'catastrophe_risk': risk_assessment.get('catastrophe_risk', 0.1)
        }

    def _load_base_rates(self) -> Dict[str, float]:
        """Load base insurance rates by property type."""
        return {
            'residential': 0.005,  # 0.5% of value
            'commercial': 0.008,   # 0.8% of value
            'industrial': 0.012,   # 1.2% of value
            'agricultural': 0.006, # 0.6% of value
            'institutional': 0.007 # 0.7% of value
        }

    def _load_territory_factors(self) -> Dict[str, float]:
        """Load territory risk factors."""
        return {
            'low_risk': 0.8,
            'medium_risk': 1.0,
            'high_risk': 1.5,
            'coastal': 1.8,
            'earthquake_zone': 1.4,
            'wildfire_prone': 1.6
        }

    def _load_construction_factors(self) -> Dict[str, float]:
        """Load construction type factors."""
        return {
            'frame': 1.2,
            'masonry': 1.0,
            'concrete': 0.8,
            'steel': 0.9,
            'fire_resistive': 0.7
        }

    def _load_protection_factors(self) -> Dict[str, float]:
        """Load protection system factors."""
        return {
            'sprinkler_system': 0.85,
            'alarm_system': 0.9,
            'security_system': 0.95,
            'fire_extinguishers': 0.98
        }

    def _load_market_rates(self) -> Dict[str, float]:
        """Load market rate data for competitive pricing."""
        return {
            'residential': 0.006,  # Market average
            'commercial': 0.009,
            'industrial': 0.014
        }

    def calculate_market_adjusted_premium(self, technical_premium: float,
                                        market_data: Dict[str, Any]) -> float:
        """
        Calculate market-adjusted premium based on competitive analysis.

        Args:
            technical_premium: Technically calculated premium
            market_data: Market rate and competition data

        Returns:
            Market-adjusted premium
        """
        try:
            # Get market rates for comparison
            property_type = market_data.get('property_type', 'residential')
            market_rate = self.market_rates.get(property_type, 0.006)

            # Calculate market-based premium
            property_value = market_data.get('property_value', 200000)
            market_premium = property_value * market_rate

            # Apply market adjustment factor
            market_factor = market_data.get('market_factor', 1.0)
            adjusted_premium = market_premium * market_factor

            # Ensure minimum premium
            min_premium = market_data.get('minimum_premium', 100)
            return max(min_premium, adjusted_premium)

        except Exception as e:
            self.logger.warning(f"Market adjustment failed: {e}")
            return technical_premium

    def calculate_risk_loaded_premium(self, base_premium: float,
                                    risk_assessment: Dict[str, Any]) -> float:
        """
        Calculate risk-loaded premium with uncertainty consideration.

        Args:
            base_premium: Base premium amount
            risk_assessment: Risk assessment results

        Returns:
            Risk-loaded premium
        """
        try:
            risk_score = risk_assessment.get('risk_score', 0.5)
            confidence = risk_assessment.get('confidence', 0.8)

            # Calculate risk loading factor
            base_loading = 1.0 + risk_score * self.risk_loading_factor

            # Adjust for confidence (lower confidence = higher loading)
            confidence_adjustment = 1.0 + (1.0 - confidence) * 0.2
            risk_loading = base_loading * confidence_adjustment

            return base_premium * risk_loading

        except Exception as e:
            self.logger.warning(f"Risk loading calculation failed: {e}")
            return base_premium * 1.2  # Default 20% loading

    def calculate_catastrophe_premium(self, base_premium: float,
                                     catastrophe_assessment: Dict[str, Any]) -> float:
        """
        Calculate catastrophe-loaded premium.

        Args:
            base_premium: Base premium amount
            catastrophe_assessment: Catastrophe risk assessment

        Returns:
            Catastrophe-loaded premium
        """
        try:
            cat_risk = catastrophe_assessment.get('catastrophe_risk', 0.1)
            cat_frequency = catastrophe_assessment.get('cat_frequency', 0.01)

            # Calculate catastrophe loading
            cat_loading = cat_risk * cat_frequency * self.catastrophe_loading_factor
            catastrophe_premium = base_premium * cat_loading

            return catastrophe_premium

        except Exception as e:
            self.logger.warning(f"Catastrophe premium calculation failed: {e}")
            return base_premium * 0.1  # Default 10% catastrophe loading

    def optimize_premium_structure(self, target_premium: float,
                                 constraints: Dict[str, Any]) -> Dict[str, float]:
        """
        Optimize premium structure to meet business objectives.

        Args:
            target_premium: Target total premium
            constraints: Business constraints and objectives

        Returns:
            Optimized premium component breakdown
        """
        try:
            # Define optimization constraints
            min_profit_margin = constraints.get('min_profit_margin', 0.1)
            max_expense_ratio = constraints.get('max_expense_ratio', 0.3)
            required_risk_loading = constraints.get('required_risk_loading', 0.15)

            # Optimize component allocation
            profit_component = target_premium * min_profit_margin
            expense_component = min(target_premium * max_expense_ratio, target_premium * 0.25)
            risk_component = target_premium * required_risk_loading

            # Calculate remaining for pure premium
            pure_premium = target_premium - profit_component - expense_component - risk_component

            return {
                PremiumComponent.PURE_PREMIUM.value: max(0, pure_premium),
                PremiumComponent.EXPENSE_LOADING.value: expense_component,
                PremiumComponent.PROFIT_LOADING.value: profit_component,
                PremiumComponent.RISK_LOADING.value: risk_component,
                PremiumComponent.CATASTROPHE_LOADING.value: target_premium * 0.05,
                PremiumComponent.REINSURANCE_COST.value: target_premium * 0.03
            }

        except Exception as e:
            self.logger.error(f"Premium optimization failed: {e}")
            # Return default breakdown
            return {
                PremiumComponent.PURE_PREMIUM.value: target_premium * 0.6,
                PremiumComponent.EXPENSE_LOADING.value: target_premium * 0.25,
                PremiumComponent.PROFIT_LOADING.value: target_premium * 0.15
            }

    def validate_premium(self, calculation: PremiumCalculation) -> Dict[str, Any]:
        """
        Validate premium calculation for compliance and reasonableness.

        Args:
            calculation: Premium calculation to validate

        Returns:
            Validation results
        """
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'recommendations': []
        }

        try:
            # Check premium reasonableness
            if calculation.total_premium <= 0:
                validation_result['errors'].append("Premium must be positive")
                validation_result['is_valid'] = False

            # Check component proportions
            total_components = sum(calculation.component_breakdown.values())
            if abs(total_components - calculation.total_premium) > 0.01:
                validation_result['warnings'].append("Component breakdown doesn't match total premium")

            # Check profit margin
            profit_margin = calculation.get_component_percentage(PremiumComponent.PROFIT_LOADING)
            if profit_margin < 0.05:
                validation_result['warnings'].append("Low profit margin may not be sustainable")
            elif profit_margin > 0.3:
                validation_result['warnings'].append("High profit margin may not be competitive")

            # Check expense ratio
            expense_ratio = calculation.get_component_percentage(PremiumComponent.EXPENSE_LOADING)
            if expense_ratio > 0.4:
                validation_result['warnings'].append("High expense ratio may indicate inefficiency")

            # Check risk loading
            risk_loading = calculation.get_component_percentage(PremiumComponent.RISK_LOADING)
            if risk_loading > 0.3:
                validation_result['warnings'].append("High risk loading may indicate poor risk selection")

        except Exception as e:
            validation_result['errors'].append(f"Validation error: {str(e)}")
            validation_result['is_valid'] = False

        return validation_result

    def _update_pricing_metrics(self, calculation: PremiumCalculation) -> None:
        """Update pricing performance metrics."""
        self.pricing_metrics['total_calculations'] += 1

        # Update average premium
        if self.pricing_metrics['average_premium'] == 0:
            self.pricing_metrics['average_premium'] = calculation.total_premium
        else:
            # Exponential moving average
            alpha = 0.1
            self.pricing_metrics['average_premium'] = (
                alpha * calculation.total_premium +
                (1 - alpha) * self.pricing_metrics['average_premium']
            )

        # Update premium distribution
        premium_bucket = self._get_premium_bucket(calculation.total_premium)
        self.pricing_metrics['premium_distribution'][premium_bucket] = (
            self.pricing_metrics['premium_distribution'].get(premium_bucket, 0) + 1
        )

    def _get_premium_bucket(self, premium: float) -> str:
        """Get premium bucket for distribution analysis."""
        if premium < 500:
            return "under_500"
        elif premium < 1000:
            return "500_1000"
        elif premium < 2500:
            return "1000_2500"
        elif premium < 5000:
            return "2500_5000"
        elif premium < 10000:
            return "5000_10000"
        else:
            return "over_10000"

    def get_pricing_metrics(self) -> Dict[str, Any]:
        """Get pricing engine performance metrics."""
        return {
            'total_calculations': self.pricing_metrics['total_calculations'],
            'average_premium': self.pricing_metrics['average_premium'],
            'premium_distribution': self.pricing_metrics['premium_distribution'],
            'calculation_times': self.pricing_metrics['calculation_times'][-10:]  # Last 10 calculations
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on pricing engine."""
        return {
            'status': 'operational',
            'total_calculations': self.pricing_metrics['total_calculations'],
            'last_calculation': datetime.now().isoformat(),
            'configuration': {
                'expense_ratio': self.expense_ratio,
                'profit_margin': self.profit_margin,
                'risk_loading_factor': self.risk_loading_factor
            }
        }


class PremiumCalculator:
    """Advanced premium calculation with multiple methodologies."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the premium calculator.

        Args:
            config: Calculator configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger("geo_infer_risk.underwriting.premium_calculator")

        # Load rate tables
        self.rate_tables = self._load_rate_tables()

        self.logger.info("Premium calculator initialized")

    def calculate_experience_rated_premium(self, policy_history: Dict[str, Any],
                                         base_premium: float) -> float:
        """
        Calculate experience-rated premium based on claims history.

        Args:
            policy_history: Historical claims and loss data
            base_premium: Base premium for rating

        Returns:
            Experience-rated premium
        """
        try:
            # Extract claims history
            claims_history = policy_history.get('claims_history', [])
            loss_history = policy_history.get('loss_history', [])

            # Calculate experience modification factor
            experience_factor = self._calculate_experience_factor(claims_history, loss_history)

            # Apply experience rating
            experience_premium = base_premium * experience_factor

            # Ensure minimum premium
            min_premium = policy_history.get('minimum_premium', 100)
            return max(min_premium, experience_premium)

        except Exception as e:
            self.logger.warning(f"Experience rating failed: {e}")
            return base_premium

    def _calculate_experience_factor(self, claims_history: List[Dict[str, Any]],
                                   loss_history: List[float]) -> float:
        """Calculate experience modification factor."""
        if not claims_history and not loss_history:
            return 1.0  # No experience data

        # Calculate claims frequency
        num_claims = len(claims_history)
        expected_claims = 1.0  # Expected claims per policy period
        frequency_factor = num_claims / expected_claims

        # Calculate loss ratio
        total_losses = sum(loss_history)
        expected_losses = 1000.0  # Expected losses
        loss_ratio = total_losses / expected_losses if expected_losses > 0 else 1.0

        # Experience modification factor
        experience_factor = (frequency_factor + loss_ratio) / 2.0

        # Cap experience factor
        return min(2.0, max(0.5, experience_factor))

    def calculate_layered_premium(self, coverage_structure: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate premium for layered coverage structures.

        Args:
            coverage_structure: Layered coverage configuration

        Returns:
            Premium breakdown by layer
        """
        layers = coverage_structure.get('layers', [])
        layer_premiums = {}

        for layer in layers:
            layer_limit = layer.get('limit', 0)
            layer_deductible = layer.get('deductible', 0)

            # Calculate layer premium (simplified)
            layer_premium = layer_limit * 0.001  # 0.1% rate
            layer_premiums[f"layer_{layer_limit}"] = layer_premium

        return layer_premiums

    def _load_rate_tables(self) -> Dict[str, Any]:
        """Load comprehensive rate tables."""
        return {
            'base_rates': self._load_base_rates(),
            'territory_factors': self._load_territory_factors(),
            'construction_factors': self._load_construction_factors(),
            'protection_factors': self._load_protection_factors(),
            'deductible_factors': {
                0.005: 1.0,   # 0.5% deductible
                0.01: 0.95,   # 1% deductible
                0.02: 0.9,    # 2% deductible
                0.05: 0.85    # 5% deductible
            }
        }

    def get_rate_table(self, table_name: str) -> Dict[str, float]:
        """Get specific rate table."""
        return self.rate_tables.get(table_name, {})

    def update_rate_table(self, table_name: str, rates: Dict[str, float]) -> None:
        """Update rate table with new rates."""
        if table_name in self.rate_tables:
            self.rate_tables[table_name].update(rates)
            self.logger.info(f"Rate table {table_name} updated")


# Convenience functions
def create_pricing_engine(config: Optional[Dict[str, Any]] = None) -> PricingEngine:
    """Create a new pricing engine."""
    return PricingEngine(config)

def create_sample_premium_calculation() -> PremiumCalculation:
    """Create a sample premium calculation for testing."""
    return PremiumCalculation(
        total_premium=2500.0,
        base_premium=2000.0,
        component_breakdown={
            PremiumComponent.PURE_PREMIUM: 1400.0,
            PremiumComponent.EXPENSE_LOADING: 500.0,
            PremiumComponent.PROFIT_LOADING: 300.0,
            PremiumComponent.RISK_LOADING: 300.0
        },
        calculation_method=PricingMethod.TECHNICAL,
        confidence_level=0.9,
        coverage_breakdown={'property': 2500.0},
        risk_factors={'location_risk': 0.6, 'property_risk': 0.4}
    )
