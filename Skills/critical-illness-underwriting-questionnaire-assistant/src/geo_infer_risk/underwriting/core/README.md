# core
 ## Overview
 This directory contains core components. It includes 7 Python modules. ## Components
 ### claims_processin
g
.py Claims Processing: insurance claims management and settlement. **Classes**: `ClaimStatus`, `ClaimType`, `Reserve`, `Payment`, `Claim`, `ClaimsProcessingConfig`, `ClaimsProcessor`, `ClaimsEngine` **Functions**: `create_claims_processor`, `create_sample_claim` ### policy_managemen
t
.py Policy Management: insurance policy lifecycle management. **Classes**: `PolicyStatus`, `CoverageType`, `Coverage`, `Endorsement`, `Policy`, `PolicyLifecycle`, `PolicyManager` **Functions**: `create_policy_manager`, `create_sample_policy` ### pricing_engin
e
.py Pricing Engine: insurance pricing and premium calculation. **Classes**: `PricingMethod`, `PremiumComponent`, `PremiumCalculation`, `PricingEngine`, `PremiumCalculator` **Functions**: `create_pricing_engine`, `create_sample_premium_calculation` ### risk_assessmen
t
.py Risk Assessment Engine: risk evaluation for underwriting decisions. **Classes**: `RiskAssessmentConfig`, `RiskMetrics`, `RiskAssessmentEngine` **Functions**: `create_risk_assessment_engine`, `assess_property_risk` ### underwriting_decision
s
.py Underwriting Decisions Engine: decision support for underwriting. **Classes**: `DecisionType`, `DecisionCriteria`, `DecisionCriteria`, `DecisionFramework`, `UnderwritingDecisionEngine` **Functions**: `create_decision_engine`, `make_sample_decision` ### underwriting_engin
e
.py Underwriting Engine: Core orchestrator for underwriting operations. **Classes**: `UnderwritingStatus`, `UnderwritingConfig`, `UnderwritingMetrics`, `UnderwritingEngine` **Functions**: `create_underwriting_engine`, `create_risk_assessment`, `create_policy_manager`, `create_claims_processor` ### underwriting_rule
s
.py Underwriting Rules Engine: Rule-based underwriting decision support. **Classes**: `RuleType`, `RuleOperator`, `RuleCondition`, `UnderwritingRule`, `UnderwritingRulesEngine`, `RuleEvaluator` **Functions**: `create_rules_engine`, `create_sample_rules` ## Usage
 See individual component documentation for usage examples. ## Integration
 This directory integrates with other module components and may be used by higher-level modules. 