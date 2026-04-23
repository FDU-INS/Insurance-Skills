---
name: patient-intake
description: Establishes a comprehensive framework for the intake and registration of new patients, encompassing data collection, insurance verification, risk stratification, and pharmacy network validation.
required_tools:
  - validateInsurance
  - validatePrescriptionBenefits
  - calculateLifestyleRisk
  - calculateOverallRisk
  - verifyPharmacy
  - registerPatient
---

### Step 1: Verify Primary Insurance Coverage
Access the payer portal to verify the patient's primary insurance coverage status and effective dates. Document benefit levels, copayment requirements, and confirm network participation. Record any authorization requirements.
Call `validateInsurance` with the following parameters:
- `patient_id`: [patient_id]
- `insurance_provider`: [insurance_provider]
- `policy_number`: [policy_number]
- `group_number`: [group_number]
- `coverage_start_date`: [coverage_start_date]
- `insurance_type`: [insurance_type]

### Step 2: Validate Prescription Benefits
Query the PBM database to verify current prescription coverage. Confirm formulary compliance parameters, document prior authorization requirements, and confirm specialty pharmacy protocols. Record the copayment structure.
Call `validatePrescriptionBenefits` with the following parameters:
- `patient_id`: [patient_id]
- `insurance_provider`: [prescription_insurance_provider]
- `policy_number`: [prescription_policy_number]

### Step 3: Evaluate Lifestyle Risk Factors
Calculate the patient's lifestyle risk index based on their smoking status, alcohol consumption frequency, and exercise patterns.
Call `calculateLifestyleRisk` with the following parameters:
- `patient_id`: [patient_id]
- `smoking_status`: [smoking_status]
- `alcohol_consumption`: [alcohol_consumption]
- `exercise_frequency`: [exercise_frequency]

### Step 4: Assess Clinical and Overall Risk
Review the patient's surgical history chronology and evaluate chronic condition severity. Calculate the comorbidity interaction score and generate a weighted risk factor index to determine the overall risk level, incorporating the previously calculated lifestyle risk.
Call `calculateOverallRisk` with the following parameters:
- `patient_id`: [patient_id]
- `previous_surgeries`: [previous_surgeries]
- `chronic_conditions`: [chronic_conditions]
- `life_style_risk_level`: [life_style_risk_level from Step 3]

### Step 5: Verify Preferred Pharmacy Network
Query the preferred pharmacy database to verify network participation for the patient's chosen pharmacy and document any special handling requirements.
Call `verifyPharmacy` with the following parameters:
- `patient_id`: [patient_id]
- `preferred_pharmacy_name`: [preferred_pharmacy_name]
- `preferred_pharmacy_address`: [preferred_pharmacy_address]
- `pharmacy_phone`: [pharmacy_phone]

### Step 6: Register Patient
Confirm that all eligibility criteria are met, including valid primary insurance, prescription benefits, acceptable lifestyle risk, compatible overall risk, and verified pharmacy network participation. Complete the patient registration process in the EHR.
Call `registerPatient` with the following parameters:
- `patient_id`: [patient_id]
- `insurance_validation`: [insurance_validation status from Step 1]
- `prescription_insurance_validation`: [prescription_insurance_validation status from Step 2]
- `life_style_risk_level`: [life_style_risk_level from Step 3]
- `overall_risk_level`: [overall_risk_level from Step 4]
- `pharmacy_check`: [pharmacy_check status from Step 5]