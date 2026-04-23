"""Tests for core models."""
from datetime import date
from decimal import Decimal

import pytest

from rxmembersim.claims.adjudication import AdjudicationEngine
from rxmembersim.claims.claim import PharmacyClaim, TransactionCode
from rxmembersim.core.drug import DEASchedule, DrugReference
from rxmembersim.core.member import (
    BenefitAccumulators,
    MemberDemographics,
    RxMember,
    RxMemberFactory,
)
from rxmembersim.core.prescription import DAWCode, Prescription
from rxmembersim.formulary.formulary import FormularyGenerator


class TestRxMember:
    """Tests for RxMember model."""

    def test_generate_member(self) -> None:
        """Test generating a member."""
        generator = RxMemberFactory()
        member = generator.generate()
        assert member.member_id.startswith("RXM-")
        assert len(member.bin) == 6

    def test_member_accumulators(self) -> None:
        """Test member accumulators."""
        generator = RxMemberFactory()
        member = generator.generate()
        assert member.accumulators.deductible_remaining >= 0
        assert member.accumulators.oop_remaining >= 0

    def test_member_demographics(self) -> None:
        """Test member demographics are populated."""
        generator = RxMemberFactory()
        member = generator.generate()
        assert member.demographics.first_name
        assert member.demographics.last_name
        assert member.demographics.date_of_birth
        assert member.demographics.gender in ["M", "F"]

    def test_member_with_custom_bin_pcn(self) -> None:
        """Test generating member with custom BIN/PCN."""
        generator = RxMemberFactory()
        member = generator.generate(bin="999999", pcn="CUSTOM", group_number="TEST01")
        assert member.bin == "999999"
        assert member.pcn == "CUSTOM"
        assert member.group_number == "TEST01"


class TestDrugReference:
    """Tests for DrugReference model."""

    def test_create_drug(self) -> None:
        """Test creating a drug reference."""
        drug = DrugReference(
            ndc="00071015523",
            drug_name="Lipitor",
            generic_name="atorvastatin calcium",
            gpi="39400010000310",
            therapeutic_class="HMG-CoA Reductase Inhibitors",
            strength="10 MG",
            dosage_form="TABLET",
            route_of_admin="ORAL",
        )
        assert drug.ndc == "00071015523"
        assert drug.drug_name == "Lipitor"
        assert drug.dea_schedule == DEASchedule.NON_CONTROLLED

    def test_controlled_substance(self) -> None:
        """Test controlled substance drug."""
        drug = DrugReference(
            ndc="00591024601",
            drug_name="Adderall",
            generic_name="amphetamine/dextroamphetamine",
            gpi="61100020100110",
            therapeutic_class="CNS Stimulants",
            strength="20 MG",
            dosage_form="TABLET",
            route_of_admin="ORAL",
            dea_schedule=DEASchedule.SCHEDULE_II,
        )
        assert drug.dea_schedule == DEASchedule.SCHEDULE_II

    def test_brand_drug(self) -> None:
        """Test brand drug flag."""
        drug = DrugReference(
            ndc="00071015523",
            drug_name="Lipitor",
            generic_name="atorvastatin calcium",
            gpi="39400010000310",
            therapeutic_class="HMG-CoA Reductase Inhibitors",
            strength="10 MG",
            dosage_form="TABLET",
            route_of_admin="ORAL",
            is_brand=True,
            multi_source_code="N",
        )
        assert drug.is_brand is True
        assert drug.multi_source_code == "N"


class TestPrescription:
    """Tests for Prescription model."""

    def test_create_prescription(self) -> None:
        """Test creating a prescription."""
        rx = Prescription(
            prescription_number="RX123456",
            ndc="00071015523",
            drug_name="Lipitor 10mg",
            quantity_prescribed=Decimal("30"),
            days_supply=30,
            refills_authorized=5,
            refills_remaining=5,
            prescriber_npi="1234567890",
            written_date=date(2025, 1, 1),
            expiration_date=date(2026, 1, 1),
        )
        assert rx.prescription_number == "RX123456"
        assert rx.daw_code == DAWCode.NO_SELECTION

    def test_prescription_with_daw(self) -> None:
        """Test prescription with DAW code."""
        rx = Prescription(
            prescription_number="RX123456",
            ndc="00071015523",
            drug_name="Lipitor 10mg",
            quantity_prescribed=Decimal("30"),
            days_supply=30,
            refills_authorized=5,
            refills_remaining=5,
            prescriber_npi="1234567890",
            written_date=date(2025, 1, 1),
            expiration_date=date(2026, 1, 1),
            daw_code=DAWCode.SUBSTITUTION_NOT_ALLOWED,
        )
        assert rx.daw_code == DAWCode.SUBSTITUTION_NOT_ALLOWED


