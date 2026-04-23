"""
Tests for entity type taxonomy validation.

Ensures that reference data (providers, facilities, pharmacies) triggers a suggestion
to use real data, while allowing override when synthetic data is explicitly needed.
"""

import pytest
import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from healthsim_mcp import (
    SCENARIO_ENTITY_TYPES,
    RELATIONSHIP_ENTITY_TYPES,
    REFERENCE_ENTITY_TYPES,
    ALLOWED_ENTITY_TYPES,
    validate_entity_types,
)


class TestEntityTypeTaxonomy:
    """Tests for the entity type taxonomy constants."""
    
    def test_cohort_entity_types_defined(self):
        """Scenario entity types should include PHI data types."""
        assert "patients" in SCENARIO_ENTITY_TYPES
        assert "members" in SCENARIO_ENTITY_TYPES
        assert "claims" in SCENARIO_ENTITY_TYPES
        assert "encounters" in SCENARIO_ENTITY_TYPES
    
    def test_relationship_entity_types_defined(self):
        """Relationship types should link cohort to reference data."""
        assert "pcp_assignments" in RELATIONSHIP_ENTITY_TYPES
        assert "network_contracts" in RELATIONSHIP_ENTITY_TYPES
    
    def test_reference_entity_types_defined(self):
        """Reference types should include real-world data that exists in shared tables."""
        assert "providers" in REFERENCE_ENTITY_TYPES
        assert "facilities" in REFERENCE_ENTITY_TYPES
        assert "pharmacies" in REFERENCE_ENTITY_TYPES
    
    def test_allowed_types_is_union(self):
        """Allowed types should be cohort data + relationships."""
        expected = SCENARIO_ENTITY_TYPES | RELATIONSHIP_ENTITY_TYPES
        assert ALLOWED_ENTITY_TYPES == expected
    
    def test_reference_types_not_in_allowed(self):
        """Reference types should NOT be in allowed types."""
        for ref_type in REFERENCE_ENTITY_TYPES:
            assert ref_type not in ALLOWED_ENTITY_TYPES


