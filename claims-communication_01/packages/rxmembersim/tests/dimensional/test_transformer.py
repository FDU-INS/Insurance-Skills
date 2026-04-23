"""Tests for RxMemberSim Dimensional Transformer."""

from datetime import date, datetime
from decimal import Decimal

import pytest

from rxmembersim.authorization.prior_auth import (
    PARequestType,
    PAStatus,
    PriorAuthRecord,
    PriorAuthRequest,
    PriorAuthResponse,
)
from rxmembersim.claims.claim import PharmacyClaim, TransactionCode
from rxmembersim.core.drug import DEASchedule, DrugReference
from rxmembersim.core.member import BenefitAccumulators, MemberDemographics, RxMember
from rxmembersim.core.pharmacy import Pharmacy, PharmacyType
from rxmembersim.core.prescriber import Prescriber, PrescriberSpecialty, PrescriberType
from rxmembersim.dimensional import RxMemberSimDimensionalTransformer
from rxmembersim.formulary.formulary import Formulary, FormularyDrug, FormularyTier


@pytest.fixture
def sample_member():
    """Sample RxMember for testing."""
    return RxMember(
        member_id="RXM-00000001",
        cardholder_id="123456789",
        person_code="01",
        bin="610014",
        pcn="RXTEST",
        group_number="GRP001",
        demographics=MemberDemographics(
            first_name="John",
            last_name="Smith",
            date_of_birth=date(1980, 5, 15),
            gender="M",
            address_line1="123 Main St",
            city="Anytown",
            state="TX",
            zip_code="75001",
        ),
        effective_date=date(2024, 1, 1),
        accumulators=BenefitAccumulators(
            deductible_met=Decimal("100"),
            deductible_remaining=Decimal("150"),
            oop_met=Decimal("500"),
            oop_remaining=Decimal("2500"),
        ),
        plan_code="COMMERCIAL",
        formulary_id="FORM001",
    )


@pytest.fixture
def sample_drug():
    """Sample DrugReference for testing."""
    return DrugReference(
        ndc="00071015523",
        drug_name="Atorvastatin 10mg",
        generic_name="Atorvastatin Calcium",
        gpi="39400010000310",
        therapeutic_class="Antihyperlipidemic - HMG CoA Reductase Inhibitors",
        strength="10mg",
        dosage_form="Tablet",
        route_of_admin="Oral",
        dea_schedule=DEASchedule.NON_CONTROLLED,
        is_brand=False,
        multi_source_code="Y",
        awp=15.50,
        wac=12.25,
    )


@pytest.fixture
def sample_pharmacy():
    """Sample Pharmacy for testing."""
    return Pharmacy(
        ncpdp_id="1234567",
        npi="1234567890",
        name="CVS Pharmacy #1234",
        pharmacy_type=PharmacyType.RETAIL,
        address_line1="456 Oak Ave",
        city="Anytown",
        state="TX",
        zip_code="75001",
        phone="555-123-4567",
        in_network=True,
        preferred=True,
        chain_code="CVS",
        chain_name="CVS Pharmacy",
    )


@pytest.fixture
def sample_prescriber():
    """Sample Prescriber for testing."""
    return Prescriber(
        npi="1987654321",
        dea="AB1234567",
        first_name="Jane",
        last_name="Doe",
        credential=PrescriberType.MD,
        specialty=PrescriberSpecialty.INTERNAL_MEDICINE,
        taxonomy_code="207R00000X",
        city="Anytown",
        state="TX",
        active=True,
        can_prescribe_controlled=True,
    )


