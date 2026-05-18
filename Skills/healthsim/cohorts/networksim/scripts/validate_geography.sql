-- Geographic Validation Queries for NetworkSim v2.0
-- Run these queries to verify geographic data quality

-- ===================================================================
-- 1. Provider Geographic Coverage Summary
-- ===================================================================
SELECT 
    'Total Providers' as metric,
    COUNT(*) as count,
    COUNT(DISTINCT practice_state) as states,
    COUNT(DISTINCT county_fips) as counties,
    ROUND(100.0 * COUNT(county_fips) / COUNT(*), 2) as pct_with_fips
FROM network.providers;

-- ===================================================================
-- 2. County Coverage Comparison with PopulationSim
-- ===================================================================
SELECT 
    'PopulationSim Counties' as source,
    COUNT(DISTINCT countyfips) as county_count
FROM population.places_county
UNION ALL
SELECT 
    'NetworkSim Counties' as source,
    COUNT(DISTINCT county_fips) as county_count
FROM network.providers
WHERE county_fips IS NOT NULL;

-- ===================================================================
-- 3. State Coverage Analysis
-- ===================================================================
SELECT 
    practice_state as state,
    COUNT(*) as provider_count,
    COUNT(county_fips) as with_fips,
    ROUND(100.0 * COUNT(county_fips) / COUNT(*), 2) as pct_coverage
FROM network.providers
GROUP BY practice_state
ORDER BY provider_count DESC
LIMIT 20;

-- ===================================================================
-- 4. Missing County FIPS by State
-- ===================================================================
SELECT 
    practice_state as state,
    COUNT(*) as providers_missing_fips,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct_of_missing
FROM network.providers
WHERE county_fips IS NULL
GROUP BY practice_state
ORDER BY providers_missing_fips DESC
LIMIT 10;

-- ===================================================================
-- 5. Verify Cross-Product Join Capability (Top 10 Counties)
-- ===================================================================
SELECT 
    p.countyname,
    p.stateabbr,
    p.diabetes_crudeprev as diabetes_rate,
    COUNT(n.npi) as provider_count
FROM population.places_county p
LEFT JOIN network.providers n ON p.countyfips = n.county_fips
GROUP BY p.countyname, p.stateabbr, p.diabetes_crudeprev
ORDER BY provider_count DESC
LIMIT 10;

-- ===================================================================
-- 6. Healthcare Deserts Analysis (Preview)
-- ===================================================================
SELECT 
    p.countyname,
    p.stateabbr,
    p.e_totpop as population,
    COUNT(n.npi) as provider_count,
    ROUND(1000.0 * COUNT(n.npi) / NULLIF(p.e_totpop, 0), 2) as providers_per_1000
FROM population.svi_county p
LEFT JOIN network.providers n ON p.fips = n.county_fips
WHERE p.e_totpop > 0
GROUP BY p.countyname, p.stateabbr, p.e_totpop
HAVING COUNT(n.npi) < 10  -- Very few providers
ORDER BY p.e_totpop DESC
LIMIT 10;

-- ===================================================================
-- 7. Facility Geographic Coverage
-- ===================================================================
SELECT 
    'Total Facilities' as metric,
    COUNT(*) as count,
    COUNT(DISTINCT state) as states,
    COUNT(DISTINCT county_fips) as counties
FROM network.facilities;
