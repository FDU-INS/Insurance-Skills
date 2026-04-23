#!/usr/bin/env python3
"""
Claims Data Analysis Utilities

Functions for cohort building, utilization metrics, and adherence calculations.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional


def build_diagnosis_cohort(
    medical_df: pd.DataFrame,
    icd_codes: List[str],
    dx_columns: List[str] = None,
    min_claims: int = 2,
    lookback_days: int = 365
) -> pd.DataFrame:
    """
    Build patient cohort based on diagnosis codes.
    
    Args:
        medical_df: Medical claims DataFrame
        icd_codes: List of ICD-10 code prefixes (e.g., ['E11', 'E13'])
        dx_columns: Diagnosis columns to search (default: dx1-dx8)
        min_claims: Minimum number of claims required
        lookback_days: Days to look back for diagnoses
    
    Returns:
        DataFrame with member_id and index_date
    """
    if dx_columns is None:
        dx_columns = [f'dx{i}' for i in range(1, 9)]
    
    cutoff_date = datetime.now() - timedelta(days=lookback_days)
    
    df = medical_df[medical_df['service_from_date'] >= cutoff_date].copy()
    
    mask = pd.Series(False, index=df.index)
    for col in dx_columns:
        if col in df.columns:
            for code in icd_codes:
                mask |= df[col].astype(str).str.startswith(code)
    
    dx_claims = df[mask].copy()
    
    cohort = (
        dx_claims
        .groupby('member_id')
        .agg(
            claim_count=('claim_id', 'nunique'),
            index_date=('service_from_date', 'min')
        )
        .reset_index()
    )
    
    cohort = cohort[cohort['claim_count'] >= min_claims]
    
    return cohort[['member_id', 'index_date']]


def calculate_pdc(
    pharmacy_df: pd.DataFrame,
    member_id: str,
    drug_codes: List[str],
    start_date: datetime,
    end_date: datetime,
    code_column: str = 'gpi'
) -> dict:
    """
    Calculate Proportion of Days Covered (PDC) for a member.
    
    Args:
        pharmacy_df: Pharmacy claims DataFrame
        member_id: Patient identifier
        drug_codes: List of drug code prefixes
        start_date: Observation period start
        end_date: Observation period end
        code_column: Column containing drug codes
    
    Returns:
        Dict with PDC metrics
    """
    mask = (
        (pharmacy_df['member_id'] == member_id) &
        (pharmacy_df['fill_date'] >= start_date) &
        (pharmacy_df['fill_date'] <= end_date)
    )
    
    for code in drug_codes:
        mask &= pharmacy_df[code_column].astype(str).str.startswith(code)
    
    fills = pharmacy_df[mask].sort_values('fill_date').copy()
    
    if len(fills) == 0:
        return {'member_id': member_id, 'pdc': None, 'fills': 0, 'days_covered': 0}
    
    observation_days = (end_date - start_date).days + 1
    
    covered = np.zeros(observation_days)
    
    for _, row in fills.iterrows():
        fill_day = (row['fill_date'] - start_date).days
        days_supply = int(row['days_supply'])
        
        for d in range(fill_day, min(fill_day + days_supply, observation_days)):
            if d >= 0:
                covered[d] = 1
    
    days_covered = int(covered.sum())
    pdc = round(100 * days_covered / observation_days, 1)
    
    return {
        'member_id': member_id,
        'pdc': pdc,
        'adherent': pdc >= 80,
        'fills': len(fills),
        'days_covered': days_covered,
        'observation_days': observation_days
    }


def calculate_pmpm(
    medical_df: pd.DataFrame,
    eligibility_df: pd.DataFrame,
    start_date: datetime,
    end_date: datetime,
    cost_column: str = 'paid_amount'
) -> pd.DataFrame:
    """
    Calculate Per Member Per Month (PMPM) costs.
    
    Args:
        medical_df: Medical claims DataFrame
        eligibility_df: Eligibility DataFrame
        start_date: Analysis period start
        end_date: Analysis period end
        cost_column: Column containing cost values
    
    Returns:
        DataFrame with PMPM by member
    """
    claims = medical_df[
        (medical_df['service_from_date'] >= start_date) &
        (medical_df['service_from_date'] <= end_date)
    ].copy()
    
    member_costs = (
        claims
        .groupby('member_id')[cost_column]
        .sum()
        .reset_index()
    )
    member_costs.columns = ['member_id', 'total_cost']
    
    elig = eligibility_df.copy()
    elig['eff_date'] = pd.to_datetime(elig['eff_date'])
    elig['term_date'] = pd.to_datetime(elig['term_date'])
    
    elig['period_start'] = elig['eff_date'].clip(lower=start_date)
    elig['period_end'] = elig['term_date'].clip(upper=end_date)
    
    elig['member_months'] = (
        (elig['period_end'].dt.year - elig['period_start'].dt.year) * 12 +
        (elig['period_end'].dt.month - elig['period_start'].dt.month) + 1
    ).clip(lower=0)
    
    member_months = elig.groupby('member_id')['member_months'].sum().reset_index()
    
    result = member_months.merge(member_costs, on='member_id', how='left')
    result['total_cost'] = result['total_cost'].fillna(0)
    result['pmpm'] = result['total_cost'] / result['member_months'].clip(lower=1)
    
    return result


def identify_episodes(
    claims_df: pd.DataFrame,
    member_id: str,
    gap_days: int = 30
) -> pd.DataFrame:
    """
    Group claims into episodes of care based on gap between services.
    
    Args:
        claims_df: Claims DataFrame for one condition
        member_id: Patient identifier
        gap_days: Days without service to start new episode
    
    Returns:
        DataFrame with episode assignments
    """
    member_claims = claims_df[claims_df['member_id'] == member_id].copy()
    member_claims = member_claims.sort_values('service_from_date')
    
    if len(member_claims) == 0:
        return pd.DataFrame()
    
    member_claims['prev_date'] = member_claims['service_from_date'].shift(1)
    member_claims['gap'] = (
        member_claims['service_from_date'] - member_claims['prev_date']
    ).dt.days
    
    member_claims['new_episode'] = (
        (member_claims['gap'] > gap_days) | 
        (member_claims['gap'].isna())
    ).astype(int)
    
    member_claims['episode_num'] = member_claims['new_episode'].cumsum()
    
    return member_claims


if __name__ == '__main__':
    print("Claims analysis utilities loaded.")
    print("Functions: build_diagnosis_cohort, calculate_pdc, calculate_pmpm, identify_episodes")
