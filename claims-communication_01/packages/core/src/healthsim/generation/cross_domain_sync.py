"""Cross-domain synchronization for multi-product generation.

This module provides coordination between HealthSim products to ensure
consistent entity linking, event correlation, and data integrity.

Key capabilities:
1. Identity Correlation - Same person across products (Patient/Member/Subject)
2. Event Triggers - Encounters generate claims, prescriptions generate fills
3. Provider Assignment - Consistent NPI assignment across products
4. Validation - Cross-product consistency checks
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import Any, Callable, Protocol
from uuid import uuid4

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ProductType(str, Enum):
    """HealthSim product types."""
    PATIENTSIM = "patientsim"
    MEMBERSIM = "membersim"
    RXMEMBERSIM = "rxmembersim"
    TRIALSIM = "trialsim"
    NETWORKSIM = "networksim"
    POPULATIONSIM = "populationsim"


class TriggerType(str, Enum):
    """Cross-product event trigger types."""
    ENCOUNTER_TO_CLAIM = "encounter_to_claim"
    PRESCRIPTION_TO_FILL = "prescription_to_fill"
    ADMISSION_TO_FACILITY_CLAIM = "admission_to_facility_claim"
    LAB_ORDER_TO_CLAIM_LINE = "lab_order_to_claim_line"
    TRIAL_VISIT_TO_ENCOUNTER = "trial_visit_to_encounter"


class CorrelatorType(str, Enum):
    """Identity correlation types."""
    SSN = "ssn"
    DOB = "dob"
    MRN = "mrn"
    MEMBER_ID = "member_id"
    PATIENT_REF = "patient_ref"
    GENERATED_UUID = "generated_uuid"


# =============================================================================
# Identity Correlation
# =============================================================================

class PersonIdentity(BaseModel):
    """Core person identity shared across products.
    
    This is the "master" identity record that links entities
    across PatientSim, MemberSim, RxMemberSim, and TrialSim.
    """
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    
    # Universal correlators
    ssn_hash: str | None = None  # Hashed for privacy
    date_of_birth: date | None = None
    gender: str | None = None
    
    # Name components (for fuzzy matching)
    first_name: str | None = None
    last_name: str | None = None
    
    # Product-specific IDs
    patient_id: str | None = None  # PatientSim
    member_id: str | None = None   # MemberSim
    rx_member_id: str | None = None  # RxMemberSim
    subject_id: str | None = None  # TrialSim
    
    def to_correlator_dict(self) -> dict[str, Any]:
        """Get correlators for matching."""
        return {
            "correlation_id": self.correlation_id,
            "ssn_hash": self.ssn_hash,
            "dob": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender,
            "name": f"{self.last_name},{self.first_name}".upper() if self.last_name else None,
        }


class IdentityRegistry:
    """Registry for cross-product identity correlation.
    
    Maintains a mapping of person identities across products,
    enabling consistent linking when generating related data.
    """
    
    def __init__(self):
        self._identities: dict[str, PersonIdentity] = {}
        self._product_indexes: dict[ProductType, dict[str, str]] = {
            p: {} for p in ProductType
        }
    
    def register(self, identity: PersonIdentity) -> str:
        """Register a person identity.
        
        Args:
            identity: Person identity to register
            
        Returns:
            Correlation ID
        """
        self._identities[identity.correlation_id] = identity
        
        # Index by product IDs
        if identity.patient_id:
            self._product_indexes[ProductType.PATIENTSIM][identity.patient_id] = identity.correlation_id
        if identity.member_id:
            self._product_indexes[ProductType.MEMBERSIM][identity.member_id] = identity.correlation_id
        if identity.rx_member_id:
            self._product_indexes[ProductType.RXMEMBERSIM][identity.rx_member_id] = identity.correlation_id
        if identity.subject_id:
            self._product_indexes[ProductType.TRIALSIM][identity.subject_id] = identity.correlation_id
        
        return identity.correlation_id
    
    def get_by_correlation_id(self, correlation_id: str) -> PersonIdentity | None:
        """Get identity by correlation ID."""
        return self._identities.get(correlation_id)
    
    def get_by_product_id(
        self,
        product: ProductType,
        product_id: str
    ) -> PersonIdentity | None:
        """Get identity by product-specific ID."""
        correlation_id = self._product_indexes.get(product, {}).get(product_id)
        if correlation_id:
            return self._identities.get(correlation_id)
        return None
    
    def link_product_id(
        self,
        correlation_id: str,
        product: ProductType,
        product_id: str
    ) -> bool:
        """Link a product ID to an existing identity.
        
        Args:
            correlation_id: Existing correlation ID
            product: Target product
            product_id: Product-specific ID
            
        Returns:
            True if linked successfully
        """
        identity = self._identities.get(correlation_id)
        if not identity:
            return False
        
        # Update identity
        if product == ProductType.PATIENTSIM:
            identity.patient_id = product_id
        elif product == ProductType.MEMBERSIM:
            identity.member_id = product_id
        elif product == ProductType.RXMEMBERSIM:
            identity.rx_member_id = product_id
        elif product == ProductType.TRIALSIM:
            identity.subject_id = product_id
        
        # Update index
        self._product_indexes[product][product_id] = correlation_id
        
        return True
    
    def find_matches(
        self,
        correlators: dict[str, Any],
        min_confidence: float = 0.8
    ) -> list[tuple[PersonIdentity, float]]:
        """Find matching identities by correlators.
        
        Args:
            correlators: Dict of correlator values
            min_confidence: Minimum match confidence (0-1)
            
        Returns:
            List of (identity, confidence) tuples
        """
        matches = []
        
        for identity in self._identities.values():
            score = self._calculate_match_score(identity, correlators)
            if score >= min_confidence:
                matches.append((identity, score))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def _calculate_match_score(
        self,
        identity: PersonIdentity,
        correlators: dict[str, Any]
    ) -> float:
        """Calculate match confidence score."""
        total_weight = 0.0
        matched_weight = 0.0
        
        # SSN hash - highest weight
        if correlators.get("ssn_hash") and identity.ssn_hash:
            total_weight += 1.0
            if correlators["ssn_hash"] == identity.ssn_hash:
                matched_weight += 1.0
        
        # DOB - high weight
        if correlators.get("dob") and identity.date_of_birth:
            total_weight += 0.5
            if correlators["dob"] == identity.date_of_birth.isoformat():
                matched_weight += 0.5
        
        # Gender - low weight
        if correlators.get("gender") and identity.gender:
            total_weight += 0.1
            if correlators["gender"] == identity.gender:
                matched_weight += 0.1
        
        # Name - medium weight
        if correlators.get("name") and identity.last_name:
            total_weight += 0.3
            identity_name = f"{identity.last_name},{identity.first_name}".upper()
            if correlators["name"] == identity_name:
                matched_weight += 0.3
        
        if total_weight == 0:
            return 0.0
        
        return matched_weight / total_weight
    
    def get_all(self) -> list[PersonIdentity]:
        """Get all registered identities."""
        return list(self._identities.values())
    
    def count(self) -> int:
        """Get count of registered identities."""
        return len(self._identities)


# =============================================================================
# Event Triggers
# =============================================================================

@dataclass
class TriggerSpec:
    """Specification for a cross-product trigger."""
    trigger_type: TriggerType
    source_product: ProductType
    target_product: ProductType
    source_event: str  # e.g., "encounter", "prescription"
    target_event: str  # e.g., "claim", "fill"
    field_mappings: dict[str, str] = field(default_factory=dict)
    delay_days: tuple[int, int] = (0, 3)  # (min, max) delay
    enabled: bool = True


@dataclass
class TriggerResult:
    """Result of trigger execution."""
    trigger_type: TriggerType
    source_id: str
    target_id: str | None
    success: bool
    message: str = ""
    generated_data: dict[str, Any] = field(default_factory=dict)


class TriggerHandler(Protocol):
    """Protocol for product-specific trigger handlers."""
    
    def handle(
        self,
        source_event: dict[str, Any],
        trigger_spec: TriggerSpec,
        context: dict[str, Any]
    ) -> TriggerResult:
        """Handle a trigger and generate target data."""
        ...


class TriggerRegistry:
    """Registry for cross-product trigger handlers."""
    
    def __init__(self):
        self._handlers: dict[TriggerType, TriggerHandler] = {}
        self._specs: dict[TriggerType, TriggerSpec] = {}
    
    def register_spec(self, spec: TriggerSpec) -> None:
        """Register a trigger specification."""
        self._specs[spec.trigger_type] = spec
    
    def register_handler(
        self,
        trigger_type: TriggerType,
        handler: TriggerHandler
    ) -> None:
        """Register a handler for a trigger type."""
        self._handlers[trigger_type] = handler
    
    def get_spec(self, trigger_type: TriggerType) -> TriggerSpec | None:
        """Get trigger specification."""
        return self._specs.get(trigger_type)
    
    def get_handler(self, trigger_type: TriggerType) -> TriggerHandler | None:
        """Get trigger handler."""
        return self._handlers.get(trigger_type)
    
    def fire(
        self,
        trigger_type: TriggerType,
        source_event: dict[str, Any],
        context: dict[str, Any] | None = None
    ) -> TriggerResult:
        """Fire a trigger and execute its handler.
        
        Args:
            trigger_type: Type of trigger to fire
            source_event: Source event data
            context: Additional context
            
        Returns:
            TriggerResult with outcome
        """
        spec = self._specs.get(trigger_type)
        handler = self._handlers.get(trigger_type)
        
        if not spec:
            return TriggerResult(
                trigger_type=trigger_type,
                source_id=source_event.get("id", "unknown"),
                target_id=None,
                success=False,
                message=f"No spec registered for {trigger_type}"
            )
        
        if not spec.enabled:
            return TriggerResult(
                trigger_type=trigger_type,
                source_id=source_event.get("id", "unknown"),
                target_id=None,
                success=False,
                message=f"Trigger {trigger_type} is disabled"
            )
        
        if not handler:
            return TriggerResult(
                trigger_type=trigger_type,
                source_id=source_event.get("id", "unknown"),
                target_id=None,
                success=False,
                message=f"No handler registered for {trigger_type}"
            )
        
        return handler.handle(source_event, spec, context or {})


# =============================================================================
# Cross-Domain Sync Coordinator
# =============================================================================

@dataclass
class SyncConfig:
    """Configuration for cross-domain sync."""
    auto_generate_claims: bool = True
    auto_generate_fills: bool = True
    claim_delay_days: tuple[int, int] = (0, 3)
    fill_delay_days: tuple[int, int] = (0, 3)
    refill_window_days: int = 7
    pcp_sticky_assignment: bool = True
    prefer_real_npis: bool = True


@dataclass
class SyncReport:
    """Report from cross-domain sync operation."""
    products: list[ProductType]
    identities_correlated: int
    triggers_fired: int
    triggers_succeeded: int
    triggers_failed: int
    validation_passed: bool
    validation_errors: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)
    
    def to_formatted_string(self) -> str:
        """Format report for display."""
        lines = [
            "═" * 67,
            "                    CROSS-DOMAIN SYNC REPORT",
            "═" * 67,
            "",
            f"Products: {', '.join(p.value for p in self.products)}",
            "",
            "IDENTITY CORRELATION",
            "─" * 67,
            f"Identities correlated: {self.identities_correlated}",
            "",
            "EVENT SYNCHRONIZATION",
            "─" * 67,
            f"Triggers fired: {self.triggers_fired}",
            f"Succeeded: {self.triggers_succeeded}",
            f"Failed: {self.triggers_failed}",
            "",
            "VALIDATION",
            "─" * 67,
            f"Status: {'✓ Pass' if self.validation_passed else '✗ Fail'}",
        ]
        
        if self.validation_warnings:
            lines.append(f"Warnings: {len(self.validation_warnings)}")
            for w in self.validation_warnings[:5]:
                lines.append(f"  - {w}")
        
        if self.validation_errors:
            lines.append(f"Errors: {len(self.validation_errors)}")
            for e in self.validation_errors[:5]:
                lines.append(f"  - {e}")
        
        lines.append("")
        lines.append("═" * 67)
        
        return "\n".join(lines)


class CrossDomainSync:
    """Coordinator for cross-product data synchronization.
    
    This class manages:
    - Identity correlation across products
    - Event triggers (encounter → claim, prescription → fill)
    - Provider assignment consistency
    - Cross-product validation
    """
    
    def __init__(
        self,
        config: SyncConfig | None = None,
        seed: int | None = None
    ):
        """Initialize cross-domain sync.
        
        Args:
            config: Sync configuration
            seed: Random seed for reproducibility
        """
        self.config = config or SyncConfig()
        self.seed = seed
        
        self.identity_registry = IdentityRegistry()
        self.trigger_registry = TriggerRegistry()
        
        self._setup_default_triggers()
    
    def _setup_default_triggers(self) -> None:
        """Set up default trigger specifications."""
        # Encounter → Claim
        self.trigger_registry.register_spec(TriggerSpec(
            trigger_type=TriggerType.ENCOUNTER_TO_CLAIM,
            source_product=ProductType.PATIENTSIM,
            target_product=ProductType.MEMBERSIM,
            source_event="encounter",
            target_event="claim",
            field_mappings={
                "encounter.service_date": "claim.service_date",
                "encounter.provider_npi": "claim.billing_npi",
                "encounter.diagnoses": "claim.diagnosis_codes",
                "encounter.procedures": "claim.procedure_codes",
            },
            delay_days=self.config.claim_delay_days,
            enabled=self.config.auto_generate_claims,
        ))
        
        # Prescription → Fill
        self.trigger_registry.register_spec(TriggerSpec(
            trigger_type=TriggerType.PRESCRIPTION_TO_FILL,
            source_product=ProductType.PATIENTSIM,
            target_product=ProductType.RXMEMBERSIM,
            source_event="prescription",
            target_event="fill",
            field_mappings={
                "prescription.ndc": "fill.ndc",
                "prescription.quantity": "fill.quantity",
                "prescription.days_supply": "fill.days_supply",
                "prescription.prescriber_npi": "fill.prescriber_npi",
            },
            delay_days=self.config.fill_delay_days,
            enabled=self.config.auto_generate_fills,
        ))
        
        # Admission → Facility Claim
        self.trigger_registry.register_spec(TriggerSpec(
            trigger_type=TriggerType.ADMISSION_TO_FACILITY_CLAIM,
            source_product=ProductType.PATIENTSIM,
            target_product=ProductType.MEMBERSIM,
            source_event="admission",
            target_event="facility_claim",
            field_mappings={
                "admission.admit_date": "claim.admit_date",
                "admission.discharge_date": "claim.discharge_date",
                "admission.facility_npi": "claim.facility_npi",
                "admission.drg": "claim.drg_code",
            },
            delay_days=(1, 5),
            enabled=self.config.auto_generate_claims,
        ))
    
    def create_linked_identity(
        self,
        products: list[ProductType],
        demographics: dict[str, Any],
        seed: int | None = None
    ) -> PersonIdentity:
        """Create a person identity linked across products.
        
        Args:
            products: Products to generate IDs for
            demographics: Person demographics
            seed: Seed for ID generation
            
        Returns:
            PersonIdentity with linked product IDs
        """
        import random
        rng = random.Random(seed or self.seed)
        
        # Generate correlation ID
        correlation_id = str(uuid4())
        
        # Hash SSN if provided
        ssn_hash = None
        if demographics.get("ssn"):
            ssn_hash = hashlib.sha256(
                demographics["ssn"].encode()
            ).hexdigest()[:16]
        
        identity = PersonIdentity(
            correlation_id=correlation_id,
            ssn_hash=ssn_hash,
            date_of_birth=demographics.get("date_of_birth"),
            gender=demographics.get("gender"),
            first_name=demographics.get("first_name"),
            last_name=demographics.get("last_name"),
        )
        
        # Generate product-specific IDs
        if ProductType.PATIENTSIM in products:
            identity.patient_id = f"PAT-{rng.randint(10000000, 99999999)}"
        
        if ProductType.MEMBERSIM in products:
            identity.member_id = f"MEM-{rng.randint(10000000, 99999999)}"
        
        if ProductType.RXMEMBERSIM in products:
            identity.rx_member_id = f"RXM-{rng.randint(10000000, 99999999)}"
        
        if ProductType.TRIALSIM in products:
            identity.subject_id = f"SUBJ-{rng.randint(10000000, 99999999)}"
        
        self.identity_registry.register(identity)
        
        return identity
    
    def fire_trigger(
        self,
        trigger_type: TriggerType,
        source_event: dict[str, Any],
        context: dict[str, Any] | None = None
    ) -> TriggerResult:
        """Fire a cross-product trigger.
        
        Args:
            trigger_type: Type of trigger
            source_event: Source event data
            context: Additional context
            
        Returns:
            TriggerResult
        """
        return self.trigger_registry.fire(trigger_type, source_event, context)
    
    def validate(
        self,
        entities: dict[ProductType, list[Any]]
    ) -> tuple[bool, list[str], list[str]]:
        """Validate cross-product consistency.
        
        Args:
            entities: Dict mapping products to entity lists
            
        Returns:
            Tuple of (passed, errors, warnings)
        """
        errors = []
        warnings = []
        
        # Check identity correlation
        for product, entity_list in entities.items():
            for entity in entity_list:
                entity_id = self._get_entity_id(entity, product)
                if entity_id:
                    identity = self.identity_registry.get_by_product_id(
                        product, entity_id
                    )
                    if not identity:
                        warnings.append(
                            f"Entity {entity_id} in {product.value} "
                            "not in identity registry"
                        )
        
        # Check date consistency (claims shouldn't precede encounters)
        if (ProductType.PATIENTSIM in entities and 
            ProductType.MEMBERSIM in entities):
            # This would require more complex matching logic
            pass
        
        passed = len(errors) == 0
        return passed, errors, warnings
    
    def _get_entity_id(
        self,
        entity: Any,
        product: ProductType
    ) -> str | None:
        """Extract entity ID based on product type."""
        id_fields = {
            ProductType.PATIENTSIM: ["patient_id", "id"],
            ProductType.MEMBERSIM: ["member_id", "id"],
            ProductType.RXMEMBERSIM: ["rx_member_id", "member_id", "id"],
            ProductType.TRIALSIM: ["subject_id", "id"],
        }
        
        fields = id_fields.get(product, ["id"])
        
        for field_name in fields:
            if hasattr(entity, field_name):
                return str(getattr(entity, field_name))
            if isinstance(entity, dict) and field_name in entity:
                return str(entity[field_name])
        
        return None
    
    def get_sync_report(
        self,
        entities: dict[ProductType, list[Any]] | None = None,
        triggers_fired: list[TriggerResult] | None = None
    ) -> SyncReport:
        """Generate a sync report.
        
        Args:
            entities: Entities to validate (optional)
            triggers_fired: Results from fired triggers (optional)
            
        Returns:
            SyncReport
        """
        products = list(entities.keys()) if entities else []
        
        # Count trigger results
        triggers_fired = triggers_fired or []
        succeeded = sum(1 for t in triggers_fired if t.success)
        failed = len(triggers_fired) - succeeded
        
        # Validate if entities provided
        passed, errors, warnings = True, [], []
        if entities:
            passed, errors, warnings = self.validate(entities)
        
        return SyncReport(
            products=products,
            identities_correlated=self.identity_registry.count(),
            triggers_fired=len(triggers_fired),
            triggers_succeeded=succeeded,
            triggers_failed=failed,
            validation_passed=passed,
            validation_errors=errors,
            validation_warnings=warnings,
        )


# =============================================================================
# Convenience Functions
# =============================================================================

def create_cross_domain_sync(
    config: SyncConfig | None = None,
    seed: int | None = None
) -> CrossDomainSync:
    """Create a cross-domain sync coordinator.
    
    Args:
        config: Sync configuration
        seed: Random seed
        
    Returns:
        Configured CrossDomainSync instance
    """
    return CrossDomainSync(config=config, seed=seed)


def hash_ssn(ssn: str) -> str:
    """Hash an SSN for privacy-safe correlation.
    
    Args:
        ssn: Social security number
        
    Returns:
        Hashed value
    """
    # Remove non-digits
    digits = "".join(c for c in ssn if c.isdigit())
    return hashlib.sha256(digits.encode()).hexdigest()[:16]