@pytest.fixture
def sample_claim(sample_member, sample_drug, sample_pharmacy, sample_prescriber):
    """Sample PharmacyClaim for testing."""
    return PharmacyClaim(
        claim_id="CLM00000001",
        transaction_code=TransactionCode.BILLING,
        service_date=date(2024, 3, 15),
        pharmacy_npi=sample_pharmacy.npi,
        pharmacy_ncpdp=sample_pharmacy.ncpdp_id,
        member_id=sample_member.member_id,
        cardholder_id=sample_member.cardholder_id,
        person_code=sample_member.person_code,
        bin=sample_member.bin,
        pcn=sample_member.pcn,
        group_number=sample_member.group_number,
        prescription_number="RX123456",
        fill_number=0,
        ndc=sample_drug.ndc,
        quantity_dispensed=Decimal("30"),
        days_supply=30,
        daw_code="0",
        prescriber_npi=sample_prescriber.npi,
        ingredient_cost_submitted=Decimal("150.00"),
        dispensing_fee_submitted=Decimal("2.50"),
        usual_customary_charge=Decimal("160.00"),
        gross_amount_due=Decimal("152.50"),
    )


@pytest.fixture
def sample_formulary():
    """Sample Formulary for testing."""
    formulary = Formulary(
        formulary_id="FORM001",
        name="Standard Commercial 4-Tier",
        effective_date="2024-01-01",
        tiers=[
            FormularyTier(tier_number=1, tier_name="Generic", copay_amount=Decimal("10")),
            FormularyTier(tier_number=2, tier_name="Preferred Brand", copay_amount=Decimal("35")),
            FormularyTier(
                tier_number=3, tier_name="Non-Preferred Brand", copay_amount=Decimal("60")
            ),
            FormularyTier(tier_number=4, tier_name="Specialty", coinsurance_percent=Decimal("25")),
        ],
    )
    formulary.add_drug(
        FormularyDrug(
            ndc="00071015523",
            gpi="39400010000310",
            drug_name="Atorvastatin 10mg",
            tier=1,
        )
    )
    return formulary


