"""
Underwriting Rules Engine: Rule-based underwriting decision support.

This module provides sophisticated rule evaluation capabilities including:
- Dynamic rule evaluation and execution
- Multi-criteria decision making
- Rule conflict resolution
- Compliance and regulatory rule enforcement
- Custom rule definition and management
"""

import logging
import re
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class RuleType(Enum):
    """Underwriting rule type enumeration."""
    ELIGIBILITY = "eligibility"
    PRICING = "pricing"
    COVERAGE = "coverage"
    EXCLUSION = "exclusion"
    COMPLIANCE = "compliance"
    RISK_LIMIT = "risk_limit"

class RuleOperator(Enum):
    """Rule operator enumeration."""
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_EQUAL = "greater_equal"
    LESS_EQUAL = "less_equal"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"
    BETWEEN = "between"
    REGEX = "regex"

@dataclass
class RuleCondition:
    """Individual rule condition."""

    field: str
    operator: RuleOperator
    value: Any
    weight: float = 1.0

    def evaluate(self, data: Dict[str, Any]) -> bool:
        """Evaluate condition against data."""
        try:
            field_value = self._get_field_value(data, self.field)

            if self.operator == RuleOperator.EQUALS:
                return field_value == self.value
            elif self.operator == RuleOperator.NOT_EQUALS:
                return field_value != self.value
            elif self.operator == RuleOperator.GREATER_THAN:
                return field_value > self.value
            elif self.operator == RuleOperator.LESS_THAN:
                return field_value < self.value
            elif self.operator == RuleOperator.GREATER_EQUAL:
                return field_value >= self.value
            elif self.operator == RuleOperator.LESS_EQUAL:
                return field_value <= self.value
            elif self.operator == RuleOperator.CONTAINS:
                return str(self.value).lower() in str(field_value).lower()
            elif self.operator == RuleOperator.NOT_CONTAINS:
                return str(self.value).lower() not in str(field_value).lower()
            elif self.operator == RuleOperator.IN:
                return field_value in self.value if isinstance(self.value, list) else False
            elif self.operator == RuleOperator.NOT_IN:
                return field_value not in self.value if isinstance(self.value, list) else True
            elif self.operator == RuleOperator.BETWEEN:
                return self.value[0] <= field_value <= self.value[1] if isinstance(self.value, list) and len(self.value) == 2 else False
            elif self.operator == RuleOperator.REGEX:
                return bool(re.search(str(self.value), str(field_value)))

            return False

        except Exception as e:
            logger.warning(f"Condition evaluation failed for field {self.field}: {e}")
            return False

    def _get_field_value(self, data: Dict[str, Any], field: str) -> Any:
        """Get field value from nested data structure."""
        keys = field.split('.')
        value = data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            elif isinstance(value, list) and key.isdigit():
                value = value[int(key)]
            else:
                return None

        return value

