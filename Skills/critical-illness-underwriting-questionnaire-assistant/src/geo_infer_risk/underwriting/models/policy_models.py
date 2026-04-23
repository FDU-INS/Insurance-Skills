"""
Policy Models: Data structures for insurance policy management.

This module provides comprehensive data models for insurance policies including:
- Policy structure and lifecycle
- Coverage definitions and management
- Endorsements and amendments
- Policy metadata and tracking
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

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

    def calculate_premium_portion(self, total_premium: float) -> float:
        """Calculate the portion of total premium for this coverage."""
        return self.premium if self.premium > 0 else total_premium * 0.1  # Default 10%

    def is_active(self, effective_date: datetime) -> bool:
        """Check if coverage is active on given date."""
        if self.waiting_period_days > 0:
            active_date = effective_date + timedelta(days=self.waiting_period_days)
            return datetime.now() >= active_date
        return True

    def get_coverage_summary(self) -> Dict[str, Any]:
        """Get summary of coverage details."""
        return {
            'type': self.coverage_type.value,
            'limit': self.limit,
            'deductible': self.deductible,
            'premium': self.premium,
            'coinsurance': self.coinsurance,
            'waiting_period_days': self.waiting_period_days,
            'retroactive_date': self.retroactive_date.isoformat() if self.retroactive_date else None,
            'conditions_count': len(self.conditions),
            'exclusions_count': len(self.exclusions)
        }

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

    def is_effective(self) -> bool:
        """Check if endorsement is currently effective."""
        return datetime.now() >= self.effective_date

    def get_endorsement_summary(self) -> Dict[str, Any]:
        """Get summary of endorsement details."""
        return {
            'endorsement_id': self.endorsement_id,
            'type': self.endorsement_type,
            'effective_date': self.effective_date.isoformat(),
            'description': self.description,
            'premium_change': self.premium_change,
            'coverage_changes_count': len(self.coverage_changes),
            'conditions_count': len(self.conditions),
            'is_effective': self.is_effective()
        }

@dataclass
class Exclusion:
    """Policy exclusion or limitation."""
    exclusion_id: str
    exclusion_type: str
    description: str
    applicability: str = "all"  # all, specific_peril, specific_location
    conditions: List[str] = field(default_factory=list)

    def applies_to_peril(self, peril: str) -> bool:
        """Check if exclusion applies to specific peril."""
        return self.applicability in ["all", "specific_peril"] and peril in self.conditions

    def get_exclusion_summary(self) -> Dict[str, Any]:
        """Get summary of exclusion details."""
        return {
            'exclusion_id': self.exclusion_id,
            'type': self.exclusion_type,
            'description': self.description,
            'applicability': self.applicability,
            'conditions_count': len(self.conditions)
        }

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
    exclusions: List[Exclusion] = field(default_factory=list)

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

    def add_exclusion(self, exclusion: Exclusion) -> None:
        """Add exclusion to the policy."""
        self.exclusions.append(exclusion)

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

    def get_coverage_for_peril(self, peril: str) -> List[Coverage]:
        """Get coverages that apply to a specific peril."""
        applicable_coverages = []

        for coverage in self.coverages:
            # Check if peril is covered (simplified logic)
            if coverage.coverage_type.value in ['all_risk', peril.lower()]:
                applicable_coverages.append(coverage)

        return applicable_coverages

    def calculate_policy_value(self) -> float:
        """Calculate total policy value (sum of all coverage limits)."""
        return sum(coverage.limit for coverage in self.coverages)

    def get_policy_summary(self) -> Dict[str, Any]:
        """Get comprehensive policy summary."""
        return {
            'policy_id': self.policy_id,
            'policy_number': self.policy_number,
            'status': self.status.value,
            'policyholder_id': self.policyholder_id,
            'property_id': self.property_id,
            'effective_date': self.effective_date.isoformat(),
            'expiration_date': self.expiration_date.isoformat(),
            'term_months': self.term_months,
            'total_premium': self.total_premium,
            'base_premium': self.base_premium,
            'risk_score': self.risk_score,
            'risk_tier': self.risk_tier,
            'coverage_count': len(self.coverages),
            'endorsement_count': len(self.endorsements),
            'exclusion_count': len(self.exclusions),
            'is_active': self.is_active(),
            'days_to_expiration': self.days_to_expiration(),
            'total_coverage_limit': self.calculate_policy_value(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

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
            'exclusions': [
                {
                    'exclusion_id': exclusion.exclusion_id,
                    'exclusion_type': exclusion.exclusion_type,
                    'description': exclusion.description,
                    'applicability': exclusion.applicability,
                    'conditions': exclusion.conditions
                }
                for exclusion in self.exclusions
            ],
            'metadata': self.metadata
        }
