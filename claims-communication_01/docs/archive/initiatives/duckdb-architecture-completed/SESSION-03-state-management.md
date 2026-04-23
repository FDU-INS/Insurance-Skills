# Session 03: State Management Migration

**Initiative**: DuckDB Unified Data Architecture  
**Phase**: 1 - Foundation  
**Estimated Duration**: 60-90 minutes  
**Prerequisites**: SESSION-01, SESSION-02 complete

---

## Objective

Update the state management MCP tools to use DuckDB as the backend instead of JSON files. This is the core migration that changes how cohorts are saved, loaded, and queried.

---

## Context

Current state management uses JSON files in `~/.healthsim/cohorts/`. This session migrates to DuckDB while maintaining the same MCP tool interface so existing skills and workflows continue to work.

### Current MCP Tools (from specification.md)

| Tool | Current Behavior | New Behavior |
|------|------------------|--------------|
| `save_cohort` | Write JSON file | INSERT to DuckDB |
| `load_cohort` | Read JSON file | SELECT from DuckDB |
| `list_cohorts` | List directory | Query cohorts table |
| `delete_cohort` | Delete JSON file | DELETE from tables |

### Reference Documents

```
docs/initiatives/duckdb-architecture/MASTER-PLAN.md
docs/state-management/specification.md              # Current MCP specs
packages/core/healthsim/state/manager.py            # Current implementation
skills/common/state-management.md                   # Current skill
packages/core/healthsim/db/                         # From SESSION-01
```

---

## Pre-Flight Checklist

- [ ] SESSION-01 and SESSION-02 complete
- [ ] Verify database exists: `ls -la ~/.healthsim/healthsim.duckdb`
- [ ] Current state manager working: test with `save_cohort`/`load_cohort`
- [ ] Read current manager.py implementation
- [ ] Note any existing JSON cohorts to migrate later

---

## Deliverables

### 1. Updated State Manager

```
packages/core/healthsim/state/
├── __init__.py
├── manager.py               # Updated for DuckDB
├── entities.py              # Entity serialization helpers
└── legacy.py                # JSON compatibility (moved from manager.py)
```

### 2. Updated MCP Tool Handlers

The MCP server files that call the state manager need updates if they directly reference JSON paths.

### 3. Tests

```
packages/core/tests/state/
├── test_manager.py          # Updated tests
├── test_entities.py         # Entity serialization tests
└── test_legacy.py           # JSON compatibility tests
```

---

## Implementation Steps

### Step 1: Create Entity Serialization Module

```python
# packages/core/healthsim/state/entities.py
"""
Entity serialization between canonical models and database.

Handles the mapping between in-memory patient/encounter/etc. objects
and their database representations.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
import json
from datetime import datetime

import duckdb


def serialize_patient(patient: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare a patient dict for database insertion.
    
    Ensures all required fields exist and types are correct.
    """
    return {
        'patient_id': patient.get('patient_id') or str(uuid4()),
        'mrn': patient.get('mrn'),
        'ssn': patient.get('ssn'),
        'given_name': patient.get('given_name') or patient.get('name', {}).get('given'),
        'family_name': patient.get('family_name') or patient.get('name', {}).get('family'),
        'date_of_birth': patient.get('date_of_birth') or patient.get('birthDate'),
        'gender': patient.get('gender'),
        'race': patient.get('race'),
        'ethnicity': patient.get('ethnicity'),
        'address_line1': _get_nested(patient, 'address', 'line1'),
        'address_line2': _get_nested(patient, 'address', 'line2'),
        'city': _get_nested(patient, 'address', 'city'),
        'state': _get_nested(patient, 'address', 'state'),
        'postal_code': _get_nested(patient, 'address', 'postalCode'),
        'phone': _get_nested(patient, 'telecom', 'phone'),
        'email': _get_nested(patient, 'telecom', 'email'),
        'created_at': datetime.utcnow(),
        'source_type': patient.get('_provenance', {}).get('source_type', 'generated'),
        'source_system': patient.get('_provenance', {}).get('source_system', 'patientsim'),
        'skill_used': patient.get('_provenance', {}).get('skill_used'),
        'generation_seed': patient.get('_provenance', {}).get('seed'),
    }


def deserialize_patient(row: tuple, columns: List[str]) -> Dict[str, Any]:
    """
    Convert a database row back to canonical patient format.
    """
    data = dict(zip(columns, row))
    return {
        'patient_id': data['patient_id'],
        'mrn': data['mrn'],
        'ssn': data['ssn'],
        'name': {
            'given': data['given_name'],
            'family': data['family_name'],
        },
        'birthDate': str(data['date_of_birth']) if data['date_of_birth'] else None,
        'gender': data['gender'],
        'race': data['race'],
        'ethnicity': data['ethnicity'],
        'address': {
            'line1': data['address_line1'],
            'line2': data['address_line2'],
            'city': data['city'],
            'state': data['state'],
            'postalCode': data['postal_code'],
        },
        'telecom': {
            'phone': data['phone'],
            'email': data['email'],
        },
        '_provenance': {
            'source_type': data['source_type'],
            'source_system': data['source_system'],
            'skill_used': data['skill_used'],
            'seed': data['generation_seed'],
        }
    }


def _get_nested(obj: Dict, *keys) -> Any:
    """Safely get nested dictionary value."""
    for key in keys:
        if obj is None or not isinstance(obj, dict):
            return None
        obj = obj.get(key)
    return obj


# Similar serialize/deserialize functions for:
# - encounters
# - diagnoses
# - procedures
# - medications
# - lab_results
# - vital_signs
# - clinical_notes
# - members
# - claims
# - claim_lines
# - prescriptions
# - subjects
# - trial_visits
```

