# Oncology Cohorts

Comprehensive oncology patient generation skills for PatientSim.

## Skills

| Skill | Description | Key Features |
|-------|-------------|--------------|
| [oncology-domain.md](../../../references/oncology-domain.md) | Foundational oncology knowledge | Staging, biomarkers, treatment modalities |
| [breast-cancer.md](breast-cancer.md) | Breast cancer cohorts | Molecular subtypes, hormonal/targeted therapy |
| [lung-cancer.md](lung-cancer.md) | Lung cancer cohorts | NSCLC/SCLC, biomarker-driven therapy |
| [colorectal-cancer.md](colorectal-cancer.md) | Colorectal cancer cohorts | Colon/rectal, MSI, hereditary syndromes |

## Quick Start

### Generate a Breast Cancer Patient
```
Generate a 55-year-old female with Stage IIA ER-positive, HER2-negative breast cancer
```

### Generate a Lung Cancer Patient
```
Generate a 68-year-old male with Stage IV NSCLC, EGFR exon 19 deletion positive
```

### Generate a Colorectal Cancer Patient
```
Generate a 58-year-old with Stage III colon cancer, MSI-high status
```

## Cross-Product Integration

### TrialSim (Clinical Trials)
- [TrialSim Oncology](../../trialsim/therapeutic-areas/oncology.md) - Trial endpoints, RECIST 1.1, survival analysis
- [Phase 3 Pivotal](../../trialsim/phase3-pivotal.md) - Pivotal trial cohorts
- [Recruitment & Enrollment](../../trialsim/recruitment-enrollment.md) - Screening funnels, I/E criteria

> **Integration Pattern:** Use PatientSim oncology skills for clinical care journeys. When a patient enrolls in a clinical trial, apply TrialSim skills for trial-specific data (RECIST assessments, randomization, SDTM format).

### MemberSim (Claims)
- [../membersim/facility-claims.md](../../membersim/facility-claims.md) - Infusion center claims, inpatient oncology
- [../membersim/professional-claims.md](../../membersim/professional-claims.md) - Oncology office visits, chemotherapy administration
- [../membersim/prior-authorization.md](../../membersim/prior-authorization.md) - Prior auth for specialty oncology drugs

> **Integration Pattern:** Use PatientSim for treatment regimens and clinical progression. Use MemberSim for oncology claims - chemotherapy infusions generate facility claims with J-codes, office visits generate E&M claims.

### RxMemberSim (Pharmacy)
- [../rxmembersim/specialty-pharmacy.md](../../rxmembersim/specialty-pharmacy.md) - Oral oncolytics (Ibrance, Tagrisso, Revlimid)
- [../rxmembersim/retail-pharmacy.md](../../rxmembersim/retail-pharmacy.md) - Supportive care (antiemetics, G-CSF)
- [../rxmembersim/manufacturer-programs.md](../../rxmembersim/manufacturer-programs.md) - Copay assistance, patient support programs
- [../rxmembersim/rx-prior-auth.md](../../rxmembersim/rx-prior-auth.md) - PA requirements for oral oncolytics

> **Integration Pattern:** Use PatientSim for medication orders. Use RxMemberSim for specialty pharmacy dispensing - oral oncolytics require specialty pharmacy, limited distribution, and often manufacturer copay assistance.

## Reference Data

See [references/oncology/](../../../references/oncology/) for:
- ICD-10 diagnosis codes (115 codes)
- Oncology medications (90 drugs)
- Chemotherapy regimens (48 protocols)
- Tumor markers with LOINC codes
- Staging templates by cancer type
