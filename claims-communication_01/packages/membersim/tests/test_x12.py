"""Tests for X12 EDI format module."""

from datetime import date
from decimal import Decimal

from healthsim.person import Address, Gender, PersonName

from membersim import Claim, ClaimLine, Member, Payment, Plan
from membersim.claims.payment import LinePayment
from membersim.formats.x12 import (
    X12Config,
    X12Generator,
    generate_270,
    generate_271,
    generate_834,
    generate_835,
    generate_837i,
    generate_837p,
)
from membersim.network import (
    MEDICARE_BASE_RATES,
    FeeSchedule,
    ProviderContract,
    create_default_fee_schedule,
)

# ============================================================================
# X12 Base Tests
# ============================================================================


class TestX12Config:
    """Tests for X12Config."""

    def test_default_config(self) -> None:
        """Test default X12 configuration."""
        config = X12Config()
        assert config.sender_id == "MEMBERSIM"
        assert config.receiver_id == "RECEIVER"
        assert config.isa_control_number == 1
        assert config.gs_control_number == 1
        assert config.st_control_number == 1

    def test_custom_config(self) -> None:
        """Test custom X12 configuration."""
        config = X12Config(
            sender_id="SENDER123",
            receiver_id="RECV456",
            isa_control_number=100,
        )
        assert config.sender_id == "SENDER123"
        assert config.receiver_id == "RECV456"
        assert config.isa_control_number == 100


class TestX12Generator:
    """Tests for X12Generator base class."""

    def test_segment_creation(self) -> None:
        """Test basic segment creation."""
        gen = X12Generator()
        gen._add("TST", "A", "B", "C")
        output = gen.to_string()
        assert "TST*A*B*C~" in output

    def test_element_separator(self) -> None:
        """Test element separator is asterisk."""
        assert X12Generator.ELEMENT_SEPARATOR == "*"

    def test_segment_terminator(self) -> None:
        """Test segment terminator is tilde."""
        assert X12Generator.SEGMENT_TERMINATOR == "~"


# ============================================================================
# EDI 834 Enrollment Tests
# ============================================================================


class TestEDI834Generator:
    """Tests for 834 Enrollment generator."""

    def test_generate_834_single_member(self, sample_member: Member) -> None:
        """Test 834 generation for single member."""
        edi = generate_834([sample_member])

        # Check envelope segments
        assert "ISA*" in edi
        assert "GS*BE*" in edi  # BE = Benefit Enrollment
        assert "ST*834*" in edi

        # Check member data
        assert "INS*Y*18*" in edi  # Subscriber
        assert "NM1*IL*1*Smith*John" in edi  # Proper case preserved
        assert "DMG*D8*19800515*M~" in edi  # Birth date and gender

        # Check trailer segments
        assert "SE*" in edi
        assert "GE*" in edi
        assert "IEA*" in edi

    def test_generate_834_multiple_members(
        self, sample_name: PersonName, sample_address: Address
    ) -> None:
        """Test 834 generation for multiple members."""
        members = [
            Member(
                id=f"person-{i}",
                name=PersonName(given_name=f"Member{i}", family_name="Test"),
                birth_date=date(1980 + i, 1, 1),
                gender=Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                address=sample_address,
                member_id=f"MEM{i:03d}",
                relationship_code="18",
                group_id="GRP001",
                coverage_start=date(2024, 1, 1),
                plan_code="PPO",
            )
            for i in range(3)
        ]

        edi = generate_834(members)

        # Each member should have an INS segment
        assert edi.count("INS*") == 3
        assert edi.count("NM1*IL*") == 3

    def test_generate_834_dependent(self, sample_name: PersonName, sample_address: Address) -> None:
        """Test 834 generation for dependent."""
        dependent = Member(
            id="person-dep",
            name=PersonName(given_name="Child", family_name="Smith"),
            birth_date=date(2015, 6, 15),
            gender=Gender.FEMALE,
            address=sample_address,
            member_id="MEM002",
            subscriber_id="MEM001",
            relationship_code="19",  # Child
            group_id="GRP001",
            coverage_start=date(2024, 1, 1),
            plan_code="PPO",
        )

        edi = generate_834([dependent])

        # Check dependent indicator
        assert "INS*N*19*" in edi  # Not subscriber, child


# ============================================================================
# EDI 837 Claims Tests
# ============================================================================


