"""Tests for DUR module."""
from datetime import date, timedelta

from rxmembersim.dur.alerts import DURAlertFormatter, DUROverrideManager
from rxmembersim.dur.rules import (
    ClinicalSignificance,
    DURAlert,
    DURAlertType,
    DURRulesEngine,
)
from rxmembersim.dur.validator import (
    DURValidationRequest,
    DURValidator,
    MemberMedication,
    MemberProfile,
)


class TestDURRulesEngine:
    """Tests for DUR rules engine."""

    def test_drug_drug_interaction_warfarin_nsaid(self) -> None:
        """Test warfarin-NSAID interaction detection."""
        engine = DURRulesEngine()

        current_meds = [
            {
                "ndc": "00056017270",
                "gpi": "83300010000330",  # Warfarin
                "name": "Warfarin 5mg",
            }
        ]

        alerts = engine.check_drug_drug_interactions(
            new_drug_gpi="66100010000310",  # NSAID
            new_drug_ndc="00000000001",
            new_drug_name="Ibuprofen 800mg",
            current_medications=current_meds,
        )

        assert len(alerts) > 0
        assert alerts[0].alert_type == DURAlertType.DRUG_DRUG
        assert alerts[0].clinical_significance == ClinicalSignificance.LEVEL_1
        assert "bleeding" in alerts[0].message.lower()

    def test_drug_drug_interaction_opioid_benzo(self) -> None:
        """Test opioid-benzodiazepine interaction detection."""
        engine = DURRulesEngine()

        current_meds = [
            {
                "ndc": "00000000001",
                "gpi": "65050010000310",  # Opioid
                "name": "Oxycodone 5mg",
            }
        ]

        alerts = engine.check_drug_drug_interactions(
            new_drug_gpi="57100010000310",  # Benzodiazepine
            new_drug_ndc="00000000002",
            new_drug_name="Alprazolam 0.5mg",
            current_medications=current_meds,
        )

        assert len(alerts) > 0
        assert alerts[0].clinical_significance == ClinicalSignificance.LEVEL_1

    def test_no_drug_interaction(self) -> None:
        """Test no interaction detected."""
        engine = DURRulesEngine()

        current_meds = [
            {
                "ndc": "00000000001",
                "gpi": "27100030000310",  # Metformin
                "name": "Metformin 500mg",
            }
        ]

        alerts = engine.check_drug_drug_interactions(
            new_drug_gpi="39400010000310",  # Statin
            new_drug_ndc="00071015523",
            new_drug_name="Atorvastatin 10mg",
            current_medications=current_meds,
        )

        assert len(alerts) == 0

    def test_therapeutic_duplication_statins(self) -> None:
        """Test therapeutic duplication detection for statins."""
        engine = DURRulesEngine()

        current_meds = [
            {
                "ndc": "00071015523",
                "gpi": "39400010000310",  # Atorvastatin
                "name": "Atorvastatin 10mg",
            }
        ]

        alerts = engine.check_therapeutic_duplication(
            new_drug_gpi="39400030000310",  # Simvastatin
            new_drug_ndc="00000000001",
            new_drug_name="Simvastatin 20mg",
            current_medications=current_meds,
        )

        assert len(alerts) > 0
        assert alerts[0].alert_type == DURAlertType.THERAPEUTIC_DUPLICATION

    def test_no_therapeutic_duplication(self) -> None:
        """Test no duplication for different classes."""
        engine = DURRulesEngine()

        current_meds = [
            {
                "ndc": "00071015523",
                "gpi": "39400010000310",  # Statin
                "name": "Atorvastatin 10mg",
            }
        ]

        alerts = engine.check_therapeutic_duplication(
            new_drug_gpi="49400020000310",  # PPI
            new_drug_ndc="00186077601",
            new_drug_name="Omeprazole 20mg",
            current_medications=current_meds,
        )

        assert len(alerts) == 0

    def test_early_refill_detected(self) -> None:
        """Test early refill detection."""
        engine = DURRulesEngine()

        previous_fills = [
            {
                "ndc": "00071015523",
                "service_date": date.today() - timedelta(days=10),
                "days_supply": 30,
            }
        ]

        alert = engine.check_early_refill(
            ndc="00071015523",
            drug_name="Atorvastatin 10mg",
            service_date=date.today(),
            previous_fills=previous_fills,
        )

        assert alert is not None
        assert alert.alert_type == DURAlertType.EARLY_REFILL
        assert alert.days_early is not None
        assert alert.days_early > 0

    def test_no_early_refill(self) -> None:
        """Test no early refill when supply is low."""
        engine = DURRulesEngine()

        previous_fills = [
            {
                "ndc": "00071015523",
                "service_date": date.today() - timedelta(days=28),
                "days_supply": 30,
            }
        ]

        alert = engine.check_early_refill(
            ndc="00071015523",
            drug_name="Atorvastatin 10mg",
            service_date=date.today(),
            previous_fills=previous_fills,
        )

        assert alert is None

    def test_age_restriction_violated(self) -> None:
        """Test age restriction violation."""
        engine = DURRulesEngine()

        alert = engine.check_age_restriction(
            drug_gpi="65100020201020",  # CNS Stimulant
            drug_ndc="00591024601",
            drug_name="Adderall 20mg",
            patient_age=70,
        )

        assert alert is not None
        assert alert.alert_type == DURAlertType.DRUG_AGE

    def test_age_restriction_passed(self) -> None:
        """Test age within allowed range."""
        engine = DURRulesEngine()

        alert = engine.check_age_restriction(
            drug_gpi="65100020201020",  # CNS Stimulant
            drug_ndc="00591024601",
            drug_name="Adderall 20mg",
            patient_age=25,
        )

        assert alert is None

    def test_gender_restriction_violated(self) -> None:
        """Test gender restriction violation."""
        engine = DURRulesEngine()

        alert = engine.check_gender_restriction(
            drug_gpi="43990010000310",  # Testosterone
            drug_ndc="00000000001",
            drug_name="Testosterone",
            patient_gender="F",
        )

        assert alert is not None
        assert alert.alert_type == DURAlertType.DRUG_GENDER

    def test_gender_restriction_passed(self) -> None:
        """Test gender within allowed."""
        engine = DURRulesEngine()

        alert = engine.check_gender_restriction(
            drug_gpi="43990010000310",  # Testosterone
            drug_ndc="00000000001",
            drug_name="Testosterone",
            patient_gender="M",
        )

        assert alert is None