### Step 2: Update State Manager

```python
# packages/core/healthsim/state/manager.py
"""
HealthSim State Manager - DuckDB Backend.

Provides save/load/list/delete operations for cohorts.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime
import json

from ..db import get_connection
from .entities import (
    serialize_patient, deserialize_patient,
    serialize_encounter, deserialize_encounter,
    # ... other entity types
)


class StateManager:
    """Manages cohort persistence in DuckDB."""
    
    ENTITY_TYPES = [
        'patient', 'encounter', 'diagnosis', 'procedure',
        'medication', 'lab_result', 'vital_sign', 'clinical_note',
        'member', 'claim', 'claim_line', 'prescription',
        'subject', 'trial_visit'
    ]
    
    def __init__(self):
        self.conn = get_connection()
    
    def save_cohort(
        self,
        name: str,
        entities: Dict[str, List[Dict]],
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        overwrite: bool = False
    ) -> str:
        """
        Save a cohort to the database.
        
        Args:
            name: Unique cohort name
            entities: Dict mapping entity type to list of entities
            description: Optional description
            tags: Optional list of tags
            overwrite: If True, replace existing cohort with same name
            
        Returns:
            Cohort ID (UUID string)
        """
        # Check for existing cohort
        existing = self._get_cohort_by_name(name)
        if existing and not overwrite:
            raise ValueError(f"Cohort '{name}' already exists. Use overwrite=True to replace.")
        
        cohort_id = existing['cohort_id'] if existing else str(uuid4())
        
        if existing and overwrite:
            self._delete_cohort_entities(cohort_id)
        
        # Create or update cohort record
        self.conn.execute("""
            INSERT INTO cohorts (cohort_id, name, description, created_at, updated_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (cohort_id) DO UPDATE SET
                name = excluded.name,
                description = excluded.description,
                updated_at = excluded.updated_at
        """, [cohort_id, name, description, datetime.utcnow(), datetime.utcnow(), False])
        
        # Insert entities and link to cohort
        entity_count = 0
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                entity_id = self._save_entity(entity_type, entity)
                self._link_entity_to_cohort(cohort_id, entity_type, entity_id)
                entity_count += 1
        
        # Update entity count
        self.conn.execute("""
            UPDATE cohorts SET entity_count = ? WHERE cohort_id = ?
        """, [entity_count, cohort_id])
        
        # Save tags
        if tags:
            for tag in tags:
                self.conn.execute("""
                    INSERT INTO cohort_tags (cohort_id, tag)
                    VALUES (?, ?)
                    ON CONFLICT DO NOTHING
                """, [cohort_id, tag])
        
        return cohort_id
    
    def load_cohort(self, name_or_id: str) -> Dict[str, Any]:
        """
        Load a cohort from the database.
        
        Args:
            name_or_id: Cohort name or UUID
            
        Returns:
            Dict with cohort metadata and entities
        """
        # Try as UUID first, then as name
        cohort = self._get_cohort_by_id(name_or_id)
        if not cohort:
            cohort = self._get_cohort_by_name(name_or_id)
        if not cohort:
            raise ValueError(f"Cohort '{name_or_id}' not found")
        
        cohort_id = cohort['cohort_id']
        
        # Load all entities for this cohort
        entities = {}
        for entity_type in self.ENTITY_TYPES:
            entities[entity_type] = self._load_entities_for_cohort(cohort_id, entity_type)
        
        # Load tags
        tags = self.conn.execute("""
            SELECT tag FROM cohort_tags WHERE cohort_id = ?
        """, [cohort_id]).fetchall()
        
        return {
            'cohort_id': cohort_id,
            'name': cohort['name'],
            'description': cohort['description'],
            'created_at': cohort['created_at'],
            'updated_at': cohort['updated_at'],
            'entity_count': cohort['entity_count'],
            'tags': [t[0] for t in tags],
            'entities': entities
        }
    
    def list_cohorts(
        self,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List available cohorts.
        
        Args:
            tag: Filter by tag
            search: Search in name/description
            limit: Max results
            
        Returns:
            List of cohort summaries
        """
        query = """
            SELECT s.cohort_id, s.name, s.description, s.created_at, 
                   s.updated_at, s.entity_count, s.is_active
            FROM cohorts s
        """
        params = []
        
        if tag:
            query += " JOIN cohort_tags t ON s.cohort_id = t.cohort_id WHERE t.tag = ?"
            params.append(tag)
        elif search:
            query += " WHERE s.name LIKE ? OR s.description LIKE ?"
            params.extend([f"%{search}%", f"%{search}%"])
        
        query += " ORDER BY s.updated_at DESC LIMIT ?"
        params.append(limit)
        
        results = self.conn.execute(query, params).fetchall()
        columns = ['cohort_id', 'name', 'description', 'created_at', 
                   'updated_at', 'entity_count', 'is_active']
        
        return [dict(zip(columns, row)) for row in results]
    
    def delete_cohort(self, name_or_id: str) -> bool:
        """
        Delete a cohort.
        
        Note: This only removes the cohort metadata and entity links.
        The actual entity data remains in canonical tables.
        
        Args:
            name_or_id: Cohort name or UUID
            
        Returns:
            True if deleted, False if not found
        """
        cohort = self._get_cohort_by_id(name_or_id) or self._get_cohort_by_name(name_or_id)
        if not cohort:
            return False
        
        cohort_id = cohort['cohort_id']
        
        # Delete in order: tags, entity links, cohort
        self.conn.execute("DELETE FROM cohort_tags WHERE cohort_id = ?", [cohort_id])
        self.conn.execute("DELETE FROM cohort_entities WHERE cohort_id = ?", [cohort_id])
        self.conn.execute("DELETE FROM cohorts WHERE cohort_id = ?", [cohort_id])
        
        return True
    
    # --- Private helper methods ---
    
    def _get_cohort_by_name(self, name: str) -> Optional[Dict]:
        """Get cohort by name."""
        result = self.conn.execute(
            "SELECT * FROM cohorts WHERE name = ?", [name]
        ).fetchone()
        if result:
            columns = ['cohort_id', 'name', 'description', 'created_at', 
                       'updated_at', 'last_accessed_at', 'entity_count', 
                       'patient_count', 'is_active', 'is_analytics_ready',
                       'healthsim_version', 'schema_version']
            return dict(zip(columns, result))
        return None
    
    def _get_cohort_by_id(self, cohort_id: str) -> Optional[Dict]:
        """Get cohort by ID."""
        try:
            result = self.conn.execute(
                "SELECT * FROM cohorts WHERE cohort_id = ?", [cohort_id]
            ).fetchone()
            if result:
                columns = ['cohort_id', 'name', 'description', 'created_at', 
                           'updated_at', 'last_accessed_at', 'entity_count', 
                           'patient_count', 'is_active', 'is_analytics_ready',
                           'healthsim_version', 'schema_version']
                return dict(zip(columns, result))
        except:
            pass
        return None
    
    def _save_entity(self, entity_type: str, entity: Dict) -> str:
        """Save entity to appropriate canonical table, return entity_id."""
        # Route to appropriate serializer and table
        table_name = f"{entity_type}s"  # patients, encounters, etc.
        
        if entity_type == 'patient':
            data = serialize_patient(entity)
        elif entity_type == 'encounter':
            data = serialize_encounter(entity)
        # ... handle other entity types
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        entity_id = data.get(f'{entity_type}_id')
        
        # Build INSERT ... ON CONFLICT UPDATE
        columns = list(data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        updates = ', '.join([f"{col} = excluded.{col}" for col in columns if col != f'{entity_type}_id'])
        
        self.conn.execute(f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT ({entity_type}_id) DO UPDATE SET {updates}
        """, list(data.values()))
        
        return entity_id
    
    def _link_entity_to_cohort(self, cohort_id: str, entity_type: str, entity_id: str):
        """Create link between cohort and entity."""
        self.conn.execute("""
            INSERT INTO cohort_entities (cohort_id, entity_type, entity_id)
            VALUES (?, ?, ?)
            ON CONFLICT DO NOTHING
        """, [cohort_id, entity_type, entity_id])
    
    def _load_entities_for_cohort(self, cohort_id: str, entity_type: str) -> List[Dict]:
        """Load all entities of a type for a cohort."""
        table_name = f"{entity_type}s"
        
        # Get entity IDs linked to this cohort
        entity_ids = self.conn.execute("""
            SELECT entity_id FROM cohort_entities 
            WHERE cohort_id = ? AND entity_type = ?
        """, [cohort_id, entity_type]).fetchall()
        
        if not entity_ids:
            return []
        
        # Load entity data
        id_list = [eid[0] for eid in entity_ids]
        placeholders = ', '.join(['?' for _ in id_list])
        
        results = self.conn.execute(f"""
            SELECT * FROM {table_name} WHERE {entity_type}_id IN ({placeholders})
        """, id_list).fetchall()
        
        # Get column names
        columns = [desc[0] for desc in self.conn.description]
        
        # Deserialize
        if entity_type == 'patient':
            return [deserialize_patient(row, columns) for row in results]
        elif entity_type == 'encounter':
            return [deserialize_encounter(row, columns) for row in results]
        # ... handle other entity types
        
        return []
    
    def _delete_cohort_entities(self, cohort_id: str):
        """Remove all entity links for a cohort (for overwrite)."""
        self.conn.execute(
            "DELETE FROM cohort_entities WHERE cohort_id = ?", 
            [cohort_id]
        )


# Module-level convenience functions (maintain backward compatibility)
_manager = None

def get_manager() -> StateManager:
    """Get singleton state manager instance."""
    global _manager
    if _manager is None:
        _manager = StateManager()
    return _manager

def save_cohort(name: str, entities: Dict, **kwargs) -> str:
    """Convenience function for save_cohort."""
    return get_manager().save_cohort(name, entities, **kwargs)

def load_cohort(name_or_id: str) -> Dict:
    """Convenience function for load_cohort."""
    return get_manager().load_cohort(name_or_id)

def list_cohorts(**kwargs) -> List[Dict]:
    """Convenience function for list_cohorts."""
    return get_manager().list_cohorts(**kwargs)

def delete_cohort(name_or_id: str) -> bool:
    """Convenience function for delete_cohort."""
    return get_manager().delete_cohort(name_or_id)
```

