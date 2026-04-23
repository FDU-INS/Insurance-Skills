"""
Policy Management: Comprehensive insurance policy lifecycle management.

This module provides sophisticated policy management capabilities including:
- Policy creation and configuration
- Policy lifecycle management (quote, bind, renew, cancel)
- Coverage management and endorsements
- Policy portfolio management
- Premium calculation and adjustment
- Policy compliance and regulatory reporting
"""

import logging
import time
import uuid
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class PolicyStatus(Enum):
    """Insurance policy status enumeration."""
    QUOTED = "quoted"
    BOUND = "bound"
    ACTIVE = "active"
    RENEWED = "renewed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    PENDING_CANCELLATION = "pending_cancellation"

class CoverageType(Enum):
    """Insurance coverage type enumeration."""
    PROPERTY = "property"
    LIABILITY = "liability"
    BUSINESS_INTERRUPTION = "business_interruption"
    FLOOD = "flood"
    EARTHQUAKE = "earthquake"
    HURRICANE = "hurricane"
    ALL_RISK = "all_risk"
    NAMED_PERILS = "named_perils"

@dataclass
class Coverage:
    """Insurance coverage configuration."""
    coverage_type: CoverageType
    limit: float
    deductible: float
    premium: float = 0.0
    coinsurance: float = 1.0  # 100% coinsurance by default
    waiting_period_days: int = 0
    retroactive_date: Optional[datetime] = None
    conditions: List[str] = field(default_factory=list)
    exclusions: List[str] = field(default_factory=list)

@dataclass
class Endorsement:
    """Policy endorsement or amendment."""
    endorsement_id: str
    endorsement_type: str
    effective_date: datetime
    description: str
    premium_change: float = 0.0
    coverage_changes: Dict[str, Any] = field(default_factory=dict)
    conditions: List[str] = field(default_factory=list)

@dataclass
class Policy:
    """Insurance policy data structure."""
    policy_id: str
    policy_number: str
    status: PolicyStatus
    policyholder_id: str
    property_id: str

    # Policy terms (required - must precede fields with defaults)
    effective_date: datetime
    expiration_date: datetime

    # Coverage information
    coverages: List[Coverage] = field(default_factory=list)
    term_months: int = 12

    # Financial information
    total_premium: float = 0.0
    base_premium: float = 0.0
    fees: float = 0.0
    taxes: float = 0.0

    # Risk information
    risk_score: float = 0.0
    risk_tier: str = "standard"

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    underwriter_id: Optional[str] = None

    # Endorsements and amendments
    endorsements: List[Endorsement] = field(default_factory=list)

    # Additional data
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_coverage(self, coverage: Coverage) -> None:
        """Add coverage to the policy."""
        self.coverages.append(coverage)
        self._update_premium()

    def remove_coverage(self, coverage_type: CoverageType) -> bool:
        """Remove coverage from the policy."""
        for i, coverage in enumerate(self.coverages):
            if coverage.coverage_type == coverage_type:
                del self.coverages[i]
                self._update_premium()
                return True
        return False

    def add_endorsement(self, endorsement: Endorsement) -> None:
        """Add endorsement to the policy."""
        self.endorsements.append(endorsement)
        self._update_premium()

    def _update_premium(self) -> None:
        """Update total premium based on coverages and endorsements."""
        base_premium = sum(coverage.premium for coverage in self.coverages)
        endorsement_adjustment = sum(endorsement.premium_change for endorsement in self.endorsements)

        self.total_premium = base_premium + endorsement_adjustment + self.fees + self.taxes
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        """Check if policy is currently active."""
        now = datetime.now()
        return (self.status == PolicyStatus.ACTIVE and
                self.effective_date <= now <= self.expiration_date)

    def days_to_expiration(self) -> int:
        """Calculate days until policy expiration."""
        now = datetime.now()
        if now > self.expiration_date:
            return 0
        return (self.expiration_date - now).days

    def to_dict(self) -> Dict[str, Any]:
        """Convert policy to dictionary for serialization."""
        return {
            'policy_id': self.policy_id,
            'policy_number': self.policy_number,
            'status': self.status.value,
            'policyholder_id': self.policyholder_id,
            'property_id': self.property_id,
            'coverages': [
                {
                    'coverage_type': coverage.coverage_type.value,
                    'limit': coverage.limit,
                    'deductible': coverage.deductible,
                    'premium': coverage.premium,
                    'coinsurance': coverage.coinsurance,
                    'waiting_period_days': coverage.waiting_period_days,
                    'retroactive_date': coverage.retroactive_date.isoformat() if coverage.retroactive_date else None,
                    'conditions': coverage.conditions,
                    'exclusions': coverage.exclusions
                }
                for coverage in self.coverages
            ],
            'effective_date': self.effective_date.isoformat(),
            'expiration_date': self.expiration_date.isoformat(),
            'term_months': self.term_months,
            'total_premium': self.total_premium,
            'base_premium': self.base_premium,
            'fees': self.fees,
            'taxes': self.taxes,
            'risk_score': self.risk_score,
            'risk_tier': self.risk_tier,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by,
            'underwriter_id': self.underwriter_id,
            'endorsements': [
                {
                    'endorsement_id': endorsement.endorsement_id,
                    'endorsement_type': endorsement.endorsement_type,
                    'effective_date': endorsement.effective_date.isoformat(),
                    'description': endorsement.description,
                    'premium_change': endorsement.premium_change,
                    'coverage_changes': endorsement.coverage_changes,
                    'conditions': endorsement.conditions
                }
                for endorsement in self.endorsements
            ],
            'metadata': self.metadata
        }