class TestDURValidator:
    """Tests for DUR Validator."""

    def test_validate_with_interaction(self) -> None:
        """Test validation with drug interaction."""
        validator = DURValidator()

        member = MemberProfile(
            member_id="TEST001",
            date_of_birth=date(1980, 1, 1),
            gender="M",
            current_medications=[
                MemberMedication(
                    ndc="00056017270",
                    gpi="83300010000330",
                    name="Warfarin 5mg",
                    service_date=date.today() - timedelta(days=10),
                    days_supply=30,
                    quantity=30,
                )
            ],
        )

        request = DURValidationRequest(
            claim_id="CLM001",
            service_date=date.today(),
            ndc="00000000001",
            gpi="66100010000310",  # NSAID
            drug_name="Ibuprofen 800mg",
            quantity=30,
            days_supply=10,
        )

        result = validator.validate(request, member)

        assert result.passed is False
        assert result.total_alerts > 0
        assert result.major_alerts > 0
        assert result.requires_override is True

    def test_validate_clean(self) -> None:
        """Test validation with no alerts."""
        validator = DURValidator()

        member = MemberProfile(
            member_id="TEST001",
            date_of_birth=date(1980, 1, 1),
            gender="M",
            current_medications=[],
        )

        request = DURValidationRequest(
            claim_id="CLM001",
            service_date=date.today(),
            ndc="00071015523",
            gpi="39400010000310",
            drug_name="Atorvastatin 10mg",
            quantity=30,
            days_supply=30,
        )

        result = validator.validate(request, member)

        assert result.passed is True
        assert result.total_alerts == 0

    def test_validate_simple_interface(self) -> None:
        """Test simplified validation interface."""
        validator = DURValidator()

        result = validator.validate_simple(
            ndc="00071015523",
            gpi="39400010000310",
            drug_name="Atorvastatin 10mg",
            member_id="TEST001",
            service_date=date.today(),
            current_medications=[],
            patient_age=45,
            patient_gender="M",
        )

        assert result.passed is True


