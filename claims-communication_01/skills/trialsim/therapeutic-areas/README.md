# Therapeutic Area Skills

Indication-specific knowledge for generating realistic clinical trial data with appropriate endpoints, assessments, and treatment patterns.

## Available Therapeutic Areas

| Therapeutic Area | Skill | Key Features |
|------------------|-------|--------------|
| **Oncology** | [oncology.md](oncology.md) | RECIST 1.1, tumor response, survival endpoints |
| **Cardiovascular** | [cardiovascular.md](cardiovascular.md) | MACE, heart failure, CV biomarkers |
| **CNS/Neurology** | [cns.md](cns.md) | Cognitive scales, imaging endpoints |
| **Cell & Gene Therapy** | [cgt.md](cgt.md) | Long-term follow-up, gene expression |

## How to Use

Therapeutic area skills work in combination with phase cohort skills:

```
"Generate a Phase III oncology trial"
→ Uses phase3-pivotal.md + therapeutic-areas/oncology.md

"Create a cardiovascular outcomes trial"  
→ Uses clinical-trials-domain.md + therapeutic-areas/cardiovascular.md
```

## Shared Concepts

All therapeutic area skills include:

- **Indication-specific endpoints** - Primary and secondary measures
- **Assessment schedules** - Visit timing and procedures
- **Safety considerations** - Expected adverse events
- **Biomarkers** - Diagnostic and predictive markers
- **Treatment patterns** - Standard of care context

## Cross-References

- [Clinical Trials Domain](../clinical-trials-domain.md) - Core trial concepts
- [Phase 3 Pivotal](../phase3-pivotal.md) - Pivotal trial cohorts
- [Recruitment & Enrollment](../recruitment-enrollment.md) - I/E criteria patterns
