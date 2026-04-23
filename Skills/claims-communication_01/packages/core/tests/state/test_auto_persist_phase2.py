"""
Tests for Phase 2 Auto-Persist Enhancements.

Tests for:
- Tag management (add_tag, remove_tag, get_tags, list_all_tags, cohorts_by_tag)
- Cohort cloning (clone_cohort)
- Cohort merging (merge_cohorts)
- Export utilities (export_cohort, export_to_csv, export_to_json)

These tests complement test_auto_persist.py which covers Phase 1 functionality.
"""

import pytest
import json
import csv
import tempfile
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from healthsim.db import DatabaseConnection
from healthsim.state.auto_persist import (
    AutoPersistService,
    get_auto_persist_service,
    reset_service,
    CloneResult,
    MergeResult,
    ExportResult,
)


@pytest.fixture
def test_db():
    """Create a temporary test database with schema applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_phase2.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def service(test_db):
    """Create a fresh AutoPersistService for each test."""
    reset_service()
    return AutoPersistService(test_db)


@pytest.fixture
def sample_patients():
    """Sample patient data for testing."""
    return [
        {
            'patient_id': str(uuid4()),
            'given_name': 'John',
            'family_name': 'Doe',
            'gender': 'male',
            'birth_date': '1980-01-15',
        },
        {
            'patient_id': str(uuid4()),
            'given_name': 'Jane',
            'family_name': 'Smith',
            'gender': 'female',
            'birth_date': '1985-03-22',
        },
        {
            'patient_id': str(uuid4()),
            'given_name': 'Bob',
            'family_name': 'Johnson',
            'gender': 'male',
            'birth_date': '1975-07-10',
        },
    ]


@pytest.fixture
def populated_cohort(service, sample_patients):
    """Create a cohort with patients for testing."""
    result = service.persist_entities(
        entities=sample_patients,
        entity_type='patient',
        cohort_name='test-cohort',
        cohort_description='Test cohort for Phase 2 tests',
        tags=['initial', 'test'],
    )
    return result


# ============================================================================
# Tag Management Tests
# ============================================================================

class TestTagManagement:
    """Tests for tag management functionality."""
    
    def test_add_tag(self, service, populated_cohort):
        """Test adding a tag to a cohort."""
        cohort_id = populated_cohort.cohort_id
        
        # Add a new tag
        tags = service.add_tag(cohort_id, 'diabetes')
        
        assert 'diabetes' in tags
        assert 'initial' in tags
        assert 'test' in tags
        assert len(tags) == 3
    
    def test_add_tag_case_insensitive(self, service, populated_cohort):
        """Test that tags are stored lowercase."""
        cohort_id = populated_cohort.cohort_id
        
        tags = service.add_tag(cohort_id, 'UPPERCASE')
        
        assert 'uppercase' in tags
        assert 'UPPERCASE' not in tags
    
    def test_add_tag_idempotent(self, service, populated_cohort):
        """Test that adding the same tag twice doesn't create duplicates."""
        cohort_id = populated_cohort.cohort_id
        
        # Add same tag twice
        service.add_tag(cohort_id, 'duplicate')
        tags = service.add_tag(cohort_id, 'duplicate')
        
        # Count occurrences
        count = sum(1 for t in tags if t == 'duplicate')
        assert count == 1
    
    def test_add_tag_empty_raises_error(self, service, populated_cohort):
        """Test that adding an empty tag raises an error."""
        cohort_id = populated_cohort.cohort_id
        
        with pytest.raises(ValueError, match="cannot be empty"):
            service.add_tag(cohort_id, '')
    
    def test_add_tag_not_found_raises_error(self, service):
        """Test that adding a tag to non-existent cohort raises error."""
        with pytest.raises(ValueError, match="not found"):
            service.add_tag('nonexistent-id', 'tag')
    
    def test_remove_tag(self, service, populated_cohort):
        """Test removing a tag from a cohort."""
        cohort_id = populated_cohort.cohort_id
        
        # Remove existing tag
        tags = service.remove_tag(cohort_id, 'initial')
        
        assert 'initial' not in tags
        assert 'test' in tags
    
    def test_remove_tag_case_insensitive(self, service, populated_cohort):
        """Test that tag removal is case-insensitive."""
        cohort_id = populated_cohort.cohort_id
        
        # Remove using different case
        tags = service.remove_tag(cohort_id, 'INITIAL')
        
        assert 'initial' not in tags
    
    def test_remove_nonexistent_tag(self, service, populated_cohort):
        """Test that removing a nonexistent tag doesn't raise error."""
        cohort_id = populated_cohort.cohort_id
        
        # This should not raise an error
        tags = service.remove_tag(cohort_id, 'nonexistent')
        
        assert 'initial' in tags
        assert 'test' in tags
    
    def test_get_tags(self, service, populated_cohort):
        """Test getting all tags for a cohort."""
        cohort_id = populated_cohort.cohort_id
        
        tags = service.get_tags(cohort_id)
        
        assert isinstance(tags, list)
        assert 'initial' in tags
        assert 'test' in tags
        # Should be sorted alphabetically
        assert tags == sorted(tags)
    
    def test_get_tags_empty(self, service, sample_patients):
        """Test getting tags for a cohort with no tags."""
        result = service.persist_entities(
            entities=sample_patients,
            entity_type='patient',
            cohort_name='no-tags-cohort',
        )
        
        tags = service.get_tags(result.cohort_id)
        
        assert tags == []
    
    def test_list_all_tags(self, service, sample_patients):
        """Test listing all tags with counts."""
        # Create multiple cohorts with overlapping tags
        service.persist_entities(
            entities=sample_patients[:1],
            entity_type='patient',
            cohort_name='cohort-1',
            tags=['common', 'unique1'],
        )
        service.persist_entities(
            entities=sample_patients[1:2],
            entity_type='patient',
            cohort_name='cohort-2',
            tags=['common', 'unique2'],
        )
        service.persist_entities(
            entities=sample_patients[2:],
            entity_type='patient',
            cohort_name='cohort-3',
            tags=['common'],
        )
        
        all_tags = service.list_all_tags()
        
        # Should have 3 unique tags
        assert len(all_tags) == 3
        
        # 'common' should have count 3
        common_tag = next(t for t in all_tags if t['tag'] == 'common')
        assert common_tag['count'] == 3
        
        # unique tags should have count 1
        unique1 = next(t for t in all_tags if t['tag'] == 'unique1')
        assert unique1['count'] == 1
    
    def test_cohorts_by_tag(self, service, sample_patients):
        """Test finding cohorts by tag."""
        # Create cohorts with different tags
        service.persist_entities(
            entities=sample_patients[:1],
            entity_type='patient',
            cohort_name='diabetes-study',
            tags=['diabetes', 'clinical'],
        )
        service.persist_entities(
            entities=sample_patients[1:2],
            entity_type='patient',
            cohort_name='cardiac-study',
            tags=['cardiac', 'clinical'],
        )
        
        # Find by 'clinical' tag
        clinical_cohorts = service.cohorts_by_tag('clinical')
        assert len(clinical_cohorts) == 2
        
        # Find by 'diabetes' tag
        diabetes_cohorts = service.cohorts_by_tag('diabetes')
        assert len(diabetes_cohorts) == 1
        assert diabetes_cohorts[0].name == 'diabetes-study'


