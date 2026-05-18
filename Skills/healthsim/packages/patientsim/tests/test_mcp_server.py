"""Tests for MCP server functionality.

Note: Some tests were removed as they tested functions that no longer exist
in the current implementation (e.g., _generate_patient_with_encounter_tool,
_serialize_patient, _serialize_cohort). The MCP server now uses human-readable
formatters instead of JSON serialization functions.
"""

import pytest

# Import the MCP server functions
from patientsim.mcp.generation_server import (
    _delete_cohort_tool,
    _generate_cohort_tool,
    _generate_patient_tool,
    _list_saved_cohorts_tool,
    _list_skills_tool,
    _load_cohort_tool,
    _save_cohort_tool,
    _workspace_summary_tool,
    list_tools,
    session_manager,
)


class TestToolListing:
    """Tests for MCP tool listing."""

    @pytest.mark.asyncio
    async def test_list_tools_returns_expected_tools(self) -> None:
        """Test that list_tools returns expected tools."""
        tools = await list_tools()

        # Should have at least the core tools
        assert len(tools) >= 4

        tool_names = [tool.name for tool in tools]
        assert "generate_patient" in tool_names
        assert "generate_cohort" in tool_names
        assert "list_skills" in tool_names
        assert "describe_skill" in tool_names

    @pytest.mark.asyncio
    async def test_tools_have_descriptions(self) -> None:
        """Test that all tools have descriptions."""
        tools = await list_tools()

        for tool in tools:
            assert tool.description
            assert len(tool.description) > 0

    @pytest.mark.asyncio
    async def test_tools_have_input_schemas(self) -> None:
        """Test that all tools have input schemas."""
        tools = await list_tools()

        for tool in tools:
            assert tool.inputSchema
            assert "type" in tool.inputSchema
            assert tool.inputSchema["type"] == "object"


class TestGeneratePatientTool:
    """Tests for generate_patient tool."""

    @pytest.mark.asyncio
    async def test_generate_patient_basic(self) -> None:
        """Test basic patient generation."""
        arguments = {}

        result = await _generate_patient_tool(arguments)

        assert len(result) == 1
        text_content = result[0]
        assert text_content.type == "text"
        # Result is human-readable text, should contain patient info
        assert len(text_content.text) > 0

    @pytest.mark.asyncio
    async def test_generate_patient_with_seed(self) -> None:
        """Test patient generation with seed for reproducibility."""
        arguments = {"seed": 42}

        result = await _generate_patient_tool(arguments)

        assert len(result) == 1
        text_content = result[0]
        assert text_content.type == "text"
        assert len(text_content.text) > 0


class TestGenerateCohortTool:
    """Tests for generate_cohort tool."""

    @pytest.mark.asyncio
    async def test_generate_cohort_basic(self) -> None:
        """Test basic cohort generation."""
        arguments = {"count": 3}

        result = await _generate_cohort_tool(arguments)

        assert len(result) == 1
        text_content = result[0]
        assert text_content.type == "text"
        # Result should mention patient count
        assert len(text_content.text) > 0

    @pytest.mark.asyncio
    async def test_generate_cohort_with_seed(self) -> None:
        """Test cohort generation with seed for reproducibility."""
        arguments = {"count": 2, "seed": 42}

        result = await _generate_cohort_tool(arguments)

        assert len(result) == 1
        text_content = result[0]
        assert text_content.type == "text"


class TestListSkillsTool:
    """Tests for list_skills tool (clinical scenario templates)."""

    @pytest.mark.asyncio
    async def test_list_skills_basic(self) -> None:
        """Test basic skills listing."""
        arguments = {}

        result = await _list_skills_tool(arguments)

        assert len(result) == 1
        text_content = result[0]
        assert text_content.type == "text"
        # Should return information about available skills
        assert len(text_content.text) > 0


