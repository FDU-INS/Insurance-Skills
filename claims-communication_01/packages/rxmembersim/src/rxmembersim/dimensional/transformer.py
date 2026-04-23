"""RxMemberSim Dimensional Transformer.

Transforms RxMemberSim canonical models into dimensional (star schema) format
for pharmacy analytics and BI tools.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pandas as pd
from healthsim.dimensional import BaseDimensionalTransformer

if TYPE_CHECKING:
    from rxmembersim.authorization.prior_auth import PriorAuthRecord
    from rxmembersim.claims.claim import PharmacyClaim
    from rxmembersim.core.drug import DrugReference
    from rxmembersim.core.member import RxMember
    from rxmembersim.core.pharmacy import Pharmacy
    from rxmembersim.core.prescriber import Prescriber
    from rxmembersim.formulary.formulary import Formulary


# GPI-based therapeutic class descriptions (first 2 digits)
GPI_THERAPEUTIC_CLASSES = {
    "27": "Antidiabetic Agents",
    "36": "Cardiovascular Agents",
    "39": "Antihyperlipidemic Agents",
    "40": "Respiratory Agents",
    "44": "Gastrointestinal Agents",
    "49": "Gastrointestinal Agents",
    "56": "Psychotherapeutic Agents",
    "57": "Anxiolytics/Sedatives/Hypnotics",
    "58": "Antidepressants",
    "60": "Central Nervous System Agents",
    "61": "Anticonvulsants",
    "65": "ADHD/Anti-Narcolepsy/Anti-Obesity",
    "66": "Biologicals/Immunologicals",
    "70": "Anti-Infectives",
    "72": "Antivirals",
    "83": "Anticoagulants/Antithrombotics",
    "90": "Analgesics/Antipyretics",
    "91": "Analgesics - Opioid",
    "99": "Miscellaneous",
}


class RxMemberSimDimensionalTransformer(BaseDimensionalTransformer):
    """Transform RxMemberSim canonical models into dimensional format.

    Creates star schema with dimensions and fact tables optimized for
    pharmacy/PBM analytics.

    Dimensions:
        - dim_rx_member: Pharmacy member demographics and benefit info
        - dim_medication: Drug reference with NDC, GPI, AWP
        - dim_pharmacy: Pharmacy locations with network status
        - dim_prescriber: Prescriber details with specialty
        - dim_formulary: Formulary tier information

    Facts:
        - fact_prescription_fills: Pharmacy claim details
        - fact_prior_auth: Prior authorization requests and outcomes

    Example:
        >>> from rxmembersim import RxMemberFactory
        >>> from rxmembersim.dimensional import RxMemberSimDimensionalTransformer
        >>>
        >>> gen = RxMemberFactory()
        >>> member = gen.generate()
        >>> # ... generate claims ...
        >>>
        >>> transformer = RxMemberSimDimensionalTransformer(
        ...     members=[member],
        ...     claims=[claim],
        ... )
        >>> dimensions, facts = transformer.transform()
    """

    def __init__(
        self,
        members: list[RxMember] | None = None,
        drugs: list[DrugReference] | None = None,
        pharmacies: list[Pharmacy] | None = None,
        prescribers: list[Prescriber] | None = None,
        formularies: list[Formulary] | None = None,
        claims: list[PharmacyClaim] | None = None,
        prior_auths: list[PriorAuthRecord] | None = None,
        snapshot_date: date | None = None,
    ) -> None:
        """Initialize the transformer with canonical model data.

        Args:
            members: List of RxMember objects.
            drugs: List of DrugReference objects.
            pharmacies: List of Pharmacy objects.
            prescribers: List of Prescriber objects.
            formularies: List of Formulary objects.
            claims: List of PharmacyClaim objects.
            prior_auths: List of PriorAuthRecord objects.
            snapshot_date: Date for age calculations. Defaults to today.
        """
        self.members = members or []
        self.drugs = drugs or []
        self.pharmacies = pharmacies or []
        self.prescribers = prescribers or []
        self.formularies = formularies or []
        self.claims = claims or []
        self.prior_auths = prior_auths or []
        self.snapshot_date = snapshot_date or date.today()

        # Build drug lookup by NDC
        self._drug_lookup: dict[str, DrugReference] = {
            self._normalize_ndc(d.ndc): d for d in self.drugs
        }

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
            dimensions["dim_rx_member"] = self._build_dim_rx_member()

        # Build medication dimension from drugs + claims
        medication_dim = self._build_dim_medication()
        if len(medication_dim) > 0:
            dimensions["dim_medication"] = medication_dim

        # Build pharmacy dimension from pharmacies + claims
        pharmacy_dim = self._build_dim_pharmacy()
        if len(pharmacy_dim) > 0:
            dimensions["dim_pharmacy"] = pharmacy_dim

        # Build prescriber dimension from prescribers + claims
        prescriber_dim = self._build_dim_prescriber()
        if len(prescriber_dim) > 0:
            dimensions["dim_prescriber"] = prescriber_dim

        if self.formularies:
            dimensions["dim_formulary"] = self._build_dim_formulary()

        # Build facts
        if self.claims:
            facts["fact_prescription_fills"] = self._build_fact_prescription_fills()

        if self.prior_auths:
            facts["fact_prior_auth"] = self._build_fact_prior_auth()

        if self.members:
            facts["fact_rx_eligibility_spans"] = self._build_fact_rx_eligibility_spans()

        return dimensions, facts

    # -------------------------------------------------------------------------
    # Dimension Builders
    # -------------------------------------------------------------------------

    def _build_dim_rx_member(self) -> pd.DataFrame:
        """Build pharmacy member dimension."""
        records = []
        for member in self.members:
            demo = member.demographics
            age = self.calculate_age(demo.date_of_birth, self.snapshot_date)

            records.append(
                {
                    "member_key": member.member_id,
                    "member_id": member.member_id,
                    "cardholder_id": member.cardholder_id,
                    "person_code": member.person_code,
                    "bin": member.bin,
                    "pcn": member.pcn,
                    "group_number": member.group_number,
                    "given_name": demo.first_name,
                    "family_name": demo.last_name,
                    "full_name": f"{demo.first_name} {demo.last_name}",
                    "birth_date_key": self.date_to_key(demo.date_of_birth),
                    "birth_date": demo.date_of_birth,
                    "gender_code": demo.gender,
                    "gender_description": self._get_gender_description(demo.gender),
                    "age_at_snapshot": age,
                    "age_band": self.age_band(age),
                    "city": demo.city,
                    "state": demo.state,
                    "postal_code": demo.zip_code,
                    "plan_code": member.plan_code,
                    "formulary_id": member.formulary_id,
                    "effective_date_key": self.date_to_key(member.effective_date),
                    "effective_date": member.effective_date,
                    "termination_date_key": (
                        self.date_to_key(member.termination_date)
                        if member.termination_date else None
                    ),
                    "termination_date": member.termination_date,
                    "deductible_met": float(member.accumulators.deductible_met),
                    "deductible_remaining": float(member.accumulators.deductible_remaining),
                    "oop_met": float(member.accumulators.oop_met),
                    "oop_remaining": float(member.accumulators.oop_remaining),
                    "is_cardholder": member.person_code == "01",
                }
            )
        return pd.DataFrame(records)

    def _build_dim_medication(self) -> pd.DataFrame:
        """Build medication dimension from drugs and claims."""
        # Collect NDCs from drugs and claims
        ndcs: dict[str, dict] = {}

        # From explicit drug references
        for drug in self.drugs:
            ndc_11 = self._normalize_ndc(drug.ndc)
            ndcs[ndc_11] = {
                "ndc_11": ndc_11,
                "ndc_10": self._ndc_11_to_10(ndc_11),
                "drug_name": drug.drug_name,
                "generic_name": drug.generic_name,
                "gpi": drug.gpi,
                "therapeutic_class": drug.therapeutic_class,
                "strength": drug.strength,
                "dosage_form": drug.dosage_form,
                "route_of_admin": drug.route_of_admin,
                "dea_schedule": (
                    drug.dea_schedule.value
                    if hasattr(drug.dea_schedule, "value")
                    else drug.dea_schedule
                ),
                "is_brand": drug.is_brand,
                "multi_source_code": drug.multi_source_code,
                "awp": drug.awp,
                "wac": drug.wac,
            }

        # From claims (add NDCs we don't have details for)
        for claim in self.claims:
            ndc_11 = self._normalize_ndc(claim.ndc)
            if ndc_11 not in ndcs:
                ndcs[ndc_11] = {
                    "ndc_11": ndc_11,
                    "ndc_10": self._ndc_11_to_10(ndc_11),
                    "drug_name": None,
                    "generic_name": None,
                    "gpi": None,
                    "therapeutic_class": None,
                    "strength": None,
                    "dosage_form": None,
                    "route_of_admin": None,
                    "dea_schedule": None,
                    "is_brand": None,
                    "multi_source_code": None,
                    "awp": None,
                    "wac": None,
                }

        records = []
        for idx, (_ndc, info) in enumerate(sorted(ndcs.items()), start=1):
            gpi = info.get("gpi") or ""
            therapeutic_category = self._get_therapeutic_category(gpi)

            records.append(
                {
                    "medication_key": idx,
                    "ndc_11": info["ndc_11"],
                    "ndc_10": info["ndc_10"],
                    "drug_name": info["drug_name"],
                    "generic_name": info["generic_name"],
                    "gpi": info["gpi"],
                    "gpi_2": gpi[:2] if len(gpi) >= 2 else None,
                    "gpi_4": gpi[:4] if len(gpi) >= 4 else None,
                    "gpi_6": gpi[:6] if len(gpi) >= 6 else None,
                    "therapeutic_class": info["therapeutic_class"],
                    "therapeutic_category": therapeutic_category,
                    "strength": info["strength"],
                    "dosage_form": info["dosage_form"],
                    "route_of_admin": info["route_of_admin"],
                    "dea_schedule": info["dea_schedule"],
                    "is_controlled": info["dea_schedule"] not in (None, "0"),
                    "is_brand": info["is_brand"],
                    "multi_source_code": info["multi_source_code"],
                    "awp": info["awp"],
                    "wac": info["wac"],
                }
            )

        if not records:
            return pd.DataFrame(columns=[
                "medication_key", "ndc_11", "ndc_10", "drug_name", "generic_name",
                "gpi", "gpi_2", "gpi_4", "gpi_6", "therapeutic_class",
                "therapeutic_category", "strength", "dosage_form", "route_of_admin",
                "dea_schedule", "is_controlled", "is_brand", "multi_source_code",
                "awp", "wac"
            ])

        return pd.DataFrame(records)

    def _build_dim_pharmacy(self) -> pd.DataFrame:
        """Build pharmacy dimension from pharmacies and claims."""
        # Collect pharmacies from explicit list and claims
        pharmacy_npis: dict[str, dict] = {}

        # From explicit pharmacies
        for pharm in self.pharmacies:
            pharmacy_npis[pharm.npi] = {
                "npi": pharm.npi,
                "ncpdp_id": pharm.ncpdp_id,
                "name": pharm.name,
                "dba_name": pharm.dba_name,
                "pharmacy_type": (
                    pharm.pharmacy_type.value
                    if hasattr(pharm.pharmacy_type, "value")
                    else pharm.pharmacy_type
                ),
                "city": pharm.city,
                "state": pharm.state,
                "zip_code": pharm.zip_code,
                "in_network": pharm.in_network,
                "preferred": pharm.preferred,
                "specialty_certified": pharm.specialty_certified,
                "chain_code": pharm.chain_code,
                "chain_name": pharm.chain_name,
                "has_delivery": pharm.has_delivery,
                "has_24_hour": pharm.has_24_hour,
            }

        # From claims (add NPIs we don't have details for)
        for claim in self.claims:
            if claim.pharmacy_npi and claim.pharmacy_npi not in pharmacy_npis:
                pharmacy_npis[claim.pharmacy_npi] = {
                    "npi": claim.pharmacy_npi,
                    "ncpdp_id": claim.pharmacy_ncpdp,
                    "name": claim.pharmacy_npi,
                    "dba_name": None,
                    "pharmacy_type": "UNKNOWN",
                    "city": None,
                    "state": None,
                    "zip_code": None,
                    "in_network": None,
                    "preferred": None,
                    "specialty_certified": None,
                    "chain_code": None,
                    "chain_name": None,
                    "has_delivery": None,
                    "has_24_hour": None,
                }

        records = []
        for idx, (_npi, info) in enumerate(sorted(pharmacy_npis.items()), start=1):
            records.append(
                {
                    "pharmacy_key": idx,
                    "pharmacy_npi": info["npi"],
                    "ncpdp_id": info["ncpdp_id"],
                    "pharmacy_name": info["name"],
                    "dba_name": info["dba_name"],
                    "pharmacy_type": info["pharmacy_type"],
                    "pharmacy_category": self._get_pharmacy_category(info["pharmacy_type"]),
                    "city": info["city"],
                    "state": info["state"],
                    "postal_code": info["zip_code"],
                    "in_network": info["in_network"],
                    "preferred": info["preferred"],
                    "specialty_certified": info["specialty_certified"],
                    "chain_code": info["chain_code"],
                    "chain_name": info["chain_name"],
                    "has_delivery": info["has_delivery"],
                    "has_24_hour": info["has_24_hour"],
                }
            )

        if not records:
            return pd.DataFrame(columns=[
                "pharmacy_key", "pharmacy_npi", "ncpdp_id", "pharmacy_name",
                "dba_name", "pharmacy_type", "pharmacy_category", "city", "state",
                "postal_code", "in_network", "preferred", "specialty_certified",
                "chain_code", "chain_name", "has_delivery", "has_24_hour"
            ])

        return pd.DataFrame(records)

    def _build_dim_prescriber(self) -> pd.DataFrame:
        """Build prescriber dimension from prescribers and claims."""
        prescriber_npis: dict[str, dict] = {}

        # From explicit prescribers
        for pres in self.prescribers:
            credential_val = (
                pres.credential.value
                if hasattr(pres.credential, "value")
                else pres.credential
            )
            specialty_val = (
                pres.specialty.value
                if hasattr(pres.specialty, "value")
                else pres.specialty
            )

            prescriber_npis[pres.npi] = {
                "npi": pres.npi,
                "dea": pres.dea,
                "first_name": pres.first_name,
                "last_name": pres.last_name,
                "full_name": pres.full_name,
                "display_name": pres.display_name,
                "credential": credential_val,
                "specialty": specialty_val,
                "taxonomy_code": pres.taxonomy_code,
                "city": pres.city,
                "state": pres.state,
                "active": pres.active,
                "can_prescribe_controlled": pres.can_prescribe_controlled,
            }

        # From claims (add NPIs we don't have details for)
        for claim in self.claims:
            if claim.prescriber_npi and claim.prescriber_npi not in prescriber_npis:
                prescriber_npis[claim.prescriber_npi] = {
                    "npi": claim.prescriber_npi,
                    "dea": None,
                    "first_name": None,
                    "last_name": None,
                    "full_name": claim.prescriber_npi,
                    "display_name": claim.prescriber_npi,
                    "credential": None,
                    "specialty": None,
                    "taxonomy_code": None,
                    "city": None,
                    "state": None,
                    "active": None,
                    "can_prescribe_controlled": None,
                }

        records = []
        for idx, (_npi, info) in enumerate(sorted(prescriber_npis.items()), start=1):
            records.append(
                {
                    "prescriber_key": idx,
                    "prescriber_npi": info["npi"],
                    "dea_number": info["dea"],
                    "first_name": info["first_name"],
                    "last_name": info["last_name"],
                    "full_name": info["full_name"],
                    "display_name": info["display_name"],
                    "credential": info["credential"],
                    "specialty": info["specialty"],
                    "taxonomy_code": info["taxonomy_code"],
                    "city": info["city"],
                    "state": info["state"],
                    "is_active": info["active"],
                    "can_prescribe_controlled": info["can_prescribe_controlled"],
                }
            )

        if not records:
            return pd.DataFrame(columns=[
                "prescriber_key", "prescriber_npi", "dea_number", "first_name",
                "last_name", "full_name", "display_name", "credential",
                "specialty", "taxonomy_code", "city", "state", "is_active",
                "can_prescribe_controlled"
            ])

        return pd.DataFrame(records)

    def _build_dim_formulary(self) -> pd.DataFrame:
        """Build formulary dimension."""
        records = []
        for idx, formulary in enumerate(self.formularies, start=1):
            # Extract tier info
            tier_copays = {}
            tier_coinsurances = {}
            for tier in formulary.tiers:
                if tier.copay_amount:
                    tier_copays[f"tier_{tier.tier_number}_copay"] = float(tier.copay_amount)
                if tier.coinsurance_percent:
                    coinsurance_key = f"tier_{tier.tier_number}_coinsurance_pct"
                    tier_coinsurances[coinsurance_key] = float(tier.coinsurance_percent)

            record = {
                "formulary_key": idx,
                "formulary_id": formulary.formulary_id,
                "formulary_name": formulary.name,
                "effective_date": formulary.effective_date,
                "tier_count": len(formulary.tiers),
                "drug_count": len(formulary.drugs),
                "default_tier": formulary.default_tier,
                "default_copay": float(formulary.default_copay),
            }
            record.update(tier_copays)
            record.update(tier_coinsurances)
            records.append(record)

        if not records:
            return pd.DataFrame(columns=[
                "formulary_key", "formulary_id", "formulary_name", "effective_date",
                "tier_count", "drug_count", "default_tier", "default_copay"
            ])

        return pd.DataFrame(records)

    # -------------------------------------------------------------------------
    # Fact Builders
    # -------------------------------------------------------------------------

    def _build_fact_prescription_fills(self) -> pd.DataFrame:
        """Build prescription fills fact table."""
        pharmacy_lookup = self._build_pharmacy_lookup()
        prescriber_lookup = self._build_prescriber_lookup()
        medication_lookup = self._build_medication_lookup()

        records = []
        for idx, claim in enumerate(self.claims, start=1):
            ndc_11 = self._normalize_ndc(claim.ndc)
            drug_info = self._drug_lookup.get(ndc_11)

            # Transaction type
            tx_code = (
                claim.transaction_code.value
                if hasattr(claim.transaction_code, "value")
                else claim.transaction_code
            )

            records.append(
                {
                    "fill_fact_key": idx,
                    "claim_id": claim.claim_id,
                    "member_key": claim.member_id,
                    "cardholder_key": claim.cardholder_id,
                    "pharmacy_key": pharmacy_lookup.get(claim.pharmacy_npi, -1),
                    "prescriber_key": prescriber_lookup.get(claim.prescriber_npi, -1),
                    "medication_key": medication_lookup.get(ndc_11, -1),
                    "service_date_key": self.date_to_key(claim.service_date),
                    "service_date": claim.service_date,
                    "transaction_code": tx_code,
                    "is_new_fill": claim.fill_number == 0,
                    "is_refill": claim.fill_number > 0,
                    "fill_number": claim.fill_number,
                    "prescription_number": claim.prescription_number,
                    "ndc_11": ndc_11,
                    "quantity_dispensed": float(claim.quantity_dispensed),
                    "days_supply": claim.days_supply,
                    "daw_code": claim.daw_code,
                    "compound_code": claim.compound_code,
                    "is_compound": claim.compound_code != "0",
                    "ingredient_cost_submitted": float(claim.ingredient_cost_submitted),
                    "dispensing_fee_submitted": float(claim.dispensing_fee_submitted),
                    "usual_customary_charge": float(claim.usual_customary_charge),
                    "gross_amount_due": float(claim.gross_amount_due),
                    "prior_auth_number": claim.prior_auth_number,
                    "has_prior_auth": claim.prior_auth_number is not None,
                    "dur_reason_for_service": claim.dur_reason_for_service,
                    "dur_professional_service": claim.dur_professional_service,
                    "has_dur_intervention": claim.dur_reason_for_service is not None,
                    "bin": claim.bin,
                    "pcn": claim.pcn,
                    "group_number": claim.group_number,
                    # Drug attributes (if available)
                    "is_brand": drug_info.is_brand if drug_info else None,
                    "is_controlled": (
                        drug_info.dea_schedule.value not in (None, "0")
                        if drug_info and hasattr(drug_info.dea_schedule, "value")
                        else None
                    ),
                    "awp_unit_price": drug_info.awp if drug_info else None,
                }
            )

        return pd.DataFrame(records) if records else pd.DataFrame(columns=[
            "fill_fact_key", "claim_id", "member_key", "cardholder_key",
            "pharmacy_key", "prescriber_key", "medication_key",
            "service_date_key", "service_date", "transaction_code",
            "is_new_fill", "is_refill", "fill_number", "prescription_number",
            "ndc_11", "quantity_dispensed", "days_supply", "daw_code",
            "compound_code", "is_compound", "ingredient_cost_submitted",
            "dispensing_fee_submitted", "usual_customary_charge",
            "gross_amount_due", "prior_auth_number", "has_prior_auth",
            "dur_reason_for_service", "dur_professional_service",
            "has_dur_intervention", "bin", "pcn", "group_number",
            "is_brand", "is_controlled", "awp_unit_price"
        ])

    def _build_fact_prior_auth(self) -> pd.DataFrame:
        """Build prior authorization fact table."""
        medication_lookup = self._build_medication_lookup()

        records = []
        for idx, pa_record in enumerate(self.prior_auths, start=1):
            req = pa_record.request
            resp = pa_record.response
            ndc_11 = self._normalize_ndc(req.ndc)

            # Get status
            if resp:
                status = (
                    resp.status.value if hasattr(resp.status, "value") else resp.status
                )
                denial_reason = (
                    resp.denial_reason.value
                    if resp.denial_reason and hasattr(resp.denial_reason, "value")
                    else resp.denial_reason
                )
            else:
                status = "PENDING"
                denial_reason = None

            records.append(
                {
                    "prior_auth_fact_key": idx,
                    "pa_request_id": req.pa_request_id,
                    "pa_number": resp.pa_number if resp else None,
                    "member_key": req.member_id,
                    "cardholder_key": req.cardholder_id,
                    "medication_key": medication_lookup.get(ndc_11, -1),
                    "request_date_key": self.date_to_key(
                        req.request_date.date()
                        if hasattr(req.request_date, "date")
                        else req.request_date
                    ),
                    "request_date": req.request_date,
                    "response_date_key": (
                        self.date_to_key(
                            resp.response_date.date()
                            if hasattr(resp.response_date, "date")
                            else resp.response_date
                        )
                        if resp
                        else None
                    ),
                    "response_date": resp.response_date if resp else None,
                    "request_type": (
                        req.request_type.value
                        if hasattr(req.request_type, "value")
                        else req.request_type
                    ),
                    "urgency": req.urgency,
                    "status": status,
                    "is_approved": status == "approved",
                    "is_denied": status == "denied",
                    "is_pending": status == "pending",
                    "auto_approved": resp.auto_approved if resp else False,
                    "denial_reason": denial_reason,
                    "ndc_11": ndc_11,
                    "drug_name": req.drug_name,
                    "quantity_requested": float(req.quantity_requested),
                    "days_supply_requested": req.days_supply_requested,
                    "quantity_approved": (
                        float(resp.quantity_approved)
                        if resp and resp.quantity_approved
                        else None
                    ),
                    "days_supply_approved": (
                        resp.days_supply_approved if resp else None
                    ),
                    "effective_date_key": (
                        self.date_to_key(resp.effective_date)
                        if resp and resp.effective_date
                        else None
                    ),
                    "expiration_date_key": (
                        self.date_to_key(resp.expiration_date)
                        if resp and resp.expiration_date
                        else None
                    ),
                    "prescriber_npi": req.prescriber_npi,
                    "prescriber_name": req.prescriber_name,
                    "prescriber_specialty": req.prescriber_specialty,
                    "diagnosis_codes": (
                        ",".join(req.diagnosis_codes)
                        if req.diagnosis_codes
                        else None
                    ),
                    "has_clinical_notes": req.clinical_notes is not None,
                    "has_lab_results": len(req.lab_results) > 0 if req.lab_results else False,
                    "turnaround_hours": (
                        (resp.response_date - req.request_date).total_seconds() / 3600
                        if resp and resp.response_date else None
                    ),
                }
            )

        return pd.DataFrame(records) if records else pd.DataFrame(columns=[
            "prior_auth_fact_key", "pa_request_id", "pa_number", "member_key",
            "cardholder_key", "medication_key", "request_date_key", "request_date",
            "response_date_key", "response_date", "request_type", "urgency",
            "status", "is_approved", "is_denied", "is_pending", "auto_approved",
            "denial_reason", "ndc_11", "drug_name", "quantity_requested",
            "days_supply_requested", "quantity_approved", "days_supply_approved",
            "effective_date_key", "expiration_date_key", "prescriber_npi",
            "prescriber_name", "prescriber_specialty", "diagnosis_codes",
            "has_clinical_notes", "has_lab_results", "turnaround_hours"
        ])

    def _build_fact_rx_eligibility_spans(self) -> pd.DataFrame:
        """Build pharmacy eligibility spans fact table."""
        records = []
        for idx, member in enumerate(self.members, start=1):
            effective = member.effective_date
            termination = member.termination_date or self.snapshot_date
            coverage_days = (termination - effective).days + 1

            records.append(
                {
                    "rx_eligibility_span_key": idx,
                    "member_key": member.member_id,
                    "cardholder_key": member.cardholder_id,
                    "effective_date_key": self.date_to_key(effective),
                    "effective_date": effective,
                    "termination_date_key": (
                        self.date_to_key(termination) if member.termination_date else None
                    ),
                    "termination_date": member.termination_date,
                    "coverage_days": coverage_days,
                    "is_active": (
                        member.termination_date is None
                        or member.termination_date >= self.snapshot_date
                    ),
                    "bin": member.bin,
                    "pcn": member.pcn,
                    "group_number": member.group_number,
                    "plan_code": member.plan_code,
                    "formulary_id": member.formulary_id,
                }
            )

        return pd.DataFrame(records) if records else pd.DataFrame(columns=[
            "rx_eligibility_span_key", "member_key", "cardholder_key",
            "effective_date_key", "effective_date", "termination_date_key",
            "termination_date", "coverage_days", "is_active", "bin", "pcn",
            "group_number", "plan_code", "formulary_id"
        ])

    # -------------------------------------------------------------------------
    # Lookup Builders
    # -------------------------------------------------------------------------

    def _build_pharmacy_lookup(self) -> dict[str, int]:
        """Build pharmacy NPI to key lookup."""
        npis: set[str] = set()
        for pharm in self.pharmacies:
            npis.add(pharm.npi)
        for claim in self.claims:
            if claim.pharmacy_npi:
                npis.add(claim.pharmacy_npi)
        return {npi: idx for idx, npi in enumerate(sorted(npis), start=1)}

    def _build_prescriber_lookup(self) -> dict[str, int]:
        """Build prescriber NPI to key lookup."""
        npis: set[str] = set()
        for pres in self.prescribers:
            npis.add(pres.npi)
        for claim in self.claims:
            if claim.prescriber_npi:
                npis.add(claim.prescriber_npi)
        return {npi: idx for idx, npi in enumerate(sorted(npis), start=1)}

    def _build_medication_lookup(self) -> dict[str, int]:
        """Build NDC to key lookup."""
        ndcs: set[str] = set()
        for drug in self.drugs:
            ndcs.add(self._normalize_ndc(drug.ndc))
        for claim in self.claims:
            ndcs.add(self._normalize_ndc(claim.ndc))
        return {ndc: idx for idx, ndc in enumerate(sorted(ndcs), start=1)}

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    def _normalize_ndc(self, ndc: str) -> str:
        """Normalize NDC to 11-digit format.

        NDC codes can be in various formats:
        - 10-digit (common): 12345-6789-01 or 1234567890
        - 11-digit (standard): 12345678901

        This normalizes to 11-digit by padding segments appropriately.
        """
        if not ndc:
            return ndc

        # Remove any dashes or hyphens
        ndc_clean = ndc.replace("-", "").replace(" ", "")

        if len(ndc_clean) == 11:
            return ndc_clean

        if len(ndc_clean) == 10:
            # 10-digit to 11-digit: NDC has 3 segments (labeler-product-package)
            # 4-4-2 -> 5-4-2 (add leading zero to labeler)
            # 5-3-2 -> 5-4-2 (add leading zero to product)
            # 5-4-1 -> 5-4-2 (add leading zero to package)
            # Default: assume 5-4-2 with leading zero on package
            return ndc_clean[:5] + ndc_clean[5:9] + "0" + ndc_clean[9:]

        return ndc_clean

    def _ndc_11_to_10(self, ndc_11: str) -> str:
        """Convert 11-digit NDC to 10-digit format.

        Removes the leading zero from whichever segment has it.
        """
        if not ndc_11 or len(ndc_11) != 11:
            return ndc_11

        # Standard 5-4-2 format - remove leading zero from package
        return ndc_11[:9] + ndc_11[10:]

    def _get_gender_description(self, gender_code: str) -> str:
        """Get human-readable gender description."""
        descriptions = {
            "M": "Male",
            "F": "Female",
            "U": "Unknown",
        }
        return descriptions.get(gender_code, "Unknown")

    def _get_therapeutic_category(self, gpi: str) -> str:
        """Get therapeutic category from GPI prefix."""
        if not gpi or len(gpi) < 2:
            return "Unknown"

        gpi_2 = gpi[:2]
        return GPI_THERAPEUTIC_CLASSES.get(gpi_2, "Other")

    def _get_pharmacy_category(self, pharmacy_type: str) -> str:
        """Categorize pharmacy type into broader categories."""
        if not pharmacy_type:
            return "Unknown"

        pharmacy_type_lower = pharmacy_type.lower()

        if pharmacy_type_lower in ("retail",):
            return "Retail"
        elif pharmacy_type_lower in ("mail", "mail_order"):
            return "Mail Order"
        elif pharmacy_type_lower in ("specialty",):
            return "Specialty"
        elif pharmacy_type_lower in ("ltc", "long_term_care"):
            return "Long Term Care"
        elif pharmacy_type_lower in ("hospital",):
            return "Hospital"
        elif pharmacy_type_lower in ("clinic",):
            return "Clinic"
        else:
            return "Other"
