#!/usr/bin/env python3
"""
Process Supplementary Data for NetworkSim v2.0
Cleans and prepares CMS POS, Hospital Compare, Physician Compare, and AHRF data
"""

import pandas as pd
import sys
from pathlib import Path

def process_pos_facilities(raw_dir, processed_dir):
    """
    Process CMS Provider of Services file
    Extract key facility information
    """
    print("\n" + "=" * 80)
    print("PROCESSING: CMS Provider of Services (Facilities)")
    print("=" * 80)
    
    pos_file = raw_dir / "POS_File_QIES_Q3_2025.csv"
    
    print(f"Reading: {pos_file}")
    df = pd.read_csv(pos_file, dtype=str, low_memory=False)
    
    print(f"  Total records: {len(df):,}")
    print(f"  Total columns: {len(df.columns):,}")
    
    # Select key columns (using actual column names from the file)
    # Note: Column names in POS files are often abbreviated
    key_columns = []
    
    # Try to find standard columns (exact names may vary)
    possible_columns = {
        'ccn': ['PRVDR_NUM', 'CCN', 'PROVIDER_NUMBER'],
        'name': ['PROVIDER_NAME', 'FAC_NAME', 'NAME'],
        'address': ['STREET_ADDR', 'ADDRESS', 'ADDR_1'],
        'city': ['CITY_NAME', 'CITY'],
        'state': ['STATE_CD', 'STATE', 'STATE_CODE'],
        'zip': ['ZIP_CD', 'ZIP', 'ZIP_CODE'],
        'county': ['COUNTY_NAME', 'COUNTY', 'CNTY_NAME'],
        'phone': ['PHNE_NUM', 'PHONE', 'PHONE_NUMBER'],
        'type': ['PRVDR_CTGRY_CD', 'PROVIDER_TYPE', 'TYPE_CODE'],
        'subtype': ['PRVDR_CTGRY_SBTYP_CD', 'PROVIDER_SUBTYPE'],
        'beds': ['BED_CNT', 'CRTFD_BED_CNT', 'BEDS']
    }
    
    # Build column mapping
    column_mapping = {}
    for std_name, variants in possible_columns.items():
        for variant in variants:
            if variant in df.columns:
                column_mapping[variant] = std_name
                key_columns.append(variant)
                break
    
    if not key_columns:
        print("  ✗ ERROR: Could not find standard columns")
        print("  Sample columns:", list(df.columns[:10]))
        return False
    
    print(f"  Mapping {len(key_columns)} columns")
    
    # Select and rename
    df_clean = df[key_columns].copy()
    df_clean = df_clean.rename(columns=column_mapping)
    
    # Add standard columns if missing
    for col in ['ccn', 'name', 'city', 'state']:
        if col not in df_clean.columns:
            df_clean[col] = None
    
    # Save
    output_file = processed_dir / "facilities.csv"
    df_clean.to_csv(output_file, index=False)
    
    print(f"  ✓ Processed: {len(df_clean):,} facilities")
    print(f"  ✓ Saved: {output_file}")
    print(f"  Columns: {list(df_clean.columns)}")
    
    return True

def process_hospital_compare(raw_dir, processed_dir):
    """
    Process Hospital Compare quality ratings
    """
    print("\n" + "=" * 80)
    print("PROCESSING: Hospital Compare Quality Ratings")
    print("=" * 80)
    
    hc_file = raw_dir / "Hospital_General_Information.csv"
    
    print(f"Reading: {hc_file}")
    df = pd.read_csv(hc_file, dtype=str)
    
    print(f"  Total records: {len(df):,}")
    print(f"  Columns: {list(df.columns[:10])}")
    
    # Select key quality columns
    key_columns = ['Facility ID', 'Facility Name', 'City/Town', 'State']
    
    # Add rating columns if they exist
    rating_cols = [col for col in df.columns if 'rating' in col.lower() or 'score' in col.lower()]
    key_columns.extend(rating_cols[:5])  # Top 5 rating columns
    
    available_columns = [col for col in key_columns if col in df.columns]
    df_clean = df[available_columns].copy()
    
    # Standardize column names
    df_clean.columns = [col.lower().replace('/', '_').replace(' ', '_') for col in df_clean.columns]
    
    # Save
    output_file = processed_dir / "hospital_quality.csv"
    df_clean.to_csv(output_file, index=False)
    
    print(f"  ✓ Processed: {len(df_clean):,} hospitals")
    print(f"  ✓ Saved: {output_file}")
    print(f"  Columns: {list(df_clean.columns)}")
    
    return True