# ============================================================================
# Cohort Cloning Tests
# ============================================================================

class TestCohortCloning:
    """Tests for cohort cloning functionality."""
    
    def test_clone_cohort_basic(self, service, populated_cohort):
        """Test basic cohort cloning."""
        source_id = populated_cohort.cohort_id
        
        result = service.clone_cohort(source_id, new_name='cloned-cohort')
        
        assert isinstance(result, CloneResult)
        assert result.source_cohort_id == source_id
        assert result.new_cohort_id != source_id
        assert result.new_cohort_name == 'cloned-cohort'
        assert result.total_entities == 3  # 3 patients
        assert 'patients' in result.entities_cloned
        assert result.entities_cloned['patients'] == 3
    
    def test_clone_cohort_auto_name(self, service, populated_cohort):
        """Test cloning with auto-generated name."""
        source_id = populated_cohort.cohort_id
        source_name = populated_cohort.cohort_name
        
        result = service.clone_cohort(source_id)
        
        assert result.new_cohort_name.startswith(f"{source_name}-copy")
    
    def test_clone_cohort_copies_tags(self, service, populated_cohort):
        """Test that cloning copies tags by default."""
        source_id = populated_cohort.cohort_id
        
        result = service.clone_cohort(source_id, new_name='cloned-with-tags')
        
        new_tags = service.get_tags(result.new_cohort_id)
        assert 'initial' in new_tags
        assert 'test' in new_tags
    
    def test_clone_cohort_custom_tags(self, service, populated_cohort):
        """Test cloning with custom tags."""
        source_id = populated_cohort.cohort_id
        
        result = service.clone_cohort(
            source_id,
            new_name='cloned-custom-tags',
            tags=['custom', 'new'],
        )
        
        new_tags = service.get_tags(result.new_cohort_id)
        assert 'custom' in new_tags
        assert 'new' in new_tags
        assert 'initial' not in new_tags
    
    def test_clone_cohort_unique_ids(self, service, populated_cohort):
        """Test that cloned entities have new unique IDs."""
        source_id = populated_cohort.cohort_id
        
        result = service.clone_cohort(source_id, new_name='cloned-unique-ids')
        
        # Query both cohorts
        source_patients = service.query_cohort(
            source_id, "SELECT id FROM patients"
        )
        clone_patients = service.query_cohort(
            result.new_cohort_id, "SELECT id FROM patients"
        )
        
        source_ids = {p['id'] for p in source_patients.results}
        clone_ids = {p['id'] for p in clone_patients.results}
        
        # IDs should be completely different
        assert source_ids.isdisjoint(clone_ids)
    
    def test_clone_cohort_preserves_data(self, service, populated_cohort):
        """Test that cloned entities preserve their data."""
        source_id = populated_cohort.cohort_id
        
        result = service.clone_cohort(source_id, new_name='cloned-data')
        
        # Get patient names from clone
        clone_patients = service.query_cohort(
            result.new_cohort_id,
            "SELECT given_name, family_name FROM patients ORDER BY given_name"
        )
        
        names = [(p['given_name'], p['family_name']) for p in clone_patients.results]
        assert ('Bob', 'Johnson') in names
        assert ('Jane', 'Smith') in names
        assert ('John', 'Doe') in names
    
    def test_clone_cohort_not_found(self, service):
        """Test cloning non-existent cohort raises error."""
        with pytest.raises(ValueError, match="not found"):
            service.clone_cohort('nonexistent-id')
    
    def test_clone_cohort_to_dict(self, service, populated_cohort):
        """Test CloneResult.to_dict() method."""
        result = service.clone_cohort(
            populated_cohort.cohort_id,
            new_name='cloned-dict'
        )
        
        result_dict = result.to_dict()
        
        assert 'source_cohort_id' in result_dict
        assert 'new_cohort_id' in result_dict
        assert 'entities_cloned' in result_dict
        assert 'total_entities' in result_dict


