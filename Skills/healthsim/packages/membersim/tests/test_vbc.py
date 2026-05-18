"""Tests for value-based care models."""

from datetime import date
from decimal import Decimal

from membersim.vbc import (
    HCC_CATEGORIES,
    Attribution,
    AttributionMethod,
    AttributionPanel,
    CapitationPayment,
    CapitationRate,
    calculate_capitation_payment,
)

# ============================================================================
# Attribution Tests
# ============================================================================


class TestAttribution:
    """Tests for Attribution model."""

    def test_attribution_creation(self) -> None:
        """Test creating an attribution."""
        attr = Attribution(
            attribution_id="ATT001",
            member_id="MEM001",
            provider_npi="1234567890",
            attribution_method=AttributionMethod.PROSPECTIVE,
            effective_date=date(2024, 1, 1),
            performance_year=2024,
            risk_score=Decimal("1.25"),
        )

        assert attr.attribution_id == "ATT001"
        assert attr.member_id == "MEM001"
        assert attr.risk_score == Decimal("1.25")
        assert attr.is_active

    def test_attribution_with_hcc_codes(self) -> None:
        """Test attribution with HCC codes."""
        attr = Attribution(
            attribution_id="ATT002",
            member_id="MEM002",
            provider_npi="1234567890",
            effective_date=date(2024, 1, 1),
            performance_year=2024,
            hcc_codes=["HCC18", "HCC85"],
        )

        assert len(attr.hcc_codes) == 2
        assert "HCC18" in attr.hcc_codes

    def test_attribution_inactive_terminated(self) -> None:
        """Test inactive attribution (terminated)."""
        attr = Attribution(
            attribution_id="ATT003",
            member_id="MEM003",
            provider_npi="1234567890",
            effective_date=date(2023, 1, 1),
            termination_date=date(2023, 12, 31),
            performance_year=2023,
        )

        assert not attr.is_active

    def test_attribution_methods(self) -> None:
        """Test attribution method constants."""
        assert AttributionMethod.PROSPECTIVE == "PROSPECTIVE"
        assert AttributionMethod.RETROSPECTIVE == "RETROSPECTIVE"
        assert AttributionMethod.HYBRID == "HYBRID"


class TestAttributionPanel:
    """Tests for AttributionPanel model."""

    def test_panel_creation(self) -> None:
        """Test creating an attribution panel."""
        panel = AttributionPanel(
            provider_npi="1234567890",
            provider_name="Dr. Smith Primary Care",
            performance_year=2024,
            attributed_members=["MEM001", "MEM002", "MEM003"],
            avg_risk_score=Decimal("1.15"),
        )

        assert panel.panel_size == 3
        assert panel.avg_risk_score == Decimal("1.15")

    def test_panel_size_from_total(self) -> None:
        """Test panel size from total_members when list is empty."""
        panel = AttributionPanel(
            provider_npi="1234567890",
            provider_name="Dr. Jones",
            performance_year=2024,
            total_members=500,
        )

        assert panel.panel_size == 500


class TestHCCCategories:
    """Tests for HCC reference data."""

    def test_hcc_categories_exist(self) -> None:
        """Test HCC categories are defined."""
        assert "HCC18" in HCC_CATEGORIES
        assert "HCC85" in HCC_CATEGORIES
        assert "Diabetes" in HCC_CATEGORIES["HCC18"]


# ============================================================================
# Capitation Tests
# ============================================================================


class TestCapitationRate:
    """Tests for CapitationRate model."""

    def test_capitation_rate_creation(self) -> None:
        """Test creating a capitation rate."""
        rate = CapitationRate(
            rate_id="RATE001",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
            rate_category="ADULT",
            base_pmpm=Decimal("250.00"),
            risk_adjusted=True,
        )

        assert rate.base_pmpm == Decimal("250.00")
        assert rate.risk_adjusted

    def test_calculate_pmpm_base(self) -> None:
        """Test PMPM calculation with 1.0 risk score."""
        rate = CapitationRate(
            rate_id="RATE001",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
            rate_category="ADULT",
            base_pmpm=Decimal("250.00"),
            risk_adjusted=True,
        )

        assert rate.calculate_pmpm(Decimal("1.0")) == Decimal("250.00")

    def test_calculate_pmpm_high_risk(self) -> None:
        """Test PMPM calculation with high risk score."""
        rate = CapitationRate(
            rate_id="RATE001",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
            rate_category="ADULT",
            base_pmpm=Decimal("250.00"),
            risk_adjusted=True,
        )

        # 1.2 risk score = 20% more
        assert rate.calculate_pmpm(Decimal("1.2")) == Decimal("300.00")

    def test_calculate_pmpm_no_risk_adjustment(self) -> None:
        """Test PMPM calculation without risk adjustment."""
        rate = CapitationRate(
            rate_id="RATE001",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
            rate_category="ADULT",
            base_pmpm=Decimal("250.00"),
            risk_adjusted=False,
        )

        # Should return base rate regardless of risk score
        assert rate.calculate_pmpm(Decimal("1.5")) == Decimal("250.00")