class TestPharmacyClaim:
    """Tests for PharmacyClaim model."""

    def test_create_claim(self) -> None:
        """Test creating a pharmacy claim."""
        claim = PharmacyClaim(
            claim_id="CLM001",
            transaction_code=TransactionCode.BILLING,
            service_date=date(2025, 1, 15),
            pharmacy_npi="1234567890",
            member_id="MEM001",
            cardholder_id="CH001",
            person_code="01",
            bin="610014",
            pcn="RXTEST",
            group_number="GRP001",
            prescription_number="RX123",
            fill_number=1,
            ndc="00071015523",
            quantity_dispensed=Decimal("30"),
            days_supply=30,
            daw_code="0",
            prescriber_npi="0987654321",
            ingredient_cost_submitted=Decimal("150.00"),
            dispensing_fee_submitted=Decimal("2.50"),
            usual_customary_charge=Decimal("175.00"),
            gross_amount_due=Decimal("152.50"),
        )
        assert claim.claim_id == "CLM001"
        assert claim.transaction_code == TransactionCode.BILLING


class TestAdjudicationEngine:
    """Tests for AdjudicationEngine."""

    @pytest.fixture
    def member(self) -> RxMember:
        """Create a test member."""
        return RxMember(
            member_id="MEM001",
            cardholder_id="CH001",
            person_code="01",
            bin="610014",
            pcn="RXTEST",
            group_number="GRP001",
            demographics=MemberDemographics(
                first_name="John",
                last_name="Doe",
                date_of_birth=date(1980, 5, 15),
                gender="M",
            ),
            effective_date=date(2025, 1, 1),
            accumulators=BenefitAccumulators(
                deductible_remaining=Decimal("250"),
                oop_remaining=Decimal("3000"),
            ),
        )

    @pytest.fixture
    def claim(self) -> PharmacyClaim:
        """Create a test claim."""
        return PharmacyClaim(
            claim_id="CLM001",
            transaction_code=TransactionCode.BILLING,
            service_date=date(2025, 1, 15),
            pharmacy_npi="1234567890",
            member_id="MEM001",
            cardholder_id="CH001",
            person_code="01",
            bin="610014",
            pcn="RXTEST",
            group_number="GRP001",
            prescription_number="RX123",
            fill_number=1,
            ndc="00071015523",
            quantity_dispensed=Decimal("30"),
            days_supply=30,
            daw_code="0",
            prescriber_npi="0987654321",
            ingredient_cost_submitted=Decimal("150.00"),
            dispensing_fee_submitted=Decimal("2.50"),
            usual_customary_charge=Decimal("175.00"),
            gross_amount_due=Decimal("152.50"),
        )

    def test_adjudicate_approved_claim(
        self, member: RxMember, claim: PharmacyClaim
    ) -> None:
        """Test adjudicating an approved claim."""
        # Use formulary with the drug on it
        formulary = FormularyGenerator().generate_standard_commercial()
        engine = AdjudicationEngine(formulary=formulary)
        response = engine.adjudicate(claim, member)

        assert response.response_status == "P"
        assert response.authorization_number is not None
        assert response.total_amount_paid is not None
        assert response.patient_pay_amount is not None

    def test_adjudicate_ineligible_member(
        self, member: RxMember, claim: PharmacyClaim
    ) -> None:
        """Test adjudicating claim for ineligible member."""
        # Set termination date before service date
        member.termination_date = date(2025, 1, 10)

        engine = AdjudicationEngine()
        response = engine.adjudicate(claim, member)

        assert response.response_status == "R"
        assert any(rc.code == "65" for rc in response.reject_codes)

    def test_adjudicate_wrong_bin(
        self, member: RxMember, claim: PharmacyClaim
    ) -> None:
        """Test adjudicating claim with wrong BIN."""
        claim.bin = "999999"

        engine = AdjudicationEngine()
        response = engine.adjudicate(claim, member)

        assert response.response_status == "R"
        assert any(rc.code == "25" for rc in response.reject_codes)

    def test_pricing_with_deductible(
        self, member: RxMember, claim: PharmacyClaim
    ) -> None:
        """Test pricing applies deductible correctly."""
        formulary = FormularyGenerator().generate_standard_commercial()
        engine = AdjudicationEngine(formulary=formulary)
        response = engine.adjudicate(claim, member)

        assert response.response_status == "P"
        # With $250 deductible and $152.50 claim, full deductible applies
        assert response.deductible_amount is not None
        assert response.deductible_amount <= member.accumulators.deductible_remaining
