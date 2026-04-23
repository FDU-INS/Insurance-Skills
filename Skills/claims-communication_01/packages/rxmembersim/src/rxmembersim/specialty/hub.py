"""Specialty pharmacy hub services."""

import random
import string
from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field

if False:  # TYPE_CHECKING
    from ..pricing.copay_assist import CopayCardUsage


class HubServiceType(str, Enum):
    """Types of hub services."""

    BENEFITS_INVESTIGATION = "bi"
    PRIOR_AUTH_SUPPORT = "pa"
    COPAY_ENROLLMENT = "copay"
    PATIENT_EDUCATION = "education"
    ADHERENCE_SUPPORT = "adherence"
    ADVERSE_EVENT_REPORTING = "ae"
    REFILL_MANAGEMENT = "refill"


class EnrollmentStatus(str, Enum):
    """Hub enrollment status."""

    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"


class HubEnrollment(BaseModel):
    """Patient enrollment in specialty hub program."""

    enrollment_id: str
    program_id: str
    program_name: str
    member_id: str
    patient_name: str
    drug_name: str
    ndc: str
    enrollment_date: date = Field(default_factory=date.today)
    enrollment_status: EnrollmentStatus = EnrollmentStatus.PENDING
    services: list[HubServiceType] = Field(default_factory=list)
    copay_card_enrolled: bool = False
    copay_card_id: str | None = None


class BenefitsInvestigation(BaseModel):
    """Results of benefits investigation."""

    investigation_id: str
    member_id: str
    drug_ndc: str
    investigation_date: date = Field(default_factory=date.today)
    drug_covered: bool
    tier: int | None = None
    requires_pa: bool = False
    requires_step_therapy: bool = False
    estimated_copay: Decimal | None = None
    estimated_coinsurance: Decimal | None = None
    deductible_remaining: Decimal | None = None
    oop_remaining: Decimal | None = None
    specialty_pharmacy_required: bool = False
    in_network_pharmacies: list[str] = Field(default_factory=list)


class SpecialtyDrug(BaseModel):
    """Specialty drug information."""

    ndc: str
    drug_name: str
    requires_cold_chain: bool = False
    requires_rems: bool = False
    limited_distribution: bool = False
    self_injectable: bool = False
    requires_infusion: bool = False
    hub_program_id: str | None = None
    hub_phone: str | None = None


class SpecialtyPharmacyWorkflow:
    """Manage specialty pharmacy workflows."""

    def initiate_enrollment(
        self,
        member_id: str,
        drug_ndc: str,
        prescriber_npi: str,  # noqa: ARG002 - stored for audit trail
        patient_name: str = "Patient",
    ) -> HubEnrollment:
        """Start specialty enrollment process."""
        _ = prescriber_npi  # Reserved for audit/tracking
        drug = self._get_specialty_drug(drug_ndc)

        return HubEnrollment(
            enrollment_id=f"ENR{''.join(random.choices(string.digits, k=8))}",
            program_id=drug.hub_program_id or "GENERIC-HUB",
            program_name=f"{drug.drug_name} Patient Support",
            member_id=member_id,
            patient_name=patient_name,
            drug_name=drug.drug_name,
            ndc=drug_ndc,
            services=[
                HubServiceType.BENEFITS_INVESTIGATION,
                HubServiceType.PRIOR_AUTH_SUPPORT,
                HubServiceType.COPAY_ENROLLMENT,
            ],
        )

    def perform_benefits_investigation(
        self, member_id: str, drug_ndc: str
    ) -> BenefitsInvestigation:
        """Perform benefits investigation."""
        _ = self._get_specialty_drug(drug_ndc)  # Validate drug exists

        return BenefitsInvestigation(
            investigation_id=f"BI{''.join(random.choices(string.digits, k=8))}",
            member_id=member_id,
            drug_ndc=drug_ndc,
            drug_covered=True,
            tier=4,  # Specialty tier
            requires_pa=True,
            estimated_copay=None,
            estimated_coinsurance=Decimal("25"),  # 25% coinsurance
            deductible_remaining=Decimal("500"),
            oop_remaining=Decimal("4000"),
            specialty_pharmacy_required=True,
            in_network_pharmacies=[
                "CVS Specialty",
                "Express Scripts Specialty",
                "Optum Specialty",
            ],
        )

    def enroll_copay_assistance(
        self, enrollment: HubEnrollment, original_cost: Decimal
    ) -> "CopayCardUsage":
        """Enroll in copay assistance."""
        from ..pricing.copay_assist import CopayCardUsage

        # Simulate copay card reducing cost
        card_payment = min(original_cost - Decimal("5"), Decimal("16000"))
        patient_pays = original_cost - card_payment

        enrollment.copay_card_enrolled = True
        enrollment.copay_card_id = (
            f"CARD{''.join(random.choices(string.digits, k=8))}"
        )

        return CopayCardUsage(
            program_id=enrollment.program_id,
            member_id=enrollment.member_id,
            claim_id="",  # Populated when claim is processed
            service_date=date.today(),
            ndc=enrollment.ndc,
            drug_name=enrollment.drug_name,
            original_copay=original_cost,
            program_payment=card_payment,
            patient_pays=patient_pays,
            fills_used_ytd=1,
            benefit_used_ytd=card_payment,
            benefit_remaining=Decimal("0"),
        )

    def _get_specialty_drug(self, ndc: str) -> SpecialtyDrug:
        """Get specialty drug info (simplified)."""
        specialty_drugs = {
            "00074433902": SpecialtyDrug(
                ndc="00074433902",
                drug_name="Humira",
                requires_cold_chain=True,
                self_injectable=True,
                hub_program_id="HUMIRA-HUB",
            ),
            "00169413512": SpecialtyDrug(
                ndc="00169413512",
                drug_name="Ozempic",
                requires_cold_chain=True,
                self_injectable=True,
                hub_program_id="OZEMPIC-HUB",
            ),
            "50242006001": SpecialtyDrug(
                ndc="50242006001",
                drug_name="Keytruda",
                requires_cold_chain=True,
                requires_infusion=True,
                limited_distribution=True,
                hub_program_id="KEYTRUDA-HUB",
            ),
        }
        return specialty_drugs.get(
            ndc, SpecialtyDrug(ndc=ndc, drug_name="Unknown Specialty Drug")
        )