class TestEDI837PGenerator:
    """Tests for 837P Professional Claims generator."""

    def test_generate_837p_single_claim(self, sample_claim: Claim) -> None:
        """Test 837P generation for single claim."""
        edi = generate_837p([sample_claim])

        # Check envelope
        assert "ISA*" in edi
        assert "GS*HC*" in edi  # HC = Health Care Claim
        assert "ST*837*" in edi

        # Check claim header
        assert "CLM*CLM001*" in edi

        # Check diagnosis (includes period in ICD-10 code)
        assert "HI*ABK:E11.9~" in edi  # Principal diagnosis

        # Check service line (SV1 for professional)
        assert "SV1*HC:99213*" in edi

    def test_generate_837p_multiple_lines(self) -> None:
        """Test 837P with multiple service lines."""
        claim = Claim(
            claim_id="CLM002",
            claim_type="PROFESSIONAL",
            member_id="MEM001",
            subscriber_id="MEM001",
            provider_npi="1234567890",
            service_date=date(2024, 3, 15),
            place_of_service="11",
            principal_diagnosis="J06.9",
            claim_lines=[
                ClaimLine(
                    line_number=1,
                    procedure_code="99213",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("150.00"),
                ),
                ClaimLine(
                    line_number=2,
                    procedure_code="87880",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("45.00"),
                ),
            ],
        )

        edi = generate_837p([claim])

        # Should have 2 SV1 segments
        assert edi.count("SV1*") == 2
        assert "SV1*HC:99213*" in edi
        assert "SV1*HC:87880*" in edi


class TestEDI837IGenerator:
    """Tests for 837I Institutional Claims generator."""

    def test_generate_837i_single_claim(self) -> None:
        """Test 837I generation for institutional claim."""
        claim = Claim(
            claim_id="CLM003",
            claim_type="INSTITUTIONAL",
            member_id="MEM001",
            subscriber_id="MEM001",
            provider_npi="9876543210",
            service_date=date(2024, 3, 15),
            place_of_service="21",  # Inpatient hospital
            principal_diagnosis="K80.00",
            claim_lines=[
                ClaimLine(
                    line_number=1,
                    procedure_code="99223",
                    revenue_code="0120",
                    service_date=date(2024, 3, 15),
                    charge_amount=Decimal("500.00"),
                ),
            ],
        )

        edi = generate_837i([claim])

        # Check institutional-specific segments
        assert "ST*837*" in edi
        assert "CLM*CLM003*" in edi

        # Should use SV2 (institutional) not SV1 (professional)
        assert "SV2*0120*" in edi


# ============================================================================
# EDI 835 Remittance Tests
# ============================================================================


class TestEDI835Generator:
    """Tests for 835 Remittance Advice generator."""

    def test_generate_835_single_payment(self) -> None:
        """Test 835 generation for single payment."""
        payment = Payment(
            payment_id="PAY001",
            claim_id="CLM001",
            payment_date=date(2024, 4, 1),
            check_number="CHK12345",
            line_payments=[
                LinePayment(
                    line_number=1,
                    charged_amount=Decimal("150.00"),
                    allowed_amount=Decimal("100.00"),
                    paid_amount=Decimal("75.00"),
                    deductible_amount=Decimal("25.00"),
                ),
            ],
        )

        edi = generate_835([payment])

        # Check envelope
        assert "ISA*" in edi
        assert "GS*HP*" in edi  # HP = Health Care Claim Payment
        assert "ST*835*" in edi

        # Check financial info
        assert "BPR*" in edi
        assert "TRN*1*CHK12345*" in edi

        # Check claim payment
        assert "CLP*CLM001*" in edi

        # Check adjustment (deductible) - includes decimal places
        assert "CAS*PR*1*25.00~" in edi

    def test_generate_835_with_adjustments(self) -> None:
        """Test 835 with various adjustment types."""
        payment = Payment(
            payment_id="PAY002",
            claim_id="CLM002",
            payment_date=date(2024, 4, 1),
            check_number="CHK12346",
            line_payments=[
                LinePayment(
                    line_number=1,
                    charged_amount=Decimal("200.00"),
                    allowed_amount=Decimal("150.00"),
                    paid_amount=Decimal("95.00"),
                    deductible_amount=Decimal("25.00"),
                    copay_amount=Decimal("30.00"),
                    coinsurance_amount=Decimal("0.00"),
                ),
            ],
        )

        edi = generate_835([payment])

        # Check deductible and copay adjustments (includes decimal places)
        assert "CAS*PR*1*25.00~" in edi  # Deductible
        assert "CAS*PR*3*30.00~" in edi  # Copay


# ============================================================================
# EDI 270/271 Eligibility Tests
# ============================================================================


class TestEDI270Generator:
    """Tests for 270 Eligibility Inquiry generator."""

    def test_generate_270_inquiry(self, sample_member: Member) -> None:
        """Test 270 eligibility inquiry generation."""
        edi = generate_270(sample_member, service_date=date(2024, 3, 15))

        # Check envelope
        assert "ISA*" in edi
        assert "GS*HS*" in edi  # HS = Eligibility
        assert "ST*270*" in edi

        # Check member info (proper case preserved)
        assert "NM1*IL*1*Smith*John" in edi

        # Check service date
        assert "DTP*291*" in edi


class TestEDI271Generator:
    """Tests for 271 Eligibility Response generator."""

    def test_generate_271_response(self, sample_member: Member, sample_plan: Plan) -> None:
        """Test 271 eligibility response generation."""
        edi = generate_271(sample_member, sample_plan)

        # Check envelope
        assert "ISA*" in edi
        assert "GS*HB*" in edi  # HB = Eligibility Response
        assert "ST*271*" in edi

        # Check member info (proper case preserved)
        assert "NM1*IL*1*Smith*John" in edi

        # Check eligibility info (should have EB segments)
        assert "EB*" in edi

    def test_generate_271_with_benefits(self, sample_member: Member, sample_plan: Plan) -> None:
        """Test 271 response includes benefit details."""
        edi = generate_271(sample_member, sample_plan)

        # Should include deductible info
        assert "EB*C*IND*30*" in edi  # Deductible segment
        # Should include out-of-pocket max
        assert "EB*G*IND*30*" in edi  # OOP max segment


