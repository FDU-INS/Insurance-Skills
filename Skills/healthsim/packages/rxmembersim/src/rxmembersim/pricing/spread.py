"""PBM spread pricing models."""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class SpreadType(str, Enum):
    """Type of spread pricing arrangement."""

    TRADITIONAL = "traditional"  # PBM keeps difference
    PASS_THROUGH = "pass_through"  # Full transparency
    HYBRID = "hybrid"  # Mix of spread and pass-through
    TRANSPARENT = "transparent"  # Full disclosure with admin fee


class ChannelType(str, Enum):
    """Pharmacy channel type."""

    RETAIL = "retail"
    MAIL = "mail"
    SPECIALTY = "specialty"


class SpreadConfig(BaseModel):
    """Configuration for spread calculation."""

    channel: ChannelType
    spread_type: SpreadType

    # For traditional spread
    target_spread_percentage: Decimal = Decimal("0")  # As % of ingredient cost
    min_spread: Decimal = Decimal("0")  # Minimum spread per claim
    max_spread: Decimal = Decimal("999")  # Maximum spread per claim

    # For pass-through
    admin_fee_per_claim: Decimal = Decimal("0")
    admin_fee_percentage: Decimal = Decimal("0")

    # Brand vs Generic
    brand_spread_multiplier: Decimal = Decimal("1.0")
    generic_spread_multiplier: Decimal = Decimal("1.0")
    specialty_spread_multiplier: Decimal = Decimal("1.5")


class PharmacyReimbursement(BaseModel):
    """Pharmacy reimbursement terms."""

    pharmacy_npi: str | None = None
    pharmacy_name: str | None = None
    channel: ChannelType

    # AWP discount terms
    brand_awp_discount: Decimal = Decimal("15")  # % off AWP
    generic_awp_discount: Decimal = Decimal("80")  # % off AWP
    specialty_awp_discount: Decimal = Decimal("12")  # % off AWP

    # MAC pricing
    use_mac_pricing: bool = True
    mac_list_id: str | None = None

    # Dispensing fees
    brand_dispensing_fee: Decimal = Decimal("1.50")
    generic_dispensing_fee: Decimal = Decimal("2.00")
    specialty_dispensing_fee: Decimal = Decimal("0")


class ClientPricing(BaseModel):
    """Client billing terms."""

    client_id: str | None = None
    client_name: str | None = None

    # AWP discount terms (better than pharmacy)
    brand_awp_discount: Decimal = Decimal("14")  # % off AWP
    generic_awp_discount: Decimal = Decimal("78")  # % off AWP
    specialty_awp_discount: Decimal = Decimal("10")  # % off AWP

    # Dispensing fees
    brand_dispensing_fee: Decimal = Decimal("2.00")
    generic_dispensing_fee: Decimal = Decimal("2.50")
    specialty_dispensing_fee: Decimal = Decimal("0")


class SpreadCalculation(BaseModel):
    """Result of spread calculation for a claim."""

    claim_id: str | None = None
    ndc: str
    drug_name: str | None = None
    channel: ChannelType
    is_brand: bool
    is_specialty: bool = False

    # AWP reference
    awp: Decimal
    quantity: Decimal

    # Pharmacy side
    pharmacy_ingredient_cost: Decimal
    pharmacy_dispensing_fee: Decimal
    pharmacy_total: Decimal

    # Client side
    client_ingredient_cost: Decimal
    client_dispensing_fee: Decimal
    client_total: Decimal

    # Spread
    ingredient_spread: Decimal
    dispensing_fee_spread: Decimal
    total_spread: Decimal
    spread_percentage: Decimal

    # Admin fees (if pass-through)
    admin_fee: Decimal = Decimal("0")
    net_margin: Decimal = Decimal("0")


class PeriodSpreadSummary(BaseModel):
    """Summary of spread for a period."""

    period_start: date
    period_end: date
    client_id: str | None = None

    total_claims: int
    brand_claims: int
    generic_claims: int
    specialty_claims: int

    total_awp: Decimal
    total_pharmacy_cost: Decimal
    total_client_cost: Decimal
    total_spread: Decimal
    total_admin_fees: Decimal
    net_margin: Decimal

    average_spread_per_claim: Decimal
    average_spread_percentage: Decimal

    by_channel: list[dict] = Field(default_factory=list)


