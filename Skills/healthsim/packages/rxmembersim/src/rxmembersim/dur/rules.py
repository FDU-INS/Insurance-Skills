"""Drug Utilization Review rules engine."""
from datetime import date, timedelta
from enum import Enum

from pydantic import BaseModel


class DURAlertType(str, Enum):
    """DUR alert types (NCPDP standard)."""

    DRUG_DRUG = "DD"  # Drug-drug interaction
    DRUG_DISEASE = "DC"  # Drug-disease contraindication
    THERAPEUTIC_DUPLICATION = "TD"  # Duplicate therapy
    EARLY_REFILL = "ER"  # Refill too soon
    HIGH_DOSE = "HD"  # High dose alert
    LOW_DOSE = "LD"  # Low dose alert
    DRUG_AGE = "PA"  # Drug-age precaution
    DRUG_GENDER = "PG"  # Drug-gender precaution
    DRUG_PREGNANCY = "PP"  # Drug-pregnancy precaution
    DRUG_LACTATION = "PL"  # Drug-lactation precaution
    DRUG_ALLERGY = "DA"  # Drug-allergy alert
    OVERUSE = "MX"  # Overuse/misuse
    UNDERUSE = "MN"  # Underuse
    DRUG_FOOD = "DF"  # Drug-food interaction


class ClinicalSignificance(str, Enum):
    """Clinical significance levels."""

    LEVEL_1 = "1"  # Major - contraindicated, do not dispense
    LEVEL_2 = "2"  # Moderate - use with caution
    LEVEL_3 = "3"  # Minor - minimal risk


class DURReasonForService(str, Enum):
    """NCPDP Reason for Service codes."""

    DRUG_DRUG_INTERACTION = "MA"
    THERAPEUTIC_DUPLICATION = "TD"
    EARLY_REFILL = "ER"
    OVERUSE = "MX"
    UNDERUSE = "MN"
    HIGH_DOSE = "HD"
    LOW_DOSE = "LD"
    DRUG_AGE = "PA"
    DRUG_GENDER = "PG"
    DRUG_DISEASE = "DC"
    DRUG_ALLERGY = "DA"
    DRUG_PREGNANCY = "PP"
    LACTATION_CONFLICT = "PL"


class DURProfessionalService(str, Enum):
    """NCPDP Professional Service codes."""

    PHARMACIST_CONSULTED = "M0"
    PHARMACIST_APPROVED = "M1"
    PRESCRIBER_CONSULTED = "P0"
    PRESCRIBER_APPROVED = "R0"
    PATIENT_CONSULTED = "CC"


class DURResultOfService(str, Enum):
    """NCPDP Result of Service codes."""

    FILLED_AS_IS = "1A"
    FILLED_WITH_CHANGE = "1B"
    FILLED_DIFFERENT_DRUG = "1C"
    NOT_FILLED = "1E"
    PARTIALLY_FILLED = "1G"


class DURAlert(BaseModel):
    """DUR alert."""

    alert_type: DURAlertType
    clinical_significance: ClinicalSignificance

    drug1_ndc: str
    drug1_name: str
    drug1_gpi: str | None = None

    drug2_ndc: str | None = None
    drug2_name: str | None = None
    drug2_gpi: str | None = None

    message: str
    recommendation: str | None = None

    # NCPDP DUR/PPS codes
    reason_for_service: str
    professional_service: str | None = None
    result_of_service: str | None = None

    # For early refill alerts
    days_early: int | None = None
    previous_fill_date: date | None = None


class DrugDrugInteraction(BaseModel):
    """Drug-drug interaction rule."""

    interaction_id: str
    drug1_gpi: str  # GPI prefix for first drug
    drug2_gpi: str  # GPI prefix for second drug
    drug1_name: str
    drug2_name: str
    interaction_description: str
    clinical_effect: str
    clinical_significance: ClinicalSignificance
    recommendation: str
    documentation_level: str = "Good"  # Good, Fair, Poor


class TherapeuticDuplication(BaseModel):
    """Therapeutic duplication rule."""

    duplication_id: str
    gpi_class: str  # GPI prefix for therapeutic class
    class_name: str
    max_concurrent: int = 1
    significance: ClinicalSignificance = ClinicalSignificance.LEVEL_2


class AgeRestriction(BaseModel):
    """Age-based restriction."""

    restriction_id: str
    drug_gpi: str
    drug_name: str
    min_age: int | None = None
    max_age: int | None = None
    significance: ClinicalSignificance = ClinicalSignificance.LEVEL_2
    message: str


class GenderRestriction(BaseModel):
    """Gender-based restriction."""

    restriction_id: str
    drug_gpi: str
    drug_name: str
    allowed_gender: str  # M or F
    significance: ClinicalSignificance = ClinicalSignificance.LEVEL_1
    message: str


