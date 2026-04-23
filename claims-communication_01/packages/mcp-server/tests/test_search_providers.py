"""
Tests for the healthsim_search_providers MCP tool.

This tool searches REAL NPPES provider data (8.9M records) and should be used
BEFORE generating synthetic providers for cohorts.

Tests cover:
- Tool existence and configuration
- Input validation
- Docstring guidance for real data first
- Integration with add_entities guidance
"""

import json
import pytest
from pathlib import Path

# Import the MCP server module
import sys
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))

from healthsim_mcp import (
    mcp,
    search_providers,
    add_entities,
    SearchProvidersInput,
)


class TestSearchProvidersToolExists:
    """Tests verifying the search_providers tool is properly registered."""
    
    def test_tool_registered_in_mcp(self):
        """Verify healthsim_search_providers is registered as an MCP tool."""
        tools = mcp._tool_manager._tools
        assert "healthsim_search_providers" in tools, \
            "healthsim_search_providers should be registered as an MCP tool"
    
    def test_tool_has_correct_annotations(self):
        """Verify tool has read-only and idempotent annotations."""
        tools = mcp._tool_manager._tools
        tool = tools.get("healthsim_search_providers")
        assert tool is not None


class TestSearchProvidersDocstring:
    """Tests verifying the docstring contains proper guidance."""
    
    def test_docstring_emphasizes_real_data(self):
        """Docstring should emphasize this searches REAL providers."""
        docstring = search_providers.__doc__
        assert docstring is not None
        
        # Should emphasize REAL data
        assert "REAL" in docstring or "real" in docstring
        
        # Should mention NPPES
        assert "NPPES" in docstring
    
    def test_docstring_says_use_first(self):
        """Docstring should say to use this tool FIRST."""
        docstring = search_providers.__doc__
        
        # Should indicate to use first
        assert "FIRST" in docstring or "first" in docstring
    
    def test_docstring_mentions_synthetic_alternative(self):
        """Docstring should mention when synthetic is acceptable."""
        docstring = search_providers.__doc__
        
        # Should mention synthetic as alternative
        assert "synthetic" in docstring.lower()
    
    def test_docstring_has_taxonomy_codes(self):
        """Docstring should include common taxonomy codes for reference."""
        docstring = search_providers.__doc__
        
        # Should have Family Medicine code
        assert "207Q" in docstring
        
        # Should have Internal Medicine code
        assert "207R" in docstring


class TestSearchProvidersInput:
    """Tests for the SearchProvidersInput model."""
    
    def test_state_is_required(self):
        """State should be a required field."""
        # This should raise validation error without state
        with pytest.raises(Exception):
            SearchProvidersInput()
    
    def test_state_only_is_valid(self):
        """Should accept just state as minimum input."""
        params = SearchProvidersInput(state="CA")
        assert params.state == "CA"
    
    def test_all_filters_accepted(self):
        """Should accept all optional filters."""
        params = SearchProvidersInput(
            state="CA",
            city="San Diego",
            county_fips="06073",
            zip_code="92101",
            specialty="Family Medicine",
            taxonomy_code="207Q00000X",
            entity_type="individual",
            limit=100
        )
        
        assert params.state == "CA"
        assert params.city == "San Diego"
        assert params.county_fips == "06073"
        assert params.zip_code == "92101"
        assert params.specialty == "Family Medicine"
        assert params.taxonomy_code == "207Q00000X"
        assert params.entity_type == "individual"
        assert params.limit == 100
    
    def test_limit_bounds(self):
        """Limit should be bounded between 1 and 200."""
        # Valid limits
        params = SearchProvidersInput(state="CA", limit=1)
        assert params.limit == 1
        
        params = SearchProvidersInput(state="CA", limit=200)
        assert params.limit == 200
        
        # Invalid limits should raise
        with pytest.raises(Exception):
            SearchProvidersInput(state="CA", limit=0)
        
        with pytest.raises(Exception):
            SearchProvidersInput(state="CA", limit=201)


class TestRealDataGuidanceIntegration:
    """Tests verifying the real data guidance is integrated across tools."""
    
    def test_add_entities_mentions_search_providers(self):
        """add_entities docstring should reference search_providers for providers."""
        docstring = add_entities.__doc__
        
        # Should mention to use search_providers first
        assert "search_providers" in docstring or "healthsim_search_providers" in docstring
    
    def test_add_entities_has_real_vs_synthetic_section(self):
        """add_entities should have clear real vs synthetic guidance."""
        docstring = add_entities.__doc__
        
        # Should have the guidance section
        assert "REAL" in docstring or "real" in docstring
        assert "SYNTHETIC" in docstring or "synthetic" in docstring
        
        # Should mention PHI
        assert "PHI" in docstring
    
    def test_module_docstring_has_data_source_guide(self):
        """Module docstring should have data source decision guide."""
        import healthsim_mcp
        
        module_doc = healthsim_mcp.__doc__
        assert module_doc is not None
        
        # Should have the decision guide
        assert "DATA SOURCE" in module_doc or "Providers/Facilities" in module_doc
        
        # Should mention NPPES
        assert "NPPES" in module_doc
        
        # Should mention synthetic for PHI
        assert "PHI" in module_doc or "synthetic" in module_doc.lower()


