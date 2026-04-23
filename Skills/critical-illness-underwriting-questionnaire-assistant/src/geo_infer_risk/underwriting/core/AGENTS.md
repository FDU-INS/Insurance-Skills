# Agent
: core

## Scope
 This directory contains core components for the module. It provides 38 classes and 16 functions.

## Classes
 and Functions

### ClaimStatus
 Insurance claim status enumeration.

### ClaimType
 Insurance claim type enumeration.

### Reserve
 Insurance claim reserve estimate.

### Payment
 Insurance claim payment record.

### Claim
 Insurance claim data structure.

**Methods**:
- `add_reserve(reserve: Reserve) -> None`: Add reserve estimate to claim.
- `add_payment(payment: Payment) -> None`: Add payment to claim.
- `calculate_total_reserves() -> float`: Calculate total reserve amount.
- `calculate_outstanding_reserves() -> float`: Calculate outstanding reserve amount.
- `is_closed() -> bool`: Check if claim is closed.
- `days_open() -> int`: Calculate days since claim was reported.
- `to_dict() -> Dict[str, Any]`: Convert claim to dictionary for serialization.

### ClaimsProcessingConfig
 Configuration for claims processing operations.

### ClaimsProcessor
 claims processing system.

**Methods**:
- `process_claim(claim_data: Dict[str, Any]) -> Claim`: Process a insurance claim.
- `settle_claim(claim_id: str, settlement_amount: float, settlement_notes: str) -> bool`: Settle an approved claim.
- `deny_claim(claim_id: str, denial_reason: str) -> bool`: Deny a claim.
- `reopen_claim(claim_id: str, reopen_reason: str) -> bool`: Reopen a closed claim.
- `get_claim(claim_id: str) -> Optional[Claim]`: Retrieve claim by ID.
- `search_claims(criteria: Dict[str, Any]) -> List[Claim]`: Search claims based on criteria.
- `get_claims_summary() -> Dict[str, Any]`: Get summary of all claims and processing metrics.
- `export_claims_data(format: str, filename: Optional[str]) -> str`: Export claims data to file.
- `health_check() -> Dict[str, Any]`: Perform health check on claims processing system.

### ClaimsEngine
 claims processing engine with AI and automation capabilities.

**Methods**:
- `predict_claim_outcome(claim_data: Dict[str, Any]) -> Dict[str, Any]`: Predict claim outcome using machine learning.
- `assess_fraud_risk(claim_data: Dict[str, Any]) -> Dict[str, Any]`: Assess fraud risk using detection methods.
- `optimize_settlement(claim: Claim, constraints: Dict[str, Any]) -> Dict[str, Any]`: Optimize settlement amount based on claim characteristics and constraints.

### PolicyStatus
 Insurance policy status enumeration.

### CoverageType
 Insurance coverage type enumeration.

### Coverage
 Insurance coverage configuration.

### Endorsement
 Policy endorsement or amendment.

### Policy
 Insurance policy data structure.

**Methods**:
- `add_coverage(coverage: Coverage) -> None`: Add coverage to the policy.
- `remove_coverage(coverage_type: CoverageType) -> bool`: Remove coverage from the policy.
- `add_endorsement(endorsement: Endorsement) -> None`: Add endorsement to the policy.
- `is_active() -> bool`: Check if policy is currently active.
- `days_to_expiration() -> int`: Calculate days until policy expiration.
- `to_dict() -> Dict[str, Any]`: Convert policy to dictionary for serialization.

### PolicyLifecycle
 Manages the lifecycle of insurance policies.

**Methods**:
- `transition_policy(policy: Policy, new_status: PolicyStatus, reason: str, **kwargs) -> bool`: Transition policy to status.

### PolicyManager
 policy management system.

