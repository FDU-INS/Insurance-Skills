"""Product-specific event handlers for the journey engine.

This module provides event handlers for each HealthSim product:
- PatientSim: Clinical events (ADT, orders, results)
- MemberSim: Enrollment and claims events
- RxMemberSim: Prescription and fill events
- TrialSim: Clinical trial events

Handlers generate the actual data artifacts when events are executed.
"""

from __future__ import annotations

import hashlib
import random
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any, Callable, Protocol

from healthsim.generation.journey_engine import (
    EventHandler,
    JourneyEngine,
    PatientEventType,
    MemberEventType,
    RxEventType,
    TrialEventType,
    TimelineEvent,
)


# =============================================================================
# Base Handler Infrastructure
# =============================================================================

class BaseEventHandler(ABC):
    """Base class for event handlers with common utilities."""
    
    def __init__(self, seed: int | None = None):
        self.seed = seed
        self._rng = random.Random(seed)
    
    def _generate_id(self, prefix: str, entity_id: str, event_id: str) -> str:
        """Generate a deterministic ID."""
        combined = f"{self.seed or 0}:{entity_id}:{event_id}"
        hash_val = hashlib.md5(combined.encode()).hexdigest()[:8]
        return f"{prefix}-{hash_val.upper()}"
    
    def _generate_uuid(self, entity_id: str, event_id: str) -> str:
        """Generate a deterministic UUID."""
        combined = f"{self.seed or 0}:{entity_id}:{event_id}"
        hash_bytes = hashlib.md5(combined.encode()).digest()
        return str(uuid.UUID(bytes=hash_bytes[:16]))
    
    @abstractmethod
    def handle(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle the event and return results."""
        pass
    
    def __call__(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Make handler callable for EventHandler protocol."""
        return self.handle(entity, event, context)


# =============================================================================
# PatientSim Handlers
# =============================================================================

class PatientSimHandlers:
    """Collection of PatientSim event handlers."""
    
    def __init__(self, seed: int | None = None):
        self.seed = seed
        self._rng = random.Random(seed)
        
        # Standard facility for generated encounters
        self.default_facility = {
            "facility_id": "FAC-001",
            "name": "Community General Hospital",
            "npi": "1234567890",
            "address": {"city": "Austin", "state": "TX", "zip": "78701"}
        }
        
        # Standard provider pool
        self.providers = [
            {"provider_id": "PROV-001", "name": "Dr. Sarah Chen", "npi": "1111111111", "specialty": "Internal Medicine"},
            {"provider_id": "PROV-002", "name": "Dr. Michael Brown", "npi": "2222222222", "specialty": "Family Medicine"},
            {"provider_id": "PROV-003", "name": "Dr. Lisa Rodriguez", "npi": "3333333333", "specialty": "Endocrinology"},
        ]
    
    def _get_entity_id(self, entity: Any) -> str:
        """Extract entity ID."""
        if isinstance(entity, dict):
            return entity.get("patient_id", entity.get("id", "unknown"))
        return getattr(entity, "patient_id", getattr(entity, "id", "unknown"))
    
    def _select_provider(self, specialty: str | None = None) -> dict:
        """Select a provider, optionally by specialty."""
        if specialty:
            matching = [p for p in self.providers if p["specialty"] == specialty]
            if matching:
                return self._rng.choice(matching)
        return self._rng.choice(self.providers)
    
    # -------------------------------------------------------------------------
    # ADT Events
    # -------------------------------------------------------------------------
    
    def handle_admission(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle patient admission event."""
        patient_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        encounter_id = self._generate_id("ENC", patient_id, event.timeline_event_id)
        
        return {
            "encounter_id": encounter_id,
            "patient_id": patient_id,
            "encounter_type": "inpatient",
            "admission_date": event.scheduled_date.isoformat(),
            "admission_type": params.get("admission_type", "elective"),
            "facility": self.default_facility,
            "attending_provider": self._select_provider(),
            "status": "active",
            "adt_type": "A01",  # HL7 ADT message type
        }
    
    def handle_discharge(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle patient discharge event."""
        patient_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        # Link to admission encounter if available
        encounter_id = context.get("active_encounter_id", 
                                   self._generate_id("ENC", patient_id, event.timeline_event_id))
        
        return {
            "encounter_id": encounter_id,
            "patient_id": patient_id,
            "discharge_date": event.scheduled_date.isoformat(),
            "discharge_disposition": params.get("disposition", "home"),
            "discharge_status": params.get("status", "alive"),
            "status": "completed",
            "adt_type": "A03",
        }
    
    # -------------------------------------------------------------------------
    # Clinical Events
    # -------------------------------------------------------------------------
    
    def handle_encounter(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle outpatient encounter event."""
        patient_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        encounter_id = self._generate_id("ENC", patient_id, event.timeline_event_id)
        
        return {
            "encounter_id": encounter_id,
            "patient_id": patient_id,
            "encounter_type": params.get("encounter_type", "outpatient"),
            "encounter_date": event.scheduled_date.isoformat(),
            "reason": params.get("reason", event.event_name),
            "facility": self.default_facility,
            "provider": self._select_provider(params.get("specialty")),
            "status": "completed",
        }
    
    def handle_diagnosis(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle diagnosis event."""
        patient_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        condition_id = self._generate_id("COND", patient_id, event.timeline_event_id)
        
        return {
            "condition_id": condition_id,
            "patient_id": patient_id,
            "icd10": params.get("icd10", "R69"),
            "description": params.get("description", "Illness, unspecified"),
            "onset_date": event.scheduled_date.isoformat(),
            "clinical_status": "active",
            "verification_status": "confirmed",
            "category": params.get("category", "encounter-diagnosis"),
        }
    
    def handle_lab_order(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle laboratory order event."""
        patient_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        order_id = self._generate_id("ORD", patient_id, event.timeline_event_id)
        
        return {
            "order_id": order_id,
            "patient_id": patient_id,
            "order_type": "laboratory",
            "loinc": params.get("loinc", "4548-4"),  # Default: A1C
            "test_name": params.get("test_name", "Hemoglobin A1c"),
            "order_date": event.scheduled_date.isoformat(),
            "ordering_provider": self._select_provider(),
            "status": "ordered",
            "priority": params.get("priority", "routine"),
        }
    
    def handle_lab_result(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle laboratory result event."""
        patient_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        result_id = self._generate_id("RES", patient_id, event.timeline_event_id)
        order_id = params.get("order_id", context.get("last_order_id"))
        
        # Generate realistic value based on LOINC
        loinc = params.get("loinc", "4548-4")
        value, unit = self._generate_lab_value(loinc, entity)
        
        return {
            "result_id": result_id,
            "order_id": order_id,
            "patient_id": patient_id,
            "loinc": loinc,
            "test_name": params.get("test_name", "Lab Test"),
            "value": value,
            "unit": unit,
            "result_date": event.scheduled_date.isoformat(),
            "status": "final",
            "interpretation": self._interpret_lab_value(loinc, value),
        }
    
    def _generate_lab_value(self, loinc: str, entity: Any) -> tuple[float, str]:
        """Generate realistic lab value based on LOINC code."""
        # A1C
        if loinc == "4548-4":
            # Check if entity has diabetes
            has_diabetes = False
            if isinstance(entity, dict):
                conditions = entity.get("conditions", [])
                has_diabetes = any("E11" in str(c) for c in conditions)
            
            if has_diabetes:
                value = self._rng.gauss(7.8, 1.2)
            else:
                value = self._rng.gauss(5.4, 0.3)
            return round(max(4.0, min(14.0, value)), 1), "%"
        
        # Glucose
        elif loinc == "2345-7":
            return round(self._rng.gauss(100, 25), 0), "mg/dL"
        
        # eGFR
        elif loinc == "33914-3":
            return round(self._rng.gauss(75, 20), 0), "mL/min/1.73m2"
        
        # Default
        return round(self._rng.gauss(100, 10), 1), "unit"
    
    def _interpret_lab_value(self, loinc: str, value: float) -> str:
        """Interpret lab value."""
        if loinc == "4548-4":  # A1C
            if value < 5.7:
                return "normal"
            elif value < 6.5:
                return "prediabetic"
            else:
                return "diabetic"
        return "normal"
    
    def handle_medication_order(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle medication order event."""
        patient_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        order_id = self._generate_id("MED", patient_id, event.timeline_event_id)
        
        return {
            "medication_order_id": order_id,
            "patient_id": patient_id,
            "rxnorm": params.get("rxnorm", "860975"),
            "drug_name": params.get("drug_name", "Metformin 500 MG"),
            "order_date": event.scheduled_date.isoformat(),
            "prescriber": self._select_provider(),
            "quantity": params.get("quantity", 30),
            "days_supply": params.get("days_supply", 30),
            "refills": params.get("refills", 3),
            "sig": params.get("sig", "Take 1 tablet by mouth twice daily"),
            "status": "active",
        }
    
    def handle_procedure(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle procedure event."""
        patient_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        procedure_id = self._generate_id("PROC", patient_id, event.timeline_event_id)
        
        return {
            "procedure_id": procedure_id,
            "patient_id": patient_id,
            "cpt": params.get("cpt", "99213"),
            "description": params.get("description", "Office visit, established patient"),
            "procedure_date": event.scheduled_date.isoformat(),
            "performer": self._select_provider(params.get("specialty")),
            "facility": self.default_facility,
            "status": "completed",
        }
    
    def _generate_id(self, prefix: str, patient_id: str, event_id: str) -> str:
        """Generate deterministic ID."""
        combined = f"{self.seed or 0}:{patient_id}:{event_id}"
        hash_val = hashlib.md5(combined.encode()).hexdigest()[:8]
        return f"{prefix}-{hash_val.upper()}"
    
    def register_all(self, engine: JourneyEngine) -> None:
        """Register all PatientSim handlers with an engine."""
        handlers = {
            "admission": self.handle_admission,
            "discharge": self.handle_discharge,
            "encounter": self.handle_encounter,
            "diagnosis": self.handle_diagnosis,
            "lab_order": self.handle_lab_order,
            "lab_result": self.handle_lab_result,
            "medication_order": self.handle_medication_order,
            "procedure": self.handle_procedure,
        }
        
        for event_type, handler in handlers.items():
            engine.register_handler("patientsim", event_type, handler)



# =============================================================================
# MemberSim Handlers
# =============================================================================

class MemberSimHandlers:
    """Collection of MemberSim event handlers."""
    
    def __init__(self, seed: int | None = None):
        self.seed = seed
        self._rng = random.Random(seed)
        
        # Standard plan options
        self.plans = [
            {"plan_id": "PLAN-MA-001", "plan_name": "Medicare Advantage Gold", "plan_type": "MA"},
            {"plan_id": "PLAN-MA-002", "plan_name": "Medicare Advantage Silver", "plan_type": "MA"},
            {"plan_id": "PLAN-COM-001", "plan_name": "Commercial PPO", "plan_type": "Commercial"},
            {"plan_id": "PLAN-MCD-001", "plan_name": "Medicaid Standard", "plan_type": "Medicaid"},
        ]
    
    def _get_entity_id(self, entity: Any) -> str:
        """Extract entity ID."""
        if isinstance(entity, dict):
            return entity.get("member_id", entity.get("id", "unknown"))
        return getattr(entity, "member_id", getattr(entity, "id", "unknown"))
    
    def _generate_id(self, prefix: str, member_id: str, event_id: str) -> str:
        """Generate deterministic ID."""
        combined = f"{self.seed or 0}:{member_id}:{event_id}"
        hash_val = hashlib.md5(combined.encode()).hexdigest()[:8]
        return f"{prefix}-{hash_val.upper()}"
    
    def _select_plan(self, plan_type: str | None = None) -> dict:
        """Select a plan, optionally by type."""
        if plan_type:
            matching = [p for p in self.plans if p["plan_type"] == plan_type]
            if matching:
                return self._rng.choice(matching)
        return self._rng.choice(self.plans)
    
    # -------------------------------------------------------------------------
    # Enrollment Events
    # -------------------------------------------------------------------------
    
    def handle_new_enrollment(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle new enrollment event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        enrollment_id = self._generate_id("ENR", member_id, event.timeline_event_id)
        plan = self._select_plan(params.get("plan_type"))
        
        return {
            "enrollment_id": enrollment_id,
            "member_id": member_id,
            "plan": plan,
            "effective_date": event.scheduled_date.isoformat(),
            "enrollment_type": params.get("enrollment_type", "new"),
            "group_id": params.get("group_id", "GRP-001"),
            "status": "active",
        }
    
    def handle_termination(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle membership termination event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        return {
            "member_id": member_id,
            "termination_date": event.scheduled_date.isoformat(),
            "termination_reason": params.get("reason", "voluntary"),
            "status": "terminated",
        }
    
    def handle_plan_change(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle plan change event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        new_plan = self._select_plan(params.get("new_plan_type"))
        
        return {
            "member_id": member_id,
            "effective_date": event.scheduled_date.isoformat(),
            "old_plan_id": params.get("old_plan_id"),
            "new_plan": new_plan,
            "change_reason": params.get("reason", "open_enrollment"),
        }
    
    # -------------------------------------------------------------------------
    # Claims Events
    # -------------------------------------------------------------------------
    
    def handle_claim_professional(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle professional claim event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        claim_id = self._generate_id("CLM", member_id, event.timeline_event_id)
        
        # Generate realistic amounts
        billed = params.get("billed_amount", round(self._rng.uniform(75, 500), 2))
        allowed = round(billed * self._rng.uniform(0.6, 0.9), 2)
        paid = round(allowed * self._rng.uniform(0.7, 0.9), 2)
        
        return {
            "claim_id": claim_id,
            "member_id": member_id,
            "claim_type": "professional",
            "service_date": event.scheduled_date.isoformat(),
            "provider_npi": params.get("provider_npi", "1234567890"),
            "diagnosis_codes": params.get("diagnosis_codes", ["R69"]),
            "procedure_codes": params.get("procedure_codes", ["99213"]),
            "billed_amount": billed,
            "allowed_amount": allowed,
            "paid_amount": paid,
            "member_responsibility": round(allowed - paid, 2),
            "status": "paid",
        }
    
    def handle_claim_institutional(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle institutional claim event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        claim_id = self._generate_id("CLM", member_id, event.timeline_event_id)
        
        # Institutional claims are larger
        billed = params.get("billed_amount", round(self._rng.uniform(5000, 50000), 2))
        allowed = round(billed * self._rng.uniform(0.5, 0.8), 2)
        paid = round(allowed * self._rng.uniform(0.8, 0.95), 2)
        
        return {
            "claim_id": claim_id,
            "member_id": member_id,
            "claim_type": "institutional",
            "admit_date": params.get("admit_date", event.scheduled_date.isoformat()),
            "discharge_date": params.get("discharge_date"),
            "facility_npi": params.get("facility_npi", "9876543210"),
            "drg": params.get("drg"),
            "diagnosis_codes": params.get("diagnosis_codes", ["R69"]),
            "procedure_codes": params.get("procedure_codes", []),
            "billed_amount": billed,
            "allowed_amount": allowed,
            "paid_amount": paid,
            "status": "paid",
        }
    
    def handle_claim_pharmacy(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle pharmacy claim event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        claim_id = self._generate_id("RX", member_id, event.timeline_event_id)
        
        # Pharmacy claim amounts
        billed = params.get("billed_amount", round(self._rng.uniform(10, 500), 2))
        allowed = round(billed * self._rng.uniform(0.7, 1.0), 2)
        copay = params.get("copay", round(self._rng.choice([5, 10, 15, 25, 50]), 2))
        paid = max(0, allowed - copay)
        
        return {
            "claim_id": claim_id,
            "member_id": member_id,
            "claim_type": "pharmacy",
            "fill_date": event.scheduled_date.isoformat(),
            "pharmacy_npi": params.get("pharmacy_npi", "5555555555"),
            "ndc": params.get("ndc", "00000-0000-00"),
            "drug_name": params.get("drug_name", "Medication"),
            "quantity": params.get("quantity", 30),
            "days_supply": params.get("days_supply", 30),
            "billed_amount": billed,
            "allowed_amount": allowed,
            "copay": copay,
            "paid_amount": round(paid, 2),
            "status": "paid",
        }
    
    # -------------------------------------------------------------------------
    # Quality Events
    # -------------------------------------------------------------------------
    
    def handle_gap_identified(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle quality gap identification event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        gap_id = self._generate_id("GAP", member_id, event.timeline_event_id)
        
        return {
            "gap_id": gap_id,
            "member_id": member_id,
            "measure": params.get("measure", "CDC"),
            "measure_description": params.get("description", "Comprehensive Diabetes Care"),
            "gap_type": params.get("gap_type", "missing_service"),
            "identified_date": event.scheduled_date.isoformat(),
            "due_date": params.get("due_date"),
            "status": "open",
            "priority": params.get("priority", "routine"),
        }
    
    def handle_gap_closed(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle quality gap closure event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        return {
            "gap_id": params.get("gap_id"),
            "member_id": member_id,
            "measure": params.get("measure"),
            "closed_date": event.scheduled_date.isoformat(),
            "closure_reason": params.get("reason", "service_completed"),
            "status": "closed",
        }
    
    def register_all(self, engine: JourneyEngine) -> None:
        """Register all MemberSim handlers with an engine."""
        handlers = {
            "new_enrollment": self.handle_new_enrollment,
            "termination": self.handle_termination,
            "plan_change": self.handle_plan_change,
            "claim_professional": self.handle_claim_professional,
            "claim_institutional": self.handle_claim_institutional,
            "claim_pharmacy": self.handle_claim_pharmacy,
            "gap_identified": self.handle_gap_identified,
            "gap_closed": self.handle_gap_closed,
        }
        
        for event_type, handler in handlers.items():
            engine.register_handler("membersim", event_type, handler)



# =============================================================================
# RxMemberSim Handlers
# =============================================================================

class RxMemberSimHandlers:
    """Collection of RxMemberSim event handlers."""
    
    def __init__(self, seed: int | None = None):
        self.seed = seed
        self._rng = random.Random(seed)
        
        # Common pharmacy chains
        self.pharmacies = [
            {"pharmacy_id": "PHR-001", "name": "CVS Pharmacy", "npi": "1111111111"},
            {"pharmacy_id": "PHR-002", "name": "Walgreens", "npi": "2222222222"},
            {"pharmacy_id": "PHR-003", "name": "Walmart Pharmacy", "npi": "3333333333"},
        ]
    
    def _get_entity_id(self, entity: Any) -> str:
        """Extract entity ID."""
        if isinstance(entity, dict):
            return entity.get("rx_member_id", entity.get("member_id", entity.get("id", "unknown")))
        return getattr(entity, "rx_member_id", getattr(entity, "member_id", "unknown"))
    
    def _generate_id(self, prefix: str, member_id: str, event_id: str) -> str:
        """Generate deterministic ID."""
        combined = f"{self.seed or 0}:{member_id}:{event_id}"
        hash_val = hashlib.md5(combined.encode()).hexdigest()[:8]
        return f"{prefix}-{hash_val.upper()}"
    
    def _select_pharmacy(self) -> dict:
        """Select a pharmacy."""
        return self._rng.choice(self.pharmacies)
    
    # -------------------------------------------------------------------------
    # Prescription Events
    # -------------------------------------------------------------------------
    
    def handle_new_rx(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle new prescription event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        rx_id = self._generate_id("RX", member_id, event.timeline_event_id)
        
        return {
            "rx_id": rx_id,
            "member_id": member_id,
            "rxnorm": params.get("rxnorm", "860975"),
            "drug_name": params.get("drug_name", "Metformin 500 MG"),
            "written_date": event.scheduled_date.isoformat(),
            "prescriber_npi": params.get("prescriber_npi", "1234567890"),
            "quantity_written": params.get("quantity", 30),
            "days_supply": params.get("days_supply", 30),
            "refills_authorized": params.get("refills", 3),
            "refills_remaining": params.get("refills", 3),
            "status": "active",
        }
    
    def handle_fill(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle prescription fill event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        fill_id = self._generate_id("FILL", member_id, event.timeline_event_id)
        pharmacy = self._select_pharmacy()
        
        return {
            "fill_id": fill_id,
            "rx_id": params.get("rx_id"),
            "member_id": member_id,
            "fill_date": event.scheduled_date.isoformat(),
            "pharmacy": pharmacy,
            "ndc": params.get("ndc", "00000-0000-00"),
            "drug_name": params.get("drug_name", "Medication"),
            "quantity_dispensed": params.get("quantity", 30),
            "days_supply": params.get("days_supply", 30),
            "fill_number": params.get("fill_number", 1),
            "status": "dispensed",
        }
    
    def handle_refill(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle prescription refill event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        fill_id = self._generate_id("FILL", member_id, event.timeline_event_id)
        pharmacy = self._select_pharmacy()
        fill_number = params.get("fill_number", 2)
        
        return {
            "fill_id": fill_id,
            "rx_id": params.get("rx_id"),
            "member_id": member_id,
            "fill_date": event.scheduled_date.isoformat(),
            "pharmacy": pharmacy,
            "quantity_dispensed": params.get("quantity", 30),
            "days_supply": params.get("days_supply", 30),
            "fill_number": fill_number,
            "is_refill": True,
            "status": "dispensed",
        }
    
    def handle_reversal(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle claim reversal event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        return {
            "fill_id": params.get("fill_id"),
            "member_id": member_id,
            "reversal_date": event.scheduled_date.isoformat(),
            "reversal_reason": params.get("reason", "returned_to_stock"),
            "status": "reversed",
        }
    
    # -------------------------------------------------------------------------
    # Therapy Events
    # -------------------------------------------------------------------------
    
    def handle_therapy_start(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle therapy start event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        therapy_id = self._generate_id("THR", member_id, event.timeline_event_id)
        
        return {
            "therapy_id": therapy_id,
            "member_id": member_id,
            "therapy_class": params.get("therapy_class", "antidiabetic"),
            "drug_name": params.get("drug_name", "Metformin"),
            "start_date": event.scheduled_date.isoformat(),
            "indication": params.get("indication", "Type 2 Diabetes"),
            "status": "active",
        }
    
    def handle_therapy_change(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle therapy change event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        return {
            "therapy_id": params.get("therapy_id"),
            "member_id": member_id,
            "change_date": event.scheduled_date.isoformat(),
            "change_type": params.get("change_type", "dose_adjustment"),
            "old_drug": params.get("old_drug"),
            "new_drug": params.get("new_drug"),
            "reason": params.get("reason", "therapeutic_optimization"),
        }
    
    def handle_therapy_discontinue(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle therapy discontinuation event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        return {
            "therapy_id": params.get("therapy_id"),
            "member_id": member_id,
            "discontinue_date": event.scheduled_date.isoformat(),
            "reason": params.get("reason", "therapy_complete"),
            "status": "discontinued",
        }
    
    # -------------------------------------------------------------------------
    # Adherence Events
    # -------------------------------------------------------------------------
    
    def handle_adherence_gap(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle adherence gap event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        gap_id = self._generate_id("ADH", member_id, event.timeline_event_id)
        
        return {
            "gap_id": gap_id,
            "member_id": member_id,
            "therapy_class": params.get("therapy_class"),
            "drug_name": params.get("drug_name"),
            "gap_start_date": event.scheduled_date.isoformat(),
            "days_without_medication": params.get("gap_days", 7),
            "status": "open",
        }
    
    def handle_mpr_threshold(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle MPR threshold event."""
        member_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        return {
            "member_id": member_id,
            "therapy_class": params.get("therapy_class"),
            "measurement_date": event.scheduled_date.isoformat(),
            "mpr": params.get("mpr", 0.75),
            "threshold": params.get("threshold", 0.80),
            "is_adherent": params.get("mpr", 0.75) >= params.get("threshold", 0.80),
        }
    
    def register_all(self, engine: JourneyEngine) -> None:
        """Register all RxMemberSim handlers with an engine."""
        handlers = {
            "new_rx": self.handle_new_rx,
            "fill": self.handle_fill,
            "refill": self.handle_refill,
            "reversal": self.handle_reversal,
            "therapy_start": self.handle_therapy_start,
            "therapy_change": self.handle_therapy_change,
            "therapy_discontinue": self.handle_therapy_discontinue,
            "adherence_gap": self.handle_adherence_gap,
            "mpr_threshold": self.handle_mpr_threshold,
        }
        
        for event_type, handler in handlers.items():
            engine.register_handler("rxmembersim", event_type, handler)



# =============================================================================
# TrialSim Handlers
# =============================================================================

class TrialSimHandlers:
    """Collection of TrialSim event handlers."""
    
    def __init__(self, seed: int | None = None):
        self.seed = seed
        self._rng = random.Random(seed)
        
        # Trial sites
        self.sites = [
            {"site_id": "SITE-001", "name": "University Medical Center", "pi": "Dr. James Wilson"},
            {"site_id": "SITE-002", "name": "Community Research Center", "pi": "Dr. Emily Davis"},
            {"site_id": "SITE-003", "name": "Regional Clinical Trials", "pi": "Dr. Robert Kim"},
        ]
        
        # Treatment arms
        self.arms = ["Treatment", "Placebo", "Active Comparator"]
    
    def _get_entity_id(self, entity: Any) -> str:
        """Extract entity ID."""
        if isinstance(entity, dict):
            return entity.get("subject_id", entity.get("id", "unknown"))
        return getattr(entity, "subject_id", getattr(entity, "id", "unknown"))
    
    def _generate_id(self, prefix: str, subject_id: str, event_id: str) -> str:
        """Generate deterministic ID."""
        combined = f"{self.seed or 0}:{subject_id}:{event_id}"
        hash_val = hashlib.md5(combined.encode()).hexdigest()[:8]
        return f"{prefix}-{hash_val.upper()}"
    
    def _select_site(self) -> dict:
        """Select a trial site."""
        return self._rng.choice(self.sites)
    
    # -------------------------------------------------------------------------
    # Enrollment Events
    # -------------------------------------------------------------------------
    
    def handle_screening(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle screening visit event."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        screening_id = self._generate_id("SCR", subject_id, event.timeline_event_id)
        site = self._select_site()
        
        # Screening pass/fail based on probability
        screen_pass = self._rng.random() < params.get("pass_rate", 0.75)
        
        return {
            "screening_id": screening_id,
            "subject_id": subject_id,
            "screening_date": event.scheduled_date.isoformat(),
            "site": site,
            "inclusion_criteria_met": screen_pass,
            "exclusion_criteria_met": not screen_pass if not screen_pass else False,
            "screen_status": "passed" if screen_pass else "failed",
            "screen_failure_reason": None if screen_pass else params.get("failure_reason", "Did not meet inclusion criteria"),
        }
    
    def handle_randomization(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle randomization event."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        randomization_id = self._generate_id("RND", subject_id, event.timeline_event_id)
        
        # Assign to treatment arm
        arm_weights = params.get("arm_weights", {"Treatment": 0.5, "Placebo": 0.5})
        arms = list(arm_weights.keys())
        weights = list(arm_weights.values())
        assigned_arm = self._rng.choices(arms, weights=weights)[0]
        
        return {
            "randomization_id": randomization_id,
            "subject_id": subject_id,
            "randomization_date": event.scheduled_date.isoformat(),
            "treatment_arm": assigned_arm,
            "randomization_number": self._generate_id("R", subject_id, "rand")[-6:],
            "stratification_factors": params.get("strata", {}),
        }
    
    def handle_withdrawal(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle subject withdrawal event."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        return {
            "subject_id": subject_id,
            "withdrawal_date": event.scheduled_date.isoformat(),
            "withdrawal_reason": params.get("reason", "Subject decision"),
            "withdrawal_type": params.get("type", "consent_withdrawn"),
            "last_visit_date": params.get("last_visit"),
        }
    
    # -------------------------------------------------------------------------
    # Visit Events
    # -------------------------------------------------------------------------
    
    def handle_scheduled_visit(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle scheduled study visit."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        visit_id = self._generate_id("VST", subject_id, event.timeline_event_id)
        
        return {
            "visit_id": visit_id,
            "subject_id": subject_id,
            "visit_date": event.scheduled_date.isoformat(),
            "visit_number": params.get("visit_number", 1),
            "visit_name": params.get("visit_name", f"Visit {params.get('visit_number', 1)}"),
            "visit_window_start": params.get("window_start"),
            "visit_window_end": params.get("window_end"),
            "procedures_completed": params.get("procedures", []),
            "status": "completed",
        }
    
    def handle_unscheduled_visit(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle unscheduled study visit."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        visit_id = self._generate_id("USV", subject_id, event.timeline_event_id)
        
        return {
            "visit_id": visit_id,
            "subject_id": subject_id,
            "visit_date": event.scheduled_date.isoformat(),
            "visit_type": "unscheduled",
            "reason": params.get("reason", "AE follow-up"),
            "status": "completed",
        }
    
    # -------------------------------------------------------------------------
    # Safety Events
    # -------------------------------------------------------------------------
    
    def handle_adverse_event(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle adverse event."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        ae_id = self._generate_id("AE", subject_id, event.timeline_event_id)
        
        return {
            "ae_id": ae_id,
            "subject_id": subject_id,
            "onset_date": event.scheduled_date.isoformat(),
            "ae_term": params.get("term", "Headache"),
            "meddra_pt": params.get("meddra_pt"),
            "severity": params.get("severity", "Mild"),
            "serious": False,
            "relationship": params.get("relationship", "Possibly related"),
            "action_taken": params.get("action", "None"),
            "outcome": params.get("outcome", "Recovered"),
            "status": "ongoing" if not params.get("resolved") else "resolved",
        }
    
    def handle_serious_adverse_event(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle serious adverse event."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        sae_id = self._generate_id("SAE", subject_id, event.timeline_event_id)
        
        return {
            "sae_id": sae_id,
            "subject_id": subject_id,
            "onset_date": event.scheduled_date.isoformat(),
            "ae_term": params.get("term", "Hospitalization"),
            "meddra_pt": params.get("meddra_pt"),
            "severity": params.get("severity", "Severe"),
            "serious": True,
            "seriousness_criteria": params.get("criteria", ["hospitalization"]),
            "relationship": params.get("relationship", "Unknown"),
            "action_taken": params.get("action", "Drug interrupted"),
            "outcome": params.get("outcome", "Recovering"),
            "reported_to_sponsor": True,
            "report_date": event.scheduled_date.isoformat(),
        }
    
    # -------------------------------------------------------------------------
    # Protocol Events
    # -------------------------------------------------------------------------
    
    def handle_protocol_deviation(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle protocol deviation."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        pd_id = self._generate_id("PD", subject_id, event.timeline_event_id)
        
        return {
            "deviation_id": pd_id,
            "subject_id": subject_id,
            "deviation_date": event.scheduled_date.isoformat(),
            "category": params.get("category", "Visit window"),
            "description": params.get("description", "Visit outside protocol window"),
            "severity": params.get("severity", "Minor"),
            "corrective_action": params.get("action", "Training provided"),
        }
    
    def handle_dose_modification(
        self,
        entity: Any,
        event: TimelineEvent,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle dose modification."""
        subject_id = self._get_entity_id(entity)
        params = event.result.get("parameters", {}) if event.result else {}
        
        return {
            "subject_id": subject_id,
            "modification_date": event.scheduled_date.isoformat(),
            "modification_type": params.get("type", "dose_reduction"),
            "old_dose": params.get("old_dose"),
            "new_dose": params.get("new_dose"),
            "reason": params.get("reason", "Toxicity"),
        }
    
    def register_all(self, engine: JourneyEngine) -> None:
        """Register all TrialSim handlers with an engine."""
        handlers = {
            "screening": self.handle_screening,
            "randomization": self.handle_randomization,
            "withdrawal": self.handle_withdrawal,
            "scheduled_visit": self.handle_scheduled_visit,
            "unscheduled_visit": self.handle_unscheduled_visit,
            "adverse_event": self.handle_adverse_event,
            "serious_adverse_event": self.handle_serious_adverse_event,
            "protocol_deviation": self.handle_protocol_deviation,
            "dose_modification": self.handle_dose_modification,
        }
        
        for event_type, handler in handlers.items():
            engine.register_handler("trialsim", event_type, handler)


# =============================================================================
# Convenience Functions
# =============================================================================

def create_patientsim_handlers(seed: int | None = None) -> PatientSimHandlers:
    """Create PatientSim handlers."""
    return PatientSimHandlers(seed)


def create_membersim_handlers(seed: int | None = None) -> MemberSimHandlers:
    """Create MemberSim handlers."""
    return MemberSimHandlers(seed)


def create_rxmembersim_handlers(seed: int | None = None) -> RxMemberSimHandlers:
    """Create RxMemberSim handlers."""
    return RxMemberSimHandlers(seed)


def create_trialsim_handlers(seed: int | None = None) -> TrialSimHandlers:
    """Create TrialSim handlers."""
    return TrialSimHandlers(seed)


def register_all_handlers(engine: JourneyEngine, seed: int | None = None) -> None:
    """Register all product handlers with an engine.
    
    Args:
        engine: JourneyEngine to register handlers with
        seed: Random seed for handlers
    """
    PatientSimHandlers(seed).register_all(engine)
    MemberSimHandlers(seed).register_all(engine)
    RxMemberSimHandlers(seed).register_all(engine)
    TrialSimHandlers(seed).register_all(engine)
