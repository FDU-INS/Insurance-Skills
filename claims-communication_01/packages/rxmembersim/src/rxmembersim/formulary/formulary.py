"""Formulary model and management."""
from decimal import Decimal

from pydantic import BaseModel, Field


class FormularyTier(BaseModel):
    """Formulary tier definition."""

    tier_number: int
    tier_name: str
    copay_amount: Decimal | None = None
    coinsurance_percent: Decimal | None = None
    deductible_applies: bool = True


class FormularyDrug(BaseModel):
    """Drug on formulary."""

    ndc: str
    gpi: str
    drug_name: str

    tier: int
    covered: bool = True

    # Requirements
    requires_pa: bool = False
    requires_step_therapy: bool = False
    step_therapy_group: str | None = None

    # Quantity limits
    quantity_limit: int | None = None
    quantity_limit_days: int | None = None
    max_days_supply: int | None = None

    # Age/gender restrictions
    min_age: int | None = None
    max_age: int | None = None
    gender_restriction: str | None = None  # M, F, or None


class FormularyStatus(BaseModel):
    """Status of drug on formulary."""

    ndc: str
    covered: bool
    tier: int | None = None
    tier_name: str | None = None

    requires_pa: bool = False
    requires_step_therapy: bool = False
    step_therapy_group: str | None = None
    quantity_limit: int | None = None
    quantity_limit_days: int | None = None
    max_days_supply: int | None = None

    copay: Decimal | None = None
    coinsurance: Decimal | None = None

    preferred_alternatives: list[str] = Field(default_factory=list)
    message: str | None = None


class Formulary(BaseModel):
    """Drug formulary."""

    formulary_id: str
    name: str
    effective_date: str

    tiers: list[FormularyTier] = Field(default_factory=list)
    drugs: dict[str, FormularyDrug] = Field(default_factory=dict)  # keyed by NDC

    # Default values for drugs not in formulary
    default_tier: int = 3
    default_copay: Decimal = Decimal("50.00")

    def check_coverage(self, ndc: str) -> FormularyStatus:
        """Check coverage status for a drug."""
        drug = self.drugs.get(ndc)

        if not drug:
            # Drug not in formulary - return non-covered
            return FormularyStatus(
                ndc=ndc,
                covered=False,
                message="Drug not on formulary",
            )

        if not drug.covered:
            return FormularyStatus(
                ndc=ndc,
                covered=False,
                message="Drug excluded from coverage",
            )

        tier_info = next(
            (t for t in self.tiers if t.tier_number == drug.tier), None
        )

        return FormularyStatus(
            ndc=ndc,
            covered=True,
            tier=drug.tier,
            tier_name=tier_info.tier_name if tier_info else f"Tier {drug.tier}",
            requires_pa=drug.requires_pa,
            requires_step_therapy=drug.requires_step_therapy,
            step_therapy_group=drug.step_therapy_group,
            quantity_limit=drug.quantity_limit,
            quantity_limit_days=drug.quantity_limit_days,
            max_days_supply=drug.max_days_supply,
            copay=tier_info.copay_amount if tier_info else self.default_copay,
            coinsurance=tier_info.coinsurance_percent if tier_info else None,
        )

    def add_drug(self, drug: FormularyDrug) -> None:
        """Add drug to formulary."""
        self.drugs[drug.ndc] = drug

    def remove_drug(self, ndc: str) -> bool:
        """Remove drug from formulary."""
        if ndc in self.drugs:
            del self.drugs[ndc]
            return True
        return False

    def get_drugs_by_tier(self, tier: int) -> list[FormularyDrug]:
        """Get all drugs in a specific tier."""
        return [d for d in self.drugs.values() if d.tier == tier]

    def get_drugs_requiring_pa(self) -> list[FormularyDrug]:
        """Get all drugs requiring prior authorization."""
        return [d for d in self.drugs.values() if d.requires_pa]

    def get_drugs_by_gpi(self, gpi_prefix: str) -> list[FormularyDrug]:
        """Get drugs by GPI prefix (therapeutic class)."""
        return [d for d in self.drugs.values() if d.gpi.startswith(gpi_prefix)]