class PolicyLifecycle:
    """Manages the complete lifecycle of insurance policies."""

    def __init__(self):
        self.states = {
            PolicyStatus.QUOTED: self._handle_quoted,
            PolicyStatus.BOUND: self._handle_bound,
            PolicyStatus.ACTIVE: self._handle_active,
            PolicyStatus.RENEWED: self._handle_renewed,
            PolicyStatus.CANCELLED: self._handle_cancelled,
            PolicyStatus.EXPIRED: self._handle_expired,
            PolicyStatus.SUSPENDED: self._handle_suspended,
            PolicyStatus.PENDING_CANCELLATION: self._handle_pending_cancellation
        }

    def transition_policy(self, policy: Policy, new_status: PolicyStatus,
                         reason: str = "", **kwargs) -> bool:
        """
        Transition policy to new status.

        Args:
            policy: Policy to transition
            new_status: Target status
            reason: Reason for transition
            **kwargs: Additional transition parameters

        Returns:
            True if transition successful
        """
        if new_status not in self.states:
            logger.error(f"Invalid policy status: {new_status}")
            return False

        try:
            # Call appropriate handler
            success = self.states[new_status](policy, reason, **kwargs)

            if success:
                policy.status = new_status
                policy.updated_at = datetime.now()

                # Log transition
                logger.info(f"Policy {policy.policy_id} transitioned to {new_status.value}: {reason}")

            return success

        except Exception as e:
            logger.error(f"Policy transition failed: {e}")
            return False

    def _handle_quoted(self, policy: Policy, reason: str, **kwargs) -> bool:
        """Handle policy in quoted status."""
        # Validate quote requirements
        if policy.total_premium <= 0:
            logger.error("Cannot quote policy with zero premium")
            return False

        return True

    def _handle_bound(self, policy: Policy, reason: str, **kwargs) -> bool:
        """Handle policy binding."""
        # Validate binding requirements
        if not policy.coverages:
            logger.error("Cannot bind policy without coverages")
            return False

        # Set effective date
        policy.effective_date = kwargs.get('effective_date', datetime.now())

        return True

    def _handle_active(self, policy: Policy, reason: str, **kwargs) -> bool:
        """Handle policy activation."""
        # Policy becomes active when effective date is reached
        now = datetime.now()
        if policy.effective_date > now:
            logger.warning("Policy effective date is in the future")
            return False

        return True

    def _handle_renewed(self, policy: Policy, reason: str, **kwargs) -> bool:
        """Handle policy renewal."""
        # Extend expiration date
        renewal_term = kwargs.get('renewal_term_months', policy.term_months)
        policy.expiration_date = policy.expiration_date + timedelta(days=renewal_term * 30)

        return True

    def _handle_cancelled(self, policy: Policy, reason: str, **kwargs) -> bool:
        """Handle policy cancellation."""
        # Calculate refund if applicable
        cancellation_date = kwargs.get('cancellation_date', datetime.now())
        days_remaining = (policy.expiration_date - cancellation_date).days

        if days_remaining > 0:
            daily_premium = policy.total_premium / (policy.term_months * 30)
            refund_amount = daily_premium * days_remaining
            policy.metadata['cancellation_refund'] = refund_amount

        return True

    def _handle_expired(self, policy: Policy, reason: str, **kwargs) -> bool:
        """Handle policy expiration."""
        # Mark as expired
        policy.metadata['expired_at'] = datetime.now().isoformat()
        return True

    def _handle_suspended(self, policy: Policy, reason: str, **kwargs) -> bool:
        """Handle policy suspension."""
        # Record suspension reason
        policy.metadata['suspension_reason'] = reason
        policy.metadata['suspended_at'] = datetime.now().isoformat()
        return True

    def _handle_pending_cancellation(self, policy: Policy, reason: str, **kwargs) -> bool:
        """Handle pending cancellation status."""
        # Set cancellation effective date
        cancellation_date = kwargs.get('cancellation_date', datetime.now() + timedelta(days=30))
        policy.metadata['pending_cancellation_date'] = cancellation_date.isoformat()
        return True