class TestCapitationPayment:
    """Tests for CapitationPayment model."""

    def test_capitation_payment_creation(self) -> None:
        """Test creating a capitation payment."""
        payment = CapitationPayment(
            payment_id="CAP-001",
            provider_npi="1234567890",
            contract_id="CTR001",
            payment_period="2024-03",
            payment_date=date(2024, 3, 15),
            member_months=100,
            base_amount=Decimal("25000.00"),
            risk_adjustment=Decimal("2500.00"),
            total_amount=Decimal("27500.00"),
            adult_members=100,
        )

        assert payment.member_months == 100
        assert payment.total_amount == Decimal("27500.00")


class TestCalculateCapitationPayment:
    """Tests for calculate_capitation_payment function."""

    def test_calculate_payment_adults_only(self) -> None:
        """Test capitation payment calculation for adult members."""
        rates = {
            "ADULT": CapitationRate(
                rate_id="R1",
                contract_id="C1",
                effective_date=date(2024, 1, 1),
                rate_category="ADULT",
                base_pmpm=Decimal("250.00"),
            ),
        }

        members = [
            {"member_id": "M1", "age": 45, "risk_score": 1.0},
            {"member_id": "M2", "age": 50, "risk_score": 1.5},
        ]

        payment = calculate_capitation_payment(
            provider_npi="1234567890",
            contract_id="C1",
            payment_period="2024-03",
            members=members,
            rates=rates,
        )

        assert payment.member_months == 2
        assert payment.adult_members == 2
        assert payment.pediatric_members == 0
        assert payment.senior_members == 0
        # Base: 250 + 250 = 500
        # Risk adjustment: 250 * (1.0 - 1) + 250 * (1.5 - 1) = 0 + 125 = 125
        assert payment.base_amount == Decimal("500.00")
        assert payment.risk_adjustment == Decimal("125.00")
        assert payment.total_amount == Decimal("625.00")

    def test_calculate_payment_mixed_ages(self) -> None:
        """Test capitation with pediatric, adult, and senior members."""
        rates = {
            "PEDIATRIC": CapitationRate(
                rate_id="R1",
                contract_id="C1",
                effective_date=date(2024, 1, 1),
                rate_category="PEDIATRIC",
                base_pmpm=Decimal("150.00"),
            ),
            "ADULT": CapitationRate(
                rate_id="R2",
                contract_id="C1",
                effective_date=date(2024, 1, 1),
                rate_category="ADULT",
                base_pmpm=Decimal("250.00"),
            ),
            "SENIOR": CapitationRate(
                rate_id="R3",
                contract_id="C1",
                effective_date=date(2024, 1, 1),
                rate_category="SENIOR",
                base_pmpm=Decimal("500.00"),
            ),
        }

        members = [
            {"member_id": "M1", "age": 10, "risk_score": 1.0},  # Pediatric
            {"member_id": "M2", "age": 45, "risk_score": 1.0},  # Adult
            {"member_id": "M3", "age": 70, "risk_score": 1.2},  # Senior
        ]

        payment = calculate_capitation_payment(
            provider_npi="1234567890",
            contract_id="C1",
            payment_period="2024-03",
            members=members,
            rates=rates,
        )

        assert payment.pediatric_members == 1
        assert payment.adult_members == 1
        assert payment.senior_members == 1
        # Base: 150 + 250 + 500 = 900
        assert payment.base_amount == Decimal("900.00")


# ============================================================================
# Export Format Tests
# ============================================================================


