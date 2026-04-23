"""
Parse loss development triangles from Excel or CSV files.
Handles standard triangle layout, columnar layout, transaction-level data,
and common variations.
"""
import pandas as pd
import numpy as np
import re
import sys
import json
import argparse


# Column names (case-insensitive) that signal transaction-level data
_TRANSACTION_COLUMNS = {
    "accident_date", "loss_date", "date_of_loss", "accident_dt",
    "evaluation_date", "eval_date", "valuation_date",
    "claim_id", "claim_number", "claimid",
    "paid_loss", "paid", "paid_amount", "paid_losses",
    "incurred_loss", "incurred", "incurred_amount", "incurred_losses",
    "case_reserve", "case_reserves", "outstanding", "os_reserve",
}


def _detect_transaction_format(df):
    """Check if the dataframe looks like claim-level transaction data.

    Returns True if the first row (potential header) contains enough
    recognizable transaction column names.
    """
    first_row = [str(v).strip().lower().replace(" ", "_") for v in df.iloc[0]]
    matches = sum(1 for v in first_row if v in _TRANSACTION_COLUMNS)
    return matches >= 3


def _find_column(headers, candidates):
    """Find the first matching column index from a list of candidate names."""
    normalized = [str(h).strip().lower().replace(" ", "_") for h in headers]
    for candidate in candidates:
        if candidate in normalized:
            return normalized.index(candidate)
    return None


def parse_transaction_format(df, value_type="incurred"):
    """Aggregate claim-level transaction data into a development triangle.

    Args:
        df: DataFrame where the first row is a header with recognizable
            column names (accident_date, evaluation_date, paid_loss, etc.)
        value_type: Which loss value to aggregate — "paid", "incurred", or "both".
            Defaults to "incurred". Falls back to "paid" if incurred is unavailable.

    Returns:
        (accident_periods, dev_periods, triangle_df)
    """
    headers = df.iloc[0].tolist()
    data = df.iloc[1:].copy()
    data.columns = [str(h).strip().lower().replace(" ", "_") for h in headers]
    data = data.reset_index(drop=True)

    # Locate required columns
    acc_col = _find_column(headers, [
        "accident_date", "loss_date", "date_of_loss", "accident_dt",
    ])
    eval_col = _find_column(headers, [
        "evaluation_date", "eval_date", "valuation_date",
    ])
    if acc_col is None or eval_col is None:
        raise ValueError(
            "Transaction data requires accident_date and evaluation_date columns"
        )

    acc_col_name = data.columns[acc_col]
    eval_col_name = data.columns[eval_col]

    # Parse dates
    data[acc_col_name] = pd.to_datetime(data[acc_col_name], errors="coerce")
    data[eval_col_name] = pd.to_datetime(data[eval_col_name], errors="coerce")
    data = data.dropna(subset=[acc_col_name, eval_col_name])

    # Derive accident year and development period (in years, 1-indexed)
    data["_accident_year"] = data[acc_col_name].dt.year
    data["_dev_period"] = data[eval_col_name].dt.year - data["_accident_year"] + 1
    data = data[data["_dev_period"] >= 1]

    # Select the value column
    paid_col = _find_column(headers, [
        "paid_loss", "paid", "paid_amount", "paid_losses",
    ])
    incurred_col = _find_column(headers, [
        "incurred_loss", "incurred", "incurred_amount", "incurred_losses",
    ])

    if value_type == "incurred" and incurred_col is not None:
        val_col_name = data.columns[incurred_col]
    elif paid_col is not None:
        val_col_name = data.columns[paid_col]
    elif incurred_col is not None:
        val_col_name = data.columns[incurred_col]
    else:
        # Try computing incurred from paid + case reserve
        case_col = _find_column(headers, [
            "case_reserve", "case_reserves", "outstanding", "os_reserve",
        ])
        if paid_col is not None and case_col is not None:
            paid_name = data.columns[paid_col]
            case_name = data.columns[case_col]
            data[paid_name] = pd.to_numeric(data[paid_name], errors="coerce").fillna(0)
            data[case_name] = pd.to_numeric(data[case_name], errors="coerce").fillna(0)
            data["_computed_incurred"] = data[paid_name] + data[case_name]
            val_col_name = "_computed_incurred"
        else:
            raise ValueError(
                "Transaction data requires a paid_loss, incurred_loss, or "
                "paid_loss + case_reserve column"
            )

    data[val_col_name] = pd.to_numeric(data[val_col_name], errors="coerce").fillna(0)

    # Take the latest evaluation per claim per development period
    claim_col = _find_column(headers, [
        "claim_id", "claim_number", "claimid",
    ])
    if claim_col is not None:
        claim_col_name = data.columns[claim_col]
        # Keep the row with the latest evaluation_date per claim per dev period
        data = data.sort_values(eval_col_name).groupby(
            [claim_col_name, "_accident_year", "_dev_period"], as_index=False
        ).last()

    # Aggregate: sum across claims by accident year and dev period
    triangle = data.groupby(["_accident_year", "_dev_period"])[val_col_name].sum()
    triangle = triangle.unstack()

    acc_periods = [str(y) for y in sorted(triangle.index)]
    dev_periods = sorted(triangle.columns.tolist())
    triangle_data = triangle.sort_index().reset_index(drop=True)
    triangle_data.columns = dev_periods

    return acc_periods, dev_periods, triangle_data


