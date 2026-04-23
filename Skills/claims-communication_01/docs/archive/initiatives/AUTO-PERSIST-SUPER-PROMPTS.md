# HealthSim Auto-Persist Implementation Super-Prompts

**Created**: December 26, 2024  
**Status**: Ready for Execution  
**Companion Doc**: [AUTO-PERSIST-IMPLEMENTATION-PLAN.md](./AUTO-PERSIST-IMPLEMENTATION-PLAN.md)

---

## How to Use This Document

Each phase below is a complete, self-contained super-prompt. Copy the entire phase section into a new Claude session to execute that phase. Each super-prompt includes:

1. **Context** - What to read first
2. **Pre-flight Checklist** - Verify before starting
3. **Deliverables** - Exact files to create/modify
4. **Step-by-Step Instructions** - Detailed implementation
5. **Post-flight Checklist** - Verify completion
6. **Success Criteria** - How to know it's done

---

## Phase 1: Core Persistence Module

### Super-Prompt 1.1: Create Auto-Persist Service

```
## Context

I'm implementing the HealthSim Auto-Persist feature. This phase creates the core persistence service that will be used by MCP tools.

**Read these files first:**
1. `/Users/markoswald/Developer/projects/healthsim-workspace/docs/healthsim-auto-persist-architecture.html` - Architecture design
2. `/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src/healthsim/state/manager.py` - Existing state manager
3. `/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src/healthsim/state/serializers.py` - Entity serializers
4. `/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src/healthsim/db/schema.py` - Database schema

**Key Design Decisions (Confirmed):**
- Batch size: 50 entities per batch
- Auto-naming format: `{keywords}-{YYYYMMDD}`
- Samples per entity type: 3
- Default query page size: 20 results
- Context budget: ~5,500 tokens working

## Pre-flight Checklist

- [ ] All 605 existing tests pass: `cd packages/core && pytest`
- [ ] DuckDB schema has 41 tables
- [ ] Understand existing StateManager patterns
- [ ] Understand existing serializer patterns

## Deliverables

Create these files:

1. `packages/core/src/healthsim/state/auto_persist.py` - Core auto-persist service
2. `packages/core/src/healthsim/state/auto_naming.py` - Auto-naming service
3. `packages/core/src/healthsim/state/summary.py` - Summary generation service
4. `packages/core/tests/state/test_auto_persist.py` - Unit tests
5. `packages/core/tests/state/test_auto_naming.py` - Unit tests
6. `packages/core/tests/state/test_summary.py` - Unit tests

## Step-by-Step Instructions

### Step 1: Create Auto-Naming Service

Create `packages/core/src/healthsim/state/auto_naming.py`:

```python
"""
Auto-naming service for HealthSim cohorts.

Generates descriptive cohort names from generation context,
following the pattern: {keywords}-{YYYYMMDD}
"""

from datetime import datetime
from typing import List, Optional
import re

from ..db import get_connection


def generate_cohort_name(
    keywords: Optional[List[str]] = None,
    context: Optional[str] = None,
    prefix: Optional[str] = None,
) -> str:
    """
    Generate a unique cohort name.
    
    Args:
        keywords: Explicit keywords to include
        context: Generation context to extract keywords from
        prefix: Optional prefix (e.g., product name)
    
    Returns:
        Unique cohort name like "diabetes-patients-20241226"
    """
    # Implementation details...
```

Key functions to implement:
- `generate_cohort_name()` - Main naming function
- `extract_keywords()` - Extract keywords from context
- `ensure_unique_name()` - Check DB and add counter if needed
- `sanitize_name()` - Clean special characters

### Step 2: Create Summary Service

Create `packages/core/src/healthsim/state/summary.py`:

```python
"""
Cohort summary generation for context-efficient loading.

Generates statistical summaries that fit within token budget (~500 tokens)
while providing enough information for generation consistency.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json

from ..db import get_connection


class CohortSummary:
    """Token-efficient cohort summary."""
    
    cohort_id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Entity counts by type
    entity_counts: Dict[str, int]
    
    # Statistics
    statistics: Dict[str, Any]
    
    # Sample entities (for pattern consistency)
    samples: Dict[str, List[Dict]]
    
    # Tags
    tags: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dict for JSON serialization."""
        pass
    
    def token_estimate(self) -> int:
        """Estimate token count for this summary."""
        pass


def generate_summary(
    cohort_id: str,
    include_samples: bool = True,
    samples_per_type: int = 3,
) -> CohortSummary:
    """
    Generate a token-efficient summary of a cohort.
    
    Target: ~500 tokens for summary, ~3000 for samples
    """
    pass
