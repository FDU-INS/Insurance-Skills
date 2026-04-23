"""
Compliance Engine: Regulatory compliance and governance for underwriting.

This module provides compliance capabilities including:
- Regulatory framework management
- Compliance rule enforcement
- Audit trail and logging
- Regulatory reporting
- Compliance monitoring and alerts
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class ComplianceFramework(Enum):
    """Compliance framework enumeration."""
    STANDARD = "standard"
    SOLVENCY_II = "solvency_ii"
    BASEL_III = "basel_iii"
    IFRS_17 = "ifrs_17"
    US_INSURANCE_REGULATION = "us_insurance"
    EU_INSURANCE_DISTRIBUTION = "eu_idd"

class ComplianceStatus(Enum):
    """Compliance status enumeration."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"
    EXEMPT = "exempt"
    UNKNOWN = "unknown"

@dataclass
class RegulatoryRequirement:
    """Regulatory requirement structure."""

    requirement_id: str
    framework: ComplianceFramework
    category: str  # capital, reporting, governance, etc.
    description: str
    regulation_reference: str
    applicability_criteria: Dict[str, Any] = field(default_factory=dict)
    compliance_threshold: float = 1.0
    monitoring_frequency: str = "quarterly"

    def is_applicable(self, context: Dict[str, Any]) -> bool:
        """Check if requirement is applicable."""
        for key, value in self.applicability_criteria.items():
            if key in context and context[key] != value:
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert requirement to dictionary."""
        return {
            'requirement_id': self.requirement_id,
            'framework': self.framework.value,
            'category': self.category,
            'description': self.description,
            'regulation_reference': self.regulation_reference,
            'applicability_criteria': self.applicability_criteria,
            'compliance_threshold': self.compliance_threshold,
            'monitoring_frequency': self.monitoring_frequency
        }

@dataclass
class ComplianceCheck:
    """Compliance check result."""

    check_id: str
    requirement_id: str
    entity_id: str
    status: ComplianceStatus
    check_date: datetime = field(default_factory=datetime.now)
    next_check_date: Optional[datetime] = None
    findings: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    remediation_required: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert check to dictionary."""
        return {
            'check_id': self.check_id,
            'requirement_id': self.requirement_id,
            'entity_id': self.entity_id,
            'status': self.status.value,
            'check_date': self.check_date.isoformat(),
            'next_check_date': self.next_check_date.isoformat() if self.next_check_date else None,
            'findings': self.findings,
            'evidence': self.evidence,
            'remediation_required': self.remediation_required
        }

