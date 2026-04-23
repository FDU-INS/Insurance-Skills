# CSV Export Format

## Trigger Phrases

- CSV
- as CSV
- CSV file
- comma separated
- spreadsheet
- Excel
- export to CSV
- tabular format
- flat file

## Overview

This skill exports HealthSim entities to CSV (Comma-Separated Values) format for use in spreadsheets, data analysis tools, and bulk data loading. Each entity type maps to a specific CSV schema.

## Export Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| delimiter | `,`, `\t`, `|`, `;` | `,` | Field separator |
| quote_char | `"`, `'` | `"` | String quotation |
| header | true, false | true | Include header row |
| null_value | empty, `NULL`, `\N` | empty | How to represent nulls |
| date_format | ISO, US, EU | ISO | Date formatting |
| encoding | UTF-8, UTF-16, ASCII | UTF-8 | Character encoding |

## Entity Schemas

### patients.csv

```csv
mrn,given_name,family_name,middle_name,birth_date,gender,ssn,street_address,city,state,postal_code,country,phone_home,phone_work,email,language,marital_status,race,ethnicity,deceased,deceased_date
MRN00000001,John,Smith,Michael,1970-03-15,M,123-45-6789,123 Main St,Springfield,IL,62701,USA,555-123-4567,555-987-6543,john.smith@email.com,ENG,M,2106-3,2186-5,N,
MRN00000002,Maria,Garcia,Elena,1955-10-20,F,987-65-4321,456 Oak Ave,Springfield,IL,62702,USA,555-876-5432,,maria.garcia@email.com,SPA,W,2106-3,2135-2,N,
```

| Column | Type | Description |
|--------|------|-------------|
| mrn | string | Medical record number |
| given_name | string | First name |
| family_name | string | Last name |
| middle_name | string | Middle name (optional) |
| birth_date | date | YYYY-MM-DD |
| gender | string | M, F, O, U |
| ssn | string | Social Security Number |
| street_address | string | Street address |
| city | string | City |
| state | string | State code (2 letters) |
| postal_code | string | ZIP code |
| country | string | Country code |
| phone_home | string | Home phone |
| phone_work | string | Work phone |
| email | string | Email address |
| language | string | Preferred language code |
| marital_status | string | S, M, D, W, etc. |
| race | string | CDC race code |
| ethnicity | string | CDC ethnicity code |
| deceased | string | Y/N |
| deceased_date | date | YYYY-MM-DD if deceased |

### encounters.csv

```csv
encounter_id,patient_mrn,encounter_class,encounter_type,status,period_start,period_end,facility_code,facility_name,location_unit,location_room,location_bed,attending_npi,attending_name,admission_source,discharge_disposition,reason_code,reason_description
ENC0000000001,MRN00000001,I,inpatient,finished,2025-01-10T14:00:00,2025-01-15T10:00:00,SPRINGFIELD,Springfield Hospital,MED,201,A,1234567890,Dr. Robert Johnson,7,01,R06.00,Dyspnea
ENC0000000002,MRN00000002,O,office_visit,finished,2025-01-15T09:00:00,2025-01-15T09:30:00,CLINIC01,Main Street Clinic,,,,,9876543210,Dr. Lisa Chen,,,,
```

| Column | Type | Description |
|--------|------|-------------|
| encounter_id | string | Unique encounter identifier |
| patient_mrn | string | Patient MRN (foreign key) |
| encounter_class | string | I, O, E, U, OBS |
| encounter_type | string | inpatient, office_visit, etc. |
| status | string | planned, arrived, in-progress, finished |
| period_start | datetime | Admission/start time |
| period_end | datetime | Discharge/end time |
| facility_code | string | Facility identifier |
| facility_name | string | Facility name |
| location_unit | string | Unit/department |
| location_room | string | Room number |
| location_bed | string | Bed identifier |
| attending_npi | string | Attending physician NPI |
| attending_name | string | Attending physician name |
| admission_source | string | Admit source code |
| discharge_disposition | string | Discharge disposition code |
| reason_code | string | Primary reason ICD-10 |
| reason_description | string | Reason description |

### diagnoses.csv

```csv
diagnosis_id,patient_mrn,encounter_id,code,code_system,description,type,onset_date,abatement_date,clinical_status,verification_status,severity,diagnosed_by_npi
DX0000000001,MRN00000001,ENC0000000001,I50.23,ICD-10-CM,Acute on chronic systolic heart failure,principal,2020-03-15,,active,confirmed,moderate,1234567890
DX0000000002,MRN00000001,ENC0000000001,I10,ICD-10-CM,Essential hypertension,secondary,2015-06-20,,active,confirmed,,1234567890
DX0000000003,MRN00000001,ENC0000000001,E11.9,ICD-10-CM,Type 2 diabetes mellitus,secondary,2018-09-10,,active,confirmed,,1234567890
```

