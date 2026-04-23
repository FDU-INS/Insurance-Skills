"""Copay assistance and discount program models."""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class ProgramType(str, Enum):
    """Type of copay assistance program."""

    MANUFACTURER_COPAY = "manufacturer_copay"  # Manufacturer copay card
    FOUNDATION = "foundation"  # Patient assistance foundation
    DISCOUNT_CARD = "discount_card"  # Generic discount programs
    COUPON = "coupon"  # Single-use coupons
    REBATE = "rebate"  # Mail-in rebate


class EligibilityType(str, Enum):
    """Eligibility requirements for program."""

    COMMERCIAL_ONLY = "commercial_only"  # No govt insurance
    ALL_PATIENTS = "all_patients"  # Any patient
    UNINSURED_ONLY = "uninsured_only"  # Cash patients only
    INCOME_BASED = "income_based"  # Based on FPL


class CopayAssistanceProgram(BaseModel):
    """Manufacturer copay assistance program."""

    program_id: str
    program_name: str
    manufacturer_name: str
    program_type: ProgramType = ProgramType.MANUFACTURER_COPAY

    # Covered products
    covered_ndcs: list[str] = Field(default_factory=list)
    covered_gpis: list[str] = Field(default_factory=list)
    drug_name: str | None = None

    # Eligibility
    eligibility_type: EligibilityType = EligibilityType.COMMERCIAL_ONLY
    min_age: int | None = None
    max_age: int | None = None
    max_income_fpl: int | None = None  # % of federal poverty level

    # Benefit terms
    max_benefit_per_fill: Decimal = Decimal("0")  # $0 = no limit
    max_benefit_annual: Decimal = Decimal("0")
    max_fills_per_year: int = 12
    patient_pays: Decimal = Decimal("0")  # Patient copay amount

    # Program dates
    effective_date: date = Field(default_factory=date.today)
    termination_date: date | None = None

    # BIN/PCN for processing
    bin_number: str | None = None
    pcn: str | None = None
    group_id: str | None = None


class CopayCardUsage(BaseModel):
    """Record of copay card usage."""

    program_id: str
    member_id: str
    claim_id: str | None = None
    service_date: date

    ndc: str
    drug_name: str | None = None

    original_copay: Decimal
    program_payment: Decimal
    patient_pays: Decimal

    fills_used_ytd: int
    benefit_used_ytd: Decimal
    benefit_remaining: Decimal


class DiscountProgram(BaseModel):
    """Generic discount card program (GoodRx, etc.)."""

    program_id: str
    program_name: str
    program_type: ProgramType = ProgramType.DISCOUNT_CARD

    # Pricing basis
    discount_type: str = "mac"  # mac, awp_discount, fixed
    awp_discount_percentage: Decimal | None = None
    fixed_price: Decimal | None = None

    # Fees
    dispensing_fee: Decimal = Decimal("2.00")
    admin_fee: Decimal = Decimal("0")

    # Pharmacy network
    pharmacy_network: str = "all"  # all, retail, mail, specialty
    contracted_pharmacies: list[str] = Field(default_factory=list)


class DiscountCardPricing(BaseModel):
    """Pricing result from discount card."""

    program_id: str
    program_name: str
    ndc: str
    drug_name: str | None = None

    awp: Decimal
    quantity: Decimal

    discounted_price: Decimal
    dispensing_fee: Decimal
    total_price: Decimal

    savings_vs_cash: Decimal
    savings_percentage: Decimal


class AccumulatorAdjustment(BaseModel):
    """Accumulator adjustment tracking."""

    member_id: str
    claim_id: str
    service_date: date

    ndc: str
    drug_name: str | None = None

    total_cost: Decimal
    member_paid: Decimal
    copay_assist_paid: Decimal

    # What counts toward accumulators
    deductible_credit: Decimal
    oop_credit: Decimal

    # Accumulator maximizer flag
    maximizer_applied: bool = False