class SpreadCalculator:
    """Calculate spread pricing."""

    def __init__(
        self,
        pharmacy_terms: PharmacyReimbursement | None = None,
        client_terms: ClientPricing | None = None,
        spread_config: SpreadConfig | None = None,
    ) -> None:
        self.pharmacy_terms = pharmacy_terms or PharmacyReimbursement(
            channel=ChannelType.RETAIL
        )
        self.client_terms = client_terms or ClientPricing()
        self.spread_config = spread_config or SpreadConfig(
            channel=ChannelType.RETAIL, spread_type=SpreadType.TRADITIONAL
        )

    def calculate_claim_spread(
        self,
        ndc: str,
        awp: Decimal,
        quantity: Decimal,
        is_brand: bool,
        is_specialty: bool = False,
        channel: ChannelType = ChannelType.RETAIL,
        claim_id: str | None = None,
        drug_name: str | None = None,
    ) -> SpreadCalculation:
        """Calculate spread for a single claim."""
        # Determine pricing type
        if is_specialty:
            pharm_discount = self.pharmacy_terms.specialty_awp_discount
            client_discount = self.client_terms.specialty_awp_discount
            pharm_disp_fee = self.pharmacy_terms.specialty_dispensing_fee
            client_disp_fee = self.client_terms.specialty_dispensing_fee
        elif is_brand:
            pharm_discount = self.pharmacy_terms.brand_awp_discount
            client_discount = self.client_terms.brand_awp_discount
            pharm_disp_fee = self.pharmacy_terms.brand_dispensing_fee
            client_disp_fee = self.client_terms.brand_dispensing_fee
        else:
            pharm_discount = self.pharmacy_terms.generic_awp_discount
            client_discount = self.client_terms.generic_awp_discount
            pharm_disp_fee = self.pharmacy_terms.generic_dispensing_fee
            client_disp_fee = self.client_terms.generic_dispensing_fee

        # Calculate ingredient costs
        total_awp = awp * quantity
        pharmacy_ingredient = (
            total_awp * (Decimal("100") - pharm_discount) / Decimal("100")
        ).quantize(Decimal("0.01"))
        client_ingredient = (
            total_awp * (Decimal("100") - client_discount) / Decimal("100")
        ).quantize(Decimal("0.01"))

        # Calculate totals
        pharmacy_total = pharmacy_ingredient + pharm_disp_fee
        client_total = client_ingredient + client_disp_fee

        # Calculate spread
        ingredient_spread = client_ingredient - pharmacy_ingredient
        dispensing_spread = client_disp_fee - pharm_disp_fee
        total_spread = ingredient_spread + dispensing_spread

        spread_pct = (
            (total_spread / pharmacy_total * Decimal("100")).quantize(Decimal("0.01"))
            if pharmacy_total
            else Decimal("0")
        )

        # Admin fee for pass-through
        admin_fee = Decimal("0")
        if self.spread_config.spread_type in (
            SpreadType.PASS_THROUGH,
            SpreadType.TRANSPARENT,
        ):
            admin_fee = (
                self.spread_config.admin_fee_per_claim
                + client_total * self.spread_config.admin_fee_percentage / 100
            ).quantize(Decimal("0.01"))

        net_margin = total_spread + admin_fee

        return SpreadCalculation(
            claim_id=claim_id,
            ndc=ndc,
            drug_name=drug_name,
            channel=channel,
            is_brand=is_brand,
            is_specialty=is_specialty,
            awp=total_awp,
            quantity=quantity,
            pharmacy_ingredient_cost=pharmacy_ingredient,
            pharmacy_dispensing_fee=pharm_disp_fee,
            pharmacy_total=pharmacy_total,
            client_ingredient_cost=client_ingredient,
            client_dispensing_fee=client_disp_fee,
            client_total=client_total,
            ingredient_spread=ingredient_spread,
            dispensing_fee_spread=dispensing_spread,
            total_spread=total_spread,
            spread_percentage=spread_pct,
            admin_fee=admin_fee,
            net_margin=net_margin,
        )

    def calculate_period_spread(
        self,
        claims: list[dict],
        period_start: date | None = None,
        period_end: date | None = None,
    ) -> PeriodSpreadSummary:
        """Calculate spread summary for a period of claims."""
        calculations: list[SpreadCalculation] = []

        for claim in claims:
            calc = self.calculate_claim_spread(
                ndc=claim.get("ndc", ""),
                awp=Decimal(str(claim.get("awp", 0))),
                quantity=Decimal(str(claim.get("quantity", 1))),
                is_brand=claim.get("is_brand", False),
                is_specialty=claim.get("is_specialty", False),
                channel=claim.get("channel", ChannelType.RETAIL),
            )
            calculations.append(calc)

        # Aggregate
        total_claims = len(calculations)
        brand_claims = sum(1 for c in calculations if c.is_brand and not c.is_specialty)
        generic_claims = sum(
            1 for c in calculations if not c.is_brand and not c.is_specialty
        )
        specialty_claims = sum(1 for c in calculations if c.is_specialty)

        total_awp = sum(c.awp for c in calculations)
        total_pharmacy = sum(c.pharmacy_total for c in calculations)
        total_client = sum(c.client_total for c in calculations)
        total_spread = sum(c.total_spread for c in calculations)
        total_admin = sum(c.admin_fee for c in calculations)
        net_margin = sum(c.net_margin for c in calculations)

        avg_spread = (
            (total_spread / total_claims).quantize(Decimal("0.01"))
            if total_claims
            else Decimal("0")
        )
        avg_spread_pct = (
            (total_spread / total_pharmacy * 100).quantize(Decimal("0.01"))
            if total_pharmacy
            else Decimal("0")
        )

        return PeriodSpreadSummary(
            period_start=period_start or date.today(),
            period_end=period_end or date.today(),
            total_claims=total_claims,
            brand_claims=brand_claims,
            generic_claims=generic_claims,
            specialty_claims=specialty_claims,
            total_awp=total_awp,
            total_pharmacy_cost=total_pharmacy,
            total_client_cost=total_client,
            total_spread=total_spread,
            total_admin_fees=total_admin,
            net_margin=net_margin,
            average_spread_per_claim=avg_spread,
            average_spread_percentage=avg_spread_pct,
        )


