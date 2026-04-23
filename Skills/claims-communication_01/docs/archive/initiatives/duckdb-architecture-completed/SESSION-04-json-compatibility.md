# Session 04: JSON Compatibility

**Initiative**: DuckDB Unified Data Architecture  
**Phase**: 1 - Foundation  
**Estimated Duration**: 30-45 minutes  
**Prerequisites**: SESSION-01, SESSION-02, SESSION-03 complete

---

## Objective

Add JSON export and import capabilities to maintain compatibility with sharing workflows. Users should be able to export cohorts to JSON for sharing and import JSON cohorts from external sources.

---

## Context

With state management now in DuckDB, we need to preserve the ability to:
1. Export cohorts to JSON for sharing via email, Slack, etc.
2. Import JSON cohorts received from others
3. Maintain backward compatibility with existing JSON-based tutorials/examples

### Reference Documents

```
docs/initiatives/duckdb-architecture/MASTER-PLAN.md
packages/core/healthsim/state/legacy.py              # From SESSION-03
docs/state-management/specification.md
```

---

## Pre-Flight Checklist

- [ ] SESSION-03 complete (state management working with DuckDB)
- [ ] Verify save/load works: test with a simple cohort
- [ ] Git status clean

---

## Deliverables

### 1. New MCP Tools

| Tool | Description |
|------|-------------|
| `export_cohort_json` | Export cohort to JSON file |
| `import_cohort_json` | Import JSON file to database |

### 2. Updated State Manager

Add export/import methods to StateManager class.

### 3. Tests

```
packages/core/tests/state/test_json_compat.py
```

---

## Implementation Steps

### Step 1: Add Export/Import to StateManager

```python
# Add to packages/core/healthsim/state/manager.py

def export_to_json(
    self,
    name_or_id: str,
    output_path: Optional[Path] = None
) -> Path:
    """
    Export a cohort to JSON file.
    
    Args:
        name_or_id: Cohort name or UUID
        output_path: Where to save (default: ~/Downloads/{name}.json)
        
    Returns:
        Path to exported file
    """
    from .legacy import export_to_json as _export
    
    cohort = self.load_cohort(name_or_id)
    
    if output_path is None:
        downloads = Path.home() / "Downloads"
        downloads.mkdir(exist_ok=True)
        output_path = downloads / f"{cohort['name']}.json"
    
    return _export(cohort, output_path)


def import_from_json(
    self,
    json_path: Path,
    name: Optional[str] = None,
    overwrite: bool = False
) -> str:
    """
    Import a cohort from JSON file.
    
    Args:
        json_path: Path to JSON file
        name: Override cohort name (default: use filename or embedded name)
        overwrite: Replace existing cohort with same name
        
    Returns:
        Cohort ID
    """
    from .legacy import import_from_json as _import
    
    data = _import(json_path)
    
    # Determine name
    cohort_name = name or data.get('name') or json_path.stem
    
    # Extract entities
    entities = data.get('entities', {})
    
    # If old format, entities might be at top level
    if not entities and 'patient' in data:
        entities = {k: v for k, v in data.items() 
                    if k in self.ENTITY_TYPES or k + 's' in [t + 's' for t in self.ENTITY_TYPES]}
    
    return self.save_cohort(
        name=cohort_name,
        entities=entities,
        description=data.get('description'),
        tags=data.get('tags'),
        overwrite=overwrite
    )
```

### Step 2: Add MCP Tool Handlers

Update the MCP server to expose these new tools:

```python
# In the MCP tool definitions

@tool("export_cohort_json")
def export_cohort_json(
    name: str,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Export a cohort to JSON file for sharing.
    
    Args:
        name: Cohort name or ID to export
        output_path: Where to save (optional, defaults to Downloads)
        
    Returns:
        file_path: Path to exported JSON
        entity_count: Number of entities exported
    """
    manager = get_manager()
    path = manager.export_to_json(
        name,
        Path(output_path) if output_path else None
    )
    
    # Get entity count
    cohort = manager.load_cohort(name)
    entity_count = sum(len(v) for v in cohort['entities'].values())
    
    return {
        "file_path": str(path),
        "entity_count": entity_count,
        "message": f"Exported cohort '{name}' to {path}"
    }


@tool("import_cohort_json")
def import_cohort_json(
    file_path: str,
    name: Optional[str] = None,
    overwrite: bool = False
) -> Dict[str, Any]:
    """
    Import a cohort from JSON file.
    
    Args:
        file_path: Path to JSON file
        name: Override cohort name (optional)
        overwrite: Replace existing if name conflicts
        
    Returns:
        cohort_id: ID of imported cohort
        name: Name of imported cohort
        entity_count: Number of entities imported
    """
    manager = get_manager()
    cohort_id = manager.import_from_json(
        Path(file_path),
        name=name,
        overwrite=overwrite
    )
    
    # Get details
    cohort = manager.load_cohort(cohort_id)
    entity_count = sum(len(v) for v in cohort['entities'].values())
    
    return {
        "cohort_id": cohort_id,
        "name": cohort['name'],
        "entity_count": entity_count,
        "message": f"Imported cohort '{cohort['name']}' with {entity_count} entities"
    }
```

### Step 3: Update Skills Documentation

Add to `skills/common/state-management.md`:

```markdown
## Sharing Cohorts

### Export for Sharing

```
User: "Export my diabetes-cohort cohort as JSON"
Claude: [Uses export_cohort_json tool]
        "Exported to ~/Downloads/diabetes-cohort.json (150 entities)"
