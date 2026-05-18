"""
Session state management for MCP server.

Maintains generated patients within a session, allowing Claude to reference
them by ID or position across multiple tool calls. Supports workspace
save/load for session persistence.
"""

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

from patientsim.core.models import (
    ClinicalNote,
    Diagnosis,
    Encounter,
    LabResult,
    Medication,
    Patient,
    Procedure,
    VitalSign,
)


class PatientSession(Session[Patient]):
    """Container for a single patient and associated clinical data with provenance."""

    def __init__(
        self,
        patient: Patient,
        encounters: list[Encounter] | None = None,
        diagnoses: list[Diagnosis] | None = None,
        medications: list[Medication] | None = None,
        labs: list[LabResult] | None = None,
        vitals: list[VitalSign] | None = None,
        procedures: list[Procedure] | None = None,
        notes: list[ClinicalNote] | None = None,
        provenance: Provenance | None = None,
    ):
        self._id = str(uuid4())[:8]  # Short ID for easy reference
        self._patient = patient
        self.encounters = encounters or []
        self.diagnoses = diagnoses or []
        self.medications = medications or []
        self.labs = labs or []
        self.vitals = vitals or []
        self.procedures = procedures or []
        self.notes = notes or []
        self.metadata: dict[str, Any] = {}

        # Provenance for the patient entity
        self._provenance = provenance or Provenance.generated()

        # Per-entity provenance (entity_id -> Provenance)
        self._entity_provenance: dict[str, Provenance] = {}

    # === Session interface implementation ===

    @property
    def id(self) -> str:
        """Unique session identifier."""
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """Set session ID (used during load)."""
        self._id = value

    @property
    def primary_entity(self) -> Patient:
        """The primary entity (patient)."""
        return self._patient

    @property
    def patient(self) -> Patient:
        """Convenience alias for primary_entity."""
        return self._patient

    @patient.setter
    def patient(self, value: Patient) -> None:
        """Set patient."""
        self._patient = value

    @property
    def provenance(self) -> Provenance:
        """Session provenance."""
        return self._provenance

    @provenance.setter
    def provenance(self, value: Provenance) -> None:
        """Set provenance."""
        self._provenance = value

    # Legacy compatibility: single encounter property
    @property
    def encounter(self) -> Encounter | None:
        """Get first encounter (legacy compatibility)."""
        return self.encounters[0] if self.encounters else None

    @encounter.setter
    def encounter(self, value: Encounter | None) -> None:
        """Set first encounter (legacy compatibility)."""
        if value:
            if self.encounters:
                self.encounters[0] = value
            else:
                self.encounters.append(value)
        elif self.encounters:
            self.encounters.pop(0)

    def add_encounter(self, encounter: Encounter, provenance: Provenance | None = None) -> None:
        """Add an encounter with provenance tracking."""
        self.encounters.append(encounter)
        if provenance:
            self._entity_provenance[encounter.encounter_id] = provenance

    def add_diagnosis(self, diagnosis: Diagnosis, provenance: Provenance | None = None) -> None:
        """Add a diagnosis with provenance tracking."""
        self.diagnoses.append(diagnosis)
        if provenance:
            entity_id = f"{diagnosis.patient_mrn}:{diagnosis.code}"
            self._entity_provenance[entity_id] = provenance

    def add_medication(self, medication: Medication, provenance: Provenance | None = None) -> None:
        """Add a medication with provenance tracking."""
        self.medications.append(medication)
        if provenance:
            entity_id = f"{medication.patient_mrn}:{medication.name}"
            self._entity_provenance[entity_id] = provenance

    def add_lab(self, lab: LabResult, provenance: Provenance | None = None) -> None:
        """Add a lab result with provenance tracking."""
        self.labs.append(lab)
        if provenance:
            entity_id = f"{lab.patient_mrn}:{lab.test_name}:{lab.collected_time.isoformat()}"
            self._entity_provenance[entity_id] = provenance

    def add_vital(self, vital: VitalSign, provenance: Provenance | None = None) -> None:
        """Add vital signs with provenance tracking."""
        self.vitals.append(vital)
        if provenance:
            entity_id = f"{vital.patient_mrn}:vitals:{vital.observation_time.isoformat()}"
            self._entity_provenance[entity_id] = provenance

    def add_procedure(self, procedure: Procedure, provenance: Provenance | None = None) -> None:
        """Add a procedure with provenance tracking."""
        self.procedures.append(procedure)
        if provenance:
            entity_id = f"{procedure.patient_mrn}:{procedure.code}"
            self._entity_provenance[entity_id] = provenance

    def add_note(self, note: ClinicalNote, provenance: Provenance | None = None) -> None:
        """Add a clinical note with provenance tracking."""
        self.notes.append(note)
        if provenance:
            entity_id = f"{note.patient_mrn}:{note.note_type}:{note.note_time.isoformat()}"
            self._entity_provenance[entity_id] = provenance

    def to_summary(self) -> dict[str, Any]:
        """Create human-readable summary of patient session."""
        summary = {
            "id": self._id,
            "mrn": self._patient.mrn,
            "name": self._patient.full_name,
            "age": self._patient.age,
            "gender": self._patient.gender,
        }

        if self.encounters:
            summary["encounters"] = [
                {
                    "id": e.encounter_id,
                    "class": e.class_code,
                    "admission_time": (e.admission_time.isoformat() if e.admission_time else None),
                }
                for e in self.encounters
            ]
            # Legacy: also include first encounter as "encounter"
            first = self.encounters[0]
            summary["encounter"] = {
                "class": first.class_code,
                "admission_time": (
                    first.admission_time.isoformat() if first.admission_time else None
                ),
                "discharge_time": (
                    first.discharge_time.isoformat() if first.discharge_time else None
                ),
            }

        if self.diagnoses:
            summary["diagnoses"] = [
                {"code": d.code, "description": d.description} for d in self.diagnoses
            ]

        if self.medications:
            summary["medications"] = [
                {"name": m.name, "dose": m.dose, "frequency": m.frequency} for m in self.medications
            ]

        if self.labs:
            summary["lab_count"] = len(self.labs)

        if self.vitals:
            summary["vital_count"] = len(self.vitals)
            # Include most recent vitals
            latest = self.vitals[-1]
            summary["vitals"] = {
                "heart_rate": latest.heart_rate,
                "systolic_bp": latest.systolic_bp,
                "diastolic_bp": latest.diastolic_bp,
                "temperature": latest.temperature,
                "respiratory_rate": latest.respiratory_rate,
                "spo2": latest.spo2,
            }

        if self.procedures:
            summary["procedure_count"] = len(self.procedures)

        if self.notes:
            summary["note_count"] = len(self.notes)

        # Provenance summary
        summary["provenance"] = {
            "source_type": self._provenance.source_type.value,
            "created_at": self._provenance.created_at.isoformat(),
        }
        if self._provenance.skill_used:
            summary["provenance"]["skill_used"] = self._provenance.skill_used

        return summary

    def to_entities_with_provenance(self) -> dict[str, list[EntityWithProvenance]]:
        """Convert session to entities with provenance for workspace serialization."""
        entities: dict[str, list[EntityWithProvenance]] = {
            "patients": [],
            "encounters": [],
            "diagnoses": [],
            "medications": [],
            "lab_results": [],
            "vital_signs": [],
            "procedures": [],
            "clinical_notes": [],
        }

        # Patient
        entities["patients"].append(
            EntityWithProvenance(
                entity_id=self._id,
                entity_type="patient",
                data=self._patient.model_dump(mode="json"),
                provenance=self._provenance,
            )
        )

        # Encounters
        for enc in self.encounters:
            prov = self._entity_provenance.get(enc.encounter_id, self._provenance)
            entities["encounters"].append(
                EntityWithProvenance(
                    entity_id=enc.encounter_id,
                    entity_type="encounter",
                    data=enc.model_dump(mode="json"),
                    provenance=prov,
                )
            )

        # Diagnoses
        for dx in self.diagnoses:
            entity_id = f"{dx.patient_mrn}:{dx.code}"
            prov = self._entity_provenance.get(entity_id, self._provenance)
            entities["diagnoses"].append(
                EntityWithProvenance(
                    entity_id=entity_id,
                    entity_type="diagnosis",
                    data=dx.model_dump(mode="json"),
                    provenance=prov,
                )
            )

        # Medications
        for med in self.medications:
            entity_id = f"{med.patient_mrn}:{med.name}"
            prov = self._entity_provenance.get(entity_id, self._provenance)
            entities["medications"].append(
                EntityWithProvenance(
                    entity_id=entity_id,
                    entity_type="medication",
                    data=med.model_dump(mode="json"),
                    provenance=prov,
                )
            )

        # Labs
        for lab in self.labs:
            entity_id = f"{lab.patient_mrn}:{lab.test_name}:{lab.collected_time.isoformat()}"
            prov = self._entity_provenance.get(entity_id, self._provenance)
            entities["lab_results"].append(
                EntityWithProvenance(
                    entity_id=entity_id,
                    entity_type="lab_result",
                    data=lab.model_dump(mode="json"),
                    provenance=prov,
                )
            )

        # Vitals
        for vital in self.vitals:
            entity_id = f"{vital.patient_mrn}:vitals:{vital.observation_time.isoformat()}"
            prov = self._entity_provenance.get(entity_id, self._provenance)
            entities["vital_signs"].append(
                EntityWithProvenance(
                    entity_id=entity_id,
                    entity_type="vital_sign",
                    data=vital.model_dump(mode="json"),
                    provenance=prov,
                )
            )

        # Procedures
        for proc in self.procedures:
            entity_id = f"{proc.patient_mrn}:{proc.code}"
            prov = self._entity_provenance.get(entity_id, self._provenance)
            entities["procedures"].append(
                EntityWithProvenance(
                    entity_id=entity_id,
                    entity_type="procedure",
                    data=proc.model_dump(mode="json"),
                    provenance=prov,
                )
            )

        # Notes
        for note in self.notes:
            entity_id = f"{note.patient_mrn}:{note.note_type}:{note.note_time.isoformat()}"
            prov = self._entity_provenance.get(entity_id, self._provenance)
            entities["clinical_notes"].append(
                EntityWithProvenance(
                    entity_id=entity_id,
                    entity_type="clinical_note",
                    data=note.model_dump(mode="json"),
                    provenance=prov,
                )
            )

        return entities

    @classmethod
    def from_entities_with_provenance(
        cls,
        patient_entity: EntityWithProvenance,
        all_entities: dict[str, list[EntityWithProvenance]],
    ) -> "PatientSession":
        """Reconstruct session from serialized entities."""
        patient = Patient.model_validate(patient_entity.data)
        session = cls(patient=patient, provenance=patient_entity.provenance)
        session.id = patient_entity.entity_id

        mrn = patient.mrn

        # Reconstruct encounters
        for ent in all_entities.get("encounters", []):
            if ent.data.get("patient_mrn") == mrn:
                enc = Encounter.model_validate(ent.data)
                session.encounters.append(enc)
                session._entity_provenance[enc.encounter_id] = ent.provenance

        # Reconstruct diagnoses
        for ent in all_entities.get("diagnoses", []):
            if ent.data.get("patient_mrn") == mrn:
                dx = Diagnosis.model_validate(ent.data)
                session.diagnoses.append(dx)
                session._entity_provenance[ent.entity_id] = ent.provenance

        # Reconstruct medications
        for ent in all_entities.get("medications", []):
            if ent.data.get("patient_mrn") == mrn:
                med = Medication.model_validate(ent.data)
                session.medications.append(med)
                session._entity_provenance[ent.entity_id] = ent.provenance

        # Reconstruct labs
        for ent in all_entities.get("lab_results", []):
            if ent.data.get("patient_mrn") == mrn:
                lab = LabResult.model_validate(ent.data)
                session.labs.append(lab)
                session._entity_provenance[ent.entity_id] = ent.provenance

        # Reconstruct vitals
        for ent in all_entities.get("vital_signs", []):
            if ent.data.get("patient_mrn") == mrn:
                vital = VitalSign.model_validate(ent.data)
                session.vitals.append(vital)
                session._entity_provenance[ent.entity_id] = ent.provenance

        # Reconstruct procedures
        for ent in all_entities.get("procedures", []):
            if ent.data.get("patient_mrn") == mrn:
                proc = Procedure.model_validate(ent.data)
                session.procedures.append(proc)
                session._entity_provenance[ent.entity_id] = ent.provenance

        # Reconstruct notes
        for ent in all_entities.get("clinical_notes", []):
            if ent.data.get("patient_mrn") == mrn:
                note = ClinicalNote.model_validate(ent.data)
                session.notes.append(note)
                session._entity_provenance[ent.entity_id] = ent.provenance

        return session


