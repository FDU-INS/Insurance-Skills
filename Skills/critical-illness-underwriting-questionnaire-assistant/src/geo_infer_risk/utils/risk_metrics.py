"""
Risk Metrics: Functions for calculating key risk metrics from event loss data.

This module provides utility functions for calculating risk metrics such as:
- Average Annual Loss (AAL)
- Exceedance Probability (EP) curves
- Probable Maximum Loss (PML)
- Return period losses
- Loss exceedance curves
"""

from typing import Dict, List, Any, Union, Optional
import numpy as np
import pandas as pd


def calculate_aal(event_loss_table: Union[pd.DataFrame, np.ndarray]) -> Union[float, Dict[str, Any]]:
    """
    Calculate the Average Annual Loss (AAL) from an event loss table or loss array.

    The AAL represents the expected annual loss averaged over many years.

    Args:
        event_loss_table: Either a DataFrame containing event losses with columns
            'event_id', 'hazard_type', and 'loss', or a numpy array of loss values.

    Returns:
        If input is a numpy array, returns float (mean loss).
        If input is a DataFrame, returns Dict with 'total' and 'by_hazard' keys.
    """
    # Handle numpy array input: compute mean loss directly
    if isinstance(event_loss_table, np.ndarray):
        losses = event_loss_table.astype(float)
        if len(losses) == 0:
            return 0.0
        return float(np.mean(losses))

    # DataFrame path: validate columns
    required_columns = ['event_id', 'hazard_type', 'loss']
    for col in required_columns:
        if col not in event_loss_table.columns:
            raise ValueError(f"event_loss_table must contain column '{col}'")

    # Calculate total AAL
    total_loss = event_loss_table['loss'].sum()
    num_events = len(event_loss_table['event_id'].unique())

    # Simple AAL calculation: total loss / number of events
    total_aal = total_loss / num_events if num_events > 0 else 0

    # Calculate AAL by hazard type
    hazard_aal = {}
    for hazard_type, group in event_loss_table.groupby('hazard_type'):
        hazard_loss = group['loss'].sum()
        hazard_events = len(group['event_id'].unique())
        hazard_aal[hazard_type] = hazard_loss / hazard_events if hazard_events > 0 else 0

    return {
        'total': total_aal,
        'by_hazard': hazard_aal
    }