class TestRxMemberSimDimensionalTransformer:
    """Test suite for RxMemberSimDimensionalTransformer."""

    def test_empty_transformer(self):
        """Test transformer with no data."""
        transformer = RxMemberSimDimensionalTransformer()
        dimensions, facts = transformer.transform()

        assert dimensions == {}
        assert facts == {}

    def test_transform_members_only(self, sample_member):
        """Test transformation with only members."""
        transformer = RxMemberSimDimensionalTransformer(members=[sample_member])
        dimensions, facts = transformer.transform()

        assert "dim_rx_member" in dimensions
        assert "fact_rx_eligibility_spans" in facts

        dim_member = dimensions["dim_rx_member"]
        assert len(dim_member) == 1
        assert dim_member.iloc[0]["member_id"] == "RXM-00000001"
        assert dim_member.iloc[0]["given_name"] == "John"
        assert dim_member.iloc[0]["bin"] == "610014"

    def test_dim_rx_member_structure(self, sample_member):
        """Test dim_rx_member has all required columns."""
        transformer = RxMemberSimDimensionalTransformer(members=[sample_member])
        dimensions, _ = transformer.transform()

        dim_member = dimensions["dim_rx_member"]
        required_columns = [
            "member_key", "member_id", "cardholder_id", "person_code",
            "bin", "pcn", "group_number", "given_name", "family_name",
            "full_name", "birth_date_key", "birth_date", "gender_code",
            "gender_description", "age_at_snapshot", "age_band",
            "effective_date_key", "effective_date", "deductible_met",
            "deductible_remaining", "is_cardholder",
        ]
        for col in required_columns:
            assert col in dim_member.columns, f"Missing column: {col}"

    def test_dim_medication_structure(self, sample_drug):
        """Test dim_medication has all required columns."""
        transformer = RxMemberSimDimensionalTransformer(drugs=[sample_drug])
        dimensions, _ = transformer.transform()

        dim_med = dimensions["dim_medication"]
        required_columns = [
            "medication_key", "ndc_11", "ndc_10", "drug_name", "generic_name",
            "gpi", "gpi_2", "gpi_4", "gpi_6", "therapeutic_class",
            "therapeutic_category", "strength", "dosage_form",
            "dea_schedule", "is_controlled", "is_brand", "awp", "wac",
        ]
        for col in required_columns:
            assert col in dim_med.columns, f"Missing column: {col}"

    def test_dim_medication_gpi_parsing(self, sample_drug):
        """Test GPI is correctly parsed into levels."""
        transformer = RxMemberSimDimensionalTransformer(drugs=[sample_drug])
        dimensions, _ = transformer.transform()

        dim_med = dimensions["dim_medication"]
        row = dim_med.iloc[0]

        assert row["gpi"] == "39400010000310"
        assert row["gpi_2"] == "39"
        assert row["gpi_4"] == "3940"
        assert row["gpi_6"] == "394000"
        assert row["therapeutic_category"] == "Antihyperlipidemic Agents"

    def test_dim_pharmacy_structure(self, sample_pharmacy):
        """Test dim_pharmacy has all required columns."""
        transformer = RxMemberSimDimensionalTransformer(pharmacies=[sample_pharmacy])
        dimensions, _ = transformer.transform()

        dim_pharm = dimensions["dim_pharmacy"]
        required_columns = [
            "pharmacy_key", "pharmacy_npi", "ncpdp_id", "pharmacy_name",
            "pharmacy_type", "pharmacy_category", "city", "state",
            "in_network", "preferred", "chain_code", "chain_name",
        ]
        for col in required_columns:
            assert col in dim_pharm.columns, f"Missing column: {col}"

        row = dim_pharm.iloc[0]
        assert row["pharmacy_npi"] == "1234567890"
        assert row["pharmacy_category"] == "Retail"

    def test_dim_prescriber_structure(self, sample_prescriber):
        """Test dim_prescriber has all required columns."""
        transformer = RxMemberSimDimensionalTransformer(prescribers=[sample_prescriber])
        dimensions, _ = transformer.transform()

        dim_pres = dimensions["dim_prescriber"]
        required_columns = [
            "prescriber_key", "prescriber_npi", "dea_number", "first_name",
            "last_name", "full_name", "credential", "specialty",
            "taxonomy_code", "is_active", "can_prescribe_controlled",
        ]
        for col in required_columns:
            assert col in dim_pres.columns, f"Missing column: {col}"

        row = dim_pres.iloc[0]
        assert row["prescriber_npi"] == "1987654321"
        assert row["credential"] == "MD"
        assert row["specialty"] == "Internal Medicine"

    def test_dim_formulary_structure(self, sample_formulary):
        """Test dim_formulary has all required columns."""
        transformer = RxMemberSimDimensionalTransformer(formularies=[sample_formulary])
        dimensions, _ = transformer.transform()

        dim_form = dimensions["dim_formulary"]
        required_columns = [
            "formulary_key", "formulary_id", "formulary_name",
            "effective_date", "tier_count", "drug_count",
        ]
        for col in required_columns:
            assert col in dim_form.columns, f"Missing column: {col}"

        row = dim_form.iloc[0]
        assert row["formulary_id"] == "FORM001"
        assert row["tier_count"] == 4
        assert row["drug_count"] == 1

    def test_fact_prescription_fills(
        self, sample_member, sample_drug, sample_pharmacy, sample_prescriber, sample_claim
    ):
        """Test fact_prescription_fills is created correctly."""
        transformer = RxMemberSimDimensionalTransformer(
            members=[sample_member],
            drugs=[sample_drug],
            pharmacies=[sample_pharmacy],
            prescribers=[sample_prescriber],
            claims=[sample_claim],
        )
        _, facts = transformer.transform()

        fact_fills = facts["fact_prescription_fills"]
        assert len(fact_fills) == 1

        row = fact_fills.iloc[0]
        assert row["claim_id"] == "CLM00000001"
        assert row["member_key"] == "RXM-00000001"
        assert row["quantity_dispensed"] == 30.0
        assert row["days_supply"] == 30
        assert row["is_new_fill"] == True  # noqa: E712
        assert row["is_refill"] == False  # noqa: E712
        assert row["ingredient_cost_submitted"] == 150.0

    def test_fact_prescription_fills_structure(self, sample_claim):
        """Test fact_prescription_fills has all required columns."""
        transformer = RxMemberSimDimensionalTransformer(claims=[sample_claim])
        _, facts = transformer.transform()

        fact_fills = facts["fact_prescription_fills"]
        required_columns = [
            "fill_fact_key", "claim_id", "member_key", "pharmacy_key",
            "prescriber_key", "medication_key", "service_date_key",
            "service_date", "transaction_code", "is_new_fill", "is_refill",
            "fill_number", "prescription_number", "ndc_11",
            "quantity_dispensed", "days_supply", "daw_code",
            "ingredient_cost_submitted", "dispensing_fee_submitted",
            "has_prior_auth", "has_dur_intervention",
        ]
        for col in required_columns:
            assert col in fact_fills.columns, f"Missing column: {col}"

    def test_fact_prior_auth(self, sample_member, sample_drug):
        """Test fact_prior_auth is created correctly."""
        pa_request = PriorAuthRequest(
            pa_request_id="PA-20240315-123456",
            request_type=PARequestType.NEW,
            request_date=datetime(2024, 3, 15, 10, 0),
            member_id=sample_member.member_id,
            cardholder_id=sample_member.cardholder_id,
            ndc=sample_drug.ndc,
            drug_name=sample_drug.drug_name,
            quantity_requested=Decimal("30"),
            days_supply_requested=30,
            prescriber_npi="1987654321",
            prescriber_name="Dr. Jane Doe",
            diagnosis_codes=["E11.9"],
        )

        pa_response = PriorAuthResponse(
            pa_request_id="PA-20240315-123456",
            pa_number="AUTH123456789",
            response_date=datetime(2024, 3, 15, 14, 0),
            status=PAStatus.APPROVED,
            effective_date=date(2024, 3, 15),
            expiration_date=date(2025, 3, 15),
            quantity_approved=Decimal("30"),
            days_supply_approved=30,
            auto_approved=False,
        )

        pa_record = PriorAuthRecord(request=pa_request, response=pa_response)

        transformer = RxMemberSimDimensionalTransformer(
            drugs=[sample_drug],
            prior_auths=[pa_record],
        )
        _, facts = transformer.transform()

        fact_pa = facts["fact_prior_auth"]
        assert len(fact_pa) == 1

        row = fact_pa.iloc[0]
        assert row["pa_request_id"] == "PA-20240315-123456"
        assert row["status"] == "approved"
        assert row["is_approved"] == True  # noqa: E712
        assert row["is_denied"] == False  # noqa: E712
        assert row["quantity_approved"] == 30.0
        assert row["turnaround_hours"] == 4.0  # 4 hours between request and response

    def test_ndc_normalization(self):
        """Test NDC normalization to 11-digit format."""
        transformer = RxMemberSimDimensionalTransformer()

        # 11-digit - no change
        assert transformer._normalize_ndc("00071015523") == "00071015523"

        # 10-digit - add leading zero to package segment
        assert transformer._normalize_ndc("0007101552") == "00071015502"

        # With dashes - remove and normalize
        assert transformer._normalize_ndc("00071-0155-23") == "00071015523"

    def test_ndc_11_to_10_conversion(self):
        """Test 11-digit to 10-digit NDC conversion."""
        transformer = RxMemberSimDimensionalTransformer()

        assert transformer._ndc_11_to_10("00071015523") == "0007101553"

    def test_age_calculation(self, sample_member):
        """Test age calculation in dim_rx_member."""
        transformer = RxMemberSimDimensionalTransformer(
            members=[sample_member],
            snapshot_date=date(2024, 5, 15),  # Exactly 44 years old
        )
        dimensions, _ = transformer.transform()

        dim_member = dimensions["dim_rx_member"]
        assert dim_member.iloc[0]["age_at_snapshot"] == 44
        assert dim_member.iloc[0]["age_band"] == "35-49"

    def test_therapeutic_category_lookup(self):
        """Test therapeutic category lookup from GPI."""
        transformer = RxMemberSimDimensionalTransformer()

        result = transformer._get_therapeutic_category("39400010000310")
        assert result == "Antihyperlipidemic Agents"
        assert transformer._get_therapeutic_category("27100030000310") == "Antidiabetic Agents"
        assert transformer._get_therapeutic_category("56320020100340") == "Psychotherapeutic Agents"
        assert transformer._get_therapeutic_category("99999999999999") == "Miscellaneous"
        assert transformer._get_therapeutic_category("") == "Unknown"

    def test_pharmacy_category_lookup(self):
        """Test pharmacy type to category mapping."""
        transformer = RxMemberSimDimensionalTransformer()

        assert transformer._get_pharmacy_category("retail") == "Retail"
        assert transformer._get_pharmacy_category("RETAIL") == "Retail"
        assert transformer._get_pharmacy_category("mail") == "Mail Order"
        assert transformer._get_pharmacy_category("specialty") == "Specialty"
        assert transformer._get_pharmacy_category("ltc") == "Long Term Care"
        assert transformer._get_pharmacy_category("hospital") == "Hospital"
        assert transformer._get_pharmacy_category("unknown_type") == "Other"

    def test_controlled_substance_flag(self):
        """Test controlled substance detection."""
        controlled_drug = DrugReference(
            ndc="00591024601",
            drug_name="Adderall 20mg",
            generic_name="Amphetamine/Dextroamphetamine",
            gpi="65100020201020",
            therapeutic_class="ADHD Agents",
            strength="20mg",
            dosage_form="Tablet",
            route_of_admin="Oral",
            dea_schedule=DEASchedule.SCHEDULE_II,
            is_brand=True,
        )

        transformer = RxMemberSimDimensionalTransformer(drugs=[controlled_drug])
        dimensions, _ = transformer.transform()

        dim_med = dimensions["dim_medication"]
        row = dim_med.iloc[0]

        assert row["dea_schedule"] == "2"
        assert row["is_controlled"] == True  # noqa: E712

    def test_refill_vs_new_fill(self, sample_member, sample_pharmacy, sample_prescriber):
        """Test new fill vs refill detection."""
        new_fill = PharmacyClaim(
            claim_id="CLM001",
            transaction_code=TransactionCode.BILLING,
            service_date=date(2024, 3, 15),
            pharmacy_npi=sample_pharmacy.npi,
            member_id=sample_member.member_id,
            cardholder_id=sample_member.cardholder_id,
            person_code="01",
            bin="610014",
            pcn="RXTEST",
            group_number="GRP001",
            prescription_number="RX123",
            fill_number=0,  # New fill
            ndc="00071015523",
            quantity_dispensed=Decimal("30"),
            days_supply=30,
            daw_code="0",
            prescriber_npi=sample_prescriber.npi,
            ingredient_cost_submitted=Decimal("100"),
            dispensing_fee_submitted=Decimal("2"),
            usual_customary_charge=Decimal("110"),
            gross_amount_due=Decimal("102"),
        )

        refill = PharmacyClaim(
            claim_id="CLM002",
            transaction_code=TransactionCode.BILLING,
            service_date=date(2024, 4, 15),
            pharmacy_npi=sample_pharmacy.npi,
            member_id=sample_member.member_id,
            cardholder_id=sample_member.cardholder_id,
            person_code="01",
            bin="610014",
            pcn="RXTEST",
            group_number="GRP001",
            prescription_number="RX123",
            fill_number=1,  # First refill
            ndc="00071015523",
            quantity_dispensed=Decimal("30"),
            days_supply=30,
            daw_code="0",
            prescriber_npi=sample_prescriber.npi,
            ingredient_cost_submitted=Decimal("100"),
            dispensing_fee_submitted=Decimal("2"),
            usual_customary_charge=Decimal("110"),
            gross_amount_due=Decimal("102"),
        )

        transformer = RxMemberSimDimensionalTransformer(claims=[new_fill, refill])
        _, facts = transformer.transform()

        fact_fills = facts["fact_prescription_fills"]
        assert len(fact_fills) == 2

        new_row = fact_fills[fact_fills["claim_id"] == "CLM001"].iloc[0]
        refill_row = fact_fills[fact_fills["claim_id"] == "CLM002"].iloc[0]

        assert new_row["is_new_fill"] == True  # noqa: E712
        assert new_row["is_refill"] == False  # noqa: E712
        assert refill_row["is_new_fill"] == False  # noqa: E712
        assert refill_row["is_refill"] == True  # noqa: E712

    def test_eligibility_spans(self, sample_member):
        """Test fact_rx_eligibility_spans is created correctly."""
        transformer = RxMemberSimDimensionalTransformer(
            members=[sample_member],
            snapshot_date=date(2024, 6, 1),
        )
        _, facts = transformer.transform()

        fact_elig = facts["fact_rx_eligibility_spans"]
        assert len(fact_elig) == 1

        row = fact_elig.iloc[0]
        assert row["member_key"] == "RXM-00000001"
        assert row["effective_date"] == date(2024, 1, 1)
        assert row["is_active"] == True  # noqa: E712
        assert row["coverage_days"] > 0
        assert row["bin"] == "610014"
        assert row["formulary_id"] == "FORM001"


