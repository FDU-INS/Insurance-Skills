"""Journey persistence for HealthSim.

Provides save/load/list/delete operations for journey specifications,
enabling reusable journey definitions and execution history tracking.

Journeys define temporal event sequences that can be applied to entities
(patients, members, subjects) to generate realistic healthcare timelines.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4
import json

import duckdb


@dataclass
class JourneyRecord:
    """A saved journey specification."""
    id: str
    name: str
    description: Optional[str]
    version: int
    journey_spec: Dict[str, Any]
    products: List[str]
    tags: List[str]
    duration_days: Optional[int]
    event_count: int
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class JourneyExecutionRecord:
    """Record of a journey execution."""
    id: int
    journey_id: str
    profile_id: Optional[str]
    cohort_id: Optional[str]
    entity_id: Optional[str]
    executed_at: datetime
    start_date: Optional[date]
    end_date: Optional[date]
    events_generated: int
    duration_ms: int
    status: str
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class JourneySummary:
    """Summary of a journey for listing."""
    id: str
    name: str
    description: Optional[str]
    version: int
    products: List[str]
    tags: List[str]
    duration_days: Optional[int]
    event_count: int
    created_at: datetime
    execution_count: int = 0
    last_executed: Optional[datetime] = None


class JourneyManager:
    """Manages journey persistence in DuckDB.
    
    Journeys are reusable temporal event sequences that define how
    healthcare events unfold over time for an entity. They can be
    saved, versioned, and executed against profiles or individual entities.
    
    Usage:
        manager = JourneyManager(conn)
        
        # Save a journey
        journey_id = manager.save_journey(
            name='diabetic-first-year',
            journey_spec={
                "journey_id": "diabetic-first-year",
                "name": "First Year Diabetes Management",
                "duration_days": 365,
                "events": [...]
            },
            description='Quarterly visits with labs for new diabetics',
            tags=['diabetes', 'chronic-care']
        )
        
        # Load and use
        journey = manager.load_journey('diabetic-first-year')
        
        # Record execution
        manager.record_execution(
            journey_id=journey_id,
            entity_id='patient-123',
            start_date=date(2024, 1, 1),
            events_generated=12,
            duration_ms=500
        )
        
        # List journeys
        journeys = manager.list_journeys(products=['patientsim'])
    """
    
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        """Initialize journey manager.
        
        Args:
            conn: DuckDB connection
        """
        self.conn = conn
        self._ensure_tables()
    
    def _ensure_tables(self) -> None:
        """Ensure journey tables exist."""
        result = self.conn.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'journeys'
        """).fetchone()
        
        if result[0] == 0:
            self.conn.execute("""
                CREATE SEQUENCE IF NOT EXISTS journeys_seq START 1
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS journeys (
                    id              VARCHAR PRIMARY KEY,
                    name            VARCHAR NOT NULL UNIQUE,
                    description     VARCHAR,
                    version         INTEGER DEFAULT 1,
                    journey_spec    JSON NOT NULL,
                    products        JSON,
                    tags            JSON,
                    duration_days   INTEGER,
                    event_count     INTEGER,
                    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata        JSON
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS journey_executions (
                    id              INTEGER PRIMARY KEY DEFAULT nextval('journeys_seq'),
                    journey_id      VARCHAR NOT NULL,
                    profile_id      VARCHAR,
                    cohort_id       VARCHAR,
                    entity_id       VARCHAR,
                    executed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    start_date      DATE,
                    end_date        DATE,
                    events_generated INTEGER,
                    duration_ms     INTEGER,
                    status          VARCHAR DEFAULT 'completed',
                    error_message   VARCHAR,
                    metadata        JSON
                )
            """)
    
    # =========================================================================
    # Journey CRUD Operations
    # =========================================================================
    
    def save_journey(
        self,
        name: str,
        journey_spec: Dict[str, Any],
        description: Optional[str] = None,
        products: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Save a new journey specification.
        
        Args:
            name: Unique journey name
            journey_spec: Journey specification dictionary (JourneySpecification format)
            description: Human-readable description
            products: List of products this journey applies to
            tags: List of tags for filtering
            metadata: Additional metadata
            
        Returns:
            Journey ID
            
        Raises:
            ValueError: If journey with name already exists
        """
        journey_id = f"journey-{uuid4().hex[:8]}"
        
        # Check for existing journey with same name
        existing = self.conn.execute(
            "SELECT id FROM journeys WHERE name = ?",
            [name]
        ).fetchone()
        
        if existing:
            raise ValueError(f"Journey with name '{name}' already exists. Use update_journey() or delete first.")
        
        # Extract metadata from spec if not provided
        if not products:
            products = journey_spec.get("products", ["patientsim"])
        
        duration_days = journey_spec.get("duration_days")
        events = journey_spec.get("events", [])
        event_count = len(events)
        
        self.conn.execute("""
            INSERT INTO journeys (id, name, description, version, journey_spec, products, tags, duration_days, event_count, metadata)
            VALUES (?, ?, ?, 1, ?, ?, ?, ?, ?, ?)
        """, [
            journey_id,
            name,
            description or journey_spec.get("description", ""),
            json.dumps(journey_spec),
            json.dumps(products),
            json.dumps(tags or []),
            duration_days,
            event_count,
            json.dumps(metadata) if metadata else None
        ])
        
        return journey_id
    
    def load_journey(self, name_or_id: str) -> JourneyRecord:
        """Load a journey by name or ID.
        
        Args:
            name_or_id: Journey name or ID
            
        Returns:
            JourneyRecord with full specification
            
        Raises:
            ValueError: If journey not found
        """
        result = self.conn.execute("""
            SELECT id, name, description, version, journey_spec, products, tags,
                   duration_days, event_count, created_at, updated_at, metadata
            FROM journeys
            WHERE name = ? OR id = ?
        """, [name_or_id, name_or_id]).fetchone()
        
        if not result:
            raise ValueError(f"Journey not found: {name_or_id}")
        
        return JourneyRecord(
            id=result[0],
            name=result[1],
            description=result[2],
            version=result[3],
            journey_spec=json.loads(result[4]) if isinstance(result[4], str) else result[4],
            products=json.loads(result[5]) if isinstance(result[5], str) else (result[5] or []),
            tags=json.loads(result[6]) if isinstance(result[6], str) else (result[6] or []),
            duration_days=result[7],
            event_count=result[8],
            created_at=result[9],
            updated_at=result[10],
            metadata=json.loads(result[11]) if result[11] and isinstance(result[11], str) else result[11]
        )
    
    def update_journey(
        self,
        name_or_id: str,
        journey_spec: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
        products: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        bump_version: bool = True,
    ) -> JourneyRecord:
        """Update an existing journey.
        
        Args:
            name_or_id: Journey name or ID
            journey_spec: New journey specification (optional)
            description: New description (optional)
            products: New products list (optional)
            tags: New tags (optional)
            metadata: New metadata (optional)
            bump_version: Whether to increment version number
            
        Returns:
            Updated JourneyRecord
            
        Raises:
            ValueError: If journey not found
        """
        existing = self.load_journey(name_or_id)
        
        new_version = existing.version + 1 if bump_version else existing.version
        new_spec = journey_spec if journey_spec is not None else existing.journey_spec
        new_desc = description if description is not None else existing.description
        new_products = products if products is not None else existing.products
        new_tags = tags if tags is not None else existing.tags
        new_metadata = metadata if metadata is not None else existing.metadata
        
        # Recalculate derived fields if spec changed
        duration_days = new_spec.get("duration_days") if journey_spec else existing.duration_days
        event_count = len(new_spec.get("events", [])) if journey_spec else existing.event_count
        
        self.conn.execute("""
            UPDATE journeys
            SET journey_spec = ?,
                description = ?,
                version = ?,
                products = ?,
                tags = ?,
                duration_days = ?,
                event_count = ?,
                metadata = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, [
            json.dumps(new_spec),
            new_desc,
            new_version,
            json.dumps(new_products),
            json.dumps(new_tags),
            duration_days,
            event_count,
            json.dumps(new_metadata) if new_metadata else None,
            existing.id
        ])
        
        return self.load_journey(existing.id)
    
    def delete_journey(self, name_or_id: str, delete_executions: bool = True) -> bool:
        """Delete a journey.
        
        Args:
            name_or_id: Journey name or ID
            delete_executions: Whether to delete execution history
            
        Returns:
            True if deleted, False if not found
        """
        result = self.conn.execute("""
            SELECT id FROM journeys WHERE name = ? OR id = ?
        """, [name_or_id, name_or_id]).fetchone()
        
        if not result:
            return False
        
        journey_id = result[0]
        
        if delete_executions:
            self.conn.execute(
                "DELETE FROM journey_executions WHERE journey_id = ?",
                [journey_id]
            )
        
        self.conn.execute("DELETE FROM journeys WHERE id = ?", [journey_id])
        return True
    
    def list_journeys(
        self,
        products: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        limit: int = 50,
    ) -> List[JourneySummary]:
        """List journeys with optional filtering.
        
        Args:
            products: Filter by products (any match)
            tags: Filter by tags (any match)
            search: Search in name and description
            limit: Maximum results
            
        Returns:
            List of JourneySummary objects
        """
        query = """
            SELECT j.id, j.name, j.description, j.version, j.products, j.tags,
                   j.duration_days, j.event_count, j.created_at,
                   COUNT(e.id) as exec_count,
                   MAX(e.executed_at) as last_exec
            FROM journeys j
            LEFT JOIN journey_executions e ON j.id = e.journey_id
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (j.name ILIKE ? OR j.description ILIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        query += " GROUP BY j.id, j.name, j.description, j.version, j.products, j.tags, j.duration_days, j.event_count, j.created_at, j.updated_at"
        query += " ORDER BY j.updated_at DESC"
        query += f" LIMIT {limit}"
        
        results = self.conn.execute(query, params).fetchall()
        
        summaries = []
        for row in results:
            journey_products = json.loads(row[4]) if isinstance(row[4], str) else (row[4] or [])
            journey_tags = json.loads(row[5]) if isinstance(row[5], str) else (row[5] or [])
            
            # Filter by products if requested
            if products:
                if not any(p in journey_products for p in products):
                    continue
            
            # Filter by tags if requested
            if tags:
                if not any(t in journey_tags for t in tags):
                    continue
            
            summaries.append(JourneySummary(
                id=row[0],
                name=row[1],
                description=row[2],
                version=row[3],
                products=journey_products,
                tags=journey_tags,
                duration_days=row[6],
                event_count=row[7],
                created_at=row[8],
                execution_count=row[9] or 0,
                last_executed=row[10]
            ))
        
        return summaries
    
    def journey_exists(self, name_or_id: str) -> bool:
        """Check if a journey exists.
        
        Args:
            name_or_id: Journey name or ID
            
        Returns:
            True if journey exists
        """
        result = self.conn.execute("""
            SELECT COUNT(*) FROM journeys WHERE name = ? OR id = ?
        """, [name_or_id, name_or_id]).fetchone()
        return result[0] > 0
    
    # =========================================================================
    # Execution History
    # =========================================================================
    
    def record_execution(
        self,
        journey_id: str,
        profile_id: Optional[str] = None,
        cohort_id: Optional[str] = None,
        entity_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        events_generated: int = 0,
        duration_ms: int = 0,
        status: str = "completed",
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Record a journey execution.
        
        Args:
            journey_id: Journey that was executed
            profile_id: Profile used (if any)
            cohort_id: Cohort created (if any)
            entity_id: Entity the journey was executed for
            start_date: Journey start date
            end_date: Journey end date
            events_generated: Number of events generated
            duration_ms: Execution time in milliseconds
            status: 'completed', 'failed', or 'partial'
            error_message: Error details if failed
            metadata: Additional execution metadata
            
        Returns:
            Execution ID
        """
        result = self.conn.execute("""
            INSERT INTO journey_executions 
            (journey_id, profile_id, cohort_id, entity_id, start_date, end_date,
             events_generated, duration_ms, status, error_message, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
        """, [
            journey_id,
            profile_id,
            cohort_id,
            entity_id,
            start_date,
            end_date,
            events_generated,
            duration_ms,
            status,
            error_message,
            json.dumps(metadata) if metadata else None
        ]).fetchone()
        
        return result[0]
    
    def get_executions(
        self,
        journey_id: str,
        limit: int = 20,
    ) -> List[JourneyExecutionRecord]:
        """Get execution history for a journey.
        
        Args:
            journey_id: Journey ID or name
            limit: Maximum executions to return
            
        Returns:
            List of JourneyExecutionRecords, newest first
        """
        journey = self.load_journey(journey_id)
        
        results = self.conn.execute("""
            SELECT id, journey_id, profile_id, cohort_id, entity_id, executed_at,
                   start_date, end_date, events_generated, duration_ms, status,
                   error_message, metadata
            FROM journey_executions
            WHERE journey_id = ?
            ORDER BY executed_at DESC
            LIMIT ?
        """, [journey.id, limit]).fetchall()
        
        return [
            JourneyExecutionRecord(
                id=row[0],
                journey_id=row[1],
                profile_id=row[2],
                cohort_id=row[3],
                entity_id=row[4],
                executed_at=row[5],
                start_date=row[6],
                end_date=row[7],
                events_generated=row[8],
                duration_ms=row[9],
                status=row[10],
                error_message=row[11],
                metadata=json.loads(row[12]) if row[12] and isinstance(row[12], str) else row[12]
            )
            for row in results
        ]
    
    def get_entity_journeys(self, entity_id: str) -> List[JourneyExecutionRecord]:
        """Get all journey executions for a specific entity.
        
        Args:
            entity_id: Entity ID (patient, member, subject)
            
        Returns:
            List of JourneyExecutionRecords for this entity
        """
        results = self.conn.execute("""
            SELECT id, journey_id, profile_id, cohort_id, entity_id, executed_at,
                   start_date, end_date, events_generated, duration_ms, status,
                   error_message, metadata
            FROM journey_executions
            WHERE entity_id = ?
            ORDER BY executed_at DESC
        """, [entity_id]).fetchall()
        
        return [
            JourneyExecutionRecord(
                id=row[0],
                journey_id=row[1],
                profile_id=row[2],
                cohort_id=row[3],
                entity_id=row[4],
                executed_at=row[5],
                start_date=row[6],
                end_date=row[7],
                events_generated=row[8],
                duration_ms=row[9],
                status=row[10],
                error_message=row[11],
                metadata=json.loads(row[12]) if row[12] and isinstance(row[12], str) else row[12]
            )
            for row in results
        ]
    
    # =========================================================================
    # Built-in Journey Templates
    # =========================================================================
    
    def import_builtin_journeys(self) -> int:
        """Import built-in journey templates.
        
        Imports the standard journey templates from skill_journeys.py
        and auto_journeys.py into the database.
        
        Returns:
            Number of journeys imported
        """
        imported = 0
        
        # Import from auto_journeys (most commonly used)
        try:
            from healthsim.generation.auto_journeys import JOURNEY_TEMPLATES
            for template in JOURNEY_TEMPLATES:
                name = template.get("journey_id", template.get("id"))
                if name and not self.journey_exists(name):
                    self.save_journey(
                        name=name,
                        journey_spec=template,
                        tags=["builtin", "auto-resolution"]
                    )
                    imported += 1
        except ImportError:
            pass
        
        # Import from skill_journeys
        try:
            from healthsim.generation.skill_journeys import SKILL_JOURNEY_TEMPLATES
            for template in SKILL_JOURNEY_TEMPLATES:
                name = template.get("journey_id", template.get("id"))
                if name and not self.journey_exists(name):
                    self.save_journey(
                        name=name,
                        journey_spec=template,
                        tags=["builtin", "skill-aware"]
                    )
                    imported += 1
        except ImportError:
            pass
        
        return imported


# Convenience function
def get_journey_manager(conn: Optional[duckdb.DuckDBPyConnection] = None) -> JourneyManager:
    """Get a JourneyManager instance.
    
    Args:
        conn: Optional database connection
        
    Returns:
        JourneyManager instance
    """
    if conn is None:
        from ..db import get_connection
        conn = get_connection()
    return JourneyManager(conn)
