"""Tests for MemberSim Dimensional Transformer."""

from datetime import date
from decimal import Decimal

import pytest

from membersim import (
    SAMPLE_PLANS,
    Claim,
    ClaimLine,
    LinePayment,
    Member,
    MemberGenerator,
    Payment,
    Plan,
)
from membersim.dimensional import MemberSimDimensionalTransformer


class TestMemberSimDimensionalTransformer:
    """Test suite for MemberSimDimensionalTransformer."""

    def test_empty_transformer(self):
        """Test transformer with no data."""
        transformer = MemberSimDimensionalTransformer()
        dimensions, facts = transformer.transform()

        assert dimensions == {}
        assert facts == {}

    def test_transform_members_only(self, sample_member, sample_plan):
        """Test transformation with only members."""
        transformer = MemberSimDimensionalTransformer(
            members=[sample_member],
            plans=[sample_plan],
        )
        dimensions, facts = transformer.transform()

        # Check dimensions created
        assert "dim_member" in dimensions
        assert "dim_plan" in dimensions

        # Check facts created
        assert "fact_eligibility_spans" in facts

        # Verify dim_member
        dim_member = dimensions["dim_member"]
        assert len(dim_member) == 1
        assert dim_member.iloc[0]["member_id"] == "MEM001"
        assert dim_member.iloc[0]["given_name"] == "John"
        assert dim_member.iloc[0]["relationship_code"] == "18"
        assert dim_member.iloc[0]["is_subscriber"] == True  # noqa: E712

    def test_dim_member_structure(self, sample_member):
        """Test dim_member has all required columns."""
        transformer = MemberSimDimensionalTransformer(members=[sample_member])
        dimensions, _ = transformer.transform()

        dim_member = dimensions["dim_member"]
        required_columns = [
            "member_key",
            "member_id",
            "subscriber_id",
            "person_id",
            "given_name",
            "family_name",
            "full_name",
            "birth_date_key",
            "birth_date",
            "gender_code",
            "gender_description",
            "relationship_code",
            "relationship_description",
            "group_id",
            "plan_code",
            "age_at_snapshot",
            "age_band",
            "is_subscriber",
            "is_active",
        ]
        for col in required_columns:
            assert col in dim_member.columns, f"Missing column: {col}"

    def test_dim_plan_structure(self, sample_plan):
        """Test dim_plan has all required columns."""
        transformer = MemberSimDimensionalTransformer(plans=[sample_plan])
        dimensions, _ = transformer.transform()

        dim_plan = dimensions["dim_plan"]
        required_columns = [
            "plan_key",
            "plan_code",
            "plan_name",
            "plan_type",
            "coverage_type",
            "deductible_individual",
            "deductible_family",
            "oop_max_individual",
            "oop_max_family",
            "copay_pcp",
            "copay_specialist",
            "copay_er",
            "coinsurance_pct",
            "requires_pcp",
            "requires_referral",
        ]
        for col in required_columns:
            assert col in dim_plan.columns, f"Missing column: {col}"

        # Check coinsurance conversion (0.20 -> 20%)
        assert dim_plan.iloc[0]["coinsurance_pct"] == 20.0

    def test_dim_provider_from_providers(self, sample_provider):
        """Test dim_provider is built from Provider objects."""
        transformer = MemberSimDimensionalTransformer(providers=[sample_provider])
        dimensions, _ = transformer.transform()

        dim_provider = dimensions["dim_provider"]
        assert len(dim_provider) == 1
        assert dim_provider.iloc[0]["provider_npi"] == "1234567890"
        assert dim_provider.iloc[0]["provider_name"] == "Dr. Jane Doe"

    def test_dim_provider_from_claims(self, sample_claim):
        """Test dim_provider is built from claim NPIs."""
        transformer = MemberSimDimensionalTransformer(claims=[sample_claim])
        dimensions, _ = transformer.transform()

        dim_provider = dimensions["dim_provider"]
        assert len(dim_provider) == 1
        assert dim_provider.iloc[0]["provider_npi"] == "1234567890"

    def test_dim_diagnosis_from_claims(self, sample_claim):
        """Test dim_diagnosis is built from claim diagnoses."""
        # Create claim with multiple diagnoses
        claim = Claim(
            claim_id="CLM001",
            claim_type="PROFESSIONAL",
            member_id="MEM001",
            subscriber_id="MEM001",
            provider_npi="1234567890",
            service_date=date(2024, 3, 15),
            principal_diagnosis="E11.9",  # Type 2 diabetes
            other_diagnoses=["I10", "K21.0"],  # Hypertension, GERD
            claim_lines=[
                ClaimLine(
                    line_number=1,
                    procedure_code="99213",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("150.00"),
                ),
            ],
        )

        transformer = MemberSimDimensionalTransformer(claims=[claim])
        dimensions, _ = transformer.transform()

        dim_diagnosis = dimensions["dim_diagnosis"]
        assert len(dim_diagnosis) == 3

        # Check ICD-10 categories
        dx_codes = set(dim_diagnosis["diagnosis_code"].tolist())
        assert "E11.9" in dx_codes
        assert "I10" in dx_codes
        assert "K21.0" in dx_codes

    def test_dim_procedure_from_claims(self):
        """Test dim_procedure is built from claim lines."""
        claim = Claim(
            claim_id="CLM001",
            claim_type="PROFESSIONAL",
            member_id="MEM001",
            subscriber_id="MEM001",
            provider_npi="1234567890",
            service_date=date(2024, 3, 15),
            principal_diagnosis="E11.9",
            claim_lines=[
                ClaimLine(
                    line_number=1,
                    procedure_code="99213",  # CPT
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("150.00"),
                ),
                ClaimLine(
                    line_number=2,
                    procedure_code="G0103",  # HCPCS
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("50.00"),
                ),
            ],
        )

        transformer = MemberSimDimensionalTransformer(claims=[claim])
        dimensions, _ = transformer.transform()

        dim_procedure = dimensions["dim_procedure"]
        assert len(dim_procedure) == 2

        # Check code systems inferred correctly
        cpt_row = dim_procedure[dim_procedure["procedure_code"] == "99213"].iloc[0]
        assert cpt_row["code_system"] == "CPT"

        hcpcs_row = dim_procedure[dim_procedure["procedure_code"] == "G0103"].iloc[0]
        assert hcpcs_row["code_system"] == "HCPCS"

    def test_dim_service_category(self):
        """Test dim_service_category is built from place of service codes."""
        claim = Claim(
            claim_id="CLM001",
            claim_type="PROFESSIONAL",
            member_id="MEM001",
            subscriber_id="MEM001",
            provider_npi="1234567890",
            service_date=date(2024, 3, 15),
            place_of_service="11",  # Office
            principal_diagnosis="E11.9",
            claim_lines=[
                ClaimLine(
                    line_number=1,
                    procedure_code="99213",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("150.00"),
                    place_of_service="11",
                ),
                ClaimLine(
                    line_number=2,
                    procedure_code="99283",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("250.00"),
                    place_of_service="23",  # ER
                ),
            ],
        )

        transformer = MemberSimDimensionalTransformer(claims=[claim])
        dimensions, _ = transformer.transform()

        dim_service = dimensions["dim_service_category"]
        assert len(dim_service) == 2

        # Check categories
        office_row = dim_service[dim_service["place_of_service_code"] == "11"].iloc[0]
        assert office_row["service_category"] == "Office"
        assert office_row["place_of_service_description"] == "Office"

        er_row = dim_service[dim_service["place_of_service_code"] == "23"].iloc[0]
        assert er_row["service_category"] == "Emergency"

    def test_fact_claims_line_explosion(self):
        """Test fact_claims creates one row per claim line."""
        claim = Claim(
            claim_id="CLM001",
            claim_type="PROFESSIONAL",
            member_id="MEM001",
            subscriber_id="MEM001",
            provider_npi="1234567890",
            service_date=date(2024, 3, 15),
            principal_diagnosis="E11.9",
            claim_lines=[
                ClaimLine(
                    line_number=1,
                    procedure_code="99213",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("150.00"),
                    units=Decimal("1"),
                ),
                ClaimLine(
                    line_number=2,
                    procedure_code="85025",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("25.00"),
                    units=Decimal("1"),
                ),
                ClaimLine(
                    line_number=3,
                    procedure_code="80053",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("30.00"),
                    units=Decimal("1"),
                ),
            ],
        )

        transformer = MemberSimDimensionalTransformer(claims=[claim])
        _, facts = transformer.transform()

        fact_claims = facts["fact_claims"]

        # Should have 3 rows (one per claim line)
        assert len(fact_claims) == 3

        # All rows should have same claim_id
        assert all(fact_claims["claim_id"] == "CLM001")

        # Line numbers should be 1, 2, 3
        assert set(fact_claims["claim_line_number"].tolist()) == {1, 2, 3}

    def test_fact_claims_with_payment(self):
        """Test fact_claims includes payment details when available."""
        claim = Claim(
            claim_id="CLM001",
            claim_type="PROFESSIONAL",
            member_id="MEM001",
            subscriber_id="MEM001",
            provider_npi="1234567890",
            service_date=date(2024, 3, 15),
            principal_diagnosis="E11.9",
            claim_lines=[
                ClaimLine(
                    line_number=1,
                    procedure_code="99213",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("150.00"),
                ),
            ],
        )

        payment = Payment(
            payment_id="PAY001",
            claim_id="CLM001",
            payment_date=date(2024, 4, 1),
            check_number="CHK123",
            line_payments=[
                LinePayment(
                    line_number=1,
                    charged_amount=Decimal("150.00"),
                    allowed_amount=Decimal("120.00"),
                    paid_amount=Decimal("96.00"),
                    deductible_amount=Decimal("0.00"),
                    copay_amount=Decimal("25.00"),
                    coinsurance_amount=Decimal("0.00"),
                ),
            ],
        )

        transformer = MemberSimDimensionalTransformer(
            claims=[claim],
            payments=[payment],
        )
        _, facts = transformer.transform()

        fact_claims = facts["fact_claims"]
        row = fact_claims.iloc[0]

        assert row["charged_amount"] == 150.00
        assert row["allowed_amount"] == 120.00
        assert row["paid_amount"] == 96.00
        assert row["copay_amount"] == 25.00
        assert row["member_responsibility"] == 25.00  # copay only in this case
        assert row["paid_date"] == date(2024, 4, 1)

    def test_fact_claims_structure(self, sample_claim):
        """Test fact_claims has all required columns."""
        transformer = MemberSimDimensionalTransformer(claims=[sample_claim])
        _, facts = transformer.transform()

        fact_claims = facts["fact_claims"]
        required_columns = [
            "claim_fact_key",
            "claim_id",
            "claim_line_number",
            "member_key",
            "subscriber_key",
            "provider_key",
            "diagnosis_key",
            "procedure_key",
            "service_category_key",
            "service_date_key",
            "service_date",
            "claim_type",
            "place_of_service_code",
            "procedure_code",
            "units",
            "line_charge_amount",
        ]
        for col in required_columns:
            assert col in fact_claims.columns, f"Missing column: {col}"

    def test_fact_eligibility_spans(self, sample_member, sample_plan):
        """Test fact_eligibility_spans records member coverage periods."""
        transformer = MemberSimDimensionalTransformer(
            members=[sample_member],
            plans=[sample_plan],
        )
        _, facts = transformer.transform()

        fact_elig = facts["fact_eligibility_spans"]
        assert len(fact_elig) == 1

        row = fact_elig.iloc[0]
        assert row["member_key"] == "MEM001"
        assert row["effective_date"] == date(2024, 1, 1)
        assert row["is_active"] == True  # noqa: E712
        assert row["group_id"] == "GRP001"
        assert row["coverage_days"] > 0

    def test_age_calculation(self):
        """Test age calculation in dim_member."""
        from healthsim.person import Address, Gender, PersonName

        member = Member(
            id="person-001",
            name=PersonName(given_name="Test", family_name="User"),
            birth_date=date(1990, 6, 15),
            gender=Gender.MALE,
            address=Address(street="123 Main", city="Test", state="TX", zip_code="75001"),
            member_id="MEM001",
            relationship_code="18",
            group_id="GRP001",
            coverage_start=date(2024, 1, 1),
            plan_code="PPO",
        )

        # Use a specific snapshot date
        transformer = MemberSimDimensionalTransformer(
            members=[member],
            snapshot_date=date(2024, 6, 15),  # Exactly 34 years old
        )
        dimensions, _ = transformer.transform()

        dim_member = dimensions["dim_member"]
        assert dim_member.iloc[0]["age_at_snapshot"] == 34
        assert dim_member.iloc[0]["age_band"] == "18-34"

    def test_age_bands(self):
        """Test age band categorization."""
        transformer = MemberSimDimensionalTransformer()

        assert transformer.age_band(5) == "0-17"
        assert transformer.age_band(17) == "0-17"
        assert transformer.age_band(18) == "18-34"
        assert transformer.age_band(34) == "18-34"
        assert transformer.age_band(35) == "35-49"
        assert transformer.age_band(49) == "35-49"
        assert transformer.age_band(50) == "50-64"
        assert transformer.age_band(64) == "50-64"
        assert transformer.age_band(65) == "65+"
        assert transformer.age_band(100) == "65+"

    def test_icd10_categories(self):
        """Test ICD-10 category classification."""
        transformer = MemberSimDimensionalTransformer()

        assert transformer._get_icd10_category("E11.9") == "Endocrine/Metabolic"
        assert transformer._get_icd10_category("I10") == "Circulatory"
        assert transformer._get_icd10_category("J44.1") == "Respiratory"
        assert transformer._get_icd10_category("K21.0") == "Digestive"
        assert transformer._get_icd10_category("M54.5") == "Musculoskeletal"
        assert transformer._get_icd10_category("Z00.00") == "Health Status"

    def test_procedure_code_system_inference(self):
        """Test procedure code system inference."""
        transformer = MemberSimDimensionalTransformer()

        # CPT (5 digits)
        assert transformer._infer_procedure_code_system("99213") == "CPT"
        assert transformer._infer_procedure_code_system("85025") == "CPT"

        # HCPCS (letter + 4 digits)
        assert transformer._infer_procedure_code_system("G0103") == "HCPCS"
        assert transformer._infer_procedure_code_system("J1234") == "HCPCS"

        # ICD-10-PCS (7 alphanumeric)
        assert transformer._infer_procedure_code_system("0BJ08ZZ") == "ICD-10-PCS"

    def test_service_category_classification(self):
        """Test place of service to service category mapping."""
        transformer = MemberSimDimensionalTransformer()

        assert transformer._get_service_category("11") == "Office"
        assert transformer._get_service_category("21") == "Inpatient"
        assert transformer._get_service_category("22") == "Outpatient"
        assert transformer._get_service_category("23") == "Emergency"
        assert transformer._get_service_category("31") == "Skilled Nursing"
        assert transformer._get_service_category("12") == "Home Health"
        assert transformer._get_service_category("02") == "Office"  # Telehealth

    def test_multiple_members_and_claims(self):
        """Test transformer with multiple members and claims."""
        from healthsim.person import Address, Gender, PersonName

        members = []
        claims = []

        for i in range(5):
            member = Member(
                id=f"person-{i:03d}",
                name=PersonName(given_name=f"Test{i}", family_name="User"),
                birth_date=date(1980 + i, 1, 1),
                gender=Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                address=Address(street="123 Main", city="Test", state="TX", zip_code="75001"),
                member_id=f"MEM{i:03d}",
                relationship_code="18",
                group_id="GRP001",
                coverage_start=date(2024, 1, 1),
                plan_code="PPO",
            )
            members.append(member)

            claim = Claim(
                claim_id=f"CLM{i:03d}",
                claim_type="PROFESSIONAL",
                member_id=member.member_id,
                subscriber_id=member.member_id,
                provider_npi=f"123456789{i}",
                service_date=date(2024, 3, 15),
                principal_diagnosis=f"E11.{i}",
                claim_lines=[
                    ClaimLine(
                        line_number=1,
                        procedure_code="99213",
                        service_date=date(2024, 3, 15),
                        charge_amount=Decimal("150.00"),
                    ),
                ],
            )
            claims.append(claim)

        plan = Plan(
            plan_code="PPO",
            plan_name="Test PPO",
            plan_type="PPO",
        )

        transformer = MemberSimDimensionalTransformer(
            members=members,
            plans=[plan],
            claims=claims,
        )
        dimensions, facts = transformer.transform()

        assert len(dimensions["dim_member"]) == 5
        assert len(dimensions["dim_provider"]) == 5
        assert len(facts["fact_claims"]) == 5
        assert len(facts["fact_eligibility_spans"]) == 5

    def test_date_to_key_conversion(self):
        """Test date to key conversion."""
        transformer = MemberSimDimensionalTransformer()

        assert transformer.date_to_key(date(2024, 12, 15)) == 20241215
        assert transformer.date_to_key(date(2024, 1, 1)) == 20240101
        assert transformer.date_to_key(None) is None
        assert transformer.date_to_key("2024-06-15") == 20240615

    def test_generated_members(self):
        """Test transformer with MemberGenerator output."""
        gen = MemberGenerator(seed=42)
        members = gen.generate_many(10)
        plans = list(SAMPLE_PLANS.values())

        transformer = MemberSimDimensionalTransformer(
            members=members,
            plans=plans,
        )
        dimensions, facts = transformer.transform()

        assert len(dimensions["dim_member"]) == 10
        assert len(dimensions["dim_plan"]) == 3
        assert len(facts["fact_eligibility_spans"]) == 10