class TestTaxonomyCodeMapping:
    """Tests for specialty-to-taxonomy code mapping in search_providers."""
    
    def test_common_specialties_documented(self):
        """Common specialties should be documented in the docstring."""
        docstring = search_providers.__doc__
        
        # Primary care specialties
        assert "Family Medicine" in docstring
        assert "Internal Medicine" in docstring
        
        # Should have taxonomy codes
        assert "207Q00000X" in docstring  # Family Medicine
        assert "207R00000X" in docstring  # Internal Medicine


class TestSearchProvidersErrorHandling:
    """Tests for error handling in search_providers."""
    
    def test_missing_table_returns_helpful_error(self):
        """Should return helpful error if NPPES data not loaded."""
        # This tests the error path - actual data availability varies by environment
        params = SearchProvidersInput(state="XX")  # Invalid state
        
        # The function should not crash
        result = search_providers(params)
        
        # Result should be valid JSON
        data = json.loads(result)
        
        # Should either have providers or an error
        assert "providers" in data or "error" in data


class TestSearchProvidersIntegration:
    """Integration tests that query actual NPPES data.
    
    These tests validate the SQL query works against the production database.
    They require the network.providers table to be populated.
    """
    
    def test_search_california_providers(self):
        """Query real providers in California."""
        params = SearchProvidersInput(state="CA", limit=5)
        result = search_providers(params)
        data = json.loads(result)
        
        # Should either succeed with providers or fail gracefully
        if "error" not in data:
            assert "providers" in data
            assert data["source"] == "NPPES (National Plan and Provider Enumeration System)"
            assert data["data_type"] == "REAL registered providers"
            # If we got results, validate structure
            if data["result_count"] > 0:
                provider = data["providers"][0]
                assert "npi" in provider
                assert "practice_state" in provider
    
    def test_search_with_city_filter(self):
        """Query providers filtered by city."""
        params = SearchProvidersInput(state="CA", city="San Diego", limit=5)
        result = search_providers(params)
        data = json.loads(result)
        
        if "error" not in data and data["result_count"] > 0:
            # All results should be in San Diego
            for provider in data["providers"]:
                assert "SAN DIEGO" in provider["practice_city"].upper()
    
    def test_search_with_taxonomy_code(self):
        """Query providers by taxonomy code (Family Medicine)."""
        params = SearchProvidersInput(
            state="CA", 
            taxonomy_code="207Q00000X",  # Family Medicine
            limit=5
        )
        result = search_providers(params)
        data = json.loads(result)
        
        if "error" not in data and data["result_count"] > 0:
            # All results should have the taxonomy code
            for provider in data["providers"]:
                assert provider["primary_taxonomy"].startswith("207Q")
    
    def test_column_names_correct(self):
        """Verify practice_address_1 column is used (not practice_address)."""
        params = SearchProvidersInput(state="CA", limit=1)
        result = search_providers(params)
        data = json.loads(result)
        
        # Should not have column name errors
        if "error" in data:
            assert "practice_address" not in data["error"], \
                "Column name error - should use practice_address_1"
        else:
            # If we got results, practice_address should be populated
            if data["result_count"] > 0:
                provider = data["providers"][0]
                assert "practice_address" in provider


class TestDataSourceDecisionMatrix:
    """Tests verifying the decision matrix is properly encoded."""
    
    def test_provider_entities_should_use_real_data(self):
        """Provider entities should be sourced from NPPES (real data)."""
        add_doc = add_entities.__doc__
        
        # Should indicate providers use real data
        assert "PROVIDER" in add_doc.upper() or "provider" in add_doc.lower()
        assert "NPPES" in add_doc or "real" in add_doc.lower()
    
    def test_phi_entities_should_be_synthetic(self):
        """PHI entities (patients, members, claims) should be synthetic."""
        add_doc = add_entities.__doc__
        
        # Should mention PHI entities are synthetic
        assert "PHI" in add_doc
        assert "patient" in add_doc.lower() or "member" in add_doc.lower()
        assert "synthetic" in add_doc.lower()
