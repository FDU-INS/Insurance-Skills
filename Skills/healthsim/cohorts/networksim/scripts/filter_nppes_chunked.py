#!/usr/bin/env python3
"""
NPPES Data Filtering Script - CHUNKED VERSION
Processes data in chunks to avoid memory issues
"""

import pandas as pd
import sys
from pathlib import Path

def filter_nppes_chunked(input_file, output_file, chunksize=100000):
    """
    Filter NPPES data in chunks to avoid memory issues
    """
    print("=" * 80)
    print("NPPES Data Filtering (CHUNKED)")
    print("=" * 80)
    print(f"\nProcessing in chunks of {chunksize:,} records")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print()
    
    # Columns we want to keep
    columns_to_keep = [
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
    
    # Column renaming
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
    
    total_input = 0
    total_output = 0
    chunk_num = 0
    first_chunk = True
    
    country_col = 'Provider Business Practice Location Address Country Code (If outside U.S.)'
    
    print("Starting chunked processing...")
    print()
    
    try:
        # Process file in chunks
        for chunk in pd.read_csv(input_file, dtype=str, low_memory=False, chunksize=chunksize):
            chunk_num += 1
            chunk_input_count = len(chunk)
            total_input += chunk_input_count
            
            # Apply filters
            # Filter 1: Active providers only
            chunk = chunk[chunk['NPI Deactivation Date'].isna()]
            
            # Filter 2: US-based only (NULL or 'US')
            chunk = chunk[(chunk[country_col].isna()) | (chunk[country_col] == 'US')]
            
            # Filter 3: Has valid taxonomy code
            chunk = chunk[chunk['Healthcare Provider Taxonomy Code_1'].notna()]
            
            # Select only the columns we want
            available_columns = [col for col in columns_to_keep if col in chunk.columns]
            chunk = chunk[available_columns]
            
            # Rename columns
            chunk = chunk.rename(columns=column_mapping)
            
            # Standardize column names (uppercase NPI and Entity Type Code)
            chunk.columns = [col.upper() if col in ['npi', 'entity_type_code'] 
                           else col for col in chunk.columns]
            
            chunk_output_count = len(chunk)
            total_output += chunk_output_count
            
            # Write to output
            if first_chunk:
                chunk.to_csv(output_file, index=False, mode='w')
                first_chunk = False
            else:
                chunk.to_csv(output_file, index=False, mode='a', header=False)
            
            # Progress update
            print(f"Chunk {chunk_num:>4}: Processed {chunk_input_count:>7,} → Kept {chunk_output_count:>7,} | Total: {total_input:>10,} → {total_output:>10,}")
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False
    
    # Summary
    print()
    print("=" * 80)
    print("FILTERING COMPLETE")
    print("=" * 80)
    print(f"Original records:  {total_input:>12,}")
    print(f"Filtered records:  {total_output:>12,}")
    print(f"Reduction:         {(1 - total_output/total_input)*100:>11.1f}%")
    print(f"Output file:       {output_file}")
    
    if output_file.exists():
        size_mb = output_file.stat().st_size / (1024**2)
        print(f"File size:         {size_mb:>11.1f} MB")
    
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    raw_dir = base_dir / "data/raw"
    
    # Find NPPES file
    nppes_files = [f for f in raw_dir.glob("npidata_pfile_*.csv") 
                   if "_fileheader" not in f.name]
    
    if not nppes_files:
        print("ERROR: No NPPES data file found in data/raw/")
        print("Looking for: npidata_pfile_*.csv (excluding fileheader)")
        sys.exit(1)
    
    input_file = nppes_files[0]
    output_file = base_dir / "data/processed/nppes_filtered.csv"
    
    # Run chunked filtering
    success = filter_nppes_chunked(input_file, output_file, chunksize=100000)
    
    sys.exit(0 if success else 1)