def detect_triangle_format(df):
    """Detect whether data is in triangle format or columnar format."""
    if df.shape[1] >= 3 and df.shape[0] > df.shape[1] * 1.5:
        return "columnar"
    numeric_cols = df.select_dtypes(include=[np.number]).shape[1]
    if numeric_cols >= 3 and df.shape[0] <= numeric_cols + 5:
        return "triangle"
    return "triangle"


def parse_triangle_format(df):
    """Parse a standard triangle: rows=accident periods, cols=development periods."""
    df = df.copy()

    # Find the first row where column 0 looks like a year/period label
    # and remaining columns are numeric (this is the data start)
    data_start = None
    for i in range(min(10, len(df))):
        row_vals = df.iloc[i, 1:].dropna()
        numeric_count = sum(1 for v in row_vals if _is_numeric(v))
        if numeric_count >= 2 and _looks_like_period(df.iloc[i, 0]):
            data_start = i
            break

    if data_start is None:
        # Fallback: skip rows until we find numeric data
        for i in range(min(10, len(df))):
            row_vals = df.iloc[i, 1:].dropna()
            numeric_count = sum(1 for v in row_vals if _is_numeric(v))
            if numeric_count >= 2:
                data_start = i
                break
        if data_start is None:
            data_start = 1  # skip header

    result = df.iloc[data_start:].copy()
    result.columns = range(result.shape[1])

    # First column = accident period labels
    acc_periods = result.iloc[:, 0].astype(str).str.strip()
    # Clean year strings
    acc_periods = acc_periods.apply(lambda x: str(int(float(x))) if _is_numeric(x) and '.' in str(x) else x)

    # Remaining columns = loss values by development period
    triangle_data = result.iloc[:, 1:]
    triangle_data = triangle_data.apply(pd.to_numeric, errors='coerce')

    # Remove rows that are all NaN or look like summary/total rows
    valid_mask = triangle_data.notna().any(axis=1)
    acc_periods = acc_periods[valid_mask].reset_index(drop=True)
    triangle_data = triangle_data[valid_mask].reset_index(drop=True)

    # Filter out rows where acc_period doesn't look like a period label
    keep_mask = acc_periods.apply(_looks_like_period)
    acc_periods = acc_periods[keep_mask].reset_index(drop=True)
    triangle_data = triangle_data[keep_mask].reset_index(drop=True)

    # Create development period labels (1, 2, 3, ...)
    dev_periods = list(range(1, triangle_data.shape[1] + 1))
    triangle_data.columns = dev_periods

    return acc_periods.tolist(), dev_periods, triangle_data


