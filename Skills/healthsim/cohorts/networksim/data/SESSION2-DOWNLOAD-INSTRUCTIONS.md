# Session 2: Supplementary Data Download Instructions

**Required for**: NetworkSim v2.0 Session 2  
**Status**: Manual download required (CMS sites require JavaScript/interaction)  
**Estimated time**: 20-30 minutes

---

## 1. CMS Provider of Services (Hospitals & Facilities)

**What**: Hospitals, SNFs, Home Health, Hospices, etc. (~35K facilities)  
**URL**: https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/provider-of-services-file-hospital-non-hospital-facilities

**Steps**:
1. Visit the URL above
2. Click "Export" button (top right)
3. Select "CSV" format
4. Save as: `cms_pos.csv` in `/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/raw/`

**Expected size**: ~10-20 MB  
**Expected records**: ~35,000 facilities

---

## 2. AHRF (Area Health Resources File) - County Data

**What**: County-level healthcare workforce and demographics (3,143 counties)  
**URL**: https://data.hrsa.gov/data/download

**Steps**:
1. Visit https://data.hrsa.gov/data/download
2. Find "Area Health Resources Files (AHRF)" 
3. Select latest year (2023-2024)
4. Download the CSV version
5. Save as: `ahrf_county.csv` in `/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/raw/`

**Expected size**: ~30-50 MB  
**Expected records**: 3,143 counties

---

## 3. Hospital Compare - Quality Ratings

**What**: Hospital quality star ratings, outcomes, safety measures (~5K hospitals)  
**URL**: https://data.cms.gov/provider-data/dataset/xubh-q36u

**Steps**:
1. Visit the URL above
2. Click "Export" → "CSV"
3. Save as: `hospital_compare.csv` in `/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/raw/`

**Expected size**: ~5-10 MB  
**Expected records**: ~4,500 hospitals

---

## 4. Physician Compare - Provider Quality

**What**: Individual physician performance and quality measures (~1M providers)  
**URL**: https://data.cms.gov/provider-data/dataset/mj5m-pzi6

**Steps**:
1. Visit the URL above  
2. Click "Export" → "CSV"
3. Save as: `physician_compare.csv` in `/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/raw/`

**Expected size**: ~50-100 MB  
**Expected records**: ~1M providers

---

## Alternative: Simplified Approach

If any of these datasets are difficult to download, we can proceed without them for now and add them later. The **minimum required** for Session 3 is:

✅ **NPPES data** (already have - 8.9M providers)  
🔲 CMS POS (nice to have - can add later)  
🔲 AHRF (nice to have - can add later)  
🔲 Hospital Compare (nice to have - can add later)  
🔲 Physician Compare (nice to have - can add later)

We can proceed with just NPPES and create the DuckDB schema, then add supplementary data in future sessions if needed.

---

## Verification

After downloading, run this to check file sizes:

```bash
cd /Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim/data/raw
ls -lh cms_pos.csv ahrf_county.csv hospital_compare.csv physician_compare.csv
```

Expected output:
```
-rw-r--r--  cms_pos.csv           ~10-20 MB
-rw-r--r--  ahrf_county.csv       ~30-50 MB  
-rw-r--r--  hospital_compare.csv   ~5-10 MB
-rw-r--r--  physician_compare.csv ~50-100 MB
```

**Once downloaded**, let Claude know and we'll proceed with processing scripts!
