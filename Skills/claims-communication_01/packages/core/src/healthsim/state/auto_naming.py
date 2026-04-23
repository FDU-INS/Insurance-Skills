"""
Auto-naming service for HealthSim cohorts.

Generates descriptive cohort names from generation context,
following the pattern: {keywords}-{YYYYMMDD}

Examples:
    - "diabetes-patients-20241226"
    - "medicare-claims-20241226"
    - "cardiac-trial-subjects-20241226"
"""

from datetime import datetime
from typing import List, Optional, Set
import re

from ..db import get_connection


# Common words to exclude from auto-generated names
STOP_WORDS: Set[str] = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
    'some', 'any', 'no', 'not', 'all', 'each', 'every', 'both', 'few',
    'more', 'most', 'other', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'between', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself', 'we',
    'our', 'ours', 'you', 'your', 'yours', 'he', 'him', 'his', 'she',
    'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'what', 'which',
    'who', 'whom', 'generate', 'create', 'make', 'build', 'add', 'new',
    'please', 'want', 'like', 'need', 'help', 'show', 'give', 'get',
}

# Healthcare-relevant keywords to prioritize
HEALTHCARE_KEYWORDS: Set[str] = {
    # Conditions
    'diabetes', 'diabetic', 'hypertension', 'cardiac', 'heart', 'cancer',
    'oncology', 'copd', 'asthma', 'respiratory', 'renal', 'kidney',
    'hepatic', 'liver', 'neurological', 'stroke', 'alzheimer', 'dementia',
    'arthritis', 'obesity', 'depression', 'anxiety', 'mental', 'psychiatric',
    
    # Demographics
    'medicare', 'medicaid', 'pediatric', 'geriatric', 'elderly', 'adult',
    'child', 'infant', 'neonatal', 'pregnant', 'maternal', 'veteran',
    
    # Care settings
    'emergency', 'inpatient', 'outpatient', 'ambulatory', 'primary',
    'specialty', 'urgent', 'icu', 'surgical', 'rehabilitation',
    
    # Entity types
    'patient', 'patients', 'member', 'members', 'claim', 'claims',
    'encounter', 'encounters', 'prescription', 'prescriptions',
    'subject', 'subjects', 'trial', 'study', 'cohort',
    
    # Products
    'pharmacy', 'rx', 'drug', 'medication', 'lab', 'diagnostic',
}


def extract_keywords(
    context: Optional[str] = None,
    entity_type: Optional[str] = None,
    max_keywords: int = 3,
) -> List[str]:
    """
    Extract meaningful keywords from generation context.
    
    Args:
        context: Natural language generation request
        entity_type: Type of entity being generated
        max_keywords: Maximum keywords to return
        
    Returns:
        List of lowercase keywords, prioritizing healthcare terms
    """
    keywords: List[str] = []
    
    if context:
        # Tokenize and clean
        words = re.findall(r'[a-zA-Z]+', context.lower())
        
        # Filter stop words and short words
        candidates = [
            w for w in words 
            if w not in STOP_WORDS and len(w) >= 3
        ]
        
        # Prioritize healthcare keywords
        healthcare = [w for w in candidates if w in HEALTHCARE_KEYWORDS]
        other = [w for w in candidates if w not in HEALTHCARE_KEYWORDS]
        
        # Take healthcare keywords first, then others
        keywords = healthcare[:max_keywords]
        if len(keywords) < max_keywords:
            keywords.extend(other[:max_keywords - len(keywords)])
    
    # Add entity type if not already present
    if entity_type:
        # Normalize entity type
        entity_word = entity_type.lower().rstrip('s')  # Remove trailing 's'
        plural = entity_word + 's'
        
        # Add pluralized form if not already in keywords
        if plural not in keywords and entity_word not in keywords:
            keywords.append(plural)
    
    return keywords[:max_keywords]


def sanitize_name(name: str) -> str:
    """
    Sanitize a cohort name for safe storage.
    
    - Converts to lowercase
    - Replaces spaces and underscores with hyphens
    - Removes special characters
    - Limits length
    
    Args:
        name: Raw name string
        
    Returns:
        Sanitized name suitable for cohort identifier
    """
    # Lowercase
    name = name.lower()
    
    # Replace spaces and underscores with hyphens
    name = re.sub(r'[\s_]+', '-', name)
    
    # Remove non-alphanumeric except hyphens
    name = re.sub(r'[^a-z0-9-]', '', name)
    
    # Collapse multiple hyphens
    name = re.sub(r'-+', '-', name)
    
    # Strip leading/trailing hyphens
    name = name.strip('-')
    
    # Limit length (max 50 chars before date suffix)
    if len(name) > 50:
        name = name[:50].rstrip('-')
    
    return name


