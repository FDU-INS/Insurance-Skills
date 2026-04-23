"""Tests for benefit accumulators."""

from decimal import Decimal

from healthsim.benefits import (
    Accumulator,
    AccumulatorLevel,
    AccumulatorSet,
    AccumulatorType,
    BenefitType,
    NetworkTier,
    create_integrated_accumulators,
    create_medical_accumulators,
    create_pharmacy_accumulators,
)


class TestAccumulator:
    """Tests for single Accumulator."""

    def test_create_deductible(self):
        """Test creating a deductible accumulator."""
        acc = Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            limit=Decimal("500"),
            plan_year=2024,
        )
        assert acc.limit == Decimal("500")
        assert acc.applied == Decimal("0")
        assert acc.remaining == Decimal("500")
        assert acc.met is False
        assert acc.percent_used == 0.0

    def test_apply_amount(self):
        """Test applying amount to accumulator."""
        acc = Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            limit=Decimal("500"),
            plan_year=2024,
        )

        new_acc, applied = acc.apply(Decimal("150"))

        assert applied == Decimal("150")
        assert new_acc.applied == Decimal("150")
        assert new_acc.remaining == Decimal("350")
        assert new_acc.met is False
        # Original is immutable
        assert acc.applied == Decimal("0")

    def test_apply_exceeds_limit(self):
        """Test applying amount that exceeds limit."""
        acc = Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            limit=Decimal("100"),
            applied=Decimal("80"),
            plan_year=2024,
        )

        new_acc, applied = acc.apply(Decimal("50"))

        assert applied == Decimal("20")  # Only 20 remaining
        assert new_acc.applied == Decimal("100")
        assert new_acc.remaining == Decimal("0")
        assert new_acc.met is True
        assert new_acc.percent_used == 100.0

    def test_apply_when_already_met(self):
        """Test applying amount when already met."""
        acc = Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            limit=Decimal("100"),
            applied=Decimal("100"),
            plan_year=2024,
        )

        new_acc, applied = acc.apply(Decimal("50"))

        assert applied == Decimal("0")
        assert new_acc.applied == Decimal("100")

    def test_reset(self):
        """Test resetting accumulator for new year."""
        acc = Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            limit=Decimal("500"),
            applied=Decimal("450"),
            plan_year=2024,
        )

        new_acc = acc.reset(2025)

        assert new_acc.applied == Decimal("0")
        assert new_acc.plan_year == 2025
        assert new_acc.limit == Decimal("500")  # Limit unchanged
        # Original unchanged
        assert acc.applied == Decimal("450")
        assert acc.plan_year == 2024

    def test_network_tier_default(self):
        """Test default network tier is in-network."""
        acc = Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            limit=Decimal("500"),
            plan_year=2024,
        )
        assert acc.network_tier == NetworkTier.IN_NETWORK

    def test_benefit_type_default(self):
        """Test default benefit type is combined."""
        acc = Accumulator(
            accumulator_type=AccumulatorType.DEDUCTIBLE,
            level=AccumulatorLevel.INDIVIDUAL,
            limit=Decimal("500"),
            plan_year=2024,
        )
        assert acc.benefit_type == BenefitType.COMBINED


