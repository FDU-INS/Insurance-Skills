"""DUR validation for pharmacy claims."""
from datetime import date

from pydantic import BaseModel, Field

from .alerts import DURAlertFormatter, DURAlertSummary, DUROverride
from .rules import ClinicalSignificance, DURAlert, DURRulesEngine


class MemberMedication(BaseModel):
    """Current medication for a member."""

    ndc: str
    gpi: str
    name: str
    service_date: date
    days_supply: int
    quantity: float


class MemberProfile(BaseModel):
    """Member profile for DUR checking."""

    member_id: str
    date_of_birth: date
    gender: str  # M or F

    # Current medications (active within lookback)
    current_medications: list[MemberMedication] = Field(default_factory=list)

    # Claim history
    claim_history: list[dict] = Field(default_factory=list)

    # Allergies
    drug_allergies: list[str] = Field(default_factory=list)  # GPI prefixes

    # Conditions
    conditions: list[str] = Field(default_factory=list)  # ICD-10 codes

    @property
    def age(self) -> int:
        """Calculate member age."""
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )


class DURValidationRequest(BaseModel):
    """Request for DUR validation."""

    claim_id: str
    service_date: date

    # Drug info
    ndc: str
    gpi: str
    drug_name: str
    quantity: float
    days_supply: int

    # Override codes (if provided)
    dur_override: DUROverride | None = None


class DURValidationResult(BaseModel):
    """Result of DUR validation."""

    claim_id: str
    passed: bool
    alerts: list[DURAlert] = Field(default_factory=list)

    # Alert summary
    total_alerts: int = 0
    major_alerts: int = 0
    moderate_alerts: int = 0
    minor_alerts: int = 0

    # Override status
    requires_override: bool = False
    override_provided: bool = False

    # Result codes for NCPDP
    dur_pps_response_codes: list[dict] = Field(default_factory=list)

    # Messages
    messages: list[str] = Field(default_factory=list)


class DURValidator:
    """Validate claims against DUR rules."""

    def __init__(self) -> None:
        self.rules_engine = DURRulesEngine()
        self.alert_formatter = DURAlertFormatter()

    def validate(
        self,
        request: DURValidationRequest,
        member_profile: MemberProfile,
    ) -> DURValidationResult:
        """Run all DUR checks for a claim."""
        all_alerts: list[DURAlert] = []
        messages: list[str] = []

        # Convert current medications to format needed by rules engine
        current_meds = [
            {
                "ndc": med.ndc,
                "gpi": med.gpi,
                "name": med.name,
                "service_date": med.service_date,
                "days_supply": med.days_supply,
            }
            for med in member_profile.current_medications
        ]

        # 1. Drug-Drug Interactions
        dd_alerts = self.rules_engine.check_drug_drug_interactions(
            new_drug_gpi=request.gpi,
            new_drug_ndc=request.ndc,
            new_drug_name=request.drug_name,
            current_medications=current_meds,
        )
        all_alerts.extend(dd_alerts)
        if dd_alerts:
            messages.append(f"{len(dd_alerts)} drug-drug interaction(s) found")

        # 2. Therapeutic Duplication
        td_alerts = self.rules_engine.check_therapeutic_duplication(
            new_drug_gpi=request.gpi,
            new_drug_ndc=request.ndc,
            new_drug_name=request.drug_name,
            current_medications=current_meds,
        )
        all_alerts.extend(td_alerts)
        if td_alerts:
            messages.append(f"{len(td_alerts)} therapeutic duplication(s) found")

        # 3. Early Refill
        previous_fills = [
            {
                "ndc": med.ndc,
                "service_date": med.service_date,
                "days_supply": med.days_supply,
            }
            for med in member_profile.current_medications
        ]
        er_alert = self.rules_engine.check_early_refill(
            ndc=request.ndc,
            drug_name=request.drug_name,
            service_date=request.service_date,
            previous_fills=previous_fills,
        )
        if er_alert:
            all_alerts.append(er_alert)
            messages.append("Early refill detected")

        # 4. Age Restriction
        age_alert = self.rules_engine.check_age_restriction(
            drug_gpi=request.gpi,
            drug_ndc=request.ndc,
            drug_name=request.drug_name,
            patient_age=member_profile.age,
        )
        if age_alert:
            all_alerts.append(age_alert)
            messages.append("Age restriction violation")

        # 5. Gender Restriction
        gender_alert = self.rules_engine.check_gender_restriction(
            drug_gpi=request.gpi,
            drug_ndc=request.ndc,
            drug_name=request.drug_name,
            patient_gender=member_profile.gender,
        )
        if gender_alert:
            all_alerts.append(gender_alert)
            messages.append("Gender restriction violation")

        # Count alerts by severity
        major = sum(
            1 for a in all_alerts
            if a.clinical_significance == ClinicalSignificance.LEVEL_1
        )
        moderate = sum(
            1 for a in all_alerts
            if a.clinical_significance == ClinicalSignificance.LEVEL_2
        )
        minor = sum(
            1 for a in all_alerts
            if a.clinical_significance == ClinicalSignificance.LEVEL_3
        )

        # Determine if override is required
        requires_override = major > 0
        override_provided = request.dur_override is not None

        # Determine if validation passes
        passed = len(all_alerts) == 0 or (requires_override and override_provided)

        # Generate NCPDP response codes
        dur_pps_codes = [
            self.alert_formatter.format_for_ncpdp(alert) for alert in all_alerts
        ]

        return DURValidationResult(
            claim_id=request.claim_id,
            passed=passed,
            alerts=all_alerts,
            total_alerts=len(all_alerts),
            major_alerts=major,
            moderate_alerts=moderate,
            minor_alerts=minor,
            requires_override=requires_override,
            override_provided=override_provided,
            dur_pps_response_codes=dur_pps_codes,
            messages=messages,
        )

    def validate_simple(
        self,
        ndc: str,
        gpi: str,
        drug_name: str,
        member_id: str,
        service_date: date,
        current_medications: list[dict],
        patient_age: int,
        patient_gender: str,
    ) -> DURValidationResult:
        """Simplified validation interface."""
        # Build member profile
        member_profile = MemberProfile(
            member_id=member_id,
            date_of_birth=date(
                service_date.year - patient_age,
                service_date.month,
                service_date.day,
            ),
            gender=patient_gender,
            current_medications=[
                MemberMedication(
                    ndc=med.get("ndc", ""),
                    gpi=med.get("gpi", ""),
                    name=med.get("name", ""),
                    service_date=med.get("service_date", service_date),
                    days_supply=med.get("days_supply", 30),
                    quantity=med.get("quantity", 30),
                )
                for med in current_medications
            ],
        )

        # Build request
        request = DURValidationRequest(
            claim_id=f"CLM-{member_id}-{service_date.isoformat()}",
            service_date=service_date,
            ndc=ndc,
            gpi=gpi,
            drug_name=drug_name,
            quantity=30,
            days_supply=30,
        )

        return self.validate(request, member_profile)

    def get_alert_summary(
        self,
        claim_id: str,
        alerts: list[DURAlert],
    ) -> DURAlertSummary:
        """Get formatted summary of alerts."""
        return self.alert_formatter.create_summary(claim_id, alerts)
