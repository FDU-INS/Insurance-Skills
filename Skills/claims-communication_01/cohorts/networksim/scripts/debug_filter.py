#!/usr/bin/env python3
"""
Debug NPPES filtering to see what's going wrong
"""

import pandas as pd
from pathlib import Path

base_dir = Path("/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim")
input_file = base_dir / "data/raw/npidata_pfile_20050523-20251207.csv"

print("=" * 80)
print("NPPES FILTERING DIAGNOSTIC")
print("=" * 80)

# Read just first 1000 rows to test
print("\nLoading first 1000 rows...")
df = pd.read_csv(input_file, dtype=str, low_memory=False, nrows=1000)
print(f"✓ Loaded {len(df)} rows")
print(f"✓ Columns: {len(df.columns)}")

# Check the filter columns
print("\n" + "=" * 80)
print("CHECKING FILTER COLUMNS")
print("=" * 80)

# Column 1: NPI Deactivation Date
col1 = 'NPI Deactivation Date'
if col1 in df.columns:
    print(f"\n✓ Column '{col1}' exists")
    null_count = df[col1].isna().sum()
    print(f"  Null values: {null_count}/{len(df)} ({null_count/len(df)*100:.1f}%)")
    print(f"  Sample values: {df[col1].dropna().head(3).tolist()}")
else:
    print(f"\n✗ Column '{col1}' NOT FOUND")

# Column 2: Country Code
col2 = 'Provider Business Practice Location Address Country Code (If outside U.S.)'
if col2 in df.columns:
    print(f"\n✓ Column '{col2}' exists")
    null_count = df[col2].isna().sum()
    print(f"  Null values: {null_count}/{len(df)} ({null_count/len(df)*100:.1f}%)")
    print(f"  Non-null values: {df[col2].notna().sum()}")
    print(f"  Sample values: {df[col2].dropna().head(3).tolist()}")
else:
    print(f"\n✗ Column '{col2}' NOT FOUND")

# Column 3: Taxonomy Code
col3 = 'Healthcare Provider Taxonomy Code_1'
if col3 in df.columns:
    print(f"\n✓ Column '{col3}' exists")
    null_count = df[col3].isna().sum()
    not_null = df[col3].notna().sum()
    print(f"  Not null values: {not_null}/{len(df)} ({not_null/len(df)*100:.1f}%)")
    print(f"  Sample values: {df[col3].dropna().head(3).tolist()}")
else:
    print(f"\n✗ Column '{col3}' NOT FOUND")

# Test the filters
print("\n" + "=" * 80)
print("TESTING FILTERS")
print("=" * 80)

original = len(df)
print(f"\nOriginal rows: {original}")

# Filter 1: Active only
filtered = df[df[col1].isna()]
print(f"\nAfter Filter 1 (Active only): {len(filtered)} rows ({len(filtered)/original*100:.1f}%)")

# Filter 2: US only
filtered = filtered[filtered[col2].isna()]
print(f"After Filter 2 (US only): {len(filtered)} rows ({len(filtered)/original*100:.1f}%)")

# Filter 3: Has taxonomy
filtered = filtered[filtered[col3].notna()]
print(f"After Filter 3 (Has taxonomy): {len(filtered)} rows ({len(filtered)/original*100:.1f}%)")

print("\n" + "=" * 80)
print(f"Final result: {len(filtered)}/{original} rows would be kept")
print("=" * 80)