**Methods**:
- `create_policy(application_data: Dict[str, Any], premium_calculation: Dict[str, Any], decision: Dict[str, Any]) -> Policy`: Create a insurance policy from application data.
- `get_policy(policy_id: str) -> Optional[Policy]`: Retrieve policy by ID.
- `search_policies(criteria: Dict[str, Any]) -> List[Policy]`: Search policies based on criteria.
- `update_policy(policy_id: str, updates: Dict[str, Any]) -> bool`: Update policy information.
- `add_endorsement(policy_id: str, endorsement: Endorsement) -> bool`: Add endorsement to policy.
- `bind_policy(policy_id: str, effective_date: Optional[datetime]) -> bool`: Bind quoted policy.
- `activate_policy(policy_id: str) -> bool`: Activate bound policy.
- `renew_policy(policy_id: str, renewal_term_months: Optional[int]) -> Optional[Policy]`: Renew existing policy.
- `cancel_policy(policy_id: str, reason: str, cancellation_date: Optional[datetime]) -> bool`: Cancel existing policy.
- `get_portfolio_summary(portfolio_criteria: Optional[Dict[str, Any]]) -> Dict[str, Any]`: Get portfolio summary and performance metrics.
- `export_portfolio(format: str, filename: Optional[str]) -> str`: Export portfolio data to file.
- `get_policy_performance(policy_id: str) -> Dict[str, Any]`: Get performance metrics for a specific policy.
- `health_check() -> Dict[str, Any]`: Perform health check on policy management system.

### PricingMethod
 Insurance pricing method enumeration.

### PremiumComponent
 Premium component enumeration.

### PremiumCalculation
 Premium calculation result structure.

**Methods**:
- `get_component_percentage(component: PremiumComponent) -> float`: Get percentage of total premium for a component.
- `to_dict() -> Dict[str, Any]`: Convert calculation to dictionary.

### PricingEngine
 insurance pricing engine with multiple calculation methods.

**Methods**:
- `calculate_premium(application_data: Dict[str, Any], risk_assessment: Dict[str, Any], rule_evaluation: Dict[str, Any]) -> PremiumCalculation`: Calculate insurance premium.
- `calculate_market_adjusted_premium(technical_premium: float, market_data: Dict[str, Any]) -> float`: Calculate market-adjusted premium based on competitive analysis.
- `calculate_risk_loaded_premium(base_premium: float, risk_assessment: Dict[str, Any]) -> float`: Calculate risk-loaded premium with uncertainty consideration.
- `calculate_catastrophe_premium(base_premium: float, catastrophe_assessment: Dict[str, Any]) -> float`: Calculate catastrophe-loaded premium.
- `optimize_premium_structure(target_premium: float, constraints: Dict[str, Any]) -> Dict[str, float]`: Optimize premium structure to meet business objectives.
- `validate_premium(calculation: PremiumCalculation) -> Dict[str, Any]`: Validate premium calculation for compliance and reasonableness.
- `get_pricing_metrics() -> Dict[str, Any]`: Get pricing engine performance metrics.
- `health_check() -> Dict[str, Any]`: Perform health check on pricing engine.

### PremiumCalculator
 premium calculation with multiple methodologies.

**Methods**:
- `calculate_experience_rated_premium(policy_history: Dict[str, Any], base_premium: float) -> float`: Calculate experience-rated premium based on claims history.
- `calculate_layered_premium(coverage_structure: Dict[str, Any]) -> Dict[str, float]`: Calculate premium for layered coverage structures.
- `get_rate_table(table_name: str) -> Dict[str, float]`: Get specific rate table.
- `update_rate_table(table_name: str, rates: Dict[str, float]) -> None`: Update rate table with rates.

### RiskAssessmentConfig
 Configuration for risk assessment operations.

### RiskMetrics
 risk metrics for underwriting assessment.

**Methods**:
- `to_dict() -> Dict[str, Any]`: Convert risk metrics to dictionary for serialization.

### RiskAssessmentEngine
 risk assessment engine for underwriting applications.

