# Hello-HealthSim: Getting Started Tutorial

Welcome to HealthSim! This tutorial walks you through the basics of generating healthcare data using the Generative Framework.

## Prerequisites

```bash
# Ensure you're in the healthsim-workspace directory
cd ~/Developer/projects/healthsim-workspace

# Install the core package (if not already)
pip install -e packages/core
```

---

## Tutorial 1: Your First Profile

Let's generate 5 simple patients.

### Step 1: Import the Framework

```python
from healthsim.generation import (
    ProfileExecutor,
    NormalDistribution,
    CategoricalDistribution,
)
```

### Step 2: Define a Simple Profile

```python
# Simple profile specification
profile_spec = {
    "generation": {
        "count": 5,
        "seed": 42,  # For reproducibility
        "products": ["patientsim"]
    },
    "demographics": {
        "age": {
            "type": "normal",
            "mean": 45,
            "std_dev": 15,
            "min": 18,
            "max": 85
        },
        "gender": {
            "type": "categorical",
            "weights": {"M": 0.49, "F": 0.51}
        }
    }
}
```

### Step 3: Execute

```python
executor = ProfileExecutor(master_seed=42)
result = executor.execute(profile_spec)

# Print generated patients
for entity in result.entities:
    print(f"Patient {entity.entity_id}:")
    print(f"  Age: {entity.attributes['age']}")
    print(f"  Gender: {entity.attributes['gender']}")
    print()
```

**Expected Output:**
```
Patient entity_0:
  Age: 52
  Gender: F

Patient entity_1:
  Age: 38
  Gender: M

Patient entity_2:
  Age: 61
  Gender: F
...
```

### Key Concepts

1. **Seed** - Using the same seed (42) always produces the same patients
2. **Distribution** - Normal distribution for continuous values, Categorical for choices
3. **Bounds** - min/max prevent unrealistic ages

---

## Tutorial 2: Adding Clinical Data

Let's add diagnoses and medications to our patients.

```python
# Enhanced profile with clinical data
clinical_profile = {
    "generation": {
        "count": 10,
        "seed": 42
    },
    "demographics": {
        "age": {"type": "normal", "mean": 65, "std_dev": 10, "min": 50, "max": 90},
        "gender": {"type": "categorical", "weights": {"M": 0.48, "F": 0.52}}
    },
    "clinical": {
        "conditions": [
            {
                "code": "E11.9",
                "description": "Type 2 diabetes",
                "prevalence": 0.80  # 80% will have this
            },
            {
                "code": "I10",
                "description": "Essential hypertension",
                "prevalence": 0.70
            },
            {
                "code": "E78.5",
                "description": "Hyperlipidemia",
                "prevalence": 0.60
            }
        ],
        "labs": {
            "a1c": {"type": "normal", "mean": 7.5, "std_dev": 1.2, "min": 5.0, "max": 14.0}
        }
    }
}

# Execute
result = executor.execute(clinical_profile)

# Show results
for entity in result.entities[:3]:  # First 3
    print(f"Patient {entity.entity_id}:")
    print(f"  Age: {entity.attributes['age']}, Gender: {entity.attributes['gender']}")
    print(f"  A1C: {entity.attributes.get('a1c', 'N/A')}")
    print(f"  Conditions: {entity.attributes.get('conditions', [])}")
    print()
```

---

## Tutorial 3: Your First Journey

Journeys define events over time. Let's create a simple diabetes care journey.

```python
from datetime import date
from healthsim.generation import (
    JourneyEngine,
    create_simple_journey,
)

# Define journey
diabetes_journey = create_simple_journey(
    journey_id="diabetes-intro",
    name="Diabetes Introduction",
    events=[
        {
            "event_id": "diagnosis",
            "name": "Initial Diagnosis",
            "event_type": "diagnosis",
            "delay": {"days": 0},
            "parameters": {"icd10": "E11.9"}
        },
        {
            "event_id": "first_a1c",
            "name": "First A1C Test",
            "event_type": "lab_order",
            "delay": {"days": 0, "days_min": 0, "days_max": 7, "distribution": "uniform"},
            "depends_on": "diagnosis"
        },
        {
            "event_id": "metformin",
            "name": "Start Metformin",
            "event_type": "medication_order",
            "delay": {"days": 3},
            "depends_on": "diagnosis",
            "parameters": {"rxnorm": "860975", "drug": "Metformin 500mg"}
        },
        {
            "event_id": "followup",
            "name": "3-Month Follow-up",
            "event_type": "encounter",
            "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
            "depends_on": "diagnosis"
        }
    ]
)

# Create engine and patient
engine = JourneyEngine(seed=42)
patient = {"patient_id": "P001", "name": "Jane Smith", "age": 55}

# Generate timeline starting Jan 1, 2025
timeline = engine.create_timeline(
    entity=patient,
    entity_type="patient",
    journey=diabetes_journey,
    start_date=date(2025, 1, 1)
)

# View the scheduled events
print("Timeline for Jane Smith:")
print("-" * 50)
for event in timeline.events:
    print(f"  {event.scheduled_date}: {event.event_name}")
    print(f"    Type: {event.event_type}")
```

