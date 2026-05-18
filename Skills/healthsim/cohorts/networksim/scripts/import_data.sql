
-- ============================================================================
-- NetworkSim v2.0 Data Import
-- Generated: 2025-12-27 15:28:56
-- ============================================================================

-- Import providers (~8.9M records)
COPY providers (
    npi, entity_type_code, last_name, first_name, middle_name,
    name_prefix, name_suffix, credential, gender, organization_name,
    mailing_address_1, mailing_city, mailing_state, mailing_zip,
    practice_address_1, practice_address_2, practice_city,
    practice_state, practice_zip, phone,
    taxonomy_1, taxonomy_2, taxonomy_3, taxonomy_4, primary_taxonomy_switch,
    enumeration_date, last_update_date, deactivation_date, reactivation_date
)
FROM '/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/processed/nppes_filtered.csv'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- Import facilities (~77K records)  
COPY facilities (ccn, name, city, state, zip, phone, type, subtype, beds)
FROM '/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/processed/facilities.csv'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- Import hospital quality (~5K records)
COPY hospital_quality (
    facility_id, facility_name, city_town, state,
    hospital_overall_rating, hospital_overall_rating_footnote
)
FROM '/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/processed/hospital_quality.csv'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- Import physician quality (~2.8M records)
COPY physician_quality (
    npi, provider_last_name, provider_first_name, provider_middle_name
)
FROM '/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/processed/physician_quality.csv'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- Import AHRF county (~3K records)
COPY ahrf_county (county_fips)
FROM '/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/processed/ahrf_county.csv'
WITH (HEADER TRUE, DELIMITER ',', QUOTE '"');

-- ============================================================================
-- Import Validation Queries
-- ============================================================================

-- Check record counts
SELECT 'providers' as table_name, COUNT(*) as record_count FROM providers
UNION ALL
SELECT 'facilities', COUNT(*) FROM facilities
UNION ALL
SELECT 'hospital_quality', COUNT(*) FROM hospital_quality
UNION ALL
SELECT 'physician_quality', COUNT(*) FROM physician_quality
UNION ALL
SELECT 'ahrf_county', COUNT(*) FROM ahrf_county;

-- Check for NULLs in primary keys
SELECT 'providers_null_npi' as check_name, COUNT(*) as null_count 
FROM providers WHERE npi IS NULL
UNION ALL
SELECT 'facilities_null_ccn', COUNT(*) FROM facilities WHERE ccn IS NULL
UNION ALL
SELECT 'hospital_quality_null_id', COUNT(*) FROM hospital_quality WHERE facility_id IS NULL
UNION ALL
SELECT 'physician_quality_null_npi', COUNT(*) FROM physician_quality WHERE npi IS NULL
UNION ALL
SELECT 'ahrf_county_null_fips', COUNT(*) FROM ahrf_county WHERE county_fips IS NULL;

-- Sample data verification
SELECT 'Sample providers' as description, npi, last_name, first_name, practice_state, taxonomy_1
FROM providers LIMIT 5;

SELECT 'Sample facilities' as description, ccn, name, state, type, beds
FROM facilities LIMIT 5;

-- ============================================================================
-- End of import script
-- ============================================================================