def ensure_unique_name(
    base_name: str,
    connection=None,
) -> str:
    """
    Ensure cohort name is unique by appending counter if needed.
    
    Args:
        base_name: Proposed cohort name
        connection: Optional database connection
        
    Returns:
        Unique cohort name (may have -2, -3, etc. suffix)
    """
    conn = connection or get_connection()
    
    # Check if base name exists
    result = conn.execute(
        "SELECT COUNT(*) FROM cohorts WHERE name = ?",
        [base_name]
    ).fetchone()
    
    if result[0] == 0:
        return base_name
    
    # Find next available number
    counter = 2
    while True:
        candidate = f"{base_name}-{counter}"
        result = conn.execute(
            "SELECT COUNT(*) FROM cohorts WHERE name = ?",
            [candidate]
        ).fetchone()
        
        if result[0] == 0:
            return candidate
        
        counter += 1
        
        # Safety limit
        if counter > 1000:
            # Fall back to timestamp
            timestamp = datetime.utcnow().strftime('%H%M%S')
            return f"{base_name}-{timestamp}"


def generate_cohort_name(
    keywords: Optional[List[str]] = None,
    context: Optional[str] = None,
    entity_type: Optional[str] = None,
    prefix: Optional[str] = None,
    include_date: bool = True,
    connection=None,
) -> str:
    """
    Generate a unique, descriptive cohort name.
    
    Priority for name components:
    1. Explicit keywords provided
    2. Keywords extracted from context
    3. Entity type
    4. Prefix (product name)
    5. Date suffix
    
    Args:
        keywords: Explicit keywords to include
        context: Natural language context to extract keywords from
        entity_type: Type of entity being generated
        prefix: Optional prefix (e.g., product name)
        include_date: Whether to append date (default True)
        connection: Optional database connection
        
    Returns:
        Unique cohort name like "diabetes-patients-20241226"
        
    Examples:
        >>> generate_cohort_name(context="Generate 50 diabetic patients over 65")
        "diabetic-patients-20241226"
        
        >>> generate_cohort_name(entity_type="claim", prefix="membersim")
        "membersim-claims-20241226"
    """
    parts: List[str] = []
    
    # Add prefix if provided
    if prefix:
        parts.append(sanitize_name(prefix))
    
    # Use explicit keywords or extract from context
    if keywords:
        parts.extend([sanitize_name(k) for k in keywords[:3]])
    elif context:
        extracted = extract_keywords(context, entity_type)
        parts.extend([sanitize_name(k) for k in extracted])
    elif entity_type:
        # Fall back to just entity type
        parts.append(sanitize_name(entity_type))
    
    # Build base name
    if not parts:
        parts = ['cohort']
    
    base_name = '-'.join(parts)
    
    # Add date suffix
    if include_date:
        date_suffix = datetime.utcnow().strftime('%Y%m%d')
        base_name = f"{base_name}-{date_suffix}"
    
    # Ensure uniqueness
    return ensure_unique_name(base_name, connection)


def parse_cohort_name(name: str) -> dict:
    """
    Parse a cohort name into its components.
    
    Args:
        name: Cohort name to parse
        
    Returns:
        Dict with 'keywords', 'date', 'counter' if present
        
    Example:
        >>> parse_cohort_name("diabetes-patients-20241226-2")
        {'keywords': ['diabetes', 'patients'], 'date': '20241226', 'counter': 2}
    """
    result = {'keywords': [], 'date': None, 'counter': None}
    
    parts = name.split('-')
    
    # Check for counter at end (numeric)
    if parts and parts[-1].isdigit() and len(parts[-1]) <= 3:
        result['counter'] = int(parts[-1])
        parts = parts[:-1]
    
    # Check for date (8 digits, starts with 20)
    if parts and len(parts[-1]) == 8 and parts[-1].startswith('20'):
        try:
            datetime.strptime(parts[-1], '%Y%m%d')
            result['date'] = parts[-1]
            parts = parts[:-1]
        except ValueError:
            pass
    
    # Remaining parts are keywords
    result['keywords'] = parts
    
    return result