**Expected Output:**
```
Timeline for Jane Smith:
--------------------------------------------------
  2025-01-01: Initial Diagnosis
    Type: diagnosis
  2025-01-04: Start Metformin
    Type: medication_order
  2025-01-05: First A1C Test
    Type: lab_order
  2025-03-28: 3-Month Follow-up
    Type: encounter
```

---

## Tutorial 4: Using Reference Data

Use real-world demographics from CDC data.

```python
import duckdb
from healthsim.generation import (
    ReferenceProfileResolver,
    create_hybrid_profile,
)

# Connect to reference database
conn = duckdb.connect("healthsim.duckdb", read_only=True)

# Look up Harris County, Texas
resolver = ReferenceProfileResolver(conn)
harris = resolver.resolve_county("48201")

print(f"Harris County, TX Demographics:")
print(f"  Population: {harris.population:,}")
print(f"  Diabetes: {harris.pct_diabetes}%")
print(f"  Obesity: {harris.pct_obesity}%")
print(f"  Hypertension: {harris.pct_hypertension}%")

# Create a profile spec from reference data
spec = resolver.to_profile_spec(harris)
print(f"\nGenerated profile has {len(spec.demographics.conditions)} conditions")

# You can override specific values
spec.demographics.age = {"type": "normal", "mean": 72, "std_dev": 8}  # Medicare age
```

---

## Tutorial 5: Cross-Product Generation

Generate correlated data across PatientSim and MemberSim.

```python
from healthsim.generation import (
    CrossProductCoordinator,
    JourneyEngine,
    get_journey_template,
)
from datetime import date

# Create coordinator
coordinator = CrossProductCoordinator()

# Create a linked entity (same person in both systems)
linked = coordinator.create_linked_entity(
    core_id="OSWALD001",
    product_ids={
        "patient_id": "P-OSWALD-001",
        "member_id": "M-OSWALD-001"
    }
)

print(f"Created linked entity: {linked.core_id}")
print(f"  Patient ID: {linked.patient_id}")
print(f"  Member ID: {linked.member_id}")

# The coordinator has default healthcare triggers:
# - Patient diagnosis → Member claim
# - Medication order → Pharmacy claim
# These ensure data consistency across products
```

---

## Next Steps

1. **Explore Templates**: Check `skills/generation/templates/` for pre-built profiles and journeys
2. **Read the Guide**: See `docs/guides/generative-framework-guide.md` for detailed documentation
3. **Try the CLI**: Use `healthsim generate` commands (coming soon)
4. **Build Custom Journeys**: Create your own event sequences for specific use cases

---

## Quick Reference

### Distribution Types

| Type | Use For | Example |
|------|---------|---------|
| `normal` | Age, lab values | `{"type": "normal", "mean": 45, "std_dev": 10}` |
| `categorical` | Gender, status | `{"type": "categorical", "weights": {"M": 0.5, "F": 0.5}}` |
| `uniform` | Random in range | `{"type": "uniform", "min": 1, "max": 10}` |
| `lognormal` | Costs, durations | `{"type": "lognormal", "mean": 1000, "sigma": 0.5}` |

### Event Types

| Product | Common Events |
|---------|---------------|
| PatientSim | diagnosis, encounter, lab_order, lab_result, medication_order |
| MemberSim | new_enrollment, claim_professional, claim_pharmacy, gap_identified |
| RxMemberSim | new_rx, fill, refill, therapy_start |

---

*Happy generating! 🏥*