```

### Import from JSON

```
User: "Import the cohort from /path/to/cohort.json"
Claude: [Uses import_cohort_json tool]
        "Imported cohort 'imported-cohort' with 75 entities"
```

### Format Compatibility

Exported JSON maintains the same format as previous HealthSim versions,
ensuring cohorts can be shared between different installations.
```

### Step 4: Write Tests

```python
# packages/core/tests/state/test_json_compat.py
"""Tests for JSON export/import compatibility."""

import pytest
import json
from pathlib import Path
import tempfile

from healthsim.state.manager import StateManager


@pytest.fixture
def state_manager(tmp_path):
    """Create state manager with test database."""
    # ... setup
    yield StateManager()


@pytest.fixture
def sample_cohort():
    """Sample cohort data."""
    return {
        'patient': [{
            'patient_id': '123e4567-e89b-12d3-a456-426614174000',
            'given_name': 'Test',
            'family_name': 'Patient',
            'date_of_birth': '1980-05-15',
            'gender': 'female'
        }],
        'encounter': [{
            'encounter_id': '223e4567-e89b-12d3-a456-426614174001',
            'patient_id': '123e4567-e89b-12d3-a456-426614174000',
            'encounter_type': 'outpatient',
            'admit_datetime': '2024-01-15T10:00:00'
        }]
    }


def test_export_to_json(state_manager, sample_cohort, tmp_path):
    """Test exporting cohort to JSON."""
    state_manager.save_cohort('export-test', sample_cohort)
    
    output_path = tmp_path / "exported.json"
    result_path = state_manager.export_to_json('export-test', output_path)
    
    assert result_path.exists()
    
    with open(result_path) as f:
        data = json.load(f)
    
    assert data['name'] == 'export-test'
    assert len(data['entities']['patient']) == 1
    assert data['entities']['patient'][0]['given_name'] == 'Test'


def test_import_from_json(state_manager, tmp_path):
    """Test importing cohort from JSON."""
    # Create a JSON file
    json_data = {
        'name': 'imported-cohort',
        'description': 'Test import',
        'entities': {
            'patient': [{
                'patient_id': '333e4567-e89b-12d3-a456-426614174002',
                'given_name': 'Imported',
                'family_name': 'Patient'
            }]
        }
    }
    
    json_path = tmp_path / "import-test.json"
    with open(json_path, 'w') as f:
        json.dump(json_data, f)
    
    cohort_id = state_manager.import_from_json(json_path)
    
    loaded = state_manager.load_cohort(cohort_id)
    assert loaded['name'] == 'imported-cohort'
    assert len(loaded['entities']['patient']) == 1


def test_round_trip(state_manager, sample_cohort, tmp_path):
    """Test export then import preserves data."""
    # Save original
    state_manager.save_cohort('round-trip-test', sample_cohort)
    
    # Export
    json_path = tmp_path / "round-trip.json"
    state_manager.export_to_json('round-trip-test', json_path)
    
    # Delete original
    state_manager.delete_cohort('round-trip-test')
    
    # Import
    state_manager.import_from_json(json_path, name='round-trip-restored')
    
    # Verify
    restored = state_manager.load_cohort('round-trip-restored')
    assert len(restored['entities']['patient']) == 1
    assert restored['entities']['patient'][0]['given_name'] == 'Test'


def test_import_legacy_format(state_manager, tmp_path):
    """Test importing old-style JSON (entities at top level)."""
    legacy_json = {
        'name': 'legacy-cohort',
        'patient': [{'given_name': 'Legacy', 'family_name': 'Patient'}],
        'encounter': []
    }
    
    json_path = tmp_path / "legacy.json"
    with open(json_path, 'w') as f:
        json.dump(legacy_json, f)
    
    cohort_id = state_manager.import_from_json(json_path)
    loaded = state_manager.load_cohort(cohort_id)
    
    assert loaded['entities']['patient'][0]['given_name'] == 'Legacy'
```

### Step 5: Run Tests

```bash
cd packages/core
source .venv/bin/activate
pytest tests/state/test_json_compat.py -v
pytest tests/ -v  # All tests
```

---

## Post-Flight Checklist

- [ ] export_to_json creates valid JSON file
- [ ] import_from_json loads JSON into database
- [ ] Round-trip (export → import) preserves data
- [ ] Legacy JSON format handled
- [ ] MCP tools exposed
- [ ] Skills documentation updated
- [ ] All tests pass

---

## Commit

```bash
git add -A
git commit -m "[State] Add JSON export/import for cohort sharing

- Add export_to_json method to StateManager
- Add import_from_json method to StateManager
- Support legacy JSON format (entities at top level)
- Add MCP tools: export_cohort_json, import_cohort_json
- Update state-management skill documentation
- Add JSON compatibility tests

Part of: DuckDB Unified Data Architecture initiative"

git push
```

---

## Update MASTER-PLAN.md

Mark SESSION-04 as complete with commit hash.

---

## Success Criteria

✅ Session complete when:
1. Can export any cohort to JSON file
2. Can import JSON file to database
3. Round-trip preserves all entity data
4. Legacy JSON format supported
5. MCP tools working
6. Documentation updated
7. All tests pass
8. Committed and pushed

---

## Next Session

Proceed to [SESSION-05: Migration Tool](SESSION-05-migration-tool.md)
