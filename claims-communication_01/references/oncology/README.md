# Oncology Reference Data

Reference data files for the oncology domain, supporting realistic cancer patient data generation.

## Files

| File | Description | Records |
|------|-------------|---------|
| `oncology-icd10-codes.csv` | ICD-10-CM codes for cancer diagnoses, metastatic sites, encounters, and adverse effects | ~115 codes |
| `oncology-medications.csv` | Oncology medications including chemotherapy, targeted therapy, immunotherapy, hormonal therapy, and supportive care | ~90 medications |
| `oncology-regimens.csv` | Standard chemotherapy regimens organized by cancer type | ~48 regimens |
| `oncology-tumor-markers.csv` | Tumor markers and laboratory tests with LOINC codes | ~32 markers |
| `oncology-staging-templates.yaml` | Staging systems and biomarker profiles for major cancer types | 8 cancer types |

## File Details

### oncology-icd10-codes.csv

Common oncology ICD-10-CM codes organized by category:

- **Primary malignancies**: Breast (C50.x), Lung (C34.x), Colorectal (C18-C20), Prostate (C61), Ovarian (C56.x), Pancreatic (C25.x)
- **Hematologic malignancies**: Lymphomas (C81-C85), Leukemias (C91-C95), Multiple myeloma (C90.x)
- **Metastatic sites**: Lymph nodes (C77.x), Lung (C78.0x), Liver (C78.7), Brain (C79.31), Bone (C79.51)
- **Encounter codes**: Chemotherapy (Z51.11), Radiation (Z51.0), Immunotherapy (Z51.12), Follow-up (Z08)
- **History codes**: Personal history of malignancy (Z85.x)
- **Adverse effects**: Myelosuppression, nausea, neuropathy

### oncology-medications.csv

Comprehensive oncology medication reference with:

- Generic and brand names
- Drug class (taxane, platinum, checkpoint_inhibitor, etc.)
- Route of administration
- Common cancer indications
- Premedication requirements
- Emetogenic risk level
- Myelosuppressive potential

Drug classes covered:
- Cytotoxic chemotherapy (taxanes, platinums, anthracyclines, antimetabolites, alkylating agents)
- Targeted therapy (monoclonal antibodies, tyrosine kinase inhibitors, CDK4/6 inhibitors, PARP inhibitors)
- Immunotherapy (checkpoint inhibitors)
- Hormonal therapy (SERMs, aromatase inhibitors, antiandrogens)
- Supportive care (antiemetics, growth factors, bisphosphonates)

### oncology-regimens.csv

Standard chemotherapy regimens with:

- Regimen name (e.g., FOLFOX, R-CHOP, AC-T)
- Cancer type indication
- Component drugs
- Cycle length in days
- Typical number of cycles
- Treatment setting (outpatient/inpatient)
- Treatment intent (adjuvant, neoadjuvant, curative, palliative)
- Emetogenic risk
- G-CSF requirement

Cancer types covered:
- Breast cancer
- Colorectal cancer
- Lung cancer (NSCLC and SCLC)
- Lymphoma (Hodgkin and Non-Hodgkin)
- Pancreatic cancer
- Ovarian cancer
- Testicular cancer
- Prostate cancer
- Multiple myeloma
- Leukemia (ALL, AML)

### oncology-tumor-markers.csv

Tumor markers with:

- Marker name
- LOINC code (where applicable)
- Associated cancer types
- Normal reference range
- Units
- Recommended monitoring frequency
- Specimen type
- Clinical utility

### oncology-staging-templates.yaml

Comprehensive staging information for major cancer types:

- **Breast cancer**: TNM staging, molecular subtypes (Luminal A/B, HER2+, Triple-negative), biomarkers (ER, PR, HER2, Ki-67)
- **Lung cancer NSCLC**: TNM staging, molecular testing (EGFR, ALK, ROS1, KRAS, BRAF, PD-L1)
- **Lung cancer SCLC**: Limited vs Extensive staging
- **Colorectal cancer**: TNM staging, biomarkers (MSI/MMR, RAS, BRAF)
- **Prostate cancer**: TNM staging, NCCN risk groups, Gleason grading
- **Hodgkin lymphoma**: Ann Arbor staging, B symptoms, IPS prognostic score
- **Diffuse large B-cell lymphoma**: Ann Arbor staging, cell of origin, IPI score
- **Multiple myeloma**: R-ISS staging, cytogenetics, response criteria

## Usage

These reference files are used by the oncology domain knowledge skill (`skills/healthcare/oncology-domain.md`) and cancer-specific scenario skills to ensure accurate and consistent oncology data generation.

### Example: Looking up a regimen

```python
import csv

with open('oncology-regimens.csv') as f:
    reader = csv.DictReader(f)
    folfox = next(r for r in reader if r['regimen_name'] == 'FOLFOX')
    print(f"Cycle length: {folfox['cycle_length_days']} days")
    print(f"Typical cycles: {folfox['typical_cycles']}")
```

### Example: Finding metastatic site codes

```python
import csv

with open('oncology-icd10-codes.csv') as f:
    reader = csv.DictReader(f)
    mets_codes = [r for r in reader if r['category'] == 'secondary']
    for code in mets_codes:
        print(f"{code['code']}: {code['description']}")
```

## Data Sources

Reference data compiled from:

- ICD-10-CM 2024 code set
- NCCN Clinical Practice Guidelines
- AJCC Cancer Staging Manual, 8th Edition
- National Cancer Institute drug dictionary
- ASCO/ESMO treatment guidelines
- LOINC database for laboratory codes

## Clinical Validation Notice

This reference data is intended for synthetic data generation for testing and training purposes. Clinical validation is required before use in any production or clinical decision-support context.

## Related Skills

- `skills/healthcare/oncology-domain.md` - Oncology domain knowledge skill
- `skills/healthcare/clinical-domain.md` - General clinical domain knowledge
