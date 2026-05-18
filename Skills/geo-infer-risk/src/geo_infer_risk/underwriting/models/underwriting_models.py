"""
Underwriting Models: Data structures for underwriting case management.

This module provides data models for underwriting operations including:
- Underwriting case management
- Decision structures and criteria
- Guideline and rule management
- Audit and compliance tracking
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

class DecisionStatus(Enum):
    """Underwriting decision status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
    REFERRED = "referred"
    CONDITIONAL = "conditional"
    EXPIRED = "expired"

class GuidelineType(Enum):
    """Underwriting guideline type enumeration."""
    MANDATORY = "mandatory"
    ELIGIBILITY = "eligibility"
    PRICING = "pricing"
    COVERAGE = "coverage"
    EXCLUSION = "exclusion"
    COMPLIANCE = "compliance"
    RISK_MANAGEMENT = "risk_management"

@dataclass
class Decision:
    """Underwriting decision structure."""

    approved: bool
    reason: str
    confidence: float = 0.0
    risk_score: float = 0.0
    rule_score: float = 0.0
    conditions: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    decision_date: datetime = field(default_factory=datetime.now)
    decision_maker: str = "system"

    def is_final(self) -> bool:
        """Check if decision is final."""
        return self.confidence >= 0.8 and self.decision_date is not None

    def requires_review(self) -> bool:
        """Check if decision requires manual review."""
        return self.confidence < 0.7 or len(self.conditions) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert decision to dictionary."""
        return {
            'approved': self.approved,
            'reason': self.reason,
            'confidence': self.confidence,
            'risk_score': self.risk_score,
            'rule_score': self.rule_score,
            'conditions': self.conditions,
            'requirements': self.requirements,
            'recommendations': self.recommendations,
            'decision_date': self.decision_date.isoformat(),
            'decision_maker': self.decision_maker,
            'is_final': self.is_final(),
            'requires_review': self.requires_review()
        }

@dataclass
class Guideline:
    """Underwriting guideline structure."""

    guideline_id: str
    guideline_type: GuidelineType
    name: str
    description: str

    # Rule definition
    rule_expression: str
    rule_parameters: Dict[str, Any] = field(default_factory=dict)

    # Applicability
    applicable_products: List[str] = field(default_factory=list)
    applicable_regions: List[str] = field(default_factory=list)
    applicable_risk_tiers: List[str] = field(default_factory=list)

    # Metadata
    effective_date: datetime = field(default_factory=datetime.now)
    expiration_date: Optional[datetime] = None
    version: str = "1.0"
    created_by: str = "system"
    approved_by: Optional[str] = None

    # Status
    is_active: bool = True
    priority: int = 1

    def is_applicable(self, product: str, region: str, risk_tier: str) -> bool:
        """Check if guideline is applicable."""
        return (
            self.is_active and
            (not self.applicable_products or product in self.applicable_products) and
            (not self.applicable_regions or region in self.applicable_regions) and
            (not self.applicable_risk_tiers or risk_tier in self.applicable_risk_tiers)
        )

    def is_effective(self) -> bool:
        """Check if guideline is currently effective."""
        now = datetime.now()
        return (
            self.is_active and
            self.effective_date <= now and
            (self.expiration_date is None or self.expiration_date >= now)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert guideline to dictionary."""
        return {
            'guideline_id': self.guideline_id,
            'guideline_type': self.guideline_type.value,
            'name': self.name,
            'description': self.description,
            'rule_expression': self.rule_expression,
            'rule_parameters': self.rule_parameters,
            'applicable_products': self.applicable_products,
            'applicable_regions': self.applicable_regions,
            'applicable_risk_tiers': self.applicable_risk_tiers,
            'effective_date': self.effective_date.isoformat(),
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'version': self.version,
            'created_by': self.created_by,
            'approved_by': self.approved_by,
            'is_active': self.is_active,
            'priority': self.priority,
            'is_applicable': self.is_applicable("default", "default", "standard"),
            'is_effective': self.is_effective()
        }

