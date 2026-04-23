"""
Common query helpers for HealthSim database operations.

Provides convenience functions for typical queries against
canonical and state management tables.
"""

from typing import Any, Dict, List, Optional
import duckdb

from .connection import get_connection


def get_patient_by_id(patient_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a patient by their ID.
    
    Args:
        patient_id: The patient's unique ID.
        
    Returns:
        Patient dict or None if not found.
    """
    conn = get_connection()
    result = conn.execute(
        "SELECT * FROM patients WHERE id = ?", [patient_id]
    ).fetchone()
    
    if result:
        columns = [desc[0] for desc in conn.description]
        return dict(zip(columns, result))
    return None


def get_patient_by_mrn(mrn: str) -> Optional[Dict[str, Any]]:
    """
    Get a patient by their MRN.
    
    Args:
        mrn: Medical Record Number.
        
    Returns:
        Patient dict or None if not found.
    """
    conn = get_connection()
    result = conn.execute(
        "SELECT * FROM patients WHERE mrn = ?", [mrn]
    ).fetchone()
    
    if result:
        columns = [desc[0] for desc in conn.description]
        return dict(zip(columns, result))
    return None


def get_patients_in_cohort(cohort_id: str) -> List[Dict[str, Any]]:
    """
    Get all patients associated with a cohort.
    
    Args:
        cohort_id: The cohort identifier.
        
    Returns:
        List of patient dicts.
    """
    conn = get_connection()
    result = conn.execute("""
        SELECT p.* FROM patients p
        JOIN cohort_entities ce ON p.id = ce.entity_id
        WHERE ce.cohort_id = ? AND ce.entity_type = 'patient'
    """, [cohort_id]).fetchall()
    
    if result:
        columns = [desc[0] for desc in conn.description]
        return [dict(zip(columns, row)) for row in result]
    return []


def count_entities_by_type(cohort_id: Optional[str] = None) -> Dict[str, int]:
    """
    Count entities by type, optionally filtered by cohort.
    
    Args:
        cohort_id: Optional cohort to filter by.
        
    Returns:
        Dict mapping entity types to counts.
    """
    conn = get_connection()
    
    if cohort_id:
        result = conn.execute("""
            SELECT entity_type, COUNT(*) as count
            FROM cohort_entities
            WHERE cohort_id = ?
            GROUP BY entity_type
        """, [cohort_id]).fetchall()
    else:
        # Count all entities across all tables
        counts = {}
        for table in ['patients', 'encounters', 'diagnoses', 'medications',
                      'lab_results', 'vital_signs', 'orders', 'clinical_notes',
                      'members', 'claims', 'claim_lines', 
                      'prescriptions', 'pharmacy_claims',
                      'subjects', 'trial_visits', 'adverse_events', 'exposures']:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            if count > 0:
                counts[table] = count
        return counts
    
    return {row[0]: row[1] for row in result}


def get_cohort_summary(cohort_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a summary of a cohort including entity counts.
    
    Args:
        cohort_id: The cohort identifier.
        
    Returns:
        Summary dict or None if cohort not found.
    """
    conn = get_connection()
    
    # Get cohort metadata
    cohort = conn.execute("""
        SELECT * FROM cohorts WHERE id = ?
    """, [cohort_id]).fetchone()
    
    if not cohort:
        return None
    
    columns = [desc[0] for desc in conn.description]
    summary = dict(zip(columns, cohort))
    
    # Get entity counts
    summary['entity_counts'] = count_entities_by_type(cohort_id)
    
    # Get tags
    tags = conn.execute("""
        SELECT tag FROM cohort_tags WHERE cohort_id = ?
    """, [cohort_id]).fetchall()
    summary['tags'] = [row[0] for row in tags]
    
    return summary


def list_cohorts(
    limit: int = 20, 
    tag: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List all cohorts, optionally filtered by tag.
    
    Args:
        limit: Maximum number of cohorts to return.
        tag: Optional tag to filter by.
        
    Returns:
        List of cohort summary dicts.
    """
    conn = get_connection()
    
    if tag:
        result = conn.execute("""
            SELECT s.* FROM cohorts s
            JOIN cohort_tags t ON s.id = t.cohort_id
            WHERE t.tag = ?
            ORDER BY s.updated_at DESC
            LIMIT ?
        """, [tag, limit]).fetchall()
    else:
        result = conn.execute("""
            SELECT * FROM cohorts
            ORDER BY updated_at DESC
            LIMIT ?
        """, [limit]).fetchall()
    
    if result:
        columns = [desc[0] for desc in conn.description]
        return [dict(zip(columns, row)) for row in result]
    return []


def cohort_exists(name: str) -> bool:
    """
    Check if a cohort with the given name exists.
    
    Args:
        name: Cohort name to check.
        
    Returns:
        True if cohort exists, False otherwise.
    """
    conn = get_connection()
    result = conn.execute(
        "SELECT 1 FROM cohorts WHERE name = ?", [name]
    ).fetchone()
    return result is not None


def get_schema_version() -> str:
    """
    Get the current database schema version.
    
    Returns:
        Schema version string.
    """
    from .migrations import get_current_version
    return get_current_version(get_connection())