class CopayAssistanceCalculator:
    """Calculate copay assistance benefits."""

    def __init__(
        self, programs: list[CopayAssistanceProgram] | None = None
    ) -> None:
        self.programs: list[CopayAssistanceProgram] = programs or []
        self.usage_tracker: dict[str, list[CopayCardUsage]] = {}

    def add_program(self, program: CopayAssistanceProgram) -> None:
        """Add a copay assistance program."""
        self.programs.append(program)

    def find_program(
        self,
        ndc: str,
        gpi: str | None = None,
        service_date: date | None = None,
        has_commercial_insurance: bool = True,
    ) -> CopayAssistanceProgram | None:
        """Find applicable copay assistance program."""
        check_date = service_date or date.today()

        for program in self.programs:
            # Check date validity
            if program.effective_date > check_date:
                continue
            if program.termination_date and program.termination_date < check_date:
                continue

            # Check eligibility
            if program.eligibility_type == EligibilityType.COMMERCIAL_ONLY:
                if not has_commercial_insurance:
                    continue
            elif program.eligibility_type == EligibilityType.UNINSURED_ONLY:
                if has_commercial_insurance:
                    continue

            # Check NDC match
            if ndc in program.covered_ndcs:
                return program

            # Check GPI prefix match
            if gpi:
                for gpi_prefix in program.covered_gpis:
                    if gpi.startswith(gpi_prefix):
                        return program

        return None

    def calculate_benefit(
        self,
        program: CopayAssistanceProgram,
        member_id: str,
        original_copay: Decimal,
        ndc: str,
        service_date: date | None = None,
        drug_name: str | None = None,
        claim_id: str | None = None,
    ) -> CopayCardUsage:
        """Calculate copay assistance benefit for a claim."""
        svc_date = service_date or date.today()

        # Get YTD usage
        key = f"{member_id}:{program.program_id}"
        prior_usage = self.usage_tracker.get(key, [])

        # Filter to current year
        year_start = date(svc_date.year, 1, 1)
        ytd_usage = [u for u in prior_usage if u.service_date >= year_start]

        fills_used = len(ytd_usage)
        benefit_used = sum(u.program_payment for u in ytd_usage)

        # Check limits
        if program.max_fills_per_year and fills_used >= program.max_fills_per_year:
            # No benefit remaining
            return CopayCardUsage(
                program_id=program.program_id,
                member_id=member_id,
                claim_id=claim_id,
                service_date=svc_date,
                ndc=ndc,
                drug_name=drug_name,
                original_copay=original_copay,
                program_payment=Decimal("0"),
                patient_pays=original_copay,
                fills_used_ytd=fills_used,
                benefit_used_ytd=benefit_used,
                benefit_remaining=Decimal("0"),
            )

        # Calculate benefit
        benefit_available = original_copay - program.patient_pays
        if benefit_available < 0:
            benefit_available = Decimal("0")

        # Apply per-fill limit
        if program.max_benefit_per_fill > 0:
            benefit_available = min(benefit_available, program.max_benefit_per_fill)

        # Apply annual limit
        if program.max_benefit_annual > 0:
            annual_remaining = program.max_benefit_annual - benefit_used
            if annual_remaining <= 0:
                benefit_available = Decimal("0")
            else:
                benefit_available = min(benefit_available, annual_remaining)

        program_payment = benefit_available.quantize(Decimal("0.01"))
        patient_pays = (original_copay - program_payment).quantize(Decimal("0.01"))

        # Ensure patient pays at least the minimum
        if patient_pays < program.patient_pays:
            patient_pays = program.patient_pays
            program_payment = original_copay - patient_pays

        # Calculate remaining benefit
        benefit_remaining = Decimal("0")
        if program.max_benefit_annual > 0:
            benefit_remaining = program.max_benefit_annual - benefit_used - program_payment

        usage = CopayCardUsage(
            program_id=program.program_id,
            member_id=member_id,
            claim_id=claim_id,
            service_date=svc_date,
            ndc=ndc,
            drug_name=drug_name,
            original_copay=original_copay,
            program_payment=program_payment,
            patient_pays=patient_pays,
            fills_used_ytd=fills_used + 1,
            benefit_used_ytd=benefit_used + program_payment,
            benefit_remaining=benefit_remaining,
        )

        # Track usage
        if key not in self.usage_tracker:
            self.usage_tracker[key] = []
        self.usage_tracker[key].append(usage)

        return usage


