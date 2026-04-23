# NetworkSim Examples

NetworkSim provides access to **8.9 million real US healthcare providers** from the NPPES registry. This is the primary use case. Synthetic generation is available when real data isn't appropriate.

---

## Real Provider Queries (Primary Use Case)

### Find Providers by Specialty and Location

**Prompt**:
```
Find cardiologists in Houston, TX
```

**Expected Response**:

Found 847 cardiologists in Houston, TX:

| NPI | Name | Credentials | Subspecialty | Practice Address |
|-----|------|-------------|--------------|------------------|
| 1234567890 | Dr. Sarah Chen | MD, FACC | Interventional Cardiology | 6624 Fannin St |
| 1876543210 | Dr. Michael Patel | MD, FSCAI | Electrophysiology | 1 Baylor Plaza |
| 1567890123 | Dr. Jennifer Williams | MD | General Cardiology | 7777 Southwest Fwy |
| ... | ... | ... | ... | ... |

Showing 20 of 847. Say "show more" for next page.

---

### Count Providers by Region

**Prompt**:
```
How many primary care physicians are in San Diego County?
```

**Expected Response**:

San Diego County has **2,847 primary care physicians**:

| Specialty | Count | % of Total |
|-----------|-------|------------|
| Family Medicine | 1,602 | 56% |
| Internal Medicine | 1,245 | 44% |

Geographic distribution:
- San Diego city: 1,423
- Chula Vista: 312
- Oceanside: 287
- Escondido: 198
- Other: 627

---

### Find Hospitals with Quality Data

**Prompt**:
```
Show me hospitals in Phoenix with 4+ star CMS ratings
```

**Expected Response**:

Found 12 hospitals in Phoenix metro with 4+ star ratings:

| Hospital | City | Beds | CMS Rating | Specialties |
|----------|------|------|------------|-------------|
| Mayo Clinic Hospital | Phoenix | 304 | 5 stars | Transplant, Cancer, Cardiology |
| Banner University Medical Center | Phoenix | 672 | 4 stars | Trauma Level 1, Teaching |
| HonorHealth Scottsdale Shea | Scottsdale | 409 | 4 stars | Cardiac, Orthopedic |
| ... | ... | ... | ... | ... |

---

### Verify a Provider's NPI

**Prompt**:
```
Is NPI 1234567890 a valid provider? What's their specialty?
```

**Expected Response**:

**NPI 1234567890 is valid.**

| Field | Value |
|-------|-------|
| Name | Dr. Sarah Chen |
| Entity Type | Individual |
| Primary Specialty | Cardiovascular Disease (207RC0000X) |
| Credentials | MD, FACC |
| City, State | Houston, TX |
| Enumeration Date | 2008-03-15 |

---

### Provider Distribution Analysis

**Prompt**:
```
Show the top 10 states by number of physicians
```

**Expected Response**:

| Rank | State | Physicians | Per 100K Population |
|------|-------|------------|---------------------|
| 1 | California | 142,567 | 361 |
| 2 | New York | 98,234 | 504 |
| 3 | Texas | 87,456 | 301 |
| 4 | Florida | 76,234 | 354 |
| 5 | Pennsylvania | 52,123 | 407 |
| 6 | Illinois | 48,567 | 383 |
| 7 | Ohio | 42,345 | 362 |
| 8 | Massachusetts | 41,234 | 598 |
| 9 | New Jersey | 38,567 | 434 |
| 10 | Michigan | 35,789 | 358 |

---

### Find Specialists for a Specific Condition

**Prompt**:
```
Find endocrinologists in Denver who specialize in diabetes
```

**Expected Response**:

Found 67 endocrinologists in Denver metro:

| NPI | Name | Credentials | Focus Areas | Accepting New Patients |
|-----|------|-------------|-------------|------------------------|
| 1234509876 | Dr. Amanda Rodriguez | MD, FACE | Diabetes, Thyroid | Yes |
| 1876540123 | Dr. David Kim | MD, PhD | Diabetes, Metabolism | Yes |
| ... | ... | ... | ... | ... |

Note: "Accepting New Patients" status may not be current in NPPES data.

---

### Network Adequacy Check

**Prompt**:
```
Are there enough PCPs in rural Montana counties?
```

**Expected Response**:

**Rural Montana PCP Analysis** (counties with <50K population):

| County | Population | PCPs | Ratio | Status |
|--------|------------|------|-------|--------|
| Flathead | 104,357 | 87 | 1:1,200 | Adequate |
| Ravalli | 44,174 | 28 | 1:1,578 | Borderline |
| Gallatin | 119,283 | 112 | 1:1,065 | Adequate |
| Lincoln | 19,589 | 8 | 1:2,449 | **Shortage** |
| Sanders | 12,148 | 4 | 1:3,037 | **Shortage** |
| ... | ... | ... | ... | ... |

6 of 52 Montana counties are designated HPSA (Health Professional Shortage Areas) for primary care.

---

## SQL Query Examples

For advanced users, direct SQL against the `network` schema:

### Find Providers by Taxonomy Code

```sql
SELECT npi, first_name, last_name, credential_text, city
FROM network.providers
WHERE state = 'CA'
  AND primary_taxonomy_code = '207RC0000X'  -- Cardiovascular Disease
  AND city = 'LOS ANGELES'
LIMIT 20;
```

