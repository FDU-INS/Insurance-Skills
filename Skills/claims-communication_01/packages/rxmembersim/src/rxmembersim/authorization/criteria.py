"""Clinical criteria for prior authorization."""

from enum import Enum

from pydantic import BaseModel, Field


class CriterionType(str, Enum):
    """Type of clinical criterion."""

    DIAGNOSIS = "diagnosis"
    PREVIOUS_THERAPY = "previous_therapy"
    LAB_RESULT = "lab_result"
    SPECIALIST = "specialist"
    AGE = "age"
    QUANTITY = "quantity"


class ClinicalCriterion(BaseModel):
    """Single clinical criterion for PA evaluation."""

    criterion_id: str
    criterion_type: CriterionType
    description: str
    required: bool = True

    # Diagnosis criteria
    diagnosis_codes: list[str] = Field(default_factory=list)

    # Previous therapy criteria
    required_therapies: list[str] = Field(default_factory=list)
    therapy_min_days: int = 0

    # Specialist criteria
    specialist_types: list[str] = Field(default_factory=list)

    # Age criteria
    min_age: int | None = None
    max_age: int | None = None

    # Lab result criteria
    lab_test: str | None = None
    lab_min_value: float | None = None
    lab_max_value: float | None = None

    # Quantity criteria
    max_quantity: int | None = None
    max_days_supply: int | None = None


class CriteriaEvaluationResult(BaseModel):
    """Result of evaluating clinical criteria."""

    criteria_set_id: str
    met: bool
    criteria_evaluated: int
    criteria_met: int
    unmet_criteria: list[str] = Field(default_factory=list)
    details: dict[str, bool] = Field(default_factory=dict)


class ClinicalCriteriaSet(BaseModel):
    """Set of clinical criteria for a drug."""

    criteria_set_id: str
    drug_gpi: str
    drug_name: str
    description: str | None = None
    criteria: list[ClinicalCriterion]
    require_all: bool = True  # If True, all required criteria must be met

    def evaluate(
        self,
        diagnosis_codes: list[str],
        previous_therapies: list[str],
        prescriber_specialty: str | None = None,
        member_age: int = 0,
        lab_results: dict[str, float] | None = None,
        quantity_requested: int = 0,
        days_supply_requested: int = 0,
    ) -> CriteriaEvaluationResult:
        """
        Evaluate criteria against provided information.

        Returns CriteriaEvaluationResult with met status and details.
        """
        unmet: list[str] = []
        details: dict[str, bool] = {}
        met_count = 0

        for criterion in self.criteria:
            criterion_met = self._evaluate_single(
                criterion,
                diagnosis_codes,
                previous_therapies,
                prescriber_specialty,
                member_age,
                lab_results or {},
                quantity_requested,
                days_supply_requested,
            )

            details[criterion.criterion_id] = criterion_met

            if criterion_met:
                met_count += 1
            elif criterion.required:
                unmet.append(criterion.description)

        # Determine if overall criteria are met
        overall_met = len(unmet) == 0 if self.require_all else met_count > 0

        return CriteriaEvaluationResult(
            criteria_set_id=self.criteria_set_id,
            met=overall_met,
            criteria_evaluated=len(self.criteria),
            criteria_met=met_count,
            unmet_criteria=unmet,
            details=details,
        )

    def _evaluate_single(
        self,
        criterion: ClinicalCriterion,
        diagnosis_codes: list[str],
        previous_therapies: list[str],
        prescriber_specialty: str | None,
        member_age: int,
        lab_results: dict[str, float],
        quantity_requested: int,
        days_supply_requested: int,
    ) -> bool:
        """Evaluate a single criterion."""
        if criterion.criterion_type == CriterionType.DIAGNOSIS:
            return self._check_diagnosis(criterion, diagnosis_codes)

        elif criterion.criterion_type == CriterionType.PREVIOUS_THERAPY:
            return self._check_previous_therapy(criterion, previous_therapies)

        elif criterion.criterion_type == CriterionType.SPECIALIST:
            return self._check_specialist(criterion, prescriber_specialty)

        elif criterion.criterion_type == CriterionType.AGE:
            return self._check_age(criterion, member_age)

        elif criterion.criterion_type == CriterionType.LAB_RESULT:
            return self._check_lab_result(criterion, lab_results)

        elif criterion.criterion_type == CriterionType.QUANTITY:
            return self._check_quantity(
                criterion, quantity_requested, days_supply_requested
            )

        return True

    def _check_diagnosis(
        self, criterion: ClinicalCriterion, diagnosis_codes: list[str]
    ) -> bool:
        """Check if any required diagnosis code is present."""
        if not criterion.diagnosis_codes:
            return True
        return any(
            self._diagnosis_matches(d, criterion.diagnosis_codes)
            for d in diagnosis_codes
        )

    def _diagnosis_matches(self, code: str, required_codes: list[str]) -> bool:
        """Check if diagnosis code matches any required code (prefix matching)."""
        return any(code == required or code.startswith(required) for required in required_codes)

    def _check_previous_therapy(
        self, criterion: ClinicalCriterion, previous_therapies: list[str]
    ) -> bool:
        """Check if previous therapy requirements are met."""
        if not criterion.required_therapies:
            return True
        return any(t in criterion.required_therapies for t in previous_therapies)

    def _check_specialist(
        self, criterion: ClinicalCriterion, prescriber_specialty: str | None
    ) -> bool:
        """Check if prescriber is required specialist type."""
        if not criterion.specialist_types:
            return True
        if not prescriber_specialty:
            return False
        return prescriber_specialty in criterion.specialist_types

    def _check_age(self, criterion: ClinicalCriterion, member_age: int) -> bool:
        """Check if member age is within allowed range."""
        if criterion.min_age is not None and member_age < criterion.min_age:
            return False
        return not (criterion.max_age is not None and member_age > criterion.max_age)

    def _check_lab_result(
        self, criterion: ClinicalCriterion, lab_results: dict[str, float]
    ) -> bool:
        """Check if lab result is within required range."""
        if not criterion.lab_test:
            return True
        if criterion.lab_test not in lab_results:
            return False

        value = lab_results[criterion.lab_test]
        if criterion.lab_min_value is not None and value < criterion.lab_min_value:
            return False
        return not (criterion.lab_max_value is not None and value > criterion.lab_max_value)

    def _check_quantity(
        self,
        criterion: ClinicalCriterion,
        quantity_requested: int,
        days_supply_requested: int,
    ) -> bool:
        """Check if quantity/days supply is within limits."""
        if (
            criterion.max_quantity is not None
            and quantity_requested > criterion.max_quantity
        ):
            return False
        return not (
            criterion.max_days_supply is not None
            and days_supply_requested > criterion.max_days_supply
        )