| Column | Type | Description |
|--------|------|-------------|
| diagnosis_id | string | Unique diagnosis identifier |
| patient_mrn | string | Patient MRN |
| encounter_id | string | Encounter ID |
| code | string | ICD-10-CM code |
| code_system | string | ICD-10-CM |
| description | string | Diagnosis description |
| type | string | principal, admitting, secondary, working |
| onset_date | date | When condition started |
| abatement_date | date | When condition resolved |
| clinical_status | string | active, resolved, inactive |
| verification_status | string | confirmed, provisional, differential |
| severity | string | mild, moderate, severe |
| diagnosed_by_npi | string | Diagnosing provider NPI |

### procedures.csv

```csv
procedure_id,patient_mrn,encounter_id,code,code_system,description,performed_datetime,performer_npi,performer_name,body_site,status
PX0000000001,MRN00000001,ENC0000000001,99223,CPT,Initial hospital care high severity,2025-01-10T16:00:00,1234567890,Dr. Robert Johnson,,completed
PX0000000002,MRN00000001,ENC0000000001,93000,CPT,Electrocardiogram routine,2025-01-10T15:30:00,1234567890,Dr. Robert Johnson,,completed
```

### medications.csv

```csv
medication_id,patient_mrn,encounter_id,ndc,rxnorm,drug_name,dose_value,dose_unit,route,frequency,start_date,end_date,status,prescriber_npi,prescriber_name,indication_code,refills_authorized,quantity_dispensed,days_supply
MED0000000001,MRN00000001,ENC0000000001,00093505601,314076,Lisinopril 10mg Tab,10,mg,oral,daily,2025-01-15,,active,1234567890,Dr. Robert Johnson,I10,5,30,30
MED0000000002,MRN00000001,ENC0000000001,00093085601,6809,Metformin 500mg Tab,500,mg,oral,BID,2025-01-15,,active,1234567890,Dr. Robert Johnson,E11.9,5,60,30
```

### observations.csv (Labs/Vitals)

```csv
observation_id,patient_mrn,encounter_id,code,code_system,description,value,unit,reference_low,reference_high,interpretation,effective_datetime,status,performer_npi,specimen_type
OBS0000000001,MRN00000001,ENC0000000001,2345-7,LOINC,Glucose,98,mg/dL,70,100,N,2025-01-15T15:00:00,final,9876543210,Blood
OBS0000000002,MRN00000001,ENC0000000001,2160-0,LOINC,Creatinine,1.1,mg/dL,0.7,1.3,N,2025-01-15T15:00:00,final,9876543210,Blood
OBS0000000003,MRN00000001,ENC0000000001,8480-6,LOINC,Systolic BP,128,mmHg,90,120,H,2025-01-15T14:30:00,final,1234567890,
```

### orders.csv

```csv
order_id,patient_mrn,encounter_id,order_type,code,code_system,description,priority,status,ordered_datetime,scheduled_datetime,completed_datetime,ordering_provider_npi,ordering_provider_name,performer_npi,performer_name
ORD0000000001,MRN00000001,ENC0000000001,LAB,80053,CPT,Comprehensive Metabolic Panel,R,completed,2025-01-15T14:30:00,,2025-01-15T16:00:00,1234567890,Dr. Robert Johnson,9876543210,Mary Jones MT
ORD0000000002,MRN00000001,ENC0000000001,RAD,71046,CPT,Chest X-ray 2 views,R,completed,2025-01-15T10:15:00,,2025-01-15T12:00:00,1234567890,Dr. Robert Johnson,4567890123,Dr. Sarah Williams
```

### claims.csv

```csv
claim_id,member_id,claim_type,status,service_from_date,service_to_date,facility_npi,facility_name,billing_provider_npi,rendering_provider_npi,principal_diagnosis,total_charge,total_allowed,total_paid,patient_responsibility,adjudicated_date,auth_number
CLM20250115001,MEM001234,professional,paid,2025-01-15,2025-01-15,,,,1234567890,E11.9,175.00,150.00,125.00,25.00,2025-01-16,
CLM20250115002,MEM001234,institutional,paid,2025-01-10,2025-01-15,1234567890,Springfield Hospital,1234567890,,I50.23,45000.00,38000.00,35000.00,3000.00,2025-01-20,AUTH001
```

### claim_lines.csv

