#!/usr/bin/env python3
"""
NPPES Data Filtering Script
Filters NPPES NPI Registry to active US-based providers
Reduces from ~6.5M to ~3M records
"""

import pandas as pd
import sys
from pathlib import Path

def filter_nppes(input_file, output_file):
    """
    Filter NPPES data to active US providers only
    
    Args:
        input_file: Path to raw NPPES CSV file
        output_file: Path for filtered output CSV
    """
    print("=" * 80)
    print("NPPES Data Filtering")
    print("=" * 80)
    
    # Load full file
    print(f"\n1. Loading data from: {input_file}")
    print("   (This may take several minutes...)")
    
    try:
        df = pd.read_csv(input_file, dtype=str, low_memory=False)
        print(f"   ✓ Loaded {len(df):,} total records")
        print(f"   ✓ Columns: {len(df.columns)}")
    except FileNotFoundError:
        print(f"   ✗ ERROR: File not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        sys.exit(1)
    
    # Apply filters
    print("\n2. Applying filters...")
    
    original_count = len(df)
    
    # Filter 1: Active providers only (no deactivation date)
    print("   - Filter: Active providers only (NPI Deactivation Date IS NULL)")
    df = df[df['NPI Deactivation Date'].isna()]
    print(f"     After filter: {len(df):,} records ({len(df)/original_count*100:.1f}%)")
    
    # Filter 2: US-based only (keep NULL or 'US')
    print("   - Filter: US-based providers only")
    country_col = 'Provider Business Practice Location Address Country Code (If outside U.S.)'
    df = df[(df[country_col].isna()) | (df[country_col] == 'US')]
    print(f"     After filter: {len(df):,} records ({len(df)/original_count*100:.1f}%)")
    
    # Filter 3: Has valid taxonomy code
    print("   - Filter: Has valid Healthcare Provider Taxonomy Code")
    df = df[df['Healthcare Provider Taxonomy Code_1'].notna()]
    print(f"     After filter: {len(df):,} records ({len(df)/original_count*100:.1f}%)")
    
    # Select key fields (35 of 330 columns)
    print("\n3. Selecting key fields (35 of 330 columns)...")
    
    columns = [
        'NPI',
        'Entity Type Code',
        'Provider Last Name (Legal Name)',
        'Provider First Name',
        'Provider Middle Name',
        'Provider Name Prefix Text',
        'Provider Name Suffix Text',
        'Provider Credential Text',
        'Provider Gender Code',
        'Provider Organization Name (Legal Business Name)',
        'Provider First Line Business Mailing Address',
        'Provider Business Mailing Address City Name',
        'Provider Business Mailing Address State Name',
        'Provider Business Mailing Address Postal Code',
        'Provider First Line Business Practice Location Address',
        'Provider Second Line Business Practice Location Address',
        'Provider Business Practice Location Address City Name',
        'Provider Business Practice Location Address State Name',
        'Provider Business Practice Location Address Postal Code',
        'Provider Business Practice Location Address Telephone Number',
        'Healthcare Provider Taxonomy Code_1',
        'Healthcare Provider Taxonomy Code_2',
        'Healthcare Provider Taxonomy Code_3',
        'Healthcare Provider Taxonomy Code_4',
        'Healthcare Provider Primary Taxonomy Switch_1',
        'Provider Enumeration Date',
        'Last Update Date',
        'NPI Deactivation Date',
        'NPI Reactivation Date',
    ]
    
    # Only select columns that exist
    available_columns = [col for col in columns if col in df.columns]
    df_filtered = df[available_columns].copy()
    
    print(f"   ✓ Selected {len(available_columns)} columns")
    
    # Rename columns to simpler names
    print("\n4. Renaming columns...")
    column_mapping = {
        'Provider Last Name (Legal Name)': 'last_name',
        'Provider First Name': 'first_name',
        'Provider Middle Name': 'middle_name',
        'Provider Name Prefix Text': 'name_prefix',
        'Provider Name Suffix Text': 'name_suffix',
        'Provider Credential Text': 'credential',
        'Provider Gender Code': 'gender',
        'Provider Organization Name (Legal Business Name)': 'organization_name',
        'Provider First Line Business Mailing Address': 'mailing_address_1',
        'Provider Business Mailing Address City Name': 'mailing_city',
        'Provider Business Mailing Address State Name': 'mailing_state',
        'Provider Business Mailing Address Postal Code': 'mailing_zip',
        'Provider First Line Business Practice Location Address': 'practice_address_1',
        'Provider Second Line Business Practice Location Address': 'practice_address_2',
        'Provider Business Practice Location Address City Name': 'practice_city',
        'Provider Business Practice Location Address State Name': 'practice_state',
        'Provider Business Practice Location Address Postal Code': 'practice_zip',
        'Provider Business Practice Location Address Telephone Number': 'phone',
        'Healthcare Provider Taxonomy Code_1': 'taxonomy_1',
        'Healthcare Provider Taxonomy Code_2': 'taxonomy_2',
        'Healthcare Provider Taxonomy Code_3': 'taxonomy_3',
        'Healthcare Provider Taxonomy Code_4': 'taxonomy_4',
        'Healthcare Provider Primary Taxonomy Switch_1': 'primary_taxonomy_switch',
        'Provider Enumeration Date': 'enumeration_date',
        'Last Update Date': 'last_update_date',
        'NPI Deactivation Date': 'deactivation_date',
        'NPI Reactivation Date': 'reactivation_date',
    }
    
    df_filtered = df_filtered.rename(columns=column_mapping)
    
    # Standardize column names
    df_filtered.columns = [col.upper() if col == 'NPI' or col.startswith('Entity') 
                           else col.lower() 
                           for col in df_filtered.columns]
    
    # Save filtered data
    print(f"\n5. Saving filtered data to: {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_filtered.to_csv(output_file, index=False)
    
    # Summary
    print("\n" + "=" * 80)
    print("FILTERING COMPLETE")
    print("=" * 80)
    print(f"Original records:  {original_count:>12,}")
    print(f"Filtered records:  {len(df_filtered):>12,}")
    print(f"Reduction:         {(1 - len(df_filtered)/original_count)*100:>11.1f}%")
    print(f"Output file:       {output_file}")
    print(f"File size:         ~{output_file.stat().st_size / (1024**2):.1f} MB")
    print("=" * 80)
    
    return df_filtered

if __name__ == "__main__":
    # Paths
    base_dir = Path(__file__).parent.parent
    
    # Look for the NPPES CSV file (filename includes date range)
    # Exclude header files
    raw_dir = base_dir / "data/raw"
    nppes_files = [f for f in raw_dir.glob("npidata_pfile_*.csv") 
                   if "_fileheader" not in f.name]
    
    if not nppes_files:
        print("ERROR: No NPPES data file found in data/raw/")
        print("Looking for: npidata_pfile_*.csv (excluding fileheader)")
        sys.exit(1)
    
    input_file = nppes_files[0]  # Use the first (should be only) match
    output_file = base_dir / "data/processed/nppes_filtered.csv"
    
    # Run filtering
    filter_nppes(input_file, output_file)