class TestDuckDBIntegration:
    """Test DuckDB integration with RxMemberSim dimensional data."""

    @pytest.fixture
    def check_duckdb(self):
        """Check if DuckDB is available."""
        try:
            import duckdb  # noqa: F401
            return True
        except ImportError:
            pytest.skip("DuckDB not installed")

    def test_write_to_duckdb(
        self, check_duckdb, sample_member, sample_drug, sample_pharmacy,
        sample_prescriber, sample_claim, sample_formulary
    ):
        """Test writing dimensional data to DuckDB."""
        from healthsim.dimensional import DuckDBDimensionalWriter

        transformer = RxMemberSimDimensionalTransformer(
            members=[sample_member],
            drugs=[sample_drug],
            pharmacies=[sample_pharmacy],
            prescribers=[sample_prescriber],
            formularies=[sample_formulary],
            claims=[sample_claim],
        )
        dimensions, facts = transformer.transform()

        with DuckDBDimensionalWriter(":memory:") as writer:
            result = writer.write_dimensional_model(dimensions, facts)

            # Check all tables written
            for table_name in dimensions:
                assert table_name in result
                assert result[table_name] >= 0

            for table_name in facts:
                assert table_name in result
                assert result[table_name] >= 0

            # Verify can query
            tables = writer.get_table_list()
            assert "dim_rx_member" in tables
            assert "dim_medication" in tables
            assert "fact_prescription_fills" in tables

    def test_analytics_queries(
        self, check_duckdb, sample_member, sample_drug, sample_pharmacy,
        sample_prescriber, sample_claim
    ):
        """Test running analytics queries on dimensional data."""
        from healthsim.dimensional import DuckDBDimensionalWriter

        transformer = RxMemberSimDimensionalTransformer(
            members=[sample_member],
            drugs=[sample_drug],
            pharmacies=[sample_pharmacy],
            prescribers=[sample_prescriber],
            claims=[sample_claim],
        )
        dimensions, facts = transformer.transform()

        with DuckDBDimensionalWriter(":memory:") as writer:
            writer.write_dimensional_model(dimensions, facts)

            # Test aggregation query
            result = writer.query("""
                SELECT
                    age_band,
                    COUNT(*) as member_count
                FROM analytics.dim_rx_member
                GROUP BY age_band
            """)
            assert len(result) > 0
            assert "age_band" in result.columns

            # Test join query
            result = writer.query("""
                SELECT
                    m.drug_name,
                    SUM(f.quantity_dispensed) as total_quantity
                FROM analytics.fact_prescription_fills f
                JOIN analytics.dim_medication m ON f.medication_key = m.medication_key
                GROUP BY m.drug_name
            """)
            assert len(result) == 1
            assert result.iloc[0]["total_quantity"] == 30.0
