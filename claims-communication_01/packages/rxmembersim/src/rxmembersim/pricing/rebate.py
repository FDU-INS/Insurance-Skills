"""Pharmaceutical rebate models."""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class RebateType(str, Enum):
    """Type of rebate arrangement."""

    ACCESS = "access"  # Basic formulary access
    MARKET_SHARE = "market_share"  # Based on market share tier
    VOLUME = "volume"  # Based on utilization volume
    PERFORMANCE = "performance"  # Based on adherence/outcomes
    ADMIN_FEE = "admin_fee"  # Administrative fee rebate


class RebateTier(BaseModel):
    """Rebate tier within a contract."""

    tier_number: int
    tier_name: str | None = None

    # Market share thresholds
    min_market_share: Decimal | None = None
    max_market_share: Decimal | None = None

    # Volume thresholds
    min_volume: int | None = None
    max_volume: int | None = None

    # Rebate terms
    rebate_type: str  # "percentage" or "fixed"
    rebate_value: Decimal  # Percentage or fixed dollar amount


class RebateContract(BaseModel):
    """Pharmaceutical rebate contract."""

    contract_id: str
    manufacturer_id: str
    manufacturer_name: str
    contract_type: RebateType
    effective_date: date
    termination_date: date | None = None

    # Covered products
    covered_ndcs: list[str] = Field(default_factory=list)
    covered_gpis: list[str] = Field(default_factory=list)

    # Rebate tiers
    tiers: list[RebateTier]

    # Payment terms
    payment_frequency: str = "quarterly"  # quarterly, monthly, annually
    payment_lag_days: int = 90
    true_up_frequency: str = "annually"

    # Admin fees
    admin_fee_percentage: Decimal = Decimal("0")


class RebateCalculation(BaseModel):
    """Result of rebate calculation for a claim or period."""

    claim_id: str | None = None
    period_start: date | None = None
    period_end: date | None = None

    contract_id: str
    ndc: str
    gpi: str | None = None
    drug_name: str | None = None

    ingredient_cost: Decimal
    quantity: Decimal

    rebate_rate: Decimal
    rebate_amount: Decimal

    tier_number: int
    tier_name: str | None = None

    # Additional details
    admin_fee: Decimal = Decimal("0")
    net_rebate: Decimal = Decimal("0")


class PeriodRebateSummary(BaseModel):
    """Summary of rebates for a period."""

    contract_id: str
    manufacturer_name: str
    period_start: date
    period_end: date

    total_claims: int
    total_ingredient_cost: Decimal
    total_quantity: Decimal

    gross_rebate: Decimal
    admin_fees: Decimal
    net_rebate: Decimal

    effective_rebate_rate: Decimal

    by_tier: list[dict] = Field(default_factory=list)