class SampleCopayPrograms:
    """Sample copay assistance programs."""

    @staticmethod
    def humira_complete() -> CopayAssistanceProgram:
        """AbbVie HUMIRA Complete copay card."""
        return CopayAssistanceProgram(
            program_id="HUMIRA-COMPLETE-001",
            program_name="HUMIRA Complete Savings Card",
            manufacturer_name="AbbVie",
            program_type=ProgramType.MANUFACTURER_COPAY,
            drug_name="Humira",
            covered_ndcs=["00074320502", "00074433902", "00074909902"],
            covered_gpis=["66400020"],
            eligibility_type=EligibilityType.COMMERCIAL_ONLY,
            max_benefit_per_fill=Decimal("0"),  # No per-fill limit
            max_benefit_annual=Decimal("20000"),
            max_fills_per_year=13,
            patient_pays=Decimal("5"),
            bin_number="004682",
            pcn="CN",
            group_id="AHUM0001",
        )

    @staticmethod
    def ozempic_savings() -> CopayAssistanceProgram:
        """Novo Nordisk Ozempic savings card."""
        return CopayAssistanceProgram(
            program_id="OZEMPIC-SAVINGS-001",
            program_name="Ozempic Savings Card",
            manufacturer_name="Novo Nordisk",
            program_type=ProgramType.MANUFACTURER_COPAY,
            drug_name="Ozempic",
            covered_ndcs=["00169413512", "00169413513", "00169413515"],
            covered_gpis=["27200060"],
            eligibility_type=EligibilityType.COMMERCIAL_ONLY,
            max_benefit_per_fill=Decimal("150"),
            max_benefit_annual=Decimal("0"),  # No annual limit
            max_fills_per_year=12,
            patient_pays=Decimal("25"),
            bin_number="610524",
            pcn="NOVO",
            group_id="OZEMP001",
        )

    @staticmethod
    def jardiance_savings() -> CopayAssistanceProgram:
        """Boehringer Ingelheim Jardiance savings card."""
        return CopayAssistanceProgram(
            program_id="JARDIANCE-SAVINGS-001",
            program_name="Jardiance Savings Card",
            manufacturer_name="Boehringer Ingelheim",
            program_type=ProgramType.MANUFACTURER_COPAY,
            drug_name="Jardiance",
            covered_ndcs=["00002323201", "00002323301"],
            covered_gpis=["27700057"],
            eligibility_type=EligibilityType.COMMERCIAL_ONLY,
            max_benefit_per_fill=Decimal("300"),
            max_benefit_annual=Decimal("3600"),
            max_fills_per_year=12,
            patient_pays=Decimal("10"),
            bin_number="003858",
            pcn="ASPN",
            group_id="JARD0001",
        )

    @staticmethod
    def lipitor_card() -> CopayAssistanceProgram:
        """Pfizer Lipitor savings card (legacy brand)."""
        return CopayAssistanceProgram(
            program_id="LIPITOR-SAVINGS-001",
            program_name="Lipitor Co-pay Card",
            manufacturer_name="Pfizer",
            program_type=ProgramType.MANUFACTURER_COPAY,
            drug_name="Lipitor",
            covered_ndcs=["00069015430", "00069015530"],
            covered_gpis=["3940"],
            eligibility_type=EligibilityType.COMMERCIAL_ONLY,
            max_benefit_per_fill=Decimal("100"),
            max_benefit_annual=Decimal("1200"),
            max_fills_per_year=12,
            patient_pays=Decimal("4"),
        )

    @staticmethod
    def goodrx_discount() -> DiscountProgram:
        """GoodRx-style discount card program."""
        return DiscountProgram(
            program_id="GOODRX-001",
            program_name="GoodRx Discount",
            program_type=ProgramType.DISCOUNT_CARD,
            discount_type="mac",
            dispensing_fee=Decimal("2.50"),
            admin_fee=Decimal("0.50"),
            pharmacy_network="all",
        )