# ============================================================================
# Cohort Merging Tests
# ============================================================================

class TestCohortMerging:
    """Tests for cohort merging functionality."""
    
    def test_merge_cohorts_basic(self, service, sample_patients):
        """Test basic cohort merging."""
        # Create two cohorts
        result1 = service.persist_entities(
            entities=sample_patients[:2],
            entity_type='patient',
            cohort_name='cohort-a',
            tags=['group-a'],
        )
        result2 = service.persist_entities(
            entities=sample_patients[2:],
            entity_type='patient',
            cohort_name='cohort-b',
            tags=['group-b'],
        )
        
        # Merge them
        merge_result = service.merge_cohorts(
            source_cohort_ids=[result1.cohort_id, result2.cohort_id],
            target_name='merged-cohort',
        )
        
        assert isinstance(merge_result, MergeResult)
        assert len(merge_result.source_cohort_ids) == 2
        assert merge_result.total_entities == 3
        assert 'patients' in merge_result.entities_merged
    
    def test_merge_cohorts_auto_name(self, service, sample_patients):
        """Test merging with auto-generated name."""
        result1 = service.persist_entities(
            entities=sample_patients[:1],
            entity_type='patient',
            cohort_name='source-1',
        )
        result2 = service.persist_entities(
            entities=sample_patients[1:2],
            entity_type='patient',
            cohort_name='source-2',
        )
        
        merge_result = service.merge_cohorts(
            source_cohort_ids=[result1.cohort_id, result2.cohort_id],
        )
        
        assert merge_result.target_cohort_name.startswith('merged-')
    
    def test_merge_cohorts_combines_tags(self, service, sample_patients):
        """Test that merging combines tags from all sources."""
        result1 = service.persist_entities(
            entities=sample_patients[:1],
            entity_type='patient',
            cohort_name='tagged-1',
            tags=['tag-a', 'common'],
        )
        result2 = service.persist_entities(
            entities=sample_patients[1:2],
            entity_type='patient',
            cohort_name='tagged-2',
            tags=['tag-b', 'common'],
        )
        
        merge_result = service.merge_cohorts(
            source_cohort_ids=[result1.cohort_id, result2.cohort_id],
        )
        
        merged_tags = service.get_tags(merge_result.target_cohort_id)
        assert 'tag-a' in merged_tags
        assert 'tag-b' in merged_tags
        assert 'common' in merged_tags
    
    def test_merge_cohorts_custom_tags(self, service, sample_patients):
        """Test merging with custom tags."""
        result1 = service.persist_entities(
            entities=sample_patients[:1],
            entity_type='patient',
            cohort_name='custom-tags-1',
            tags=['original'],
        )
        result2 = service.persist_entities(
            entities=sample_patients[1:2],
            entity_type='patient',
            cohort_name='custom-tags-2',
            tags=['original'],
        )
        
        merge_result = service.merge_cohorts(
            source_cohort_ids=[result1.cohort_id, result2.cohort_id],
            tags=['merged', 'custom'],
        )
        
        merged_tags = service.get_tags(merge_result.target_cohort_id)
        assert 'merged' in merged_tags
        assert 'custom' in merged_tags
        assert 'original' not in merged_tags
    
    def test_merge_cohorts_fewer_than_two_raises_error(self, service, populated_cohort):
        """Test that merging fewer than 2 cohorts raises error."""
        with pytest.raises(ValueError, match="At least 2"):
            service.merge_cohorts(
                source_cohort_ids=[populated_cohort.cohort_id],
            )
    
    def test_merge_cohorts_not_found_raises_error(self, service, populated_cohort):
        """Test that merging with non-existent cohort raises error."""
        with pytest.raises(ValueError, match="not found"):
            service.merge_cohorts(
                source_cohort_ids=[
                    populated_cohort.cohort_id,
                    'nonexistent-id',
                ],
            )
    
    def test_merge_cohorts_three_or_more(self, service, sample_patients):
        """Test merging three or more cohorts."""
        results = []
        for i, patient in enumerate(sample_patients):
            result = service.persist_entities(
                entities=[patient],
                entity_type='patient',
                cohort_name=f'multi-{i}',
            )
            results.append(result)
        
        merge_result = service.merge_cohorts(
            source_cohort_ids=[r.cohort_id for r in results],
            target_name='merged-three',
        )
        
        assert merge_result.total_entities == 3
        assert len(merge_result.source_cohort_ids) == 3
    
    def test_merge_result_to_dict(self, service, sample_patients):
        """Test MergeResult.to_dict() method."""
        result1 = service.persist_entities(
            entities=sample_patients[:1],
            entity_type='patient',
            cohort_name='dict-test-1',
        )
        result2 = service.persist_entities(
            entities=sample_patients[1:2],
            entity_type='patient',
            cohort_name='dict-test-2',
        )
        
        merge_result = service.merge_cohorts(
            source_cohort_ids=[result1.cohort_id, result2.cohort_id],
        )
        
        result_dict = merge_result.to_dict()
        
        assert 'source_cohort_ids' in result_dict
        assert 'target_cohort_id' in result_dict
        assert 'entities_merged' in result_dict
        assert 'conflicts_resolved' in result_dict


