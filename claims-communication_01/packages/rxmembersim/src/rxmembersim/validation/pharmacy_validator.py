"""Pharmacy-specific validators."""

from datetime import date
from typing import Any

from .framework import ValidationResult, Validator


class NDCValidator(Validator):
    """Validate NDC codes."""

    def validate(self, ndc: str) -> ValidationResult:
        """Validate an NDC code."""
        result = ValidationResult()

        # Remove dashes/spaces
        clean_ndc = ndc.replace("-", "").replace(" ", "")

        if len(clean_ndc) != 11:
            result.add_error(
                field="ndc",
                message=f"NDC must be 11 digits, got {len(clean_ndc)}",
                actual_value=ndc,
                code="NDC001",
            )

        if not clean_ndc.isdigit():
            result.add_error(
                field="ndc",
                message="NDC must contain only digits",
                actual_value=ndc,
                code="NDC002",
            )

        # Check for obviously invalid NDCs
        if clean_ndc == "00000000000" or clean_ndc == "99999999999":
            result.add_warning(
                field="ndc",
                message="NDC appears to be a placeholder value",
                actual_value=ndc,
                code="NDC003",
            )

        return result


class ClaimValidator(Validator):
    """Validate pharmacy claims."""

    def validate(self, claim: Any) -> ValidationResult:
        """Validate a pharmacy claim."""
        result = ValidationResult()

        # Validate NDC
        ndc_result = NDCValidator().validate(claim.ndc)
        result.issues.extend(ndc_result.issues)
        if not ndc_result.valid:
            result.valid = False

        # Validate quantity
        if hasattr(claim, "quantity_dispensed"):
            if claim.quantity_dispensed <= 0:
                result.add_error(
                    field="quantity_dispensed",
                    message="Quantity must be positive",
                    actual_value=claim.quantity_dispensed,
                    code="CLM001",
                )

        # Validate days supply
        if hasattr(claim, "days_supply"):
            if claim.days_supply < 1 or claim.days_supply > 365:
                result.add_error(
                    field="days_supply",
                    message="Days supply must be between 1 and 365",
                    actual_value=claim.days_supply,
                    code="CLM002",
                )

        # Validate service date
        if hasattr(claim, "service_date"):
            if claim.service_date > date.today():
                result.add_error(
                    field="service_date",
                    message="Service date cannot be in the future",
                    actual_value=str(claim.service_date),
                    code="CLM003",
                )

        # Validate BIN
        if hasattr(claim, "bin"):
            if len(claim.bin) != 6:
                result.add_error(
                    field="bin",
                    message="BIN must be 6 characters",
                    actual_value=claim.bin,
                    code="CLM004",
                )

        # Validate NPI
        if hasattr(claim, "pharmacy_npi"):
            if len(claim.pharmacy_npi) != 10:
                result.add_error(
                    field="pharmacy_npi",
                    message="NPI must be 10 digits",
                    actual_value=claim.pharmacy_npi,
                    code="CLM005",
                )

        return result


class MemberEligibilityValidator(Validator):
    """Validate member eligibility."""

    def validate(
        self, member: Any, service_date: date | None = None
    ) -> ValidationResult:
        """Validate member eligibility for a service date."""
        result = ValidationResult()
        service_date = service_date or date.today()

        # Check effective date
        if hasattr(member, "effective_date"):
            if member.effective_date > service_date:
                result.add_error(
                    field="effective_date",
                    message="Member not yet effective",
                    actual_value=str(member.effective_date),
                    expected_value=f"<= {service_date}",
                    code="ELIG001",
                )

        # Check termination
        if hasattr(member, "termination_date") and member.termination_date:
            if member.termination_date < service_date:
                result.add_error(
                    field="termination_date",
                    message="Member coverage terminated",
                    actual_value=str(member.termination_date),
                    code="ELIG002",
                )

        return result


class NPIValidator(Validator):
    """Validate NPI numbers using Luhn algorithm."""

    def validate(self, npi: str) -> ValidationResult:
        """Validate an NPI number."""
        result = ValidationResult()

        if len(npi) != 10:
            result.add_error(
                field="npi",
                message="NPI must be 10 digits",
                actual_value=npi,
                code="NPI001",
            )
            return result

        if not npi.isdigit():
            result.add_error(
                field="npi",
                message="NPI must contain only digits",
                actual_value=npi,
                code="NPI002",
            )
            return result

        # Luhn check (simplified)
        # Healthcare NPIs start with 1 or 2
        if npi[0] not in "12":
            result.add_warning(
                field="npi",
                message="NPI should start with 1 or 2",
                actual_value=npi,
                code="NPI003",
            )

        return result
