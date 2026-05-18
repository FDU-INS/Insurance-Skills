"""HEDIS measure definitions."""

from membersim.quality.measure import QualityMeasure

# HEDIS Measure Definitions
HEDIS_MEASURES: dict[str, QualityMeasure] = {
    "BCS": QualityMeasure(
        measure_id="BCS",
        measure_name="Breast Cancer Screening",
        measure_year=2024,
        denominator_criteria="Women 50-74 years with continuous enrollment",
        numerator_criteria="Mammogram within past 2 years",
        measure_type="ADMINISTRATIVE",
        measure_domain="EFFECTIVENESS",
        min_age=50,
        max_age=74,
        gender="F",
        compliant_codes=["77067", "77066", "77065", "G0202", "G0204", "G0206"],
        exclusion_codes=[
            "Z90.1",
            "Z90.10",
            "Z90.11",
            "Z90.12",
            "Z90.13",
        ],  # Bilateral mastectomy
    ),
    "CCS": QualityMeasure(
        measure_id="CCS",
        measure_name="Cervical Cancer Screening",
        measure_year=2024,
        denominator_criteria="Women 21-64 years with continuous enrollment",
        numerator_criteria="Cervical cytology (21-64) or hrHPV test (30-64)",
        measure_type="ADMINISTRATIVE",
        measure_domain="EFFECTIVENESS",
        min_age=21,
        max_age=64,
        gender="F",
        compliant_codes=[
            "88141",
            "88142",
            "88143",
            "88147",
            "88148",
            "88150",
            "88152",
            "88153",
            "88164",
            "88165",
            "88166",
            "88167",
            "88174",
            "88175",
            "G0101",
            "G0123",
            "G0124",
            "G0141",
            "G0143",
            "G0144",
            "G0145",
            "G0147",
            "G0148",
            "87624",
            "87625",
        ],  # HPV tests
    ),
    "COL": QualityMeasure(
        measure_id="COL",
        measure_name="Colorectal Cancer Screening",
        measure_year=2024,
        denominator_criteria="Adults 50-75 years with continuous enrollment",
        numerator_criteria="Colonoscopy in 10 yrs, FIT in 1 yr, or other screening",
        measure_type="ADMINISTRATIVE",
        measure_domain="EFFECTIVENESS",
        min_age=50,
        max_age=75,
        compliant_codes=[
            "45378",
            "45380",
            "45381",
            "45382",
            "45383",
            "45384",
            "45385",
            "45386",
            "45387",
            "45388",
            "45389",
            "45390",
            "45391",
            "45392",
            "82270",
            "82274",
            "G0328",
        ],  # Colonoscopy and FIT
        exclusion_codes=["Z90.49"],  # Total colectomy
    ),
    "CDC-A1C": QualityMeasure(
        measure_id="CDC-A1C",
        measure_name="Comprehensive Diabetes Care: HbA1c Testing",
        measure_year=2024,
        denominator_criteria="Adults 18-75 with diabetes",
        numerator_criteria="HbA1c test performed during measurement year",
        measure_type="ADMINISTRATIVE",
        measure_domain="EFFECTIVENESS",
        min_age=18,
        max_age=75,
        compliant_codes=["83036", "83037", "3044F", "3046F", "3051F", "3052F"],
    ),
    "CDC-EYE": QualityMeasure(
        measure_id="CDC-EYE",
        measure_name="Comprehensive Diabetes Care: Eye Exam",
        measure_year=2024,
        denominator_criteria="Adults 18-75 with diabetes",
        numerator_criteria="Dilated retinal eye exam during measurement year",
        measure_type="ADMINISTRATIVE",
        measure_domain="EFFECTIVENESS",
        min_age=18,
        max_age=75,
        compliant_codes=[
            "67028",
            "67030",
            "67031",
            "67036",
            "67039",
            "67040",
            "67041",
            "67042",
            "67043",
            "67101",
            "67105",
            "67107",
            "67108",
            "67110",
            "92002",
            "92004",
            "92012",
            "92014",
            "92227",
            "92228",
            "92230",
            "92235",
            "92240",
            "92250",
            "2022F",
            "2024F",
            "2026F",
            "3072F",
        ],
    ),
    "CBP": QualityMeasure(
        measure_id="CBP",
        measure_name="Controlling High Blood Pressure",
        measure_year=2024,
        denominator_criteria="Adults 18-85 with hypertension",
        numerator_criteria="BP adequately controlled (<140/90)",
        measure_type="HYBRID",  # Requires medical record review
        measure_domain="EFFECTIVENESS",
        min_age=18,
        max_age=85,
    ),
}


def get_measure(measure_id: str) -> QualityMeasure:
    """Get a HEDIS measure by ID."""
    if measure_id not in HEDIS_MEASURES:
        raise ValueError(f"Unknown measure: {measure_id}")
    return HEDIS_MEASURES[measure_id]


def get_all_measures() -> dict[str, QualityMeasure]:
    """Get all defined HEDIS measures."""
    return HEDIS_MEASURES.copy()


def get_measures_for_member(
    age: int,
    gender: str,
    diagnoses: list[str] | None = None,
) -> list[str]:
    """Get applicable measure IDs for a member based on demographics."""
    applicable = []

    for measure_id, measure in HEDIS_MEASURES.items():
        # Age check
        if measure.min_age and age < measure.min_age:
            continue
        if measure.max_age and age > measure.max_age:
            continue

        # Gender check
        if measure.gender and measure.gender != gender:
            continue

        # Diagnosis-based measures (simplified)
        if "CDC" in measure_id:
            # Would need diabetes diagnosis
            if diagnoses and any(dx.startswith("E11") for dx in diagnoses):
                applicable.append(measure_id)
        else:
            applicable.append(measure_id)

    return applicable