class PatientSessionManager(BaseSessionManager[Patient]):
    """Manages patient sessions for the MCP server with workspace support.

    Extends the healthsim.state.SessionManager base class with PatientSim-specific
    entity reconstruction and legacy compatibility methods.
    """

    def __init__(self, workspace_dir: Path | None = None):
        self._sessions: list[PatientSession] = []
        self._workspace_dir = workspace_dir

    @property
    def product_name(self) -> str:
        """Product identifier for workspace filtering."""
        return "patientsim"

    def _get_workspace_dir(self) -> Path | None:
        """Get workspace directory for persistence operations."""
        return self._workspace_dir

    # === Abstract method implementations ===

    def count(self) -> int:
        """Get total number of patient sessions."""
        return len(self._sessions)

    def clear(self) -> None:
        """Clear all patient sessions."""
        self._sessions.clear()

    def get_all(self) -> list[Session[Patient]]:
        """Get all patient sessions."""
        return list(self._sessions)

    def get_by_id(self, session_id: str) -> Session[Patient] | None:
        """Get patient session by ID."""
        for session in self._sessions:
            if session.id == session_id:
                return session
        return None

    def add(
        self,
        entity: Patient,
        provenance: Provenance | None = None,
        **related: Any,
    ) -> Session[Patient]:
        """Add new session with patient.

        Args:
            entity: Patient to add
            provenance: Optional provenance for the patient
            **related: Related entities (encounters, diagnoses, etc.)

        Returns:
            Created PatientSession
        """
        session = PatientSession(
            patient=entity,
            encounters=related.get("encounters"),
            diagnoses=related.get("diagnoses"),
            medications=related.get("medications"),
            labs=related.get("labs"),
            vitals=related.get("vitals"),
            procedures=related.get("procedures"),
            notes=related.get("notes"),
            provenance=provenance,
        )
        self._sessions.append(session)
        return session

    def _load_entities_from_workspace(
        self,
        workspace: Workspace,
    ) -> tuple[Workspace, dict[str, Any]]:
        """Reconstruct patient sessions from workspace entities.

        Args:
            workspace: Workspace to load entities from

        Returns:
            Tuple of (workspace, load statistics dict)
        """
        stats = {
            "patients_loaded": 0,
            "patients_skipped": 0,
            "total_entities": workspace.get_entity_count(),
            "conflicts": [],
        }

        patient_entities = workspace.entities.get("patients", [])

        for patient_ent in patient_entities:
            mrn = patient_ent.data.get("mrn")

            # Check for MRN conflict
            if mrn:
                existing = self.get_by_mrn(mrn)
                if existing:
                    stats["conflicts"].append(
                        {
                            "mrn": mrn,
                            "workspace_patient": existing.id,
                            "cohort_patient": patient_ent.entity_id,
                            "resolution": "skipped",
                        }
                    )
                    stats["patients_skipped"] += 1
                    continue

            # Reconstruct session
            session = PatientSession.from_entities_with_provenance(patient_ent, workspace.entities)

            # Update provenance to mark as loaded
            session.provenance = Provenance.loaded(source_system="patientsim")

            self.add_session(session)
            stats["patients_loaded"] += 1

        return workspace, stats

    # === PatientSim-specific methods ===

    def add_patient(
        self,
        patient: Patient,
        encounter: Encounter | None = None,
        diagnoses: list[Diagnosis] | None = None,
        medications: list[Medication] | None = None,
        labs: list[LabResult] | None = None,
        vitals: VitalSign | None = None,
        procedures: list[Procedure] | None = None,
        notes: list[ClinicalNote] | None = None,
        provenance: Provenance | None = None,
    ) -> PatientSession:
        """Add a patient to the session (legacy method).

        This is the PatientSim-specific add method that handles
        single encounter/vitals for backwards compatibility.
        """
        session = PatientSession(
            patient=patient,
            encounters=[encounter] if encounter else None,
            diagnoses=diagnoses,
            medications=medications,
            labs=labs,
            vitals=[vitals] if vitals else None,
            procedures=procedures,
            notes=notes,
            provenance=provenance,
        )
        self._sessions.append(session)
        return session

    def add_session(self, session: PatientSession) -> PatientSession:
        """Add an existing session to the manager."""
        self._sessions.append(session)
        return session

    def get_by_mrn(self, mrn: str) -> PatientSession | None:
        """Get patient session by MRN."""
        for session in self._sessions:
            if session.patient.mrn == mrn:
                return session
        return None

    def get_by_position(self, position: int) -> PatientSession | None:
        """Get patient session by position (1-indexed)."""
        if 1 <= position <= len(self._sessions):
            return self._sessions[position - 1]
        return None

    def get_latest(self) -> PatientSession | None:
        """Get the most recently added patient session."""
        if self._sessions:
            return self._sessions[-1]
        return None

    def list_all(self) -> list[PatientSession]:
        """Get all patient sessions (legacy method, use get_all())."""
        return self._sessions.copy()

    def update_patient(
        self,
        patient_id: str,
        modifications: dict[str, Any],
    ) -> PatientSession | None:
        """Update a patient with modifications.

        Args:
            patient_id: Patient session ID
            modifications: Dict of fields to modify

        Returns:
            Updated session or None if not found
        """
        session = self.get_by_id(patient_id)
        if not session or not isinstance(session, PatientSession):
            return None

        # Update patient fields using Pydantic's model_copy
        session.patient = session.patient.model_copy(update=modifications)
        return session

    # === Legacy cohort methods (delegate to workspace methods) ===

    def save_cohort(
        self,
        name: str,
        description: str | None = None,
        tags: list[str] | None = None,
        patient_ids: list[str] | None = None,
    ) -> Workspace:
        """Save current workspace as a cohort (legacy alias for save_workspace).

        Args:
            name: Human-readable name for the cohort
            description: Optional description
            tags: Optional tags for organization
            patient_ids: Specific patient IDs to save (None = all)

        Returns:
            Saved Workspace object
        """
        # Filter sessions if patient_ids specified
        if patient_ids:
            original_sessions = self._sessions
            self._sessions = [s for s in self._sessions if s.id in patient_ids]
            result = self.save_workspace(name, description, tags)
            self._sessions = original_sessions
            return result
        return self.save_workspace(name, description, tags)

    def load_cohort(
        self,
        cohort_id: str | None = None,
        name: str | None = None,
        mode: str = "replace",
        patient_ids: list[str] | None = None,  # noqa: ARG002
    ) -> tuple[Workspace, dict[str, Any]]:
        """Load a cohort into the workspace (legacy alias for load_workspace).

        Args:
            cohort_id: UUID of cohort to load
            name: Name to search for (if cohort_id not provided)
            mode: "replace" (clear first) or "merge" (add to existing)
            patient_ids: Specific patient IDs to load (ignored, loads all)

        Returns:
            Tuple of (Workspace, load_summary)
        """
        del patient_ids  # Unused - loads all patients
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
            w["patient_count"] = w.get("entity_count", 0)

        return workspaces

    def delete_cohort(self, cohort_id: str) -> dict[str, Any] | None:
        """Delete a saved cohort (legacy alias for delete_workspace)."""
        result = self.delete_workspace(cohort_id)
        if result:
            result["cohort_id"] = result["workspace_id"]
            result["patient_count"] = result.get("entity_count", 0)
        return result

    def get_workspace_summary(self) -> dict[str, Any]:
        """Get summary of current workspace state."""
        total_encounters = sum(len(s.encounters) for s in self._sessions)
        total_diagnoses = sum(len(s.diagnoses) for s in self._sessions)
        total_medications = sum(len(s.medications) for s in self._sessions)
        total_labs = sum(len(s.labs) for s in self._sessions)
        total_vitals = sum(len(s.vitals) for s in self._sessions)
        total_procedures = sum(len(s.procedures) for s in self._sessions)
        total_notes = sum(len(s.notes) for s in self._sessions)

        # Provenance breakdown
        prov_counts = {"loaded": 0, "generated": 0, "derived": 0}
        for session in self._sessions:
            prov_counts[session.provenance.source_type.value] += 1

        return {
            "patient_count": len(self._sessions),
            "encounter_count": total_encounters,
            "diagnosis_count": total_diagnoses,
            "medication_count": total_medications,
            "lab_count": total_labs,
            "vital_count": total_vitals,
            "procedure_count": total_procedures,
            "note_count": total_notes,
            "provenance_summary": prov_counts,
        }


# Backwards-compatible alias
SessionManager = PatientSessionManager