### Step 3: Move Legacy JSON Support

```python
# packages/core/healthsim/state/legacy.py
"""
Legacy JSON file support for backward compatibility.

Used for:
- Exporting cohorts to JSON for sharing
- Importing JSON cohorts from external sources
- Reading old JSON cohorts during migration
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


LEGACY_SCENARIOS_PATH = Path.home() / ".healthsim" / "cohorts"


def export_to_json(cohort: Dict[str, Any], output_path: Path) -> Path:
    """
    Export a cohort to JSON file.
    
    Args:
        cohort: Cohort dict from load_cohort()
        output_path: Where to write the file
        
    Returns:
        Path to written file
    """
    # Convert datetime objects to ISO strings
    cohort_copy = _serialize_for_json(cohort)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(cohort_copy, f, indent=2, default=str)
    
    return output_path


def import_from_json(json_path: Path) -> Dict[str, Any]:
    """
    Read a cohort from JSON file.
    
    Args:
        json_path: Path to JSON file
        
    Returns:
        Cohort dict ready for save_cohort()
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    return data


def list_legacy_cohorts() -> List[Dict[str, Any]]:
    """
    List JSON cohorts in legacy location.
    
    Returns:
        List of {name, path, modified_at}
    """
    if not LEGACY_SCENARIOS_PATH.exists():
        return []
    
    cohorts = []
    for json_file in LEGACY_SCENARIOS_PATH.glob("*.json"):
        cohorts.append({
            'name': json_file.stem,
            'path': json_file,
            'modified_at': datetime.fromtimestamp(json_file.stat().st_mtime)
        })
    
    return sorted(cohorts, key=lambda x: x['modified_at'], reverse=True)


def _serialize_for_json(obj: Any) -> Any:
    """Recursively convert non-JSON-serializable objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: _serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_serialize_for_json(item) for item in obj]
    return obj
```