class SampleSpreadConfigs:
    """Sample spread configurations."""

    @staticmethod
    def traditional_pbm() -> tuple[PharmacyReimbursement, ClientPricing, SpreadConfig]:
        """Traditional spread pricing model."""
        pharmacy = PharmacyReimbursement(
            channel=ChannelType.RETAIL,
            brand_awp_discount=Decimal("16"),
            generic_awp_discount=Decimal("82"),
            brand_dispensing_fee=Decimal("1.00"),
            generic_dispensing_fee=Decimal("1.50"),
        )
        client = ClientPricing(
            brand_awp_discount=Decimal("14"),
            generic_awp_discount=Decimal("77"),
            brand_dispensing_fee=Decimal("2.00"),
            generic_dispensing_fee=Decimal("2.50"),
        )
        config = SpreadConfig(
            channel=ChannelType.RETAIL,
            spread_type=SpreadType.TRADITIONAL,
        )
        return pharmacy, client, config

    @staticmethod
    def pass_through() -> tuple[PharmacyReimbursement, ClientPricing, SpreadConfig]:
        """Pass-through pricing with admin fee."""
        pharmacy = PharmacyReimbursement(
            channel=ChannelType.RETAIL,
            brand_awp_discount=Decimal("16"),
            generic_awp_discount=Decimal("82"),
            brand_dispensing_fee=Decimal("1.50"),
            generic_dispensing_fee=Decimal("2.00"),
        )
        client = ClientPricing(
            brand_awp_discount=Decimal("16"),  # Same as pharmacy
            generic_awp_discount=Decimal("82"),  # Same as pharmacy
            brand_dispensing_fee=Decimal("1.50"),
            generic_dispensing_fee=Decimal("2.00"),
        )
        config = SpreadConfig(
            channel=ChannelType.RETAIL,
            spread_type=SpreadType.PASS_THROUGH,
            admin_fee_per_claim=Decimal("4.50"),
        )
        return pharmacy, client, config

    @staticmethod
    def transparent() -> tuple[PharmacyReimbursement, ClientPricing, SpreadConfig]:
        """Transparent pricing with percentage admin fee."""
        pharmacy = PharmacyReimbursement(
            channel=ChannelType.RETAIL,
            brand_awp_discount=Decimal("17"),
            generic_awp_discount=Decimal("85"),
            brand_dispensing_fee=Decimal("0.50"),
            generic_dispensing_fee=Decimal("1.00"),
        )
        client = ClientPricing(
            brand_awp_discount=Decimal("17"),
            generic_awp_discount=Decimal("85"),
            brand_dispensing_fee=Decimal("0.50"),
            generic_dispensing_fee=Decimal("1.00"),
        )
        config = SpreadConfig(
            channel=ChannelType.RETAIL,
            spread_type=SpreadType.TRANSPARENT,
            admin_fee_percentage=Decimal("2"),
        )
        return pharmacy, client, config