class TestValidateEntityTypes:
    """Tests for the validate_entity_types() function."""
    
    # === Tests for VALID entity types ===
    
    def test_patients_allowed(self):
        """Patients should be allowed (cohort data)."""
        entities = {"patients": [{"patient_id": "P001"}]}
        assert validate_entity_types(entities) is None
    
    def test_members_allowed(self):
        """Members should be allowed (cohort data)."""
        entities = {"members": [{"member_id": "M001"}]}
        assert validate_entity_types(entities) is None
    
    def test_claims_allowed(self):
        """Claims should be allowed (cohort data)."""
        entities = {"claims": [{"claim_id": "C001"}]}
        assert validate_entity_types(entities) is None
    
    def test_pcp_assignments_allowed(self):
        """PCP assignments should be allowed (relationship data)."""
        entities = {"pcp_assignments": [{"member_id": "M001", "provider_npi": "1234567890"}]}
        assert validate_entity_types(entities) is None
    
    def test_network_contracts_allowed(self):
        """Network contracts should be allowed (relationship data)."""
        entities = {"network_contracts": [{"plan_id": "PLAN001", "provider_npi": "1234567890"}]}
        assert validate_entity_types(entities) is None
    
    def test_multiple_allowed_types(self):
        """Multiple allowed types in one call should be valid."""
        entities = {
            "patients": [{"patient_id": "P001"}],
            "members": [{"member_id": "M001"}],
            "pcp_assignments": [{"member_id": "M001", "provider_npi": "123"}],
        }
        assert validate_entity_types(entities) is None
    
    # === Tests for reference data types (soft block by default) ===
    
    def test_providers_suggests_real_data(self):
        """Providers should suggest using real data by default."""
        entities = {"providers": [{"npi": "1234567890", "name": "Dr. Test"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "REFERENCE DATA" in error or "reference" in error.lower()
        assert "allow_reference_entities" in error  # Shows how to override
    
    def test_facilities_suggests_real_data(self):
        """Facilities should suggest using real data by default."""
        entities = {"facilities": [{"npi": "1234567890", "name": "Test Hospital"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "allow_reference_entities" in error
    
    def test_pharmacies_suggests_real_data(self):
        """Pharmacies should suggest using real data by default."""
        entities = {"pharmacies": [{"npi": "1234567890", "name": "Test Pharmacy"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "allow_reference_entities" in error
    
    def test_hospitals_suggests_real_data(self):
        """Hospitals should suggest using real data by default."""
        entities = {"hospitals": [{"npi": "1234567890", "name": "Test Hospital"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "allow_reference_entities" in error
    
    def test_suggestion_message_has_correct_approach(self):
        """Suggestion message should explain the correct approach."""
        entities = {"providers": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        
        assert "healthsim_search_providers" in error
        assert "pcp_assignments" in error or "network_contracts" in error
    
    def test_mixed_valid_and_reference_suggests_override(self):
        """If ANY type is reference data, should suggest override."""
        entities = {
            "patients": [{"patient_id": "P001"}],  # Valid
            "providers": [{"npi": "123"}],          # Reference - suggests real data
        }
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "providers" in error.lower()
    
    # === Tests for override behavior ===
    
    def test_providers_allowed_with_override(self):
        """Providers should be allowed when override is True."""
        entities = {"providers": [{"npi": "1234567890", "name": "Dr. Test"}]}
        error = validate_entity_types(entities, allow_reference_override=True)
        
        assert error is None  # Should be allowed
    
    def test_facilities_allowed_with_override(self):
        """Facilities should be allowed when override is True."""
        entities = {"facilities": [{"npi": "1234567890", "name": "Test Hospital"}]}
        error = validate_entity_types(entities, allow_reference_override=True)
        
        assert error is None
    
    def test_mixed_types_allowed_with_override(self):
        """Mixed cohort + reference types should be allowed with override."""
        entities = {
            "patients": [{"patient_id": "P001"}],
            "providers": [{"npi": "123", "name": "Dr. Test"}],
        }
        error = validate_entity_types(entities, allow_reference_override=True)
        
        assert error is None
    
    # === Tests for singular/plural normalization ===
    
    def test_singular_patient_normalized(self):
        """Singular 'patient' should be normalized and allowed."""
        entities = {"patient": [{"patient_id": "P001"}]}
        assert validate_entity_types(entities) is None
    
    def test_singular_provider_suggests_real_data(self):
        """Singular 'provider' should be normalized and suggest real data."""
        entities = {"provider": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        assert error is not None
        assert "allow_reference_entities" in error
    
    def test_singular_provider_allowed_with_override(self):
        """Singular 'provider' with override should be allowed."""
        entities = {"provider": [{"npi": "123"}]}
        error = validate_entity_types(entities, allow_reference_override=True)
        assert error is None
    
    # === Tests for unknown types ===
    
    def test_unknown_type_returns_warning(self):
        """Unknown entity types should return a warning with allowed types."""
        entities = {"foobar": [{"id": "1"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "Unknown entity type" in error
        assert "foobar" in error
        assert "patients" in error  # Should list allowed types


class TestValidationInTools:
    """Tests that validation is actually called in the MCP tools."""
    
    def test_add_entities_suggests_real_data_for_providers(self):
        """add_entities should suggest real data for providers."""
        from healthsim_mcp import add_entities, AddEntitiesInput
        
        params = AddEntitiesInput(
            cohort_name="test-cohort",
            entities={"providers": [{"npi": "1234567890", "name": "Dr. Test"}]}
        )
        
        result = json.loads(add_entities(params))
        
        assert "error" in result
        assert "allow_reference_entities" in result["error"]
    
    def test_add_entities_allows_providers_with_override(self):
        """add_entities should allow providers when override is set."""
        from healthsim_mcp import AddEntitiesInput
        
        # Just test the input accepts the parameter
        params = AddEntitiesInput(
            cohort_name="test-cohort",
            entities={"providers": [{"npi": "1234567890", "name": "Dr. Test"}]},
            allow_reference_entities=True
        )
        
        # Validation should pass
        error = validate_entity_types(params.entities, allow_reference_override=params.allow_reference_entities)
        assert error is None
    
    def test_add_entities_allows_patients(self):
        """add_entities should allow patients without override."""
        from healthsim_mcp import AddEntitiesInput
        
        params = AddEntitiesInput(
            cohort_name="test-cohort",
            entities={"patients": [{"patient_id": "P001", "name": "Test Patient"}]}
        )
        
        error = validate_entity_types(params.entities)
        assert error is None
    
    def test_save_cohort_suggests_real_data_for_facilities(self):
        """save_cohort should suggest real data for facilities."""
        from healthsim_mcp import save_cohort, SaveCohortInput
        
        params = SaveCohortInput(
            name="test-cohort",
            entities={"facilities": [{"npi": "1234567890", "name": "Test Hospital"}]}
        )
        
        result = json.loads(save_cohort(params))
        
        assert "error" in result
        assert "allow_reference_entities" in result["error"]
    
    def test_save_cohort_accepts_override_parameter(self):
        """save_cohort should accept allow_reference_entities parameter."""
        from healthsim_mcp import SaveCohortInput
        
        # Just test the input model accepts the parameter
        params = SaveCohortInput(
            name="test-cohort",
            entities={"providers": [{"npi": "123"}]},
            allow_reference_entities=True
        )
        
        assert params.allow_reference_entities is True


class TestSuggestionMessageQuality:
    """Tests that suggestion messages are helpful and educational."""
    
    def test_message_recommends_real_data(self):
        """Suggestion should recommend using real data."""
        entities = {"providers": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        
        assert "RECOMMENDED" in error or "recommend" in error.lower()
        assert "real" in error.lower() or "network.providers" in error
    
    def test_message_shows_override_syntax(self):
        """Suggestion should show how to override."""
        entities = {"providers": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        
        assert "allow_reference_entities=True" in error
    
    def test_message_mentions_query_tools(self):
        """Suggestion should point to query tools for accessing reference data."""
        entities = {"providers": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        
        assert "healthsim_search_providers" in error