# ============================================================================
# Provider Contract Tests
# ============================================================================


class TestProviderContract:
    """Tests for ProviderContract model."""

    def test_create_contract(self) -> None:
        """Test creating a provider contract."""
        contract = ProviderContract(
            contract_id="CTR001",
            provider_npi="1234567890",
            network_id="NET001",
            effective_date=date(2024, 1, 1),
        )

        assert contract.contract_id == "CTR001"
        assert contract.contract_type == "FFS"
        assert contract.fee_schedule_type == "MEDICARE_PCT"
        assert contract.fee_schedule_pct == Decimal("1.20")

    def test_contract_is_active(self) -> None:
        """Test contract active status."""
        contract = ProviderContract(
            contract_id="CTR002",
            provider_npi="1234567890",
            network_id="NET001",
            effective_date=date(2020, 1, 1),
        )

        assert contract.is_active

    def test_contract_terminated(self) -> None:
        """Test terminated contract."""
        contract = ProviderContract(
            contract_id="CTR003",
            provider_npi="1234567890",
            network_id="NET001",
            effective_date=date(2020, 1, 1),
            termination_date=date(2023, 12, 31),
        )

        assert not contract.is_active

    def test_capitation_contract(self) -> None:
        """Test capitated contract."""
        contract = ProviderContract(
            contract_id="CTR004",
            provider_npi="1234567890",
            network_id="NET001",
            effective_date=date(2024, 1, 1),
            contract_type="CAPITATION",
            capitation_rate=Decimal("45.00"),
        )

        assert contract.contract_type == "CAPITATION"
        assert contract.capitation_rate == Decimal("45.00")


# ============================================================================
# Fee Schedule Tests
# ============================================================================


class TestFeeSchedule:
    """Tests for FeeSchedule model."""

    def test_medicare_base_rates_exist(self) -> None:
        """Test that Medicare base rates are defined."""
        assert "99213" in MEDICARE_BASE_RATES
        assert "99214" in MEDICARE_BASE_RATES
        assert MEDICARE_BASE_RATES["99213"] == Decimal("92.00")

    def test_create_fee_schedule(self) -> None:
        """Test creating a fee schedule."""
        schedule = FeeSchedule(
            schedule_id="FS001",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
        )

        assert schedule.base_rate_type == "MEDICARE_PCT"
        assert schedule.medicare_percentage == Decimal("1.20")

    def test_get_allowed_amount_medicare(self) -> None:
        """Test allowed amount calculation at Medicare percentage."""
        schedule = FeeSchedule(
            schedule_id="FS002",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
            medicare_percentage=Decimal("1.20"),
        )

        # 99213 base is $92, at 120% = $110.40
        allowed = schedule.get_allowed_amount("99213")
        assert allowed == Decimal("110.40")

    def test_get_allowed_amount_custom_rate(self) -> None:
        """Test allowed amount with custom rate override."""
        schedule = FeeSchedule(
            schedule_id="FS003",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
            custom_rates={"99213": Decimal("125.00")},
        )

        # Custom rate should override Medicare calculation
        allowed = schedule.get_allowed_amount("99213")
        assert allowed == Decimal("125.00")

    def test_get_allowed_amount_with_units(self) -> None:
        """Test allowed amount with multiple units."""
        schedule = FeeSchedule(
            schedule_id="FS004",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
            medicare_percentage=Decimal("1.00"),
        )

        # 99213 base is $92, 2 units = $184
        allowed = schedule.get_allowed_amount("99213", units=Decimal("2"))
        assert allowed == Decimal("184.00")

    def test_create_default_fee_schedule(self) -> None:
        """Test convenience function for creating fee schedule."""
        schedule = create_default_fee_schedule("CTR001")

        assert schedule.schedule_id == "FS-CTR001"
        assert schedule.contract_id == "CTR001"
        assert schedule.medicare_percentage == Decimal("1.20")

    def test_create_default_fee_schedule_custom_pct(self) -> None:
        """Test default fee schedule with custom Medicare percentage."""
        schedule = create_default_fee_schedule("CTR002", medicare_pct=Decimal("1.50"))

        assert schedule.medicare_percentage == Decimal("1.50")

    def test_unknown_procedure_fallback(self) -> None:
        """Test fallback for unknown procedure codes."""
        schedule = FeeSchedule(
            schedule_id="FS005",
            contract_id="CTR001",
            effective_date=date(2024, 1, 1),
            medicare_percentage=Decimal("1.20"),
        )

        # Unknown code should use $50 default * 120%
        allowed = schedule.get_allowed_amount("UNKNOWN")
        assert allowed == Decimal("60.00")