### Join Provider and Quality Data

```sql
SELECT 
  p.organization_name,
  p.city,
  h.overall_rating,
  h.mortality_rating,
  h.readmission_rating
FROM network.providers p
JOIN network.hospital_quality h ON p.npi = h.facility_id
WHERE p.state = 'TX'
  AND h.overall_rating >= 4
ORDER BY h.overall_rating DESC;
```

### Provider Count by Specialty

```sql
SELECT 
  primary_taxonomy_code,
  COUNT(*) as provider_count
FROM network.providers
WHERE state = 'NY'
  AND entity_type_code = '1'
GROUP BY primary_taxonomy_code
ORDER BY provider_count DESC
LIMIT 15;
```

---

## Synthetic Generation Examples

When real provider data isn't appropriate (demos, tutorials, testing), generate synthetic providers:

### Generate a Provider for an Encounter

**Prompt**:
```
Generate a synthetic cardiologist for this heart failure patient's encounter
```

**Expected Response**:
```json
{
  "npi": "1999999001",
  "entity_type": "individual",
  "provider": {
    "last_name": "Martinez",
    "first_name": "Elena",
    "credential": "MD, FACC"
  },
  "taxonomy": {
    "code": "207RC0200X",
    "display": "Advanced Heart Failure and Transplant Cardiology"
  },
  "practice_location": {
    "city": "Houston",
    "state": "TX"
  },
  "_synthetic": true
}
```

Note: Synthetic NPIs use the `199XXXXXX` range to distinguish from real NPIs.

---

### Generate a Hospital

**Prompt**:
```
Generate a 200-bed community hospital in suburban Dallas
```

**Expected Response**:
```json
{
  "ccn": "450XXX",
  "npi": "1999999002",
  "facility": {
    "name": "Plano Community Medical Center",
    "type": "Short Term Acute Care Hospital"
  },
  "characteristics": {
    "bed_count": 200,
    "emergency_department": true,
    "trauma_level": null,
    "teaching_hospital": false
  },
  "location": {
    "city": "Plano",
    "state": "TX"
  },
  "_synthetic": true
}
```

---

### Generate a Pharmacy

**Prompt**:
```
Generate a retail pharmacy in San Diego
```

**Expected Response**:
```json
{
  "ncpdp_id": "9999001",
  "npi": "1999999003",
  "pharmacy": {
    "name": "Pacific Coast Pharmacy",
    "type": "Community/Retail Pharmacy"
  },
  "services": {
    "immunizations": true,
    "drive_through": true,
    "24_hour": false
  },
  "location": {
    "city": "San Diego",
    "state": "CA"
  },
  "_synthetic": true
}
```

---

## Cross-Product Integration

### Provider for PatientSim Encounter

**Prompt**:
```
This heart failure patient needs a cardiology referral in Houston. Find a real cardiologist.
```

**Expected Response**:

Found a heart failure specialist for this referral:

**Dr. Michael Chen, MD, FACC, FHFSA**
- NPI: 1234567890
- Specialty: Advanced Heart Failure and Transplant Cardiology
- Practice: Houston Methodist DeBakey Heart Center
- Address: 6550 Fannin St, Houston, TX 77030

This NPI can be used for the referral encounter.

---

### Network Status for MemberSim Claim

**Prompt**:
```
Is NPI 1234567890 in-network for Aetna PPO in Texas?
```

**Expected Response**:

I can verify the provider exists:
- **NPI 1234567890** is a valid cardiologist in Houston, TX

However, network participation (in-network vs out-of-network) depends on the specific health plan's contracts, which aren't in NPPES data. For claims processing:
- Use the NPI for the claim
- Network status would be determined by the payer's provider directory

---

## Domain Knowledge Examples

### Explain Network Types

**Prompt**:
```
Explain the difference between HMO and PPO networks
```

**Expected Response**:

| Aspect | HMO | PPO |
|--------|-----|-----|
| Network Access | Closed - in-network only | Open - any provider |
| Referrals | Required for specialists | Not required |
| PCP Required | Yes | No |
| Out-of-Network | Emergency only | Covered at higher cost |
| Premiums | Lower | Higher |
| Cost Control | Higher | Lower |

---

### Explain Taxonomy Codes

**Prompt**:
```
What taxonomy code is used for interventional cardiologists?
```

**Expected Response**:

**Interventional Cardiology**: `207RC0001X`

Taxonomy hierarchy:
- `207R00000X` - Internal Medicine
  - `207RC0000X` - Cardiovascular Disease
    - `207RC0001X` - Interventional Cardiology
    - `207RC0200X` - Advanced Heart Failure and Transplant Cardiology
    - `207RA0001X` - Clinical Cardiac Electrophysiology

---

## Related Examples

- [PatientSim Examples](patientsim-examples.md) - Clinical encounters using providers
- [MemberSim Examples](membersim-examples.md) - Claims with provider NPIs
- [RxMemberSim Examples](rxmembersim-examples.md) - Pharmacy claims
- [Cross-Domain Examples](cross-domain-examples.md) - Multi-product scenarios

---

*NetworkSim Examples v2.0 - December 2024*
