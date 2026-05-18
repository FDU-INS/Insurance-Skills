"""Claim adjudication engine."""
import random
from dataclasses import dataclass
from decimal import Decimal

from ..core.member import RxMember
from ..formulary.formulary import Formulary, FormularyStatus
from .claim import PharmacyClaim
from .response import ClaimResponse, RejectCode


@dataclass
class EligibilityResult:
    """Result of eligibility check."""

    eligible: bool
    reject_codes: list[RejectCode]


@dataclass
class PricingResult:
    """Result of pricing calculation."""

    ingredient_cost: Decimal
    dispensing_fee: Decimal
    plan_pays: Decimal
    patient_pays: Decimal
    copay: Decimal
    deductible_applied: Decimal


class AdjudicationEngine:
    """Process pharmacy claims."""

    def __init__(self, formulary: Formulary | None = None):
        self.formulary = formulary or Formulary(
            formulary_id="DEFAULT",
            name="Default Formulary",
            effective_date="2025-01-01",
        )

    def adjudicate(self, claim: PharmacyClaim, member: RxMember) -> ClaimResponse:
        """Adjudicate a pharmacy claim."""
        # Check eligibility
        eligibility = self._check_eligibility(claim, member)
        if not eligibility.eligible:
            return self._create_rejection(claim, eligibility.reject_codes)

        # Check formulary
        formulary_status = self.formulary.check_coverage(claim.ndc)
        if not formulary_status.covered:
            return self._create_rejection(
                claim,
                [RejectCode(code="70", description="Product/Service Not Covered")],
            )

        # Check PA requirement
        if formulary_status.requires_pa and not claim.prior_auth_number:
            return self._create_rejection(
                claim,
                [RejectCode(code="75", description="Prior Authorization Required")],
            )

        # Calculate pricing
        pricing = self._calculate_pricing(claim, member, formulary_status)

        return ClaimResponse(
            claim_id=claim.claim_id,
            transaction_response_status="A",
            response_status="P",
            authorization_number=self._generate_auth_number(),
            ingredient_cost_paid=pricing.ingredient_cost,
            dispensing_fee_paid=pricing.dispensing_fee,
            total_amount_paid=pricing.plan_pays,
            patient_pay_amount=pricing.patient_pays,
            copay_amount=pricing.copay,
            deductible_amount=pricing.deductible_applied,
            remaining_deductible=member.accumulators.deductible_remaining
            - pricing.deductible_applied,
            remaining_oop=member.accumulators.oop_remaining - pricing.patient_pays,
        )

    def _check_eligibility(
        self, claim: PharmacyClaim, member: RxMember
    ) -> EligibilityResult:
        """Check member eligibility."""
        reject_codes: list[RejectCode] = []

        # Check if member is active
        if member.termination_date and claim.service_date > member.termination_date:
            reject_codes.append(
                RejectCode(code="65", description="Patient Not Covered")
            )

        # Check if service date is within coverage period
        if claim.service_date < member.effective_date:
            reject_codes.append(
                RejectCode(code="65", description="Patient Not Covered")
            )

        # Check BIN/PCN/Group match
        if claim.bin != member.bin:
            reject_codes.append(
                RejectCode(code="25", description="Missing/Invalid BIN Number")
            )
        if claim.pcn != member.pcn:
            reject_codes.append(
                RejectCode(code="26", description="Missing/Invalid PCN")
            )
        if claim.group_number != member.group_number:
            reject_codes.append(
                RejectCode(code="64", description="Invalid Group ID")
            )

        return EligibilityResult(
            eligible=len(reject_codes) == 0, reject_codes=reject_codes
        )

    def _calculate_pricing(
        self,
        claim: PharmacyClaim,
        member: RxMember,
        formulary_status: FormularyStatus,
    ) -> PricingResult:
        """Calculate claim pricing."""
        # Use submitted costs (in real system would price based on contract)
        ingredient_cost = claim.ingredient_cost_submitted
        dispensing_fee = claim.dispensing_fee_submitted

        total_cost = ingredient_cost + dispensing_fee

        # Get copay from formulary
        copay = Decimal(str(formulary_status.copay or 30))

        # Check deductible
        deductible_remaining = member.accumulators.deductible_remaining
        deductible_applied = Decimal("0")

        if deductible_remaining > 0:
            deductible_applied = min(deductible_remaining, total_cost)
            total_cost_after_deductible = total_cost - deductible_applied
        else:
            total_cost_after_deductible = total_cost

        # Patient pays copay (or less if cost is lower)
        patient_pays = min(copay + deductible_applied, total_cost)

        # Plan pays the rest
        plan_pays = total_cost - patient_pays

        return PricingResult(
            ingredient_cost=ingredient_cost,
            dispensing_fee=dispensing_fee,
            plan_pays=max(plan_pays, Decimal("0")),
            patient_pays=patient_pays,
            copay=min(copay, total_cost_after_deductible),
            deductible_applied=deductible_applied,
        )

    def _create_rejection(
        self, claim: PharmacyClaim, reject_codes: list[RejectCode]
    ) -> ClaimResponse:
        """Create rejection response."""
        return ClaimResponse(
            claim_id=claim.claim_id,
            transaction_response_status="R",
            response_status="R",
            reject_codes=reject_codes,
        )

    def _generate_auth_number(self) -> str:
        """Generate authorization number."""
        return f"AUTH{random.randint(100000000, 999999999)}"