```

Key functions to implement:
- `CohortSummary` dataclass with all fields
- `generate_summary()` - Main summary generation
- `_calculate_statistics()` - Aggregate stats (date ranges, totals, distributions)
- `_get_diverse_samples()` - Select representative samples
- `_estimate_tokens()` - Rough token count estimation

### Step 3: Create Auto-Persist Service

Create `packages/core/src/healthsim/state/auto_persist.py`:

```python
"""
Auto-persist service for HealthSim.

Implements the Structured RAG pattern:
- Summary in context (~500 tokens)
- Samples for consistency (~3000 tokens)
- Data stays in DuckDB
- Paginated queries for retrieval
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from ..db import get_connection
from .serializers import get_serializer, get_table_info, ENTITY_TABLE_MAP
from .auto_naming import generate_cohort_name, ensure_unique_name
from .summary import generate_summary, CohortSummary


@dataclass
class PersistResult:
    """Result of a persist operation."""
    cohort_id: str
    cohort_name: str
    entity_type: str
    entities_persisted: int
    entity_ids: List[str]
    summary: CohortSummary
    is_new_cohort: bool


@dataclass  
class QueryResult:
    """Result of a paginated query."""
    results: List[Dict]
    total_count: int
    page: int
    page_size: int
    has_more: bool
    query_executed: str


class AutoPersistService:
    """
    Service for auto-persisting generated entities.
    
    Implements the core Structured RAG pattern:
    1. Persist entities to DuckDB immediately after generation
    2. Return summary (not full data) to context
    3. Provide paginated queries for data retrieval
    """
    
    def __init__(self, connection=None):
        self._conn = connection
    
    @property
    def conn(self):
        if self._conn is None:
            self._conn = get_connection()
        return self._conn
    
    def persist_entities(
        self,
        entities: List[Dict],
        entity_type: str,
        cohort_id: Optional[str] = None,
        cohort_name: Optional[str] = None,
        context_keywords: Optional[List[str]] = None,
    ) -> PersistResult:
        """
        Persist entities to DuckDB and return summary.
        
        If no cohort_id provided:
        - Creates new cohort with auto-generated name
        - Uses context_keywords for naming if available
        
        Returns PersistResult with summary (NOT full entity data).
        """
        pass
    
    def get_cohort_summary(
        self,
        cohort_id: Optional[str] = None,
        cohort_name: Optional[str] = None,
        include_samples: bool = True,
        samples_per_type: int = 3,
    ) -> CohortSummary:
        """
        Get cohort summary for loading into context.
        
        IMPORTANT: Never loads full entity data!
        Returns summary (~500 tokens) + samples (~3000 tokens)
        """
        pass
    
    def query_cohort(
        self,
        cohort_id: str,
        query: str,
        limit: int = 20,
        offset: int = 0,
    ) -> QueryResult:
        """
        Execute paginated query against cohort data.
        
        - Validates query is SELECT only
        - Enforces pagination
        - Scopes to cohort_id
        """
        pass
    
    def get_entity_samples(
        self,
        cohort_id: str,
        entity_type: str,
        count: int = 3,
        strategy: str = "diverse",
    ) -> List[Dict]:
        """
        Get sample entities for pattern consistency.
        
        Strategies:
        - "diverse": Maximize variety (default)
        - "random": Random selection
        - "recent": Most recently added
        """
        pass
    
    def list_cohorts(
        self,
        filter_pattern: Optional[str] = None,
        limit: int = 20,
        sort_by: str = "updated_at",
    ) -> List[Dict]:
        """List available cohorts with brief stats."""
        pass
    
    def rename_cohort(
        self,
        cohort_id: str,
        new_name: str,
    ) -> Tuple[str, str]:
        """
        Rename a cohort.
        
        Returns: (old_name, new_name)
        """
        pass
    
    def delete_cohort(
        self,
        cohort_id: str,
        confirm: bool = False,
    ) -> Dict:
        """
        Delete cohort and all linked entities.
        
        Requires confirm=True for safety.
        """
        pass


# Module-level singleton
_service: Optional[AutoPersistService] = None


def get_auto_persist_service() -> AutoPersistService:
    """Get singleton service instance."""
    global _service
    if _service is None:
        _service = AutoPersistService()
    return _service
```

### Step 4: Write Unit Tests

Create comprehensive tests for each service:

**test_auto_naming.py:**
- Test keyword extraction from various contexts
- Test unique name generation
- Test name sanitization
- Test counter appending for duplicates

**test_summary.py:**
- Test summary generation with various entity counts
- Test statistics calculation
- Test sample selection (diverse, random, recent)
- Test token estimation

**test_auto_persist.py:**
- Test persist_entities creates cohort if needed
- Test persist_entities returns summary not data
- Test query_cohort enforces SELECT only
- Test query_cohort respects pagination
- Test list_cohorts filtering
- Test rename_cohort
- Test delete_cohort requires confirmation

### Step 5: Update __init__.py

Update `packages/core/src/healthsim/state/__init__.py` to export new classes:

```python
from .auto_persist import (
    AutoPersistService,
    PersistResult,
    QueryResult,
    get_auto_persist_service,
)
from .auto_naming import (
    generate_cohort_name,
    extract_keywords,
    ensure_unique_name,
)
from .summary import (
    CohortSummary,
    generate_summary,
)
```

### Step 6: Run Tests

```bash
cd packages/core
source .venv/bin/activate
pytest tests/state/test_auto_naming.py -v
pytest tests/state/test_summary.py -v
pytest tests/state/test_auto_persist.py -v
pytest  # All tests to check for regressions
```

## Post-flight Checklist

- [ ] All new files created with proper docstrings
- [ ] All unit tests pass
- [ ] No regressions in existing 605 tests
- [ ] Code follows existing patterns in state/ module
- [ ] Type hints on all public functions

## Success Criteria

1. `AutoPersistService` can persist entities and return summary
2. Summary is ~500 tokens (test with token estimation)
3. Queries are paginated and SELECT-only
4. Auto-naming generates unique, readable names
5. All tests pass (new + existing)

## Git Commit

```bash
git add packages/core/src/healthsim/state/auto_*.py
git add packages/core/src/healthsim/state/summary.py
git add packages/core/tests/state/test_auto_*.py
git add packages/core/tests/state/test_summary.py
git commit -m "[AutoPersist] Phase 1.1: Core auto-persist service with summary generation"
```
```

---

### Super-Prompt 1.2: Create MCP Tools

```
## Context

I'm implementing MCP tools that expose the AutoPersistService. These tools will be called by Claude during conversations.

**Read these files first:**
1. `/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src/healthsim/state/auto_persist.py` - Service we created
2. `/Users/markoswald/Developer/projects/healthsim-workspace/packages/patientsim/src/patientsim/mcp/state_server.py` - Existing MCP pattern
3. `/Users/markoswald/Developer/projects/healthsim-workspace/packages/patientsim/src/patientsim/mcp/generation_server.py` - Another MCP example

**MCP Tool Specifications (from architecture doc):**

1. `persist_entities` - Save entities, return summary
2. `get_cohort_summary` - Load summary only  
3. `query_cohort` - Paginated SQL queries
4. `list_cohorts` - List available cohorts
5. `rename_cohort` - Rename a cohort
6. `delete_cohort` - Delete with confirmation
7. `get_entity_samples` - Get samples for consistency

## Pre-flight Checklist

- [ ] Phase 1.1 complete (AutoPersistService exists)
- [ ] All existing tests pass
- [ ] Understand existing MCP server patterns

## Deliverables

1. `packages/core/src/healthsim/mcp/__init__.py` - MCP module init
2. `packages/core/src/healthsim/mcp/auto_persist_server.py` - MCP server
3. `packages/core/tests/mcp/__init__.py` - Test module init
4. `packages/core/tests/mcp/test_auto_persist_server.py` - Tests

## Step-by-Step Instructions

### Step 1: Create MCP Module Structure

```bash
mkdir -p packages/core/src/healthsim/mcp
touch packages/core/src/healthsim/mcp/__init__.py
mkdir -p packages/core/tests/mcp
touch packages/core/tests/mcp/__init__.py
```

### Step 2: Create MCP Server

Create `packages/core/src/healthsim/mcp/auto_persist_server.py`:

```python
"""
MCP Server for HealthSim Auto-Persist capabilities.