@dataclass
class UnderwritingCase:
    """Underwriting case structure."""

    case_id: str
    application_data: Dict[str, Any]
    status: str = "pending"

    # Assessment results
    risk_assessment: Optional[Dict[str, Any]] = None
    rule_evaluation: Optional[Dict[str, Any]] = None

    # Financial information
    premium: float = 0.0

    # Decision
    decision: Optional[Decision] = None

    # Policy (if approved)
    policy: Optional[Dict[str, Any]] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    assigned_to: Optional[str] = None
    priority: str = "normal"

    # Error handling
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None

    def is_completed(self) -> bool:
        """Check if case is completed."""
        return self.completed_at is not None

    def days_open(self) -> int:
        """Calculate days since case was created."""
        now = datetime.now()
        if self.completed_at:
            return (self.completed_at - self.created_at).days
        return (now - self.created_at).days

    def requires_attention(self) -> bool:
        """Check if case requires attention."""
        return (
            self.status in ["pending", "in_review"] and
            self.days_open() > 2  # Cases open > 2 days need attention
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert underwriting case to dictionary."""
        return {
            'case_id': self.case_id,
            'application_data': self.application_data,
            'status': self.status,
            'risk_assessment': self.risk_assessment,
            'rule_evaluation': self.rule_evaluation,
            'premium': self.premium,
            'decision': self.decision.to_dict() if self.decision else None,
            'policy': self.policy,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'assigned_to': self.assigned_to,
            'priority': self.priority,
            'error_message': self.error_message,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_completed': self.is_completed(),
            'days_open': self.days_open(),
            'requires_attention': self.requires_attention()
        }

@dataclass
class AuditTrail:
    """Audit trail for underwriting operations."""

    audit_id: str
    case_id: str
    action: str
    performed_by: str
    timestamp: datetime = field(default_factory=datetime.now)

    # Action details
    old_values: Dict[str, Any] = field(default_factory=dict)
    new_values: Dict[str, Any] = field(default_factory=dict)
    reason: str = ""

    # Context
    system_context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert audit trail to dictionary."""
        return {
            'audit_id': self.audit_id,
            'case_id': self.case_id,
            'action': self.action,
            'performed_by': self.performed_by,
            'timestamp': self.timestamp.isoformat(),
            'old_values': self.old_values,
            'new_values': self.new_values,
            'reason': self.reason,
            'system_context': self.system_context
        }

@dataclass
class ComplianceCheck:
    """Compliance check result."""

    check_id: str
    check_type: str
    regulation: str
    requirement: str
    status: str  # passed, failed, warning, not_applicable
    details: str = ""
    evidence: List[str] = field(default_factory=list)
    checked_at: datetime = field(default_factory=datetime.now)

    def is_compliant(self) -> bool:
        """Check if compliance check passed."""
        return self.status in ["passed", "not_applicable"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert compliance check to dictionary."""
        return {
            'check_id': self.check_id,
            'check_type': self.check_type,
            'regulation': self.regulation,
            'requirement': self.requirement,
            'status': self.status,
            'details': self.details,
            'evidence': self.evidence,
            'checked_at': self.checked_at.isoformat(),
            'is_compliant': self.is_compliant()
        }

@dataclass
class UnderwritingQueue:
    """Underwriting queue management."""

    queue_id: str
    queue_type: str  # standard, priority, specialist, manual_review
    max_concurrent: int = 10
    priority_levels: List[str] = field(default_factory=lambda: ["low", "normal", "high", "urgent"])

    # Queue statistics
    total_pending: int = 0
    average_wait_time: float = 0.0
    longest_wait_time: float = 0.0

    def add_to_queue(self, case_id: str, priority: str = "normal") -> bool:
        """Add case to queue."""
        if priority not in self.priority_levels:
            return False

        self.total_pending += 1
        # Update wait time statistics (simplified)
        self.average_wait_time = (self.average_wait_time * (self.total_pending - 1) + 0.0) / self.total_pending

        return True

    def remove_from_queue(self, case_id: str) -> bool:
        """Remove case from queue."""
        if self.total_pending > 0:
            self.total_pending -= 1
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert queue to dictionary."""
        return {
            'queue_id': self.queue_id,
            'queue_type': self.queue_type,
            'max_concurrent': self.max_concurrent,
            'priority_levels': self.priority_levels,
            'total_pending': self.total_pending,
            'average_wait_time': self.average_wait_time,
            'longest_wait_time': self.longest_wait_time
        }
