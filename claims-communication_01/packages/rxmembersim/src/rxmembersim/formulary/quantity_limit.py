"""Quantity limit management."""
from datetime import date, timedelta
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class QuantityLimitType(str, Enum):
    """Types of quantity limits."""

    PER_FILL = "per_fill"  # Limit per individual fill
    PER_DAY = "per_day"  # Daily limit
    PER_MONTH = "per_month"  # Monthly limit
    PER_YEAR = "per_year"  # Annual limit
    MAX_DAYS_SUPPLY = "max_days"  # Maximum days supply


class QuantityLimit(BaseModel):
    """Quantity limit definition."""

    limit_id: str
    drug_identifier: str  # NDC or GPI prefix
    limit_type: QuantityLimitType

    # Limit values
    max_quantity: Decimal | None = None
    max_days_supply: int | None = None

    # Time period (for accumulating limits)
    period_days: int = 30

    # Description
    description: str | None = None
    clinical_rationale: str | None = None


class QuantityLimitResult(BaseModel):
    """Result of quantity limit check."""

    passed: bool
    limit_type: QuantityLimitType | None = None

    requested_quantity: Decimal
    allowed_quantity: Decimal
    max_quantity: Decimal | None = None

    requested_days_supply: int
    allowed_days_supply: int
    max_days_supply: int | None = None

    # Accumulator info
    quantity_used_in_period: Decimal = Decimal("0")
    quantity_remaining_in_period: Decimal | None = None

    message: str


