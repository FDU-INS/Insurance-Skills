"""DUR alert management and formatting."""
from datetime import date

from pydantic import BaseModel, Field

from .rules import (
    ClinicalSignificance,
    DURAlert,
    DURAlertType,
    DURProfessionalService,
    DURResultOfService,
)


class DURAlertSummary(BaseModel):
    """Summary of DUR alerts for a claim."""

    claim_id: str
    total_alerts: int
    level_1_alerts: int = 0  # Major - contraindicated
    level_2_alerts: int = 0  # Moderate
    level_3_alerts: int = 0  # Minor

    alerts: list[DURAlert] = Field(default_factory=list)

    # Override status
    requires_override: bool = False
    override_provided: bool = False
    override_codes: list[str] = Field(default_factory=list)

    # Processing result
    can_proceed: bool = True
    rejection_reason: str | None = None


class DUROverride(BaseModel):
    """DUR override information."""

    alert_type: DURAlertType
    reason_for_service: str
    professional_service: str
    result_of_service: str
    pharmacist_name: str | None = None
    override_date: date | None = None
    notes: str | None = None


class DURAlertFormatter:
    """Format DUR alerts for display and transmission."""

    def format_for_display(self, alert: DURAlert) -> str:
        """Format alert for human-readable display."""
        severity_map = {
            ClinicalSignificance.LEVEL_1: "MAJOR",
            ClinicalSignificance.LEVEL_2: "MODERATE",
            ClinicalSignificance.LEVEL_3: "MINOR",
        }

        type_map = {
            DURAlertType.DRUG_DRUG: "Drug-Drug Interaction",
            DURAlertType.THERAPEUTIC_DUPLICATION: "Therapeutic Duplication",
            DURAlertType.EARLY_REFILL: "Early Refill",
            DURAlertType.HIGH_DOSE: "High Dose",
            DURAlertType.LOW_DOSE: "Low Dose",
            DURAlertType.DRUG_AGE: "Age Precaution",
            DURAlertType.DRUG_GENDER: "Gender Precaution",
            DURAlertType.DRUG_DISEASE: "Drug-Disease Contraindication",
            DURAlertType.DRUG_ALLERGY: "Drug Allergy",
            DURAlertType.DRUG_PREGNANCY: "Pregnancy Precaution",
        }

        severity = severity_map.get(alert.clinical_significance, "UNKNOWN")
        alert_type = type_map.get(alert.alert_type, alert.alert_type.value)

        lines = [
            f"[{severity}] {alert_type}",
            f"  Drug: {alert.drug1_name}",
        ]

        if alert.drug2_name:
            lines.append(f"  Interacting Drug: {alert.drug2_name}")

        lines.append(f"  Message: {alert.message}")

        if alert.recommendation:
            lines.append(f"  Recommendation: {alert.recommendation}")

        if alert.days_early:
            lines.append(f"  Days Early: {alert.days_early}")

        return "\n".join(lines)

    def format_for_ncpdp(self, alert: DURAlert) -> dict:
        """Format alert for NCPDP transmission."""
        return {
            "reason_for_service": alert.reason_for_service,
            "clinical_significance": alert.clinical_significance.value,
            "other_pharmacy_indicator": "",
            "previous_fill_date": (
                alert.previous_fill_date.strftime("%Y%m%d")
                if alert.previous_fill_date
                else ""
            ),
            "quantity_of_previous_fill": "",
            "database_indicator": "1",  # First DataBank
            "other_prescriber_indicator": "",
            "conflict_code": alert.alert_type.value,
            "intervention_code": alert.professional_service or "",
            "outcome_code": alert.result_of_service or "",
        }

    def create_summary(
        self,
        claim_id: str,
        alerts: list[DURAlert],
        override_provided: bool = False,
        override_codes: list[str] | None = None,
    ) -> DURAlertSummary:
        """Create summary of alerts for a claim."""
        level_1 = sum(
            1 for a in alerts if a.clinical_significance == ClinicalSignificance.LEVEL_1
        )
        level_2 = sum(
            1 for a in alerts if a.clinical_significance == ClinicalSignificance.LEVEL_2
        )
        level_3 = sum(
            1 for a in alerts if a.clinical_significance == ClinicalSignificance.LEVEL_3
        )

        # Major alerts require override
        requires_override = level_1 > 0

        # Determine if can proceed
        can_proceed = True
        rejection_reason = None

        if level_1 > 0 and not override_provided:
            can_proceed = False
            rejection_reason = (
                f"{level_1} major DUR alert(s) require pharmacist override"
            )

        return DURAlertSummary(
            claim_id=claim_id,
            total_alerts=len(alerts),
            level_1_alerts=level_1,
            level_2_alerts=level_2,
            level_3_alerts=level_3,
            alerts=alerts,
            requires_override=requires_override,
            override_provided=override_provided,
            override_codes=override_codes or [],
            can_proceed=can_proceed,
            rejection_reason=rejection_reason,
        )


class DUROverrideManager:
    """Manage DUR override processing."""

    VALID_PROFESSIONAL_SERVICES = [
        DURProfessionalService.PHARMACIST_CONSULTED.value,
        DURProfessionalService.PHARMACIST_APPROVED.value,
        DURProfessionalService.PRESCRIBER_CONSULTED.value,
        DURProfessionalService.PRESCRIBER_APPROVED.value,
        DURProfessionalService.PATIENT_CONSULTED.value,
    ]

    VALID_RESULTS = [
        DURResultOfService.FILLED_AS_IS.value,
        DURResultOfService.FILLED_WITH_CHANGE.value,
        DURResultOfService.FILLED_DIFFERENT_DRUG.value,
        DURResultOfService.NOT_FILLED.value,
        DURResultOfService.PARTIALLY_FILLED.value,
    ]

    def validate_override(self, override: DUROverride) -> tuple[bool, str]:
        """Validate override codes."""
        if override.professional_service not in self.VALID_PROFESSIONAL_SERVICES:
            return False, f"Invalid professional service code: {override.professional_service}"

        if override.result_of_service not in self.VALID_RESULTS:
            return False, f"Invalid result of service code: {override.result_of_service}"

        return True, "Override valid"

    def create_override(
        self,
        alert: DURAlert,
        professional_service: str,
        result_of_service: str,
        pharmacist_name: str | None = None,
        notes: str | None = None,
    ) -> DUROverride:
        """Create an override for an alert."""
        return DUROverride(
            alert_type=alert.alert_type,
            reason_for_service=alert.reason_for_service,
            professional_service=professional_service,
            result_of_service=result_of_service,
            pharmacist_name=pharmacist_name,
            override_date=date.today(),
            notes=notes,
        )

    def apply_override_to_alert(
        self, alert: DURAlert, override: DUROverride
    ) -> DURAlert:
        """Apply override codes to an alert."""
        return DURAlert(
            alert_type=alert.alert_type,
            clinical_significance=alert.clinical_significance,
            drug1_ndc=alert.drug1_ndc,
            drug1_name=alert.drug1_name,
            drug1_gpi=alert.drug1_gpi,
            drug2_ndc=alert.drug2_ndc,
            drug2_name=alert.drug2_name,
            drug2_gpi=alert.drug2_gpi,
            message=alert.message,
            recommendation=alert.recommendation,
            reason_for_service=alert.reason_for_service,
            professional_service=override.professional_service,
            result_of_service=override.result_of_service,
            days_early=alert.days_early,
            previous_fill_date=alert.previous_fill_date,
        )