def calculate_ep_curve(event_loss_table: Union[pd.DataFrame, np.ndarray],
                       exceedance_probs: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    Calculate the Exceedance Probability (EP) curve from an event loss table or loss array.

    The EP curve shows the probability of exceeding different loss thresholds.

    Args:
        event_loss_table: Either a DataFrame with columns 'event_id', 'hazard_type',
            'loss', or a numpy array of loss values.
        exceedance_probs: List of exceedance probabilities to calculate losses for.

    Returns:
        Dict with 'exceedance_probability', 'loss', and 'return_period' lists.
    """
    # Handle numpy array input
    if isinstance(event_loss_table, np.ndarray):
        losses = np.sort(event_loss_table.astype(float))[::-1]
        n = len(losses)
        if n == 0:
            return {'exceedance_probability': [], 'loss': [], 'return_period': []}
        ep = [(i + 1) / (n + 1) for i in range(n)]
        rp = [1.0 / p if p > 0 else float('inf') for p in ep]
        return {
            'exceedance_probability': ep,
            'loss': losses.tolist(),
            'return_period': rp,
        }

    # DataFrame path: validate columns
    required_columns = ['event_id', 'hazard_type', 'loss']
    for col in required_columns:
        if col not in event_loss_table.columns:
            raise ValueError(f"event_loss_table must contain column '{col}'")
    
    # Use default exceedance probabilities if not provided
    if exceedance_probs is None:
        exceedance_probs = [0.5, 0.2, 0.1, 0.04, 0.02, 0.01, 0.004, 0.002]
    
    # Sort exceedance probabilities in descending order (for consistency)
    exceedance_probs = sorted(exceedance_probs, reverse=True)
    
    # Calculate total loss by event
    event_totals = event_loss_table.groupby('event_id')['loss'].sum().reset_index()
    
    # Sort losses in descending order
    sorted_losses = sorted(event_totals['loss'].values, reverse=True)
    
    # Calculate exceedance probabilities
    num_events = len(sorted_losses)
    empirical_probs = [(i + 1) / (num_events + 1) for i in range(num_events)]
    
    # Calculate losses at specified exceedance probabilities
    losses_at_probs = []
    
    for prob in exceedance_probs:
        # Find nearest empirical probability
        idx = np.searchsorted(empirical_probs[::-1], prob)
        if idx == 0:
            # Probability is higher than any empirical probability
            loss = sorted_losses[0] if sorted_losses else 0
        elif idx >= len(empirical_probs):
            # Probability is lower than any empirical probability
            loss = sorted_losses[-1] if sorted_losses else 0
        else:
            # Interpolate between the two nearest empirical probabilities
            p1 = empirical_probs[::-1][idx-1]
            p2 = empirical_probs[::-1][idx] if idx < len(empirical_probs) else 0
            l1 = sorted_losses[idx-1] if idx-1 < len(sorted_losses) else 0
            l2 = sorted_losses[idx] if idx < len(sorted_losses) else 0
            
            if p1 == p2:
                loss = l1
            else:
                # Linear interpolation
                loss = l1 + (l2 - l1) * (prob - p1) / (p2 - p1)
        
        losses_at_probs.append(loss)
    
    # Calculate return periods
    return_periods = [1.0 / prob for prob in exceedance_probs]
    
    return {
        'exceedance_probability': exceedance_probs,
        'loss': losses_at_probs,
        'return_period': return_periods
    }


def calculate_pml(event_loss_table: pd.DataFrame, 
                 return_period: float = 250) -> float:
    """
    Calculate the Probable Maximum Loss (PML) for a given return period.
    
    The PML is the loss that is expected to be exceeded with a probability of 1/return_period.
    
    Args:
        event_loss_table (pd.DataFrame): DataFrame containing event losses.
            Must have columns 'event_id', 'hazard_type', and 'loss'.
        return_period (float, optional): Return period in years. Default is 250 years.
            
    Returns:
        float: Probable Maximum Loss (PML) for the specified return period
    """
    # Calculate EP curve
    exceedance_prob = 1.0 / return_period
    ep_curve = calculate_ep_curve(event_loss_table, [exceedance_prob])
    
    # Extract PML from EP curve
    pml = ep_curve['loss'][0] if ep_curve['loss'] else 0
    
    return pml


def calculate_loss_by_return_period(event_loss_table: pd.DataFrame,
                                   return_periods: List[float]) -> Dict[str, float]:
    """
    Calculate losses for multiple return periods.
    
    Args:
        event_loss_table (pd.DataFrame): DataFrame containing event losses.
            Must have columns 'event_id', 'hazard_type', and 'loss'.
        return_periods (List[float]): List of return periods to calculate losses for.
            
    Returns:
        Dict[str, float]: Dictionary mapping return periods to losses
    """
    # Calculate exceedance probabilities from return periods
    exceedance_probs = [1.0 / rp for rp in return_periods]
    
    # Calculate EP curve
    ep_curve = calculate_ep_curve(event_loss_table, exceedance_probs)
    
    # Create dictionary mapping return periods to losses
    return_period_losses = {}
    for rp, loss in zip(return_periods, ep_curve['loss']):
        return_period_losses[str(rp)] = loss
    
    return return_period_losses


def calculate_tail_value_at_risk(event_loss_table: pd.DataFrame,
                                confidence_level: float = 0.99) -> float:
    """
    Calculate the Tail Value at Risk (TVaR) at a specified confidence level.
    
    The TVaR is the expected loss given that the loss exceeds the Value at Risk (VaR).
    It is a more conservative risk measure than VaR.
    
    Args:
        event_loss_table (pd.DataFrame): DataFrame containing event losses.
            Must have columns 'event_id', 'hazard_type', and 'loss'.
        confidence_level (float, optional): Confidence level (e.g., 0.99 for 99%).
            Default is 0.99.
            
    Returns:
        float: Tail Value at Risk (TVaR) at the specified confidence level
    """
    # Calculate total loss by event
    event_totals = event_loss_table.groupby('event_id')['loss'].sum().reset_index()
    
    # Sort losses
    sorted_losses = sorted(event_totals['loss'].values)
    
    # Calculate Value at Risk (VaR)
    var_idx = int(np.ceil(confidence_level * len(sorted_losses))) - 1
    var_idx = max(0, min(var_idx, len(sorted_losses) - 1))
    var = sorted_losses[var_idx]
    
    # Calculate TVaR
    tail_losses = [loss for loss in sorted_losses if loss >= var]
    tvar = np.mean(tail_losses) if tail_losses else var
    
    return tvar


def calculate_annual_occurrence_exceedance_probability(event_loss_table: pd.DataFrame,
                                                     threshold: float) -> float:
    """
    Calculate the Annual Occurrence Exceedance Probability (OEP) for a loss threshold.
    
    The OEP is the probability that at least one event in a year exceeds the threshold.
    
    Args:
        event_loss_table (pd.DataFrame): DataFrame containing event losses.
            Must have columns 'event_id', 'hazard_type', and 'loss'.
        threshold (float): Loss threshold.
            
    Returns:
        float: Annual occurrence exceedance probability
    """
    # Calculate total loss by event
    event_totals = event_loss_table.groupby('event_id')['loss'].sum().reset_index()
    
    # Count events exceeding threshold
    exceeding_events = sum(event_totals['loss'] > threshold)
    
    # Calculate probability
    # In a simple model, assuming events are uniformly distributed across all years
    # In a real model, this would account for the actual yearly distribution
    num_events = len(event_totals)
    num_years = 1  # Placeholder - in a real model, this would be the number of years in the simulation
    
    # Simple probability calculation
    avg_events_per_year = num_events / num_years
    events_exceeding_per_year = exceeding_events / num_years
    
    # Probability that at least one event exceeds the threshold
    # Using Poisson distribution approximation
    oep = 1.0 - np.exp(-events_exceeding_per_year)
    
    return oep


def calculate_annual_aggregate_exceedance_probability(event_loss_table: pd.DataFrame,
                                                    threshold: float,
                                                    num_years: int = 10000) -> float:
    """
    Calculate the Annual Aggregate Exceedance Probability (AEP) for a loss threshold.
    
    The AEP is the probability that the sum of all event losses in a year exceeds the threshold.
    
    Args:
        event_loss_table (pd.DataFrame): DataFrame containing event losses.
            Must have columns 'event_id', 'hazard_type', and 'loss'.
        threshold (float): Loss threshold.
        num_years (int, optional): Number of years to simulate. Default is 10000.
            
    Returns:
        float: Annual aggregate exceedance probability
    """
    # Calculate total loss by event
    event_totals = event_loss_table.groupby('event_id')['loss'].sum().reset_index()
    
    # Simple Monte Carlo simulation to estimate AEP
    # In a real model, this would use a more sophisticated approach
    
    # Get all event losses
    all_losses = event_totals['loss'].values
    
    # Calculate average number of events per year
    avg_events_per_year = len(all_losses) / 1  # Placeholder - in a real model, this would be based on actual data
    
    # Simulate years
    years_exceeding = 0
    
    for _ in range(num_years):
        # Generate random number of events for this year
        num_events = np.random.poisson(avg_events_per_year)
        
        # Sample events and sum losses
        if num_events > 0:
            year_losses = np.random.choice(all_losses, size=num_events, replace=True)
            total_year_loss = np.sum(year_losses)
            
            # Check if year loss exceeds threshold
            if total_year_loss > threshold:
                years_exceeding += 1
    
    # Calculate probability
    aep = years_exceeding / num_years
    
    return aep


def calculate_loss_frequency_curve(event_loss_table: pd.DataFrame,
                                  num_bins: int = 20) -> Dict[str, List[float]]:
    """
    Calculate a loss frequency curve (histogram of losses).
    
    Args:
        event_loss_table (pd.DataFrame): DataFrame containing event losses.
            Must have columns 'event_id', 'hazard_type', and 'loss'.
        num_bins (int, optional): Number of bins for the histogram. Default is 20.
            
    Returns:
        Dict[str, List[float]]: Dictionary containing:
            - bin_edges: Edges of the histogram bins
            - frequencies: Frequencies (counts) for each bin
            - normalized_frequencies: Frequencies normalized to sum to 1
    """
    # Calculate total loss by event
    event_totals = event_loss_table.groupby('event_id')['loss'].sum().reset_index()
    
    # Calculate histogram
    frequencies, bin_edges = np.histogram(event_totals['loss'], bins=num_bins)
    
    # Normalize frequencies
    normalized_frequencies = frequencies / np.sum(frequencies) if np.sum(frequencies) > 0 else frequencies
    
    return {
        'bin_edges': bin_edges.tolist(),
        'frequencies': frequencies.tolist(),
        'normalized_frequencies': normalized_frequencies.tolist()
    }


def calculate_correlation_matrix(event_loss_table: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate the correlation matrix between losses for different hazard types.
    
    Args:
        event_loss_table (pd.DataFrame): DataFrame containing event losses.
            Must have columns 'event_id', 'hazard_type', and 'loss'.
            
    Returns:
        Dict[str, Any]: Dictionary containing:
            - hazard_types: List of hazard types
            - correlation_matrix: Correlation matrix as a nested list
    """
    # Pivot the data to get losses by hazard type for each event
    pivot_table = event_loss_table.pivot_table(
        index='event_id',
        columns='hazard_type',
        values='loss',
        aggfunc='sum',
        fill_value=0
    )
    
    # Calculate correlation matrix
    corr_matrix = pivot_table.corr().values.tolist()
    
    return {
        'hazard_types': pivot_table.columns.tolist(),
        'correlation_matrix': corr_matrix
    }