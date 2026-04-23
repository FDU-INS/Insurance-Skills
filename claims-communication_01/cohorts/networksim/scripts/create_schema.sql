-- NetworkSim v2.0 DuckDB Schema
-- Creates 5 tables in existing healthsim.duckdb
-- Designed to integrate with PopulationSim reference tables

-- ============================================================================
-- TABLE 1: providers
-- ============================================================================
-- Primary provider registry from NPPES
-- ~8.9M active US healthcare providers

CREATE TABLE IF NOT EXISTS providers (
    -- Identity
    npi VARCHAR(10) PRIMARY KEY,
    entity_type_code VARCHAR(1) NOT NULL,  -- '1'=Individual, '2'=Organization
    
    -- Individual Names
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    middle_name VARCHAR(50),
    name_prefix VARCHAR(10),
    name_suffix VARCHAR(10),
    credential VARCHAR(50),
    gender VARCHAR(1),
    
    -- Organization Name
    organization_name VARCHAR(255),
    
    -- Mailing Address
    mailing_address_1 VARCHAR(255),
    mailing_city VARCHAR(100),
    mailing_state VARCHAR(2),
    mailing_zip VARCHAR(10),
    
    -- Practice Location
    practice_address_1 VARCHAR(255),
    practice_address_2 VARCHAR(100),
    practice_city VARCHAR(100),
    practice_state VARCHAR(2),
    practice_zip VARCHAR(10),
    phone VARCHAR(20),
    
    -- Taxonomy (Specialty)
    taxonomy_1 VARCHAR(10),
    taxonomy_2 VARCHAR(10),
    taxonomy_3 VARCHAR(10),
    taxonomy_4 VARCHAR(10),
    primary_taxonomy_switch VARCHAR(1),
    
    -- Dates
    enumeration_date DATE,
    last_update_date DATE,
    deactivation_date DATE,
    reactivation_date DATE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE providers IS 'NPPES National Provider Identifier registry - active US healthcare providers';
COMMENT ON COLUMN providers.npi IS '10-digit National Provider Identifier (unique)';
COMMENT ON COLUMN providers.entity_type_code IS '1=Individual provider, 2=Organization';
COMMENT ON COLUMN providers.taxonomy_1 IS 'Primary specialty taxonomy code (NUCC standard)';

-- ============================================================================
-- TABLE 2: facilities
-- ============================================================================
-- CMS Provider of Services - hospitals, SNFs, home health, hospices, etc.
-- ~77K healthcare facilities

CREATE TABLE IF NOT EXISTS facilities (
    -- Identity
    ccn VARCHAR(10) PRIMARY KEY,  -- CMS Certification Number
    name VARCHAR(255),
    
    -- Location
    city VARCHAR(100),
    state VARCHAR(2),
    zip VARCHAR(10),
    phone VARCHAR(20),
    
    -- Classification
    type VARCHAR(50),
    subtype VARCHAR(50),
    beds INTEGER,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE facilities IS 'CMS Provider of Services file - Medicare/Medicaid certified facilities';
COMMENT ON COLUMN facilities.ccn IS 'CMS Certification Number (CCN)';
COMMENT ON COLUMN facilities.type IS 'Facility category code';
COMMENT ON COLUMN facilities.beds IS 'Licensed/certified bed count';

-- ============================================================================
-- TABLE 3: hospital_quality
-- ============================================================================
-- Hospital Compare quality ratings and measures
-- ~5K hospitals with quality data

CREATE TABLE IF NOT EXISTS hospital_quality (
    -- Identity
    facility_id VARCHAR(10) PRIMARY KEY,  -- Links to facilities.ccn
    facility_name VARCHAR(255),
    city_town VARCHAR(100),
    state VARCHAR(2),
    
    -- Quality Ratings
    hospital_overall_rating VARCHAR(10),
    hospital_overall_rating_footnote VARCHAR(255),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE hospital_quality IS 'CMS Hospital Compare quality ratings and star ratings';
COMMENT ON COLUMN hospital_quality.hospital_overall_rating IS 'Overall hospital star rating (1-5)';

-- ============================================================================
-- TABLE 4: physician_quality
-- ============================================================================
-- Physician Compare quality and performance data
-- ~2.8M physicians with quality measures

CREATE TABLE IF NOT EXISTS physician_quality (
    -- Identity
    npi VARCHAR(10) PRIMARY KEY,  -- Links to providers.npi
    provider_last_name VARCHAR(100),
    provider_first_name VARCHAR(100),
    provider_middle_name VARCHAR(50),
    
    -- Quality measures would go here
    -- (Current file has limited quality columns)
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE physician_quality IS 'CMS Physician Compare quality and performance measures';
COMMENT ON COLUMN physician_quality.npi IS 'Links to providers.npi for quality enrichment';

-- ============================================================================
-- TABLE 5: ahrf_county
-- ============================================================================
-- Area Health Resources File - county-level healthcare resources
-- 3,235 US counties

CREATE TABLE IF NOT EXISTS ahrf_county (
    -- Identity
    county_fips VARCHAR(5) PRIMARY KEY,
    
    -- Basic fields (AHRF has 4,352 columns - selecting subset later)
    -- Will be enriched in Session 4 with additional fields
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE ahrf_county IS 'HRSA Area Health Resources File - county-level healthcare workforce and resources';
COMMENT ON COLUMN ahrf_county.county_fips IS '5-digit FIPS code (state+county) - links to PopulationSim tables';

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Provider indexes
CREATE INDEX IF NOT EXISTS idx_providers_state ON providers(practice_state);
CREATE INDEX IF NOT EXISTS idx_providers_zip ON providers(practice_zip);
CREATE INDEX IF NOT EXISTS idx_providers_taxonomy ON providers(taxonomy_1);
CREATE INDEX IF NOT EXISTS idx_providers_type ON providers(entity_type_code);
CREATE INDEX IF NOT EXISTS idx_providers_name ON providers(last_name, first_name);

-- Facility indexes
CREATE INDEX IF NOT EXISTS idx_facilities_state ON facilities(state);
CREATE INDEX IF NOT EXISTS idx_facilities_type ON facilities(type);
CREATE INDEX IF NOT EXISTS idx_facilities_name ON facilities(name);

-- Quality indexes
CREATE INDEX IF NOT EXISTS idx_hospital_quality_state ON hospital_quality(state);
CREATE INDEX IF NOT EXISTS idx_hospital_quality_rating ON hospital_quality(hospital_overall_rating);

-- Cross-product join optimization
CREATE INDEX IF NOT EXISTS idx_physician_quality_npi ON physician_quality(npi);

-- ============================================================================
-- COMMENTS AND DOCUMENTATION
-- ============================================================================

COMMENT ON INDEX idx_providers_state IS 'Fast state-based provider searches';
COMMENT ON INDEX idx_providers_taxonomy IS 'Fast specialty-based provider searches';
COMMENT ON INDEX idx_providers_zip IS 'Geographic proximity searches';