class TestAccumulatorSet:
    """Tests for AccumulatorSet."""

    def test_create_empty_set(self):
        """Test creating empty accumulator set."""
        acc_set = AccumulatorSet(
            member_id="MEM-001",
            plan_year=2024,
        )
        assert acc_set.member_id == "MEM-001"
        assert acc_set.deductible_individual_in is None

    def test_apply_to_deductible_individual(self):
        """Test applying to individual deductible."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        new_set, applied = acc_set.apply_to_deductible(Decimal("200"))

        assert applied == Decimal("200")
        assert new_set.deductible_individual_in.applied == Decimal("200")
        assert new_set.deductible_individual_in.remaining == Decimal("300")
        # Family also updated
        assert new_set.deductible_family_in.applied == Decimal("200")

    def test_apply_to_deductible_family_met(self):
        """Test deductible when family limit met."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1000"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        # Manually set family deductible as met
        acc_set = acc_set.model_copy(
            update={
                "deductible_family_in": acc_set.deductible_family_in.model_copy(
                    update={"applied": Decimal("1000")}
                )
            }
        )

        # Try to apply more
        new_set, applied = acc_set.apply_to_deductible(Decimal("200"))

        # Nothing applied because family is met
        assert applied == Decimal("0")
        assert new_set.is_deductible_met() is True

    def test_apply_to_oop(self):
        """Test applying to OOP accumulator."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        new_set, applied = acc_set.apply_to_oop(Decimal("500"))

        assert applied == Decimal("500")
        assert new_set.oop_individual_in.applied == Decimal("500")
        assert new_set.oop_family_in.applied == Decimal("500")

    def test_out_of_network(self):
        """Test out-of-network accumulator tracking."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        new_set, applied = acc_set.apply_to_deductible(
            Decimal("200"), network=NetworkTier.OUT_OF_NETWORK
        )

        assert applied == Decimal("200")
        assert new_set.deductible_individual_out.applied == Decimal("200")
        # In-network unchanged
        assert new_set.deductible_individual_in.applied == Decimal("0")

    def test_is_deductible_met(self):
        """Test deductible met check."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        assert acc_set.is_deductible_met() is False

        # Apply full deductible
        new_set, _ = acc_set.apply_to_deductible(Decimal("500"))

        assert new_set.is_deductible_met() is True

    def test_get_remaining(self):
        """Test getting remaining amounts."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        assert acc_set.get_deductible_remaining() == Decimal("500")
        assert acc_set.get_oop_remaining() == Decimal("3000")

        new_set, _ = acc_set.apply_to_deductible(Decimal("200"))
        new_set, _ = new_set.apply_to_oop(Decimal("200"))

        assert new_set.get_deductible_remaining() == Decimal("300")
        assert new_set.get_oop_remaining() == Decimal("2800")

    def test_reset_for_new_year(self):
        """Test resetting all accumulators for new year."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        # Apply some amounts
        acc_set, _ = acc_set.apply_to_deductible(Decimal("300"))
        acc_set, _ = acc_set.apply_to_oop(Decimal("1000"))

        # Reset for 2025
        new_set = acc_set.reset_for_new_year(2025)

        assert new_set.plan_year == 2025
        assert new_set.deductible_individual_in.applied == Decimal("0")
        assert new_set.oop_individual_in.applied == Decimal("0")
        assert new_set.deductible_individual_in.plan_year == 2025


class TestCreateMedicalAccumulators:
    """Tests for create_medical_accumulators factory."""

    def test_creates_all_accumulators(self):
        """Test all accumulators are created."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        # In-network
        assert acc_set.deductible_individual_in is not None
        assert acc_set.deductible_family_in is not None
        assert acc_set.oop_individual_in is not None
        assert acc_set.oop_family_in is not None

        # Out-of-network
        assert acc_set.deductible_individual_out is not None
        assert acc_set.oop_individual_out is not None

    def test_default_oon_is_2x(self):
        """Test OON defaults to 2x in-network."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        assert acc_set.deductible_individual_out.limit == Decimal("1000")
        assert acc_set.oop_individual_out.limit == Decimal("6000")

    def test_custom_oon_values(self):
        """Test custom OON values."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
            deductible_individual_oon=Decimal("750"),
            oop_individual_oon=Decimal("5000"),
        )

        assert acc_set.deductible_individual_out.limit == Decimal("750")
        assert acc_set.oop_individual_out.limit == Decimal("5000")

    def test_benefit_type_is_medical(self):
        """Test benefit type is set to medical."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        assert acc_set.deductible_individual_in.benefit_type == BenefitType.MEDICAL


class TestCreatePharmacyAccumulators:
    """Tests for create_pharmacy_accumulators factory."""

    def test_creates_rx_accumulators(self):
        """Test Rx accumulators are created."""
        acc_set = create_pharmacy_accumulators(
            member_id="RXM-001",
            plan_year=2024,
            deductible=Decimal("100"),
            oop_max=Decimal("2000"),
        )

        assert acc_set.rx_deductible is not None
        assert acc_set.rx_oop is not None
        assert acc_set.specialty_oop is None  # Not specified

    def test_with_specialty_oop(self):
        """Test creating with specialty OOP."""
        acc_set = create_pharmacy_accumulators(
            member_id="RXM-001",
            plan_year=2024,
            deductible=Decimal("100"),
            oop_max=Decimal("2000"),
            specialty_oop=Decimal("500"),
        )

        assert acc_set.specialty_oop is not None
        assert acc_set.specialty_oop.limit == Decimal("500")

    def test_benefit_type_is_pharmacy(self):
        """Test benefit type is set to pharmacy."""
        acc_set = create_pharmacy_accumulators(
            member_id="RXM-001",
            plan_year=2024,
            deductible=Decimal("100"),
            oop_max=Decimal("2000"),
        )

        assert acc_set.rx_deductible.benefit_type == BenefitType.PHARMACY
        assert acc_set.rx_oop.benefit_type == BenefitType.PHARMACY

    def test_network_tier_is_preferred_pharmacy(self):
        """Test network tier is preferred pharmacy."""
        acc_set = create_pharmacy_accumulators(
            member_id="RXM-001",
            plan_year=2024,
            deductible=Decimal("100"),
            oop_max=Decimal("2000"),
        )

        assert acc_set.rx_deductible.network_tier == NetworkTier.PREFERRED_PHARMACY

    def test_apply_to_pharmacy_deductible(self):
        """Test applying to pharmacy-specific deductible."""
        acc_set = create_pharmacy_accumulators(
            member_id="RXM-001",
            plan_year=2024,
            deductible=Decimal("100"),
            oop_max=Decimal("2000"),
        )

        new_set, applied = acc_set.apply_to_deductible(
            Decimal("45"), benefit_type=BenefitType.PHARMACY
        )

        assert applied == Decimal("45")
        assert new_set.rx_deductible.applied == Decimal("45")
        assert new_set.rx_deductible.remaining == Decimal("55")


class TestCreateIntegratedAccumulators:
    """Tests for create_integrated_accumulators factory."""

    def test_creates_combined_accumulators(self):
        """Test combined accumulators are created."""
        acc_set = create_integrated_accumulators(
            member_id="INT-001",
            plan_year=2024,
            deductible_individual=Decimal("750"),
            deductible_family=Decimal("2250"),
            oop_individual=Decimal("4000"),
            oop_family=Decimal("8000"),
        )

        assert acc_set.deductible_individual_in is not None
        assert acc_set.deductible_family_in is not None
        assert acc_set.oop_individual_in is not None
        assert acc_set.oop_family_in is not None

    def test_benefit_type_is_combined(self):
        """Test benefit type is combined."""
        acc_set = create_integrated_accumulators(
            member_id="INT-001",
            plan_year=2024,
            deductible_individual=Decimal("750"),
            deductible_family=Decimal("2250"),
            oop_individual=Decimal("4000"),
            oop_family=Decimal("8000"),
        )

        assert acc_set.deductible_individual_in.benefit_type == BenefitType.COMBINED

    def test_no_oon_accumulators(self):
        """Test no OON accumulators for integrated plans."""
        acc_set = create_integrated_accumulators(
            member_id="INT-001",
            plan_year=2024,
            deductible_individual=Decimal("750"),
            deductible_family=Decimal("2250"),
            oop_individual=Decimal("4000"),
            oop_family=Decimal("8000"),
        )

        assert acc_set.deductible_individual_out is None
        assert acc_set.oop_individual_out is None


class TestNetworkTierClassification:
    """Tests for network tier classification."""

    def test_in_network_tiers(self):
        """Test tiers classified as in-network."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        # These should all use in-network accumulators
        for tier in [
            NetworkTier.IN_NETWORK,
            NetworkTier.TIER_1,
            NetworkTier.TIER_2,
            NetworkTier.PREFERRED_PHARMACY,
            NetworkTier.MAIL_ORDER,
        ]:
            new_set, applied = acc_set.apply_to_deductible(Decimal("100"), network=tier)
            assert new_set.deductible_individual_in.applied == Decimal("100")

    def test_out_of_network_tiers(self):
        """Test tiers classified as out-of-network."""
        acc_set = create_medical_accumulators(
            member_id="MEM-001",
            plan_year=2024,
            deductible_individual=Decimal("500"),
            deductible_family=Decimal("1500"),
            oop_individual=Decimal("3000"),
            oop_family=Decimal("6000"),
        )

        for tier in [NetworkTier.OUT_OF_NETWORK, NetworkTier.TIER_3]:
            # Reset for each test
            test_set = acc_set
            new_set, applied = test_set.apply_to_deductible(Decimal("100"), network=tier)
            assert new_set.deductible_individual_out.applied == Decimal("100")
            assert new_set.deductible_individual_in.applied == Decimal("0")
