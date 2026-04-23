"""
Cohort summary generation for context-efficient loading.

Generates statistical summaries that fit within token budget (~500 tokens)
while providing enough information for generation consistency.

This implements the "summary-in-context" part of the Structured RAG pattern:
- Full data stays in DuckDB
- Only summary + samples loaded to conversation
- Queries retrieve specific data on demand
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID
import json

from ..db import get_connection


@dataclass
class CohortSummary:
    """
    Token-efficient cohort summary.
    
    Target budget:
    - Metadata: ~100 tokens
    - Entity counts: ~100 tokens
    - Statistics: ~300 tokens
    - Samples: ~3000 tokens (3 per major type)
    
    Total: ~3,500 tokens for full summary with samples
    """
    
    cohort_id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Entity counts by type
    entity_counts: Dict[str, int] = field(default_factory=dict)
    
    # Aggregate statistics
    statistics: Dict[str, Any] = field(default_factory=dict)
    
    # Sample entities for pattern consistency
    samples: Dict[str, List[Dict]] = field(default_factory=dict)
    
    # Tags for organization
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for JSON serialization."""
        return {
            'cohort_id': self.cohort_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'entity_counts': self.entity_counts,
            'statistics': self.statistics,
            'samples': self.samples,
            'tags': self.tags,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CohortSummary':
        """Create from dictionary."""
        return cls(
            cohort_id=data['cohort_id'],
            name=data['name'],
            description=data.get('description'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            entity_counts=data.get('entity_counts', {}),
            statistics=data.get('statistics', {}),
            samples=data.get('samples', {}),
            tags=data.get('tags', []),
        )
    
    def total_entities(self) -> int:
        """Get total entity count across all types."""
        return sum(self.entity_counts.values())
    
    def token_estimate(self) -> int:
        """
        Estimate token count for this summary.
        
        Rough heuristic: ~4 characters per token for JSON.
        """
        json_str = self.to_json(indent=None)
        return len(json_str) // 4


# Entity type to table mapping for counts
ENTITY_COUNT_TABLES = {
    # PatientSim
    'patients': 'patients',
    'encounters': 'encounters',
    'diagnoses': 'diagnoses',
    'procedures': 'procedures',
    'lab_results': 'lab_results',
    'medications': 'medications',
    'allergies': 'allergies',
    'vitals': 'vital_signs',
    
    # MemberSim
    'members': 'members',
    'claims': 'claims',
    'claim_lines': 'claim_lines',
    'authorizations': 'authorizations',
    'accumulators': 'accumulators',
    
    # RxMemberSim
    'rx_members': 'rx_members',
    'prescriptions': 'prescriptions',
    'pharmacy_claims': 'pharmacy_claims',
    'dur_alerts': 'dur_alerts',
    
    # TrialSim
    'studies': 'studies',
    'sites': 'sites',
    'subjects': 'subjects',
    'adverse_events': 'adverse_events',
    'actual_visits': 'actual_visits',
    
    # PopulationSim
    'population_profiles': 'population_profiles',
    'cohort_specifications': 'cohort_specifications',
    
    # NetworkSim
    'networks': 'networks',
    'network_providers': 'network_providers',
    'network_facilities': 'network_facilities',
}


def _get_entity_counts(cohort_id: str, connection=None) -> Dict[str, int]:
    """Get entity counts for all tables in a cohort."""
    conn = connection or get_connection()
    counts = {}
    
    for entity_type, table_name in ENTITY_COUNT_TABLES.items():
        try:
            result = conn.execute(f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE cohort_id = ?
            """, [cohort_id]).fetchone()
            
            count = result[0] if result else 0
            if count > 0:
                counts[entity_type] = count
        except Exception:
            # Table may not exist or have cohort_id column
            pass
    
    return counts


def _calculate_patient_statistics(cohort_id: str, connection=None) -> Dict[str, Any]:
    """Calculate statistics for patient data."""
    conn = connection or get_connection()
    stats = {}
    
    try:
        # Age statistics
        result = conn.execute("""
            SELECT 
                MIN(CAST((julianday('now') - julianday(birth_date)) / 365.25 AS INTEGER)) as min_age,
                MAX(CAST((julianday('now') - julianday(birth_date)) / 365.25 AS INTEGER)) as max_age,
                AVG(CAST((julianday('now') - julianday(birth_date)) / 365.25 AS INTEGER)) as avg_age
            FROM patients
            WHERE cohort_id = ? AND birth_date IS NOT NULL
        """, [cohort_id]).fetchone()
        
        if result and result[0] is not None:
            stats['age_range'] = {
                'min': result[0],
                'max': result[1],
                'avg': round(result[2], 1) if result[2] else None
            }
        
        # Gender distribution
        result = conn.execute("""
            SELECT gender, COUNT(*) as count
            FROM patients
            WHERE cohort_id = ?
            GROUP BY gender
        """, [cohort_id]).fetchall()
        
        if result:
            stats['gender_distribution'] = {row[0]: row[1] for row in result if row[0]}
        
    except Exception:
        pass
    
    return stats


def _calculate_encounter_statistics(cohort_id: str, connection=None) -> Dict[str, Any]:
    """Calculate statistics for encounter data."""
    conn = connection or get_connection()
    stats = {}
    
    try:
        # Date range
        result = conn.execute("""
            SELECT 
                MIN(DATE(admission_time)) as min_date,
                MAX(DATE(admission_time)) as max_date
            FROM encounters
            WHERE cohort_id = ? AND admission_time IS NOT NULL
        """, [cohort_id]).fetchone()
        
        if result and result[0]:
            stats['date_range'] = {
                'min': str(result[0]),
                'max': str(result[1])
            }
        
        # Encounter class distribution
        result = conn.execute("""
            SELECT class_code, COUNT(*) as count
            FROM encounters
            WHERE cohort_id = ?
            GROUP BY class_code
            ORDER BY count DESC
            LIMIT 5
        """, [cohort_id]).fetchall()
        
        if result:
            stats['encounter_types'] = {row[0]: row[1] for row in result if row[0]}
        
    except Exception:
        pass
    
    return stats


def _calculate_claims_statistics(cohort_id: str, connection=None) -> Dict[str, Any]:
    """Calculate statistics for claims data."""
    conn = connection or get_connection()
    stats = {}
    
    try:
        # Financial totals
        result = conn.execute("""
            SELECT 
                SUM(total_charge) as total_billed,
                SUM(total_paid) as total_paid,
                SUM(patient_responsibility) as total_patient_resp,
                AVG(total_charge) as avg_charge
            FROM claims
            WHERE cohort_id = ?
        """, [cohort_id]).fetchone()
        
        if result and result[0]:
            stats['financials'] = {
                'total_billed': round(result[0], 2),
                'total_paid': round(result[1], 2) if result[1] else 0,
                'total_patient_resp': round(result[2], 2) if result[2] else 0,
                'avg_charge': round(result[3], 2) if result[3] else 0
            }
        
        # Claim type distribution
        result = conn.execute("""
            SELECT claim_type, COUNT(*) as count
            FROM claims
            WHERE cohort_id = ?
            GROUP BY claim_type
        """, [cohort_id]).fetchall()
        
        if result:
            stats['claim_types'] = {row[0]: row[1] for row in result if row[0]}
        
    except Exception:
        pass
    
    return stats


def _calculate_diagnosis_statistics(cohort_id: str, connection=None) -> Dict[str, Any]:
    """Calculate statistics for diagnosis data."""
    conn = connection or get_connection()
    stats = {}
    
    try:
        # Top diagnoses
        result = conn.execute("""
            SELECT code, description, COUNT(*) as count
            FROM diagnoses
            WHERE cohort_id = ?
            GROUP BY code, description
            ORDER BY count DESC
            LIMIT 5
        """, [cohort_id]).fetchall()
        
        if result:
            stats['top_diagnoses'] = [
                {'code': row[0], 'description': row[1], 'count': row[2]}
                for row in result if row[0]
            ]
        
    except Exception:
        pass
    
    return stats


def _get_diverse_samples(
    cohort_id: str,
    entity_type: str,
    table_name: str,
    count: int = 3,
    connection=None,
) -> List[Dict]:
    """
    Get diverse sample entities for pattern consistency.
    
    Tries to select samples that show variety (e.g., different genders,
    age ranges, conditions) rather than just random selection.
    """
    conn = connection or get_connection()
    samples = []
    
    try:
        # Get column names for this table
        columns_result = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        columns = [col[1] for col in columns_result]
        
        # Simple diverse sampling: order by created_at and take evenly spaced
        result = conn.execute(f"""
            SELECT * FROM {table_name}
            WHERE cohort_id = ?
            ORDER BY created_at
        """, [cohort_id]).fetchall()
        
        if result:
            total = len(result)
            if total <= count:
                indices = list(range(total))
            else:
                # Take evenly spaced samples
                step = total / count
                indices = [int(i * step) for i in range(count)]
            
            for idx in indices:
                row = result[idx]
                sample = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    # Convert special types to strings
                    if isinstance(value, (datetime, date)):
                        value = str(value)
                    elif isinstance(value, UUID):
                        value = str(value)
                    # Skip internal columns
                    if col not in ('cohort_id', 'created_at', 'generation_seed'):
                        sample[col] = value
                samples.append(sample)
        
    except Exception:
        pass
    
    return samples


def generate_summary(
    cohort_id: str,
    include_samples: bool = True,
    samples_per_type: int = 3,
    connection=None,
) -> CohortSummary:
    """
    Generate a token-efficient summary of a cohort.
    
    Args:
        cohort_id: UUID of the cohort
        include_samples: Whether to include sample entities
        samples_per_type: Number of samples per major entity type
        connection: Optional database connection
        
    Returns:
        CohortSummary with counts, statistics, and optional samples
        
    Target token budget:
    - Without samples: ~500 tokens
    - With samples: ~3,500 tokens
    """
    conn = connection or get_connection()
    
    # Get cohort metadata
    result = conn.execute("""
        SELECT id, name, description, created_at, updated_at
        FROM cohorts
        WHERE id = ?
    """, [cohort_id]).fetchone()
    
    if not result:
        raise ValueError(f"Cohort not found: {cohort_id}")
    
    summary = CohortSummary(
        cohort_id=str(result[0]),
        name=result[1],
        description=result[2],
        created_at=result[3],
        updated_at=result[4],
    )
    
    # Get tags
    tags_result = conn.execute("""
        SELECT tag FROM cohort_tags
        WHERE cohort_id = ?
        ORDER BY tag
    """, [cohort_id]).fetchall()
    summary.tags = [row[0] for row in tags_result]
    
    # Get entity counts
    summary.entity_counts = _get_entity_counts(cohort_id, conn)
    
    # Calculate statistics based on what entities exist
    statistics = {}
    
    if summary.entity_counts.get('patients', 0) > 0:
        statistics.update(_calculate_patient_statistics(cohort_id, conn))
    
    if summary.entity_counts.get('encounters', 0) > 0:
        statistics.update(_calculate_encounter_statistics(cohort_id, conn))
    
    if summary.entity_counts.get('claims', 0) > 0:
        statistics.update(_calculate_claims_statistics(cohort_id, conn))
    
    if summary.entity_counts.get('diagnoses', 0) > 0:
        statistics.update(_calculate_diagnosis_statistics(cohort_id, conn))
    
    summary.statistics = statistics
    
    # Get samples if requested
    if include_samples:
        samples = {}
        
        # Sample major entity types that have data
        sample_types = [
            ('patients', 'patients'),
            ('encounters', 'encounters'),
            ('members', 'members'),
            ('claims', 'claims'),
            ('subjects', 'subjects'),
            ('prescriptions', 'prescriptions'),
        ]
        
        for entity_type, table_name in sample_types:
            if summary.entity_counts.get(entity_type, 0) > 0:
                entity_samples = _get_diverse_samples(
                    cohort_id, entity_type, table_name,
                    count=samples_per_type, connection=conn
                )
                if entity_samples:
                    samples[entity_type] = entity_samples
        
        summary.samples = samples
    
    return summary


def get_cohort_by_name(
    name: str,
    connection=None,
) -> Optional[str]:
    """
    Find cohort ID by name (fuzzy match).
    
    Args:
        name: Cohort name to search for
        connection: Optional database connection
        
    Returns:
        Cohort ID if found, None otherwise
    """
    conn = connection or get_connection()
    
    # Try exact match first
    result = conn.execute("""
        SELECT id FROM cohorts
        WHERE name = ?
    """, [name]).fetchone()
    
    if result:
        return str(result[0])
    
    # Try case-insensitive match
    result = conn.execute("""
        SELECT id FROM cohorts
        WHERE LOWER(name) = LOWER(?)
    """, [name]).fetchone()
    
    if result:
        return str(result[0])
    
    # Try contains match
    result = conn.execute("""
        SELECT id FROM cohorts
        WHERE LOWER(name) LIKE LOWER(?)
        ORDER BY updated_at DESC
        LIMIT 1
    """, [f"%{name}%"]).fetchone()
    
    if result:
        return str(result[0])
    
    return None