class QuantityLimitManager:
    """Manage quantity limits."""

    def __init__(self) -> None:
        self.limits: dict[str, list[QuantityLimit]] = {}  # keyed by drug identifier
        self._load_default_limits()

    def _load_default_limits(self) -> None:
        """Load common quantity limits."""
        # Controlled substances - typically limited quantities
        self.add_limit(
            QuantityLimit(
                limit_id="STIMULANT-QL",
                drug_identifier="6510",  # CNS Stimulants GPI prefix
                limit_type=QuantityLimitType.PER_FILL,
                max_quantity=Decimal("60"),
                max_days_supply=30,
                description="Stimulant quantity limit",
                clinical_rationale="Controlled substance - limit to 30 day supply",
            )
        )

        # Opioids
        self.add_limit(
            QuantityLimit(
                limit_id="OPIOID-QL",
                drug_identifier="6505",  # Opioid GPI prefix
                limit_type=QuantityLimitType.PER_FILL,
                max_quantity=Decimal("120"),
                max_days_supply=30,
                description="Opioid quantity limit",
                clinical_rationale="Opioid safety - limit quantity per fill",
            )
        )

        # PPIs - often have monthly limits
        self.add_limit(
            QuantityLimit(
                limit_id="PPI-QL",
                drug_identifier="4940",  # PPI GPI prefix
                limit_type=QuantityLimitType.PER_FILL,
                max_quantity=Decimal("30"),
                max_days_supply=30,
                description="PPI quantity limit",
                clinical_rationale="Long-term PPI use monitoring",
            )
        )

        # Triptan limits
        self.add_limit(
            QuantityLimit(
                limit_id="TRIPTAN-QL",
                drug_identifier="5830",  # Triptan GPI prefix
                limit_type=QuantityLimitType.PER_MONTH,
                max_quantity=Decimal("9"),
                period_days=30,
                description="Triptan monthly limit",
                clinical_rationale="Prevent medication overuse headache",
            )
        )

        # GLP-1 agonists - weekly injections
        self.add_limit(
            QuantityLimit(
                limit_id="GLP1-QL",
                drug_identifier="27200060",  # GLP-1 GPI prefix
                limit_type=QuantityLimitType.MAX_DAYS_SUPPLY,
                max_days_supply=28,
                description="GLP-1 days supply limit",
                clinical_rationale="Specialty drug - 28 day supply max",
            )
        )

        # Specialty biologics
        self.add_limit(
            QuantityLimit(
                limit_id="BIOLOGIC-QL",
                drug_identifier="6640",  # Biologics GPI prefix
                limit_type=QuantityLimitType.MAX_DAYS_SUPPLY,
                max_days_supply=28,
                description="Biologic days supply limit",
                clinical_rationale="Specialty drug monitoring",
            )
        )

    def add_limit(self, limit: QuantityLimit) -> None:
        """Add a quantity limit."""
        if limit.drug_identifier not in self.limits:
            self.limits[limit.drug_identifier] = []
        self.limits[limit.drug_identifier].append(limit)

    def find_limits_for_drug(
        self, ndc: str, gpi: str | None = None
    ) -> list[QuantityLimit]:
        """Find all quantity limits that apply to a drug."""
        applicable_limits: list[QuantityLimit] = []

        # Check NDC-specific limits
        if ndc in self.limits:
            applicable_limits.extend(self.limits[ndc])

        # Check GPI-based limits
        if gpi:
            for identifier, limits in self.limits.items():
                if gpi.startswith(identifier):
                    applicable_limits.extend(limits)

        return applicable_limits

    def check_quantity_limit(
        self,
        ndc: str,
        gpi: str | None,
        requested_quantity: Decimal,
        requested_days_supply: int,
        claim_history: list | None = None,
        service_date: date | None = None,
    ) -> QuantityLimitResult:
        """Check if requested quantity is within limits."""
        limits = self.find_limits_for_drug(ndc, gpi)

        if not limits:
            # No limits apply
            return QuantityLimitResult(
                passed=True,
                requested_quantity=requested_quantity,
                allowed_quantity=requested_quantity,
                requested_days_supply=requested_days_supply,
                allowed_days_supply=requested_days_supply,
                message="No quantity limits apply",
            )

        # Check each limit
        most_restrictive_result: QuantityLimitResult | None = None

        for limit in limits:
            result = self._check_single_limit(
                limit,
                ndc,
                requested_quantity,
                requested_days_supply,
                claim_history or [],
                service_date or date.today(),
            )

            if not result.passed:
                # Return first failure
                return result

            # Track most restrictive
            if most_restrictive_result is None or (
                result.allowed_quantity < most_restrictive_result.allowed_quantity
            ):
                most_restrictive_result = result

        return most_restrictive_result or QuantityLimitResult(
            passed=True,
            requested_quantity=requested_quantity,
            allowed_quantity=requested_quantity,
            requested_days_supply=requested_days_supply,
            allowed_days_supply=requested_days_supply,
            message="Quantity within limits",
        )

    def _check_single_limit(
        self,
        limit: QuantityLimit,
        ndc: str,
        requested_quantity: Decimal,
        requested_days_supply: int,
        claim_history: list,
        service_date: date,
    ) -> QuantityLimitResult:
        """Check a single quantity limit."""
        if limit.limit_type == QuantityLimitType.PER_FILL:
            return self._check_per_fill_limit(
                limit, requested_quantity, requested_days_supply
            )

        elif limit.limit_type == QuantityLimitType.MAX_DAYS_SUPPLY:
            return self._check_days_supply_limit(
                limit, requested_quantity, requested_days_supply
            )

        elif limit.limit_type in (
            QuantityLimitType.PER_MONTH,
            QuantityLimitType.PER_YEAR,
        ):
            return self._check_accumulating_limit(
                limit, ndc, requested_quantity, requested_days_supply,
                claim_history, service_date
            )

        return QuantityLimitResult(
            passed=True,
            requested_quantity=requested_quantity,
            allowed_quantity=requested_quantity,
            requested_days_supply=requested_days_supply,
            allowed_days_supply=requested_days_supply,
            message="Unknown limit type",
        )

    def _check_per_fill_limit(
        self,
        limit: QuantityLimit,
        requested_quantity: Decimal,
        requested_days_supply: int,
    ) -> QuantityLimitResult:
        """Check per-fill quantity limit."""
        qty_passed = True
        days_passed = True
        allowed_qty = requested_quantity
        allowed_days = requested_days_supply

        if limit.max_quantity and requested_quantity > limit.max_quantity:
            qty_passed = False
            allowed_qty = limit.max_quantity

        if limit.max_days_supply and requested_days_supply > limit.max_days_supply:
            days_passed = False
            allowed_days = limit.max_days_supply

        passed = qty_passed and days_passed
        messages = []
        if not qty_passed:
            messages.append(
                f"Quantity exceeds limit of {limit.max_quantity}"
            )
        if not days_passed:
            messages.append(
                f"Days supply exceeds limit of {limit.max_days_supply}"
            )

        return QuantityLimitResult(
            passed=passed,
            limit_type=limit.limit_type,
            requested_quantity=requested_quantity,
            allowed_quantity=allowed_qty,
            max_quantity=limit.max_quantity,
            requested_days_supply=requested_days_supply,
            allowed_days_supply=allowed_days,
            max_days_supply=limit.max_days_supply,
            message="; ".join(messages) if messages else "Within per-fill limit",
        )

    def _check_days_supply_limit(
        self,
        limit: QuantityLimit,
        requested_quantity: Decimal,
        requested_days_supply: int,
    ) -> QuantityLimitResult:
        """Check days supply limit."""
        if limit.max_days_supply and requested_days_supply > limit.max_days_supply:
            return QuantityLimitResult(
                passed=False,
                limit_type=limit.limit_type,
                requested_quantity=requested_quantity,
                allowed_quantity=requested_quantity,
                requested_days_supply=requested_days_supply,
                allowed_days_supply=limit.max_days_supply,
                max_days_supply=limit.max_days_supply,
                message=f"Days supply exceeds maximum of {limit.max_days_supply}",
            )

        return QuantityLimitResult(
            passed=True,
            limit_type=limit.limit_type,
            requested_quantity=requested_quantity,
            allowed_quantity=requested_quantity,
            requested_days_supply=requested_days_supply,
            allowed_days_supply=requested_days_supply,
            max_days_supply=limit.max_days_supply,
            message="Within days supply limit",
        )

    def _check_accumulating_limit(
        self,
        limit: QuantityLimit,
        ndc: str,
        requested_quantity: Decimal,
        requested_days_supply: int,
        claim_history: list,
        service_date: date,
    ) -> QuantityLimitResult:
        """Check accumulating quantity limit (monthly/yearly)."""
        period_start = service_date - timedelta(days=limit.period_days)

        # Sum quantity in period
        quantity_used = Decimal("0")
        for claim in claim_history:
            claim_ndc = getattr(claim, "ndc", None)
            claim_date = getattr(claim, "service_date", None)
            claim_qty = getattr(claim, "quantity_dispensed", Decimal("0"))

            if claim_ndc == ndc and claim_date and claim_date >= period_start:
                quantity_used += claim_qty

        remaining = (
            (limit.max_quantity - quantity_used)
            if limit.max_quantity
            else Decimal("999999")
        )
        allowed_qty = min(requested_quantity, max(remaining, Decimal("0")))

        passed = requested_quantity <= remaining

        return QuantityLimitResult(
            passed=passed,
            limit_type=limit.limit_type,
            requested_quantity=requested_quantity,
            allowed_quantity=allowed_qty,
            max_quantity=limit.max_quantity,
            requested_days_supply=requested_days_supply,
            allowed_days_supply=requested_days_supply,
            quantity_used_in_period=quantity_used,
            quantity_remaining_in_period=remaining,
            message=(
                f"Within {limit.period_days}-day limit"
                if passed
                else f"Exceeds {limit.period_days}-day limit. "
                f"Used: {quantity_used}, Max: {limit.max_quantity}, "
                f"Remaining: {remaining}"
            ),
        )
