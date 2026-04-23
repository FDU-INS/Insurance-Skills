# Templates

Pre-built profiles and journeys for common healthcare cohorts.

## Overview

Templates provide ready-to-use specifications that can be customized as needed. They encode best practices for realistic data generation across different populations and care patterns.

## Template Categories

| Category | Description | Location |
|----------|-------------|----------|
| **Profiles** | Population specifications | [profiles/](profiles/) |
| **Journeys** | Temporal event sequences | [journeys/](journeys/) |

## Available Profile Templates

| Template | Population | Key Characteristics |
|----------|------------|---------------------|
| [medicare-diabetic](profiles/medicare-diabetic.md) | Medicare T2DM | Age 65+, diabetes with comorbidities |
| [commercial-healthy](profiles/commercial-healthy.md) | Employer/Commercial | Working age, low chronic burden |
| [medicaid-pediatric](profiles/medicaid-pediatric.md) | Medicaid children | Age 0-17, SDOH factors |
| [commercial-maternity](profiles/commercial-maternity.md) | Pregnancy | Prenatal through postpartum |
| [medicare-advantage-complex](profiles/medicare-advantage-complex.md) | MA high-risk | Multiple chronic conditions |

## Available Journey Templates

| Template | Duration | Use Case |
|----------|----------|----------|
| [diabetic-first-year](journeys/diabetic-first-year.md) | 12 months | New T2DM diagnosis |
| [surgical-episode](journeys/surgical-episode.md) | 3 months | Elective surgery |
| [new-member-onboarding](journeys/new-member-onboarding.md) | 90 days | Plan enrollment |
| [hf-exacerbation](journeys/hf-exacerbation.md) | 30 days | Heart failure acute episode |
| [oncology-treatment-cycle](journeys/oncology-treatment-cycle.md) | 6 months | Cancer treatment |

## Using Templates

### Basic Usage
```
Use the Medicare diabetic template for 100 patients
```

### With Customization
```
Use the Medicare diabetic template but:
- Restrict to Texas
- Increase HTN prevalence to 85%
- Add the diabetic first-year journey
```

### Template + Journey Combination
```
Use the commercial healthy template with the new member onboarding journey
```

## Template Structure

All templates follow a consistent structure:

```yaml
template:
  id: unique-identifier
  name: Human-readable name
  version: "1.0"
  category: payer | clinical | trial
  tags: [searchable, tags]

profile/journey:
  # Full specification following ProfileSpec or JourneySpec schema
  
customizable:
  # List of fields that are commonly customized
```

## Creating Custom Templates

1. Start with the closest existing template
2. Use Profile Builder or Journey Builder to customize
3. Save the specification as a new template file
4. Add to the appropriate README index

## Related Categories

- [Builders](../builders/) - Create custom specifications
- [Executors](../executors/) - Execute templates

---

*Part of the HealthSim Generative Framework*