class RebateCalculator:
    """Calculate rebates based on contracts."""

    def __init__(self, contracts: list[RebateContract] | None = None) -> None:
        self.contracts: list[RebateContract] = contracts or []

    def add_contract(self, contract: RebateContract) -> None:
        """Add a rebate contract."""
        self.contracts.append(contract)

    def calculate_claim_rebate(
        self,
        ndc: str,
        ingredient_cost: Decimal,
        quantity: Decimal,
        gpi: str | None = None,
        claim_id: str | None = None,
        service_date: date | None = None,
    ) -> RebateCalculation | None:
        """Calculate rebate for a single claim."""
        contract = self._find_contract(ndc, gpi, service_date)
        if not contract or not contract.tiers:
            return None

        # Use base tier for individual claim (actual tier determined at period end)
        base_tier = contract.tiers[0]

        if base_tier.rebate_type == "percentage":
            rebate_amount = ingredient_cost * (base_tier.rebate_value / 100)
        else:
            rebate_amount = base_tier.rebate_value * quantity

        rebate_amount = rebate_amount.quantize(Decimal("0.01"))

        # Calculate admin fee
        admin_fee = (rebate_amount * contract.admin_fee_percentage / 100).quantize(
            Decimal("0.01")
        )
        net_rebate = rebate_amount - admin_fee

        return RebateCalculation(
            claim_id=claim_id,
            contract_id=contract.contract_id,
            ndc=ndc,
            gpi=gpi,
            ingredient_cost=ingredient_cost,
            quantity=quantity,
            rebate_rate=base_tier.rebate_value,
            rebate_amount=rebate_amount,
            tier_number=base_tier.tier_number,
            tier_name=base_tier.tier_name,
            admin_fee=admin_fee,
            net_rebate=net_rebate,
        )

    def calculate_period_rebate(
        self,
        claims: list[dict],
        market_share: Decimal | None = None,
        period_start: date | None = None,
        period_end: date | None = None,
    ) -> list[PeriodRebateSummary]:
        """Calculate rebates for a period of claims."""
        summaries: list[PeriodRebateSummary] = []

        # Group claims by contract
        contract_claims: dict[str, list[dict]] = {}
        for claim in claims:
            ndc = claim.get("ndc", "")
            gpi = claim.get("gpi")
            contract = self._find_contract(ndc, gpi)
            if contract:
                if contract.contract_id not in contract_claims:
                    contract_claims[contract.contract_id] = []
                contract_claims[contract.contract_id].append(claim)

        # Calculate rebates for each contract
        for contract_id, contract_claim_list in contract_claims.items():
            contract = next(
                (c for c in self.contracts if c.contract_id == contract_id), None
            )
            if not contract:
                continue

            # Determine tier based on market share or volume
            tier = self._determine_tier(
                contract, market_share, len(contract_claim_list)
            )
            if not tier:
                tier = contract.tiers[0]

            # Calculate totals
            total_ingredient = sum(
                Decimal(str(c.get("ingredient_cost", 0))) for c in contract_claim_list
            )
            total_quantity = sum(
                Decimal(str(c.get("quantity", 0))) for c in contract_claim_list
            )

            # Calculate gross rebate
            if tier.rebate_type == "percentage":
                gross_rebate = total_ingredient * (tier.rebate_value / 100)
            else:
                gross_rebate = tier.rebate_value * total_quantity

            gross_rebate = gross_rebate.quantize(Decimal("0.01"))

            # Admin fees
            admin_fees = (gross_rebate * contract.admin_fee_percentage / 100).quantize(
                Decimal("0.01")
            )
            net_rebate = gross_rebate - admin_fees

            # Effective rate
            effective_rate = (
                (gross_rebate / total_ingredient * 100).quantize(Decimal("0.01"))
                if total_ingredient
                else Decimal("0")
            )

            summaries.append(
                PeriodRebateSummary(
                    contract_id=contract_id,
                    manufacturer_name=contract.manufacturer_name,
                    period_start=period_start or date.today(),
                    period_end=period_end or date.today(),
                    total_claims=len(contract_claim_list),
                    total_ingredient_cost=total_ingredient,
                    total_quantity=total_quantity,
                    gross_rebate=gross_rebate,
                    admin_fees=admin_fees,
                    net_rebate=net_rebate,
                    effective_rebate_rate=effective_rate,
                )
            )

        return summaries

    def _find_contract(
        self,
        ndc: str,
        gpi: str | None = None,
        service_date: date | None = None,
    ) -> RebateContract | None:
        """Find applicable contract for a drug."""
        check_date = service_date or date.today()

        for contract in self.contracts:
            # Check date validity
            if contract.effective_date > check_date:
                continue
            if contract.termination_date and contract.termination_date < check_date:
                continue

            # Check NDC match
            if ndc in contract.covered_ndcs:
                return contract

            # Check GPI prefix match
            if gpi:
                for gpi_prefix in contract.covered_gpis:
                    if gpi.startswith(gpi_prefix):
                        return contract

        return None

    def _determine_tier(
        self,
        contract: RebateContract,
        market_share: Decimal | None,
        volume: int,
    ) -> RebateTier | None:
        """Determine which tier applies based on market share or volume."""
        if contract.contract_type == RebateType.MARKET_SHARE and market_share:
            for tier in contract.tiers:
                if tier.min_market_share is not None and tier.max_market_share is not None:
                    if tier.min_market_share <= market_share < tier.max_market_share:
                        return tier

        elif contract.contract_type == RebateType.VOLUME:
            for tier in contract.tiers:
                if tier.min_volume is not None and tier.max_volume is not None:
                    if tier.min_volume <= volume < tier.max_volume:
                        return tier

        return contract.tiers[0] if contract.tiers else None


