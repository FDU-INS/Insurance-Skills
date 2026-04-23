# Pediatrics Cohorts

Cohort templates for generating pediatric patient data across common childhood conditions.

## Overview

These cohorts model realistic pediatric patient journeys with age-appropriate clinical presentations, dosing, and management protocols. All cohorts follow AAP (American Academy of Pediatrics) and NHLBI guidelines.

## Available Cohorts

| Cohort | Description | Key Features |
|----------|-------------|--------------|
| [childhood-asthma.md](childhood-asthma.md) | Pediatric asthma across severity levels | NHLBI step therapy, spirometry, action plans |
| [acute-otitis-media.md](acute-otitis-media.md) | Ear infections (AOM, OME) | AAP watchful waiting, antibiotic selection |

## Common Parameters

All pediatric cohorts support:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 2-12 | Patient age in years |
| age_months | int | null | For infants, age in months |
| weight_percentile | int | 50 | Weight percentile for dosing |

## Pediatric Considerations

### Age-Based Dosing
- All medication doses are weight-based (mg/kg)
- Formulations are pediatric-appropriate (liquids, chewables)
- Maximum adult doses are respected

### Developmental Context
- Vital signs normalized for age (higher HR, RR in young children)
- Developmental milestones considered
- Caregiver documentation included

### Safety Features
- Weight-based dose calculations included
- Age-appropriate formulation selection
- Contraindication checking (e.g., aspirin in children)

## Cross-References

### Related PatientSim Cohorts
- [../maternal-health.md](../maternal-health.md) - Neonatal transition
- [../sepsis-acute-care.md](../sepsis-acute-care.md) - Pediatric sepsis considerations

### MemberSim Integration
- [../../membersim/professional-claims.md](../../membersim/professional-claims.md) - Pediatric E&M coding

### RxMemberSim Integration
- [../../rxmembersim/retail-pharmacy.md](../../rxmembersim/retail-pharmacy.md) - Pediatric formulations