class ComplianceEngine:
    """
    Comprehensive compliance engine for regulatory adherence.

    This engine provides:
    - Regulatory framework management and monitoring
    - Compliance rule enforcement and validation
    - Audit trail maintenance and reporting
    - Regulatory reporting and filing support
    - Compliance risk assessment and mitigation
    """

    def __init__(self, framework: ComplianceFramework = ComplianceFramework.STANDARD):
        """
        Initialize the compliance engine.

        Args:
            framework: Primary compliance framework
        """
        self.framework = framework
        self.logger = logging.getLogger("geo_infer_risk.underwriting.compliance")

        # Regulatory requirements
        self.requirements: Dict[str, RegulatoryRequirement] = {}
        self.compliance_checks: Dict[str, ComplianceCheck] = {}

        # Load framework requirements
        self._load_framework_requirements()

        self.logger.info(f"Compliance engine initialized for {framework.value}")

    def _load_framework_requirements(self) -> None:
        """Load regulatory requirements for the framework."""
        if self.framework == ComplianceFramework.SOLVENCY_II:
            self._load_solvency_ii_requirements()
        elif self.framework == ComplianceFramework.BASEL_III:
            self._load_basel_iii_requirements()
        elif self.framework == ComplianceFramework.US_INSURANCE_REGULATION:
            self._load_us_insurance_requirements()
        else:
            self._load_standard_requirements()

    def _load_standard_requirements(self) -> None:
        """Load standard compliance requirements."""
        requirements = [
            RegulatoryRequirement(
                requirement_id="std_capital_adequacy",
                framework=ComplianceFramework.STANDARD,
                category="capital",
                description="Maintain adequate capital reserves",
                regulation_reference="Standard Insurance Regulation §1.1",
                applicability_criteria={"entity_type": "insurer"},
                compliance_threshold=1.0,
                monitoring_frequency="quarterly"
            ),
            RegulatoryRequirement(
                requirement_id="std_reporting_accuracy",
                framework=ComplianceFramework.STANDARD,
                category="reporting",
                description="Ensure accurate and timely reporting",
                regulation_reference="Standard Insurance Regulation §2.3",
                applicability_criteria={},
                compliance_threshold=0.95,
                monitoring_frequency="monthly"
            )
        ]

        for req in requirements:
            self.requirements[req.requirement_id] = req

    def _load_solvency_ii_requirements(self) -> None:
        """Load Solvency II requirements."""
        requirements = [
            RegulatoryRequirement(
                requirement_id="sii_scr_coverage",
                framework=ComplianceFramework.SOLVENCY_II,
                category="capital",
                description="Solvency Capital Requirement coverage",
                regulation_reference="Solvency II Directive Article 101",
                applicability_criteria={"entity_type": "european_insurer"},
                compliance_threshold=1.0,
                monitoring_frequency="quarterly"
            ),
            RegulatoryRequirement(
                requirement_id="sii_or_reporting",
                framework=ComplianceFramework.SOLVENCY_II,
                category="reporting",
                description="Own Risk and Solvency Assessment reporting",
                regulation_reference="Solvency II Directive Article 45",
                applicability_criteria={},
                compliance_threshold=1.0,
                monitoring_frequency="annual"
            )
        ]

        for req in requirements:
            self.requirements[req.requirement_id] = req

    def _load_basel_iii_requirements(self) -> None:
        """Load Basel III requirements."""
        requirements = [
            RegulatoryRequirement(
                requirement_id="basel_tier1_capital",
                framework=ComplianceFramework.BASEL_III,
                category="capital",
                description="Tier 1 capital ratio requirement",
                regulation_reference="Basel III Framework",
                applicability_criteria={"entity_type": "bank"},
                compliance_threshold=0.06,  # 6%
                monitoring_frequency="quarterly"
            )
        ]

        for req in requirements:
            self.requirements[req.requirement_id] = req

    def _load_us_insurance_requirements(self) -> None:
        """Load US insurance regulation requirements."""
        requirements = [
            RegulatoryRequirement(
                requirement_id="us_risk_based_capital",
                framework=ComplianceFramework.US_INSURANCE_REGULATION,
                category="capital",
                description="Risk-Based Capital requirements",
                regulation_reference="NAIC Risk-Based Capital Model Act",
                applicability_criteria={"entity_type": "us_insurer"},
                compliance_threshold=2.0,  # 200% RBC ratio
                monitoring_frequency="annual"
            )
        ]

        for req in requirements:
            self.requirements[req.requirement_id] = req

    def perform_compliance_check(self, entity_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform compliance check for entity.

        Args:
            entity_id: Entity identifier
            context: Context information for compliance evaluation

        Returns:
            Compliance check results
        """
        check_results = []
        overall_status = ComplianceStatus.COMPLIANT

        for requirement in self.requirements.values():
            if requirement.is_applicable(context):
                check_result = self._check_requirement_compliance(requirement, entity_id, context)
                check_results.append(check_result)

                # Update overall status
                if check_result.status == ComplianceStatus.NON_COMPLIANT:
                    overall_status = ComplianceStatus.NON_COMPLIANT
                elif check_result.status == ComplianceStatus.PENDING_REVIEW and overall_status == ComplianceStatus.COMPLIANT:
                    overall_status = ComplianceStatus.PENDING_REVIEW

        return {
            'entity_id': entity_id,
            'check_date': datetime.now().isoformat(),
            'overall_status': overall_status.value,
            'framework': self.framework.value,
            'requirement_checks': check_results,
            'total_requirements': len(check_results),
            'compliant_requirements': len([r for r in check_results if r.status == ComplianceStatus.COMPLIANT]),
            'non_compliant_requirements': len([r for r in check_results if r.status == ComplianceStatus.NON_COMPLIANT])
        }

    def _check_requirement_compliance(self, requirement: RegulatoryRequirement,
                                    entity_id: str, context: Dict[str, Any]) -> ComplianceCheck:
        """Check compliance for specific requirement."""
        check_id = f"check_{entity_id}_{requirement.requirement_id}_{int(time.time())}"

        # Get compliance value
        compliance_value = self._get_compliance_value(requirement, context)

        # Determine status
        if compliance_value >= requirement.compliance_threshold:
            status = ComplianceStatus.COMPLIANT
            findings = ["Requirement satisfied"]
        else:
            status = ComplianceStatus.NON_COMPLIANT
            findings = [f"Compliance value {compliance_value} below threshold {requirement.compliance_threshold}"]

        # Calculate next check date
        next_check_date = self._calculate_next_check_date(requirement.monitoring_frequency)

        check = ComplianceCheck(
            check_id=check_id,
            requirement_id=requirement.requirement_id,
            entity_id=entity_id,
            status=status,
            next_check_date=next_check_date,
            findings=findings,
            evidence={'compliance_value': compliance_value, 'threshold': requirement.compliance_threshold}
        )

        self.compliance_checks[check_id] = check
        return check

    def _get_compliance_value(self, requirement: RegulatoryRequirement, context: Dict[str, Any]) -> float:
        """Get compliance value for requirement."""
        # Simplified compliance calculation - in practice would be more sophisticated
        if requirement.category == "capital":
            return context.get('capital_ratio', 1.0)
        elif requirement.category == "reporting":
            return context.get('reporting_accuracy', 0.95)
        else:
            return 1.0  # Default compliant

    def _calculate_next_check_date(self, frequency: str) -> datetime:
        """Calculate next check date based on frequency."""
        now = datetime.now()

        if frequency == "daily":
            return now + timedelta(days=1)
        elif frequency == "weekly":
            return now + timedelta(weeks=1)
        elif frequency == "monthly":
            return now + timedelta(days=30)
        elif frequency == "quarterly":
            return now + timedelta(days=90)
        elif frequency == "annual":
            return now + timedelta(days=365)
        else:
            return now + timedelta(days=90)  # Default to quarterly

    def generate_compliance_report(self, entity_id: str, period: str = "quarterly") -> Dict[str, Any]:
        """
        Generate compliance report for entity.

        Args:
            entity_id: Entity identifier
            period: Reporting period

        Returns:
            Compliance report
        """
        # Get relevant compliance checks
        entity_checks = [
            check for check in self.compliance_checks.values()
            if check.entity_id == entity_id and
            check.check_date >= datetime.now() - self._get_period_timedelta(period)
        ]

        # Calculate compliance metrics
        total_checks = len(entity_checks)
        compliant_checks = len([c for c in entity_checks if c.status == ComplianceStatus.COMPLIANT])
        compliance_rate = compliant_checks / total_checks if total_checks > 0 else 0

        # Identify issues
        issues = []
        for check in entity_checks:
            if check.status != ComplianceStatus.COMPLIANT:
                issues.extend(check.findings)

        return {
            'entity_id': entity_id,
            'report_period': period,
            'report_date': datetime.now().isoformat(),
            'framework': self.framework.value,
            'compliance_rate': compliance_rate,
            'total_checks': total_checks,
            'compliant_checks': compliant_checks,
            'non_compliant_checks': total_checks - compliant_checks,
            'issues': issues,
            'requirements_checked': list(set(check.requirement_id for check in entity_checks)),
            'next_review_date': (datetime.now() + self._get_period_timedelta(period)).isoformat()
        }

    def _get_period_timedelta(self, period: str) -> timedelta:
        """Get timedelta for reporting period."""
        if period == "daily":
            return timedelta(days=1)
        elif period == "weekly":
            return timedelta(weeks=1)
        elif period == "monthly":
            return timedelta(days=30)
        elif period == "quarterly":
            return timedelta(days=90)
        elif period == "annual":
            return timedelta(days=365)
        else:
            return timedelta(days=90)

    def add_requirement(self, requirement: RegulatoryRequirement) -> bool:
        """Add regulatory requirement."""
        try:
            self.requirements[requirement.requirement_id] = requirement
            self.logger.info(f"Requirement added: {requirement.requirement_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add requirement: {e}")
            return False

    def remove_requirement(self, requirement_id: str) -> bool:
        """Remove regulatory requirement."""
        if requirement_id in self.requirements:
            del self.requirements[requirement_id]
            self.logger.info(f"Requirement removed: {requirement_id}")
            return True
        return False

    def get_compliance_status(self, entity_id: str) -> Dict[str, Any]:
        """Get compliance status for entity."""
        # Get recent checks for entity
        entity_checks = [
            check for check in self.compliance_checks.values()
            if check.entity_id == entity_id and
            check.check_date >= datetime.now() - timedelta(days=30)  # Last 30 days
        ]

        if not entity_checks:
            return {'status': ComplianceStatus.UNKNOWN.value, 'last_check': None}

        # Determine overall status
        statuses = [check.status for check in entity_checks]

        if ComplianceStatus.NON_COMPLIANT in statuses:
            overall_status = ComplianceStatus.NON_COMPLIANT
        elif ComplianceStatus.PENDING_REVIEW in statuses:
            overall_status = ComplianceStatus.PENDING_REVIEW
        else:
            overall_status = ComplianceStatus.COMPLIANT

        return {
            'entity_id': entity_id,
            'status': overall_status.value,
            'last_check': max(check.check_date for check in entity_checks).isoformat(),
            'total_checks': len(entity_checks),
            'compliant_checks': len([c for c in entity_checks if c.status == ComplianceStatus.COMPLIANT])
        }

    def get_framework_requirements(self) -> List[Dict[str, Any]]:
        """Get all requirements for current framework."""
        return [req.to_dict() for req in self.requirements.values()]

    def set_framework(self, framework: ComplianceFramework) -> None:
        """Set compliance framework."""
        self.framework = framework
        self.requirements.clear()
        self._load_framework_requirements()
        self.logger.info(f"Compliance framework changed to {framework.value}")

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on compliance engine."""
        return {
            'status': 'operational',
            'framework': self.framework.value,
            'total_requirements': len(self.requirements),
            'total_checks': len(self.compliance_checks),
            'last_check': max(self.compliance_checks.values(), key=lambda x: x.check_date).check_date.isoformat() if self.compliance_checks else None,
            'timestamp': datetime.now().isoformat()
        }


class RegulatoryFramework:
    """Regulatory framework management."""

    def __init__(self):
        """Initialize regulatory framework manager."""
        self.logger = logging.getLogger("geo_infer_risk.underwriting.regulatory_framework")

        # Framework definitions
        self.frameworks = {
            ComplianceFramework.STANDARD: self._define_standard_framework(),
            ComplianceFramework.SOLVENCY_II: self._define_solvency_ii_framework(),
            ComplianceFramework.BASEL_III: self._define_basel_iii_framework(),
            ComplianceFramework.US_INSURANCE_REGULATION: self._define_us_insurance_framework()
        }

    def _define_standard_framework(self) -> Dict[str, Any]:
        """Define standard compliance framework."""
        return {
            'name': 'Standard Insurance Regulation',
            'description': 'Basic insurance regulatory compliance',
            'requirements': ['capital_adequacy', 'reporting_accuracy', 'consumer_protection'],
            'reporting_frequency': 'quarterly',
            'penalties': ['fines', 'license_suspension']
        }

    def _define_solvency_ii_framework(self) -> Dict[str, Any]:
        """Define Solvency II framework."""
        return {
            'name': 'Solvency II',
            'description': 'European insurance regulatory framework',
            'requirements': ['scr_coverage', 'or_reporting', 'governance', 'public_disclosure'],
            'reporting_frequency': 'quarterly',
            'penalties': ['fines', 'capital_addons', 'supervisory_intervention']
        }

    def _define_basel_iii_framework(self) -> Dict[str, Any]:
        """Define Basel III framework."""
        return {
            'name': 'Basel III',
            'description': 'Banking regulatory framework',
            'requirements': ['tier1_capital', 'leverage_ratio', 'liquidity_coverage'],
            'reporting_frequency': 'quarterly',
            'penalties': ['capital_restrictions', 'supervisory_measures']
        }

    def _define_us_insurance_framework(self) -> Dict[str, Any]:
        """Define US insurance regulation framework."""
        return {
            'name': 'US Insurance Regulation',
            'description': 'US state-based insurance regulation',
            'requirements': ['rbc_requirements', 'market_conduct', 'financial_reporting'],
            'reporting_frequency': 'annual',
            'penalties': ['fines', 'license_revocation', 'civil_penalties']
        }

    def get_framework_info(self, framework: ComplianceFramework) -> Dict[str, Any]:
        """Get framework information."""
        return self.frameworks.get(framework, {})

    def get_all_frameworks(self) -> Dict[str, Dict[str, Any]]:
        """Get all framework definitions."""
        return {k.value: v for k, v in self.frameworks.items()}


# Convenience functions
def create_compliance_engine(framework: ComplianceFramework = ComplianceFramework.STANDARD) -> ComplianceEngine:
    """Create a new compliance engine."""
    return ComplianceEngine(framework)

def check_policy_compliance(policy_data: Dict[str, Any],
                           framework: ComplianceFramework = ComplianceFramework.STANDARD) -> Dict[str, Any]:
    """
    Check policy compliance with regulatory framework.

    Args:
        policy_data: Policy information
        framework: Compliance framework to check against

    Returns:
        Compliance check results
    """
    engine = ComplianceEngine(framework)
    return engine.perform_compliance_check(
        entity_id=policy_data.get('policy_id', 'unknown'),
        context={'entity_type': 'insurer', 'policy_type': policy_data.get('policy_type', 'standard')}
    )