```csv
claim_id,line_number,procedure_code,procedure_modifier,revenue_code,ndc,description,service_date,quantity,charge_amount,allowed_amount,paid_amount,deductible,copay,coinsurance,diagnosis_pointer,place_of_service
CLM20250115001,1,99214,,,,Office visit established,2025-01-15,1,175.00,150.00,125.00,0.00,25.00,0.00,1,11
CLM20250115002,1,99223,,0120,,Hospital initial care,2025-01-10,1,1800.00,1500.00,1400.00,100.00,0.00,0.00,1,21
CLM20250115002,2,,,0250,,Pharmacy,2025-01-12,1,450.00,400.00,400.00,0.00,0.00,0.00,,21
```

### pharmacy_claims.csv

```csv
claim_id,member_id,prescription_number,fill_date,ndc,drug_name,quantity_dispensed,days_supply,pharmacy_npi,pharmacy_name,prescriber_npi,prescriber_name,ingredient_cost,dispensing_fee,patient_pay,plan_pay,copay,coinsurance,formulary_tier,daw_code,transaction_code
RX20250115001,MEM001234,SPX001234,2025-01-15,00093505601,Lisinopril 10mg Tab,30,30,1122334455,Main Street Pharmacy,1234567890,Dr. Robert Johnson,8.50,2.00,10.00,0.50,10.00,0.00,1,0,B1
```

### members.csv

```csv
member_id,subscriber_id,relationship_code,given_name,family_name,birth_date,gender,ssn,street_address,city,state,postal_code,email,phone,group_id,plan_code,coverage_start,coverage_end,pcp_npi,pcp_name,coverage_tier
MEM001234567,MEM001234567,18,Michael,Johnson,1985-03-15,M,123-45-6789,456 Oak Avenue,Springfield,IL,62702,michael.johnson@email.com,555-234-5678,GRP001234,PPO-GOLD,2025-02-01,,1234567890,Dr. Sarah Williams,FAM
MEM001234568,MEM001234567,01,Sarah,Johnson,1987-07-22,F,987-65-4321,456 Oak Avenue,Springfield,IL,62702,,,GRP001234,PPO-GOLD,2025-02-01,,,FAM
MEM001234569,MEM001234567,19,Emma,Johnson,2015-11-10,F,456-78-9012,456 Oak Avenue,Springfield,IL,62702,,,GRP001234,PPO-GOLD,2025-02-01,,,FAM
```

| Column | Type | Description |
|--------|------|-------------|
| member_id | string | Unique member identifier |
| subscriber_id | string | Subscriber's member ID (self for subscriber) |
| relationship_code | string | 18=Self, 01=Spouse, 19=Child |
| given_name | string | First name |
| family_name | string | Last name |
| birth_date | date | YYYY-MM-DD |
| gender | string | M, F, O, U |
| ssn | string | Social Security Number |
| street_address | string | Street address |
| city | string | City |
| state | string | State code (2 letters) |
| postal_code | string | ZIP code |
| email | string | Email address |
| phone | string | Phone number |
| group_id | string | Employer group identifier |
| plan_code | string | Benefit plan code |
| coverage_start | date | Coverage effective date |
| coverage_end | date | Coverage termination date |
| pcp_npi | string | Primary care provider NPI |
| pcp_name | string | PCP name |
| coverage_tier | string | EMP, ESP, ECH, FAM |

### enrollments.csv

```csv
enrollment_id,member_id,transaction_type,transaction_date,effective_date,enrollment_reason,plan_code,coverage_tier,premium_amount,employer_contribution,employee_contribution,status
ENR20250115001,MEM001234567,add,2025-01-15,2025-02-01,new_hire,PPO-GOLD,FAM,850.00,650.00,200.00,active
ENR20250115002,MEM001234568,add,2025-01-15,2025-02-01,new_hire,PPO-GOLD,FAM,0.00,0.00,0.00,active
ENR20250115003,MEM001234569,add,2025-01-15,2025-02-01,new_hire,PPO-GOLD,FAM,0.00,0.00,0.00,active
ENR20250120001,MEM001234570,add,2025-01-20,2025-01-20,qle,PPO-GOLD,FAM,0.00,0.00,0.00,active
```

| Column | Type | Description |
|--------|------|-------------|
| enrollment_id | string | Unique enrollment transaction ID |
| member_id | string | Member identifier |
| transaction_type | string | add, change, termination, reinstatement |
| transaction_date | date | Date transaction submitted |
| effective_date | date | Date change takes effect |
| enrollment_reason | string | new_hire, open_enrollment, qle, cobra |
| plan_code | string | Benefit plan code |
| coverage_tier | string | EMP, ESP, ECH, FAM |
| premium_amount | decimal | Total premium |
| employer_contribution | decimal | Employer portion |
| employee_contribution | decimal | Employee portion |
| status | string | active, pending, terminated |

### groups.csv