class ClinicalCriteriaLibrary:
    """Library of pre-built clinical criteria sets."""

    @staticmethod
    def glp1_criteria() -> ClinicalCriteriaSet:
        """Clinical criteria for GLP-1 agonists (Ozempic, Wegovy, etc.)."""
        return ClinicalCriteriaSet(
            criteria_set_id="GLP1-PA-001",
            drug_gpi="27200060",
            drug_name="GLP-1 Agonists",
            description="Criteria for GLP-1 receptor agonists",
            criteria=[
                ClinicalCriterion(
                    criterion_id="GLP1-DX",
                    criterion_type=CriterionType.DIAGNOSIS,
                    description="Diagnosis of type 2 diabetes (E11.x) or obesity (E66.x)",
                    required=True,
                    diagnosis_codes=["E11", "E66"],
                ),
                ClinicalCriterion(
                    criterion_id="GLP1-STEP",
                    criterion_type=CriterionType.PREVIOUS_THERAPY,
                    description="Trial of metformin for at least 90 days",
                    required=True,
                    required_therapies=["metformin", "2710003"],
                    therapy_min_days=90,
                ),
                ClinicalCriterion(
                    criterion_id="GLP1-A1C",
                    criterion_type=CriterionType.LAB_RESULT,
                    description="HbA1c >= 7.0%",
                    required=False,
                    lab_test="HbA1c",
                    lab_min_value=7.0,
                ),
            ],
            require_all=True,
        )

    @staticmethod
    def tnf_inhibitor_criteria() -> ClinicalCriteriaSet:
        """Clinical criteria for TNF inhibitors (Humira, Enbrel, etc.)."""
        return ClinicalCriteriaSet(
            criteria_set_id="TNF-PA-001",
            drug_gpi="66400020",
            drug_name="TNF Inhibitors",
            description="Criteria for TNF-alpha inhibitors",
            criteria=[
                ClinicalCriterion(
                    criterion_id="TNF-DX",
                    criterion_type=CriterionType.DIAGNOSIS,
                    description="Diagnosis of RA (M05/M06), Psoriasis (L40), or Crohn's (K50)",
                    required=True,
                    diagnosis_codes=["M05", "M06", "L40", "K50"],
                ),
                ClinicalCriterion(
                    criterion_id="TNF-STEP1",
                    criterion_type=CriterionType.PREVIOUS_THERAPY,
                    description="Trial of methotrexate for at least 90 days",
                    required=True,
                    required_therapies=["methotrexate", "6620001"],
                    therapy_min_days=90,
                ),
                ClinicalCriterion(
                    criterion_id="TNF-SPEC",
                    criterion_type=CriterionType.SPECIALIST,
                    description="Prescribed by rheumatologist, dermatologist, or GI",
                    required=True,
                    specialist_types=[
                        "rheumatology",
                        "dermatology",
                        "gastroenterology",
                    ],
                ),
            ],
            require_all=True,
        )

    @staticmethod
    def stimulant_criteria() -> ClinicalCriteriaSet:
        """Clinical criteria for CNS stimulants (Adderall, Vyvanse, etc.)."""
        return ClinicalCriteriaSet(
            criteria_set_id="STIM-PA-001",
            drug_gpi="65100020",
            drug_name="CNS Stimulants",
            description="Criteria for ADHD stimulant medications",
            criteria=[
                ClinicalCriterion(
                    criterion_id="STIM-DX",
                    criterion_type=CriterionType.DIAGNOSIS,
                    description="Diagnosis of ADHD (F90.x)",
                    required=True,
                    diagnosis_codes=["F90"],
                ),
                ClinicalCriterion(
                    criterion_id="STIM-AGE",
                    criterion_type=CriterionType.AGE,
                    description="Age between 6 and 65 years",
                    required=True,
                    min_age=6,
                    max_age=65,
                ),
                ClinicalCriterion(
                    criterion_id="STIM-QTY",
                    criterion_type=CriterionType.QUANTITY,
                    description="Maximum 60 units per 30 days",
                    required=True,
                    max_quantity=60,
                    max_days_supply=30,
                ),
            ],
            require_all=True,
        )