class TestExportFormats:
    """Tests for export utilities."""

    def test_to_json_model(self) -> None:
        """Test JSON export of a model."""
        from membersim.formats import to_json

        rate = CapitationRate(
            rate_id="R1",
            contract_id="C1",
            effective_date=date(2024, 1, 1),
            rate_category="ADULT",
            base_pmpm=Decimal("250.00"),
        )

        json_str = to_json(rate)
        assert "rate_id" in json_str
        assert "250.0" in json_str  # Decimal converted to float

    def test_to_json_list(self) -> None:
        """Test JSON export of a list."""
        from membersim.formats import to_json

        data = [{"a": 1}, {"b": 2}]
        json_str = to_json(data)
        assert '"a": 1' in json_str


class TestFHIRFormats:
    """Tests for FHIR resource generation."""

    def test_member_to_fhir_coverage(self, sample_address) -> None:
        """Test FHIR Coverage resource generation."""
        from healthsim.person import Gender, PersonName

        from membersim import Member
        from membersim.formats import member_to_fhir_coverage

        member = Member(
            id="person-001",
            name=PersonName(given_name="John", family_name="Doe"),
            birth_date=date(1980, 5, 15),
            gender=Gender.MALE,
            address=sample_address,
            member_id="MEM001",
            relationship_code="18",
            group_id="GRP001",
            coverage_start=date(2024, 1, 1),
            plan_code="PPO",
        )

        coverage = member_to_fhir_coverage(member)

        assert coverage["resourceType"] == "Coverage"
        assert coverage["id"] == "MEM001"
        assert coverage["status"] == "active"

    def test_member_to_fhir_patient(self, sample_address) -> None:
        """Test FHIR Patient resource generation."""
        from healthsim.person import Gender, PersonName

        from membersim import Member
        from membersim.formats import member_to_fhir_patient

        member = Member(
            id="person-001",
            name=PersonName(given_name="Jane", family_name="Smith"),
            birth_date=date(1990, 3, 20),
            gender=Gender.FEMALE,
            address=sample_address,
            member_id="MEM002",
            relationship_code="18",
            group_id="GRP001",
            coverage_start=date(2024, 1, 1),
            plan_code="HMO",
        )

        patient = member_to_fhir_patient(member)

        assert patient["resourceType"] == "Patient"
        assert patient["id"] == "MEM002"
        assert patient["gender"] == "female"
        assert patient["name"][0]["family"] == "Smith"

    def test_create_fhir_bundle(self) -> None:
        """Test FHIR Bundle creation."""
        from membersim.formats import create_fhir_bundle

        resources = [
            {"resourceType": "Patient", "id": "P1"},
            {"resourceType": "Coverage", "id": "C1"},
        ]

        bundle = create_fhir_bundle(resources)

        assert bundle["resourceType"] == "Bundle"
        assert bundle["type"] == "collection"
        assert bundle["total"] == 2
        assert len(bundle["entry"]) == 2


# ============================================================================
# MCP Handler Tests
# ============================================================================


class TestMCPHandler:
    """Tests for MCP handler."""

    def test_handler_initialization(self) -> None:
        """Test MCP handler initialization."""
        from membersim.mcp.server import MemberSimMCPHandler

        handler = MemberSimMCPHandler()
        # Handler now uses session_manager for state, not internal attributes
        assert handler._counter == 0
        assert handler.get_tools() is not None

    def test_get_tools(self) -> None:
        """Test getting tool definitions."""
        from membersim.mcp.server import MemberSimMCPHandler

        handler = MemberSimMCPHandler()
        tools = handler.get_tools()

        assert len(tools) == 10
        tool_names = [t["name"] for t in tools]
        assert "create_member" in tool_names
        assert "create_claim" in tool_names

    def test_list_plans(self) -> None:
        """Test listing plans through MCP handler."""
        import json

        from membersim.mcp.server import MemberSimMCPHandler

        handler = MemberSimMCPHandler()
        result = handler.call_tool("list_plans", {})
        plans = json.loads(result)

        assert "HMO_STANDARD" in plans
        assert "PPO_GOLD" in plans

    def test_list_hedis_measures(self) -> None:
        """Test listing HEDIS measures through MCP handler."""
        import json

        from membersim.mcp.server import MemberSimMCPHandler

        handler = MemberSimMCPHandler()
        result = handler.call_tool("list_hedis_measures", {})
        measures = json.loads(result)

        assert "BCS" in measures
        assert "COL" in measures
