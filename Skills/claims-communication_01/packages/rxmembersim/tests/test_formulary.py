"""Tests for formulary module."""
from datetime import date, timedelta
from decimal import Decimal

from rxmembersim.formulary.formulary import (
    Formulary,
    FormularyDrug,
    FormularyGenerator,
    FormularyTier,
)
from rxmembersim.formulary.quantity_limit import (
    QuantityLimit,
    QuantityLimitManager,
    QuantityLimitType,
)
from rxmembersim.formulary.step_therapy import (
    StepTherapyManager,
)


class TestFormulary:
    """Tests for Formulary model."""

    def test_check_covered_drug(self) -> None:
        """Test checking a covered drug."""
        formulary = FormularyGenerator().generate_standard_commercial()
        status = formulary.check_coverage("00071015523")  # Atorvastatin

        assert status.covered is True
        assert status.tier == 1
        assert status.tier_name == "Preferred Generic"
        assert status.copay == Decimal("10")

    def test_check_not_covered(self) -> None:
        """Test checking a drug not on formulary."""
        formulary = FormularyGenerator().generate_standard_commercial()
        status = formulary.check_coverage("99999999999")

        assert status.covered is False
        assert status.message == "Drug not on formulary"

    def test_check_drug_with_pa(self) -> None:
        """Test checking a drug requiring prior auth."""
        formulary = FormularyGenerator().generate_standard_commercial()
        status = formulary.check_coverage("00069015430")  # Brand Lipitor

        assert status.covered is True
        assert status.requires_pa is True

    def test_check_drug_with_step_therapy(self) -> None:
        """Test checking a drug requiring step therapy."""
        formulary = FormularyGenerator().generate_standard_commercial()
        status = formulary.check_coverage("00186077831")  # Brand Nexium

        assert status.covered is True
        assert status.requires_step_therapy is True
        assert status.step_therapy_group == "PPI"

    def test_check_drug_with_quantity_limit(self) -> None:
        """Test checking a drug with quantity limits."""
        formulary = FormularyGenerator().generate_standard_commercial()
        status = formulary.check_coverage("00186077601")  # Omeprazole

        assert status.covered is True
        assert status.quantity_limit == 30
        assert status.quantity_limit_days == 30

    def test_add_drug_to_formulary(self) -> None:
        """Test adding a drug to formulary."""
        formulary = Formulary(
            formulary_id="TEST-001",
            name="Test Formulary",
            effective_date="2025-01-01",
            tiers=[
                FormularyTier(
                    tier_number=1,
                    tier_name="Generic",
                    copay_amount=Decimal("10"),
                )
            ],
        )

        formulary.add_drug(
            FormularyDrug(
                ndc="12345678901",
                gpi="12340010000310",
                drug_name="Test Drug",
                tier=1,
            )
        )

        status = formulary.check_coverage("12345678901")
        assert status.covered is True

    def test_remove_drug_from_formulary(self) -> None:
        """Test removing a drug from formulary."""
        formulary = FormularyGenerator().generate_standard_commercial()

        # Verify drug exists
        assert formulary.check_coverage("00071015523").covered is True

        # Remove drug
        result = formulary.remove_drug("00071015523")
        assert result is True

        # Verify drug no longer covered
        assert formulary.check_coverage("00071015523").covered is False

    def test_get_drugs_by_tier(self) -> None:
        """Test getting drugs by tier."""
        formulary = FormularyGenerator().generate_standard_commercial()

        tier1_drugs = formulary.get_drugs_by_tier(1)
        assert len(tier1_drugs) > 0
        assert all(d.tier == 1 for d in tier1_drugs)

    def test_get_drugs_requiring_pa(self) -> None:
        """Test getting drugs requiring PA."""
        formulary = FormularyGenerator().generate_standard_commercial()

        pa_drugs = formulary.get_drugs_requiring_pa()
        assert len(pa_drugs) > 0
        assert all(d.requires_pa for d in pa_drugs)

    def test_get_drugs_by_gpi(self) -> None:
        """Test getting drugs by GPI prefix."""
        formulary = FormularyGenerator().generate_standard_commercial()

        # Get statins (GPI 3940)
        statins = formulary.get_drugs_by_gpi("3940")
        assert len(statins) > 0


class TestFormularyGenerator:
    """Tests for FormularyGenerator."""

    def test_generate_standard_commercial(self) -> None:
        """Test generating standard commercial formulary."""
        generator = FormularyGenerator()
        formulary = generator.generate_standard_commercial()

        assert formulary.formulary_id == "COMM-STD-2025"
        assert len(formulary.tiers) == 5
        assert len(formulary.drugs) > 0

    def test_generate_medicare_part_d(self) -> None:
        """Test generating Medicare Part D formulary."""
        generator = FormularyGenerator()
        formulary = generator.generate_medicare_part_d()

        assert formulary.formulary_id == "MED-D-2025"
        assert len(formulary.tiers) == 5

    def test_generate_specialty(self) -> None:
        """Test generating specialty formulary."""
        generator = FormularyGenerator()
        formulary = generator.generate_specialty()

        assert formulary.formulary_id == "SPEC-2025"
        assert len(formulary.tiers) == 2