### Step 4: Update Tests

Create comprehensive tests for the new state manager:

```python
# packages/core/tests/state/test_manager.py
"""Tests for DuckDB-backed state manager."""

import pytest
from datetime import datetime
import tempfile
from pathlib import Path

from healthsim.db import DatabaseConnection
from healthsim.state.manager import StateManager


@pytest.fixture
def state_manager(tmp_path):
    """Create state manager with test database."""
    db_path = tmp_path / "test.duckdb"
    # Temporarily override the database connection
    # ... setup code
    yield StateManager()
    # ... cleanup


def test_save_and_load_cohort(state_manager):
    """Test basic save and load cycle."""
    entities = {
        'patient': [{
            'patient_id': '123e4567-e89b-12d3-a456-426614174000',
            'given_name': 'John',
            'family_name': 'Doe',
            'date_of_birth': '1980-01-15',
            'gender': 'male'
        }],
        'encounter': []
    }
    
    cohort_id = state_manager.save_cohort(
        name='test-cohort',
        entities=entities,
        description='Test cohort'
    )
    
    assert cohort_id is not None
    
    loaded = state_manager.load_cohort('test-cohort')
    assert loaded['name'] == 'test-cohort'
    assert len(loaded['entities']['patient']) == 1
    assert loaded['entities']['patient'][0]['given_name'] == 'John'


def test_list_cohorts(state_manager):
    """Test listing cohorts."""
    state_manager.save_cohort('cohort-1', {'patient': []})
    state_manager.save_cohort('cohort-2', {'patient': []})
    
    cohorts = state_manager.list_cohorts()
    assert len(cohorts) >= 2
    
    names = [s['name'] for s in cohorts]
    assert 'cohort-1' in names
    assert 'cohort-2' in names


def test_delete_cohort(state_manager):
    """Test cohort deletion."""
    state_manager.save_cohort('to-delete', {'patient': []})
    
    result = state_manager.delete_cohort('to-delete')
    assert result is True
    
    cohorts = state_manager.list_cohorts()
    names = [s['name'] for s in cohorts]
    assert 'to-delete' not in names


def test_overwrite_cohort(state_manager):
    """Test overwriting existing cohort."""
    state_manager.save_cohort('overwrite-test', {'patient': [{'given_name': 'First'}]})
    state_manager.save_cohort('overwrite-test', {'patient': [{'given_name': 'Second'}]}, overwrite=True)
    
    loaded = state_manager.load_cohort('overwrite-test')
    assert loaded['entities']['patient'][0]['given_name'] == 'Second'


def test_cohort_tags(state_manager):
    """Test tag filtering."""
    state_manager.save_cohort('tagged', {'patient': []}, tags=['diabetes', 'test'])
    
    cohorts = state_manager.list_cohorts(tag='diabetes')
    assert any(s['name'] == 'tagged' for s in cohorts)
    
    cohorts = state_manager.list_cohorts(tag='nonexistent')
    assert not any(s['name'] == 'tagged' for s in cohorts)
```