```csv
group_id,group_name,tax_id,street_address,city,state,postal_code,effective_date,termination_date,contact_name,contact_email,contact_phone
GRP001234,Acme Corporation,12-3456789,100 Corporate Drive,Springfield,IL,62701,2020-01-01,,Jane Smith,jane.smith@acme.com,555-100-2000
GRP001235,Widget Industries,98-7654321,200 Industrial Blvd,Springfield,IL,62702,2021-07-01,,Bob Wilson,bob.wilson@widget.com,555-200-3000
```

| Column | Type | Description |
|--------|------|-------------|
| group_id | string | Unique group identifier |
| group_name | string | Employer/group name |
| tax_id | string | Federal Tax ID/EIN |
| street_address | string | Street address |
| city | string | City |
| state | string | State code |
| postal_code | string | ZIP code |
| effective_date | date | Group effective date |
| termination_date | date | Group termination date |
| contact_name | string | Primary contact name |
| contact_email | string | Contact email |
| contact_phone | string | Contact phone |

### plans.csv

```csv
plan_code,plan_name,plan_type,network_requirement,individual_deductible,family_deductible,individual_oop_max,family_oop_max,pcp_copay,specialist_copay,er_copay,coinsurance,pcp_required,referral_required
PPO-GOLD,PPO Gold Plan,PPO,in_network_preferred,500.00,1000.00,4000.00,8000.00,25.00,50.00,150.00,20,N,N
HMO-STD,HMO Standard,HMO,in_network_only,0.00,0.00,3000.00,6000.00,20.00,40.00,150.00,0,Y,Y
HDHP-HSA,HDHP with HSA,HDHP,in_network_preferred,1600.00,3200.00,7000.00,14000.00,0.00,0.00,0.00,20,N,N
```

| Column | Type | Description |
|--------|------|-------------|
| plan_code | string | Unique plan identifier |
| plan_name | string | Plan display name |
| plan_type | string | HMO, PPO, EPO, POS, HDHP |
| network_requirement | string | in_network_only, in_network_preferred |
| individual_deductible | decimal | Individual deductible amount |
| family_deductible | decimal | Family deductible amount |
| individual_oop_max | decimal | Individual out-of-pocket max |
| family_oop_max | decimal | Family out-of-pocket max |
| pcp_copay | decimal | Primary care copay |
| specialist_copay | decimal | Specialist copay |
| er_copay | decimal | Emergency room copay |
| coinsurance | integer | Coinsurance percentage |
| pcp_required | string | Y/N - PCP assignment required |
| referral_required | string | Y/N - Referral required for specialists |

### plan_service_benefits.csv

Detailed benefit structure by service type for each plan:

```csv
plan_code,service_type,network_tier,cost_sharing_type,cost_sharing_amount,deductible_applies,annual_limit,prior_auth_required
PPO-GOLD,pcp_visit,in_network,copay,25.00,N,,N
PPO-GOLD,pcp_visit,out_of_network,coinsurance,40,,N
PPO-GOLD,specialist_visit,in_network,copay,50.00,N,,N
PPO-GOLD,specialist_visit,out_of_network,coinsurance,40,,N
PPO-GOLD,urgent_care,in_network,copay,75.00,N,,N
PPO-GOLD,emergency_room,in_network,copay,150.00,N,,N
PPO-GOLD,inpatient,in_network,coinsurance,20,Y,,Y
PPO-GOLD,inpatient,out_of_network,coinsurance,40,Y,,Y
PPO-GOLD,outpatient_surgery,in_network,copay,200.00,Y,,Y
PPO-GOLD,advanced_imaging,in_network,coinsurance,20,Y,,Y
PPO-GOLD,lab_work,in_network,copay,0.00,N,,N
PPO-GOLD,preventive,in_network,covered_100,0.00,N,,N
HMO-STD,pcp_visit,in_network,copay,20.00,N,,N
HMO-STD,specialist_visit,in_network,copay,40.00,N,,Y
HDHP-HSA,pcp_visit,in_network,coinsurance,20,Y,,N
HDHP-HSA,preventive,in_network,covered_100,0.00,N,,N
```

| Column | Type | Description |
|--------|------|-------------|
| plan_code | string | Plan identifier |
| service_type | string | Service type (pcp_visit, specialist_visit, etc.) |
| network_tier | string | in_network, out_of_network, tier_1, tier_2 |
| cost_sharing_type | string | copay, coinsurance, covered_100 |
| cost_sharing_amount | decimal | Copay amount or coinsurance percentage |
| deductible_applies | string | Y/N - Does deductible apply |
| annual_limit | integer | Visit limit per year (if applicable) |
| prior_auth_required | string | Y/N - Prior auth needed |

### pharmacy_benefits.csv

Pharmacy benefit tiers for each plan:

```csv
plan_code,tier,tier_name,retail_30_copay,retail_90_copay,mail_90_copay,specialty_coinsurance,specialty_max,deductible_applies
PPO-GOLD,1,Preferred Generic,10.00,25.00,25.00,,,N
PPO-GOLD,2,Non-Preferred Generic,25.00,62.50,62.50,,,N
PPO-GOLD,3,Preferred Brand,50.00,125.00,125.00,,,N
PPO-GOLD,4,Non-Preferred Brand,80.00,200.00,200.00,,,N
PPO-GOLD,5,Specialty,,,,,25,250.00,N
HDHP-HSA,1,Preferred Generic,10.00,25.00,25.00,,,Y
HDHP-HSA,2,Non-Preferred Generic,25.00,62.50,62.50,,,Y
HDHP-HSA,3,Preferred Brand,50.00,125.00,125.00,,,Y
HDHP-HSA,4,Non-Preferred Brand,80.00,200.00,200.00,,,Y
HDHP-HSA,5,Specialty,,,,,25,250.00,Y
HMO-STD,1,Generic,15.00,37.50,37.50,,,N
HMO-STD,2,Preferred Brand,40.00,100.00,100.00,,,N
HMO-STD,3,Non-Preferred Brand,75.00,187.50,187.50,,,N
HMO-STD,4,Specialty,,,,,30,200.00,N
```

| Column | Type | Description |
|--------|------|-------------|
| plan_code | string | Plan identifier |
| tier | integer | Formulary tier (1-5) |
| tier_name | string | Tier description |
| retail_30_copay | decimal | 30-day retail copay |
| retail_90_copay | decimal | 90-day retail copay |
| mail_90_copay | decimal | 90-day mail order copay |
| specialty_coinsurance | integer | Coinsurance % for specialty |
| specialty_max | decimal | Maximum copay for specialty |
| deductible_applies | string | Y/N - Does Rx deductible apply |

### plan_accumulators.csv

Member-level accumulator tracking:

```csv
member_id,plan_code,plan_year,accumulator_type,individual_applied,individual_limit,family_applied,family_limit,as_of_date
MEM001234567,PPO-GOLD,2025,deductible,325.00,500.00,325.00,1000.00,2025-01-20
MEM001234567,PPO-GOLD,2025,oop_max,350.00,4000.00,350.00,8000.00,2025-01-20
MEM001234568,PPO-GOLD,2025,deductible,0.00,500.00,325.00,1000.00,2025-01-20
MEM001234568,PPO-GOLD,2025,oop_max,0.00,4000.00,350.00,8000.00,2025-01-20
```

| Column | Type | Description |
|--------|------|-------------|
| member_id | string | Member identifier |
| plan_code | string | Plan identifier |
| plan_year | integer | Benefit year |
| accumulator_type | string | deductible, oop_max, rx_deductible |
| individual_applied | decimal | Amount applied to individual |
| individual_limit | decimal | Individual limit |
| family_applied | decimal | Amount applied to family |
| family_limit | decimal | Family limit |
| as_of_date | date | Date of accumulator snapshot |

### eligibility_inquiries.csv

```csv
trace_number,inquiry_date,member_id,member_name,birth_date,provider_npi,provider_name,service_type,service_date,response_status,eligibility_status,plan_code,coverage_start,coverage_end,deductible_remaining,oop_remaining
TRN20250115001,2025-01-15,MEM001234567,Michael Johnson,1985-03-15,1234567890,Springfield General Hospital,48,2025-01-20,success,active,PPO-GOLD,2025-02-01,,175.00,3675.00
TRN20250115002,2025-01-15,MEM999999999,John Doe,1970-05-15,1234567890,Springfield General Hospital,48,2025-01-20,error,not_found,,,,,,
```

| Column | Type | Description |
|--------|------|-------------|
| trace_number | string | Unique inquiry trace number |
| inquiry_date | date | Date of inquiry |
| member_id | string | Member identifier |
| member_name | string | Member full name |
| birth_date | date | Member date of birth |
| provider_npi | string | Requesting provider NPI |
| provider_name | string | Provider name |
| service_type | string | Service type code (30, 47, 48, etc.) |
| service_date | date | Proposed date of service |
| response_status | string | success, error |
| eligibility_status | string | active, inactive, not_found |
| plan_code | string | Benefit plan code |
| coverage_start | date | Coverage effective date |
| coverage_end | date | Coverage termination date |
| deductible_remaining | decimal | Remaining deductible |
| oop_remaining | decimal | Remaining out-of-pocket |

### rx_members.csv