class FormularyGenerator:
    """Generate sample formularies."""

    def generate_standard_commercial(self) -> Formulary:
        """Generate standard 4-tier commercial formulary."""
        formulary = Formulary(
            formulary_id="COMM-STD-2025",
            name="Standard Commercial 4-Tier",
            effective_date="2025-01-01",
            tiers=[
                FormularyTier(
                    tier_number=1,
                    tier_name="Preferred Generic",
                    copay_amount=Decimal("10"),
                ),
                FormularyTier(
                    tier_number=2,
                    tier_name="Non-Preferred Generic",
                    copay_amount=Decimal("25"),
                ),
                FormularyTier(
                    tier_number=3,
                    tier_name="Preferred Brand",
                    copay_amount=Decimal("50"),
                ),
                FormularyTier(
                    tier_number=4,
                    tier_name="Non-Preferred Brand",
                    copay_amount=Decimal("80"),
                ),
                FormularyTier(
                    tier_number=5,
                    tier_name="Specialty",
                    coinsurance_percent=Decimal("25"),
                ),
            ],
        )

        # Add sample drugs - Statins (GPI 3940)
        formulary.add_drug(
            FormularyDrug(
                ndc="00071015523",
                gpi="39400010000310",
                drug_name="Atorvastatin 10mg",
                tier=1,
            )
        )
        formulary.add_drug(
            FormularyDrug(
                ndc="00071015540",
                gpi="39400010000320",
                drug_name="Atorvastatin 20mg",
                tier=1,
            )
        )
        formulary.add_drug(
            FormularyDrug(
                ndc="00069015430",
                gpi="39400050000310",
                drug_name="Lipitor 10mg",
                tier=4,
                requires_pa=True,
            )
        )

        # Add sample drugs - PPIs (GPI 4940)
        formulary.add_drug(
            FormularyDrug(
                ndc="00186077601",
                gpi="49400020000310",
                drug_name="Omeprazole 20mg",
                tier=1,
                quantity_limit=30,
                quantity_limit_days=30,
            )
        )
        formulary.add_drug(
            FormularyDrug(
                ndc="00186077831",
                gpi="49400030000310",
                drug_name="Nexium 20mg",
                tier=4,
                requires_step_therapy=True,
                step_therapy_group="PPI",
            )
        )

        # Add sample drugs - Diabetes (GPI 2710, 2720)
        formulary.add_drug(
            FormularyDrug(
                ndc="00002814001",
                gpi="27100030000310",
                drug_name="Metformin 500mg",
                tier=1,
            )
        )
        formulary.add_drug(
            FormularyDrug(
                ndc="00169413512",
                gpi="27200060003120",
                drug_name="Ozempic 0.5mg",
                tier=5,
                requires_pa=True,
                max_days_supply=28,
            )
        )

        # Add sample drugs - Anticoagulants (GPI 8330)
        formulary.add_drug(
            FormularyDrug(
                ndc="00056017270",
                gpi="83300010000330",
                drug_name="Warfarin 5mg",
                tier=1,
            )
        )
        formulary.add_drug(
            FormularyDrug(
                ndc="00597002860",
                gpi="83370030100320",
                drug_name="Eliquis 5mg",
                tier=3,
            )
        )

        # Add sample drugs - Controlled (GPI 6510)
        formulary.add_drug(
            FormularyDrug(
                ndc="00591024601",
                gpi="65100020201020",
                drug_name="Adderall 20mg",
                tier=2,
                requires_pa=True,
                quantity_limit=60,
                quantity_limit_days=30,
                max_age=65,
            )
        )

        return formulary

    def generate_medicare_part_d(self) -> Formulary:
        """Generate Medicare Part D formulary."""
        formulary = Formulary(
            formulary_id="MED-D-2025",
            name="Medicare Part D 5-Tier",
            effective_date="2025-01-01",
            tiers=[
                FormularyTier(
                    tier_number=1,
                    tier_name="Preferred Generic",
                    copay_amount=Decimal("5"),
                ),
                FormularyTier(
                    tier_number=2,
                    tier_name="Generic",
                    copay_amount=Decimal("15"),
                ),
                FormularyTier(
                    tier_number=3,
                    tier_name="Preferred Brand",
                    copay_amount=Decimal("47"),
                ),
                FormularyTier(
                    tier_number=4,
                    tier_name="Non-Preferred",
                    coinsurance_percent=Decimal("40"),
                ),
                FormularyTier(
                    tier_number=5,
                    tier_name="Specialty",
                    coinsurance_percent=Decimal("25"),
                ),
            ],
        )

        # Add common Medicare drugs
        formulary.add_drug(
            FormularyDrug(
                ndc="00071015523",
                gpi="39400010000310",
                drug_name="Atorvastatin 10mg",
                tier=1,
            )
        )
        formulary.add_drug(
            FormularyDrug(
                ndc="00002814001",
                gpi="27100030000310",
                drug_name="Metformin 500mg",
                tier=1,
            )
        )
        formulary.add_drug(
            FormularyDrug(
                ndc="00056017270",
                gpi="83300010000330",
                drug_name="Warfarin 5mg",
                tier=1,
            )
        )

        return formulary

    def generate_specialty(self) -> Formulary:
        """Generate specialty-only formulary."""
        formulary = Formulary(
            formulary_id="SPEC-2025",
            name="Specialty Formulary",
            effective_date="2025-01-01",
            tiers=[
                FormularyTier(
                    tier_number=1,
                    tier_name="Preferred Specialty",
                    coinsurance_percent=Decimal("20"),
                ),
                FormularyTier(
                    tier_number=2,
                    tier_name="Non-Preferred Specialty",
                    coinsurance_percent=Decimal("30"),
                ),
            ],
        )

        # Add specialty drugs
        formulary.add_drug(
            FormularyDrug(
                ndc="00074320502",
                gpi="66400020001020",
                drug_name="Humira 40mg",
                tier=1,
                requires_pa=True,
                requires_step_therapy=True,
                step_therapy_group="TNF",
                max_days_supply=28,
            )
        )
        formulary.add_drug(
            FormularyDrug(
                ndc="00169413512",
                gpi="27200060003120",
                drug_name="Ozempic 0.5mg",
                tier=1,
                requires_pa=True,
                max_days_supply=28,
            )
        )

        return formulary