**Methods**:
- `assess_risk(application_data: Dict[str, Any], assessment_type: str) -> Dict[str, Any]`: Perform risk assessment for underwriting application.
- `get_risk_score_explanation(risk_results: Dict[str, Any]) -> str`: Generate human-readable explanation of risk score.
- `validate_risk_assessment(risk_results: Dict[str, Any]) -> Dict[str, Any]`: Validate risk assessment results.
- `clear_cache() -> None`: Clear risk assessment cache.
- `get_cache_info() -> Dict[str, Any]`: Get information about cached risk assessments.
- `health_check() -> Dict[str, Any]`: Perform health check on risk assessment engine.

### DecisionType
 Underwriting decision type enumeration.

### DecisionCriteria
 Decision criteria enumeration.

### DecisionCriteria
 Decision criteria configuration.

**Methods**:
- `evaluate(value: float) -> bool`: Evaluate criteria against value.
- `get_score(value: float) -> float`: Get normalized score for criteria.

### DecisionFramework
 Decision framework configuration.

**Methods**:
- `evaluate_decision_criteria(assessment_data: Dict[str, Any]) -> Dict[str, Any]`: Evaluate all decision criteria.
- `calculate_overall_score(criteria_results: Dict[str, Any]) -> float`: Calculate overall decision score.

### UnderwritingDecisionEngine
 underwriting decision engine with multi-criteria analysis.

**Methods**:
- `make_decision(assessment_data: Dict[str, Any], framework_name: str) -> Dict[str, Any]`: Make underwriting decision based on assessment data.
- `add_framework(framework: DecisionFramework) -> bool`: Add decision framework.
- `get_framework(framework_name: str) -> Optional[DecisionFramework]`: Get decision framework by name.
- `get_decision_analytics() -> Dict[str, Any]`: Get decision analytics and performance metrics.
- `export_decision_history(format: str, filename: Optional[str]) -> str`: Export decision history to file.
- `health_check() -> Dict[str, Any]`: Perform health check on decision engine.

### UnderwritingStatus
 Underwriting case status enumeration.

### UnderwritingConfig
 Configuration for underwriting operations.

### UnderwritingMetrics
 Metrics and KPIs for underwriting operations.

**Methods**:
- `update_metrics(case: UnderwritingCase, processing_time: float) -> None`: Update metrics with a completed underwriting case.
- `get_metrics_summary() -> Dict[str, Any]`: Get summary of underwriting metrics.

### UnderwritingEngine
 Main underwriting engine that orchestrates all underwriting operations.

**Methods**:
- `underwrite_policy(application_data: Dict[str, Any], auto_decide: bool) -> UnderwritingCase`: Underwrite a insurance policy application.
- `process_claim(claim_data: Dict[str, Any]) -> Claim`: Process an insurance claim.
- `get_portfolio_summary(portfolio_id: str) -> Dict[str, Any]`: Get portfolio summary and performance metrics.
- `get_underwriting_metrics() -> Dict[str, Any]`: Get underwriting performance metrics.
- `get_case_status(case_id: str) -> Optional[Dict[str, Any]]`: Get status of a specific underwriting case.
- `cancel_case(case_id: str) -> bool`: Cancel a pending underwriting case.
- `get_active_cases() -> List[Dict[str, Any]]`: Get list of all active underwriting cases.
- `update_configuration(config_updates: Dict[str, Any]) -> None`: Update underwriting configuration.
- `health_check() -> Dict[str, Any]`: Perform health check on underwriting system.
- `shutdown() -> None`: Shutdown the underwriting engine and cleanup resources.

### RuleType
 Underwriting rule type enumeration.

### RuleOperator
 Rule operator enumeration.

### RuleCondition
 Individual rule condition.

**Methods**:
- `evaluate(data: Dict[str, Any]) -> bool`: Evaluate condition against data.

### UnderwritingRule
 Underwriting rule definition.

**Methods**:
- `evaluate(data: Dict[str, Any]) -> Dict[str, Any]`: Evaluate rule against data.
- `is_applicable(data: Dict[str, Any]) -> bool`: Check if rule is applicable to the data.
- `is_effective() -> bool`: Check if rule is currently effective.
- `to_dict() -> Dict[str, Any]`: Convert rule to dictionary.