@dataclass
class UnderwritingRule:
    """Underwriting rule definition."""

    rule_id: str
    name: str
    description: str
    rule_type: RuleType
    conditions: List[RuleCondition] = field(default_factory=list)

    # Rule behavior
    action: str = "approve"  # approve, decline, refer, modify
    action_parameters: Dict[str, Any] = field(default_factory=dict)

    # Rule metadata
    priority: int = 1
    is_active: bool = True
    effective_date: datetime = field(default_factory=datetime.now)
    expiration_date: Optional[datetime] = None

    # Applicability
    applicable_products: List[str] = field(default_factory=list)
    applicable_regions: List[str] = field(default_factory=list)

    def evaluate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate rule against data."""
        if not self.is_active or not self.is_effective():
            return {
                'rule_id': self.rule_id,
                'passed': False,
                'reason': 'Rule not active or effective',
                'action': None
            }

        # Check if rule is applicable
        if not self.is_applicable(data):
            return {
                'rule_id': self.rule_id,
                'passed': True,
                'reason': 'Rule not applicable',
                'action': None
            }

        # Evaluate all conditions
        condition_results = []
        for condition in self.conditions:
            result = condition.evaluate(data)
            condition_results.append(result)

        # Determine if rule passes
        rule_passed = all(condition_results)

        return {
            'rule_id': self.rule_id,
            'rule_name': self.name,
            'passed': rule_passed,
            'action': self.action if rule_passed else None,
            'action_parameters': self.action_parameters if rule_passed else {},
            'condition_results': condition_results,
            'priority': self.priority
        }

    def is_applicable(self, data: Dict[str, Any]) -> bool:
        """Check if rule is applicable to the data."""
        # Check product applicability
        if self.applicable_products:
            product = data.get('product_type', '')
            if product not in self.applicable_products:
                return False

        # Check region applicability
        if self.applicable_regions:
            region = data.get('region', '')
            if region not in self.applicable_regions:
                return False

        return True

    def is_effective(self) -> bool:
        """Check if rule is currently effective."""
        now = datetime.now()
        return (
            self.is_active and
            self.effective_date <= now and
            (self.expiration_date is None or self.expiration_date >= now)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary."""
        return {
            'rule_id': self.rule_id,
            'name': self.name,
            'description': self.description,
            'rule_type': self.rule_type.value,
            'conditions': [
                {
                    'field': condition.field,
                    'operator': condition.operator.value,
                    'value': condition.value,
                    'weight': condition.weight
                }
                for condition in self.conditions
            ],
            'action': self.action,
            'action_parameters': self.action_parameters,
            'priority': self.priority,
            'is_active': self.is_active,
            'effective_date': self.effective_date.isoformat(),
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'applicable_products': self.applicable_products,
            'applicable_regions': self.applicable_regions,
            'is_effective': self.is_effective()
        }

