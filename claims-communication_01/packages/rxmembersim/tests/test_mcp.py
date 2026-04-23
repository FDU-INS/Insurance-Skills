"""Tests for MCP tools (without actual MCP server)."""

from datetime import date
from decimal import Decimal

from rxmembersim.mcp.server import (
    dur_validator,
    formulary,
    member_generator,
    pa_workflow,
    journey_engine,
)
from rxmembersim.journeys import (
    get_rx_journey_template,
    RX_JOURNEY_TEMPLATES,
    list_rx_journey_templates,
)


class TestMCPComponents:
    """Tests for MCP server components."""

    def test_member_generator(self) -> None:
        """Test member generator creates valid members."""
        member = member_generator.generate()
        assert member.member_id.startswith("RXM-")
        assert member.bin is not None
        assert member.pcn is not None

    def test_member_generator_with_params(self) -> None:
        """Test member generator with custom parameters."""
        member = member_generator.generate(
            bin="999999",
            pcn="TESTPCN",
            group_number="TESTGRP",
        )
        assert member.bin == "999999"
        assert member.pcn == "TESTPCN"
        assert member.group_number == "TESTGRP"

    def test_formulary(self) -> None:
        """Test formulary coverage lookup."""
        status = formulary.check_coverage("00071015523")
        assert status.covered is True

    def test_formulary_drug_count(self) -> None:
        """Test formulary has drugs loaded."""
        assert len(formulary.drugs) >= 5

    def test_dur_validator(self) -> None:
        """Test DUR validator returns result."""
        result = dur_validator.validate_simple(
            ndc="00000000001",
            gpi="39400010000000",
            drug_name="Test Drug",
            member_id="TEST",
            service_date=date.today(),
            current_medications=[],
            patient_age=45,
            patient_gender="M",
        )
        assert hasattr(result, "passed")

    def test_pa_workflow_create_request(self) -> None:
        """Test PA workflow creates request."""
        request = pa_workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00078057715",
            drug_name="Ozempic",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
        )
        assert request.pa_request_id.startswith("PA-")
        assert request.drug_name == "Ozempic"

    def test_pa_workflow_auto_approval(self) -> None:
        """Test PA workflow auto-approval for emergency."""
        request = pa_workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00078057715",
            drug_name="Ozempic",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            urgency="emergency",
        )
        response = pa_workflow.check_auto_approval(request)
        assert response is not None
        assert response.auto_approved is True

    def test_journey_engine_list_templates(self) -> None:
        """Test journey engine lists journey templates."""
        templates = list_rx_journey_templates()
        assert len(templates) >= 5
        assert "new-therapy-start" in templates
        assert "specialty-onboarding" in templates

    def test_journey_engine_create_timeline(self) -> None:
        """Test journey engine creates timeline from template."""
        journey = get_rx_journey_template("new-therapy-start")
        rx_member = {"member_id": "MEM001"}
        
        timeline = journey_engine.create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=journey,
            start_date=date.today(),
        )
        
        assert len(timeline.events) >= 3
        assert timeline.entity_id == "MEM001"


class TestMCPIntegration:
    """Integration tests for MCP workflow."""

    def test_member_to_pa_workflow(self) -> None:
        """Test generating member and submitting PA."""
        # Generate member
        member = member_generator.generate()

        # Create PA request
        request = pa_workflow.create_request(
            member_id=member.member_id,
            cardholder_id=member.cardholder_id,
            ndc="00169413512",
            drug_name="Ozempic",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
        )

        assert request.member_id == member.member_id

    def test_formulary_to_dur_workflow(self) -> None:
        """Test checking formulary then running DUR."""
        # Check formulary
        status = formulary.check_coverage("00069015430")  # Lipitor

        # Run DUR if covered
        if status.covered:
            result = dur_validator.validate_simple(
                ndc="00069015430",
                gpi="39400010100310",
                drug_name="Lipitor",
                member_id="TEST",
                service_date=date.today(),
                current_medications=[],
                patient_age=55,
                patient_gender="F",
            )
            assert result is not None

    def test_member_journey_workflow(self) -> None:
        """Test generating member and executing a journey."""
        # Generate member
        member = member_generator.generate()
        
        # Get journey template
        journey = get_rx_journey_template("new-therapy-start")
        
        # Create timeline
        timeline = journey_engine.create_timeline(
            entity={"member_id": member.member_id},
            entity_type="rx_member",
            journey=journey,
            start_date=date.today(),
        )
        
        assert timeline.entity_id == member.member_id
        assert len(timeline.events) >= 3
