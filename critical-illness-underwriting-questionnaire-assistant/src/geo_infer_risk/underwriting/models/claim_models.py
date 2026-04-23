"""
Claim Models: Data structures for insurance claims management.

This module provides comprehensive data models for insurance claims including:
- Claim structure and lifecycle
- Payment and reserve management
- Claim status tracking
- Claim documentation and notes
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

class ClaimStatus(Enum):
    """Insurance claim status enumeration."""
    REPORTED = "reported"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    DENIED = "denied"
    SETTLED = "settled"
    CLOSED = "closed"
    REOPENED = "reopened"
    INVALID = "invalid"
    ERROR = "error"

class ClaimType(Enum):
    """Insurance claim type enumeration."""
    PROPERTY_DAMAGE = "property_damage"
    LIABILITY = "liability"
    BUSINESS_INTERRUPTION = "business_interruption"
    PERSONAL_INJURY = "personal_injury"
    THEFT = "theft"
    FIRE = "fire"
    FLOOD = "flood"
    EARTHQUAKE = "earthquake"
    HURRICANE = "hurricane"
    OTHER = "other"

class PaymentType(Enum):
    """Insurance payment type enumeration."""
    INDEMNITY = "indemnity"
    EXPENSE = "expense"
    SALVAGE = "salvage"
    SUBROGATION = "subrogation"
    REINSURANCE_RECOVERY = "reinsurance_recovery"

@dataclass
class Reserve:
    """Insurance claim reserve estimate."""
    reserve_id: str
    claim_id: str
    reserve_type: str  # indemnity, expense, legal
    amount: float
    confidence_level: float = 0.8
    calculation_method: str = "expected_value"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None

    def update_amount(self, new_amount: float, reason: str = "") -> None:
        """Update reserve amount."""
        self.amount = new_amount
        self.updated_at = datetime.now()
        if reason:
            self.notes = (self.notes or "") + f"\nUpdated {datetime.now().isoformat()}: {reason}"

    def is_adequate(self, paid_amount: float) -> bool:
        """Check if reserve is adequate for paid amount."""
        return self.amount >= paid_amount

    def get_reserve_summary(self) -> Dict[str, Any]:
        """Get summary of reserve details."""
        return {
            'reserve_id': self.reserve_id,
            'reserve_type': self.reserve_type,
            'amount': self.amount,
            'confidence_level': self.confidence_level,
            'calculation_method': self.calculation_method,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'notes': self.notes
        }

@dataclass
class Payment:
    """Insurance claim payment record."""
    payment_id: str
    claim_id: str
    payment_type: str  # indemnity, expense, salvage
    amount: float
    payment_date: datetime
    payment_method: str = "electronic"
    reference_number: Optional[str] = None
    notes: Optional[str] = None

    def is_valid(self) -> bool:
        """Validate payment record."""
        return (self.amount > 0 and
                self.payment_date <= datetime.now() and
                self.payment_type in ['indemnity', 'expense', 'salvage', 'subrogation'])

    def get_payment_summary(self) -> Dict[str, Any]:
        """Get summary of payment details."""
        return {
            'payment_id': self.payment_id,
            'payment_type': self.payment_type,
            'amount': self.amount,
            'payment_date': self.payment_date.isoformat(),
            'payment_method': self.payment_method,
            'reference_number': self.reference_number,
            'notes': self.notes,
            'is_valid': self.is_valid()
        }

@dataclass
class Claim:
    """Insurance claim data structure."""
    claim_id: str
    policy_id: str
    claim_number: str
    status: ClaimStatus
    claim_type: ClaimType

    # Claim details
    date_of_loss: datetime
    reported_date: datetime = field(default_factory=datetime.now)
    description: str = ""

    # Financial information
    claimed_amount: float = 0.0
    approved_amount: float = 0.0
    paid_amount: float = 0.0

    # Reserves
    reserves: List[Reserve] = field(default_factory=list)

    # Payments
    payments: List[Payment] = field(default_factory=list)

    # Assessment information
    cause_of_loss: str = ""
    adjuster_id: Optional[str] = None
    supervisor_id: Optional[str] = None
    loss_location: Optional[str] = None

    # Documentation
    supporting_documents: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"

    # Error handling
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_reserve(self, reserve: Reserve) -> None:
        """Add reserve estimate to claim."""
        self.reserves.append(reserve)
        self.updated_at = datetime.now()

    def add_payment(self, payment: Payment) -> None:
        """Add payment to claim."""
        if payment.is_valid():
            self.payments.append(payment)
            self.paid_amount += payment.amount
            self.updated_at = datetime.now()
        else:
            self.errors.append(f"Invalid payment: {payment.payment_id}")

    def calculate_total_reserves(self) -> float:
        """Calculate total reserve amount."""
        return sum(reserve.amount for reserve in self.reserves)

    def calculate_outstanding_reserves(self) -> float:
        """Calculate outstanding reserve amount."""
        total_reserves = self.calculate_total_reserves()
        return max(0, total_reserves - self.paid_amount)

    def is_closed(self) -> bool:
        """Check if claim is closed."""
        return self.status in [ClaimStatus.CLOSED, ClaimStatus.DENIED]

    def days_open(self) -> int:
        """Calculate days since claim was reported."""
        return (datetime.now() - self.reported_date).days

    def get_financial_summary(self) -> Dict[str, Any]:
        """Get financial summary of the claim."""
        return {
            'claimed_amount': self.claimed_amount,
            'approved_amount': self.approved_amount,
            'paid_amount': self.paid_amount,
            'total_reserves': self.calculate_total_reserves(),
            'outstanding_reserves': self.calculate_outstanding_reserves(),
            'reserve_adequacy': self.calculate_outstanding_reserves() >= 0,
            'payment_count': len(self.payments)
        }

    def get_claim_summary(self) -> Dict[str, Any]:
        """Get comprehensive claim summary."""
        return {
            'claim_id': self.claim_id,
            'claim_number': self.claim_number,
            'status': self.status.value,
            'claim_type': self.claim_type.value,
            'date_of_loss': self.date_of_loss.isoformat(),
            'reported_date': self.reported_date.isoformat(),
            'days_open': self.days_open(),
            'is_closed': self.is_closed(),
            'financial_summary': self.get_financial_summary(),
            'adjuster_id': self.adjuster_id,
            'supervisor_id': self.supervisor_id,
            'documents_count': len(self.supporting_documents),
            'notes_count': len(self.notes),
            'photos_count': len(self.photos),
            'errors_count': len(self.errors),
            'warnings_count': len(self.warnings)
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert claim to dictionary for serialization."""
        return {
            'claim_id': self.claim_id,
            'policy_id': self.policy_id,
            'claim_number': self.claim_number,
            'status': self.status.value,
            'claim_type': self.claim_type.value,
            'date_of_loss': self.date_of_loss.isoformat(),
            'reported_date': self.reported_date.isoformat(),
            'description': self.description,
            'claimed_amount': self.claimed_amount,
            'approved_amount': self.approved_amount,
            'paid_amount': self.paid_amount,
            'reserves': [
                {
                    'reserve_id': reserve.reserve_id,
                    'reserve_type': reserve.reserve_type,
                    'amount': reserve.amount,
                    'confidence_level': reserve.confidence_level,
                    'calculation_method': reserve.calculation_method,
                    'created_at': reserve.created_at.isoformat(),
                    'updated_at': reserve.updated_at.isoformat(),
                    'notes': reserve.notes
                }
                for reserve in self.reserves
            ],
            'payments': [
                {
                    'payment_id': payment.payment_id,
                    'payment_type': payment.payment_type,
                    'amount': payment.amount,
                    'payment_date': payment.payment_date.isoformat(),
                    'payment_method': payment.payment_method,
                    'reference_number': payment.reference_number,
                    'notes': payment.notes
                }
                for payment in self.payments
            ],
            'cause_of_loss': self.cause_of_loss,
            'adjuster_id': self.adjuster_id,
            'supervisor_id': self.supervisor_id,
            'loss_location': self.loss_location,
            'supporting_documents': self.supporting_documents,
            'notes': self.notes,
            'photos': self.photos,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by,
            'errors': self.errors,
            'warnings': self.warnings
        }

    def validate_claim(self) -> Dict[str, Any]:
        """Validate claim data and return validation results."""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }

        # Validate required fields
        if not self.claim_id:
            validation_result['errors'].append("Claim ID is required")
            validation_result['is_valid'] = False

        if not self.policy_id:
            validation_result['errors'].append("Policy ID is required")
            validation_result['is_valid'] = False

        # Validate amounts
        if self.claimed_amount < 0:
            validation_result['errors'].append("Claimed amount cannot be negative")
            validation_result['is_valid'] = False

        if self.approved_amount < 0:
            validation_result['errors'].append("Approved amount cannot be negative")
            validation_result['is_valid'] = False

        if self.paid_amount < 0:
            validation_result['errors'].append("Paid amount cannot be negative")
            validation_result['is_valid'] = False

        # Validate dates
        if self.date_of_loss > datetime.now():
            validation_result['warnings'].append("Date of loss is in the future")

        if self.reported_date < self.date_of_loss:
            validation_result['errors'].append("Reported date cannot be before date of loss")
            validation_result['is_valid'] = False

        # Validate status consistency
        if self.status == ClaimStatus.APPROVED and self.approved_amount == 0:
            validation_result['warnings'].append("Approved claim has zero approved amount")

        if self.status == ClaimStatus.SETTLED and self.paid_amount == 0:
            validation_result['warnings'].append("Settled claim has zero paid amount")

        return validation_result
