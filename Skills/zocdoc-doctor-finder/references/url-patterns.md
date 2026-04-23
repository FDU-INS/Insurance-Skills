# Zocdoc URL Patterns

## Search URL

```
https://www.zocdoc.com/search?
  address=Chicago%2C%20IL        # URL-encoded city, state or zip
  &dr_specialty=153               # Specialty ID (required for specialty search)
  &insurance_carrier=Aetna        # Carrier name (empty = no filter)
  &insurance_plan=-1              # Plan ID (-1 = any plan from carrier)
  &day_filter=AnyDay              # AnyDay | Today | Tomorrow | NextWeek
  &sort_type=Default              # Default | Distance
  &visitType=inPersonAndVirtualVisits  # inPersonAndVirtualVisits | virtualVisits | inPersonVisits
  &after_5pm=false                # Evening appointments
  &before_10am=false              # Morning appointments
  &gender=-1                      # -1 = any, 1 = female, 2 = male
  &language=-1                    # -1 = any, or language ID
  &offset=0                       # Pagination (0-indexed page number)
  &reason_visit=75                # Visit reason ID (75 = general/new patient)
  &sees_children=false            # Pediatric filter
  &searchType=specialty           # specialty | condition
  &filters={}                     # JSON object for advanced filters
```

### Advanced Filters (JSON in `filters` param)

```
{"sp_top_rated":["is_highly_recommended"]}    # Highly recommended only
{"sp_wait_times":["has_low_wait_times"]}      # Excellent wait time only
```

### Search by condition (alternative to specialty)

Navigate to zocdoc.com and type the condition (e.g., "acne", "back pain") into the search combobox. Select from autocomplete — Zocdoc maps conditions to the correct specialties and sets appropriate URL params.

## Provider Profile URL

```
https://www.zocdoc.com/doctor/<name-slug>-<id>
```

Example: `https://www.zocdoc.com/doctor/laurence-gordon-do-491327`

### Profile URL Query Parameters

```
?LocIdent=258139          # Specific office location ID
&reason_visit=75          # Visit reason
&insuranceCarrier=Aetna   # Pre-fill insurance
&insurancePlan=-1         # Plan ID
&dr_specialty=153         # Specialty context
&isNewPatient=true        # New vs existing patient
```

## Common Specialty IDs

| Specialty | ID |
|-----------|-----|
| Primary Care Doctor | 153 |
| Dentist | 98 |
| OB-GYN | 133 |
| Dermatologist | 105 |
| Psychiatrist | 319 |
| Eye Doctor | 113 |
| Ear, Nose & Throat Doctor | 7 |
| Orthopedic Surgeon | 141 |
| Cardiologist | 47 |
| Gastroenterologist | 117 |
| Pediatrician | 149 |
| Urologist | 179 |
| Psychologist | 319 |
| Chiropractor | 230 |
| Urgent Care | 702 |
| Allergist | 1 |
| Endocrinologist | 9 |
| Neurologist | 129 |
| Pulmonologist | 159 |
| Podiatrist | 155 |
| Physical Therapist | 236 |
| Ophthalmologist | 139 |
| Plastic Surgeon | 155 |
| Rheumatologist | 163 |

> **Note:** If a specialty ID is unknown or the user describes a condition rather than a specialty, use the homepage search autocomplete to find the right mapping. Zocdoc handles condition→specialty routing internally.

## SEO / Friendly URLs

Use friendly specialty URLs as an alternative to parameterized search:

```
https://www.zocdoc.com/primary-care-doctors
https://www.zocdoc.com/dentists
https://www.zocdoc.com/dermatologists
https://www.zocdoc.com/obgyns
https://www.zocdoc.com/psychiatrists
https://www.zocdoc.com/eye-doctors
```

These redirect to the search page with appropriate filters applied.

## Insurance Carriers Page

```
https://www.zocdoc.com/specialty/insurances/primary-care-doctors
```

Use this to look up supported insurance carriers for a given specialty.

## Pagination

Paginate search results with `offset=N` (0-indexed page number). Each page returns ~20 results.

Example page 2: `&offset=1`

## Visit Reason IDs

| Reason | ID |
|--------|-----|
| New patient visit / general | 75 |

> Visit reasons vary by specialty. Check the "Choose a visit reason" dropdown on the provider profile for available options.
