"""
PatientSim — Autoresearch Eval
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.eval_engine import (
    Criterion, TestCase, mentions_any, mentions_all, mentions_none,
    count_keywords, has_question, get_shared_cases, main_cli,
)

DOMAIN_CASES = [
    TestCase(id="pat-001", name="Diabetic patient generation", category="domain_accuracy",
        user_request="Generate a 65-year-old diabetic patient with hypertension.",
        criteria=[
            Criterion("demographics", "Includes age-appropriate demographics",
                      lambda r: mentions_any(r, ["65", "age", "demographics", "name"])),
            Criterion("diabetes_dx", "Assigns diabetes ICD-10 code",
                      lambda r: mentions_any(r, ["E11", "diabetes", "ICD-10"])),
            Criterion("hypertension_dx", "Assigns hypertension code",
                      lambda r: mentions_any(r, ["I10", "hypertension"])),
            Criterion("medications", "Includes appropriate medications",
                      lambda r: mentions_any(r, ["metformin", "lisinopril", "medication"])),
            Criterion("labs", "Includes relevant lab results",
                      lambda r: mentions_any(r, ["A1C", "lab", "BMP", "glucose"])),
        ]),
    TestCase(id="pat-002", name="Encounter types", category="workflow",
        user_request="Create an inpatient encounter for pneumonia.",
        criteria=[
            Criterion("inpatient_setting", "Sets inpatient encounter type",
                      lambda r: mentions_any(r, ["inpatient", "admission", "hospital"])),
            Criterion("pneumonia_dx", "Assigns pneumonia diagnosis",
                      lambda r: mentions_any(r, ["J18", "pneumonia", "respiratory"])),
            Criterion("procedures", "Includes appropriate procedures",
                      lambda r: mentions_any(r, ["CPT", "procedure", "chest", "imaging"])),
        ]),
    TestCase(id="pat-003", name="Clinical cohort routing", category="workflow",
        user_request="Generate a heart failure cohort of 20 patients.",
        criteria=[
            Criterion("cohort_size", "Creates requested number of patients",
                      lambda r: mentions_any(r, ["20", "cohort", "patients", "group"])),
            Criterion("hf_diagnosis", "Assigns heart failure diagnoses",
                      lambda r: mentions_any(r, ["I50", "heart failure", "CHF"])),
            Criterion("clinical_realism", "Includes realistic comorbidities",
                      lambda r: mentions_any(r, ["comorbid", "hypertension", "diabetes", "CKD", "renal"])),
        ]),
    TestCase(id="pat-004", name="Output format compliance", category="domain_accuracy",
        user_request="Generate a patient record in FHIR R4 format.",
        criteria=[
            Criterion("fhir_mention", "References FHIR R4 format",
                      lambda r: mentions_any(r, ["FHIR", "R4", "resource", "Bundle"])),
            Criterion("structured_output", "Produces structured data",
                      lambda r: mentions_any(r, ["Patient", "Encounter", "Condition", "resource"])),
        ]),
]

if __name__ == "__main__":
    main_cli("PatientSim", DOMAIN_CASES, domain_key="patientsim")