```csv
member_id,cardholder_id,bin,pcn,group_number,person_code,given_name,family_name,birth_date,gender,rx_plan_code,coverage_start,coverage_end,relationship_code,subscriber_id,mail_order_eligible,specialty_eligible
MEM001234567,ABC123456789,003858,A4,RX1234,01,Michael,Johnson,1985-03-15,M,RX-COMMERCIAL-3TIER,2025-02-01,,18,,Y,Y
MEM001234568,ABC123456789,003858,A4,RX1234,02,Sarah,Johnson,1987-07-22,F,RX-COMMERCIAL-3TIER,2025-02-01,,01,MEM001234567,Y,Y
MEM001234569,ABC123456789,003858,A4,RX1234,03,Emma,Johnson,2015-11-10,F,RX-COMMERCIAL-3TIER,2025-02-01,,19,MEM001234567,Y,Y
```

| Column | Type | Description |
|--------|------|-------------|
| member_id | string | Unique member identifier |
| cardholder_id | string | ID on pharmacy card |
| bin | string | Bank Identification Number (6 digits) |
| pcn | string | Processor Control Number |
| group_number | string | Pharmacy group number |
| person_code | string | 01=subscriber, 02=spouse, 03+=children |
| given_name | string | First name |
| family_name | string | Last name |
| birth_date | date | YYYY-MM-DD |
| gender | string | M, F, O, U |
| rx_plan_code | string | Pharmacy plan identifier |
| coverage_start | date | Coverage effective date |
| coverage_end | date | Coverage termination date |
| relationship_code | string | 18=Self, 01=Spouse, 19=Child |
| subscriber_id | string | Subscriber member ID (if dependent) |
| mail_order_eligible | string | Y/N |
| specialty_eligible | string | Y/N |

### rx_plans.csv

```csv
rx_plan_code,plan_name,plan_type,formulary_id,rx_deductible,rx_oop_max,combined_with_medical_oop,tier1_retail_30,tier1_mail_90,tier2_retail_30,tier2_mail_90,tier3_retail_30,tier3_mail_90,specialty_coinsurance,specialty_max_per_fill
RX-COMMERCIAL-3TIER,Commercial 3-Tier Formulary,commercial,FORM2025-A,0.00,2500.00,N,10.00,20.00,35.00,70.00,60.00,120.00,25,250.00
RX-PARTD-STD,Medicare Part D Standard,medicare_d,FORM2025-PARTD,590.00,8000.00,N,5.00,,15.00,,47.00,,,
RX-HDHP-HSA,HDHP Pharmacy Benefit,commercial,FORM2025-HDHP,1600.00,7000.00,Y,10.00,20.00,40.00,80.00,30,60,20,200.00
```

| Column | Type | Description |
|--------|------|-------------|
| rx_plan_code | string | Unique plan identifier |
| plan_name | string | Plan display name |
| plan_type | string | commercial, medicare_d, medicaid |
| formulary_id | string | Associated formulary |
| rx_deductible | decimal | Pharmacy deductible |
| rx_oop_max | decimal | Pharmacy out-of-pocket max |
| combined_with_medical_oop | string | Y/N |
| tier1_retail_30 | decimal | Tier 1 30-day retail copay |
| tier1_mail_90 | decimal | Tier 1 90-day mail copay |
| tier2_retail_30 | decimal | Tier 2 30-day retail copay |
| tier2_mail_90 | decimal | Tier 2 90-day mail copay |
| tier3_retail_30 | decimal | Tier 3 30-day retail copay |
| tier3_mail_90 | decimal | Tier 3 90-day mail copay |
| specialty_coinsurance | integer | Specialty coinsurance % |
| specialty_max_per_fill | decimal | Max copay per specialty fill |

### rx_accumulators.csv

```csv
member_id,rx_plan_code,plan_year,rx_deductible_applied,rx_deductible_limit,rx_deductible_met,rx_oop_applied,rx_oop_limit,rx_oop_met,specialty_ytd,daw_penalty_ytd,part_d_phase,troop_applied,as_of_date
MEM001234567,RX-COMMERCIAL-3TIER,2025,250.00,250.00,Y,875.00,2500.00,N,750.00,45.00,,,2025-06-15
MBI1234567890,RX-PARTD-STD,2025,590.00,590.00,Y,,,N,,,coverage_gap,6125.00,2025-09-15
MEM001234568,RX-HDHP-HSA,2025,320.00,1600.00,N,450.00,7000.00,N,,,,2025-06-15
```

