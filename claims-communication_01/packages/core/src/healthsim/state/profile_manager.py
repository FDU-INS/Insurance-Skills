"""Profile persistence for HealthSim.

Provides save/load/list/delete operations for profile specifications,
enabling reusable profile definitions and execution history tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4
import json
import time

import duckdb


@dataclass
class ProfileRecord:
    """A saved profile specification."""
    id: str
    name: str
    description: Optional[str]
    version: int
    profile_spec: Dict[str, Any]
    product: Optional[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ExecutionRecord:
    """Record of a profile execution."""
    id: int
    profile_id: str
    cohort_id: Optional[str]
    executed_at: datetime
    seed: Optional[int]
    count: int
    duration_ms: int
    status: str
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ProfileSummary:
    """Summary of a profile for listing."""
    id: str
    name: str
    description: Optional[str]
    version: int
    product: Optional[str]
    tags: List[str]
    created_at: datetime
    execution_count: int = 0
    last_executed: Optional[datetime] = None


class ProfileManager:
    """Manages profile persistence in DuckDB.
    
    Profiles are reusable generation specifications that define how to
    create entities. They can be saved, versioned, and re-executed.
    
    Usage:
        manager = ProfileManager(conn)
        
        # Save a profile
        profile_id = manager.save_profile(
            name='harris-diabetic',
            profile_spec={...},
            description='Diabetic patients in Harris County',
            tags=['diabetes', 'harris-county']
        )
        
        # Load and use
        profile = manager.load_profile('harris-diabetic')
        
        # Record execution
        manager.record_execution(
            profile_id=profile_id,
            cohort_id='cohort-123',
            seed=42,
            count=100,
            duration_ms=1500
        )
        
        # List profiles
        profiles = manager.list_profiles(tags=['diabetes'])
    """
    
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        """Initialize profile manager.
        
        Args:
            conn: DuckDB connection
        """
        self.conn = conn
        self._ensure_tables()
    
    def _ensure_tables(self) -> None:
        """Ensure profile tables exist."""
        # Check if profiles table exists
        result = self.conn.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'profiles'
        """).fetchone()
        
        if result[0] == 0:
            # Create sequence and tables
            self.conn.execute("""
                CREATE SEQUENCE IF NOT EXISTS profiles_seq START 1
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id              VARCHAR PRIMARY KEY,
                    name            VARCHAR NOT NULL UNIQUE,
                    description     VARCHAR,
                    version         INTEGER DEFAULT 1,
                    profile_spec    JSON NOT NULL,
                    product         VARCHAR,
                    tags            JSON,
                    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata        JSON
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS profile_executions (
                    id              INTEGER PRIMARY KEY DEFAULT nextval('profiles_seq'),
                    profile_id      VARCHAR NOT NULL,
                    cohort_id       VARCHAR,
                    executed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    seed            INTEGER,
                    count           INTEGER,
                    duration_ms     INTEGER,
                    status          VARCHAR DEFAULT 'completed',
                    error_message   VARCHAR,
                    metadata        JSON
                )
            """)
    
    # =========================================================================
    # Profile CRUD Operations
    # =========================================================================
    
    def save_profile(
        self,
        name: str,
        profile_spec: Dict[str, Any],
        description: Optional[str] = None,
        product: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Save a new profile specification.
        
        Args:
            name: Unique profile name
            profile_spec: Profile specification dictionary
            description: Human-readable description
            product: Product type (patientsim, membersim, etc.)
            tags: List of tags for filtering
            metadata: Additional metadata
            
        Returns:
            Profile ID
            
        Raises:
            ValueError: If profile with name already exists
        """
        profile_id = f"profile-{uuid4().hex[:8]}"
        
        # Check for existing profile with same name
        existing = self.conn.execute(
            "SELECT id FROM profiles WHERE name = ?",
            [name]
        ).fetchone()
        
        if existing:
            raise ValueError(f"Profile with name '{name}' already exists. Use update_profile() or delete first.")
        
        # Infer product from profile_spec if not provided
        if not product:
            product = profile_spec.get("profile", {}).get("product")
        
        self.conn.execute("""
            INSERT INTO profiles (id, name, description, version, profile_spec, product, tags, metadata)
            VALUES (?, ?, ?, 1, ?, ?, ?, ?)
        """, [
            profile_id,
            name,
            description,
            json.dumps(profile_spec),
            product,
            json.dumps(tags or []),
            json.dumps(metadata) if metadata else None
        ])
        
        return profile_id
    
    def load_profile(self, name_or_id: str) -> ProfileRecord:
        """Load a profile by name or ID.
        
        Args:
            name_or_id: Profile name or ID
            
        Returns:
            ProfileRecord with full specification
            
        Raises:
            ValueError: If profile not found
        """
        result = self.conn.execute("""
            SELECT id, name, description, version, profile_spec, product, tags, 
                   created_at, updated_at, metadata
            FROM profiles
            WHERE name = ? OR id = ?
        """, [name_or_id, name_or_id]).fetchone()
        
        if not result:
            raise ValueError(f"Profile not found: {name_or_id}")
        
        return ProfileRecord(
            id=result[0],
            name=result[1],
            description=result[2],
            version=result[3],
            profile_spec=json.loads(result[4]) if isinstance(result[4], str) else result[4],
            product=result[5],
            tags=json.loads(result[6]) if isinstance(result[6], str) else (result[6] or []),
            created_at=result[7],
            updated_at=result[8],
            metadata=json.loads(result[9]) if result[9] and isinstance(result[9], str) else result[9]
        )
    
    def update_profile(
        self,
        name_or_id: str,
        profile_spec: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        bump_version: bool = True,
    ) -> ProfileRecord:
        """Update an existing profile.
        
        Args:
            name_or_id: Profile name or ID
            profile_spec: New profile specification (optional)
            description: New description (optional)
            tags: New tags (optional)
            metadata: New metadata (optional)
            bump_version: Whether to increment version number
            
        Returns:
            Updated ProfileRecord
            
        Raises:
            ValueError: If profile not found
        """
        # Load existing profile
        existing = self.load_profile(name_or_id)
        
        # Build update
        new_version = existing.version + 1 if bump_version else existing.version
        new_spec = profile_spec if profile_spec is not None else existing.profile_spec
        new_desc = description if description is not None else existing.description
        new_tags = tags if tags is not None else existing.tags
        new_metadata = metadata if metadata is not None else existing.metadata
        
        self.conn.execute("""
            UPDATE profiles
            SET profile_spec = ?,
                description = ?,
                version = ?,
                tags = ?,
                metadata = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, [
            json.dumps(new_spec),
            new_desc,
            new_version,
            json.dumps(new_tags),
            json.dumps(new_metadata) if new_metadata else None,
            existing.id
        ])
        
        return self.load_profile(existing.id)
    
    def delete_profile(self, name_or_id: str, delete_executions: bool = True) -> bool:
        """Delete a profile.
        
        Args:
            name_or_id: Profile name or ID
            delete_executions: Whether to delete execution history
            
        Returns:
            True if deleted, False if not found
        """
        # Get profile ID
        result = self.conn.execute("""
            SELECT id FROM profiles WHERE name = ? OR id = ?
        """, [name_or_id, name_or_id]).fetchone()
        
        if not result:
            return False
        
        profile_id = result[0]
        
        # Delete executions if requested
        if delete_executions:
            self.conn.execute(
                "DELETE FROM profile_executions WHERE profile_id = ?",
                [profile_id]
            )
        
        # Delete profile
        self.conn.execute("DELETE FROM profiles WHERE id = ?", [profile_id])
        return True
    
    def list_profiles(
        self,
        product: Optional[str] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        limit: int = 50,
    ) -> List[ProfileSummary]:
        """List profiles with optional filtering.
        
        Args:
            product: Filter by product type
            tags: Filter by tags (any match)
            search: Search in name and description
            limit: Maximum results
            
        Returns:
            List of ProfileSummary objects
        """
        query = """
            SELECT p.id, p.name, p.description, p.version, p.product, p.tags, p.created_at,
                   COUNT(e.id) as exec_count,
                   MAX(e.executed_at) as last_exec
            FROM profiles p
            LEFT JOIN profile_executions e ON p.id = e.profile_id
            WHERE 1=1
        """
        params = []
        
        if product:
            query += " AND p.product = ?"
            params.append(product)
        
        if search:
            query += " AND (p.name ILIKE ? OR p.description ILIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        query += " GROUP BY p.id, p.name, p.description, p.version, p.product, p.tags, p.created_at, p.updated_at"
        query += " ORDER BY p.updated_at DESC"
        query += f" LIMIT {limit}"
        
        results = self.conn.execute(query, params).fetchall()
        
        summaries = []
        for row in results:
            profile_tags = json.loads(row[5]) if isinstance(row[5], str) else (row[5] or [])
            
            # Filter by tags if requested
            if tags:
                if not any(t in profile_tags for t in tags):
                    continue
            
            summaries.append(ProfileSummary(
                id=row[0],
                name=row[1],
                description=row[2],
                version=row[3],
                product=row[4],
                tags=profile_tags,
                created_at=row[6],
                execution_count=row[7] or 0,
                last_executed=row[8]
            ))
        
        return summaries
    
    # =========================================================================
    # Execution History
    # =========================================================================
    
    def record_execution(
        self,
        profile_id: str,
        cohort_id: Optional[str] = None,
        seed: Optional[int] = None,
        count: int = 0,
        duration_ms: int = 0,
        status: str = "completed",
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Record a profile execution.
        
        Args:
            profile_id: Profile that was executed
            cohort_id: Cohort that was created (if any)
            seed: Random seed used
            count: Number of entities generated
            duration_ms: Execution time in milliseconds
            status: 'completed', 'failed', or 'partial'
            error_message: Error details if failed
            metadata: Additional execution metadata
            
        Returns:
            Execution ID
        """
        result = self.conn.execute("""
            INSERT INTO profile_executions 
            (profile_id, cohort_id, seed, count, duration_ms, status, error_message, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
        """, [
            profile_id,
            cohort_id,
            seed,
            count,
            duration_ms,
            status,
            error_message,
            json.dumps(metadata) if metadata else None
        ]).fetchone()
        
        return result[0]
    
    def get_executions(
        self,
        profile_id: str,
        limit: int = 20,
    ) -> List[ExecutionRecord]:
        """Get execution history for a profile.
        
        Args:
            profile_id: Profile ID or name
            limit: Maximum executions to return
            
        Returns:
            List of ExecutionRecords, newest first
        """
        # Resolve profile ID
        profile = self.load_profile(profile_id)
        
        results = self.conn.execute("""
            SELECT id, profile_id, cohort_id, executed_at, seed, count, 
                   duration_ms, status, error_message, metadata
            FROM profile_executions
            WHERE profile_id = ?
            ORDER BY executed_at DESC
            LIMIT ?
        """, [profile.id, limit]).fetchall()
        
        return [
            ExecutionRecord(
                id=row[0],
                profile_id=row[1],
                cohort_id=row[2],
                executed_at=row[3],
                seed=row[4],
                count=row[5],
                duration_ms=row[6],
                status=row[7],
                error_message=row[8],
                metadata=json.loads(row[9]) if row[9] and isinstance(row[9], str) else row[9]
            )
            for row in results
        ]
    
    def get_cohort_profile(self, cohort_id: str) -> Optional[ProfileRecord]:
        """Get the profile used to generate a cohort.
        
        Args:
            cohort_id: Cohort ID
            
        Returns:
            ProfileRecord if cohort was generated from a profile, None otherwise
        """
        result = self.conn.execute("""
            SELECT profile_id FROM profile_executions WHERE cohort_id = ?
        """, [cohort_id]).fetchone()
        
        if not result:
            return None
        
        return self.load_profile(result[0])
    
    # =========================================================================
    # Re-execution Support
    # =========================================================================
    
    def get_execution_spec(
        self,
        execution_id: int,
    ) -> Dict[str, Any]:
        """Get profile spec with seed from a specific execution.
        
        Useful for re-running with the same seed to reproduce results.
        
        Args:
            execution_id: Execution ID
            
        Returns:
            Profile spec with seed applied
        """
        result = self.conn.execute("""
            SELECT e.seed, e.count, p.profile_spec
            FROM profile_executions e
            JOIN profiles p ON e.profile_id = p.id
            WHERE e.id = ?
        """, [execution_id]).fetchone()
        
        if not result:
            raise ValueError(f"Execution not found: {execution_id}")
        
        seed, count, spec_json = result
        spec = json.loads(spec_json) if isinstance(spec_json, str) else spec_json
        
        # Apply seed and count from execution
        if "profile" not in spec:
            spec["profile"] = {}
        if "generation" not in spec["profile"]:
            spec["profile"]["generation"] = {}
        
        if seed is not None:
            spec["profile"]["generation"]["seed"] = seed
        if count:
            spec["profile"]["generation"]["count"] = count
        
        return spec


# Convenience function
def get_profile_manager(conn: Optional[duckdb.DuckDBPyConnection] = None) -> ProfileManager:
    """Get a ProfileManager instance.
    
    Args:
        conn: Optional database connection
        
    Returns:
        ProfileManager instance
    """
    if conn is None:
        from ..db import get_connection
        conn = get_connection()
    return ProfileManager(conn)
