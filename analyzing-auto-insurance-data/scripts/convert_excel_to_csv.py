"""
Convert Excel files to CSV format for AI-friendly processing

This script helps convert insurance data Excel files to CSV format,
which is much easier for AI assistants to read and parse directly.

Usage:
    python convert_excel_to_csv.py input.xlsx output.csv
    python convert_excel_to_csv.py input.xlsx  # Auto-generates output filename
"""

import sys
import pandas as pd
from pathlib import Path


def convert_excel_to_csv(excel_path: str, csv_path: str = None) -> str:
    """
    Convert Excel file to CSV format

    Args:
        excel_path: Path to input Excel file
        csv_path: Path to output CSV file (optional, auto-generated if not provided)

    Returns:
        Path to the created CSV file
    """
    excel_file = Path(excel_path)

    if not excel_file.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Auto-generate CSV filename if not provided
    if csv_path is None:
        csv_path = excel_file.with_suffix('.csv')

    # Read Excel file
    print(f"Reading Excel file: {excel_path}")
    df = pd.read_excel(excel_path)

    # Save as CSV with UTF-8 encoding
    print(f"Converting to CSV: {csv_path}")
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')

    print(f"✓ Successfully converted!")
    print(f"  - Rows: {len(df)}")
    print(f"  - Columns: {len(df.columns)}")
    print(f"  - Output: {csv_path}")

    return str(csv_path)


def convert_staff_mapping_to_json(excel_path: str, json_path: str = "staff_mapping.json") -> str:
    """
    Convert staff-institution mapping Excel to JSON format

    This is specifically for the 业务员机构团队对照表 file.

    Args:
        excel_path: Path to mapping Excel file
        json_path: Path to output JSON file

    Returns:
        Path to the created JSON file
    """
    import json

    print(f"Reading staff mapping Excel: {excel_path}")
    df = pd.read_excel(excel_path)

    # Remove first unnamed column if exists
    if df.columns[0].startswith('Unnamed'):
        df = df.iloc[:, 1:]

    # Set proper column names
    df.columns = ['序号', '三级机构', '四级机构', '团队简称', '业务员']

    # Skip header row if it exists
    df = df[df['序号'] != '序号']

    # Create mapping dictionary
    mapping = {}
    for _, row in df.iterrows():
        agent = str(row['业务员']).strip()
        if agent and agent != 'nan':
            mapping[agent] = {
                '三级机构': str(row['三级机构']) if pd.notna(row['三级机构']) else None,
                '四级机构': str(row['四级机构']) if pd.notna(row['四级机构']) else None,
                '团队简称': str(row['团队简称']) if pd.notna(row['团队简称']) else None
            }

    # Save as JSON
    print(f"Saving JSON mapping: {json_path}")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"✓ Successfully created JSON mapping!")
    print(f"  - Total agents: {len(mapping)}")
    print(f"  - Output: {json_path}")

    return json_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python convert_excel_to_csv.py <excel_file> [csv_file]")
        print("")
        print("Examples:")
        print("  python convert_excel_to_csv.py data.xlsx")
        print("  python convert_excel_to_csv.py data.xlsx output.csv")
        print("  python convert_excel_to_csv.py 业务员机构团队对照表.xlsx --mapping")
        sys.exit(1)

    excel_path = sys.argv[1]

    # Special handling for staff mapping file
    if '--mapping' in sys.argv or '业务员机构' in excel_path:
        convert_staff_mapping_to_json(excel_path)
    else:
        csv_path = sys.argv[2] if len(sys.argv) > 2 else None
        convert_excel_to_csv(excel_path, csv_path)