| Column | Type | Description |
|--------|------|-------------|
| member_id | string | Member identifier |
| rx_plan_code | string | Pharmacy plan identifier |
| plan_year | integer | Benefit year |
| rx_deductible_applied | decimal | Deductible amount used |
| rx_deductible_limit | decimal | Deductible limit |
| rx_deductible_met | string | Y/N |
| rx_oop_applied | decimal | OOP amount used |
| rx_oop_limit | decimal | OOP limit |
| rx_oop_met | string | Y/N |
| specialty_ytd | decimal | Specialty drugs YTD paid |
| daw_penalty_ytd | decimal | DAW penalties YTD |
| part_d_phase | string | deductible, icl, coverage_gap, catastrophic |
| troop_applied | decimal | True Out-of-Pocket (Part D) |
| as_of_date | date | Accumulator snapshot date |

### pharmacy_prior_auth.csv

```csv
pa_id,member_id,ndc,drug_name,pa_type,status,request_date,decision_date,urgency,effective_date,expiration_date,override_code,denial_reason_code,prescriber_npi,prescriber_name
RX-PA-2025-0001234,MEM001234567,00074437909,Humira 40mg/0.4ml Pen,specialty,approved,2025-01-15,2025-01-17,standard,2025-01-17,2026-01-17,PA12345678,,1234567890,Dr. Emily Chen
RX-PA-2025-0001235,MEM001234568,00597024101,Repatha 140mg Pen,step_therapy_override,denied,2025-01-15,2025-01-17,standard,,,STEP_THERAPY_NOT_MET,1234567891,Dr. James Wilson
RX-PA-2025-0001236,MEM001234569,00169413312,Ozempic 2mg/1.5ml Pen,clinical_pa,pending,2025-01-15,,urgent,,,,1234567892,Dr. Lisa Park
```

| Column | Type | Description |
|--------|------|-------------|
| pa_id | string | Unique PA identifier |
| member_id | string | Member identifier |
| ndc | string | National Drug Code |
| drug_name | string | Drug name |
| pa_type | string | formulary_exception, step_therapy_override, quantity_limit, age_edit, clinical_pa, specialty |
| status | string | pending, approved, denied, cancelled, expired |
| request_date | date | PA request date |
| decision_date | date | Decision date |
| urgency | string | standard, urgent, expedited |
| effective_date | date | Override effective date |
| expiration_date | date | Override expiration date |
| override_code | string | PA override code for claim submission |
| denial_reason_code | string | Denial reason code |
| prescriber_npi | string | Requesting prescriber NPI |
| prescriber_name | string | Prescriber name |

### dur_alerts.csv

```csv
alert_id,claim_id,member_id,ndc,drug_name,dur_code,dur_type,clinical_significance,interacting_ndc,interacting_drug,severity,pharmacist_message,override_code,outcome_code,alert_datetime
DUR20250115001,RX20250115000003,MEM001234567,00378180110,Warfarin 5mg,DD,drug_drug,1,63323021601,Aspirin 325mg,major,Increased bleeding risk - monitor INR,2A,1B,2025-01-15T10:30:00
DUR20250115002,RX20250115000004,MEM001234567,00093505601,Lisinopril 10mg,ER,early_refill,3,,,minor,Refill 8 days early (73% supply used),,1A,2025-01-15T11:15:00
DUR20250115003,RX20250115000005,MEM001234568,00071015523,Atorvastatin 20mg,TD,therapeutic_dup,2,00093764156,Simvastatin 40mg,moderate,Duplicate statin therapy detected,1K,1C,2025-01-15T14:00:00
```

| Column | Type | Description |
|--------|------|-------------|
| alert_id | string | Unique alert identifier |
| claim_id | string | Associated claim ID |
| member_id | string | Member identifier |
| ndc | string | NDC of drug causing alert |
| drug_name | string | Drug name |
| dur_code | string | DUR code (DD, ER, TD, HD, etc.) |
| dur_type | string | Alert type description |
| clinical_significance | integer | 1=major, 2=moderate, 3=minor, 4=undetermined |
| interacting_ndc | string | NDC of interacting drug (if applicable) |
| interacting_drug | string | Interacting drug name |
| severity | string | major, moderate, minor |
| pharmacist_message | string | Alert message |
| override_code | string | Pharmacist override code |
| outcome_code | string | Outcome of service code |
| alert_datetime | datetime | When alert was generated |

### copay_assistance.csv

```csv
program_id,member_id,ndc,drug_name,program_type,program_name,program_start,program_end,annual_max_benefit,benefit_used_ytd,benefit_remaining,status
ASSIST001,MEM001234567,00074433906,Humira 40mg Pen,manufacturer_copay,Humira Complete,2025-01-01,2025-12-31,16000.00,495.00,15505.00,active
ASSIST002,MEM001234568,00003089421,Eliquis 5mg Tab,manufacturer_copay,Eliquis Savings Card,2025-01-01,2025-12-31,6000.00,250.00,5750.00,active
ASSIST003,MEM001234569,00002323080,Trulicity 1.5mg Pen,patient_assistance,Lilly Cares,2025-01-01,2025-12-31,,,0.00,pending
```

