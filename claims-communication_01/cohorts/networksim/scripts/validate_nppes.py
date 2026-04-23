#!/usr/bin/env python3
"""
NPPES Data Validation Script
Validates the filtered NPPES dataset for quality and completeness
"""

import pandas as pd
import sys
from pathlib import Path

def validate_nppes(file_path):
    """
    Validate filtered NPPES data
    Returns quality score (0-100)
    """
    print("=" * 80)
    print("NPPES DATA VALIDATION")
    print("=" * 80)
    print(f"\nFile: {file_path}")
    print()
    
    # Read sample for quick validation
    print("Loading sample (100,000 records)...")
    df_sample = pd.read_csv(file_path, nrows=100000)
    
    # Get full file stats
    print("Analyzing full file...")
    df_full = pd.read_csv(file_path, usecols=['NPI', 'Entity Type Code', 'practice_state'])
    
    total_records = len(df_full)
    print(f"Total records: {total_records:,}\n")
    
    # Validation checks
    issues = []
    score = 100
    
    print("VALIDATION CHECKS:")
    print("-" * 80)
    
    # Check 1: NPI format (10 digits)
    print("\n1. NPI Format Validation")
    invalid_npi = df_sample[~df_sample['NPI'].astype(str).str.match(r'^\d{10}$')].shape[0]
    if invalid_npi > 0:
        pct = invalid_npi / len(df_sample) * 100
        print(f"   ✗ {invalid_npi:,} invalid NPIs found ({pct:.2f}%)")
        issues.append(f"Invalid NPI format: {invalid_npi}")
        score -= min(20, pct)
    else:
        print(f"   ✓ All NPIs are valid 10-digit numbers")
    
    # Check 2: Duplicate NPIs
    print("\n2. Duplicate Check")
    duplicates = df_full[df_full['NPI'].duplicated()].shape[0]
    if duplicates > 0:
        pct = duplicates / len(df_full) * 100
        print(f"   ✗ {duplicates:,} duplicate NPIs found ({pct:.2f}%)")
        issues.append(f"Duplicate NPIs: {duplicates}")
        score -= min(20, pct * 10)
    else:
        print(f"   ✓ No duplicate NPIs")
    
    # Check 3: Entity type distribution
    print("\n3. Entity Type Distribution")
    entity_types = df_full['Entity Type Code'].value_counts()
    print(f"   Type 1 (Individual): {entity_types.get('1', 0):,} ({entity_types.get('1', 0)/total_records*100:.1f}%)")
    print(f"   Type 2 (Organization): {entity_types.get('2', 0):,} ({entity_types.get('2', 0)/total_records*100:.1f}%)")
    if len(entity_types) > 2:
        print(f"   ✗ Unexpected entity types found: {list(entity_types.index)}")
        issues.append("Unexpected entity types")
        score -= 10
    
    # Check 4: Geographic coverage
    print("\n4. Geographic Coverage")
    states = df_full['practice_state'].value_counts()
    print(f"   States/territories covered: {len(states)}")
    print(f"   Top 5 states:")
    for state, count in states.head(5).items():
        print(f"      {state}: {count:,} ({count/total_records*100:.1f}%)")
    
    if len(states) < 50:
        print(f"   ⚠ Only {len(states)} states (expected ~50+)")
        score -= 5
    
    # Check 5: Taxonomy codes
    print("\n5. Taxonomy Code Coverage")
    has_taxonomy = df_sample['taxonomy_1'].notna().sum()
    pct = has_taxonomy / len(df_sample) * 100
    print(f"   Records with taxonomy: {has_taxonomy:,} ({pct:.1f}%)")
    if pct < 95:
        print(f"   ⚠ Lower than expected (should be ~100%)")
        score -= 5
    
    # Check 6: Required fields
    print("\n6. Required Fields Check")
    required_fields = ['NPI', 'Entity Type Code', 'practice_state', 'taxonomy_1']
    missing = []
    for field in required_fields:
        if field not in df_sample.columns:
            missing.append(field)
    
    if missing:
        print(f"   ✗ Missing fields: {missing}")
        issues.append(f"Missing required fields: {missing}")
        score -= 20
    else:
        print(f"   ✓ All required fields present")
    
    # Summary
    print()
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total Records:     {total_records:,}")
    print(f"File Size:         {file_path.stat().st_size / (1024**2):.1f} MB")
    print(f"Quality Score:     {max(0, score)}/100")
    
    if issues:
        print(f"\nIssues Found:      {len(issues)}")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print(f"\nIssues Found:      None")
    
    print()
    if score >= 90:
        print("✓ VALIDATION PASSED - Data quality is excellent!")
    elif score >= 70:
        print("⚠ VALIDATION WARNING - Data quality is acceptable but has issues")
    else:
        print("✗ VALIDATION FAILED - Data quality issues need to be addressed")
    
    print("=" * 80)
    
    return score >= 70

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "data/processed/nppes_filtered.csv"
    
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)
    
    success = validate_nppes(file_path)
    sys.exit(0 if success else 1)