class TestDURAlertFormatter:
    """Tests for DUR alert formatting."""

    def test_format_for_display(self) -> None:
        """Test formatting alert for display."""
        formatter = DURAlertFormatter()

        alert = DURAlert(
            alert_type=DURAlertType.DRUG_DRUG,
            clinical_significance=ClinicalSignificance.LEVEL_1,
            drug1_ndc="00000000001",
            drug1_name="Ibuprofen",
            drug2_ndc="00000000002",
            drug2_name="Warfarin",
            message="Increased bleeding risk",
            recommendation="Avoid combination",
            reason_for_service="MA",
        )

        display = formatter.format_for_display(alert)

        assert "MAJOR" in display
        assert "Drug-Drug Interaction" in display
        assert "Ibuprofen" in display
        assert "Warfarin" in display

    def test_format_for_ncpdp(self) -> None:
        """Test formatting alert for NCPDP."""
        formatter = DURAlertFormatter()

        alert = DURAlert(
            alert_type=DURAlertType.DRUG_DRUG,
            clinical_significance=ClinicalSignificance.LEVEL_1,
            drug1_ndc="00000000001",
            drug1_name="Ibuprofen",
            message="Interaction",
            reason_for_service="MA",
        )

        ncpdp = formatter.format_for_ncpdp(alert)

        assert ncpdp["reason_for_service"] == "MA"
        assert ncpdp["clinical_significance"] == "1"
        assert ncpdp["conflict_code"] == "DD"

    def test_create_summary(self) -> None:
        """Test creating alert summary."""
        formatter = DURAlertFormatter()

        alerts = [
            DURAlert(
                alert_type=DURAlertType.DRUG_DRUG,
                clinical_significance=ClinicalSignificance.LEVEL_1,
                drug1_ndc="00000000001",
                drug1_name="Drug1",
                message="Interaction",
                reason_for_service="MA",
            ),
            DURAlert(
                alert_type=DURAlertType.THERAPEUTIC_DUPLICATION,
                clinical_significance=ClinicalSignificance.LEVEL_2,
                drug1_ndc="00000000002",
                drug1_name="Drug2",
                message="Duplication",
                reason_for_service="TD",
            ),
        ]

        summary = formatter.create_summary("CLM001", alerts)

        assert summary.total_alerts == 2
        assert summary.level_1_alerts == 1
        assert summary.level_2_alerts == 1
        assert summary.requires_override is True
        assert summary.can_proceed is False


class TestDUROverrideManager:
    """Tests for DUR override management."""

    def test_validate_override_valid(self) -> None:
        """Test validating a valid override."""
        from rxmembersim.dur.alerts import DUROverride

        manager = DUROverrideManager()

        override = DUROverride(
            alert_type=DURAlertType.DRUG_DRUG,
            reason_for_service="MA",
            professional_service="M0",
            result_of_service="1A",
        )

        valid, message = manager.validate_override(override)

        assert valid is True
        assert message == "Override valid"

    def test_validate_override_invalid(self) -> None:
        """Test validating an invalid override."""
        from rxmembersim.dur.alerts import DUROverride

        manager = DUROverrideManager()

        override = DUROverride(
            alert_type=DURAlertType.DRUG_DRUG,
            reason_for_service="MA",
            professional_service="XX",  # Invalid
            result_of_service="1A",
        )

        valid, message = manager.validate_override(override)

        assert valid is False
        assert "Invalid professional service" in message

    def test_create_override(self) -> None:
        """Test creating an override."""
        manager = DUROverrideManager()

        alert = DURAlert(
            alert_type=DURAlertType.DRUG_DRUG,
            clinical_significance=ClinicalSignificance.LEVEL_1,
            drug1_ndc="00000000001",
            drug1_name="Test Drug",
            message="Test interaction",
            reason_for_service="MA",
        )

        override = manager.create_override(
            alert=alert,
            professional_service="M0",
            result_of_service="1A",
            pharmacist_name="John Pharmacist",
        )

        assert override.professional_service == "M0"
        assert override.result_of_service == "1A"
        assert override.pharmacist_name == "John Pharmacist"