def process_physician_compare(raw_dir, processed_dir):
    """
    Process Physician Compare quality data
    """
    print("\n" + "=" * 80)
    print("PROCESSING: Physician Compare Quality Data")
    print("=" * 80)
    
    pc_file = raw_dir / "DAC_NationalDownloadableFile.csv"
    
    print(f"Reading: {pc_file} (this may take a minute...)")
    df = pd.read_csv(pc_file, dtype=str, low_memory=False)
    
    print(f"  Total records: {len(df):,}")
    print(f"  Sample columns: {list(df.columns[:10])}")
    
    # Select key columns
    key_columns = ['NPI']
    
    # Add name columns
    name_cols = [col for col in df.columns if 'name' in col.lower() or 'first' in col.lower() or 'last' in col.lower()]
    key_columns.extend(name_cols[:3])
    
    # Add quality/performance columns
    quality_cols = [col for col in df.columns if any(x in col.lower() for x in ['score', 'rating', 'quality', 'performance', 'mips'])]
    key_columns.extend(quality_cols[:5])
    
    available_columns = [col for col in key_columns if col in df.columns]
    df_clean = df[available_columns].copy()
    
    # Standardize column names
    df_clean.columns = [col.lower().replace('/', '_').replace(' ', '_') for col in df_clean.columns]
    
    # Save
    output_file = processed_dir / "physician_quality.csv"
    df_clean.to_csv(output_file, index=False)
    
    print(f"  ✓ Processed: {len(df_clean):,} physicians")
    print(f"  ✓ Saved: {output_file}")
    print(f"  Columns: {list(df_clean.columns)}")
    
    return True

def process_ahrf_county(raw_dir, processed_dir):
    """
    Process AHRF county-level healthcare resources
    """
    print("\n" + "=" * 80)
    print("PROCESSING: AHRF County Healthcare Resources")
    print("=" * 80)
    
    ahrf_file = raw_dir / "NCHWA-2024-2025+AHRF+COUNTY+CSV/AHRF2025.csv"
    
    print(f"Reading: {ahrf_file}")
    df = pd.read_csv(ahrf_file, dtype=str, low_memory=False)
    
    print(f"  Total records: {len(df):,}")
    print(f"  Total columns: {len(df.columns):,} (will select subset)")
    
    # AHRF has thousands of columns - select key ones
    # Common AHRF field codes (check actual file for exact names)
    key_fields = {
        'fips_st_cnty': 'county_fips',  # County FIPS code
        'f00002': 'county_name',         # County name
        'f00010': 'state_abbr',          # State abbreviation
    }
    
    # Try to find these columns
    available_fields = {}
    for old_name, new_name in key_fields.items():
        if old_name in df.columns:
            available_fields[old_name] = new_name
        else:
            # Try variations
            for col in df.columns:
                if old_name.lower() in col.lower():
                    available_fields[col] = new_name
                    break
    
    if not available_fields:
        print("  ✗ ERROR: Could not find FIPS or county name columns")
        print("  Sample columns:", list(df.columns[:20]))
        return False
    
    # Select available columns
    df_clean = df[list(available_fields.keys())].copy()
    df_clean = df_clean.rename(columns=available_fields)
    
    # Save
    output_file = processed_dir / "ahrf_county.csv"
    df_clean.to_csv(output_file, index=False)
    
    print(f"  ✓ Processed: {len(df_clean):,} counties")
    print(f"  ✓ Saved: {output_file}")
    print(f"  Columns: {list(df_clean.columns)}")
    
    return True

def main():
    """
    Process all supplementary data files
    """
    base_dir = Path(__file__).parent.parent
    raw_dir = base_dir / "data/raw"
    processed_dir = base_dir / "data/processed"
    
    print("=" * 80)
    print("SUPPLEMENTARY DATA PROCESSING")
    print("=" * 80)
    print(f"Raw directory: {raw_dir}")
    print(f"Processed directory: {processed_dir}")
    
    # Process each dataset
    results = {
        'Facilities': process_pos_facilities(raw_dir, processed_dir),
        'Hospital Quality': process_hospital_compare(raw_dir, processed_dir),
        'Physician Quality': process_physician_compare(raw_dir, processed_dir),
        'AHRF County': process_ahrf_county(raw_dir, processed_dir)
    }
    
    # Summary
    print("\n" + "=" * 80)
    print("PROCESSING SUMMARY")
    print("=" * 80)
    
    for name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{name:.<40} {status}")
    
    all_success = all(results.values())
    
    if all_success:
        print("\n✓ All supplementary data processed successfully!")
        print(f"\nProcessed files in: {processed_dir}")
        return 0
    else:
        print("\n✗ Some files failed to process")
        return 1

if __name__ == "__main__":
    sys.exit(main())
