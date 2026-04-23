"""FHIR R4 transformer.

Converts PatientSim objects to FHIR R4 resources.
"""

import uuid
from datetime import datetime

from patientsim.core.models import (
    Diagnosis,
    Encounter,
    LabResult,
    Patient,
    VitalSign,
)
from patientsim.formats.fhir.resources import (
    Bundle,
    BundleEntry,
    CodeableConcept,
    CodeSystems,
    ConditionResource,
    EncounterResource,
    HumanName,
    Identifier,
    ObservationResource,
    PatientResource,
    Period,
    Quantity,
    Reference,
    create_codeable_concept,
    get_loinc_code,
    get_vital_loinc,
)


class FHIRTransformer:
    """Transforms PatientSim objects to FHIR R4 resources.

    Example:
        >>> transformer = FHIRTransformer()
        >>> patient_resource = transformer.transform_patient(patient)
        >>> bundle = transformer.create_bundle([patient], [encounter], [diagnosis])
    """

    def __init__(self) -> None:
        """Initialize transformer."""
        self._resource_id_map: dict[str, str] = {}  # Map our IDs to FHIR resource IDs

    def _get_resource_id(self, resource_type: str, source_id: str) -> str:
        """Get or create a FHIR resource ID for a source ID.

        Args:
            resource_type: Type of FHIR resource
            source_id: Source identifier (MRN, encounter_id, etc.)

        Returns:
            FHIR resource ID
        """
        key = f"{resource_type}/{source_id}"
        if key not in self._resource_id_map:
            # Generate UUID-based ID
            self._resource_id_map[key] = str(uuid.uuid5(uuid.NAMESPACE_DNS, source_id))
        return self._resource_id_map[key]

    def transform_patient(self, patient: Patient) -> PatientResource:
        """Transform Patient to FHIR Patient resource.

        Args:
            patient: PatientSim Patient object

        Returns:
            FHIR Patient resource
        """
        resource_id = self._get_resource_id("Patient", patient.mrn)

        # Create name
        name = HumanName(
            use="official",
            family=patient.family_name,
            given=[patient.given_name],
            text=f"{patient.given_name} {patient.family_name}",
        )

        # Create identifier
        identifier = Identifier(
            system=CodeSystems.PATIENT_MRN,
            value=patient.mrn,
            use="usual",
        )

        # Map gender
        gender_map = {
            "M": "male",
            "F": "female",
            "O": "other",
            "U": "unknown",
        }
        gender = gender_map.get(patient.gender, "unknown")

        # Format birth date as YYYY-MM-DD
        birth_date = patient.birth_date.isoformat()

        # Handle deceased status
        deceased_bool = patient.deceased if patient.deceased else None
        deceased_dt = None
        if patient.deceased and patient.death_date:
            deceased_dt = patient.death_date.isoformat()

        return PatientResource(
            id=resource_id,
            identifier=[identifier],
            name=[name],
            gender=gender,
            birthDate=birth_date,
            deceasedBoolean=deceased_bool if not deceased_dt else None,
            deceasedDateTime=deceased_dt,
        )

    def transform_encounter(self, encounter: Encounter) -> EncounterResource:
        """Transform Encounter to FHIR Encounter resource.

        Args:
            encounter: PatientSim Encounter object

        Returns:
            FHIR Encounter resource
        """
        resource_id = self._get_resource_id("Encounter", encounter.encounter_id)
        patient_id = self._get_resource_id("Patient", encounter.patient_mrn)

        # Create identifier
        identifier = Identifier(
            system=CodeSystems.ENCOUNTER_ID,
            value=encounter.encounter_id,
        )

        # Map status
        status_map = {
            "planned": "planned",
            "in-progress": "in-progress",
            "finished": "finished",
            "cancelled": "cancelled",
        }
        status = status_map.get(encounter.status, "finished")

        # Map encounter class
        class_map = {
            "I": ("IMP", "inpatient encounter"),
            "O": ("AMB", "ambulatory"),
            "E": ("EMER", "emergency"),
            "U": ("OBSENC", "observation encounter"),
        }
        class_code, class_display = class_map.get(encounter.class_code, ("AMB", "ambulatory"))

        encounter_class = create_codeable_concept(
            CodeSystems.ENCOUNTER_CLASS,
            class_code,
            class_display,
        )

        # Create subject reference
        subject = Reference(
            reference=f"Patient/{patient_id}",
            display=f"Patient {encounter.patient_mrn}",
        )

        # Create period
        period = None
        if encounter.admission_time:
            period = Period(
                start=encounter.admission_time.isoformat(),
                end=encounter.discharge_time.isoformat() if encounter.discharge_time else None,
            )

        # Reason for visit
        reason_codes = []
        if encounter.admitting_diagnosis:
            reason_codes.append(CodeableConcept(text=encounter.admitting_diagnosis))

        # Hospitalization info
        hospitalization = None
        if encounter.discharge_disposition:
            hospitalization = {"dischargeDisposition": {"text": encounter.discharge_disposition}}

        return EncounterResource(
            id=resource_id,
            identifier=[identifier],
            status=status,
            **{"class": encounter_class},
            subject=subject,
            period=period,
            reasonCode=reason_codes,
            hospitalization=hospitalization,
        )

    def transform_condition(self, diagnosis: Diagnosis) -> ConditionResource:
        """Transform Diagnosis to FHIR Condition resource.

        Args:
            diagnosis: PatientSim Diagnosis object

        Returns:
            FHIR Condition resource
        """
        # Create unique ID for this diagnosis
        diag_id = f"{diagnosis.patient_mrn}-{diagnosis.code}"
        resource_id = self._get_resource_id("Condition", diag_id)
        patient_id = self._get_resource_id("Patient", diagnosis.patient_mrn)

        # Clinical status
        clinical_status = create_codeable_concept(
            CodeSystems.CONDITION_CLINICAL,
            "active",
            "Active",
        )

        # Verification status
        verification_status = create_codeable_concept(
            CodeSystems.CONDITION_VERIFICATION,
            "confirmed",
            "Confirmed",
        )

        # Category
        category = [
            create_codeable_concept(
                "http://terminology.hl7.org/CodeSystem/condition-category",
                "encounter-diagnosis",
                "Encounter Diagnosis",
            )
        ]

        # Code (ICD-10)
        code = create_codeable_concept(
            CodeSystems.ICD10,
            diagnosis.code,
            diagnosis.description,
        )

        # Subject reference
        subject = Reference(
            reference=f"Patient/{patient_id}",
        )

        # Encounter reference
        encounter = None
        if diagnosis.encounter_id:
            encounter_id = self._get_resource_id("Encounter", diagnosis.encounter_id)
            encounter = Reference(
                reference=f"Encounter/{encounter_id}",
            )

        # Onset and recorded date
        onset_dt = None
        recorded_date = None
        if diagnosis.diagnosed_date:
            onset_dt = diagnosis.diagnosed_date.isoformat()
            recorded_date = diagnosis.diagnosed_date.isoformat()

        return ConditionResource(
            id=resource_id,
            clinicalStatus=clinical_status,
            verificationStatus=verification_status,
            category=category,
            code=code,
            subject=subject,
            encounter=encounter,
            onsetDateTime=onset_dt,
            recordedDate=recorded_date,
        )

    def transform_lab_observation(self, lab: LabResult) -> ObservationResource | None:
        """Transform LabResult to FHIR Observation resource.

        Args:
            lab: PatientSim LabResult object

        Returns:
            FHIR Observation resource or None if LOINC code not found
        """
        # Get LOINC code
        loinc_info = get_loinc_code(lab.test_name)
        if not loinc_info:
            # Skip labs without LOINC mapping
            return None

        loinc_code, loinc_display = loinc_info

        # Create unique ID
        obs_id = f"{lab.patient_mrn}-lab-{loinc_code}-{lab.collected_time.isoformat()}"
        resource_id = self._get_resource_id("Observation", obs_id)
        patient_id = self._get_resource_id("Patient", lab.patient_mrn)

        # Category - laboratory
        category = [
            create_codeable_concept(
                CodeSystems.OBSERVATION_CATEGORY,
                "laboratory",
                "Laboratory",
            )
        ]

        # Code - LOINC
        code = create_codeable_concept(
            CodeSystems.LOINC,
            loinc_code,
            loinc_display,
        )

        # Subject reference
        subject = Reference(
            reference=f"Patient/{patient_id}",
        )

        # Encounter reference
        encounter = None
        if lab.encounter_id:
            encounter_id = self._get_resource_id("Encounter", lab.encounter_id)
            encounter = Reference(
                reference=f"Encounter/{encounter_id}",
            )

        # Effective datetime
        effective_dt = lab.collected_time.isoformat()

        # Issued datetime
        issued = None
        if lab.resulted_time:
            issued = lab.resulted_time.isoformat()

        # Value - try to parse as numeric, fall back to string
        value_quantity = None
        value_string = None
        try:
            numeric_value = float(lab.value)
            value_quantity = Quantity(
                value=numeric_value,
                unit=lab.unit,
                system=CodeSystems.UCUM,
                code=lab.unit,
            )
        except (ValueError, TypeError):
            value_string = lab.value

        return ObservationResource(
            id=resource_id,
            status="final",
            category=category,
            code=code,
            subject=subject,
            encounter=encounter,
            effectiveDateTime=effective_dt,
            issued=issued,
            valueQuantity=value_quantity,
            valueString=value_string,
        )

    def transform_vital_observations(self, vital: VitalSign) -> list[ObservationResource]:
        """Transform VitalSign to FHIR Observation resources.

        Creates one Observation per vital sign measurement.

        Args:
            vital: PatientSim VitalSign object

        Returns:
            List of FHIR Observation resources
        """
        observations = []
        patient_id = self._get_resource_id("Patient", vital.patient_mrn)

        # Category - vital signs
        category = [
            create_codeable_concept(
                CodeSystems.OBSERVATION_CATEGORY,
                "vital-signs",
                "Vital Signs",
            )
        ]

        # Subject reference
        subject = Reference(
            reference=f"Patient/{patient_id}",
        )

        # Encounter reference
        encounter = None
        if vital.encounter_id:
            encounter_id = self._get_resource_id("Encounter", vital.encounter_id)
            encounter = Reference(
                reference=f"Encounter/{encounter_id}",
            )

        # Effective datetime
        effective_dt = vital.observation_time.isoformat()

        # Map each vital sign field
        vital_mappings = [
            ("temperature", vital.temperature, "F"),
            ("heart_rate", vital.heart_rate, "bpm"),
            ("respiratory_rate", vital.respiratory_rate, "/min"),
            ("systolic_bp", vital.systolic_bp, "mm[Hg]"),
            ("diastolic_bp", vital.diastolic_bp, "mm[Hg]"),
            ("spo2", vital.spo2, "%"),
            ("height", vital.height_cm, "cm"),
            ("weight", vital.weight_kg, "kg"),
        ]

        for vital_type, value, unit in vital_mappings:
            if value is None:
                continue

            # Get LOINC code
            loinc_info = get_vital_loinc(vital_type)
            if not loinc_info:
                continue

            loinc_code, loinc_display = loinc_info

            # Create unique ID
            obs_id = f"{vital.patient_mrn}-vital-{loinc_code}-{effective_dt}"
            resource_id = self._get_resource_id("Observation", obs_id)

            # Code
            code = create_codeable_concept(
                CodeSystems.LOINC,
                loinc_code,
                loinc_display,
            )

            # Value
            value_quantity = Quantity(
                value=float(value),
                unit=unit,
                system=CodeSystems.UCUM,
                code=unit,
            )

            obs = ObservationResource(
                id=resource_id,
                status="final",
                category=category,
                code=code,
                subject=subject,
                encounter=encounter,
                effectiveDateTime=effective_dt,
                valueQuantity=value_quantity,
            )
            observations.append(obs)

        return observations

    def create_bundle(
        self,
        patients: list[Patient] | None = None,
        encounters: list[Encounter] | None = None,
        diagnoses: list[Diagnosis] | None = None,
        labs: list[LabResult] | None = None,
        vitals: list[VitalSign] | None = None,
        bundle_type: str = "collection",
    ) -> Bundle:
        """Create a FHIR Bundle containing all resources.

        Args:
            patients: List of Patient objects
            encounters: List of Encounter objects
            diagnoses: List of Diagnosis objects
            labs: List of LabResult objects
            vitals: List of VitalSign objects
            bundle_type: Type of bundle (collection, transaction, etc.)

        Returns:
            FHIR Bundle
        """
        entries = []

        # Add patients
        if patients:
            for patient in patients:
                resource = self.transform_patient(patient)
                entry = BundleEntry(
                    fullUrl=f"urn:uuid:{resource.id}",
                    resource=resource.model_dump(by_alias=True, exclude_none=True),
                )
                entries.append(entry)

        # Add encounters
        if encounters:
            for encounter in encounters:
                resource = self.transform_encounter(encounter)
                entry = BundleEntry(
                    fullUrl=f"urn:uuid:{resource.id}",
                    resource=resource.model_dump(by_alias=True, exclude_none=True),
                )
                entries.append(entry)

        # Add conditions
        if diagnoses:
            for diagnosis in diagnoses:
                resource = self.transform_condition(diagnosis)
                entry = BundleEntry(
                    fullUrl=f"urn:uuid:{resource.id}",
                    resource=resource.model_dump(by_alias=True, exclude_none=True),
                )
                entries.append(entry)

        # Add lab observations
        if labs:
            for lab in labs:
                resource = self.transform_lab_observation(lab)
                if resource:  # Skip if no LOINC mapping
                    entry = BundleEntry(
                        fullUrl=f"urn:uuid:{resource.id}",
                        resource=resource.model_dump(by_alias=True, exclude_none=True),
                    )
                    entries.append(entry)

        # Add vital sign observations
        if vitals:
            for vital in vitals:
                vital_obs = self.transform_vital_observations(vital)
                for resource in vital_obs:
                    entry = BundleEntry(
                        fullUrl=f"urn:uuid:{resource.id}",
                        resource=resource.model_dump(by_alias=True, exclude_none=True),
                    )
                    entries.append(entry)

        # Create bundle
        bundle = Bundle(
            id=str(uuid.uuid4()),
            type=bundle_type,
            timestamp=datetime.now().isoformat(),
            entry=entries,
        )

        return bundle
