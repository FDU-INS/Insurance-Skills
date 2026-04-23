"""
Underwriting Validation: Comprehensive validation utilities for underwriting operations.

This module provides validation capabilities for:
- Application data validation
- Policy validation
- Claim validation
- Risk assessment validation
- Compliance validation
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Validation result structure."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    validated_data: Dict[str, Any]

class UnderwritingValidator:
    """Comprehensive validator for underwriting operations."""

    def __init__(self):
        """Initialize the validator."""
        self.logger = logging.getLogger("geo_infer_risk.underwriting.validator")

        # Validation rules
        self.application_rules = self._load_application_rules()
        self.policy_rules = self._load_policy_rules()
        self.claim_rules = self._load_claim_rules()

    def validate_application(self, application_data: Dict[str, Any]) -> ValidationResult:
        """Validate underwriting application data."""
        errors = []
        warnings = []
        validated_data = application_data.copy()

        try:
            # Validate required fields
            required_fields = ['property', 'applicant', 'coverage_requests']
            for field in required_fields:
                if field not in application_data:
                    errors.append(f"Required field missing: {field}")

            # Validate property information
            if 'property' in application_data:
                property_validation = self._validate_property_data(application_data['property'])
                errors.extend(property_validation['errors'])
                warnings.extend(property_validation['warnings'])

            # Validate applicant information
            if 'applicant' in application_data:
                applicant_validation = self._validate_applicant_data(application_data['applicant'])
                errors.extend(applicant_validation['errors'])
                warnings.extend(applicant_validation['warnings'])

            # Validate coverage requests
            if 'coverage_requests' in application_data:
                coverage_validation = self._validate_coverage_requests(application_data['coverage_requests'])
                errors.extend(coverage_validation['errors'])
                warnings.extend(coverage_validation['warnings'])

            # Business logic validation
            business_validation = self._validate_business_logic(application_data)
            errors.extend(business_validation['errors'])
            warnings.extend(business_validation['warnings'])

        except Exception as e:
            errors.append(f"Validation error: {str(e)}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_data=validated_data
        )

    def validate_policy(self, policy_data: Dict[str, Any]) -> ValidationResult:
        """Validate policy data."""
        errors = []
        warnings = []
        validated_data = policy_data.copy()

        try:
            # Validate required fields
            required_fields = ['policy_id', 'policyholder_id', 'effective_date', 'coverages']
            for field in required_fields:
                if field not in policy_data:
                    errors.append(f"Required field missing: {field}")

            # Validate dates
            if 'effective_date' in policy_data:
                date_validation = self._validate_date(policy_data['effective_date'], 'effective_date')
                errors.extend(date_validation['errors'])
                warnings.extend(date_validation['warnings'])

            if 'expiration_date' in policy_data:
                date_validation = self._validate_date(policy_data['expiration_date'], 'expiration_date')
                errors.extend(date_validation['errors'])
                warnings.extend(date_validation['warnings'])

            # Validate coverages
            if 'coverages' in policy_data:
                for i, coverage in enumerate(policy_data['coverages']):
                    coverage_validation = self._validate_coverage(coverage, i)
                    errors.extend(coverage_validation['errors'])
                    warnings.extend(coverage_validation['warnings'])

            # Validate premium
            if 'total_premium' in policy_data:
                premium_validation = self._validate_premium(policy_data['total_premium'])
                errors.extend(premium_validation['errors'])
                warnings.extend(premium_validation['warnings'])

        except Exception as e:
            errors.append(f"Policy validation error: {str(e)}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_data=validated_data
        )

    def validate_claim(self, claim_data: Dict[str, Any]) -> ValidationResult:
        """Validate claim data."""
        errors = []
        warnings = []
        validated_data = claim_data.copy()

        try:
            # Validate required fields
            required_fields = ['policy_id', 'date_of_loss', 'claimed_amount', 'description']
            for field in required_fields:
                if field not in claim_data:
                    errors.append(f"Required field missing: {field}")

            # Validate amounts
            if 'claimed_amount' in claim_data:
                amount_validation = self._validate_amount(claim_data['claimed_amount'], 'claimed_amount')
                errors.extend(amount_validation['errors'])
                warnings.extend(amount_validation['warnings'])

            # Validate dates
            if 'date_of_loss' in claim_data:
                date_validation = self._validate_date(claim_data['date_of_loss'], 'date_of_loss')
                errors.extend(date_validation['errors'])
                warnings.extend(date_validation['warnings'])

            if 'reported_date' in claim_data:
                date_validation = self._validate_date(claim_data['reported_date'], 'reported_date')
                errors.extend(date_validation['errors'])
                warnings.extend(date_validation['warnings'])

            # Validate description
            if 'description' in claim_data:
                desc_validation = self._validate_description(claim_data['description'])
                errors.extend(desc_validation['errors'])
                warnings.extend(desc_validation['warnings'])

        except Exception as e:
            errors.append(f"Claim validation error: {str(e)}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_data=validated_data
        )

    def _validate_property_data(self, property_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate property information."""
        errors = []
        warnings = []

        # Validate coordinates
        if 'latitude' in property_data:
            lat = property_data['latitude']
            if not -90 <= lat <= 90:
                errors.append("Latitude must be between -90 and 90")

        if 'longitude' in property_data:
            lon = property_data['longitude']
            if not -180 <= lon <= 180:
                errors.append("Longitude must be between -180 and 180")

        # Validate value
        if 'value' in property_data:
            value = property_data['value']
            if value <= 0:
                errors.append("Property value must be positive")
            elif value > 50000000:  # 50M limit
                warnings.append("Very high property value - may require special approval")

        # Validate year built
        if 'year_built' in property_data:
            year = property_data['year_built']
            current_year = datetime.now().year
            if not 1800 <= year <= current_year:
                errors.append(f"Invalid year built: {year}")

        return {'errors': errors, 'warnings': warnings}

    def _validate_applicant_data(self, applicant_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate applicant information."""
        errors = []
        warnings = []

        # Validate required applicant fields
        required_fields = ['name', 'contact_info']
        for field in required_fields:
            if field not in applicant_data:
                errors.append(f"Required applicant field missing: {field}")

        # Validate contact information
        if 'contact_info' in applicant_data:
            contact = applicant_data['contact_info']
            if 'email' in contact:
                email = contact['email']
                if '@' not in email or '.' not in email:
                    errors.append("Invalid email format")

        return {'errors': errors, 'warnings': warnings}

    def _validate_coverage_requests(self, coverage_requests: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Validate coverage requests."""
        errors = []
        warnings = []

        if not coverage_requests:
            errors.append("At least one coverage request is required")
            return {'errors': errors, 'warnings': warnings}

        for i, coverage in enumerate(coverage_requests):
            coverage_validation = self._validate_single_coverage_request(coverage, i)
            errors.extend(coverage_validation['errors'])
            warnings.extend(coverage_validation['warnings'])

        return {'errors': errors, 'warnings': warnings}

    def _validate_single_coverage_request(self, coverage: Dict[str, Any], index: int) -> Dict[str, List[str]]:
        """Validate single coverage request."""
        errors = []
        warnings = []

        required_fields = ['coverage_type', 'limit']
        for field in required_fields:
            if field not in coverage:
                errors.append(f"Coverage request {index}: required field missing: {field}")

        # Validate limit
        if 'limit' in coverage:
            limit = coverage['limit']
            if limit <= 0:
                errors.append(f"Coverage request {index}: limit must be positive")
            elif limit > 10000000:  # 10M limit
                warnings.append(f"Coverage request {index}: high limit may require approval")

        # Validate deductible
        if 'deductible' in coverage:
            deductible = coverage['deductible']
            if deductible < 0:
                errors.append(f"Coverage request {index}: deductible cannot be negative")

        return {'errors': errors, 'warnings': warnings}

    def _validate_coverage(self, coverage: Dict[str, Any], index: int) -> Dict[str, List[str]]:
        """Validate coverage configuration."""
        errors = []
        warnings = []

        # Validate limit
        if 'limit' in coverage:
            limit = coverage['limit']
            if limit <= 0:
                errors.append(f"Coverage {index}: limit must be positive")

        # Validate deductible
        if 'deductible' in coverage:
            deductible = coverage['deductible']
            if deductible < 0:
                errors.append(f"Coverage {index}: deductible cannot be negative")
            elif deductible >= coverage.get('limit', float('inf')):
                errors.append(f"Coverage {index}: deductible cannot exceed limit")

        return {'errors': errors, 'warnings': warnings}

    def _validate_business_logic(self, application_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate business logic rules."""
        errors = []
        warnings = []

        property_data = application_data.get('property', {})
        coverage_requests = application_data.get('coverage_requests', [])

        # Check if coverage limits exceed property value
        total_coverage = sum(coverage.get('limit', 0) for coverage in coverage_requests)
        property_value = property_data.get('value', 0)

        if total_coverage > property_value * 1.5:  # Allow 50% over-insurance
            warnings.append("Total coverage exceeds property value significantly")

        # Check for reasonable deductibles
        for coverage in coverage_requests:
            deductible = coverage.get('deductible', 0)
            limit = coverage.get('limit', 0)
            if limit > 0 and deductible / limit > 0.1:  # Deductible > 10% of limit
                warnings.append("High deductible relative to coverage limit")

        return {'errors': errors, 'warnings': warnings}

    def _validate_date(self, date_str: str, field_name: str) -> Dict[str, List[str]]:
        """Validate date field."""
        errors = []
        warnings = []

        try:
            if isinstance(date_str, str):
                datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            elif isinstance(date_str, datetime):
                pass  # Already a datetime object
            else:
                errors.append(f"{field_name}: Invalid date format")

        except ValueError:
            errors.append(f"{field_name}: Invalid date format")

        return {'errors': errors, 'warnings': warnings}

    def _validate_amount(self, amount: float, field_name: str) -> Dict[str, List[str]]:
        """Validate amount field."""
        errors = []
        warnings = []

        if not isinstance(amount, (int, float)):
            errors.append(f"{field_name}: Must be a number")
        elif amount <= 0:
            errors.append(f"{field_name}: Must be positive")
        elif amount > 100000000:  # 100M limit
            warnings.append(f"{field_name}: Very large amount - may require approval")

        return {'errors': errors, 'warnings': warnings}

    def _validate_premium(self, premium: float) -> Dict[str, List[str]]:
        """Validate premium amount."""
        errors = []
        warnings = []

        if premium <= 0:
            errors.append("Premium must be positive")
        elif premium > 100000:  # 100K limit
            warnings.append("Very high premium - may require approval")

        return {'errors': errors, 'warnings': warnings}

    def _validate_description(self, description: str) -> Dict[str, List[str]]:
        """Validate description field."""
        errors = []
        warnings = []

        if not description or len(description.strip()) == 0:
            errors.append("Description is required")
        elif len(description) < 10:
            warnings.append("Description is very short - may need more detail")
        elif len(description) > 1000:
            warnings.append("Description is very long - consider shortening")

        return {'errors': errors, 'warnings': warnings}

    def _load_application_rules(self) -> Dict[str, Any]:
        """Load application validation rules."""
        return {
            'required_fields': ['property', 'applicant', 'coverage_requests'],
            'max_property_value': 50000000,
            'max_coverage_limit': 10000000,
            'min_description_length': 10
        }

    def _load_policy_rules(self) -> Dict[str, Any]:
        """Load policy validation rules."""
        return {
            'required_fields': ['policy_id', 'policyholder_id', 'effective_date', 'coverages'],
            'max_premium': 100000,
            'max_term_months': 120,
            'min_term_months': 1
        }

    def _load_claim_rules(self) -> Dict[str, Any]:
        """Load claim validation rules."""
        return {
            'required_fields': ['policy_id', 'date_of_loss', 'claimed_amount', 'description'],
            'max_claimed_amount': 10000000,
            'max_description_length': 1000
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on validator."""
        return {
            'status': 'operational',
            'rules_loaded': {
                'application_rules': len(self.application_rules),
                'policy_rules': len(self.policy_rules),
                'claim_rules': len(self.claim_rules)
            },
            'timestamp': datetime.now().isoformat()
        }


class PolicyValidator:
    """Specialized validator for policy operations."""

    def __init__(self):
        """Initialize the policy validator."""
        self.logger = logging.getLogger("geo_infer_risk.underwriting.policy_validator")

    def validate_policy_renewal(self, current_policy: Dict[str, Any],
                               renewal_data: Dict[str, Any]) -> ValidationResult:
        """Validate policy renewal."""
        errors = []
        warnings = []
        validated_data = renewal_data.copy()

        try:
            # Validate renewal timing
            current_expiration = datetime.fromisoformat(current_policy['expiration_date'].replace('Z', '+00:00'))
            renewal_effective = datetime.fromisoformat(renewal_data['effective_date'].replace('Z', '+00:00'))

            if renewal_effective <= current_expiration:
                errors.append("Renewal effective date must be after current expiration")

            # Validate renewal terms
            if 'term_months' in renewal_data:
                term = renewal_data['term_months']
                if not 1 <= term <= 120:
                    errors.append("Renewal term must be between 1 and 120 months")

        except Exception as e:
            errors.append(f"Renewal validation error: {str(e)}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_data=validated_data
        )

    def validate_policy_endorsement(self, policy: Dict[str, Any],
                                   endorsement: Dict[str, Any]) -> ValidationResult:
        """Validate policy endorsement."""
        errors = []
        warnings = []
        validated_data = endorsement.copy()

        try:
            # Validate endorsement date
            if 'effective_date' in endorsement:
                effective_date = datetime.fromisoformat(endorsement['effective_date'].replace('Z', '+00:00'))
                policy_effective = datetime.fromisoformat(policy['effective_date'].replace('Z', '+00:00'))

                if effective_date < policy_effective:
                    errors.append("Endorsement effective date cannot be before policy effective date")

            # Validate premium change
            if 'premium_change' in endorsement:
                premium_change = endorsement['premium_change']
                if abs(premium_change) > policy.get('total_premium', 0) * 0.5:  # 50% change limit
                    warnings.append("Large premium change - may require approval")

        except Exception as e:
            errors.append(f"Endorsement validation error: {str(e)}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_data=validated_data
        )


# Convenience functions
def validate_underwriting_application(application_data: Dict[str, Any]) -> ValidationResult:
    """Validate underwriting application data."""
    validator = UnderwritingValidator()
    return validator.validate_application(application_data)

def validate_policy_data(policy_data: Dict[str, Any]) -> ValidationResult:
    """Validate policy data."""
    validator = UnderwritingValidator()
    return validator.validate_policy(policy_data)

def validate_claim_data(claim_data: Dict[str, Any]) -> ValidationResult:
    """Validate claim data."""
    validator = UnderwritingValidator()
    return validator.validate_claim(claim_data)