class SampleRebateContracts:
    """Sample rebate contracts for simulation."""

    @staticmethod
    def brand_statin() -> RebateContract:
        """Lipitor/brand statin rebate contract."""
        return RebateContract(
            contract_id="REBATE-STATIN-001",
            manufacturer_id="MFR-PFE",
            manufacturer_name="Pfizer",
            contract_type=RebateType.MARKET_SHARE,
            effective_date=date(2025, 1, 1),
            covered_gpis=["3940"],
            covered_ndcs=["00069015430"],  # Lipitor
            tiers=[
                RebateTier(
                    tier_number=1,
                    tier_name="Base",
                    min_market_share=Decimal("0"),
                    max_market_share=Decimal("30"),
                    rebate_type="percentage",
                    rebate_value=Decimal("15"),
                ),
                RebateTier(
                    tier_number=2,
                    tier_name="Preferred",
                    min_market_share=Decimal("30"),
                    max_market_share=Decimal("50"),
                    rebate_type="percentage",
                    rebate_value=Decimal("25"),
                ),
                RebateTier(
                    tier_number=3,
                    tier_name="Exclusive",
                    min_market_share=Decimal("50"),
                    max_market_share=Decimal("100"),
                    rebate_type="percentage",
                    rebate_value=Decimal("35"),
                ),
            ],
            admin_fee_percentage=Decimal("3"),
        )

    @staticmethod
    def glp1_agonist() -> RebateContract:
        """Ozempic/GLP-1 rebate contract."""
        return RebateContract(
            contract_id="REBATE-GLP1-001",
            manufacturer_id="MFR-NVO",
            manufacturer_name="Novo Nordisk",
            contract_type=RebateType.ACCESS,
            effective_date=date(2025, 1, 1),
            covered_gpis=["27200060"],
            covered_ndcs=["00169413512", "00169413513"],  # Ozempic
            tiers=[
                RebateTier(
                    tier_number=1,
                    tier_name="Formulary Access",
                    rebate_type="percentage",
                    rebate_value=Decimal("10"),
                ),
            ],
            admin_fee_percentage=Decimal("2"),
        )

    @staticmethod
    def tnf_inhibitor() -> RebateContract:
        """Humira/TNF inhibitor rebate contract."""
        return RebateContract(
            contract_id="REBATE-TNF-001",
            manufacturer_id="MFR-ABV",
            manufacturer_name="AbbVie",
            contract_type=RebateType.MARKET_SHARE,
            effective_date=date(2025, 1, 1),
            covered_gpis=["66400020"],
            covered_ndcs=["00074320502", "00074433902"],  # Humira
            tiers=[
                RebateTier(
                    tier_number=1,
                    tier_name="Base",
                    min_market_share=Decimal("0"),
                    max_market_share=Decimal("40"),
                    rebate_type="percentage",
                    rebate_value=Decimal("20"),
                ),
                RebateTier(
                    tier_number=2,
                    tier_name="Preferred",
                    min_market_share=Decimal("40"),
                    max_market_share=Decimal("100"),
                    rebate_type="percentage",
                    rebate_value=Decimal("40"),
                ),
            ],
            admin_fee_percentage=Decimal("3"),
        )