class TestStateManagementTools:
    """Tests for state management MCP tools."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmp_path):
        """Clear session and set temp workspace directory for each test."""
        # Store original and set temp path on session_manager directly
        original_dir = session_manager._workspace_dir

        session_manager._workspace_dir = tmp_path

        # Clear session before each test
        session_manager.clear()

        yield

        # Restore and cleanup
        session_manager.clear()
        session_manager._workspace_dir = original_dir

    @pytest.mark.asyncio
    async def test_workspace_summary_empty(self) -> None:
        """Test workspace summary with empty session."""
        result = await _workspace_summary_tool({})

        assert len(result) == 1
        assert "empty" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_workspace_summary_with_patients(self) -> None:
        """Test workspace summary with patients."""
        # Generate a patient first
        await _generate_patient_tool({})

        result = await _workspace_summary_tool({})

        assert len(result) == 1
        assert "Patients:" in result[0].text
        assert "1" in result[0].text

    @pytest.mark.asyncio
    async def test_save_cohort_empty_workspace(self) -> None:
        """Test saving empty workspace returns error."""
        result = await _save_cohort_tool({"name": "test"})

        assert len(result) == 1
        assert "Nothing to save" in result[0].text or "Error" in result[0].text

    @pytest.mark.asyncio
    async def test_save_cohort_success(self) -> None:
        """Test saving scenario with patients."""
        # Generate a patient first
        await _generate_patient_tool({})

        result = await _save_cohort_tool(
            {
                "name": "test-cohort",
                "description": "Test description",
                "tags": ["test"],
            }
        )

        assert len(result) == 1
        assert "Saved" in result[0].text
        assert "test-cohort" in result[0].text

    @pytest.mark.asyncio
    async def test_list_saved_cohorts_empty(self) -> None:
        """Test listing cohorts when none saved."""
        result = await _list_saved_cohorts_tool({})

        assert len(result) == 1
        assert "No saved cohorts" in result[0].text

    @pytest.mark.asyncio
    async def test_list_saved_cohorts_with_data(self) -> None:
        """Test listing saved cohorts."""
        # Generate and save
        await _generate_patient_tool({})
        await _save_cohort_tool({"name": "list-test"})

        result = await _list_saved_cohorts_tool({})

        assert len(result) == 1
        assert "list-test" in result[0].text

    @pytest.mark.asyncio
    async def test_load_cohort_not_found(self) -> None:
        """Test loading non-existent scenario."""
        result = await _load_cohort_tool({"name": "nonexistent"})

        assert len(result) == 1
        assert "not found" in result[0].text.lower() or "error" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_load_cohort_success(self) -> None:
        """Test loading a saved scenario."""
        # Generate, save, then clear
        await _generate_patient_tool({})
        await _save_cohort_tool({"name": "load-test"})
        session_manager.clear()

        # Load it back
        result = await _load_cohort_tool({"name": "load-test"})

        assert len(result) == 1
        assert "Loaded" in result[0].text
        assert session_manager.count() == 1

    @pytest.mark.asyncio
    async def test_delete_cohort_requires_confirm(self) -> None:
        """Test delete requires confirmation."""
        result = await _delete_cohort_tool(
            {
                "cohort_id": "some-id",
                "confirm": False,
            }
        )

        assert len(result) == 1
        assert "confirm" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_delete_cohort_not_found(self) -> None:
        """Test deleting non-existent scenario."""
        result = await _delete_cohort_tool(
            {
                "cohort_id": "nonexistent-id",
                "confirm": True,
            }
        )

        assert len(result) == 1
        assert "not found" in result[0].text.lower() or "error" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_tools_include_state_management(self) -> None:
        """Test that list_tools includes state management tools."""
        tools = await list_tools()
        tool_names = [tool.name for tool in tools]

        assert "save_cohort" in tool_names
        assert "load_cohort" in tool_names
        assert "list_saved_cohorts" in tool_names
        assert "delete_cohort" in tool_names
        assert "workspace_summary" in tool_names
