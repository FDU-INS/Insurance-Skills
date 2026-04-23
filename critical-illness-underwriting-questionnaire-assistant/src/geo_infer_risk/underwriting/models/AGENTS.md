# Agent
: models

## Scope
 This directory contains models components for the module. It provides 25 classes and 0 functions.

## Classes
 and Functions

### ClaimStatus
 Insurance claim status enumeration.

### ClaimType
 Insurance claim type enumeration.

### PaymentType
 Insurance payment type enumeration.

### Reserve
 Insurance claim reserve estimate.

**Methods**:
- `update_amount(new_amount: float, reason: str) -> None`: Update reserve amount.
- `is_adequate(paid_amount: float) -> bool`: Check if reserve is adequate for paid amount.
- `get_reserve_summary() -> Dict[str, Any]`: Get summary of reserve details.

### Payment
 Insurance claim payment record.

**Methods**:
- `is_valid() -> bool`: Validate payment record.
- `get_payment_summary() -> Dict[str, Any]`: Get summary of payment details.

### Claim
 Insurance claim data structure.

**Methods**:
- `add_reserve(reserve: Reserve) -> None`: Add reserve estimate to claim.
- `add_payment(payment: Payment) -> None`: Add payment to claim.
- `calculate_total_reserves() -> float`: Calculate total reserve amount.
- `calculate_outstanding_reserves() -> float`: Calculate outstanding reserve amount.
- `is_closed() -> bool`: Check if claim is closed.
- `days_open() -> int`: Calculate days since claim was reported.
- `get_financial_summary() -> Dict[str, Any]`: Get financial summary of the claim.
- `get_claim_summary() -> Dict[str, Any]`: Get claim summary.
- `to_dict() -> Dict[str, Any]`: Convert claim to dictionary for serialization.
- `validate_claim() -> Dict[str, Any]`: Validate claim data and return validation results.

### PolicyStatus
 Insurance policy status enumeration.

### CoverageType
 Insurance coverage type enumeration.

### Coverage
 Insurance coverage configuration.

**Methods**:
- `calculate_premium_portion(total_premium: float) -> float`: Calculate the portion of total premium for this coverage.
- `is_active(effective_date: datetime) -> bool`: Check if coverage is active on given date.
- `get_coverage_summary() -> Dict[str, Any]`: Get summary of coverage details.

### Endorsement
 Policy endorsement or amendment.

**Methods**:
- `is_effective() -> bool`: Check if endorsement is currently effective.
- `get_endorsement_summary() -> Dict[str, Any]`: Get summary of endorsement details.

### Exclusion
 Policy exclusion or limitation.

**Methods**:
- `applies_to_peril(peril: str) -> bool`: Check if exclusion applies to specific peril.
- `get_exclusion_summary() -> Dict[str, Any]`: Get summary of exclusion details.

### Policy
 Insurance policy data structure.

**Methods**:
- `add_coverage(coverage: Coverage) -> None`: Add coverage to the policy.
- `remove_coverage(coverage_type: CoverageType) -> bool`: Remove coverage from the policy.
- `add_endorsement(endorsement: Endorsement) -> None`: Add endorsement to the policy.
- `add_exclusion(exclusion: Exclusion) -> None`: Add exclusion to the policy.
- `is_active() -> bool`: Check if policy is currently active.
- `days_to_expiration() -> int`: Calculate days until policy expiration.
- `get_coverage_for_peril(peril: str) -> List[Coverage]`: Get coverages that apply to a specific peril.
- `calculate_policy_value() -> float`: Calculate total policy value (sum of all coverage limits).
- `get_policy_summary() -> Dict[str, Any]`: Get policy summary.
- `to_dict() -> Dict[str, Any]`: Convert policy to dictionary for serialization.

### RiskLevel
 Risk level enumeration.

### RiskCategory
 Risk category enumeration.

### RiskProfile
 risk profile for underwriting assessment.

**Methods**:
- `calculate_weighted_risk_score(weights: Optional[Dict[str, float]]) -> float`: Calculate weighted risk score.
- `update_risk_level() -> None`: Update risk level based on overall risk score.
- `to_dict() -> Dict[str, Any]`: Convert risk profile to dictionary.

### ExposureProfile
 Exposure profile for risk assessment.

**Methods**:
- `calculate_value_at_risk(confidence_level: float) -> float`: Calculate value at risk for the exposure.
- `get_seasonal_adjustment(season: str) -> float`: Get seasonal adjustment factor.
- `to_dict() -> Dict[str, Any]`: Convert exposure profile to dictionary.

### VulnerabilityProfile
 Vulnerability profile for risk assessment.

**Methods**:
- `get_damage_ratio(hazard_type: str) -> float`: Get damage ratio for specific hazard.
- `calculate_expected_loss(hazard_intensity: float) -> float`: Calculate expected loss for given hazard intensity.
- `to_dict() -> Dict[str, Any]`: Convert vulnerability profile to dictionary.

### DecisionStatus
 Underwriting decision status enumeration.

### GuidelineType
 Underwriting guideline type enumeration.

### Decision
 Underwriting decision structure.

**Methods**:
- `is_final() -> bool`: Check if decision is final.
- `requires_review() -> bool`: Check if decision requires manual review.
- `to_dict() -> Dict[str, Any]`: Convert decision to dictionary.

### Guideline
 Underwriting guideline structure.

**Methods**:
- `is_applicable(product: str, region: str, risk_tier: str) -> bool`: Check if guideline is applicable.
- `is_effective() -> bool`: Check if guideline is currently effective.
- `to_dict() -> Dict[str, Any]`: Convert guideline to dictionary.

### UnderwritingCase
 Underwriting case structure.

**Methods**:
- `is_completed() -> bool`: Check if case is completed.
- `days_open() -> int`: Calculate days since case was created.
- `requires_attention() -> bool`: Check if case requires attention.
- `to_dict() -> Dict[str, Any]`: Convert underwriting case to dictionary.

### AuditTrail
 Audit trail for underwriting operations.

**Methods**:
- `to_dict() -> Dict[str, Any]`: Convert audit trail to dictionary.

### ComplianceCheck
 Compliance check result.

**Methods**:
- `is_compliant() -> bool`: Check if compliance check passed.
- `to_dict() -> Dict[str, Any]`: Convert compliance check to dictionary.

### UnderwritingQueue
 Underwriting queue management.

**Methods**:
- `add_to_queue(case_id: str, priority: str) -> bool`: Add case to queue.
- `remove_from_queue(case_id: str) -> bool`: Remove case from queue.
- `to_dict() -> Dict[str, Any]`: Convert queue to dictionary.

## Capabilities

- **25 classes** for core functionality

## Integration

- **Location**: `src/geo_infer_risk/underwriting/models`
- **Type**: Directory Node