### Step 5: Run Full Test Suite

```bash
cd packages/core
source .venv/bin/activate

# Run state management tests
pytest tests/state/ -v

# Run all tests
pytest tests/ -v
```

---

## Post-Flight Checklist

- [ ] StateManager class implemented with all methods
- [ ] Entity serialization/deserialization working
- [ ] save_cohort writes to DuckDB
- [ ] load_cohort reads from DuckDB
- [ ] list_cohorts queries work (with filters)
- [ ] delete_cohort removes cohort properly
- [ ] Overwrite functionality works
- [ ] Tags filtering works
- [ ] All new tests pass
- [ ] All existing tests pass (476+)

---

## Commit

```bash
git add -A
git commit -m "[State] Migrate state management to DuckDB backend

- Update StateManager to use DuckDB instead of JSON files
- Add entity serialization/deserialization module
- Move legacy JSON support to separate module
- Maintain same MCP tool interface
- Add comprehensive state management tests

Part of: DuckDB Unified Data Architecture initiative"

git push
```

---

## Update MASTER-PLAN.md

Mark SESSION-03 as complete with commit hash.

---

## Success Criteria

✅ Session complete when:
1. save_cohort writes entities to DuckDB tables
2. load_cohort retrieves entities correctly
3. list_cohorts shows database cohorts
4. delete_cohort removes from database
5. Entity data round-trips correctly (save → load = same data)
6. All tests pass
7. Committed and pushed

---

## Next Session

Proceed to [SESSION-04: JSON Compatibility](SESSION-04-json-compatibility.md)