class DURRulesEngine:
    """DUR rules processing engine."""

    def __init__(self) -> None:
        self.drug_interactions: list[DrugDrugInteraction] = []
        self.therapeutic_duplications: list[TherapeuticDuplication] = []
        self.age_restrictions: list[AgeRestriction] = []
        self.gender_restrictions: list[GenderRestriction] = []
        self._load_default_rules()

    def _load_default_rules(self) -> None:
        """Load common DUR rules."""
        self._load_drug_interactions()
        self._load_therapeutic_duplications()
        self._load_age_restrictions()
        self._load_gender_restrictions()

    def _load_drug_interactions(self) -> None:
        """Load common drug-drug interactions."""
        self.drug_interactions = [
            # Warfarin interactions
            DrugDrugInteraction(
                interaction_id="DD-001",
                drug1_gpi="8330",
                drug2_gpi="6610",
                drug1_name="Warfarin",
                drug2_name="NSAIDs",
                interaction_description="Increased bleeding risk",
                clinical_effect="NSAIDs increase anticoagulant effect and bleeding risk",
                clinical_significance=ClinicalSignificance.LEVEL_1,
                recommendation="Avoid combination or use with close monitoring",
            ),
            DrugDrugInteraction(
                interaction_id="DD-002",
                drug1_gpi="8330",
                drug2_gpi="0510",
                drug1_name="Warfarin",
                drug2_name="Fluoroquinolones",
                interaction_description="Increased INR",
                clinical_effect="Fluoroquinolones may increase warfarin effect",
                clinical_significance=ClinicalSignificance.LEVEL_2,
                recommendation="Monitor INR closely when starting/stopping",
            ),
            # Statin interactions
            DrugDrugInteraction(
                interaction_id="DD-003",
                drug1_gpi="3940",
                drug2_gpi="0490",
                drug1_name="Statins",
                drug2_name="Macrolides",
                interaction_description="Increased myopathy risk",
                clinical_effect="Macrolides inhibit statin metabolism",
                clinical_significance=ClinicalSignificance.LEVEL_2,
                recommendation="Use lower statin dose or avoid combination",
            ),
            DrugDrugInteraction(
                interaction_id="DD-004",
                drug1_gpi="39400010",  # Simvastatin
                drug2_gpi="3445",  # Calcium channel blockers
                drug1_name="Simvastatin",
                drug2_name="Diltiazem/Verapamil",
                interaction_description="Increased myopathy risk",
                clinical_effect="CCBs inhibit simvastatin metabolism",
                clinical_significance=ClinicalSignificance.LEVEL_2,
                recommendation="Limit simvastatin to 10mg with diltiazem/verapamil",
            ),
            # Opioid interactions
            DrugDrugInteraction(
                interaction_id="DD-005",
                drug1_gpi="6505",
                drug2_gpi="5710",
                drug1_name="Opioids",
                drug2_name="Benzodiazepines",
                interaction_description="CNS depression - death risk",
                clinical_effect="Concurrent use increases overdose risk",
                clinical_significance=ClinicalSignificance.LEVEL_1,
                recommendation="Avoid combination when possible",
            ),
            DrugDrugInteraction(
                interaction_id="DD-006",
                drug1_gpi="6505",
                drug2_gpi="6105",
                drug1_name="Opioids",
                drug2_name="Muscle Relaxants",
                interaction_description="CNS depression",
                clinical_effect="Additive sedation and respiratory depression",
                clinical_significance=ClinicalSignificance.LEVEL_2,
                recommendation="Use caution, consider dose reduction",
            ),
            # Methotrexate interactions
            DrugDrugInteraction(
                interaction_id="DD-007",
                drug1_gpi="6620",
                drug2_gpi="6610",
                drug1_name="Methotrexate",
                drug2_name="NSAIDs",
                interaction_description="Methotrexate toxicity",
                clinical_effect="NSAIDs decrease methotrexate clearance",
                clinical_significance=ClinicalSignificance.LEVEL_1,
                recommendation="Avoid high-dose MTX with NSAIDs",
            ),
            # SSRI interactions
            DrugDrugInteraction(
                interaction_id="DD-008",
                drug1_gpi="5816",
                drug2_gpi="5812",
                drug1_name="SSRIs",
                drug2_name="MAOIs",
                interaction_description="Serotonin syndrome",
                clinical_effect="Life-threatening serotonin excess",
                clinical_significance=ClinicalSignificance.LEVEL_1,
                recommendation="Contraindicated - do not combine",
            ),
            DrugDrugInteraction(
                interaction_id="DD-009",
                drug1_gpi="5816",
                drug2_gpi="5830",
                drug1_name="SSRIs",
                drug2_name="Triptans",
                interaction_description="Serotonin syndrome risk",
                clinical_effect="Potential serotonin excess",
                clinical_significance=ClinicalSignificance.LEVEL_2,
                recommendation="Use with caution, monitor for symptoms",
            ),
            # QT prolongation
            DrugDrugInteraction(
                interaction_id="DD-010",
                drug1_gpi="0455",
                drug2_gpi="0490",
                drug1_name="Azithromycin",
                drug2_name="Levofloxacin",
                interaction_description="QT prolongation",
                clinical_effect="Additive QT prolongation risk",
                clinical_significance=ClinicalSignificance.LEVEL_2,
                recommendation="Avoid combination, monitor ECG if needed",
            ),
        ]

    def _load_therapeutic_duplications(self) -> None:
        """Load therapeutic duplication rules."""
        self.therapeutic_duplications = [
            TherapeuticDuplication(
                duplication_id="TD-001",
                gpi_class="3940",
                class_name="HMG-CoA Reductase Inhibitors (Statins)",
                max_concurrent=1,
            ),
            TherapeuticDuplication(
                duplication_id="TD-002",
                gpi_class="4940",
                class_name="Proton Pump Inhibitors",
                max_concurrent=1,
            ),
            TherapeuticDuplication(
                duplication_id="TD-003",
                gpi_class="5816",
                class_name="SSRIs",
                max_concurrent=1,
            ),
            TherapeuticDuplication(
                duplication_id="TD-004",
                gpi_class="3615",
                class_name="ACE Inhibitors",
                max_concurrent=1,
            ),
            TherapeuticDuplication(
                duplication_id="TD-005",
                gpi_class="3617",
                class_name="ARBs",
                max_concurrent=1,
            ),
            TherapeuticDuplication(
                duplication_id="TD-006",
                gpi_class="6505",
                class_name="Opioid Analgesics",
                max_concurrent=2,  # May have short + long acting
                significance=ClinicalSignificance.LEVEL_2,
            ),
        ]

    def _load_age_restrictions(self) -> None:
        """Load age-based restrictions."""
        self.age_restrictions = [
            AgeRestriction(
                restriction_id="AGE-001",
                drug_gpi="6510",
                drug_name="CNS Stimulants",
                min_age=6,
                max_age=65,
                message="CNS stimulants: typically ages 6-65",
            ),
            AgeRestriction(
                restriction_id="AGE-002",
                drug_gpi="0455",
                drug_name="Fluoroquinolones",
                min_age=18,
                significance=ClinicalSignificance.LEVEL_2,
                message="Fluoroquinolones not recommended in children",
            ),
        ]

    def _load_gender_restrictions(self) -> None:
        """Load gender-based restrictions."""
        self.gender_restrictions = [
            GenderRestriction(
                restriction_id="GEN-001",
                drug_gpi="4399",
                drug_name="Testosterone",
                allowed_gender="M",
                message="Testosterone indicated for males only",
            ),
            GenderRestriction(
                restriction_id="GEN-002",
                drug_gpi="4320",
                drug_name="Estrogens",
                allowed_gender="F",
                message="Estrogens typically indicated for females",
            ),
        ]

    def check_drug_drug_interactions(
        self,
        new_drug_gpi: str,
        new_drug_ndc: str,
        new_drug_name: str,
        current_medications: list[dict],
    ) -> list[DURAlert]:
        """Check for drug-drug interactions."""
        alerts: list[DURAlert] = []

        for current_med in current_medications:
            current_gpi = current_med.get("gpi", "")
            current_ndc = current_med.get("ndc", "")
            current_name = current_med.get("name", "")

            for interaction in self.drug_interactions:
                # Check if either direction matches
                match1 = (
                    new_drug_gpi.startswith(interaction.drug1_gpi)
                    and current_gpi.startswith(interaction.drug2_gpi)
                )
                match2 = (
                    new_drug_gpi.startswith(interaction.drug2_gpi)
                    and current_gpi.startswith(interaction.drug1_gpi)
                )

                if match1 or match2:
                    alerts.append(
                        DURAlert(
                            alert_type=DURAlertType.DRUG_DRUG,
                            clinical_significance=interaction.clinical_significance,
                            drug1_ndc=new_drug_ndc,
                            drug1_name=new_drug_name,
                            drug1_gpi=new_drug_gpi,
                            drug2_ndc=current_ndc,
                            drug2_name=current_name,
                            drug2_gpi=current_gpi,
                            message=interaction.interaction_description,
                            recommendation=interaction.recommendation,
                            reason_for_service=DURReasonForService.DRUG_DRUG_INTERACTION.value,
                        )
                    )

        return alerts

    def check_therapeutic_duplication(
        self,
        new_drug_gpi: str,
        new_drug_ndc: str,
        new_drug_name: str,
        current_medications: list[dict],
    ) -> list[DURAlert]:
        """Check for therapeutic duplication."""
        alerts: list[DURAlert] = []

        for dup_rule in self.therapeutic_duplications:
            if not new_drug_gpi.startswith(dup_rule.gpi_class):
                continue

            # Count current medications in same class
            same_class = [
                med
                for med in current_medications
                if med.get("gpi", "").startswith(dup_rule.gpi_class)
            ]

            if len(same_class) >= dup_rule.max_concurrent:
                for existing in same_class:
                    alerts.append(
                        DURAlert(
                            alert_type=DURAlertType.THERAPEUTIC_DUPLICATION,
                            clinical_significance=dup_rule.significance,
                            drug1_ndc=new_drug_ndc,
                            drug1_name=new_drug_name,
                            drug1_gpi=new_drug_gpi,
                            drug2_ndc=existing.get("ndc", ""),
                            drug2_name=existing.get("name", ""),
                            drug2_gpi=existing.get("gpi", ""),
                            message=f"Therapeutic duplication: {dup_rule.class_name}",
                            recommendation=f"Maximum {dup_rule.max_concurrent} concurrent",
                            reason_for_service=DURReasonForService.THERAPEUTIC_DUPLICATION.value,
                        )
                    )

        return alerts

    def check_early_refill(
        self,
        ndc: str,
        drug_name: str,
        service_date: date,
        previous_fills: list[dict],
        threshold_percent: float = 0.80,
    ) -> DURAlert | None:
        """Check for early refill."""
        if not previous_fills:
            return None

        # Find most recent fill for this NDC
        same_drug_fills = [
            fill for fill in previous_fills if fill.get("ndc") == ndc
        ]

        if not same_drug_fills:
            return None

        # Get most recent
        last_fill = max(
            same_drug_fills,
            key=lambda f: f.get("service_date", date.min),
        )

        last_fill_date = last_fill.get("service_date")
        last_days_supply = last_fill.get("days_supply", 30)

        if not last_fill_date:
            return None

        # Calculate expected empty date
        expected_empty = last_fill_date + timedelta(days=last_days_supply)
        days_early = (expected_empty - service_date).days

        # Threshold is typically 80% used
        threshold_days = int(last_days_supply * (1 - threshold_percent))

        if days_early > threshold_days:
            return DURAlert(
                alert_type=DURAlertType.EARLY_REFILL,
                clinical_significance=ClinicalSignificance.LEVEL_3,
                drug1_ndc=ndc,
                drug1_name=drug_name,
                message=(
                    f"Refill {days_early} days early "
                    f"(before {threshold_percent*100:.0f}% used)"
                ),
                recommendation="Wait until medication supply is lower",
                reason_for_service=DURReasonForService.EARLY_REFILL.value,
                days_early=days_early,
                previous_fill_date=last_fill_date,
            )

        return None

    def check_age_restriction(
        self,
        drug_gpi: str,
        drug_ndc: str,
        drug_name: str,
        patient_age: int,
    ) -> DURAlert | None:
        """Check for age-based restrictions."""
        for restriction in self.age_restrictions:
            if not drug_gpi.startswith(restriction.drug_gpi):
                continue

            violated = False
            if restriction.min_age and patient_age < restriction.min_age:
                violated = True
            if restriction.max_age and patient_age > restriction.max_age:
                violated = True

            if violated:
                return DURAlert(
                    alert_type=DURAlertType.DRUG_AGE,
                    clinical_significance=restriction.significance,
                    drug1_ndc=drug_ndc,
                    drug1_name=drug_name,
                    drug1_gpi=drug_gpi,
                    message=restriction.message,
                    recommendation=f"Patient age {patient_age} outside range "
                    f"{restriction.min_age or 0}-{restriction.max_age or 'unlimited'}",
                    reason_for_service=DURReasonForService.DRUG_AGE.value,
                )

        return None

    def check_gender_restriction(
        self,
        drug_gpi: str,
        drug_ndc: str,
        drug_name: str,
        patient_gender: str,
    ) -> DURAlert | None:
        """Check for gender-based restrictions."""
        for restriction in self.gender_restrictions:
            if not drug_gpi.startswith(restriction.drug_gpi):
                continue

            if patient_gender != restriction.allowed_gender:
                return DURAlert(
                    alert_type=DURAlertType.DRUG_GENDER,
                    clinical_significance=restriction.significance,
                    drug1_ndc=drug_ndc,
                    drug1_name=drug_name,
                    drug1_gpi=drug_gpi,
                    message=restriction.message,
                    recommendation=f"Drug intended for gender: {restriction.allowed_gender}",
                    reason_for_service=DURReasonForService.DRUG_GENDER.value,
                )

        return None