Exposes 7 tools for the Structured RAG pattern:
- persist_entities: Save entities, return summary
- get_cohort_summary: Load summary (NOT full data)
- query_cohort: Paginated SQL queries
- list_cohorts: Browse available cohorts
- rename_cohort: Rename a cohort
- delete_cohort: Delete with confirmation
- get_entity_samples: Get samples for consistency
"""

import logging
from typing import Any, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from ..state.auto_persist import get_auto_persist_service, PersistResult, QueryResult
from ..state.summary import CohortSummary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("healthsim.mcp.auto_persist")

# Initialize MCP server
app = Server("healthsim-auto-persist")


def format_persist_result(result: PersistResult) -> str:
    """Format persist result for human-readable output."""
    lines = [
        f"**Persisted {result.entities_persisted} {result.entity_type}**",
        "",
        f"- Cohort: {result.cohort_name}",
        f"- Cohort ID: `{result.cohort_id}`",
        f"- New cohort: {'Yes' if result.is_new_cohort else 'No'}",
        "",
        "**Current Totals:**",
    ]
    
    for entity_type, count in result.summary.entity_counts.items():
        lines.append(f"- {entity_type}: {count}")
    
    return "\n".join(lines)


def format_summary(summary: CohortSummary) -> str:
    """Format cohort summary for human-readable output."""
    lines = [
        f"**Cohort: {summary.name}**",
        "",
    ]
    
    if summary.description:
        lines.append(f"_{summary.description}_")
        lines.append("")
    
    lines.append("**Entity Counts:**")
    for entity_type, count in summary.entity_counts.items():
        lines.append(f"- {entity_type}: {count}")
    
    if summary.statistics:
        lines.append("")
        lines.append("**Statistics:**")
        stats = summary.statistics
        if stats.get('date_range'):
            lines.append(f"- Date range: {stats['date_range']['min']} to {stats['date_range']['max']}")
        if stats.get('total_billed'):
            lines.append(f"- Total billed: ${stats['total_billed']:,.2f}")
        if stats.get('age_range'):
            lines.append(f"- Age range: {stats['age_range']['min']}-{stats['age_range']['max']}")
    
    if summary.tags:
        lines.append("")
        lines.append(f"**Tags:** {', '.join(summary.tags)}")
    
    return "\n".join(lines)


def format_query_result(result: QueryResult) -> str:
    """Format query result with pagination info."""
    lines = [
        f"**Query Results** (Page {result.page + 1}, {len(result.results)} of {result.total_count} total)",
        "",
    ]
    
    if result.results:
        # Format as markdown table if results are dicts
        if isinstance(result.results[0], dict):
            keys = list(result.results[0].keys())[:6]  # Limit columns
            lines.append("| " + " | ".join(keys) + " |")
            lines.append("| " + " | ".join(["---"] * len(keys)) + " |")
            for row in result.results[:20]:  # Limit rows
                values = [str(row.get(k, ""))[:30] for k in keys]
                lines.append("| " + " | ".join(values) + " |")
    else:
        lines.append("_No results found._")
    
    if result.has_more:
        lines.append("")
        lines.append(f"_More results available. Use offset={result.offset + result.page_size} to see next page._")
    
    return "\n".join(lines)


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available auto-persist tools."""
    return [
        Tool(
            name="persist_entities",
            description="Save generated entities to DuckDB and return a summary. Use this after generating entities to persist them. Returns summary (NOT full entity data) to keep context manageable.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entities": {
                        "type": "array",
                        "description": "Array of entity objects to persist",
                        "items": {"type": "object"},
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "Type of entities (patient, encounter, claim, etc.)",
                    },
                    "cohort_id": {
                        "type": "string",
                        "description": "Existing cohort ID to add to (optional - creates new if not provided)",
                    },
                    "cohort_name": {
                        "type": "string",
                        "description": "Name for new cohort (optional - auto-generated if not provided)",
                    },
                    "context_keywords": {
                        "type": "array",
                        "description": "Keywords from generation context for auto-naming",
                        "items": {"type": "string"},
                    },
                },
                "required": ["entities", "entity_type"],
            },
        ),
        Tool(
            name="get_cohort_summary",
            description="Load a cohort summary into context. Returns counts, statistics, and sample entities - NOT full data. Use this when user says 'load cohort' or 'continue from'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "string",
                        "description": "Cohort UUID",
                    },
                    "cohort_name": {
                        "type": "string",
                        "description": "Cohort name (fuzzy match)",
                    },
                    "include_samples": {
                        "type": "boolean",
                        "description": "Include sample entities (default: true)",
                        "default": True,
                    },
                    "samples_per_type": {
                        "type": "integer",
                        "description": "Number of samples per entity type (default: 3)",
                        "default": 3,
                    },
                },
            },
        ),
        Tool(
            name="query_cohort",
            description="Run a paginated SQL query against cohort data. Use when user asks to 'show', 'find', 'list', or 'filter' specific data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "string",
                        "description": "Cohort to query",
                    },
                    "query": {
                        "type": "string",
                        "description": "SQL SELECT query",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Results per page (default: 20, max: 100)",
                        "default": 20,
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Starting offset for pagination",
                        "default": 0,
                    },
                },
                "required": ["cohort_id", "query"],
            },
        ),
        Tool(
            name="list_cohorts",
            description="List available cohorts. Use when user asks 'what cohorts do I have' or 'show my cohorts'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter_pattern": {
                        "type": "string",
                        "description": "Filter by name pattern",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results (default: 20)",
                        "default": 20,
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "Sort field (updated_at, name, entity_count)",
                        "default": "updated_at",
                    },
                },
            },
        ),
        Tool(
            name="rename_cohort",
            description="Rename a cohort. Use when user says 'rename this cohort' or 'call this cohort X'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "string",
                        "description": "Cohort to rename",
                    },
                    "new_name": {
                        "type": "string",
                        "description": "New name for the cohort",
                    },
                },
                "required": ["cohort_id", "new_name"],
            },
        ),
        Tool(
            name="delete_cohort",
            description="Delete a cohort and all its entities. Requires confirmation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "string",
                        "description": "Cohort to delete",
                    },
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be true to confirm deletion",
                    },
                },
                "required": ["cohort_id", "confirm"],
            },
        ),
        Tool(
            name="get_entity_samples",
            description="Get sample entities of a specific type for pattern consistency during generation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "string",
                        "description": "Cohort to get samples from",
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "Type of entities to sample",
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of samples (default: 3)",
                        "default": 3,
                    },
                    "strategy": {
                        "type": "string",
                        "description": "Sampling strategy: diverse, random, recent",
                        "default": "diverse",
                    },
                },
                "required": ["cohort_id", "entity_type"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls."""
    service = get_auto_persist_service()
    
    try:
        if name == "persist_entities":
            result = service.persist_entities(
                entities=arguments["entities"],
                entity_type=arguments["entity_type"],
                cohort_id=arguments.get("cohort_id"),
                cohort_name=arguments.get("cohort_name"),
                context_keywords=arguments.get("context_keywords"),
            )
            return [TextContent(type="text", text=format_persist_result(result))]
        
        elif name == "get_cohort_summary":
            summary = service.get_cohort_summary(
                cohort_id=arguments.get("cohort_id"),
                cohort_name=arguments.get("cohort_name"),
                include_samples=arguments.get("include_samples", True),
                samples_per_type=arguments.get("samples_per_type", 3),
            )
            return [TextContent(type="text", text=format_summary(summary))]
        
        elif name == "query_cohort":
            result = service.query_cohort(
                cohort_id=arguments["cohort_id"],
                query=arguments["query"],
                limit=min(arguments.get("limit", 20), 100),
                offset=arguments.get("offset", 0),
            )
            return [TextContent(type="text", text=format_query_result(result))]
        
        elif name == "list_cohorts":
            cohorts = service.list_cohorts(
                filter_pattern=arguments.get("filter_pattern"),
                limit=arguments.get("limit", 20),
                sort_by=arguments.get("sort_by", "updated_at"),
            )
            # Format as list
            if not cohorts:
                return [TextContent(type="text", text="No cohorts found.")]
            
            lines = ["**Your Cohorts:**", ""]
            for s in cohorts:
                lines.append(f"- **{s['name']}** ({s['updated_at'][:10]})")
                lines.append(f"  {s['entity_count']} entities")
            return [TextContent(type="text", text="\n".join(lines))]
        
        elif name == "rename_cohort":
            old_name, new_name = service.rename_cohort(
                cohort_id=arguments["cohort_id"],
                new_name=arguments["new_name"],
            )
            return [TextContent(
                type="text",
                text=f"Renamed cohort from **{old_name}** to **{new_name}**"
            )]
        
        elif name == "delete_cohort":
            if not arguments.get("confirm"):
                return [TextContent(
                    type="text",
                    text="Deletion requires `confirm: true`. This cannot be undone."
                )]
            result = service.delete_cohort(
                cohort_id=arguments["cohort_id"],
                confirm=True,
            )
            return [TextContent(
                type="text",
                text=f"Deleted cohort **{result['name']}** ({result['entity_count']} entities)"
            )]
        
        elif name == "get_entity_samples":
            samples = service.get_entity_samples(
                cohort_id=arguments["cohort_id"],
                entity_type=arguments["entity_type"],
                count=arguments.get("count", 3),
                strategy=arguments.get("strategy", "diverse"),
            )
            return [TextContent(
                type="text",
                text=f"**{len(samples)} Sample {arguments['entity_type']}:**\n\n```json\n{json.dumps(samples, indent=2, default=str)}\n```"
            )]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        logger.exception(f"Error in tool {name}")
        return [TextContent(type="text", text=f"**Error:** {str(e)}")]


async def main():
    """Run the auto-persist MCP server."""
    logger.info("Starting HealthSim Auto-Persist MCP Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Step 3: Write MCP Tests

Create `packages/core/tests/mcp/test_auto_persist_server.py` with tests for:
- Each tool returns expected format
- Error handling for missing parameters
- Pagination works correctly
- Confirmation required for delete

### Step 4: Update pyproject.toml

Add MCP server entry point:

```toml
[project.scripts]
healthsim-auto-persist = "healthsim.mcp.auto_persist_server:main"
```

### Step 5: Run Tests

```bash
cd packages/core
pytest tests/mcp/ -v
pytest  # All tests
```

## Post-flight Checklist

- [ ] All 7 MCP tools implemented
- [ ] All tools have proper descriptions
- [ ] All tools have input schemas
- [ ] Tests pass
- [ ] Entry point configured

## Success Criteria

1. MCP server starts without errors
2. All 7 tools are listed
3. Tools return properly formatted output
4. Error handling works correctly

## Git Commit

```bash
git add packages/core/src/healthsim/mcp/
git add packages/core/tests/mcp/
git commit -m "[AutoPersist] Phase 1.2: MCP tools for auto-persist service"
```
```

---

## Phase 2: Skill Updates

### Super-Prompt 2.1: Update State Management Skill

```
## Context

I'm updating the state-management skill to document the new auto-persist behavior.

**Read these files first:**
1. `/Users/markoswald/Developer/projects/healthsim-workspace/skills/common/state-management.md` - Current skill
2. `/Users/markoswald/Developer/projects/healthsim-workspace/docs/healthsim-auto-persist-architecture.html` - Architecture

**Key Changes:**
- Generation now auto-persists (no explicit save needed)
- Loading returns summary, not full data
- New MCP tools for querying
- Batch generation pattern
- Rename capability for auto-named cohorts

## Pre-flight Checklist

- [ ] Phase 1 complete (MCP tools exist)
- [ ] Understand current skill structure
- [ ] Understand new auto-persist patterns

## Deliverables

1. `skills/common/state-management.md` - Updated skill

## Step-by-Step Instructions

### Step 1: Update Overview Section

Add auto-persist explanation:

```markdown
## Overview

State Management in HealthSim now follows the **Auto-Persist Pattern**:

1. **Auto-Persist**: Generated entities are automatically saved to DuckDB
2. **Summary-in-Context**: Loading returns statistics + samples, not full data
3. **Query-on-Demand**: Full data retrieved via paginated SQL queries

This pattern enables:
- Large-scale generation (1000+ entities) without context overflow
- Fast cohort switching (only summary loaded)
- Efficient data exploration (paginated queries)
```

### Step 2: Update Trigger Phrases

Add new triggers:

```markdown
## Trigger Phrases

**Generation (Auto-Persists)**:
- "Generate 100 patients..." (auto-persists to new cohort)
- "Add more encounters..." (auto-persists to active cohort)

**Loading**:
- "Load cohort X" (loads summary only)
- "Continue from yesterday" (loads recent cohort summary)
- "Switch to diabetes cohort" (loads different cohort)

**Querying**:
- "Show patients over 65"
- "Find claims over $10,000"
- "List all encounters"
- "Show more" / "Next page"

**Management**:
- "Rename this cohort to X"
- "What cohorts do I have?"
- "Delete the test cohort"
```

### Step 3: Add New Patterns

**Batch Generation Pattern**:

```markdown
### Batch Generation (Large Scale)

When generating many entities (>50), Claude will:

1. Create cohort with auto-generated name
2. Generate in batches of 50
3. Persist each batch immediately
4. Use samples from previous batches for consistency
5. Report progress after each batch

**Example:**

User: Generate 200 Medicare members with various conditions

Claude: [Creates cohort "medicare-members-20241226"]
Batch 1: Generated 50 members... persisted.
Batch 2: Generated 50 members... persisted.
Batch 3: Generated 50 members... persisted.
Batch 4: Generated 50 members... persisted.

Complete! 200 members generated.

Summary:
- Age range: 65-89
- Conditions: Diabetes (45), Hypertension (78), COPD (32)...

Would you like to rename this cohort?
```

**Query Pattern**:

```markdown
### Querying Data

Data stays in DuckDB. Use natural language to query:

User: Show me members with diabetes

Claude: [Executes SQL query with pagination]

Results (page 1 of 5):
| member_id | name | age | primary_diagnosis |
| M001 | John Smith | 67 | E11.9 - Type 2 Diabetes |
...

20 of 97 results shown. Say "show more" for next page.
```

### Step 4: Update Examples

Replace old examples with new auto-persist patterns.

### Step 5: Update Validation Rules

Add rules about context management:

```markdown
## Validation Rules

| Rule | Description |
|------|-------------|
| Auto-persist on generation | All generated entities are automatically persisted |
| Summary loading only | `load_cohort` returns ~3,500 tokens (summary + samples) |
| Paginated queries | Queries return max 20 results per page |
| Batch size | Large generations processed in batches of 50 |
```

## Post-flight Checklist

- [ ] Overview explains auto-persist pattern
- [ ] New trigger phrases documented
- [ ] Batch generation pattern documented
- [ ] Query pattern documented
- [ ] Examples updated
- [ ] Validation rules updated

## Success Criteria

1. Skill explains auto-persist behavior clearly
2. All new capabilities documented
3. Examples are accurate and helpful

## Git Commit

```bash
git add skills/common/state-management.md
git commit -m "[AutoPersist] Phase 2.1: Update state-management skill with auto-persist patterns"
```
```

### Super-Prompt 2.2: Update DuckDB Skill

```
## Context

I'm updating the DuckDB skill to document the new MCP tools.

**Read these files first:**
1. `/Users/markoswald/Developer/projects/healthsim-workspace/skills/common/duckdb-skill.md` - Current skill
2. `/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src/healthsim/mcp/auto_persist_server.py` - MCP tools

## Deliverables

1. `skills/common/duckdb-skill.md` - Updated skill

## Step-by-Step Instructions

### Step 1: Add MCP Tools Section

Add documentation for all 7 tools:

```markdown
## MCP Tools

### persist_entities

Save generated entities to DuckDB. Returns summary (not full data).

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| entities | array | Yes | Array of entity objects |
| entity_type | string | Yes | Entity type (patient, claim, etc.) |
| cohort_id | string | No | Existing cohort to add to |
| cohort_name | string | No | Name for new cohort |
| context_keywords | array | No | Keywords for auto-naming |

**Example:**
```json
{
  "entities": [{"patient_id": "P001", "name": {...}}],
  "entity_type": "patient",
  "context_keywords": ["diabetes", "elderly"]
}
```

### get_cohort_summary

Load cohort summary into context. Never loads full data!

...
```

### Step 2: Add Query Examples

Add examples for common queries:

```markdown
## Example Queries via MCP

### Find patients with specific condition
```sql
SELECT p.*, d.code, d.description
FROM patients p
JOIN diagnoses d ON p.patient_id = d.patient_id
WHERE d.code LIKE 'E11%'  -- Type 2 Diabetes
```

### Claims over threshold
```sql
SELECT c.claim_id, c.total_billed, c.status
FROM claims c
WHERE c.total_billed > 10000
ORDER BY c.total_billed DESC
```
```

### Step 3: Update Trigger Phrases

Add triggers for new tools:

```markdown
## Trigger Phrases

- "persist these entities"
- "load cohort summary"
- "query the cohort for..."
- "show patients where..."
- "find claims with..."
- "list my cohorts"
- "rename cohort"
- "delete cohort"
- "get sample patients"
```

## Post-flight Checklist

- [ ] All 7 MCP tools documented
- [ ] Parameters table for each tool
- [ ] Examples for each tool
- [ ] Query examples updated
- [ ] Trigger phrases added

## Git Commit

```bash
git add skills/common/duckdb-skill.md
git commit -m "[AutoPersist] Phase 2.2: Update DuckDB skill with MCP tool documentation"
```
```

### Super-Prompt 2.3: Update Generation Skills

```
## Context

I'm updating generation skills across all products to include auto-persist behavior.

**Files to update:**
1. `skills/patientsim/patient-generation.md`
2. `skills/membersim/member-generation.md`
3. `skills/rxmembersim/prescription-generation.md`
4. `skills/trialsim/subject-generation.md`
5. `skills/healthsim-master-SKILL.md`

## Step-by-Step Instructions

### Step 1: Add Auto-Persist Section to Each Generation Skill

Add this pattern to each generation skill:

```markdown
## Auto-Persist Behavior

Generated entities are automatically persisted to DuckDB:

1. **Single Entity**: Persisted immediately, summary returned
2. **Small Batch (<50)**: Persisted as one batch, summary returned
3. **Large Batch (>50)**: Persisted in batches of 50 with progress updates

**Cohort Management:**
- If no active cohort: Creates new with auto-generated name
- If active cohort: Adds to existing cohort
- Auto-naming: Uses generation keywords (e.g., "diabetes-patients-20241226")

**What's Returned:**
- Summary statistics (entity counts, date ranges, etc.)
- 3 sample entities for reference
- NOT full entity data (stays in database)

**To retrieve data:**
- "Show me the patients" → Paginated query results
- "Export to JSON" → Full export to file
```

### Step 2: Update Master SKILL.md

Add auto-persist routing:

```markdown
### Auto-Persist Keywords

Route to state-management + generation skill when:
- "Generate X and save..."
- "Create 100 patients..."
- "Add more encounters..."
- "Continue generating..."

The generation will auto-persist; no explicit save needed.
```

## Post-flight Checklist

- [ ] All generation skills updated
- [ ] Master SKILL.md updated
- [ ] Consistent language across all skills

## Git Commit

```bash
git add skills/*/
git commit -m "[AutoPersist] Phase 2.3: Update generation skills with auto-persist behavior"
```
```

---

## Phase 3: Documentation Updates

### Super-Prompt 3.1: Update Architecture Documents

```
## Context

I'm updating architecture documentation to reflect auto-persist.

**Files to update:**
1. `docs/healthsim-duckdb-architecture.html`
2. `docs/healthsim-data-architecture.html`
3. `docs/healthsim-component-architecture.html`

## Deliverables

Update these HTML documents with:
- Auto-persist pattern description
- Structured RAG explanation
- Context management section
- Updated component diagrams

## Post-flight Checklist

- [ ] All architecture docs updated
- [ ] Diagrams updated
- [ ] Cross-references accurate

## Git Commit

```bash
git add docs/healthsim-*-architecture.html
git commit -m "[AutoPersist] Phase 3.1: Update architecture documentation"
```
```

### Super-Prompt 3.2: Create Hello-HealthSim Examples

```
## Context

I'm creating new examples that demonstrate auto-persist capabilities.

**Files to create:**
1. `hello-healthsim/auto-persist-basics.md`
2. `hello-healthsim/batch-generation.md`
3. `hello-healthsim/cohort-management.md`
4. `hello-healthsim/query-and-analyze.md`

## Step-by-Step Instructions

### Example 1: auto-persist-basics.md

```markdown
# Auto-Persist Basics

Learn how HealthSim automatically saves your generated data.

## What You'll Learn

1. How auto-persist works
2. Understanding cohort summaries
3. Basic querying

## Try It

### Generate a Patient (Auto-Persists!)

> "Generate a patient with Type 2 Diabetes"

Notice: A cohort was automatically created!

**Response shows:**
- Cohort name (auto-generated)
- Patient summary
- Sample data (3 patients)
- NOT full patient JSON

### Check What's Saved

> "Show my cohorts"

### Load a Cohort

> "Load the diabetes cohort"

This loads a SUMMARY, not all data. You'll see:
- Entity counts
- Statistics
- Sample entities

### Query the Data

> "Show me the patient's diagnoses"

Now you see full data (paginated).
```

### Example 2: batch-generation.md

```markdown
# Batch Generation

Generate large datasets efficiently.

## The Pattern

Large requests (>50 entities) are processed in batches:

1. Cohort created
2. Generate 50 → persist → progress update
3. Repeat until complete
4. Final summary

## Try It

> "Generate 100 Medicare members aged 65-85"

Watch the progress updates:
- "Batch 1: 50 members persisted..."
- "Batch 2: 50 members persisted..."
- "Complete! Summary: ..."

## Rename After Generation

> "Rename this cohort to medicare-demo-cohort"
```

### Example 3: cohort-management.md

```markdown
# Cohort Management

Organize and navigate your cohorts.

## List Cohorts

> "What cohorts do I have?"

## Switch Cohorts

> "Load the diabetes-cohort cohort"

## Rename Cohorts

> "Rename this to training-data-v2"

## Delete Cohorts

> "Delete the test cohort"

Note: Requires confirmation!
```

### Example 4: query-and-analyze.md

```markdown
# Query and Analyze

Explore your data with natural language queries.

## Basic Queries

> "Show all patients"
> "Find claims over $5,000"
> "List encounters from last month"

## Filtered Queries

> "Show diabetic patients over 65"
> "Find members with high deductibles"

## Pagination

Results are paginated (20 per page):

> "Show more"
> "Next page"
> "Go to page 5"

## Cross-Product Queries

> "Show patients and their claims"
> "Find members with pharmacy claims over $500"
```

## Post-flight Checklist

- [ ] All 4 examples created
- [ ] Examples follow existing hello-healthsim format
- [ ] Each example is self-contained
- [ ] Update hello-healthsim/README.md index

## Git Commit

```bash
git add hello-healthsim/
git commit -m "[AutoPersist] Phase 3.2: Create hello-healthsim examples for auto-persist"
```
```

### Super-Prompt 3.3: Update README Files

```
## Context

I'm updating README files across the project.

**Files to update:**
1. `README.md` (main)
2. `packages/core/README.md`
3. `tools/README.md`
4. `skills/README.md`

## Step-by-Step Instructions

### Main README.md

Add section:

```markdown
## Auto-Persist & Structured RAG

HealthSim uses an intelligent data management pattern:

- **Auto-Persist**: Generated entities are automatically saved to DuckDB
- **Summary-in-Context**: Only summaries loaded to conversation (not full data)
- **Query-on-Demand**: Retrieve specific data via paginated SQL queries

This enables generating and managing thousands of entities without context overflow.

See [Auto-Persist Architecture](docs/healthsim-auto-persist-architecture.html) for details.
```

### packages/core/README.md

Add MCP server documentation:

```markdown
## MCP Servers

### Auto-Persist Server

```bash
python -m healthsim.mcp.auto_persist_server
```

Tools:
- `persist_entities` - Save entities, return summary
- `get_cohort_summary` - Load cohort summary
- `query_cohort` - Paginated SQL queries
- `list_cohorts` - Browse cohorts
- `rename_cohort` - Rename cohort
- `delete_cohort` - Delete cohort
- `get_entity_samples` - Get sample entities
```

## Post-flight Checklist

- [ ] Main README updated
- [ ] packages/core/README updated
- [ ] tools/README updated
- [ ] skills/README updated

## Git Commit

```bash
git add README.md
git add packages/core/README.md
git add tools/README.md
git add skills/README.md
git commit -m "[AutoPersist] Phase 3.3: Update README files with auto-persist documentation"
```
```

---

## Phase 4: Integration Testing

### Super-Prompt 4.1: End-to-End Testing

```
## Context

I'm running comprehensive integration tests for auto-persist.

## Pre-flight Checklist

- [ ] All phases 1-3 complete
- [ ] All unit tests pass
- [ ] Database is clean/reset

## Test Cohorts

### Test 1: Single Entity Generation

1. Clear any existing test cohort
2. Generate 1 patient with diabetes
3. Verify: Cohort created with auto-name
4. Verify: Summary returned (not full JSON)
5. Query: "Show the patient"
6. Verify: Full patient data returned

### Test 2: Batch Generation

1. Generate 100 patients
2. Verify: Progress updates shown (2 batches)
3. Verify: Final summary shows 100 patients
4. Query: "Show patients over 65"
5. Verify: Paginated results

### Test 3: Cohort Management

1. List cohorts
2. Rename the batch cohort
3. Verify: Name changed
4. Delete a test cohort
5. Verify: Cohort removed

### Test 4: Cross-Product Flow

1. Generate member with patient linkage
2. Generate claim for the member
3. Query: "Show member with their claims"
4. Verify: Cross-product query works

### Test 5: Large Scale (stress test)

1. Generate 500 patients
2. Verify: No context overflow
3. Verify: All patients persisted
4. Query various subsets
5. Verify: Pagination works at scale

## Post-flight Checklist

- [ ] All 5 test cohorts pass
- [ ] No regressions in existing tests
- [ ] Performance acceptable

## Git Commit

```bash
git add tests/integration/
git commit -m "[AutoPersist] Phase 4.1: Integration tests for auto-persist"
```
```

---

## Phase 5: Final Cleanup

### Super-Prompt 5.1: Final Review and Commit

```
## Context

Final cleanup and comprehensive commit.

## Pre-flight Checklist

- [ ] All phases 1-4 complete
- [ ] All tests pass (run pytest across all packages)
- [ ] All documentation updated

## Steps

### 1. Run Full Test Suite

```bash
# Core package
cd packages/core && pytest -v

# PatientSim
cd ../patientsim && pytest -v

# MemberSim
cd ../membersim && pytest -v

# RxMemberSim
cd ../rxmembersim && pytest -v
```

### 2. Verify Documentation Links

Check all cross-references in:
- Skills files
- README files
- Architecture docs

### 3. Update CHANGELOG.md

```markdown
## [Unreleased]

### Added
- **Auto-Persist Feature**: Generated entities are automatically saved to DuckDB
- **Structured RAG Pattern**: Summary-in-context, data-in-database approach
- New MCP tools: persist_entities, get_cohort_summary, query_cohort, 
  list_cohorts, rename_cohort, delete_cohort, get_entity_samples
- Batch generation support for large-scale entity creation (>50 entities)
- Auto-naming service for cohorts based on generation context
- Token-efficient cohort summaries (~500 tokens)
- Paginated query results (20 per page default)
- Hello-HealthSim examples for auto-persist patterns

### Changed
- State management skill updated with auto-persist behavior
- DuckDB skill updated with new MCP tool documentation
- All generation skills updated to document auto-persist
- Architecture documentation updated

### Technical Details
- New modules: healthsim.state.auto_persist, auto_naming, summary
- New MCP server: healthsim-auto-persist
- Context budget: ~5,500 tokens working (500 summary + 3000 samples + 2000 query)
- Batch size: 50 entities per batch
```

### 4. Git Operations

```bash
# Verify status
git status

# Add all changes
git add .

# Commit
git commit -m "[AutoPersist] Complete implementation of auto-persist feature

- Core service: AutoPersistService with Structured RAG pattern
- MCP tools: 7 tools for persist, query, and manage operations
- Skills: Updated state-management, duckdb, and generation skills
- Documentation: Architecture docs, README files, hello-healthsim examples
- Tests: Unit tests and integration tests

Design decisions:
- Batch size: 50 entities
- Auto-naming: {keywords}-{YYYYMMDD}
- Samples: 3 per entity type
- Query page size: 20 results
- Context budget: ~5,500 tokens"

# Tag milestone
git tag -a v0.5.0-auto-persist -m "Auto-persist feature complete"

# Push
git push origin main --tags
```

## Post-flight Checklist

- [ ] All tests pass
- [ ] All documentation updated
- [ ] CHANGELOG.md updated
- [ ] Git commit complete
- [ ] Tag created
- [ ] Implementation plan marked complete

## Success Criteria

1. "Generate 1000 patients" works without context overflow
2. "Load cohort X" returns summary in <1 second
3. "Show patients where..." returns paginated results
4. All existing functionality still works
5. Documentation is complete and accurate
```

---

## Appendix: File Reference

### Files to CREATE (16 files)

| File | Phase | Purpose |
|------|-------|---------|
| `packages/core/src/healthsim/state/auto_persist.py` | 1.1 | Core service |
| `packages/core/src/healthsim/state/auto_naming.py` | 1.1 | Naming service |
| `packages/core/src/healthsim/state/summary.py` | 1.1 | Summary generation |
| `packages/core/tests/state/test_auto_persist.py` | 1.1 | Unit tests |
| `packages/core/tests/state/test_auto_naming.py` | 1.1 | Unit tests |
| `packages/core/tests/state/test_summary.py` | 1.1 | Unit tests |
| `packages/core/src/healthsim/mcp/__init__.py` | 1.2 | Module init |
| `packages/core/src/healthsim/mcp/auto_persist_server.py` | 1.2 | MCP server |
| `packages/core/tests/mcp/__init__.py` | 1.2 | Test module |
| `packages/core/tests/mcp/test_auto_persist_server.py` | 1.2 | MCP tests |
| `hello-healthsim/auto-persist-basics.md` | 3.2 | Example |
| `hello-healthsim/batch-generation.md` | 3.2 | Example |
| `hello-healthsim/cohort-management.md` | 3.2 | Example |
| `hello-healthsim/query-and-analyze.md` | 3.2 | Example |
| `tests/integration/test_auto_persist.py` | 4.1 | Integration tests |

### Files to MODIFY (15+ files)

| File | Phase | Changes |
|------|-------|---------|
| `packages/core/src/healthsim/state/__init__.py` | 1.1 | Export new classes |
| `packages/core/pyproject.toml` | 1.2 | Add entry point |
| `skills/common/state-management.md` | 2.1 | Auto-persist patterns |
| `skills/common/duckdb-skill.md` | 2.2 | MCP tool docs |
| `skills/patientsim/*.md` | 2.3 | Generation skills |
| `skills/membersim/*.md` | 2.3 | Generation skills |
| `skills/rxmembersim/*.md` | 2.3 | Generation skills |
| `skills/trialsim/*.md` | 2.3 | Generation skills |
| `skills/healthsim-master-SKILL.md` | 2.3 | Routing updates |
| `docs/healthsim-duckdb-architecture.html` | 3.1 | Architecture |
| `docs/healthsim-data-architecture.html` | 3.1 | Architecture |
| `README.md` | 3.3 | Main README |
| `packages/core/README.md` | 3.3 | Package README |
| `tools/README.md` | 3.3 | Tools README |
| `CHANGELOG.md` | 5.1 | Release notes |

---

*Document created: December 26, 2024*
*For use with: HealthSim Auto-Persist Implementation*
