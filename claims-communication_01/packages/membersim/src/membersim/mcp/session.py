"""MemberSim session and workspace management.

Extends healthsim-core's Session and SessionManager for health plan
member-specific data management with claims, authorizations, and
care gaps tracking.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from healthsim.state import (
    EntityWithProvenance,
    Provenance,
    Session,
    Workspace,
)
from healthsim.state import (
    SessionManager as BaseSessionManager,
)

from membersim.claims.claim import Claim
from membersim.core.member import Member


class MemberSession(Session[Member]):
    """Session containing a member and related payer entities.

    A MemberSession tracks a health plan member along with their:
    - Claims (medical, pharmacy, dental)
    - Authorizations (prior auth requests/decisions)
    - Care gaps (HEDIS measure compliance status)
    - Accumulators (deductible, OOP tracking)
    """

    def __init__(
        self,
        member: Member,
        claims: list[Claim] | None = None,
        authorizations: list[Any] | None = None,
        care_gaps: list[Any] | None = None,
        accumulators: dict[str, Any] | None = None,
        provenance: Provenance | None = None,
    ):
        """Initialize a member session.

        Args:
            member: The health plan member
            claims: Associated claims
            authorizations: Prior auth requests/decisions
            care_gaps: HEDIS care gap status
            accumulators: Deductible/OOP tracking
            provenance: How this data was created
        """
        self._id = str(uuid4())[:8]
        self._member = member
        self.claims = claims or []
        self.authorizations = authorizations or []
        self.care_gaps = care_gaps or []
        self.accumulators = accumulators or {}
        self._provenance = provenance or Provenance.generated()

    @property
    def id(self) -> str:
        """Unique session identifier."""
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """Set session ID (used during load)."""
        self._id = value

    @property
    def primary_entity(self) -> Member:
        """The primary entity (member)."""
        return self._member

    @property
    def member(self) -> Member:
        """Convenience alias for primary_entity."""
        return self._member

    @property
    def provenance(self) -> Provenance:
        """Session provenance."""
        return self._provenance

    @provenance.setter
    def provenance(self, value: Provenance) -> None:
        """Set provenance."""
        self._provenance = value

    def to_entities_with_provenance(self) -> dict[str, list[EntityWithProvenance]]:
        """Convert session to serializable entities with provenance.

        Returns:
            Dict mapping entity type to list of EntityWithProvenance
        """
        entities: dict[str, list[EntityWithProvenance]] = {}

        # Member
        entities["members"] = [
            EntityWithProvenance(
                entity_id=self._member.member_id,
                entity_type="members",
                data=self._member.model_dump(mode="json"),
                provenance=self._provenance,
            )
        ]

        # Claims
        if self.claims:
            entities["claims"] = [
                EntityWithProvenance(
                    entity_id=claim.claim_id,
                    entity_type="claims",
                    data=claim.model_dump(mode="json"),
                    provenance=self._provenance,
                )
                for claim in self.claims
            ]

        # Authorizations
        if self.authorizations:
            entities["authorizations"] = [
                EntityWithProvenance(
                    entity_id=getattr(auth, "auth_id", str(uuid4())),
                    entity_type="authorizations",
                    data=auth.model_dump(mode="json") if hasattr(auth, "model_dump") else auth,
                    provenance=self._provenance,
                )
                for auth in self.authorizations
            ]

        # Care gaps
        if self.care_gaps:
            entities["care_gaps"] = [
                EntityWithProvenance(
                    entity_id=str(uuid4())[:8],
                    entity_type="care_gaps",
                    data=gap.model_dump(mode="json") if hasattr(gap, "model_dump") else gap,
                    provenance=self._provenance,
                )
                for gap in self.care_gaps
            ]

        # Accumulators (stored per-member)
        if self.accumulators:
            entities["accumulators"] = [
                EntityWithProvenance(
                    entity_id=f"{self._member.member_id}-accum",
                    entity_type="accumulators",
                    data={
                        "member_id": self._member.member_id,
                        **self.accumulators,
                    },
                    provenance=self._provenance,
                )
            ]

        return entities

    def to_summary(self) -> dict[str, Any]:
        """Create summary dict for display.

        Returns:
            Dict with session overview information
        """
        member = self._member
        return {
            "id": self._id,
            "member_id": member.member_id,
            "name": f"{member.name.given_name} {member.name.family_name}",
            "age": member.age,
            "gender": member.gender.value if hasattr(member.gender, "value") else str(member.gender),
            "plan_code": member.plan_code,
            "coverage_status": "Active" if member.is_active else "Inactive",
            "claims_count": len(self.claims),
            "auth_count": len(self.authorizations),
            "care_gaps_count": len(self.care_gaps),
        }

    @classmethod
    def from_entities_with_provenance(
        cls,
        member_entity: EntityWithProvenance,
        all_entities: dict[str, list[EntityWithProvenance]],
    ) -> MemberSession:
        """Reconstruct a session from workspace entities.

        Args:
            member_entity: The member entity with provenance
            all_entities: All entities from the workspace

        Returns:
            Reconstructed MemberSession
        """
        from datetime import date

        from healthsim.person import Address, Gender, PersonName

        # Reconstruct Member from entity data
        data = member_entity.data
        member_id = data["member_id"]

        # Build name
        name_data = data.get("name", {})
        name = PersonName(
            given_name=name_data.get("given_name", ""),
            family_name=name_data.get("family_name", ""),
            middle_name=name_data.get("middle_name"),
            prefix=name_data.get("prefix"),
            suffix=name_data.get("suffix"),
        )

        # Build address if present
        address = None
        if data.get("address"):
            addr_data = data["address"]
            address = Address(
                street=addr_data.get("street", ""),
                city=addr_data.get("city", ""),
                state=addr_data.get("state", ""),
                zip_code=addr_data.get("zip_code", ""),
            )

        # Parse gender
        gender_val = data.get("gender", "M")
        if isinstance(gender_val, str):
            gender = Gender.MALE if gender_val.upper() in ("M", "MALE") else Gender.FEMALE
        else:
            gender = gender_val

        # Parse dates
        birth_date = data.get("birth_date")
        if isinstance(birth_date, str):
            birth_date = date.fromisoformat(birth_date)

        coverage_start = data.get("coverage_start")
        if isinstance(coverage_start, str):
            coverage_start = date.fromisoformat(coverage_start)

        coverage_end = data.get("coverage_end")
        if coverage_end and isinstance(coverage_end, str):
            coverage_end = date.fromisoformat(coverage_end)

        member = Member(
            id=data.get("id", f"member-{member_id}"),
            name=name,
            birth_date=birth_date,
            gender=gender,
            address=address,
            member_id=member_id,
            subscriber_id=data.get("subscriber_id"),
            relationship_code=data.get("relationship_code", "18"),
            group_id=data.get("group_id", ""),
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            plan_code=data.get("plan_code", ""),
            pcp_npi=data.get("pcp_npi"),
        )

        # Find related claims for this member
        claims = []
        for claim_ent in all_entities.get("claims", []):
            if claim_ent.data.get("member_id") == member_id:
                claims.append(cls._reconstruct_claim(claim_ent.data))

        # Find related authorizations
        authorizations = []
        for auth_ent in all_entities.get("authorizations", []):
            if auth_ent.data.get("member_id") == member_id:
                authorizations.append(auth_ent.data)

        # Find care gaps
        care_gaps = []
        for gap_ent in all_entities.get("care_gaps", []):
            if gap_ent.data.get("member_id") == member_id:
                care_gaps.append(gap_ent.data)

        # Find accumulators
        accumulators = {}
        for acc_ent in all_entities.get("accumulators", []):
            if acc_ent.data.get("member_id") == member_id:
                # Copy all data except member_id
                accumulators = {k: v for k, v in acc_ent.data.items() if k != "member_id"}
                break  # One accumulator per member

        return cls(
            member=member,
            claims=claims,
            authorizations=authorizations,
            care_gaps=care_gaps,
            accumulators=accumulators,
            provenance=member_entity.provenance,
        )

    @staticmethod
    def _reconstruct_claim(data: dict) -> Claim:
        """Reconstruct a Claim from serialized data."""
        from datetime import date
        from decimal import Decimal

        from membersim.claims.claim import Claim, ClaimLine

        # Reconstruct claim lines
        lines = []
        for line_data in data.get("claim_lines", []):
            service_date = line_data.get("service_date")
            if isinstance(service_date, str):
                service_date = date.fromisoformat(service_date)

            lines.append(
                ClaimLine(
                    line_number=line_data["line_number"],
                    procedure_code=line_data["procedure_code"],
                    procedure_modifiers=line_data.get("procedure_modifiers", []),
                    service_date=service_date,
                    units=Decimal(str(line_data.get("units", "1"))),
                    charge_amount=Decimal(str(line_data["charge_amount"])),
                    diagnosis_pointers=line_data.get("diagnosis_pointers", [1]),
                    revenue_code=line_data.get("revenue_code"),
                    ndc_code=line_data.get("ndc_code"),
                    place_of_service=line_data.get("place_of_service", "11"),
                )
            )

        # Parse dates
        service_date = data.get("service_date")
        if isinstance(service_date, str):
            service_date = date.fromisoformat(service_date)

        admission_date = data.get("admission_date")
        if admission_date and isinstance(admission_date, str):
            admission_date = date.fromisoformat(admission_date)

        discharge_date = data.get("discharge_date")
        if discharge_date and isinstance(discharge_date, str):
            discharge_date = date.fromisoformat(discharge_date)

        return Claim(
            claim_id=data["claim_id"],
            claim_type=data.get("claim_type", "PROFESSIONAL"),
            member_id=data["member_id"],
            subscriber_id=data.get("subscriber_id", data["member_id"]),
            provider_npi=data["provider_npi"],
            facility_npi=data.get("facility_npi"),
            service_date=service_date,
            admission_date=admission_date,
            discharge_date=discharge_date,
            place_of_service=data.get("place_of_service", "11"),
            claim_lines=lines,
            principal_diagnosis=data["principal_diagnosis"],
            other_diagnoses=data.get("other_diagnoses", []),
            authorization_number=data.get("authorization_number"),
        )


class MemberSessionManager(BaseSessionManager[Member]):
    """Session manager for MemberSim workspace operations.

    Manages member sessions and provides save/load functionality
    using healthsim-core's workspace persistence.
    """

    def __init__(self, workspace_dir: Path | None = None):
        """Initialize the session manager.

        Args:
            workspace_dir: Optional directory for workspace storage.
                          Uses default WORKSPACES_DIR if not specified.
        """
        self._sessions: list[MemberSession] = []
        self._workspace_dir = workspace_dir

    @property
    def product_name(self) -> str:
        """Product identifier for workspace filtering."""
        return "membersim"

    def _get_workspace_dir(self) -> Path | None:
        """Get workspace directory for persistence operations."""
        return self._workspace_dir

    # === Abstract method implementations ===

    def count(self) -> int:
        """Get total number of member sessions."""
        return len(self._sessions)

    def clear(self) -> None:
        """Clear all member sessions."""
        self._sessions.clear()

    def get_all(self) -> list[Session[Member]]:
        """Get all member sessions."""
        return list(self._sessions)

    def get_by_id(self, session_id: str) -> Session[Member] | None:
        """Get member session by ID."""
        for session in self._sessions:
            if session.id == session_id:
                return session
        return None

    def add(
        self,
        entity: Member,
        provenance: Provenance | None = None,
        **related: Any,
    ) -> Session[Member]:
        """Add new session with primary entity.

        Args:
            entity: Member to add
            provenance: Optional provenance for the entity
            **related: Related entities (claims, authorizations, etc.)

        Returns:
            Created session
        """
        session = MemberSession(
            member=entity,
            claims=related.get("claims"),
            authorizations=related.get("authorizations"),
            care_gaps=related.get("care_gaps"),
            accumulators=related.get("accumulators"),
            provenance=provenance,
        )
        self._sessions.append(session)
        return session

    def _load_entities_from_workspace(
        self,
        workspace: Workspace,
    ) -> tuple[Workspace, dict[str, Any]]:
        """Reconstruct member sessions from workspace entities.

        Args:
            workspace: Workspace to load entities from

        Returns:
            Tuple of (workspace, load statistics dict)
        """
        stats = {
            "members_loaded": 0,
            "members_skipped": 0,
            "total_entities": workspace.get_entity_count(),
            "conflicts": [],
        }

        member_entities = workspace.entities.get("members", [])

        for member_ent in member_entities:
            member_id = member_ent.data.get("member_id")

            # Check for member_id conflict
            if member_id:
                existing = self.get_by_member_id(member_id)
                if existing:
                    stats["conflicts"].append({
                        "member_id": member_id,
                        "resolution": "skipped",
                    })
                    stats["members_skipped"] += 1
                    continue

            # Reconstruct session
            session = MemberSession.from_entities_with_provenance(
                member_ent, workspace.entities
            )

            # Update provenance to mark as loaded
            session.provenance = Provenance.loaded(source_system="membersim")

            self._sessions.append(session)
            stats["members_loaded"] += 1

        return workspace, stats

    # === MemberSim-specific methods ===

    def add_member(
        self,
        member: Member,
        claims: list[Claim] | None = None,
        authorizations: list[Any] | None = None,
        care_gaps: list[Any] | None = None,
        accumulators: dict[str, Any] | None = None,
        provenance: Provenance | None = None,
    ) -> MemberSession:
        """Add a member to the session (convenience method).

        Args:
            member: The health plan member
            claims: Associated claims
            authorizations: Prior auth requests
            care_gaps: HEDIS care gaps
            accumulators: Deductible/OOP tracking
            provenance: How this data was created

        Returns:
            Created MemberSession
        """
        session = MemberSession(
            member=member,
            claims=claims,
            authorizations=authorizations,
            care_gaps=care_gaps,
            accumulators=accumulators,
            provenance=provenance,
        )
        self._sessions.append(session)
        return session

    def get_by_member_id(self, member_id: str) -> MemberSession | None:
        """Get member session by member ID."""
        for session in self._sessions:
            if session.member.member_id == member_id:
                return session
        return None

    def get_latest(self) -> MemberSession | None:
        """Get the most recently added member session."""
        if self._sessions:
            return self._sessions[-1]
        return None

    def list_all(self) -> list[MemberSession]:
        """Get all member sessions (legacy method, use get_all())."""
        return self._sessions.copy()

    def add_claim(self, member_id: str, claim: Claim) -> bool:
        """Add a claim to a member's session.

        Args:
            member_id: Member ID to add claim to
            claim: Claim to add

        Returns:
            True if claim was added, False if member not found
        """
        session = self.get_by_member_id(member_id)
        if session:
            session.claims.append(claim)
            return True
        return False

    # === Legacy cohort methods (delegate to workspace methods) ===

    def save_cohort(
        self,
        name: str,
        description: str | None = None,
        tags: list[str] | None = None,
        member_ids: list[str] | None = None,
    ) -> Workspace:
        """Save current workspace as a cohort (legacy alias for save_workspace).

        Args:
            name: Human-readable name for the cohort
            description: Optional description
            tags: Optional tags for organization
            member_ids: Specific member IDs to save (None = all)

        Returns:
            Saved Workspace object
        """
        # Filter sessions if member_ids specified
        if member_ids:
            original_sessions = self._sessions
            self._sessions = [s for s in self._sessions if s.member.member_id in member_ids]
            result = self.save_workspace(name, description, tags)
            self._sessions = original_sessions
            return result
        return self.save_workspace(name, description, tags)

    def load_cohort(
        self,
        cohort_id: str | None = None,
        name: str | None = None,
        mode: str = "replace",
        member_ids: list[str] | None = None,  # noqa: ARG002
    ) -> tuple[Workspace, dict[str, Any]]:
        """Load a cohort into the workspace (legacy alias for load_workspace).

        Args:
            cohort_id: UUID of cohort to load
            name: Name to search for (if cohort_id not provided)
            mode: "replace" (clear first) or "merge" (add to existing)
            member_ids: Specific member IDs to load (ignored, loads all)

        Returns:
            Tuple of (Workspace, load_summary)
        """
        del member_ids  # Unused - loads all members
        return self.load_workspace(
            workspace_id=cohort_id,
            name=name,
            mode=mode,
        )

    def list_cohorts(
        self,
        search: str | None = None,
        tags: list[str] | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """List saved cohorts with metadata (legacy alias for list_workspaces)."""
        workspaces = self.list_workspaces(search=search, tags=tags, limit=limit)

        # Add legacy field names
        for w in workspaces:
            w["cohort_id"] = w["workspace_id"]
            w["member_count"] = w.get("entity_count", 0)

        return workspaces

    def delete_cohort(self, cohort_id: str) -> dict[str, Any] | None:
        """Delete a saved cohort (legacy alias for delete_workspace)."""
        result = self.delete_workspace(cohort_id)
        if result:
            result["cohort_id"] = result["workspace_id"]
            result["member_count"] = result.get("entity_count", 0)
        return result

    def get_workspace_summary(self) -> dict[str, Any]:
        """Get summary of current workspace state."""
        total_claims = sum(len(s.claims) for s in self._sessions)
        total_auths = sum(len(s.authorizations) for s in self._sessions)
        total_care_gaps = sum(len(s.care_gaps) for s in self._sessions)

        # Provenance breakdown
        prov_counts = {"loaded": 0, "generated": 0, "derived": 0}
        for session in self._sessions:
            prov_counts[session.provenance.source_type.value] += 1

        return {
            "member_count": len(self._sessions),
            "claims_count": total_claims,
            "authorization_count": total_auths,
            "care_gap_count": total_care_gaps,
            "provenance_summary": prov_counts,
        }


# Global session manager for MCP server
session_manager = MemberSessionManager()