### UnderwritingRulesEngine
 underwriting rules engine with dynamic evaluation capabilities.

**Methods**:
- `add_rule(rule: UnderwritingRule) -> bool`: Add rule to the engine.
- `remove_rule(rule_id: str) -> bool`: Remove rule from the engine.
- `update_rule(rule_id: str, updates: Dict[str, Any]) -> bool`: Update existing rule.
- `evaluate_rules(data: Dict[str, Any], risk_assessment: Dict[str, Any]) -> Dict[str, Any]`: Evaluate all applicable rules against data.
- `create_rule_from_expression(expression: str, rule_type: RuleType, name: str, description: str) -> Optional[UnderwritingRule]`: Create rule from expression string.
- `get_rules_by_type(rule_type: RuleType) -> List[UnderwritingRule]`: Get rules by type.
- `get_rules_by_product(product: str) -> List[UnderwritingRule]`: Get rules applicable to product.
- `validate_rule_set() -> Dict[str, Any]`: Validate the current rule set for conflicts and issues.
- `export_rules(format: str) -> str`: Export rules to file.
- `get_evaluation_metrics() -> Dict[str, Any]`: Get rule evaluation performance metrics.
- `health_check() -> Dict[str, Any]`: Perform health check on rules engine.

### RuleEvaluator
 rule evaluation with complex logic support.

**Methods**:
- `evaluate_complex_rule(rule_expression: str, data: Dict[str, Any]) -> bool`: Evaluate complex rule expressions.

### create_claims_processor
 `create_claims_processor(config: Optional[ClaimsProcessingConfig]) -> ClaimsProcessor` Create a claims processor.

### create_sample_claim
 `create_sample_claim() -> Claim` Create a sample claim for testing.

### create_policy_manager
 `create_policy_manager(config: Optional[Dict[str, Any]]) -> PolicyManager` Create a policy manager.

### create_sample_policy
 `create_sample_policy() -> Policy` Create a sample policy for testing.

### create_pricing_engine
 `create_pricing_engine(config: Optional[Dict[str, Any]]) -> PricingEngine` Create a pricing engine.

### create_sample_premium_calculation
 `create_sample_premium_calculation() -> PremiumCalculation` Create a sample premium calculation for testing.

### create_risk_assessment_engine
 `create_risk_assessment_engine(config: Optional[RiskAssessmentConfig]) -> RiskAssessmentEngine` Create a risk assessment engine.

### assess_property_risk
 `assess_property_risk(property_data: Dict[str, Any], assessment_method: str) -> Dict[str, Any]` Convenience function to assess risk for a single property.

### create_decision_engine
 `create_decision_engine(config: Optional[Dict[str, Any]]) -> UnderwritingDecisionEngine` Create a underwriting decision engine.

### make_sample_decision
 `make_sample_decision() -> Dict[str, Any]` Make a sample underwriting decision for testing.

### create_underwriting_engine
 `create_underwriting_engine(config: Optional[UnderwritingConfig]) -> UnderwritingEngine` Create a underwriting engine instance.

### create_risk_assessment
 `create_risk_assessment(config: Optional[UnderwritingConfig]) -> RiskAssessmentEngine` Create a risk assessment engine.

### create_policy_manager
 `create_policy_manager(config: Optional[UnderwritingConfig]) -> PolicyManager` Create a policy manager.

### create_claims_processor
 `create_claims_processor(config: Optional[UnderwritingConfig]) -> ClaimsProcessor` Create a claims processor.

### create_rules_engine
 `create_rules_engine(config: Optional[Dict[str, Any]]) -> UnderwritingRulesEngine` Create a underwriting rules engine.

### create_sample_rules
 `create_sample_rules() -> List[UnderwritingRule]` Create sample underwriting rules for testing.

## Capabilities

- **38 classes** for core functionality
- **16 functions** for utility operations

## Integration

- **Location**: `src/geo_infer_risk/underwriting/core`
- **Type**: Directory Node