| Column | Type | Description |
|--------|------|-------------|
| program_id | string | Unique program identifier |
| member_id | string | Member identifier |
| ndc | string | NDC of covered drug |
| drug_name | string | Drug name |
| program_type | string | manufacturer_copay, patient_assistance, foundation, bridge |
| program_name | string | Program display name |
| program_start | date | Program effective date |
| program_end | date | Program expiration date |
| annual_max_benefit | decimal | Annual benefit maximum |
| benefit_used_ytd | decimal | Benefits used YTD |
| benefit_remaining | decimal | Remaining benefits |
| status | string | active, pending, expired, exhausted |

## Multi-File Export

When exporting a complete patient record, generate related CSV files:

```
export/
├── patients.csv
├── encounters.csv
├── diagnoses.csv
├── procedures.csv
├── medications.csv
├── observations.csv
├── orders.csv
├── allergies.csv
├── claims.csv
├── claim_lines.csv
└── pharmacy_claims.csv
```

When exporting enrollment and eligibility data:

```
export/
├── groups.csv
├── plans.csv
├── plan_service_benefits.csv
├── pharmacy_benefits.csv
├── members.csv
├── enrollments.csv
├── plan_accumulators.csv
└── eligibility_inquiries.csv
```

When exporting pharmacy/RxMemberSim data:

```
export/
├── rx_members.csv
├── rx_plans.csv
├── rx_accumulators.csv
├── pharmacy_claims.csv
├── pharmacy_prior_auth.csv
├── dur_alerts.csv
├── formulary_drugs.csv
└── copay_assistance.csv
```

## Example Transformations

### Single Patient Export

**Request:** "Export patient MRN00000001 to CSV"

**Output:**
```csv
mrn,given_name,family_name,birth_date,gender,street_address,city,state,postal_code
MRN00000001,John,Smith,1970-03-15,M,123 Main St,Springfield,IL,62701
```

### Batch Patient Export

**Request:** "Export 100 patients as CSV"

**Output:**
```csv
mrn,given_name,family_name,birth_date,gender,street_address,city,state,postal_code
MRN00000001,John,Smith,1970-03-15,M,123 Main St,Springfield,IL,62701
MRN00000002,Maria,Garcia,1955-10-20,F,456 Oak Ave,Springfield,IL,62702
MRN00000003,Eleanor,Thompson,1950-08-12,F,789 Elm St,Springfield,IL,62703
...
```

### Claims Export with Options

**Request:** "Export claims as pipe-delimited CSV with NULL markers"

**Output:**
```csv
claim_id|member_id|claim_type|status|service_date|total_charge|total_paid
CLM20250115001|MEM001234|professional|paid|2025-01-15|175.00|125.00
CLM20250115002|MEM001234|institutional|paid|2025-01-10|45000.00|35000.00
CLM20250115003|MEM001234|professional|denied|2025-01-16|200.00|NULL
```

## Special Handling

### Escaping Rules

| Scenario | Example Input | CSV Output |
|----------|---------------|------------|
| Comma in value | `Smith, Jr.` | `"Smith, Jr."` |
| Quote in value | `O'Brien` | `O'Brien` |
| Double quote in value | `He said "hello"` | `"He said ""hello"""` |
| Newline in value | `Line1\nLine2` | `"Line1\nLine2"` |

### Date Formats

| Format | Example | Use When |
|--------|---------|----------|
| ISO | 2025-01-15 | Default, international |
| US | 01/15/2025 | US systems |
| EU | 15/01/2025 | European systems |
| Timestamp | 2025-01-15T14:30:00 | Include time |

### Null Handling

| Option | Empty | With Value |
|--------|-------|------------|
| empty | `,,,` | Default behavior |
| NULL | `,NULL,NULL,` | Database loading |
| \N | `,\N,\N,` | MySQL LOAD DATA |

## Validation Rules

1. **Header required by default**: First row contains column names
2. **Consistent columns**: Every row same number of fields
3. **Proper quoting**: Fields with delimiters must be quoted
4. **UTF-8 encoding**: Default encoding for special characters
5. **Date consistency**: All dates in same format within file
6. **No trailing delimiters**: Lines end after last field

## Related Skills

- [sql.md](sql.md) - SQL INSERT statements
- [fhir-r4.md](fhir-r4.md) - FHIR format
- [../skills/patientsim/SKILL.md](../skills/patientsim/SKILL.md) - Patient data
- [../skills/membersim/SKILL.md](../skills/membersim/SKILL.md) - Claims data
- [../skills/rxmembersim/SKILL.md](../skills/rxmembersim/SKILL.md) - Pharmacy data
