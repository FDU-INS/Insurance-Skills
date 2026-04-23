"""
Reporting: Comprehensive reporting and analytics for underwriting operations.

This module provides reporting capabilities including:
- Underwriting performance reports
- Portfolio analysis and reporting
- Claims analytics and trends
- Regulatory compliance reporting
- Management dashboards and KPIs
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

@dataclass
class ReportConfig:
    """Configuration for reporting operations."""

    report_type: str = "summary"
    date_range: Optional[Tuple[datetime, datetime]] = None
    include_charts: bool = True
    include_details: bool = False
    output_format: str = "json"
    aggregation_level: str = "daily"  # daily, weekly, monthly, quarterly, annual

class UnderwritingReporter:
    """Comprehensive reporting for underwriting operations."""

    def __init__(self, underwriting_engine: Optional[Any] = None):
        """
        Initialize the underwriting reporter.

        Args:
            underwriting_engine: Underwriting engine instance for data access
        """
        self.underwriting_engine = underwriting_engine
        self.logger = logging.getLogger("geo_infer_risk.underwriting.reporting")

        # Report templates and configurations
        self.report_templates = self._load_report_templates()

    def _load_report_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load report templates and configurations."""
        return {
            'underwriting_summary': {
                'title': 'Underwriting Summary Report',
                'sections': ['overview', 'performance', 'trends', 'recommendations'],
                'metrics': ['total_cases', 'approval_rate', 'average_premium', 'processing_time'],
                'charts': ['approval_trends', 'premium_distribution', 'processing_efficiency']
            },
            'portfolio_analysis': {
                'title': 'Portfolio Analysis Report',
                'sections': ['composition', 'risk_distribution', 'performance', 'optimization'],
                'metrics': ['total_premium', 'risk_concentration', 'diversification_ratio', 'return_on_capital'],
                'charts': ['portfolio_composition', 'risk_heatmap', 'performance_trends']
            },
            'claims_analysis': {
                'title': 'Claims Analysis Report',
                'sections': ['overview', 'trends', 'patterns', 'fraud_detection'],
                'metrics': ['total_claims', 'average_settlement', 'processing_time', 'fraud_rate'],
                'charts': ['claims_trends', 'severity_distribution', 'processing_efficiency']
            },
            'compliance_report': {
                'title': 'Compliance Report',
                'sections': ['framework_status', 'requirement_analysis', 'audit_findings', 'remediation'],
                'metrics': ['compliance_rate', 'audit_score', 'outstanding_issues', 'improvement_areas'],
                'charts': ['compliance_trends', 'requirement_heatmap', 'audit_results']
            }
        }

    def generate_report(self, report_type: str, config: Optional[ReportConfig] = None) -> Dict[str, Any]:
        """
        Generate comprehensive underwriting report.

        Args:
            report_type: Type of report to generate
            config: Report configuration

        Returns:
            Generated report data
        """
        config = config or ReportConfig(report_type=report_type)

        try:
            if report_type == "underwriting_summary":
                return self._generate_underwriting_summary(config)
            elif report_type == "portfolio_analysis":
                return self._generate_portfolio_analysis(config)
            elif report_type == "claims_analysis":
                return self._generate_claims_analysis(config)
            elif report_type == "compliance_report":
                return self._generate_compliance_report(config)
            else:
                raise ValueError(f"Unknown report type: {report_type}")

        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return {
                'report_type': report_type,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _generate_underwriting_summary(self, config: ReportConfig) -> Dict[str, Any]:
        """Generate underwriting summary report."""
        if not self.underwriting_engine:
            return {'error': 'Underwriting engine not available'}

        # Get underwriting metrics
        metrics = self.underwriting_engine.get_underwriting_metrics()

        # Get case data
        active_cases = self.underwriting_engine.get_active_cases()
        case_details = [self.underwriting_engine.get_case_status(case_id) for case_id in active_cases[:10]]

        # Generate overview
        overview = {
            'total_cases_processed': metrics.get('total_cases', 0),
            'active_cases': len(active_cases),
            'approval_rate': metrics.get('approval_rate', 0.0),
            'average_processing_time': metrics.get('average_processing_time_hours', 0.0),
            'average_premium': metrics.get('average_premium', 0.0),
            'last_updated': datetime.now().isoformat()
        }

        # Generate performance analysis
        performance = self._analyze_underwriting_performance(metrics)

        # Generate trends
        trends = self._analyze_underwriting_trends()

        # Generate recommendations
        recommendations = self._generate_underwriting_recommendations(metrics, performance)

        return {
            'report_type': 'underwriting_summary',
            'title': self.report_templates['underwriting_summary']['title'],
            'timestamp': datetime.now().isoformat(),
            'config': config.__dict__ if config else {},
            'overview': overview,
            'performance': performance,
            'trends': trends,
            'recommendations': recommendations,
            'case_details': case_details
        }

    def _generate_portfolio_analysis(self, config: ReportConfig) -> Dict[str, Any]:
        """Generate portfolio analysis report."""
        if not self.underwriting_engine:
            return {'error': 'Underwriting engine not available'}

        # Get portfolio summary
        portfolio_summary = self.underwriting_engine.get_portfolio_summary()

        # Get policy data
        policies = []
        if hasattr(self.underwriting_engine, 'policy_manager'):
            # Get sample of policies for analysis
            sample_policies = list(self.underwriting_engine.policy_manager.policies.values())[:100]
            policies = [policy.get_policy_summary() for policy in sample_policies]

        # Analyze portfolio composition
        composition = self._analyze_portfolio_composition(policies)

        # Analyze risk distribution
        risk_distribution = self._analyze_risk_distribution(policies)

        # Analyze performance
        performance = self._analyze_portfolio_performance(portfolio_summary)

        return {
            'report_type': 'portfolio_analysis',
            'title': self.report_templates['portfolio_analysis']['title'],
            'timestamp': datetime.now().isoformat(),
            'portfolio_summary': portfolio_summary,
            'composition': composition,
            'risk_distribution': risk_distribution,
            'performance': performance
        }

    def _generate_claims_analysis(self, config: ReportConfig) -> Dict[str, Any]:
        """Generate claims analysis report."""
        if not self.underwriting_engine:
            return {'error': 'Underwriting engine not available'}

        # Get claims summary
        claims_summary = self.underwriting_engine.get_claims_summary()

        # Get claim data
        claims = []
        if hasattr(self.underwriting_engine, 'claims_processor'):
            # Get sample of claims for analysis
            sample_claims = list(self.underwriting_engine.claims_processor.claims.values())[:100]
            claims = [claim.get_claim_summary() for claim in sample_claims]

        # Analyze claims trends
        trends = self._analyze_claims_trends(claims)

        # Analyze claims patterns
        patterns = self._analyze_claims_patterns(claims)

        # Generate fraud analysis
        fraud_analysis = self._analyze_fraud_patterns(claims)

        return {
            'report_type': 'claims_analysis',
            'title': self.report_templates['claims_analysis']['title'],
            'timestamp': datetime.now().isoformat(),
            'claims_summary': claims_summary,
            'trends': trends,
            'patterns': patterns,
            'fraud_analysis': fraud_analysis
        }

    def _generate_compliance_report(self, config: ReportConfig) -> Dict[str, Any]:
        """Generate compliance report."""
        if not self.underwriting_engine:
            return {'error': 'Underwriting engine not available'}

        # Get compliance data
        compliance_status = {}
        if hasattr(self.underwriting_engine, 'compliance_engine'):
            compliance_status = self.underwriting_engine.compliance_engine.get_compliance_status()

        # Generate framework analysis
        framework_analysis = self._analyze_compliance_framework()

        # Generate audit findings
        audit_findings = self._analyze_audit_findings()

        # Generate remediation recommendations
        remediation = self._generate_remediation_recommendations()

        return {
            'report_type': 'compliance_report',
            'title': self.report_templates['compliance_report']['title'],
            'timestamp': datetime.now().isoformat(),
            'compliance_status': compliance_status,
            'framework_analysis': framework_analysis,
            'audit_findings': audit_findings,
            'remediation': remediation
        }

    def _analyze_underwriting_performance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze underwriting performance metrics."""
        performance = {
            'efficiency_score': 0.0,
            'quality_score': 0.0,
            'productivity_score': 0.0,
            'overall_performance': 'good'
        }

        # Calculate efficiency (processing time)
        avg_processing_time = metrics.get('average_processing_time_hours', 0)
        if avg_processing_time > 0:
            # Lower processing time = higher efficiency (normalized)
            efficiency = max(0, 1 - (avg_processing_time / 24))  # 24 hours max
            performance['efficiency_score'] = efficiency

        # Calculate quality (approval rate and accuracy)
        approval_rate = metrics.get('approval_rate', 0)
        quality = approval_rate * 0.8  # Weight approval rate
        performance['quality_score'] = quality

        # Calculate productivity (cases processed)
        total_cases = metrics.get('total_cases', 0)
        productivity = min(1.0, total_cases / 1000)  # Normalize to 1000 cases
        performance['productivity_score'] = productivity

        # Overall performance
        overall = np.mean([performance['efficiency_score'], performance['quality_score'], performance['productivity_score']])
        if overall >= 0.8:
            performance['overall_performance'] = 'excellent'
        elif overall >= 0.6:
            performance['overall_performance'] = 'good'
        elif overall >= 0.4:
            performance['overall_performance'] = 'fair'
        else:
            performance['overall_performance'] = 'poor'

        return performance

    def _analyze_underwriting_trends(self) -> Dict[str, Any]:
        """Analyze underwriting trends."""
        # Placeholder for trend analysis
        return {
            'approval_rate_trend': 'stable',
            'processing_time_trend': 'improving',
            'premium_trend': 'increasing',
            'risk_profile_trend': 'stable',
            'trend_period': 'last_30_days'
        }

    def _generate_underwriting_recommendations(self, metrics: Dict[str, Any],
                                             performance: Dict[str, Any]) -> List[str]:
        """Generate underwriting recommendations."""
        recommendations = []

        # Processing time recommendations
        avg_time = metrics.get('average_processing_time_hours', 0)
        if avg_time > 8:
            recommendations.append("Consider automation improvements to reduce processing time")
        if avg_time > 16:
            recommendations.append("Processing time significantly above average - investigate bottlenecks")

        # Approval rate recommendations
        approval_rate = metrics.get('approval_rate', 0)
        if approval_rate < 0.7:
            recommendations.append("Low approval rate - review underwriting criteria")
        if approval_rate > 0.95:
            recommendations.append("High approval rate - ensure adequate risk controls")

        # Performance-based recommendations
        if performance.get('overall_performance') == 'poor':
            recommendations.append("Overall performance needs improvement - consider process review")
        if performance.get('efficiency_score', 0) < 0.5:
            recommendations.append("Low efficiency - optimize workflow and automation")

        return recommendations

    def _analyze_portfolio_composition(self, policies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze portfolio composition."""
        if not policies:
            return {'error': 'No policy data available'}

        # Analyze by risk tier
        risk_tiers = {}
        for policy in policies:
            tier = policy.get('risk_tier', 'standard')
            risk_tiers[tier] = risk_tiers.get(tier, 0) + 1

        # Analyze by coverage type
        coverage_types = {}
        for policy in policies:
            for coverage in policy.get('coverages', []):
                coverage_type = coverage.get('coverage_type', 'unknown')
                coverage_types[coverage_type] = coverage_types.get(coverage_type, 0) + 1

        # Calculate concentration metrics
        total_policies = len(policies)
        concentration_ratio = max(risk_tiers.values()) / total_policies if total_policies > 0 else 0

        return {
            'risk_tier_distribution': risk_tiers,
            'coverage_type_distribution': coverage_types,
            'concentration_ratio': concentration_ratio,
            'diversification_score': 1 - concentration_ratio,
            'total_policies_analyzed': total_policies
        }

    def _analyze_risk_distribution(self, policies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze risk distribution in portfolio."""
        if not policies:
            return {'error': 'No policy data available'}

        # Analyze risk scores
        risk_scores = [policy.get('risk_score', 0.5) for policy in policies]
        risk_distribution = {
            'mean_risk_score': np.mean(risk_scores),
            'median_risk_score': np.median(risk_scores),
            'risk_score_std': np.std(risk_scores),
            'high_risk_policies': len([p for p in policies if p.get('risk_score', 0) > 0.7]),
            'low_risk_policies': len([p for p in policies if p.get('risk_score', 0) < 0.3])
        }

        return risk_distribution

    def _analyze_portfolio_performance(self, portfolio_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze portfolio performance."""
        performance = {
            'profitability_score': 0.0,
            'risk_adjusted_return': 0.0,
            'capital_efficiency': 0.0,
            'growth_trend': 'stable'
        }

        # Calculate basic performance metrics
        total_premium = portfolio_summary.get('total_premium', 0)
        total_policies = portfolio_summary.get('total_policies', 0)

        if total_policies > 0:
            avg_premium = total_premium / total_policies
            performance['profitability_score'] = min(1.0, avg_premium / 10000)  # Normalize to $10K

        return performance

    def _analyze_claims_trends(self, claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze claims trends."""
        if not claims:
            return {'error': 'No claims data available'}

        # Analyze claim frequency over time
        claims_by_month = {}
        for claim in claims:
            claim_date = datetime.fromisoformat(claim['reported_date'].replace('Z', '+00:00'))
            month_key = claim_date.strftime('%Y-%m')
            claims_by_month[month_key] = claims_by_month.get(month_key, 0) + 1

        # Calculate trend
        months = sorted(claims_by_month.keys())
        if len(months) >= 2:
            recent_claims = list(claims_by_month.values())[-3:]  # Last 3 months
            trend = 'increasing' if recent_claims[-1] > recent_claims[0] else 'decreasing' if recent_claims[-1] < recent_claims[0] else 'stable'
        else:
            trend = 'insufficient_data'

        return {
            'monthly_claims': claims_by_month,
            'trend': trend,
            'average_monthly_claims': np.mean(list(claims_by_month.values())),
            'total_claims_analyzed': len(claims)
        }

    def _analyze_claims_patterns(self, claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze claims patterns."""
        if not claims:
            return {'error': 'No claims data available'}

        # Analyze by claim type
        claim_types = {}
        for claim in claims:
            claim_type = claim.get('claim_type', 'unknown')
            claim_types[claim_type] = claim_types.get(claim_type, 0) + 1

        # Analyze by cause of loss
        causes = {}
        for claim in claims:
            cause = claim.get('cause_of_loss', 'unknown')
            causes[cause] = causes.get(cause, 0) + 1

        # Analyze severity distribution
        amounts = [claim.get('claimed_amount', 0) for claim in claims]
        severity_distribution = {
            'mean_amount': np.mean(amounts),
            'median_amount': np.median(amounts),
            'max_amount': np.max(amounts),
            'high_severity_count': len([a for a in amounts if a > 50000])
        }

        return {
            'claim_type_distribution': claim_types,
            'cause_distribution': causes,
            'severity_distribution': severity_distribution,
            'total_claims_analyzed': len(claims)
        }

    def _analyze_fraud_patterns(self, claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze fraud patterns in claims."""
        # Placeholder for fraud analysis
        return {
            'fraud_risk_score': 0.05,  # 5% fraud risk
            'suspicious_patterns': ['large_claims', 'quick_reporting'],
            'fraud_detection_rate': 0.8,
            'false_positive_rate': 0.1,
            'recommendations': ['Enhance fraud detection algorithms', 'Implement manual review for high-risk claims']
        }

    def _analyze_compliance_framework(self) -> Dict[str, Any]:
        """Analyze compliance framework status."""
        # Placeholder for compliance analysis
        return {
            'framework_status': 'compliant',
            'compliance_score': 0.92,
            'outstanding_issues': 2,
            'next_audit_date': (datetime.now() + timedelta(days=90)).isoformat()
        }

    def _analyze_audit_findings(self) -> Dict[str, Any]:
        """Analyze audit findings."""
        # Placeholder for audit analysis
        return {
            'total_audits': 4,
            'passed_audits': 3,
            'failed_audits': 1,
            'common_findings': ['documentation_gaps', 'process_variations'],
            'improvement_areas': ['training', 'automation', 'quality_control']
        }

    def _generate_remediation_recommendations(self) -> List[str]:
        """Generate remediation recommendations."""
        return [
            'Implement additional training for underwriting staff',
            'Enhance automated quality control checks',
            'Improve documentation standards',
            'Review and update underwriting guidelines',
            'Implement continuous monitoring and feedback loops'
        ]

    def export_report(self, report_data: Dict[str, Any], format: str = "json",
                     filename: Optional[str] = None) -> str:
        """
        Export report to file.

        Args:
            report_data: Report data to export
            format: Export format ('json', 'csv', 'pdf')
            filename: Output filename

        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"underwriting_report_{report_data.get('report_type', 'unknown')}_{timestamp}.{format}"

        if format == "json":
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
        elif format == "csv":
            # Convert to CSV format
            df = pd.DataFrame([report_data])
            df.to_csv(filename, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")

        self.logger.info(f"Report exported to {filename}")
        return filename


class ReportingEngine:
    """Advanced reporting engine with automation capabilities."""

    def __init__(self, underwriting_engine: Optional[Any] = None):
        """
        Initialize the reporting engine.

        Args:
            underwriting_engine: Underwriting engine for data access
        """
        self.underwriting_engine = underwriting_engine
        self.reporter = UnderwritingReporter(underwriting_engine)

    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate data for underwriting dashboard."""
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'kpis': {},
            'charts': {},
            'alerts': []
        }

        # Get key metrics
        if self.underwriting_engine:
            metrics = self.underwriting_engine.get_underwriting_metrics()

            dashboard_data['kpis'] = {
                'total_cases': metrics.get('total_cases', 0),
                'approval_rate': metrics.get('approval_rate', 0.0),
                'average_premium': metrics.get('average_premium', 0.0),
                'processing_time': metrics.get('average_processing_time_hours', 0.0)
            }

            # Generate alerts
            if metrics.get('approval_rate', 0) < 0.7:
                dashboard_data['alerts'].append({
                    'type': 'warning',
                    'message': 'Low approval rate detected',
                    'metric': 'approval_rate',
                    'value': metrics['approval_rate']
                })

        return dashboard_data

    def schedule_reports(self, report_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Schedule automated report generation."""
        schedule_results = {
            'scheduled_reports': [],
            'errors': [],
            'timestamp': datetime.now().isoformat()
        }

        for config in report_configs:
            try:
                report_type = config.get('report_type')
                frequency = config.get('frequency', 'weekly')
                recipients = config.get('recipients', [])

                schedule_result = {
                    'report_type': report_type,
                    'frequency': frequency,
                    'recipients': recipients,
                    'next_run': self._calculate_next_run(frequency),
                    'status': 'scheduled'
                }

                schedule_results['scheduled_reports'].append(schedule_result)

            except Exception as e:
                schedule_results['errors'].append({
                    'report_type': config.get('report_type'),
                    'error': str(e)
                })

        return schedule_results

    def _calculate_next_run(self, frequency: str) -> str:
        """Calculate next scheduled run time."""
        now = datetime.now()

        if frequency == "daily":
            next_run = now + timedelta(days=1)
        elif frequency == "weekly":
            next_run = now + timedelta(weeks=1)
        elif frequency == "monthly":
            next_run = now + timedelta(days=30)
        elif frequency == "quarterly":
            next_run = now + timedelta(days=90)
        else:
            next_run = now + timedelta(days=7)  # Default to weekly

        return next_run.isoformat()


# Convenience functions
def create_underwriting_reporter(underwriting_engine: Optional[Any] = None) -> UnderwritingReporter:
    """Create a new underwriting reporter."""
    return UnderwritingReporter(underwriting_engine)

def generate_underwriting_summary(underwriting_engine: Any) -> Dict[str, Any]:
    """Generate underwriting summary report."""
    reporter = UnderwritingReporter(underwriting_engine)
    return reporter.generate_report("underwriting_summary")

def generate_portfolio_report(underwriting_engine: Any) -> Dict[str, Any]:
    """Generate portfolio analysis report."""
    reporter = UnderwritingReporter(underwriting_engine)
    return reporter.generate_report("portfolio_analysis")

def generate_claims_report(underwriting_engine: Any) -> Dict[str, Any]:
    """Generate claims analysis report."""
    reporter = UnderwritingReporter(underwriting_engine)
    return reporter.generate_report("claims_analysis")