class TestStepTherapy:
    """Tests for Step Therapy."""

    def test_step_therapy_satisfied(self) -> None:
        """Test step therapy when requirements are met."""
        manager = StepTherapyManager()
        protocol = manager.get_protocol("PPI-ST")
        assert protocol is not None

        # Create history with generic PPI fills
        claim_history = [
            type(
                "Claim",
                (),
                {
                    "ndc": "00186077601",
                    "gpi": "49400020000310",
                    "service_date": date.today() - timedelta(days=45),
                    "days_supply": 30,
                },
            )(),
            type(
                "Claim",
                (),
                {
                    "ndc": "00186077601",
                    "gpi": "49400020000310",
                    "service_date": date.today() - timedelta(days=15),
                    "days_supply": 30,
                },
            )(),
        ]

        result = protocol.check_satisfied(
            target_ndc="00186077831",  # Brand Nexium
            claim_history=claim_history,
            service_date=date.today(),
        )

        assert result.satisfied is True

    def test_step_therapy_not_satisfied(self) -> None:
        """Test step therapy when requirements not met."""
        manager = StepTherapyManager()
        protocol = manager.get_protocol("PPI-ST")
        assert protocol is not None

        # Empty claim history
        result = protocol.check_satisfied(
            target_ndc="00186077831",
            claim_history=[],
            service_date=date.today(),
        )

        assert result.satisfied is False
        assert result.failed_step == 1
        assert len(result.required_drugs) > 0

    def test_find_protocol_for_drug(self) -> None:
        """Test finding step therapy protocol for a drug."""
        manager = StepTherapyManager()

        protocol = manager.find_protocol_for_drug("00186077831")  # Brand Nexium
        assert protocol is not None
        assert protocol.protocol_id == "PPI-ST"

    def test_no_protocol_for_drug(self) -> None:
        """Test when no step therapy applies."""
        manager = StepTherapyManager()

        protocol = manager.find_protocol_for_drug("00071015523")  # Generic statin
        assert protocol is None


class TestQuantityLimit:
    """Tests for Quantity Limits."""

    def test_per_fill_limit_passed(self) -> None:
        """Test per-fill limit when quantity is within limit."""
        manager = QuantityLimitManager()

        result = manager.check_quantity_limit(
            ndc="00000000001",
            gpi="65100020201020",  # CNS Stimulant
            requested_quantity=Decimal("30"),
            requested_days_supply=30,
        )

        assert result.passed is True

    def test_per_fill_limit_exceeded(self) -> None:
        """Test per-fill limit when quantity exceeds limit."""
        manager = QuantityLimitManager()

        result = manager.check_quantity_limit(
            ndc="00000000001",
            gpi="65100020201020",  # CNS Stimulant
            requested_quantity=Decimal("90"),
            requested_days_supply=30,
        )

        assert result.passed is False
        assert result.allowed_quantity == Decimal("60")
        assert "exceeds limit" in result.message.lower()

    def test_days_supply_limit_exceeded(self) -> None:
        """Test days supply limit exceeded."""
        manager = QuantityLimitManager()

        result = manager.check_quantity_limit(
            ndc="00000000001",
            gpi="27200060003120",  # GLP-1
            requested_quantity=Decimal("1"),
            requested_days_supply=90,
        )

        assert result.passed is False
        assert result.allowed_days_supply == 28

    def test_accumulating_limit(self) -> None:
        """Test accumulating monthly limit."""
        manager = QuantityLimitManager()

        # Add triptan limit manually
        manager.add_limit(
            QuantityLimit(
                limit_id="TEST-TRIPTAN",
                drug_identifier="00000000001",
                limit_type=QuantityLimitType.PER_MONTH,
                max_quantity=Decimal("9"),
                period_days=30,
            )
        )

        # Previous fill this month
        claim_history = [
            type(
                "Claim",
                (),
                {
                    "ndc": "00000000001",
                    "service_date": date.today() - timedelta(days=10),
                    "quantity_dispensed": Decimal("6"),
                },
            )()
        ]

        result = manager.check_quantity_limit(
            ndc="00000000001",
            gpi=None,
            requested_quantity=Decimal("6"),
            requested_days_supply=30,
            claim_history=claim_history,
            service_date=date.today(),
        )

        assert result.passed is False
        assert result.quantity_used_in_period == Decimal("6")
        assert result.quantity_remaining_in_period == Decimal("3")

    def test_no_limit_applies(self) -> None:
        """Test when no quantity limit applies."""
        manager = QuantityLimitManager()

        result = manager.check_quantity_limit(
            ndc="99999999999",
            gpi="99990000000000",
            requested_quantity=Decimal("100"),
            requested_days_supply=90,
        )

        assert result.passed is True
        assert "No quantity limits apply" in result.message