# ============================================================================
# Export Tests
# ============================================================================

class TestExport:
    """Tests for export functionality."""
    
    def test_export_json(self, service, populated_cohort):
        """Test JSON export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'export.json'
            
            result = service.export_cohort(
                populated_cohort.cohort_id,
                format='json',
                output_path=str(output_path),
            )
            
            assert isinstance(result, ExportResult)
            assert result.format == 'json'
            assert result.total_entities == 3
            assert result.file_size_bytes > 0
            
            # Verify JSON content
            with open(output_path) as f:
                data = json.load(f)
            
            assert data['cohort_id'] == populated_cohort.cohort_id
            assert data['cohort_name'] == populated_cohort.cohort_name
            assert 'patients' in data['entities']
            assert len(data['entities']['patients']) == 3
    
    def test_export_csv(self, service, populated_cohort):
        """Test CSV export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'export'
            
            result = service.export_cohort(
                populated_cohort.cohort_id,
                format='csv',
                output_path=str(output_path),
            )
            
            assert result.format == 'csv'
            assert result.total_entities == 3
            
            # Verify CSV files exist
            csv_dir = Path(result.file_path)
            assert csv_dir.is_dir()
            
            patients_csv = csv_dir / 'patients.csv'
            assert patients_csv.exists()
            
            # Verify CSV content
            with open(patients_csv) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            assert len(rows) == 3
            names = [r['given_name'] for r in rows]
            assert 'John' in names
            assert 'Jane' in names
            assert 'Bob' in names
    
    def test_export_json_convenience(self, service, populated_cohort):
        """Test export_to_json convenience method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'convenience.json'
            
            result = service.export_to_json(
                populated_cohort.cohort_id,
                output_path=str(output_path),
            )
            
            assert result.format == 'json'
            assert output_path.exists()
    
    def test_export_csv_convenience(self, service, populated_cohort):
        """Test export_to_csv convenience method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'convenience'
            
            result = service.export_to_csv(
                populated_cohort.cohort_id,
                output_path=str(output_path),
            )
            
            assert result.format == 'csv'
    
    def test_export_without_provenance(self, service, populated_cohort):
        """Test export without provenance columns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'no-provenance.json'
            
            result = service.export_cohort(
                populated_cohort.cohort_id,
                format='json',
                output_path=str(output_path),
                include_provenance=False,
            )
            
            with open(output_path) as f:
                data = json.load(f)
            
            # Provenance columns should not be present
            patient = data['entities']['patients'][0]
            assert 'source_type' not in patient
            assert 'source_system' not in patient
            assert 'cohort_id' not in patient
    
    def test_export_includes_tags(self, service, populated_cohort):
        """Test that export includes tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'with-tags.json'
            
            result = service.export_cohort(
                populated_cohort.cohort_id,
                format='json',
                output_path=str(output_path),
            )
            
            with open(output_path) as f:
                data = json.load(f)
            
            assert 'tags' in data
            assert 'initial' in data['tags']
            assert 'test' in data['tags']
    
    def test_export_unsupported_format(self, service, populated_cohort):
        """Test that unsupported format raises error."""
        with pytest.raises(ValueError, match="Unsupported"):
            service.export_cohort(
                populated_cohort.cohort_id,
                format='xml',
            )
    
    def test_export_not_found(self, service):
        """Test export of non-existent cohort raises error."""
        with pytest.raises(ValueError, match="not found"):
            service.export_cohort('nonexistent-id')
    
    def test_export_result_to_dict(self, service, populated_cohort):
        """Test ExportResult.to_dict() method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'to-dict.json'
            
            result = service.export_cohort(
                populated_cohort.cohort_id,
                format='json',
                output_path=str(output_path),
            )
            
            result_dict = result.to_dict()
            
            assert 'cohort_id' in result_dict
            assert 'format' in result_dict
            assert 'file_path' in result_dict
            assert 'entities_exported' in result_dict
            assert 'file_size_bytes' in result_dict


# ============================================================================
# Integration Tests
# ============================================================================

class TestPhase2Integration:
    """Integration tests combining multiple Phase 2 features."""
    
    def test_clone_then_tag(self, service, populated_cohort):
        """Test cloning a cohort then adding tags."""
        clone = service.clone_cohort(
            populated_cohort.cohort_id,
            new_name='clone-to-tag',
        )
        
        service.add_tag(clone.new_cohort_id, 'cloned')
        service.add_tag(clone.new_cohort_id, 'modified')
        
        tags = service.get_tags(clone.new_cohort_id)
        assert 'cloned' in tags
        assert 'modified' in tags
        assert 'initial' in tags  # From source
    
    def test_merge_then_export(self, service, sample_patients):
        """Test merging cohorts then exporting the result."""
        result1 = service.persist_entities(
            entities=sample_patients[:2],
            entity_type='patient',
            cohort_name='merge-export-1',
        )
        result2 = service.persist_entities(
            entities=sample_patients[2:],
            entity_type='patient',
            cohort_name='merge-export-2',
        )
        
        merge_result = service.merge_cohorts(
            source_cohort_ids=[result1.cohort_id, result2.cohort_id],
            target_name='merged-for-export',
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            export = service.export_cohort(
                merge_result.target_cohort_id,
                format='json',
                output_path=str(Path(tmpdir) / 'merged.json'),
            )
            
            assert export.total_entities == 3
    
    def test_clone_modify_merge(self, service, sample_patients):
        """Test complex workflow: clone, modify, merge."""
        # Create original
        original = service.persist_entities(
            entities=sample_patients[:2],
            entity_type='patient',
            cohort_name='workflow-original',
        )
        
        # Clone it
        clone = service.clone_cohort(
            original.cohort_id,
            new_name='workflow-clone',
        )
        
        # Add different tags
        service.add_tag(original.cohort_id, 'original')
        service.add_tag(clone.new_cohort_id, 'cloned')
        
        # Merge them back together
        merged = service.merge_cohorts(
            source_cohort_ids=[original.cohort_id, clone.new_cohort_id],
            target_name='workflow-merged',
        )
        
        # Verify merged has entities from both
        assert merged.total_entities == 4  # 2 + 2 (cloned copies)
        
        # Verify merged has both tags
        tags = service.get_tags(merged.target_cohort_id)
        assert 'original' in tags
        assert 'cloned' in tags