class PolicyManager:
    """
    Comprehensive policy management system.

    This manager handles:
    - Policy creation and configuration
    - Policy search and retrieval
    - Policy portfolio management
    - Policy performance tracking
    - Policy compliance monitoring
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the policy manager.

        Args:
            config: Policy management configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger("geo_infer_risk.underwriting.policy_manager")

        # Policy storage
        self.policies: Dict[str, Policy] = {}
        self.policy_index: Dict[str, List[str]] = {}  # Index by various criteria

        # Lifecycle manager
        self.lifecycle = PolicyLifecycle()

        # Performance tracking
        self.performance_metrics = {
            'total_policies': 0,
            'active_policies': 0,
            'total_premium': 0.0,
            'average_premium': 0.0,
            'policies_by_status': {},
            'policies_by_risk_tier': {}
        }

        self.logger.info("Policy manager initialized")

    def create_policy(self, application_data: Dict[str, Any],
                     premium_calculation: Dict[str, Any],
                     decision: Dict[str, Any]) -> Policy:
        """
        Create a new insurance policy from application data.

        Args:
            application_data: Policy application information
            premium_calculation: Premium calculation results
            decision: Underwriting decision

        Returns:
            Created policy object
        """
        # Generate policy identifiers
        policy_id = str(uuid.uuid4())
        policy_number = self._generate_policy_number()

        # Extract policyholder and property information
        policyholder_id = application_data.get('policyholder_id', 'unknown')
        property_id = application_data.get('property_id', 'unknown')

        # Set policy term
        effective_date = application_data.get('effective_date', datetime.now())
        term_months = application_data.get('term_months', 12)
        expiration_date = effective_date + timedelta(days=term_months * 30)

        # Create policy
        policy = Policy(
            policy_id=policy_id,
            policy_number=policy_number,
            status=PolicyStatus.QUOTED,
            policyholder_id=policyholder_id,
            property_id=property_id,
            effective_date=effective_date,
            expiration_date=expiration_date,
            term_months=term_months,
            total_premium=premium_calculation.get('total_premium', 0),
            base_premium=premium_calculation.get('base_premium', 0),
            risk_score=decision.get('risk_score', 0.5),
            risk_tier=self._determine_risk_tier(decision.get('risk_score', 0.5)),
            created_by="underwriting_system"
        )

        # Add coverages based on application
        coverages = self._create_coverages_from_application(application_data, premium_calculation)
        for coverage in coverages:
            policy.add_coverage(coverage)

        # Store policy
        self.policies[policy_id] = policy
        self._update_policy_index(policy)

        # Update metrics
        self._update_performance_metrics()

        self.logger.info(f"Policy created: {policy_number} for property {property_id}")
        return policy

    def _generate_policy_number(self) -> str:
        """Generate unique policy number."""
        timestamp = int(time.time())
        random_suffix = np.random.randint(1000, 9999)
        return f"POL{timestamp}{random_suffix}"

    def _determine_risk_tier(self, risk_score: float) -> str:
        """Determine risk tier from risk score."""
        if risk_score < 0.3:
            return "preferred"
        elif risk_score < 0.6:
            return "standard"
        elif risk_score < 0.8:
            return "high"
        else:
            return "decline"

    def _create_coverages_from_application(self, application_data: Dict[str, Any],
                                         premium_calculation: Dict[str, Any]) -> List[Coverage]:
        """Create coverages from application data."""
        coverages = []
        coverage_requests = application_data.get('coverage_requests', [])

        for coverage_request in coverage_requests:
            coverage_type = CoverageType(coverage_request.get('coverage_type', 'property'))
            limit = coverage_request.get('limit', 100000)
            deductible = coverage_request.get('deductible', 0.02 * limit)

            # Get premium for this coverage
            coverage_premium = premium_calculation.get('coverage_breakdown', {}).get(
                coverage_type.value, 0
            )

            coverage = Coverage(
                coverage_type=coverage_type,
                limit=limit,
                deductible=deductible,
                premium=coverage_premium,
                conditions=coverage_request.get('conditions', []),
                exclusions=coverage_request.get('exclusions', [])
            )

            coverages.append(coverage)

        return coverages

    def get_policy(self, policy_id: str) -> Optional[Policy]:
        """Retrieve policy by ID."""
        return self.policies.get(policy_id)

    def search_policies(self, criteria: Dict[str, Any]) -> List[Policy]:
        """
        Search policies based on criteria.

        Args:
            criteria: Search criteria (status, risk_tier, policyholder_id, etc.)

        Returns:
            List of matching policies
        """
        matching_policies = []

        for policy in self.policies.values():
            matches = True

            for key, value in criteria.items():
                if hasattr(policy, key):
                    policy_value = getattr(policy, key)
                    if policy_value != value:
                        matches = False
                        break
                elif key == 'status' and policy.status != PolicyStatus(value):
                    matches = False
                    break

            if matches:
                matching_policies.append(policy)

        return matching_policies

    def update_policy(self, policy_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update policy information.

        Args:
            policy_id: Policy to update
            updates: Fields to update

        Returns:
            True if update successful
        """
        if policy_id not in self.policies:
            return False

        policy = self.policies[policy_id]

        try:
            # Update policy fields
            for key, value in updates.items():
                if hasattr(policy, key):
                    setattr(policy, key, value)
                elif key == 'status':
                    policy.status = PolicyStatus(value)

            policy.updated_at = datetime.now()

            # Update index
            self._update_policy_index(policy)

            # Update metrics
            self._update_performance_metrics()

            self.logger.info(f"Policy {policy_id} updated")
            return True

        except Exception as e:
            self.logger.error(f"Policy update failed: {e}")
            return False

    def add_endorsement(self, policy_id: str, endorsement: Endorsement) -> bool:
        """
        Add endorsement to policy.

        Args:
            policy_id: Policy to modify
            endorsement: Endorsement to add

        Returns:
            True if successful
        """
        if policy_id not in self.policies:
            return False

        policy = self.policies[policy_id]
        policy.add_endorsement(endorsement)

        # Update index
        self._update_policy_index(policy)

        self.logger.info(f"Endorsement {endorsement.endorsement_id} added to policy {policy_id}")
        return True

    def bind_policy(self, policy_id: str, effective_date: Optional[datetime] = None) -> bool:
        """
        Bind quoted policy.

        Args:
            policy_id: Policy to bind
            effective_date: Effective date for binding

        Returns:
            True if binding successful
        """
        if policy_id not in self.policies:
            return False

        policy = self.policies[policy_id]

        if policy.status != PolicyStatus.QUOTED:
            self.logger.error(f"Cannot bind policy in status: {policy.status}")
            return False

        # Transition to bound status
        success = self.lifecycle.transition_policy(
            policy, PolicyStatus.BOUND,
            reason="Policy bound by underwriter",
            effective_date=effective_date or datetime.now()
        )

        if success:
            self._update_policy_index(policy)
            self._update_performance_metrics()

        return success

    def activate_policy(self, policy_id: str) -> bool:
        """
        Activate bound policy.

        Args:
            policy_id: Policy to activate

        Returns:
            True if activation successful
        """
        if policy_id not in self.policies:
            return False

        policy = self.policies[policy_id]

        if policy.status != PolicyStatus.BOUND:
            self.logger.error(f"Cannot activate policy in status: {policy.status}")
            return False

        # Transition to active status
        success = self.lifecycle.transition_policy(
            policy, PolicyStatus.ACTIVE,
            reason="Policy activated"
        )

        if success:
            self._update_policy_index(policy)
            self._update_performance_metrics()

        return success

    def renew_policy(self, policy_id: str, renewal_term_months: Optional[int] = None) -> Optional[Policy]:
        """
        Renew existing policy.

        Args:
            policy_id: Policy to renew
            renewal_term_months: Renewal term in months

        Returns:
            New renewed policy or None if renewal failed
        """
        if policy_id not in self.policies:
            return None

        original_policy = self.policies[policy_id]

        if original_policy.status != PolicyStatus.ACTIVE:
            self.logger.error(f"Cannot renew policy in status: {original_policy.status}")
            return None

        # Create renewal policy
        renewal_policy = Policy(
            policy_id=str(uuid.uuid4()),
            policy_number=self._generate_policy_number(),
            status=PolicyStatus.QUOTED,
            policyholder_id=original_policy.policyholder_id,
            property_id=original_policy.property_id,
            effective_date=original_policy.expiration_date + timedelta(days=1),
            expiration_date=original_policy.expiration_date + timedelta(days=(renewal_term_months or original_policy.term_months) * 30),
            term_months=renewal_term_months or original_policy.term_months,
            coverages=original_policy.coverages.copy(),  # Copy coverages
            total_premium=original_policy.total_premium * 0.95,  # Small renewal discount
            risk_score=original_policy.risk_score,
            risk_tier=original_policy.risk_tier,
            created_by="renewal_system"
        )

        # Store renewal policy
        self.policies[renewal_policy.policy_id] = renewal_policy
        self._update_policy_index(renewal_policy)

        # Mark original as renewed
        original_policy.status = PolicyStatus.RENEWED
        original_policy.metadata['renewed_to'] = renewal_policy.policy_id

        self._update_performance_metrics()

        self.logger.info(f"Policy {policy_id} renewed to {renewal_policy.policy_id}")
        return renewal_policy

    def cancel_policy(self, policy_id: str, reason: str, cancellation_date: Optional[datetime] = None) -> bool:
        """
        Cancel existing policy.

        Args:
            policy_id: Policy to cancel
            reason: Cancellation reason
            cancellation_date: Effective cancellation date

        Returns:
            True if cancellation successful
        """
        if policy_id not in self.policies:
            return False

        policy = self.policies[policy_id]

        if policy.status not in [PolicyStatus.ACTIVE, PolicyStatus.BOUND]:
            self.logger.error(f"Cannot cancel policy in status: {policy.status}")
            return False

        # Transition to cancelled status
        success = self.lifecycle.transition_policy(
            policy, PolicyStatus.CANCELLED,
            reason=reason,
            cancellation_date=cancellation_date or datetime.now()
        )

        if success:
            self._update_policy_index(policy)
            self._update_performance_metrics()

        return success

    def get_portfolio_summary(self, portfolio_criteria: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get portfolio summary and performance metrics.

        Args:
            portfolio_criteria: Filter criteria for portfolio

        Returns:
            Portfolio summary with key metrics
        """
        # Filter policies if criteria provided
        if portfolio_criteria:
            policies = self.search_policies(portfolio_criteria)
        else:
            policies = list(self.policies.values())

        # Calculate portfolio metrics
        active_policies = [p for p in policies if p.is_active()]
        total_premium = sum(p.total_premium for p in policies)
        average_premium = total_premium / len(policies) if policies else 0

        # Risk tier distribution
        risk_tiers = {}
        for policy in policies:
            tier = policy.risk_tier
            risk_tiers[tier] = risk_tiers.get(tier, 0) + 1

        # Status distribution
        status_counts = {}
        for policy in policies:
            status = policy.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            'total_policies': len(policies),
            'active_policies': len(active_policies),
            'total_premium': total_premium,
            'average_premium': average_premium,
            'risk_tier_distribution': risk_tiers,
            'status_distribution': status_counts,
            'policies_expiring_soon': self._get_expiring_policies(30),  # Next 30 days
            'last_updated': datetime.now().isoformat()
        }

    def _get_expiring_policies(self, days_ahead: int) -> List[str]:
        """Get list of policies expiring within specified days."""
        now = datetime.now()
        threshold_date = now + timedelta(days=days_ahead)

        expiring_policies = []
        for policy in self.policies.values():
            if policy.expiration_date <= threshold_date and policy.status == PolicyStatus.ACTIVE:
                expiring_policies.append(policy.policy_number)

        return expiring_policies

    def _update_policy_index(self, policy: Policy) -> None:
        """Update policy index for efficient searching."""
        # Index by status
        status_key = policy.status.value
        if status_key not in self.policy_index:
            self.policy_index[status_key] = []
        if policy.policy_id not in self.policy_index[status_key]:
            self.policy_index[status_key].append(policy.policy_id)

        # Index by risk tier
        tier_key = policy.risk_tier
        if tier_key not in self.policy_index:
            self.policy_index[tier_key] = []
        if policy.policy_id not in self.policy_index[tier_key]:
            self.policy_index[tier_key].append(policy.policy_id)

    def _update_performance_metrics(self) -> None:
        """Update performance metrics."""
        policies = list(self.policies.values())

        self.performance_metrics['total_policies'] = len(policies)
        self.performance_metrics['active_policies'] = len([p for p in policies if p.is_active()])
        self.performance_metrics['total_premium'] = sum(p.total_premium for p in policies)
        self.performance_metrics['average_premium'] = (
            self.performance_metrics['total_premium'] / len(policies) if policies else 0
        )

        # Update status distribution
        status_counts = {}
        for policy in policies:
            status = policy.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        self.performance_metrics['policies_by_status'] = status_counts

        # Update risk tier distribution
        tier_counts = {}
        for policy in policies:
            tier = policy.risk_tier
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        self.performance_metrics['policies_by_risk_tier'] = tier_counts

    def export_portfolio(self, format: str = "csv", filename: Optional[str] = None) -> str:
        """
        Export portfolio data to file.

        Args:
            format: Export format ('csv', 'json', 'excel')
            filename: Output filename

        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"portfolio_export_{timestamp}.{format}"

        if format == "csv":
            df = pd.DataFrame([policy.to_dict() for policy in self.policies.values()])
            df.to_csv(filename, index=False)
        elif format == "json":
            data = [policy.to_dict() for policy in self.policies.values()]
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        elif format == "excel":
            df = pd.DataFrame([policy.to_dict() for policy in self.policies.values()])
            df.to_excel(filename, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")

        self.logger.info(f"Portfolio exported to {filename}")
        return filename

    def get_policy_performance(self, policy_id: str) -> Dict[str, Any]:
        """Get performance metrics for a specific policy."""
        if policy_id not in self.policies:
            return {}

        policy = self.policies[policy_id]

        return {
            'policy_id': policy_id,
            'policy_number': policy.policy_number,
            'status': policy.status.value,
            'premium': policy.total_premium,
            'risk_score': policy.risk_score,
            'risk_tier': policy.risk_tier,
            'days_to_expiration': policy.days_to_expiration(),
            'is_active': policy.is_active(),
            'coverage_count': len(policy.coverages),
            'endorsement_count': len(policy.endorsements),
            'last_updated': policy.updated_at.isoformat()
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on policy management system."""
        return {
            'status': 'operational',
            'total_policies': len(self.policies),
            'active_policies': self.performance_metrics['active_policies'],
            'total_premium': self.performance_metrics['total_premium'],
            'timestamp': datetime.now().isoformat()
        }


# Convenience functions
def create_policy_manager(config: Optional[Dict[str, Any]] = None) -> PolicyManager:
    """Create a new policy manager."""
    return PolicyManager(config)

def create_sample_policy() -> Policy:
    """Create a sample policy for testing."""
    policy = Policy(
        policy_id=str(uuid.uuid4()),
        policy_number="SAMPLE001",
        status=PolicyStatus.ACTIVE,
        policyholder_id="sample_holder",
        property_id="sample_property",
        effective_date=datetime.now() - timedelta(days=30),
        expiration_date=datetime.now() + timedelta(days=335),  # 11 months
        term_months=12,
        total_premium=2500.0,
        risk_score=0.4,
        risk_tier="preferred"
    )

    # Add sample coverage
    coverage = Coverage(
        coverage_type=CoverageType.PROPERTY,
        limit=500000,
        deductible=10000,
        premium=2000.0
    )
    policy.add_coverage(coverage)

    return policy