class TestDuckDBIntegration:
    """Test DuckDB integration with MemberSim dimensional data."""

    @pytest.fixture
    def check_duckdb(self):
        """Check if DuckDB is available."""
        import importlib.util

        if importlib.util.find_spec("duckdb") is None:
            pytest.skip("DuckDB not installed")
        return True

    def test_write_to_duckdb(self, check_duckdb, sample_member, sample_plan, sample_claim):
        """Test writing dimensional data to DuckDB."""
        from healthsim.dimensional import DuckDBDimensionalWriter

        transformer = MemberSimDimensionalTransformer(
            members=[sample_member],
            plans=[sample_plan],
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
            assert "dim_member" in tables
            assert "fact_claims" in tables

    def test_analytics_queries(self, check_duckdb, sample_member, sample_plan, sample_claim):
        """Test running analytics queries on dimensional data."""
        from healthsim.dimensional import DuckDBDimensionalWriter

        transformer = MemberSimDimensionalTransformer(
            members=[sample_member],
            plans=[sample_plan],
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
                FROM analytics.dim_member
                GROUP BY age_band
            """)
            assert len(result) > 0
            assert "age_band" in result.columns
            assert "member_count" in result.columns

            # Test join query
            result = writer.query("""
                SELECT
                    m.member_id,
                    COUNT(*) as claim_count
                FROM analytics.fact_claims f
                JOIN analytics.dim_member m ON f.member_key = m.member_key
                GROUP BY m.member_id
            """)
            assert len(result) == 1
            assert result.iloc[0]["claim_count"] == 1