def _is_numeric(val):
    """Check if a value is numeric."""
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False


def _looks_like_period(val):
    """Check if a value looks like an accident period (year, quarter, date)."""
    s = str(val).strip()
    # Year-like: 2016, 2017, etc.
    if s.isdigit() and 1970 <= int(s) <= 2050:
        return True
    # Float year: 2016.0
    try:
        f = float(s)
        if 1970 <= f <= 2050:
            return True
    except ValueError:
        pass
    # Contains a year
    import re
    if re.search(r'(19|20)\d{2}', s):
        return True
    # Quarter format: 2016Q1, 2016-Q1, etc.
    if re.search(r'Q[1-4]', s, re.IGNORECASE):
        return True
    return False


def parse_columnar_format(df, acc_col=0, dev_col=1, val_col=2):
    """Parse columnar format: columns for accident period, dev period, and value."""
    df = df.copy()
    acc = df.iloc[:, acc_col]
    dev = df.iloc[:, dev_col]
    val = pd.to_numeric(df.iloc[:, val_col], errors='coerce')

    pivot = val.groupby([acc, dev]).sum().unstack()
    acc_periods = [str(x) for x in pivot.index.tolist()]
    dev_periods = pivot.columns.tolist()
    triangle_data = pivot.reset_index(drop=True)
    triangle_data.columns = dev_periods

    return acc_periods, dev_periods, triangle_data


def read_triangle(filepath, sheet_name=None):
    """
    Read a triangle from Excel or CSV.
    Returns: (accident_periods, dev_periods, triangle_df, metadata)
    """
    ext = filepath.lower().split('.')[-1]

    if ext == 'csv':
        df = pd.read_csv(filepath, header=None)
    elif ext in ('xlsx', 'xls', 'xlsm'):
        if sheet_name:
            df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
        else:
            xls = pd.ExcelFile(filepath)
            sheets = xls.sheet_names
            df = pd.read_excel(xls, sheet_name=sheets[0], header=None)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    # Check for transaction-level data first (needs header row)
    if _detect_transaction_format(df):
        fmt = "transaction"
        acc_periods, dev_periods, triangle_data = parse_transaction_format(df)
    else:
        fmt = detect_triangle_format(df)
        if fmt == "triangle":
            acc_periods, dev_periods, triangle_data = parse_triangle_format(df)
        else:
            acc_periods, dev_periods, triangle_data = parse_columnar_format(df)

    metadata = {
        "format_detected": fmt,
        "n_accident_periods": len(acc_periods),
        "n_dev_periods": len(dev_periods),
        "accident_periods": acc_periods,
        "dev_periods": [str(d) for d in dev_periods],
        "has_negative_values": bool((triangle_data < 0).any().any()),
        "sparsity": float(triangle_data.isna().sum().sum() / triangle_data.size),
    }

    return acc_periods, dev_periods, triangle_data, metadata


def read_premium(filepath, sheet_name=None):
    """Read earned premium data. Expects accident period and premium columns."""
    ext = filepath.lower().split('.')[-1]
    if ext == 'csv':
        df = pd.read_csv(filepath)
    else:
        if sheet_name is None:
            sheet_name = 0
        df = pd.read_excel(filepath, sheet_name=sheet_name)

    # Assume first col = accident period, second col = premium
    premiums = {}
    for _, row in df.iterrows():
        key = str(row.iloc[0]).strip()
        # Clean up float-like year strings (e.g., "2016.0" -> "2016")
        if '.' in key:
            try:
                key = str(int(float(key)))
            except ValueError:
                pass
        premiums[key] = float(row.iloc[1])
    return premiums


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a loss development triangle")
    parser.add_argument("--input", required=True, help="Path to triangle file")
    parser.add_argument("--sheet", default=None, help="Sheet name for Excel files")
    args = parser.parse_args()

    acc, dev, tri, meta = read_triangle(args.input, args.sheet)
    print(json.dumps(meta, indent=2))
    print("\nTriangle Preview:")
    print(tri.to_string())
