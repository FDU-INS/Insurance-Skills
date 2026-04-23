"""MemberSim Dimensional Transformer.

Transforms MemberSim canonical models into dimensional (star schema) format
for analytics and BI tools.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pandas as pd
from healthsim.dimensional import BaseDimensionalTransformer

if TYPE_CHECKING:
    from membersim.claims.claim import Claim
    from membersim.claims.payment import Payment
    from membersim.core.member import Member
    from membersim.core.plan import Plan
    from membersim.core.provider import Provider


# Place of Service code descriptions (X12 standard)
PLACE_OF_SERVICE_CODES = {
    "02": "Telehealth",
    "11": "Office",
    "12": "Home",
    "20": "Urgent Care Facility",
    "21": "Inpatient Hospital",
    "22": "Outpatient Hospital",
    "23": "Emergency Room - Hospital",
    "24": "Ambulatory Surgical Center",
    "31": "Skilled Nursing Facility",
    "32": "Nursing Facility",
    "33": "Custodial Care Facility",
    "34": "Hospice",
    "41": "Ambulance - Land",
    "42": "Ambulance - Air or Water",
    "50": "Federally Qualified Health Center",
    "51": "Inpatient Psychiatric Facility",
    "52": "Psychiatric Facility - Partial Hospitalization",
    "53": "Community Mental Health Center",
    "54": "Intermediate Care Facility",
    "61": "Comprehensive Inpatient Rehabilitation",
    "62": "Comprehensive Outpatient Rehabilitation",
    "65": "End-Stage Renal Disease Treatment",
    "71": "Public Health Clinic",
    "72": "Rural Health Clinic",
    "81": "Independent Laboratory",
    "99": "Other",
}


class MemberSimDimensionalTransformer(BaseDimensionalTransformer):
    """Transform MemberSim canonical models into dimensional format.

    Creates star schema with dimensions and fact tables optimized for
    payer/claims analytics.

    Dimensions:
        - dim_member: Member demographics with coverage info
        - dim_plan: Benefit plans with cost sharing details
        - dim_provider: Healthcare providers
        - dim_facility: Healthcare facilities
        - dim_diagnosis: ICD-10 diagnosis codes
        - dim_procedure: CPT/HCPCS procedure codes
        - dim_service_category: Place of service categories

    Facts:
        - fact_claims: Claim line-level detail (one row per claim line)
        - fact_eligibility_spans: Member coverage periods

    Example:
        >>> from membersim import MemberGenerator, Claim, Payment, Plan
        >>> from membersim.dimensional import MemberSimDimensionalTransformer
        >>>
        >>> gen = MemberGenerator(seed=42)
        >>> member = gen.generate_one()
        >>> # ... generate claims and payments ...
        >>>
        >>> transformer = MemberSimDimensionalTransformer(
        ...     members=[member],
        ...     plans=[plan],
        ...     claims=[claim],
        ...     payments=[payment],
        ... )
        >>> dimensions, facts = transformer.transform()
    """

    def __init__(
        self,
        members: list[Member] | None = None,
        plans: list[Plan] | None = None,
        providers: list[Provider] | None = None,
        claims: list[Claim] | None = None,
        payments: list[Payment] | None = None,
        snapshot_date: date | None = None,
    ) -> None:
        """Initialize the transformer with canonical model data.

        Args:
            members: List of Member objects.
            plans: List of Plan objects.
            providers: List of Provider objects.
            claims: List of Claim objects.
            payments: List of Payment objects.
            snapshot_date: Date for age calculations. Defaults to today.
        """
        self.members = members or []
        self.plans = plans or []
        self.providers = providers or []
        self.claims = claims or []
        self.payments = payments or []
        self.snapshot_date = snapshot_date or date.today()

        # Build payment lookup by claim_id for efficient joining
        self._payment_lookup: dict[str, Payment] = {p.claim_id: p for p in self.payments}

    def transform(self) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
        """Transform canonical models into dimensional format.

        Returns:
            Tuple of (dimensions dict, facts dict) where each dict maps
            table names to DataFrames.
        """
        dimensions = {}
        facts = {}

        # Build dimensions
        if self.members:
            dimensions["dim_member"] = self._build_dim_member()

        if self.plans:
            dimensions["dim_plan"] = self._build_dim_plan()

        # Build provider/facility dimensions from explicit providers + claims
        provider_dim, facility_dim = self._build_provider_and_facility_dims()
        if len(provider_dim) > 0:
            dimensions["dim_provider"] = provider_dim
        if len(facility_dim) > 0:
            dimensions["dim_facility"] = facility_dim

        # Build code dimensions from claims
        if self.claims:
            dimensions["dim_diagnosis"] = self._build_dim_diagnosis()
            dimensions["dim_procedure"] = self._build_dim_procedure()
            dimensions["dim_service_category"] = self._build_dim_service_category()

        # Build facts
        if self.claims:
            facts["fact_claims"] = self._build_fact_claims()

        if self.members:
            facts["fact_eligibility_spans"] = self._build_fact_eligibility_spans()

        return dimensions, facts

    # -------------------------------------------------------------------------
    # Dimension Builders
    # -------------------------------------------------------------------------

    def _build_dim_member(self) -> pd.DataFrame:
        """Build member dimension with demographics and coverage info."""
        records = []
        for member in self.members:
            age = self.calculate_age(member.birth_date, self.snapshot_date)
            gender_value = member.gender.value if hasattr(member.gender, "value") else member.gender

            records.append(
                {
                    "member_key": member.member_id,
                    "member_id": member.member_id,
                    "subscriber_id": member.subscriber_id,
                    "person_id": member.id,
                    "given_name": member.name.given_name,
                    "family_name": member.name.family_name,
                    "full_name": f"{member.name.given_name} {member.name.family_name}",
                    "birth_date_key": self.date_to_key(member.birth_date),
                    "birth_date": member.birth_date,
                    "gender_code": gender_value,
                    "gender_description": self._get_gender_description(gender_value),
                    "relationship_code": member.relationship_code,
                    "relationship_description": self._get_relationship_description(
                        member.relationship_code
                    ),
                    "group_id": member.group_id,
                    "plan_code": member.plan_code,
                    "pcp_npi": member.pcp_npi,
                    "age_at_snapshot": age,
                    "age_band": self.age_band(age),
                    "city": self.get_attr(member, "address.city"),
                    "state": self.get_attr(member, "address.state"),
                    "postal_code": self.get_attr(member, "address.zip_code"),
                    "is_subscriber": member.is_subscriber,
                    "is_active": member.is_active,
                }
            )
        return pd.DataFrame(records)

    def _build_dim_plan(self) -> pd.DataFrame:
        """Build plan dimension with benefit details."""
        records = []
        for idx, plan in enumerate(self.plans, start=1):
            records.append(
                {
                    "plan_key": idx,
                    "plan_code": plan.plan_code,
                    "plan_name": plan.plan_name,
                    "plan_type": plan.plan_type,
                    "coverage_type": plan.coverage_type,
                    "deductible_individual": float(plan.deductible_individual),
                    "deductible_family": float(plan.deductible_family),
                    "oop_max_individual": float(plan.oop_max_individual),
                    "oop_max_family": float(plan.oop_max_family),
                    "copay_pcp": float(plan.copay_pcp),
                    "copay_specialist": float(plan.copay_specialist),
                    "copay_er": float(plan.copay_er),
                    "coinsurance_pct": float(plan.coinsurance) * 100,  # Store as percentage
                    "requires_pcp": plan.requires_pcp,
                    "requires_referral": plan.requires_referral,
                }
            )

        if not records:
            return pd.DataFrame(columns=[
                "plan_key", "plan_code", "plan_name", "plan_type", "coverage_type",
                "deductible_individual", "deductible_family", "oop_max_individual",
                "oop_max_family", "copay_pcp", "copay_specialist", "copay_er",
                "coinsurance_pct", "requires_pcp", "requires_referral"
            ])

        return pd.DataFrame(records)

    def _build_provider_and_facility_dims(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Build provider and facility dimensions from providers and claims."""
        # Collect provider NPIs from explicit providers and claims
        provider_npis: dict[str, dict] = {}
        facility_npis: dict[str, dict] = {}

        # From explicit providers
        for provider in self.providers:
            if provider.provider_type == "FACILITY":
                facility_npis[provider.npi] = {
                    "npi": provider.npi,
                    "tax_id": provider.tax_id,
                    "name": provider.name,
                    "specialty": provider.specialty,
                    "provider_type": provider.provider_type,
                    "network_status": provider.network_status,
                    "city": self.get_attr(provider, "address.city"),
                    "state": self.get_attr(provider, "address.state"),
                }
            else:
                provider_npis[provider.npi] = {
                    "npi": provider.npi,
                    "tax_id": provider.tax_id,
                    "name": provider.name,
                    "specialty": provider.specialty,
                    "provider_type": provider.provider_type,
                    "network_status": provider.network_status,
                    "city": self.get_attr(provider, "address.city"),
                    "state": self.get_attr(provider, "address.state"),
                }

        # From claims (add NPIs we don't have details for)
        for claim in self.claims:
            if claim.provider_npi and claim.provider_npi not in provider_npis:
                provider_npis[claim.provider_npi] = {
                    "npi": claim.provider_npi,
                    "tax_id": None,
                    "name": claim.provider_npi,
                    "specialty": None,
                    "provider_type": "INDIVIDUAL",
                    "network_status": "UNKNOWN",
                    "city": None,
                    "state": None,
                }

            if claim.facility_npi and claim.facility_npi not in facility_npis:
                facility_npis[claim.facility_npi] = {
                    "npi": claim.facility_npi,
                    "tax_id": None,
                    "name": claim.facility_npi,
                    "specialty": None,
                    "provider_type": "FACILITY",
                    "network_status": "UNKNOWN",
                    "city": None,
                    "state": None,
                }

        # Build provider DataFrame
        provider_records = []
        for idx, (_npi, info) in enumerate(sorted(provider_npis.items()), start=1):
            provider_records.append(
                {
                    "provider_key": idx,
                    "provider_npi": info["npi"],
                    "tax_id": info["tax_id"],
                    "provider_name": info["name"],
                    "specialty": info["specialty"],
                    "provider_type": info["provider_type"],
                    "network_status": info["network_status"],
                    "city": info["city"],
                    "state": info["state"],
                }
            )

        # Build facility DataFrame
        facility_records = []
        for idx, (_npi, info) in enumerate(sorted(facility_npis.items()), start=1):
            facility_records.append(
                {
                    "facility_key": idx,
                    "facility_npi": info["npi"],
                    "tax_id": info["tax_id"],
                    "facility_name": info["name"],
                    "facility_type": info["specialty"],  # Taxonomy code
                    "network_status": info["network_status"],
                    "city": info["city"],
                    "state": info["state"],
                }
            )

        provider_df = pd.DataFrame(provider_records) if provider_records else pd.DataFrame(columns=[
            "provider_key", "provider_npi", "tax_id", "provider_name", "specialty",
            "provider_type", "network_status", "city", "state"
        ])

        facility_df = pd.DataFrame(facility_records) if facility_records else pd.DataFrame(columns=[
            "facility_key", "facility_npi", "tax_id", "facility_name", "facility_type",
            "network_status", "city", "state"
        ])

        return provider_df, facility_df

    def _build_dim_diagnosis(self) -> pd.DataFrame:
        """Build diagnosis dimension from claim diagnoses."""
        diagnosis_codes: set[str] = set()

        for claim in self.claims:
            diagnosis_codes.add(claim.principal_diagnosis)
            for dx in claim.other_diagnoses:
                diagnosis_codes.add(dx)

        records = []
        for idx, code in enumerate(sorted(diagnosis_codes), start=1):
            records.append(
                {
                    "diagnosis_key": idx,
                    "diagnosis_code": code,
                    "diagnosis_description": None,  # Would need lookup table
                    "diagnosis_category": self._get_icd10_category(code),
                    "code_system": "ICD-10-CM",
                }
            )

        if not records:
            return pd.DataFrame(columns=[
                "diagnosis_key", "diagnosis_code", "diagnosis_description",
                "diagnosis_category", "code_system"
            ])

        return pd.DataFrame(records)

    def _build_dim_procedure(self) -> pd.DataFrame:
        """Build procedure dimension from claim lines."""
        procedure_codes: set[str] = set()

        for claim in self.claims:
            for line in claim.claim_lines:
                procedure_codes.add(line.procedure_code)

        records = []
        for idx, code in enumerate(sorted(procedure_codes), start=1):
            records.append(
                {
                    "procedure_key": idx,
                    "procedure_code": code,
                    "procedure_description": None,  # Would need lookup table
                    "code_system": self._infer_procedure_code_system(code),
                }
            )

        if not records:
            return pd.DataFrame(columns=[
                "procedure_key", "procedure_code", "procedure_description", "code_system"
            ])

        return pd.DataFrame(records)

    def _build_dim_service_category(self) -> pd.DataFrame:
        """Build service category dimension from place of service codes."""
        pos_codes: set[str] = set()

        for claim in self.claims:
            pos_codes.add(claim.place_of_service)
            for line in claim.claim_lines:
                pos_codes.add(line.place_of_service)

        records = []
        for idx, code in enumerate(sorted(pos_codes), start=1):
            description = PLACE_OF_SERVICE_CODES.get(code, "Unknown")
            category = self._get_service_category(code)
            records.append(
                {
                    "service_category_key": idx,
                    "place_of_service_code": code,
                    "place_of_service_description": description,
                    "service_category": category,
                }
            )

        if not records:
            return pd.DataFrame(columns=[
                "service_category_key", "place_of_service_code",
                "place_of_service_description", "service_category"
            ])

        return pd.DataFrame(records)

    # -------------------------------------------------------------------------
    # Fact Builders
    # -------------------------------------------------------------------------

    def _build_fact_claims(self) -> pd.DataFrame:
        """Build claim line-level fact table (claim line explosion)."""
        # Build lookups
        provider_lookup = self._build_provider_lookup()
        facility_lookup = self._build_facility_lookup()
        diagnosis_lookup = self._build_diagnosis_lookup()
        procedure_lookup = self._build_procedure_lookup()
        service_category_lookup = self._build_service_category_lookup()

        records = []
        fact_key = 0

        for claim in self.claims:
            # Get payment if available
            payment = self._payment_lookup.get(claim.claim_id)

            # Build line payment lookup
            line_payment_lookup: dict[int, dict] = {}
            if payment:
                for lp in payment.line_payments:
                    line_payment_lookup[lp.line_number] = {
                        "charged_amount": float(lp.charged_amount),
                        "allowed_amount": float(lp.allowed_amount),
                        "paid_amount": float(lp.paid_amount),
                        "deductible_amount": float(lp.deductible_amount),
                        "copay_amount": float(lp.copay_amount),
                        "coinsurance_amount": float(lp.coinsurance_amount),
                        "member_responsibility": float(lp.patient_responsibility),
                        "adjustment_reason": lp.adjustment_reason,
                    }

            # One row per claim LINE (claim line explosion)
            for line in claim.claim_lines:
                fact_key += 1

                # Get line payment details if available
                line_pay = line_payment_lookup.get(line.line_number, {})

                # Get primary diagnosis key (first diagnosis pointer, usually 1)
                primary_dx_idx = line.diagnosis_pointers[0] - 1 if line.diagnosis_pointers else 0
                all_dx = claim.all_diagnoses
                primary_dx = (
                    all_dx[primary_dx_idx]
                    if primary_dx_idx < len(all_dx)
                    else claim.principal_diagnosis
                )

                records.append(
                    {
                        "claim_fact_key": fact_key,
                        "claim_id": claim.claim_id,
                        "claim_line_number": line.line_number,
                        "member_key": claim.member_id,
                        "subscriber_key": claim.subscriber_id,
                        "provider_key": provider_lookup.get(claim.provider_npi, -1),
                        "facility_key": (
                            facility_lookup.get(claim.facility_npi, -1)
                            if claim.facility_npi
                            else None
                        ),
                        "diagnosis_key": diagnosis_lookup.get(primary_dx, -1),
                        "procedure_key": procedure_lookup.get(line.procedure_code, -1),
                        "service_category_key": service_category_lookup.get(
                            line.place_of_service, -1
                        ),
                        "service_date_key": self.date_to_key(line.service_date),
                        "service_date": line.service_date,
                        "paid_date_key": (
                            self.date_to_key(payment.payment_date) if payment else None
                        ),
                        "paid_date": payment.payment_date if payment else None,
                        "claim_type": claim.claim_type,
                        "place_of_service_code": line.place_of_service,
                        "revenue_code": line.revenue_code,
                        "procedure_code": line.procedure_code,
                        "procedure_modifiers": (
                            ",".join(line.procedure_modifiers)
                            if line.procedure_modifiers
                            else None
                        ),
                        "ndc_code": line.ndc_code,
                        "units": float(line.units),
                        "line_charge_amount": float(line.charge_amount * line.units),
                        "charged_amount": line_pay.get("charged_amount"),
                        "allowed_amount": line_pay.get("allowed_amount"),
                        "paid_amount": line_pay.get("paid_amount"),
                        "deductible_amount": line_pay.get("deductible_amount"),
                        "copay_amount": line_pay.get("copay_amount"),
                        "coinsurance_amount": line_pay.get("coinsurance_amount"),
                        "member_responsibility": line_pay.get("member_responsibility"),
                        "adjustment_reason": line_pay.get("adjustment_reason"),
                        "principal_diagnosis_code": claim.principal_diagnosis,
                        "authorization_number": claim.authorization_number,
                    }
                )

        return pd.DataFrame(records) if records else pd.DataFrame(columns=[
            "claim_fact_key", "claim_id", "claim_line_number", "member_key",
            "subscriber_key", "provider_key", "facility_key", "diagnosis_key",
            "procedure_key", "service_category_key", "service_date_key", "service_date",
            "paid_date_key", "paid_date", "claim_type", "place_of_service_code",
            "revenue_code", "procedure_code", "procedure_modifiers", "ndc_code",
            "units", "line_charge_amount", "charged_amount", "allowed_amount",
            "paid_amount", "deductible_amount", "copay_amount", "coinsurance_amount",
            "member_responsibility", "adjustment_reason", "principal_diagnosis_code",
            "authorization_number"
        ])

    def _build_fact_eligibility_spans(self) -> pd.DataFrame:
        """Build eligibility spans fact table."""
        plan_lookup = self._build_plan_lookup()

        records = []
        for idx, member in enumerate(self.members, start=1):
            coverage_start = member.coverage_start
            coverage_end = member.coverage_end or self.snapshot_date

            # Calculate coverage days
            coverage_days = (coverage_end - coverage_start).days + 1

            records.append(
                {
                    "eligibility_span_key": idx,
                    "member_key": member.member_id,
                    "plan_key": plan_lookup.get(member.plan_code, -1),
                    "effective_date_key": self.date_to_key(coverage_start),
                    "effective_date": coverage_start,
                    "termination_date_key": (
                        self.date_to_key(coverage_end) if member.coverage_end else None
                    ),
                    "termination_date": member.coverage_end,
                    "coverage_days": coverage_days,
                    "is_active": member.is_active,
                    "group_id": member.group_id,
                    "relationship_code": member.relationship_code,
                }
            )

        return pd.DataFrame(records) if records else pd.DataFrame(columns=[
            "eligibility_span_key", "member_key", "plan_key", "effective_date_key",
            "effective_date", "termination_date_key", "termination_date",
            "coverage_days", "is_active", "group_id", "relationship_code"
        ])

    # -------------------------------------------------------------------------
    # Lookup Builders
    # -------------------------------------------------------------------------

    def _build_provider_lookup(self) -> dict[str, int]:
        """Build provider NPI to key lookup."""
        provider_npis: set[str] = set()
        for provider in self.providers:
            if provider.provider_type != "FACILITY":
                provider_npis.add(provider.npi)
        for claim in self.claims:
            if claim.provider_npi:
                provider_npis.add(claim.provider_npi)
        return {npi: idx for idx, npi in enumerate(sorted(provider_npis), start=1)}

    def _build_facility_lookup(self) -> dict[str, int]:
        """Build facility NPI to key lookup."""
        facility_npis: set[str] = set()
        for provider in self.providers:
            if provider.provider_type == "FACILITY":
                facility_npis.add(provider.npi)
        for claim in self.claims:
            if claim.facility_npi:
                facility_npis.add(claim.facility_npi)
        return {npi: idx for idx, npi in enumerate(sorted(facility_npis), start=1)}

    def _build_diagnosis_lookup(self) -> dict[str, int]:
        """Build diagnosis code to key lookup."""
        diagnosis_codes: set[str] = set()
        for claim in self.claims:
            diagnosis_codes.add(claim.principal_diagnosis)
            for dx in claim.other_diagnoses:
                diagnosis_codes.add(dx)
        return {code: idx for idx, code in enumerate(sorted(diagnosis_codes), start=1)}

    def _build_procedure_lookup(self) -> dict[str, int]:
        """Build procedure code to key lookup."""
        procedure_codes: set[str] = set()
        for claim in self.claims:
            for line in claim.claim_lines:
                procedure_codes.add(line.procedure_code)
        return {code: idx for idx, code in enumerate(sorted(procedure_codes), start=1)}

    def _build_service_category_lookup(self) -> dict[str, int]:
        """Build place of service code to key lookup."""
        pos_codes: set[str] = set()
        for claim in self.claims:
            pos_codes.add(claim.place_of_service)
            for line in claim.claim_lines:
                pos_codes.add(line.place_of_service)
        return {code: idx for idx, code in enumerate(sorted(pos_codes), start=1)}

    def _build_plan_lookup(self) -> dict[str, int]:
        """Build plan code to key lookup."""
        return {plan.plan_code: idx for idx, plan in enumerate(self.plans, start=1)}

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    def _get_gender_description(self, gender_code: str) -> str:
        """Get human-readable gender description."""
        descriptions = {
            "M": "Male",
            "F": "Female",
            "MALE": "Male",
            "FEMALE": "Female",
            "O": "Other",
            "U": "Unknown",
        }
        return descriptions.get(gender_code, "Unknown")

    def _get_relationship_description(self, relationship_code: str) -> str:
        """Get human-readable relationship description."""
        descriptions = {
            "18": "Self",
            "01": "Spouse",
            "19": "Child",
            "20": "Employee",
            "21": "Unknown",
            "39": "Organ Donor",
            "40": "Cadaver Donor",
            "53": "Life Partner",
            "G8": "Other Relationship",
        }
        return descriptions.get(relationship_code, "Other")

    def _get_icd10_category(self, code: str) -> str:
        """Get ICD-10 category from code.

        ICD-10 categories are based on the first letter:
        A-B: Infectious diseases
        C-D: Neoplasms
        E: Endocrine, nutritional, metabolic
        F: Mental/behavioral
        G: Nervous system
        H: Eye/ear
        I: Circulatory
        J: Respiratory
        K: Digestive
        L: Skin
        M: Musculoskeletal
        N: Genitourinary
        O: Pregnancy
        P: Perinatal
        Q: Congenital
        R: Symptoms
        S-T: Injury
        V-Y: External causes
        Z: Health status
        """
        if not code:
            return "Unknown"

        first_char = code[0].upper()
        categories = {
            "A": "Infectious",
            "B": "Infectious",
            "C": "Neoplasm",
            "D": "Neoplasm/Blood",
            "E": "Endocrine/Metabolic",
            "F": "Mental/Behavioral",
            "G": "Nervous System",
            "H": "Eye/Ear",
            "I": "Circulatory",
            "J": "Respiratory",
            "K": "Digestive",
            "L": "Skin",
            "M": "Musculoskeletal",
            "N": "Genitourinary",
            "O": "Pregnancy",
            "P": "Perinatal",
            "Q": "Congenital",
            "R": "Symptoms",
            "S": "Injury",
            "T": "Injury/Poisoning",
            "V": "External Causes",
            "W": "External Causes",
            "X": "External Causes",
            "Y": "External Causes",
            "Z": "Health Status",
        }
        return categories.get(first_char, "Other")

    def _infer_procedure_code_system(self, code: str) -> str:
        """Infer procedure code system from code format.

        - CPT: 5 digits
        - HCPCS: 1 letter + 4 digits
        - ICD-10-PCS: 7 alphanumeric characters
        """
        if not code:
            return "Unknown"

        code = code.strip()

        # CPT codes are 5 digits
        if code.isdigit() and len(code) == 5:
            return "CPT"

        # HCPCS codes start with letter and have 4 digits
        if len(code) == 5 and code[0].isalpha() and code[1:].isdigit():
            return "HCPCS"

        # ICD-10-PCS codes are 7 alphanumeric
        if len(code) == 7 and code.isalnum():
            return "ICD-10-PCS"

        return "Unknown"

    def _get_service_category(self, pos_code: str) -> str:
        """Categorize place of service into broader service categories."""
        inpatient_codes = {"21", "51", "61"}
        outpatient_codes = {"22", "24", "52", "62"}
        office_codes = {"11", "02"}
        er_codes = {"23"}
        snf_codes = {"31", "32", "33", "34", "54"}
        home_codes = {"12"}
        ambulance_codes = {"41", "42"}
        clinic_codes = {"50", "71", "72"}

        if pos_code in inpatient_codes:
            return "Inpatient"
        elif pos_code in outpatient_codes:
            return "Outpatient"
        elif pos_code in office_codes:
            return "Office"
        elif pos_code in er_codes:
            return "Emergency"
        elif pos_code in snf_codes:
            return "Skilled Nursing"
        elif pos_code in home_codes:
            return "Home Health"
        elif pos_code in ambulance_codes:
            return "Ambulance"
        elif pos_code in clinic_codes:
            return "Clinic"
        else:
            return "Other"