class UnderwritingRulesEngine:
    """
    Advanced underwriting rules engine with dynamic evaluation capabilities.

    This engine provides:
    - Dynamic rule evaluation and execution
    - Multi-criteria decision making
    - Rule conflict resolution
    - Compliance and regulatory rule enforcement
    - Performance monitoring and optimization
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the rules engine.

        Args:
            config: Rules engine configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger("geo_infer_risk.underwriting.rules_engine")

        # Rule storage and management
        self.rules: Dict[str, UnderwritingRule] = {}
        self.rule_index: Dict[str, List[str]] = {}  # Index by type, product, etc.

        # Performance tracking
        self.evaluation_metrics = {
            'total_evaluations': 0,
            'average_evaluation_time': 0.0,
            'rule_hits': {},
            'rule_conflicts': 0
        }

        # Load default rules
        self._load_default_rules()

        self.logger.info("Underwriting rules engine initialized")

    def add_rule(self, rule: UnderwritingRule) -> bool:
        """Add rule to the engine."""
        try:
            self.rules[rule.rule_id] = rule
            self._update_rule_index(rule)
            self.logger.info(f"Rule added: {rule.rule_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add rule {rule.rule_id}: {e}")
            return False

    def remove_rule(self, rule_id: str) -> bool:
        """Remove rule from the engine."""
        if rule_id not in self.rules:
            return False

        rule = self.rules[rule_id]
        del self.rules[rule_id]
        self._remove_from_index(rule)
        self.logger.info(f"Rule removed: {rule_id}")
        return True

    def update_rule(self, rule_id: str, updates: Dict[str, Any]) -> bool:
        """Update existing rule."""
        if rule_id not in self.rules:
            return False

        rule = self.rules[rule_id]

        try:
            # Update rule attributes
            for key, value in updates.items():
                if hasattr(rule, key):
                    setattr(rule, key, value)

            # Update index
            self._remove_from_index(rule)
            self._update_rule_index(rule)

            self.logger.info(f"Rule updated: {rule_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update rule {rule_id}: {e}")
            return False

    def evaluate_rules(self, data: Dict[str, Any], risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate all applicable rules against data.

        Args:
            data: Application or policy data
            risk_assessment: Risk assessment results

        Returns:
            Rule evaluation results
        """
        start_time = datetime.now()

        # Combine data with risk assessment
        evaluation_data = {**data, 'risk_assessment': risk_assessment}

        # Find applicable rules
        applicable_rules = self._find_applicable_rules(data)

        # Evaluate rules
        rule_results = []
        for rule_id in applicable_rules:
            rule = self.rules[rule_id]
            result = rule.evaluate(evaluation_data)
            rule_results.append(result)

            # Track metrics
            rule_key = f"{rule.rule_type.value}:{rule.name}"
            self.evaluation_metrics['rule_hits'][rule_key] = self.evaluation_metrics['rule_hits'].get(rule_key, 0) + 1

        # Resolve conflicts and determine final action
        final_decision = self._resolve_rule_conflicts(rule_results)

        # Update metrics
        self.evaluation_metrics['total_evaluations'] += 1
        evaluation_time = (datetime.now() - start_time).total_seconds()
        self.evaluation_metrics['average_evaluation_time'] = (
            self.evaluation_metrics['average_evaluation_time'] * 0.9 + evaluation_time * 0.1
        )

        return {
            'evaluation_id': f"eval_{int(time.time())}",
            'total_rules_evaluated': len(applicable_rules),
            'passed_rules': len([r for r in rule_results if r['passed']]),
            'failed_rules': len([r for r in rule_results if not r['passed']]),
            'rule_results': rule_results,
            'final_decision': final_decision,
            'evaluation_timestamp': datetime.now().isoformat(),
            'evaluation_time_seconds': evaluation_time
        }

    def _find_applicable_rules(self, data: Dict[str, Any]) -> List[str]:
        """Find rules applicable to the data."""
        applicable_rules = []

        for rule in self.rules.values():
            if rule.is_applicable(data):
                applicable_rules.append(rule.rule_id)

        # Sort by priority (higher priority first)
        applicable_rules.sort(key=lambda rid: self.rules[rid].priority, reverse=True)

        return applicable_rules

    def _resolve_rule_conflicts(self, rule_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Resolve conflicts between rule results."""
        if not rule_results:
            return {'action': 'approve', 'reason': 'No rules applicable'}

        # Separate passed and failed rules
        passed_rules = [r for r in rule_results if r['passed']]
        failed_rules = [r for r in rule_results if not r['passed']]

        # If any rule fails, the application may be declined or referred
        if failed_rules:
            # Check if there are any approval actions in passed rules
            approval_actions = [r for r in passed_rules if r.get('action') == 'approve']

            if approval_actions:
                # Conflict: some rules approve, some fail
                self.evaluation_metrics['rule_conflicts'] += 1

                # For now, be conservative and refer for manual review
                return {
                    'action': 'refer',
                    'reason': 'Rule conflict detected - manual review required',
                    'conflicting_rules': len(failed_rules) + len(approval_actions),
                    'failed_rules': len(failed_rules),
                    'approval_rules': len(approval_actions)
                }
            else:
                # All approval rules failed, decline
                return {
                    'action': 'decline',
                    'reason': f"Failed {len(failed_rules)} underwriting rules",
                    'failed_rules': len(failed_rules)
                }

        # All rules passed, check for specific actions
        if passed_rules:
            # Get highest priority action
            highest_priority_rule = max(passed_rules, key=lambda r: r.get('priority', 0))

            return {
                'action': highest_priority_rule.get('action', 'approve'),
                'reason': f"Passed {len(passed_rules)} rules, highest priority: {highest_priority_rule.get('rule_name', 'unknown')}",
                'action_parameters': highest_priority_rule.get('action_parameters', {}),
                'passed_rules': len(passed_rules)
            }

        return {'action': 'approve', 'reason': 'No applicable rules'}

    def _update_rule_index(self, rule: UnderwritingRule) -> None:
        """Update rule index for efficient searching."""
        # Index by rule type
        rule_type = rule.rule_type.value
        if rule_type not in self.rule_index:
            self.rule_index[rule_type] = []
        if rule.rule_id not in self.rule_index[rule_type]:
            self.rule_index[rule_type].append(rule.rule_id)

        # Index by product
        for product in rule.applicable_products:
            if product not in self.rule_index:
                self.rule_index[product] = []
            if rule.rule_id not in self.rule_index[product]:
                self.rule_index[product].append(rule.rule_id)

    def _remove_from_index(self, rule: UnderwritingRule) -> None:
        """Remove rule from index."""
        # Remove from type index
        rule_type = rule.rule_type.value
        if rule_type in self.rule_index and rule.rule_id in self.rule_index[rule_type]:
            self.rule_index[rule_type].remove(rule.rule_id)

        # Remove from product indexes
        for product in rule.applicable_products:
            if product in self.rule_index and rule.rule_id in self.rule_index[product]:
                self.rule_index[product].remove(rule.rule_id)

    def _load_default_rules(self) -> None:
        """Load default underwriting rules."""
        # Property value limits
        self.add_rule(UnderwritingRule(
            rule_id="max_property_value",
            name="Maximum Property Value",
            description="Property value cannot exceed $10M",
            rule_type=RuleType.ELIGIBILITY,
            conditions=[
                RuleCondition("property.value", RuleOperator.LESS_EQUAL, 10000000)
            ],
            action="approve",
            priority=10
        ))

        # Minimum property value
        self.add_rule(UnderwritingRule(
            rule_id="min_property_value",
            name="Minimum Property Value",
            description="Property value must be at least $10K",
            rule_type=RuleType.ELIGIBILITY,
            conditions=[
                RuleCondition("property.value", RuleOperator.GREATER_EQUAL, 10000)
            ],
            action="approve",
            priority=10
        ))

        # Age restrictions for certain properties
        self.add_rule(UnderwritingRule(
            rule_id="property_age_limit",
            name="Property Age Limit",
            description="Properties older than 100 years require special approval",
            rule_type=RuleType.RISK_LIMIT,
            conditions=[
                RuleCondition("property.year_built", RuleOperator.GREATER_THAN, datetime.now().year - 100)
            ],
            action="refer",
            priority=5
        ))

        # High-risk locations
        self.add_rule(UnderwritingRule(
            rule_id="high_risk_location",
            name="High Risk Location",
            description="Properties in high-risk flood zones require review",
            rule_type=RuleType.RISK_LIMIT,
            conditions=[
                RuleCondition("property.flood_zone", RuleOperator.EQUALS, "A")
            ],
            action="refer",
            priority=8
        ))

        # Coverage limits
        self.add_rule(UnderwritingRule(
            rule_id="coverage_limit_check",
            name="Coverage Limit Check",
            description="Coverage cannot exceed property value",
            rule_type=RuleType.COVERAGE,
            conditions=[
                RuleCondition("coverage.limit", RuleOperator.LESS_EQUAL, "property.value")
            ],
            action="modify",
            action_parameters={"max_limit": "property.value"},
            priority=9
        ))

        self.logger.info("Default underwriting rules loaded")

    def create_rule_from_expression(self, expression: str, rule_type: RuleType,
                                  name: str, description: str = "") -> Optional[UnderwritingRule]:
        """
        Create rule from expression string.

        Args:
            expression: Rule expression (e.g., "property.value > 100000")
            rule_type: Type of rule
            name: Rule name
            description: Rule description

        Returns:
            Created rule or None if parsing failed
        """
        try:
            # Simple expression parser (could be enhanced)
            # Format: field operator value
            parts = expression.split()
            if len(parts) >= 3:
                field = parts[0]
                operator_str = parts[1]
                value = " ".join(parts[2:])

                # Parse operator
                operator_map = {
                    '=': RuleOperator.EQUALS,
                    '==': RuleOperator.EQUALS,
                    '!=': RuleOperator.NOT_EQUALS,
                    '>': RuleOperator.GREATER_THAN,
                    '<': RuleOperator.LESS_THAN,
                    '>=': RuleOperator.GREATER_EQUAL,
                    '<=': RuleOperator.LESS_EQUAL,
                    'contains': RuleOperator.CONTAINS,
                    'in': RuleOperator.IN
                }

                operator = operator_map.get(operator_str)
                if not operator:
                    self.logger.error(f"Unknown operator: {operator_str}")
                    return None

                # Parse value
                try:
                    if value.isdigit():
                        parsed_value = int(value)
                    elif value.replace('.', '').isdigit():
                        parsed_value = float(value)
                    else:
                        parsed_value = value
                except:
                    parsed_value = value

                # Create condition
                condition = RuleCondition(field=field, operator=operator, value=parsed_value)

                # Create rule
                rule = UnderwritingRule(
                    rule_id=f"expr_{int(time.time())}",
                    name=name,
                    description=description or f"Rule from expression: {expression}",
                    rule_type=rule_type,
                    conditions=[condition]
                )

                return rule

        except Exception as e:
            self.logger.error(f"Failed to create rule from expression: {e}")

        return None

    def get_rules_by_type(self, rule_type: RuleType) -> List[UnderwritingRule]:
        """Get rules by type."""
        rule_ids = self.rule_index.get(rule_type.value, [])
        return [self.rules[rid] for rid in rule_ids if rid in self.rules]

    def get_rules_by_product(self, product: str) -> List[UnderwritingRule]:
        """Get rules applicable to product."""
        rule_ids = self.rule_index.get(product, [])
        return [self.rules[rid] for rid in rule_ids if rid in self.rules]

    def validate_rule_set(self) -> Dict[str, Any]:
        """Validate the current rule set for conflicts and issues."""
        validation_result = {
            'is_valid': True,
            'conflicts': [],
            'warnings': [],
            'coverage_gaps': []
        }

        # Check for conflicting rules
        rules_by_priority = sorted(self.rules.values(), key=lambda r: r.priority, reverse=True)

        for i, rule1 in enumerate(rules_by_priority):
            for rule2 in rules_by_priority[i+1:]:
                if self._rules_conflict(rule1, rule2):
                    validation_result['conflicts'].append({
                        'rule1': rule1.rule_id,
                        'rule2': rule2.rule_id,
                        'conflict_type': 'action_conflict'
                    })
                    validation_result['is_valid'] = False

        # Check for coverage gaps
        required_checks = ['property_value', 'location_risk', 'coverage_limits']
        covered_checks = set()

        for rule in self.rules.values():
            for condition in rule.conditions:
                if condition.field in required_checks:
                    covered_checks.add(condition.field)

        missing_checks = set(required_checks) - covered_checks
        if missing_checks:
            validation_result['warnings'].append(f"Missing rule coverage for: {missing_checks}")

        return validation_result

    def _rules_conflict(self, rule1: UnderwritingRule, rule2: UnderwritingRule) -> bool:
        """Check if two rules conflict."""
        # Simple conflict detection - rules with same conditions but different actions
        if (rule1.action != rule2.action and
            rule1.conditions == rule2.conditions and
            rule1.is_applicable == rule2.is_applicable):
            return True
        return False

    def export_rules(self, format: str = "json") -> str:
        """Export rules to file."""
        if format == "json":
            rules_data = [rule.to_dict() for rule in self.rules.values()]
            filename = f"underwriting_rules_{int(time.time())}.json"

            import json
            with open(filename, 'w') as f:
                json.dump(rules_data, f, indent=2)

            return filename

        return ""

    def get_evaluation_metrics(self) -> Dict[str, Any]:
        """Get rule evaluation performance metrics."""
        return {
            'total_evaluations': self.evaluation_metrics['total_evaluations'],
            'average_evaluation_time': self.evaluation_metrics['average_evaluation_time'],
            'rule_hit_counts': self.evaluation_metrics['rule_hits'],
            'conflicts_resolved': self.evaluation_metrics['rule_conflicts']
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on rules engine."""
        return {
            'status': 'operational',
            'total_rules': len(self.rules),
            'active_rules': len([r for r in self.rules.values() if r.is_active]),
            'rules_by_type': {rt: len(self.rule_index.get(rt, [])) for rt in ['eligibility', 'pricing', 'coverage']},
            'last_evaluation': datetime.now().isoformat()
        }


class RuleEvaluator:
    """Advanced rule evaluation with complex logic support."""

    def __init__(self):
        self.logger = logging.getLogger("geo_infer_risk.underwriting.rule_evaluator")

    def evaluate_complex_rule(self, rule_expression: str, data: Dict[str, Any]) -> bool:
        """
        Evaluate complex rule expressions.

        Args:
            rule_expression: Complex rule expression
            data: Data to evaluate against

        Returns:
            True if rule passes
        """
        try:
            # Simple expression evaluation (could be enhanced with AST parsing)
            # Example: "property.value > 100000 AND property.age < 50"

            # Split by logical operators
            and_parts = rule_expression.upper().split(' AND ')
            or_parts = rule_expression.upper().split(' OR ')

            if len(and_parts) > 1:
                # AND logic
                return all(self._evaluate_simple_expression(part.strip(), data) for part in and_parts)
            elif len(or_parts) > 1:
                # OR logic
                return any(self._evaluate_simple_expression(part.strip(), data) for part in or_parts)
            else:
                # Single condition
                return self._evaluate_simple_expression(rule_expression, data)

        except Exception as e:
            self.logger.error(f"Complex rule evaluation failed: {e}")
            return False

    def _evaluate_simple_expression(self, expression: str, data: Dict[str, Any]) -> bool:
        """Evaluate simple rule expression."""
        # Simple pattern matching for common expressions
        if '>' in expression:
            parts = expression.split('>')
            if len(parts) == 2:
                field = parts[0].strip()
                value = float(parts[1].strip())
                field_value = self._get_nested_value(data, field)
                return field_value > value

        elif '<' in expression:
            parts = expression.split('<')
            if len(parts) == 2:
                field = parts[0].strip()
                value = float(parts[1].strip())
                field_value = self._get_nested_value(data, field)
                return field_value < value

        elif '==' in expression or '=' in expression:
            parts = expression.replace('==', '=').split('=')
            if len(parts) == 2:
                field = parts[0].strip()
                value = parts[1].strip().strip('"\'')
                field_value = self._get_nested_value(data, field)
                return str(field_value) == str(value)

        return False

    def _get_nested_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """Get value from nested data structure."""
        keys = field_path.split('.')
        value = data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None

        return value


# Convenience functions
def create_rules_engine(config: Optional[Dict[str, Any]] = None) -> UnderwritingRulesEngine:
    """Create a new underwriting rules engine."""
    return UnderwritingRulesEngine(config)

def create_sample_rules() -> List[UnderwritingRule]:
    """Create sample underwriting rules for testing."""
    rules = []

    # Property value rule
    rules.append(UnderwritingRule(
        rule_id="sample_prop_value",
        name="Sample Property Value Check",
        description="Property value must be reasonable",
        rule_type=RuleType.ELIGIBILITY,
        conditions=[
            RuleCondition("property.value", RuleOperator.BETWEEN, [10000, 10000000])
        ],
        action="approve"
    ))

    # Risk score rule
    rules.append(UnderwritingRule(
        rule_id="sample_risk_score",
        name="Sample Risk Score Check",
        description="Risk score must be acceptable",
        rule_type=RuleType.RISK_LIMIT,
        conditions=[
            RuleCondition("risk_assessment.risk_score", RuleOperator.LESS_THAN, 0.8)
        ],
        action="approve"
    ))

    return rules
