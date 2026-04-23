# SQL Export Format

## Trigger Phrases

- SQL
- INSERT statements
- SQL INSERT
- database insert
- as SQL
- load to database
- SQL script
- database export

## Overview

This skill exports HealthSim entities as SQL INSERT statements for direct database loading. Supports multiple SQL dialects and batch operations.

## Export Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| dialect | postgresql, mysql, sqlserver, oracle, sqlite | postgresql | SQL dialect |
| batch_size | 1-1000 | 100 | Rows per INSERT (multi-row) |
| include_schema | true, false | false | Include CREATE TABLE |
| transaction | true, false | true | Wrap in transaction |
| on_conflict | ignore, update, error | error | Conflict handling |
| null_style | NULL, DEFAULT | NULL | How to handle nulls |

## Table Schemas

### patients

```sql
CREATE TABLE patients (
    mrn VARCHAR(20) PRIMARY KEY,
    given_name VARCHAR(50) NOT NULL,
    family_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    birth_date DATE NOT NULL,
    gender CHAR(1) NOT NULL,
    ssn VARCHAR(11),
    street_address VARCHAR(100),
    city VARCHAR(50),
    state CHAR(2),
    postal_code VARCHAR(10),
    country VARCHAR(3) DEFAULT 'USA',
    phone_home VARCHAR(20),
    phone_work VARCHAR(20),
    email VARCHAR(100),
    language_code VARCHAR(3),
    marital_status CHAR(1),
    race_code VARCHAR(10),
    ethnicity_code VARCHAR(10),
    deceased BOOLEAN DEFAULT FALSE,
    deceased_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### encounters

```sql
CREATE TABLE encounters (
    encounter_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_class CHAR(3) NOT NULL,
    encounter_type VARCHAR(50),
    status VARCHAR(20) NOT NULL,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP,
    facility_code VARCHAR(20),
    facility_name VARCHAR(100),
    location_unit VARCHAR(20),
    location_room VARCHAR(10),
    location_bed VARCHAR(5),
    attending_npi VARCHAR(10),
    attending_name VARCHAR(100),
    admission_source VARCHAR(5),
    discharge_disposition VARCHAR(5),
    reason_code VARCHAR(10),
    reason_description VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### diagnoses

```sql
CREATE TABLE diagnoses (
    diagnosis_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    code VARCHAR(10) NOT NULL,
    code_system VARCHAR(20) DEFAULT 'ICD-10-CM',
    description VARCHAR(200),
    diagnosis_type VARCHAR(20),
    onset_date DATE,
    abatement_date DATE,
    clinical_status VARCHAR(20),
    verification_status VARCHAR(20),
    severity VARCHAR(20),
    diagnosed_by_npi VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### procedures

```sql
CREATE TABLE procedures (
    procedure_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    code VARCHAR(10) NOT NULL,
    code_system VARCHAR(20) NOT NULL,
    description VARCHAR(200),
    performed_datetime TIMESTAMP,
    performer_npi VARCHAR(10),
    performer_name VARCHAR(100),
    body_site VARCHAR(50),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### medications

```sql
CREATE TABLE medications (
    medication_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    ndc VARCHAR(11),
    rxnorm_code VARCHAR(10),
    drug_name VARCHAR(200) NOT NULL,
    dose_value DECIMAL(10,2),
    dose_unit VARCHAR(20),
    route VARCHAR(20),
    frequency VARCHAR(50),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    prescriber_npi VARCHAR(10),
    prescriber_name VARCHAR(100),
    indication_code VARCHAR(10),
    refills_authorized INT,
    quantity_dispensed INT,
    days_supply INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### observations

```sql
CREATE TABLE observations (
    observation_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    code VARCHAR(20) NOT NULL,
    code_system VARCHAR(20) NOT NULL,
    description VARCHAR(200),
    value_numeric DECIMAL(12,4),
    value_string VARCHAR(500),
    value_code VARCHAR(20),
    unit VARCHAR(20),
    reference_low DECIMAL(10,2),
    reference_high DECIMAL(10,2),
    interpretation VARCHAR(5),
    effective_datetime TIMESTAMP,
    status VARCHAR(20),
    performer_npi VARCHAR(10),
    specimen_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### orders

```sql
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    patient_mrn VARCHAR(20) NOT NULL REFERENCES patients(mrn),
    encounter_id VARCHAR(20) REFERENCES encounters(encounter_id),
    order_type VARCHAR(20) NOT NULL,
    code VARCHAR(20),
    code_system VARCHAR(20),
    description VARCHAR(200),
    priority CHAR(1),
    status VARCHAR(20),
    ordered_datetime TIMESTAMP,
    scheduled_datetime TIMESTAMP,
    completed_datetime TIMESTAMP,
    ordering_provider_npi VARCHAR(10),
    ordering_provider_name VARCHAR(100),
    performer_npi VARCHAR(10),
    performer_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### claims

```sql
CREATE TABLE claims (
    claim_id VARCHAR(20) PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL,
    claim_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    service_from_date DATE NOT NULL,
    service_to_date DATE,
    facility_npi VARCHAR(10),
    facility_name VARCHAR(100),
    billing_provider_npi VARCHAR(10),
    rendering_provider_npi VARCHAR(10),
    principal_diagnosis VARCHAR(10),
    total_charge DECIMAL(12,2),
    total_allowed DECIMAL(12,2),
    total_paid DECIMAL(12,2),
    patient_responsibility DECIMAL(12,2),
    adjudicated_date DATE,
    auth_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### claim_lines

```sql
CREATE TABLE claim_lines (
    claim_id VARCHAR(20) NOT NULL REFERENCES claims(claim_id),
    line_number INT NOT NULL,
    procedure_code VARCHAR(10),
    procedure_modifier VARCHAR(10),
    revenue_code VARCHAR(4),
    ndc VARCHAR(11),
    description VARCHAR(200),
    service_date DATE,
    quantity DECIMAL(10,3),
    charge_amount DECIMAL(12,2),
    allowed_amount DECIMAL(12,2),
    paid_amount DECIMAL(12,2),
    deductible DECIMAL(10,2),
    copay DECIMAL(10,2),
    coinsurance DECIMAL(10,2),
    diagnosis_pointer VARCHAR(10),
    place_of_service VARCHAR(2),
    PRIMARY KEY (claim_id, line_number)
);
```

### groups

```sql
CREATE TABLE groups (
    group_id VARCHAR(20) PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL,
    tax_id VARCHAR(12),
    street_address VARCHAR(100),
    city VARCHAR(50),
    state CHAR(2),
    postal_code VARCHAR(10),
    effective_date DATE NOT NULL,
    termination_date DATE,
    contact_name VARCHAR(100),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### plans

```sql
CREATE TABLE plans (
    plan_code VARCHAR(20) PRIMARY KEY,
    plan_name VARCHAR(100) NOT NULL,
    plan_type VARCHAR(10) NOT NULL,
    network_requirement VARCHAR(30),
    individual_deductible DECIMAL(10,2),
    family_deductible DECIMAL(10,2),
    individual_oop_max DECIMAL(10,2),
    family_oop_max DECIMAL(10,2),
    pcp_copay DECIMAL(10,2),
    specialist_copay DECIMAL(10,2),
    er_copay DECIMAL(10,2),
    inpatient_copay DECIMAL(10,2),
    coinsurance INT,
    pcp_required BOOLEAN DEFAULT FALSE,
    referral_required BOOLEAN DEFAULT FALSE,
    hsa_eligible BOOLEAN DEFAULT FALSE,
    effective_date DATE,
    termination_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### plan_service_benefits

Detailed benefit structure by service type:

```sql
CREATE TABLE plan_service_benefits (
    plan_code VARCHAR(20) NOT NULL REFERENCES plans(plan_code),
    service_type VARCHAR(30) NOT NULL,
    network_tier VARCHAR(20) NOT NULL,
    cost_sharing_type VARCHAR(20) NOT NULL,
    cost_sharing_amount DECIMAL(10,2),
    deductible_applies BOOLEAN DEFAULT TRUE,
    annual_limit INT,
    prior_auth_required BOOLEAN DEFAULT FALSE,
    notes VARCHAR(200),
    PRIMARY KEY (plan_code, service_type, network_tier)
);

-- Service types: pcp_visit, specialist_visit, urgent_care, emergency_room,
--                inpatient, outpatient_surgery, lab_work, xray, advanced_imaging,
--                mental_health_outpatient, mental_health_inpatient, physical_therapy,
--                preventive, telehealth, ambulance, skilled_nursing, home_health
-- Cost sharing types: copay, coinsurance, covered_100
-- Network tiers: in_network, out_of_network, tier_1, tier_2, tier_3
```

### pharmacy_benefits

Pharmacy tier structure for each plan:

```sql
CREATE TABLE pharmacy_benefits (
    plan_code VARCHAR(20) NOT NULL REFERENCES plans(plan_code),
    tier INT NOT NULL,
    tier_name VARCHAR(50) NOT NULL,
    tier_description VARCHAR(200),
    retail_30_copay DECIMAL(10,2),
    retail_90_copay DECIMAL(10,2),
    mail_90_copay DECIMAL(10,2),
    specialty_coinsurance INT,
    specialty_max DECIMAL(10,2),
    deductible_applies BOOLEAN DEFAULT FALSE,
    quantity_limit_days INT,
    prior_auth_common BOOLEAN DEFAULT FALSE,
    step_therapy_common BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (plan_code, tier)
);
```

### plan_accumulators

Member-level accumulator tracking:

```sql
CREATE TABLE plan_accumulators (
    accumulator_id VARCHAR(20) PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL REFERENCES members(member_id),
    plan_code VARCHAR(20) NOT NULL REFERENCES plans(plan_code),
    plan_year INT NOT NULL,
    accumulator_type VARCHAR(20) NOT NULL,
    individual_applied DECIMAL(10,2) DEFAULT 0,
    individual_limit DECIMAL(10,2),
    family_applied DECIMAL(10,2) DEFAULT 0,
    family_limit DECIMAL(10,2),
    as_of_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (member_id, plan_code, plan_year, accumulator_type)
);

-- Accumulator types: deductible, oop_max, rx_deductible, rx_oop_max
```

### members

```sql
CREATE TABLE members (
    member_id VARCHAR(20) PRIMARY KEY,
    subscriber_id VARCHAR(20) NOT NULL,
    relationship_code CHAR(2) NOT NULL,
    group_id VARCHAR(20) REFERENCES groups(group_id),
    plan_code VARCHAR(20) REFERENCES plans(plan_code),
    given_name VARCHAR(50) NOT NULL,
    family_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    birth_date DATE NOT NULL,
    gender CHAR(1) NOT NULL,
    ssn VARCHAR(11),
    street_address VARCHAR(100),
    city VARCHAR(50),
    state CHAR(2),
    postal_code VARCHAR(10),
    email VARCHAR(100),
    phone VARCHAR(20),
    coverage_start DATE NOT NULL,
    coverage_end DATE,
    coverage_tier VARCHAR(5),
    pcp_npi VARCHAR(10),
    pcp_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### enrollments

```sql
CREATE TABLE enrollments (
    enrollment_id VARCHAR(20) PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL REFERENCES members(member_id),
    transaction_type VARCHAR(20) NOT NULL,
    transaction_date DATE NOT NULL,
    effective_date DATE NOT NULL,
    enrollment_reason VARCHAR(30),
    plan_code VARCHAR(20) REFERENCES plans(plan_code),
    coverage_tier VARCHAR(5),
    premium_amount DECIMAL(10,2),
    employer_contribution DECIMAL(10,2),
    employee_contribution DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    processed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### eligibility_inquiries

```sql
CREATE TABLE eligibility_inquiries (
    trace_number VARCHAR(30) PRIMARY KEY,
    inquiry_date DATE NOT NULL,
    member_id VARCHAR(20),
    member_name VARCHAR(100),
    birth_date DATE,
    provider_npi VARCHAR(10),
    provider_name VARCHAR(100),
    service_type VARCHAR(5),
    service_date DATE,
    request_timestamp TIMESTAMP,
    response_timestamp TIMESTAMP,
    response_status VARCHAR(20),
    eligibility_status VARCHAR(20),
    plan_code VARCHAR(20),
    coverage_start DATE,
    coverage_end DATE,
    deductible_remaining DECIMAL(10,2),
    oop_remaining DECIMAL(10,2),
    error_code VARCHAR(10),
    error_message VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### rx_members

```sql
CREATE TABLE rx_members (
    member_id VARCHAR(20) PRIMARY KEY,
    cardholder_id VARCHAR(20) NOT NULL,
    bin CHAR(6) NOT NULL,
    pcn VARCHAR(20) NOT NULL,
    group_number VARCHAR(20) NOT NULL,
    person_code CHAR(2) NOT NULL,
    given_name VARCHAR(50) NOT NULL,
    family_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    gender CHAR(1) NOT NULL,
    rx_plan_code VARCHAR(20) NOT NULL REFERENCES rx_plans(rx_plan_code),
    coverage_start DATE NOT NULL,
    coverage_end DATE,
    relationship_code CHAR(2) NOT NULL,
    subscriber_id VARCHAR(20),
    mail_order_eligible BOOLEAN DEFAULT TRUE,
    specialty_eligible BOOLEAN DEFAULT TRUE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rx_members_cardholder ON rx_members(cardholder_id, bin, pcn);
```

### rx_plans

```sql
CREATE TABLE rx_plans (
    rx_plan_code VARCHAR(20) PRIMARY KEY,
    plan_name VARCHAR(100) NOT NULL,
    plan_type VARCHAR(20) NOT NULL,
    formulary_id VARCHAR(20),
    rx_deductible DECIMAL(10,2) DEFAULT 0,
    rx_oop_max DECIMAL(10,2),
    combined_with_medical_oop BOOLEAN DEFAULT FALSE,
    tier1_retail_30 DECIMAL(10,2),
    tier1_mail_90 DECIMAL(10,2),
    tier2_retail_30 DECIMAL(10,2),
    tier2_mail_90 DECIMAL(10,2),
    tier3_retail_30 DECIMAL(10,2),
    tier3_mail_90 DECIMAL(10,2),
    tier4_retail_30 DECIMAL(10,2),
    tier4_mail_90 DECIMAL(10,2),
    specialty_coinsurance INT,
    specialty_max_per_fill DECIMAL(10,2),
    part_d_deductible DECIMAL(10,2),
    part_d_icl DECIMAL(10,2),
    part_d_catastrophic_threshold DECIMAL(10,2),
    effective_date DATE,
    termination_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Plan types: commercial, medicare_d, medicaid, discount, hdhp
```

### rx_accumulators

```sql
CREATE TABLE rx_accumulators (
    accumulator_id VARCHAR(20) PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL REFERENCES rx_members(member_id),
    rx_plan_code VARCHAR(20) NOT NULL REFERENCES rx_plans(rx_plan_code),
    plan_year INT NOT NULL,
    rx_deductible_applied DECIMAL(10,2) DEFAULT 0,
    rx_deductible_limit DECIMAL(10,2),
    rx_deductible_met BOOLEAN DEFAULT FALSE,
    rx_deductible_met_date DATE,
    rx_oop_applied DECIMAL(10,2) DEFAULT 0,
    rx_oop_limit DECIMAL(10,2),
    rx_oop_met BOOLEAN DEFAULT FALSE,
    rx_oop_met_date DATE,
    specialty_ytd DECIMAL(10,2) DEFAULT 0,
    daw_penalty_ytd DECIMAL(10,2) DEFAULT 0,
    part_d_phase VARCHAR(20),
    troop_applied DECIMAL(10,2),
    gross_drug_cost_ytd DECIMAL(12,2),
    as_of_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (member_id, rx_plan_code, plan_year)
);

-- Part D phases: deductible, icl, coverage_gap, catastrophic
```

### pharmacy_prior_auth

```sql
CREATE TABLE pharmacy_prior_auth (
    pa_id VARCHAR(30) PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL REFERENCES rx_members(member_id),
    ndc VARCHAR(11) NOT NULL,
    drug_name VARCHAR(200),
    pa_type VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL,
    urgency VARCHAR(20) DEFAULT 'standard',
    request_date DATE NOT NULL,
    request_datetime TIMESTAMP,
    decision_date DATE,
    decision_datetime TIMESTAMP,
    effective_date DATE,
    expiration_date DATE,
    override_code VARCHAR(20),
    approved_quantity INT,
    approved_days_supply INT,
    approved_fills INT,
    denial_reason_code VARCHAR(50),
    denial_reason TEXT,
    prescriber_npi VARCHAR(10),
    prescriber_name VARCHAR(100),
    reviewer_name VARCHAR(100),
    reviewer_credentials VARCHAR(50),
    clinical_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pharmacy_pa_member ON pharmacy_prior_auth(member_id);
CREATE INDEX idx_pharmacy_pa_status ON pharmacy_prior_auth(status);

-- PA types: formulary_exception, step_therapy_override, quantity_limit, age_edit, clinical_pa, specialty
-- Status: pending, approved, denied, cancelled, expired
-- Urgency: standard, urgent, expedited
```

### dur_alerts

```sql
CREATE TABLE dur_alerts (
    alert_id VARCHAR(30) PRIMARY KEY,
    claim_id VARCHAR(30) NOT NULL,
    member_id VARCHAR(20) NOT NULL,
    ndc VARCHAR(11) NOT NULL,
    drug_name VARCHAR(200),
    dur_code VARCHAR(5) NOT NULL,
    dur_type VARCHAR(30) NOT NULL,
    clinical_significance INT NOT NULL,
    interacting_ndc VARCHAR(11),
    interacting_drug VARCHAR(200),
    severity VARCHAR(20),
    pharmacist_message TEXT,
    recommendation TEXT,
    override_code VARCHAR(5),
    outcome_code VARCHAR(5),
    alert_datetime TIMESTAMP NOT NULL,
    resolved_datetime TIMESTAMP,
    resolved_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dur_alerts_claim ON dur_alerts(claim_id);
CREATE INDEX idx_dur_alerts_member ON dur_alerts(member_id);

-- DUR codes: DD (drug-drug), ER (early refill), TD (therapeutic dup), HD (high dose),
--            LD (low dose), DA (drug-age), DG (drug-gender), DC (drug-disease), PA (prior auth)
-- Clinical significance: 1=major, 2=moderate, 3=minor, 4=undetermined
```

### copay_assistance

```sql
CREATE TABLE copay_assistance (
    program_id VARCHAR(30) PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL REFERENCES rx_members(member_id),
    ndc VARCHAR(11) NOT NULL,
    drug_name VARCHAR(200),
    program_type VARCHAR(30) NOT NULL,
    program_name VARCHAR(100),
    program_bin CHAR(6),
    program_pcn VARCHAR(20),
    program_group VARCHAR(20),
    program_start DATE NOT NULL,
    program_end DATE,
    annual_max_benefit DECIMAL(12,2),
    benefit_used_ytd DECIMAL(12,2) DEFAULT 0,
    benefit_remaining DECIMAL(12,2),
    max_per_fill DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'active',
    enrollment_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_copay_assistance_member ON copay_assistance(member_id);

-- Program types: manufacturer_copay, patient_assistance, foundation, bridge, free_trial, loyalty
-- Status: active, pending, expired, exhausted
```

## Example INSERT Statements

### Single Patient Insert

```sql
INSERT INTO patients (
    mrn, given_name, family_name, middle_name, birth_date, gender,
    ssn, street_address, city, state, postal_code, country,
    phone_home, email, language_code, marital_status
) VALUES (
    'MRN00000001', 'John', 'Smith', 'Michael', '1970-03-15', 'M',
    '123-45-6789', '123 Main St', 'Springfield', 'IL', '62701', 'USA',
    '555-123-4567', 'john.smith@email.com', 'ENG', 'M'
);
```

### Multi-Row Insert (PostgreSQL/MySQL)

```sql
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender, city, state) VALUES
    ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M', 'Springfield', 'IL'),
    ('MRN00000002', 'Maria', 'Garcia', '1955-10-20', 'F', 'Springfield', 'IL'),
    ('MRN00000003', 'Eleanor', 'Thompson', '1950-08-12', 'F', 'Springfield', 'IL'),
    ('MRN00000004', 'James', 'Wilson', '1965-07-10', 'M', 'Springfield', 'IL'),
    ('MRN00000005', 'Carlos', 'Martinez', '1968-02-20', 'M', 'Springfield', 'IL');
```

### Complete Patient with Related Data

```sql
BEGIN;

-- Insert patient
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender, city, state)
VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M', 'Springfield', 'IL');

-- Insert encounter
INSERT INTO encounters (encounter_id, patient_mrn, encounter_class, encounter_type, status, period_start, period_end, attending_npi, attending_name)
VALUES ('ENC0000000001', 'MRN00000001', 'I', 'inpatient', 'finished', '2025-01-10 14:00:00', '2025-01-15 10:00:00', '1234567890', 'Dr. Robert Johnson');

-- Insert diagnoses
INSERT INTO diagnoses (diagnosis_id, patient_mrn, encounter_id, code, code_system, description, diagnosis_type, clinical_status)
VALUES
    ('DX0000000001', 'MRN00000001', 'ENC0000000001', 'I50.23', 'ICD-10-CM', 'Acute on chronic systolic heart failure', 'principal', 'active'),
    ('DX0000000002', 'MRN00000001', 'ENC0000000001', 'I10', 'ICD-10-CM', 'Essential hypertension', 'secondary', 'active'),
    ('DX0000000003', 'MRN00000001', 'ENC0000000001', 'E11.9', 'ICD-10-CM', 'Type 2 diabetes mellitus', 'secondary', 'active');

-- Insert medications
INSERT INTO medications (medication_id, patient_mrn, encounter_id, ndc, drug_name, dose_value, dose_unit, route, frequency, status, prescriber_npi)
VALUES
    ('MED0000000001', 'MRN00000001', 'ENC0000000001', '00093505601', 'Lisinopril 10mg Tab', 10, 'mg', 'oral', 'daily', 'active', '1234567890'),
    ('MED0000000002', 'MRN00000001', 'ENC0000000001', '00093085601', 'Metformin 500mg Tab', 500, 'mg', 'oral', 'BID', 'active', '1234567890');

-- Insert observations (labs)
INSERT INTO observations (observation_id, patient_mrn, encounter_id, code, code_system, description, value_numeric, unit, reference_low, reference_high, interpretation, status)
VALUES
    ('OBS0000000001', 'MRN00000001', 'ENC0000000001', '2345-7', 'LOINC', 'Glucose', 98, 'mg/dL', 70, 100, 'N', 'final'),
    ('OBS0000000002', 'MRN00000001', 'ENC0000000001', '2160-0', 'LOINC', 'Creatinine', 1.1, 'mg/dL', 0.7, 1.3, 'N', 'final'),
    ('OBS0000000003', 'MRN00000001', 'ENC0000000001', '4548-4', 'LOINC', 'HbA1c', 7.8, '%', 4.0, 5.6, 'H', 'final');

COMMIT;
```

### Claims Insert

```sql
-- Insert claim
INSERT INTO claims (
    claim_id, member_id, claim_type, status, service_from_date, service_to_date,
    rendering_provider_npi, principal_diagnosis, total_charge, total_allowed,
    total_paid, patient_responsibility, adjudicated_date
) VALUES (
    'CLM20250115001', 'MEM001234', 'professional', 'paid', '2025-01-15', '2025-01-15',
    '1234567890', 'E11.9', 175.00, 150.00, 125.00, 25.00, '2025-01-16'
);

-- Insert claim lines
INSERT INTO claim_lines (
    claim_id, line_number, procedure_code, description, service_date,
    quantity, charge_amount, allowed_amount, paid_amount, deductible, copay,
    coinsurance, diagnosis_pointer, place_of_service
) VALUES (
    'CLM20250115001', 1, '99214', 'Office visit established', '2025-01-15',
    1, 175.00, 150.00, 125.00, 0.00, 25.00, 0.00, '1', '11'
);
```

### Enrollment Insert

```sql
BEGIN;

-- Insert group
INSERT INTO groups (group_id, group_name, tax_id, street_address, city, state, postal_code, effective_date, contact_name, contact_email)
VALUES ('GRP001234', 'Acme Corporation', '12-3456789', '100 Corporate Drive', 'Springfield', 'IL', '62701', '2020-01-01', 'Jane Smith', 'jane.smith@acme.com');

-- Insert plan
INSERT INTO plans (plan_code, plan_name, plan_type, network_requirement, individual_deductible, family_deductible, individual_oop_max, family_oop_max, pcp_copay, specialist_copay, coinsurance, pcp_required, referral_required)
VALUES ('PPO-GOLD', 'PPO Gold Plan', 'PPO', 'in_network_preferred', 500.00, 1000.00, 4000.00, 8000.00, 25.00, 50.00, 20, FALSE, FALSE);

-- Insert subscriber
INSERT INTO members (member_id, subscriber_id, relationship_code, group_id, plan_code, given_name, family_name, birth_date, gender, ssn, street_address, city, state, postal_code, email, phone, coverage_start, coverage_tier, status)
VALUES ('MEM001234567', 'MEM001234567', '18', 'GRP001234', 'PPO-GOLD', 'Michael', 'Johnson', '1985-03-15', 'M', '123-45-6789', '456 Oak Avenue', 'Springfield', 'IL', '62702', 'michael.johnson@email.com', '555-234-5678', '2025-02-01', 'FAM', 'active');

-- Insert spouse
INSERT INTO members (member_id, subscriber_id, relationship_code, group_id, plan_code, given_name, family_name, birth_date, gender, ssn, street_address, city, state, postal_code, coverage_start, coverage_tier, status)
VALUES ('MEM001234568', 'MEM001234567', '01', 'GRP001234', 'PPO-GOLD', 'Sarah', 'Johnson', '1987-07-22', 'F', '987-65-4321', '456 Oak Avenue', 'Springfield', 'IL', '62702', '2025-02-01', 'FAM', 'active');

-- Insert child
INSERT INTO members (member_id, subscriber_id, relationship_code, group_id, plan_code, given_name, family_name, birth_date, gender, ssn, street_address, city, state, postal_code, coverage_start, coverage_tier, status)
VALUES ('MEM001234569', 'MEM001234567', '19', 'GRP001234', 'PPO-GOLD', 'Emma', 'Johnson', '2015-11-10', 'F', '456-78-9012', '456 Oak Avenue', 'Springfield', 'IL', '62702', '2025-02-01', 'FAM', 'active');

-- Insert enrollment transactions
INSERT INTO enrollments (enrollment_id, member_id, transaction_type, transaction_date, effective_date, enrollment_reason, plan_code, coverage_tier, premium_amount, employer_contribution, employee_contribution, status)
VALUES
    ('ENR20250115001', 'MEM001234567', 'add', '2025-01-15', '2025-02-01', 'new_hire', 'PPO-GOLD', 'FAM', 850.00, 650.00, 200.00, 'active'),
    ('ENR20250115002', 'MEM001234568', 'add', '2025-01-15', '2025-02-01', 'new_hire', 'PPO-GOLD', 'FAM', 0.00, 0.00, 0.00, 'active'),
    ('ENR20250115003', 'MEM001234569', 'add', '2025-01-15', '2025-02-01', 'new_hire', 'PPO-GOLD', 'FAM', 0.00, 0.00, 0.00, 'active');

COMMIT;
```

### Plan Benefits Insert

```sql
BEGIN;

-- Insert plan service benefits for PPO-GOLD
INSERT INTO plan_service_benefits (plan_code, service_type, network_tier, cost_sharing_type, cost_sharing_amount, deductible_applies, prior_auth_required)
VALUES
    ('PPO-GOLD', 'pcp_visit', 'in_network', 'copay', 25.00, FALSE, FALSE),
    ('PPO-GOLD', 'pcp_visit', 'out_of_network', 'coinsurance', 40, TRUE, FALSE),
    ('PPO-GOLD', 'specialist_visit', 'in_network', 'copay', 50.00, FALSE, FALSE),
    ('PPO-GOLD', 'specialist_visit', 'out_of_network', 'coinsurance', 40, TRUE, FALSE),
    ('PPO-GOLD', 'urgent_care', 'in_network', 'copay', 75.00, FALSE, FALSE),
    ('PPO-GOLD', 'emergency_room', 'in_network', 'copay', 150.00, FALSE, FALSE),
    ('PPO-GOLD', 'inpatient', 'in_network', 'coinsurance', 20, TRUE, TRUE),
    ('PPO-GOLD', 'inpatient', 'out_of_network', 'coinsurance', 40, TRUE, TRUE),
    ('PPO-GOLD', 'outpatient_surgery', 'in_network', 'copay', 200.00, TRUE, TRUE),
    ('PPO-GOLD', 'advanced_imaging', 'in_network', 'coinsurance', 20, TRUE, TRUE),
    ('PPO-GOLD', 'lab_work', 'in_network', 'copay', 0.00, FALSE, FALSE),
    ('PPO-GOLD', 'preventive', 'in_network', 'covered_100', 0.00, FALSE, FALSE);

-- Insert pharmacy benefits for PPO-GOLD
INSERT INTO pharmacy_benefits (plan_code, tier, tier_name, retail_30_copay, retail_90_copay, mail_90_copay, specialty_coinsurance, specialty_max, deductible_applies)
VALUES
    ('PPO-GOLD', 1, 'Preferred Generic', 10.00, 25.00, 25.00, NULL, NULL, FALSE),
    ('PPO-GOLD', 2, 'Non-Preferred Generic', 25.00, 62.50, 62.50, NULL, NULL, FALSE),
    ('PPO-GOLD', 3, 'Preferred Brand', 50.00, 125.00, 125.00, NULL, NULL, FALSE),
    ('PPO-GOLD', 4, 'Non-Preferred Brand', 80.00, 200.00, 200.00, NULL, NULL, FALSE),
    ('PPO-GOLD', 5, 'Specialty', NULL, NULL, NULL, 25, 250.00, FALSE);

-- Insert plan accumulators for a member
INSERT INTO plan_accumulators (accumulator_id, member_id, plan_code, plan_year, accumulator_type, individual_applied, individual_limit, family_applied, family_limit, as_of_date)
VALUES
    ('ACC20250120001', 'MEM001234567', 'PPO-GOLD', 2025, 'deductible', 325.00, 500.00, 325.00, 1000.00, '2025-01-20'),
    ('ACC20250120002', 'MEM001234567', 'PPO-GOLD', 2025, 'oop_max', 350.00, 4000.00, 350.00, 8000.00, '2025-01-20');

COMMIT;
```

### Eligibility Inquiry Insert

```sql
INSERT INTO eligibility_inquiries (
    trace_number, inquiry_date, member_id, member_name, birth_date,
    provider_npi, provider_name, service_type, service_date,
    request_timestamp, response_timestamp, response_status, eligibility_status,
    plan_code, coverage_start, deductible_remaining, oop_remaining
) VALUES (
    'TRN20250115001', '2025-01-15', 'MEM001234567', 'Michael Johnson', '1985-03-15',
    '1234567890', 'Springfield General Hospital', '48', '2025-01-20',
    '2025-01-15 10:00:00', '2025-01-15 10:00:01', 'success', 'active',
    'PPO-GOLD', '2025-02-01', 175.00, 3675.00
);
```

### RxMemberSim Insert

```sql
BEGIN;

-- Insert pharmacy plan
INSERT INTO rx_plans (rx_plan_code, plan_name, plan_type, formulary_id, rx_deductible, rx_oop_max, combined_with_medical_oop, tier1_retail_30, tier1_mail_90, tier2_retail_30, tier2_mail_90, tier3_retail_30, tier3_mail_90, specialty_coinsurance, specialty_max_per_fill)
VALUES ('RX-COMMERCIAL-3TIER', 'Commercial 3-Tier Formulary', 'commercial', 'FORM2025-A', 0.00, 2500.00, FALSE, 10.00, 20.00, 35.00, 70.00, 60.00, 120.00, 25, 250.00);

-- Insert pharmacy members
INSERT INTO rx_members (member_id, cardholder_id, bin, pcn, group_number, person_code, given_name, family_name, birth_date, gender, rx_plan_code, coverage_start, relationship_code, subscriber_id, mail_order_eligible, specialty_eligible)
VALUES
    ('MEM001234567', 'ABC123456789', '003858', 'A4', 'RX1234', '01', 'Michael', 'Johnson', '1985-03-15', 'M', 'RX-COMMERCIAL-3TIER', '2025-02-01', '18', NULL, TRUE, TRUE),
    ('MEM001234568', 'ABC123456789', '003858', 'A4', 'RX1234', '02', 'Sarah', 'Johnson', '1987-07-22', 'F', 'RX-COMMERCIAL-3TIER', '2025-02-01', '01', 'MEM001234567', TRUE, TRUE),
    ('MEM001234569', 'ABC123456789', '003858', 'A4', 'RX1234', '03', 'Emma', 'Johnson', '2015-11-10', 'F', 'RX-COMMERCIAL-3TIER', '2025-02-01', '19', 'MEM001234567', TRUE, TRUE);

-- Insert pharmacy accumulators
INSERT INTO rx_accumulators (accumulator_id, member_id, rx_plan_code, plan_year, rx_deductible_applied, rx_deductible_limit, rx_deductible_met, rx_oop_applied, rx_oop_limit, specialty_ytd, daw_penalty_ytd, as_of_date)
VALUES
    ('RXACC20250615001', 'MEM001234567', 'RX-COMMERCIAL-3TIER', 2025, 0.00, 0.00, TRUE, 875.00, 2500.00, 750.00, 45.00, '2025-06-15'),
    ('RXACC20250615002', 'MEM001234568', 'RX-COMMERCIAL-3TIER', 2025, 0.00, 0.00, TRUE, 225.00, 2500.00, 0.00, 0.00, '2025-06-15');

-- Insert pharmacy prior authorization
INSERT INTO pharmacy_prior_auth (pa_id, member_id, ndc, drug_name, pa_type, status, urgency, request_date, decision_date, effective_date, expiration_date, override_code, approved_quantity, approved_days_supply, approved_fills, prescriber_npi, prescriber_name)
VALUES ('RX-PA-2025-0001234', 'MEM001234567', '00074437909', 'Humira 40mg/0.4ml Pen', 'specialty', 'approved', 'standard', '2025-01-15', '2025-01-17', '2025-01-17', '2026-01-17', 'PA12345678', 2, 28, 12, '1234567890', 'Dr. Emily Chen');

-- Insert DUR alert
INSERT INTO dur_alerts (alert_id, claim_id, member_id, ndc, drug_name, dur_code, dur_type, clinical_significance, interacting_ndc, interacting_drug, severity, pharmacist_message, override_code, outcome_code, alert_datetime)
VALUES ('DUR20250115001', 'RX20250115000003', 'MEM001234567', '00378180110', 'Warfarin 5mg', 'DD', 'drug_drug', 1, '63323021601', 'Aspirin 325mg', 'major', 'Increased bleeding risk - monitor INR', '2A', '1B', '2025-01-15 10:30:00');

-- Insert copay assistance program
INSERT INTO copay_assistance (program_id, member_id, ndc, drug_name, program_type, program_name, program_bin, program_pcn, program_start, program_end, annual_max_benefit, benefit_used_ytd, benefit_remaining, status)
VALUES ('ASSIST001', 'MEM001234567', '00074433906', 'Humira 40mg Pen', 'manufacturer_copay', 'Humira Complete', '004682', 'HUMIRA', '2025-01-01', '2025-12-31', 16000.00, 495.00, 15505.00, 'active');

COMMIT;
```

### Medicare Part D Insert

```sql
BEGIN;

-- Insert Medicare Part D plan
INSERT INTO rx_plans (rx_plan_code, plan_name, plan_type, formulary_id, rx_deductible, rx_oop_max, tier1_retail_30, tier2_retail_30, tier3_retail_30, part_d_deductible, part_d_icl, part_d_catastrophic_threshold)
VALUES ('RX-PARTD-STD', 'Medicare Part D Standard', 'medicare_d', 'FORM2025-PARTD', 590.00, 8000.00, 5.00, 15.00, 47.00, 590.00, 5030.00, 8000.00);

-- Insert Medicare member
INSERT INTO rx_members (member_id, cardholder_id, bin, pcn, group_number, person_code, given_name, family_name, birth_date, gender, rx_plan_code, coverage_start, relationship_code, mail_order_eligible, specialty_eligible)
VALUES ('MBI1234567890', 'MBI1234567890', '015581', 'HRX', 'PARTD2025', '01', 'Robert', 'Williams', '1957-06-15', 'M', 'RX-PARTD-STD', '2025-01-01', '18', TRUE, TRUE);

-- Insert Part D accumulator with phase tracking
INSERT INTO rx_accumulators (accumulator_id, member_id, rx_plan_code, plan_year, rx_deductible_applied, rx_deductible_limit, rx_deductible_met, rx_deductible_met_date, part_d_phase, troop_applied, gross_drug_cost_ytd, as_of_date)
VALUES ('RXACC20250915001', 'MBI1234567890', 'RX-PARTD-STD', 2025, 590.00, 590.00, TRUE, '2025-02-28', 'coverage_gap', 6125.00, 12850.00, '2025-09-15');

COMMIT;
```

## Dialect-Specific Syntax

### PostgreSQL

```sql
-- Use ON CONFLICT for upsert
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender)
VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M')
ON CONFLICT (mrn) DO UPDATE SET
    given_name = EXCLUDED.given_name,
    family_name = EXCLUDED.family_name,
    updated_at = CURRENT_TIMESTAMP;
```

### MySQL

```sql
-- Use INSERT ... ON DUPLICATE KEY UPDATE
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender)
VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M')
ON DUPLICATE KEY UPDATE
    given_name = VALUES(given_name),
    family_name = VALUES(family_name),
    updated_at = CURRENT_TIMESTAMP;
```

### SQL Server

```sql
-- Use MERGE for upsert
MERGE INTO patients AS target
USING (VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M'))
    AS source (mrn, given_name, family_name, birth_date, gender)
ON target.mrn = source.mrn
WHEN MATCHED THEN
    UPDATE SET given_name = source.given_name, family_name = source.family_name
WHEN NOT MATCHED THEN
    INSERT (mrn, given_name, family_name, birth_date, gender)
    VALUES (source.mrn, source.given_name, source.family_name, source.birth_date, source.gender);
```

### Oracle

```sql
-- Use MERGE for upsert
MERGE INTO patients target
USING (SELECT 'MRN00000001' AS mrn, 'John' AS given_name, 'Smith' AS family_name,
       TO_DATE('1970-03-15', 'YYYY-MM-DD') AS birth_date, 'M' AS gender FROM dual) source
ON (target.mrn = source.mrn)
WHEN MATCHED THEN
    UPDATE SET target.given_name = source.given_name, target.family_name = source.family_name
WHEN NOT MATCHED THEN
    INSERT (mrn, given_name, family_name, birth_date, gender)
    VALUES (source.mrn, source.given_name, source.family_name, source.birth_date, source.gender);
```

### SQLite

```sql
-- Use INSERT OR REPLACE
INSERT OR REPLACE INTO patients (mrn, given_name, family_name, birth_date, gender)
VALUES ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M');
```

## Batch Loading Script

**Request:** "Generate SQL load script for 100 patients"

**Output:**
```sql
-- HealthSim Data Load Script
-- Generated: 2025-01-15T14:30:00
-- Dialect: PostgreSQL
-- Records: 100 patients with related data

BEGIN;

-- Patients (batch 1 of 1)
INSERT INTO patients (mrn, given_name, family_name, birth_date, gender, city, state) VALUES
    ('MRN00000001', 'John', 'Smith', '1970-03-15', 'M', 'Springfield', 'IL'),
    ('MRN00000002', 'Maria', 'Garcia', '1955-10-20', 'F', 'Springfield', 'IL'),
    -- ... 98 more rows ...
    ('MRN00000100', 'Robert', 'Taylor', '1982-11-30', 'M', 'Springfield', 'IL');

-- Verify count
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM patients) < 100 THEN
        RAISE EXCEPTION 'Expected 100 patients, found %', (SELECT COUNT(*) FROM patients);
    END IF;
END $$;

COMMIT;
```

## String Escaping

| Character | Escaped As |
|-----------|------------|
| Single quote | `''` |
| Backslash | `\\` (MySQL) |
| NULL value | `NULL` keyword |
| Unicode | Native UTF-8 |

**Example:**
```sql
-- Name with apostrophe
INSERT INTO patients (mrn, family_name)
VALUES ('MRN00000001', 'O''Brien');

-- Address with special characters
INSERT INTO patients (mrn, street_address)
VALUES ('MRN00000001', '123 Main St, Apt #5');
```

## Validation Rules

1. **Foreign keys**: Referenced records must exist
2. **NOT NULL constraints**: Required fields must have values
3. **Data types**: Values must match column types
4. **Unique constraints**: No duplicate primary keys
5. **Check constraints**: Values within valid ranges

## Related Skills

- [csv.md](csv.md) - CSV export
- [../skills/patientsim/SKILL.md](../skills/patientsim/SKILL.md) - Patient data
- [../skills/membersim/SKILL.md](../skills/membersim/SKILL.md) - Claims data
- [../skills/rxmembersim/SKILL.md](../skills/rxmembersim/SKILL.md) - Pharmacy data
- [../references/code-systems.md](../references/code-systems.md) - Code systems
