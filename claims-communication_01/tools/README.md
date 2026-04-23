# HealthSim Tools

Command-line utilities for working with HealthSim DuckDB.

## Prerequisites

```bash
pip install duckdb
```

## Scenario Loader

Loads JSON scenario files into DuckDB canonical tables.

### Usage

```bash
python scenario_loader.py <scenario_path> [--db <duckdb_path>] [--name <override_name>]
```

### Example

```bash
# Load Bob Thompson scenario
python scenario_loader.py ../scenarios/saved/bob-thompson-er-visit

# Load with custom database path
python scenario_loader.py ../scenarios/saved/bob-thompson-er-visit --db ../healthsim.duckdb
```

### Supported JSON Structures

The loader handles various JSON formats:

```json
// Single entity
{"person": {"person_id": "...", ...}}

// Multiple entities
{"persons": [{"person_id": "..."}, {"person_id": "..."}]}

// Mixed
{
  "person": {...},
  "member": {...},
  "encounters": [{...}, {...}]
}
```

## Scenario Saver

Exports scenarios from DuckDB to JSON files.

### Usage

```bash
python scenario_saver.py <scenario_name> [--output <output_path>] [--db <duckdb_path>] [--format <format>]
```

### Options

- `--output, -o`: Output directory (default: `./exports`)
- `--db`: DuckDB database path (default: `healthsim.duckdb`)
- `--format`: Export format
  - `by_product`: Separate JSON files per product (default)
  - `single`: Single JSON file with all data

### Example

```bash
# Export to separate files per product
python scenario_saver.py "bob-thompson-er-visit"

# Export to single file
python scenario_saver.py "bob-thompson-er-visit" --format single

# Custom output path
python scenario_saver.py "bob-thompson-er-visit" -o ../scenarios/exported
```

### Output Structure (by_product format)

```
exports/bob-thompson-er-visit/
├── scenario.json       # Scenario metadata
├── core.json          # persons, providers, facilities
├── patientsim.json    # patients, encounters, diagnoses, etc.
├── membersim.json     # members, claims, claim_lines, etc.
├── rxmembersim.json   # rx_members, prescriptions, pharmacy_claims
├── trialsim.json      # studies, subjects, adverse_events, etc.
├── populationsim.json # geographic_entities, population_profiles
├── networksim.json    # networks, network_providers
└── README.md          # Summary
```

## Entity Type Mapping

| Entity Type | Table | Primary Key |
|-------------|-------|-------------|
| **Core** | | |
| person | persons | person_id |
| provider | providers | provider_id |
| facility | facilities | facility_id |
| **PatientSim** | | |
| patient | patients | patient_id |
| encounter | encounters | encounter_id |
| diagnosis | diagnoses | diagnosis_id |
| procedure | procedures | procedure_id |
| lab_result | lab_results | lab_result_id |
| medication | medications | medication_id |
| allergy | allergies | allergy_id |
| vital | vitals | vital_id |
| **MemberSim** | | |
| member | members | member_id |
| accumulator | accumulators | accumulator_id |
| claim | claims | claim_id |
| claim_line | claim_lines | claim_line_id |
| authorization | authorizations | authorization_id |
| **RxMemberSim** | | |
| rx_member | rx_members | rx_member_id |
| prescription | prescriptions | prescription_id |
| pharmacy_claim | pharmacy_claims | pharmacy_claim_id |
| dur_alert | dur_alerts | dur_alert_id |
| pharmacy | pharmacies | pharmacy_id |
| **TrialSim** | | |
| study | studies | study_id |
| site | sites | site_id |
| treatment_arm | treatment_arms | arm_id |
| subject | subjects | subject_id |
| adverse_event | adverse_events | ae_id |
| visit_schedule | visit_schedule | visit_schedule_id |
| actual_visit | actual_visits | actual_visit_id |
| disposition_event | disposition_events | disposition_id |
| **PopulationSim** | | |
| geographic_entity | geographic_entities | geo_id |
| population_profile | population_profiles | profile_id |
| health_indicator | health_indicators | indicator_id |
| sdoh_index | sdoh_indices | sdoh_id |
| cohort_specification | cohort_specifications | cohort_spec_id |
| **NetworkSim** | | |
| network | networks | network_id |
| network_provider | network_providers | network_provider_id |
| network_facility | network_facilities | network_facility_id |
| provider_specialty | provider_specialties | specialty_id |
