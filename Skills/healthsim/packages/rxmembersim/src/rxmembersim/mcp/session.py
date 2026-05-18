"""RxMemberSim session and workspace management.

Extends healthsim-core's Session and SessionManager for pharmacy
benefit member-specific data management with prescriptions,
pharmacy claims, DUR alerts, and prior authorizations.
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

from rxmembersim.claims.claim import PharmacyClaim
from rxmembersim.core.member import RxMember
from rxmembersim.core.prescription import Prescription


class RxMemberSession(Session[RxMember]):
    """Session containing an RxMember and related pharmacy entities.

    An RxMemberSession tracks a pharmacy benefit member along with their:
    - Prescriptions (active Rx)
    - Pharmacy claims (adjudicated claims)
    - DUR alerts (drug utilization review)
    - Prior authorizations (specialty/step therapy)
    """

    def __init__(
        self,
        rx_member: RxMember,
        prescriptions: list[Prescription] | None = None,
        pharmacy_claims: list[PharmacyClaim] | None = None,
        dur_alerts: list[Any] | None = None,
        prior_auths: list[Any] | None = None,
        provenance: Provenance | None = None,
    ):
        """Initialize an RxMember session.

        Args:
            rx_member: The pharmacy benefit member
            prescriptions: Active prescriptions
            pharmacy_claims: Adjudicated pharmacy claims
            dur_alerts: Drug utilization review alerts
            prior_auths: Prior authorization requests
            provenance: How this data was created
        """
        self._id = str(uuid4())[:8]
        self._rx_member = rx_member
        self.prescriptions = prescriptions or []
        self.pharmacy_claims = pharmacy_claims or []
        self.dur_alerts = dur_alerts or []
        self.prior_auths = prior_auths or []
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
    def primary_entity(self) -> RxMember:
        """The primary entity (rx_member)."""
        return self._rx_member

    @property
    def rx_member(self) -> RxMember:
        """Convenience alias for primary_entity."""
        return self._rx_member

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

        # RxMember
        entities["rx_members"] = [
            EntityWithProvenance(
                entity_id=self._rx_member.member_id,
                entity_type="rx_members",
                data=self._rx_member.model_dump(mode="json"),
                provenance=self._provenance,
            )
        ]

        # Prescriptions - inject member_id for filtering on load
        if self.prescriptions:
            entities["prescriptions"] = []
            for rx in self.prescriptions:
                rx_data = rx.model_dump(mode="json")
                rx_data["member_id"] = self._rx_member.member_id  # Add for linkage
                entities["prescriptions"].append(
                    EntityWithProvenance(
                        entity_id=rx.prescription_number,
                        entity_type="prescriptions",
                        data=rx_data,
                        provenance=self._provenance,
                    )
                )

        # Pharmacy claims
        if self.pharmacy_claims:
            entities["pharmacy_claims"] = [
                EntityWithProvenance(
                    entity_id=claim.claim_id,
                    entity_type="pharmacy_claims",
                    data=claim.model_dump(mode="json"),
                    provenance=self._provenance,
                )
                for claim in self.pharmacy_claims
            ]

        # DUR alerts
        if self.dur_alerts:
            entities["dur_alerts"] = [
                EntityWithProvenance(
                    entity_id=str(uuid4())[:8],
                    entity_type="dur_alerts",
                    data=alert.model_dump(mode="json") if hasattr(alert, "model_dump") else alert,
                    provenance=self._provenance,
                )
                for alert in self.dur_alerts
            ]

        # Prior authorizations
        if self.prior_auths:
            entities["prior_auths"] = [
                EntityWithProvenance(
                    entity_id=getattr(pa, "auth_id", str(uuid4())),
                    entity_type="prior_auths",
                    data=pa.model_dump(mode="json") if hasattr(pa, "model_dump") else pa,
                    provenance=self._provenance,
                )
                for pa in self.prior_auths
            ]

        return entities

    def to_summary(self) -> dict[str, Any]:
        """Create summary dict for display.

        Returns:
            Dict with session overview information
        """
        member = self._rx_member
        demo = member.demographics
        return {
            "id": self._id,
            "member_id": member.member_id,
            "cardholder_id": member.cardholder_id,
            "name": f"{demo.first_name} {demo.last_name}",
            "bin": member.bin,
            "pcn": member.pcn,
            "group": member.group_number,
            "prescription_count": len(self.prescriptions),
            "claims_count": len(self.pharmacy_claims),
            "dur_alerts_count": len(self.dur_alerts),
            "prior_auth_count": len(self.prior_auths),
        }

    @classmethod
    def from_entities_with_provenance(
        cls,
        rx_member_entity: EntityWithProvenance,
        all_entities: dict[str, list[EntityWithProvenance]],
    ) -> RxMemberSession:
        """Reconstruct a session from workspace entities.

        Args:
            rx_member_entity: The rx_member entity with provenance
            all_entities: All entities from the workspace

        Returns:
            Reconstructed RxMemberSession
        """
        from datetime import date
        from decimal import Decimal

        from rxmembersim.core.member import (
            BenefitAccumulators,
            MemberDemographics,
            RxMember,
        )

        # Reconstruct RxMember from entity data
        data = rx_member_entity.data
        member_id = data["member_id"]

        # Build demographics
        demo_data = data.get("demographics", {})
        dob = demo_data.get("date_of_birth")
        if isinstance(dob, str):
            dob = date.fromisoformat(dob)

        demographics = MemberDemographics(
            first_name=demo_data.get("first_name", ""),
            last_name=demo_data.get("last_name", ""),
            date_of_birth=dob,
            gender=demo_data.get("gender", "U"),
            address_line1=demo_data.get("address_line1"),
            address_line2=demo_data.get("address_line2"),
            city=demo_data.get("city"),
            state=demo_data.get("state"),
            zip_code=demo_data.get("zip_code"),
            phone=demo_data.get("phone"),
        )

        # Build accumulators
        acc_data = data.get("accumulators", {})
        accumulators = BenefitAccumulators(
            deductible_met=Decimal(str(acc_data.get("deductible_met", "0"))),
            deductible_remaining=Decimal(str(acc_data.get("deductible_remaining", "0"))),
            oop_met=Decimal(str(acc_data.get("oop_met", "0"))),
            oop_remaining=Decimal(str(acc_data.get("oop_remaining", "0"))),
        )

        # Parse effective date
        effective_date = data.get("effective_date")
        if isinstance(effective_date, str):
            effective_date = date.fromisoformat(effective_date)

        termination_date = data.get("termination_date")
        if termination_date and isinstance(termination_date, str):
            termination_date = date.fromisoformat(termination_date)

        rx_member = RxMember(
            member_id=member_id,
            cardholder_id=data.get("cardholder_id", member_id),
            person_code=data.get("person_code", "01"),
            bin=data.get("bin", ""),
            pcn=data.get("pcn", ""),
            group_number=data.get("group_number", ""),
            demographics=demographics,
            effective_date=effective_date,
            termination_date=termination_date,
            accumulators=accumulators,
            plan_code=data.get("plan_code"),
            formulary_id=data.get("formulary_id"),
        )

        # Find related prescriptions for this member
        prescriptions = []
        for rx_ent in all_entities.get("prescriptions", []):
            if rx_ent.data.get("member_id") == member_id:
                prescriptions.append(cls._reconstruct_prescription(rx_ent.data))

        # Find related pharmacy claims
        pharmacy_claims = []
        for claim_ent in all_entities.get("pharmacy_claims", []):
            if claim_ent.data.get("member_id") == member_id:
                pharmacy_claims.append(cls._reconstruct_pharmacy_claim(claim_ent.data))

        # DUR alerts and prior auths (just store as dicts for now)
        dur_alerts = [
            a.data for a in all_entities.get("dur_alerts", [])
            if a.data.get("member_id") == member_id
        ]
        prior_auths = [
            pa.data for pa in all_entities.get("prior_auths", [])
            if pa.data.get("member_id") == member_id
        ]

        return cls(
            rx_member=rx_member,
            prescriptions=prescriptions,
            pharmacy_claims=pharmacy_claims,
            dur_alerts=dur_alerts,
            prior_auths=prior_auths,
            provenance=rx_member_entity.provenance,
        )

    @staticmethod
    def _reconstruct_prescription(data: dict) -> Prescription:
        """Reconstruct a Prescription from serialized data."""
        from datetime import date
        from decimal import Decimal

        from rxmembersim.core.prescription import DAWCode, Prescription

        written_date = data.get("written_date")
        if isinstance(written_date, str):
            written_date = date.fromisoformat(written_date)

        expiration_date = data.get("expiration_date")
        if isinstance(expiration_date, str):
            expiration_date = date.fromisoformat(expiration_date)

        daw_code = data.get("daw_code", "0")
        if isinstance(daw_code, str):
            daw_code = DAWCode(daw_code)

        return Prescription(
            prescription_number=data["prescription_number"],
            ndc=data["ndc"],
            drug_name=data.get("drug_name", ""),
            quantity_prescribed=Decimal(str(data.get("quantity_prescribed", "0"))),
            days_supply=data.get("days_supply", 0),
            refills_authorized=data.get("refills_authorized", 0),
            refills_remaining=data.get("refills_remaining", 0),
            prescriber_npi=data.get("prescriber_npi", ""),
            prescriber_name=data.get("prescriber_name"),
            prescriber_dea=data.get("prescriber_dea"),
            written_date=written_date,
            expiration_date=expiration_date,
            daw_code=daw_code,
            diagnosis_codes=data.get("diagnosis_codes", []),
            directions=data.get("directions"),
        )

    @staticmethod
    def _reconstruct_pharmacy_claim(data: dict) -> PharmacyClaim:
        """Reconstruct a PharmacyClaim from serialized data."""
        from datetime import date
        from decimal import Decimal

        from rxmembersim.claims.claim import PharmacyClaim, TransactionCode

        service_date = data.get("service_date")
        if isinstance(service_date, str):
            service_date = date.fromisoformat(service_date)

        transaction_code = data.get("transaction_code", "B1")
        if isinstance(transaction_code, str):
            transaction_code = TransactionCode(transaction_code)

        return PharmacyClaim(
            claim_id=data["claim_id"],
            transaction_code=transaction_code,
            service_date=service_date,
            pharmacy_npi=data["pharmacy_npi"],
            pharmacy_ncpdp=data.get("pharmacy_ncpdp"),
            member_id=data["member_id"],
            cardholder_id=data.get("cardholder_id", data["member_id"]),
            person_code=data.get("person_code", "01"),
            bin=data.get("bin", ""),
            pcn=data.get("pcn", ""),
            group_number=data.get("group_number", ""),
            prescription_number=data["prescription_number"],
            fill_number=data.get("fill_number", 1),
            ndc=data["ndc"],
            quantity_dispensed=Decimal(str(data.get("quantity_dispensed", "0"))),
            days_supply=data.get("days_supply", 0),
            daw_code=data.get("daw_code", "0"),
            compound_code=data.get("compound_code", "0"),
            prescriber_npi=data.get("prescriber_npi", ""),
            ingredient_cost_submitted=Decimal(str(data.get("ingredient_cost_submitted", "0"))),
            dispensing_fee_submitted=Decimal(str(data.get("dispensing_fee_submitted", "0"))),
            usual_customary_charge=Decimal(str(data.get("usual_customary_charge", "0"))),
            gross_amount_due=Decimal(str(data.get("gross_amount_due", "0"))),
            prior_auth_number=data.get("prior_auth_number"),
            prior_auth_type=data.get("prior_auth_type"),
            dur_pps_code_counter=data.get("dur_pps_code_counter", 0),
            dur_reason_for_service=data.get("dur_reason_for_service"),
            dur_professional_service=data.get("dur_professional_service"),
            dur_result_of_service=data.get("dur_result_of_service"),
        )


class RxMemberSessionManager(BaseSessionManager[RxMember]):
    """Session manager for RxMemberSim workspace operations.

    Manages rx_member sessions and provides save/load functionality
    using healthsim-core's workspace persistence.
    """

    def __init__(self, workspace_dir: Path | None = None):
        """Initialize the session manager.

        Args:
            workspace_dir: Optional directory for workspace storage.
                          Uses default WORKSPACES_DIR if not specified.
        """
        self._sessions: list[RxMemberSession] = []
        self._workspace_dir = workspace_dir

    @property
    def product_name(self) -> str:
        """Product identifier for workspace filtering."""
        return "rxmembersim"

    def _get_workspace_dir(self) -> Path | None:
        """Get workspace directory for persistence operations."""
        return self._workspace_dir

    # === Abstract method implementations ===

    def count(self) -> int:
        """Get total number of rx_member sessions."""
        return len(self._sessions)

    def clear(self) -> None:
        """Clear all rx_member sessions."""
        self._sessions.clear()

    def get_all(self) -> list[Session[RxMember]]:
        """Get all rx_member sessions."""
        return list(self._sessions)

    def get_by_id(self, session_id: str) -> Session[RxMember] | None:
        """Get rx_member session by ID."""
        for session in self._sessions:
            if session.id == session_id:
                return session
        return None

    def add(
        self,
        entity: RxMember,
        provenance: Provenance | None = None,
        **related: Any,
    ) -> Session[RxMember]:
        """Add new session with primary entity.

        Args:
            entity: RxMember to add
            provenance: Optional provenance for the entity
            **related: Related entities (prescriptions, claims, etc.)

        Returns:
            Created session
        """
        session = RxMemberSession(
            rx_member=entity,
            prescriptions=related.get("prescriptions"),
            pharmacy_claims=related.get("pharmacy_claims"),
            dur_alerts=related.get("dur_alerts"),
            prior_auths=related.get("prior_auths"),
            provenance=provenance,
        )
        self._sessions.append(session)
        return session

    def _load_entities_from_workspace(
        self,
        workspace: Workspace,
    ) -> tuple[Workspace, dict[str, Any]]:
        """Reconstruct rx_member sessions from workspace entities.

        Args:
            workspace: Workspace to load entities from

        Returns:
            Tuple of (workspace, load statistics dict)
        """
        stats = {
            "rx_members_loaded": 0,
            "rx_members_skipped": 0,
            "total_entities": workspace.get_entity_count(),
            "conflicts": [],
        }

        rx_member_entities = workspace.entities.get("rx_members", [])

        for rx_member_ent in rx_member_entities:
            member_id = rx_member_ent.data.get("member_id")

            # Check for member_id conflict
            if member_id:
                existing = self.get_by_member_id(member_id)
                if existing:
                    stats["conflicts"].append({
                        "member_id": member_id,
                        "resolution": "skipped",
                    })
                    stats["rx_members_skipped"] += 1
                    continue

            # Reconstruct session
            session = RxMemberSession.from_entities_with_provenance(
                rx_member_ent, workspace.entities
            )

            # Update provenance to mark as loaded
            session.provenance = Provenance.loaded(source_system="rxmembersim")

            self._sessions.append(session)
            stats["rx_members_loaded"] += 1

        return workspace, stats

    # === RxMemberSim-specific methods ===

    def add_rx_member(
        self,
        rx_member: RxMember,
        prescriptions: list[Prescription] | None = None,
        pharmacy_claims: list[PharmacyClaim] | None = None,
        dur_alerts: list[Any] | None = None,
        prior_auths: list[Any] | None = None,
        provenance: Provenance | None = None,
    ) -> RxMemberSession:
        """Add an rx_member to the session (convenience method).

        Args:
            rx_member: The pharmacy benefit member
            prescriptions: Active prescriptions
            pharmacy_claims: Pharmacy claims
            dur_alerts: DUR alerts
            prior_auths: Prior authorizations
            provenance: How this data was created

        Returns:
            Created RxMemberSession
        """
        session = RxMemberSession(
            rx_member=rx_member,
            prescriptions=prescriptions,
            pharmacy_claims=pharmacy_claims,
            dur_alerts=dur_alerts,
            prior_auths=prior_auths,
            provenance=provenance,
        )
        self._sessions.append(session)
        return session

    def get_by_member_id(self, member_id: str) -> RxMemberSession | None:
        """Get rx_member session by member ID."""
        for session in self._sessions:
            if session.rx_member.member_id == member_id:
                return session
        return None

    def get_latest(self) -> RxMemberSession | None:
        """Get the most recently added rx_member session."""
        if self._sessions:
            return self._sessions[-1]
        return None

    def list_all(self) -> list[RxMemberSession]:
        """Get all rx_member sessions (legacy method, use get_all())."""
        return self._sessions.copy()

    def add_claim(self, member_id: str, claim: PharmacyClaim) -> bool:
        """Add a pharmacy claim to an rx_member's session.

        Args:
            member_id: Member ID to add claim to
            claim: Pharmacy claim to add

        Returns:
            True if claim was added, False if member not found
        """
        session = self.get_by_member_id(member_id)
        if session:
            session.pharmacy_claims.append(claim)
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
            self._sessions = [
                s for s in self._sessions if s.rx_member.member_id in member_ids
            ]
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
        del member_ids  # Unused - loads all rx_members
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
            w["rx_member_count"] = w.get("entity_count", 0)

        return workspaces

    def delete_cohort(self, cohort_id: str) -> dict[str, Any] | None:
        """Delete a saved cohort (legacy alias for delete_workspace)."""
        result = self.delete_workspace(cohort_id)
        if result:
            result["cohort_id"] = result["workspace_id"]
            result["rx_member_count"] = result.get("entity_count", 0)
        return result

    def get_workspace_summary(self) -> dict[str, Any]:
        """Get summary of current workspace state."""
        total_prescriptions = sum(len(s.prescriptions) for s in self._sessions)
        total_claims = sum(len(s.pharmacy_claims) for s in self._sessions)
        total_dur_alerts = sum(len(s.dur_alerts) for s in self._sessions)
        total_prior_auths = sum(len(s.prior_auths) for s in self._sessions)

        # Provenance breakdown
        prov_counts = {"loaded": 0, "generated": 0, "derived": 0}
        for session in self._sessions:
            prov_counts[session.provenance.source_type.value] += 1

        return {
            "rx_member_count": len(self._sessions),
            "prescription_count": total_prescriptions,
            "pharmacy_claims_count": total_claims,
            "dur_alerts_count": total_dur_alerts,
            "prior_auth_count": total_prior_auths,
            "provenance_summary": prov_counts,
        }


# Global session manager for MCP server
session_manager = RxMemberSessionManager()
