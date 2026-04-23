# Agent
: utils

## Scope
 This directory contains utils components for the module. It provides 14 classes and 12 functions.

## Classes
 and Functions

### ComplianceFramework
 Compliance framework enumeration.

### ComplianceStatus
 Compliance status enumeration.

### RegulatoryRequirement
 Regulatory requirement structure.

**Methods**:
- `is_applicable(context: Dict[str, Any]) -> bool`: Check if requirement is applicable.
- `to_dict() -> Dict[str, Any]`: Convert requirement to dictionary.

### ComplianceCheck
 Compliance check result.

**Methods**:
- `to_dict() -> Dict[str, Any]`: Convert check to dictionary.

### ComplianceEngine
 compliance engine for regulatory adherence.

**Methods**:
- `perform_compliance_check(entity_id: str, context: Dict[str, Any]) -> Dict[str, Any]`: Perform compliance check for entity.
- `generate_compliance_report(entity_id: str, period: str) -> Dict[str, Any]`: Generate compliance report for entity.
- `add_requirement(requirement: RegulatoryRequirement) -> bool`: Add regulatory requirement.
- `remove_requirement(requirement_id: str) -> bool`: Remove regulatory requirement.
- `get_compliance_status(entity_id: str) -> Dict[str, Any]`: Get compliance status for entity.
- `get_framework_requirements() -> List[Dict[str, Any]]`: Get all requirements for current framework.
- `set_framework(framework: ComplianceFramework) -> None`: Set compliance framework.
- `health_check() -> Dict[str, Any]`: Perform health check on compliance engine.

### RegulatoryFramework
 Regulatory framework management.

**Methods**:
- `get_framework_info(framework: ComplianceFramework) -> Dict[str, Any]`: Get framework information.
- `get_all_frameworks() -> Dict[str, Dict[str, Any]]`: Get all framework definitions.

### ExternalDataSource
 External data source configuration.

**Methods**:
- `get_cache_key() -> str`: Generate cache key for this data source.

### DataIntegrationManager
 Manager for external data source integration.

**Methods**:
- `get_data(source_name: str, query_parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]`: Get data from external source.
- `add_data_source(source: ExternalDataSource) -> bool`: Add data source.
- `remove_data_source(source_name: str) -> bool`: Remove data source.
- `get_data_source_info(source_name: str) -> Optional[Dict[str, Any]]`: Get information about data source.
- `clear_cache(source_name: Optional[str]) -> None`: Clear data cache.
- `get_cache_info() -> Dict[str, Any]`: Get cache information.
- `health_check() -> Dict[str, Any]`: Perform health check on data integration.
- `close_connections() -> None`: Close any open connections.

### ReportConfig
 Configuration for reporting operations.

### UnderwritingReporter
 reporting for underwriting operations.

**Methods**:
- `generate_report(report_type: str, config: Optional[ReportConfig]) -> Dict[str, Any]`: Generate underwriting report.
- `export_report(report_data: Dict[str, Any], format: str, filename: Optional[str]) -> str`: Export report to file.

### ReportingEngine
 reporting engine with automation capabilities.

**Methods**:
- `generate_dashboard_data() -> Dict[str, Any]`: Generate data for underwriting dashboard.
- `schedule_reports(report_configs: List[Dict[str, Any]]) -> Dict[str, Any]`: Schedule automated report generation.

### ValidationResult
 Validation result structure.

### UnderwritingValidator
 validator for underwriting operations.

**Methods**:
- `validate_application(application_data: Dict[str, Any]) -> ValidationResult`: Validate underwriting application data.
- `validate_policy(policy_data: Dict[str, Any]) -> ValidationResult`: Validate policy data.
- `validate_claim(claim_data: Dict[str, Any]) -> ValidationResult`: Validate claim data.
- `health_check() -> Dict[str, Any]`: Perform health check on validator.

### PolicyValidator
 Specialized validator for policy operations.

**Methods**:
- `validate_policy_renewal(current_policy: Dict[str, Any], renewal_data: Dict[str, Any]) -> ValidationResult`: Validate policy renewal.
- `validate_policy_endorsement(policy: Dict[str, Any], endorsement: Dict[str, Any]) -> ValidationResult`: Validate policy endorsement.

### create_compliance_engine
 `create_compliance_engine(framework: ComplianceFramework) -> ComplianceEngine` Create a compliance engine.

### check_policy_compliance
 `check_policy_compliance(policy_data: Dict[str, Any], framework: ComplianceFramework) -> Dict[str, Any]` Check policy compliance with regulatory framework.

### create_data_integration_manager
 `create_data_integration_manager(data_sources: List[str]) -> DataIntegrationManager` Create a data integration manager.

### get_credit_score
 `get_credit_score(ssn: str, data_manager: DataIntegrationManager) -> Optional[int]` Get credit score from external credit bureau.

### get_property_history
 `get_property_history(property_id: str, data_manager: DataIntegrationManager) -> Optional[Dict[str, Any]]` Get property history from external database.

### create_underwriting_reporter
 `create_underwriting_reporter(underwriting_engine: Optional[Any]) -> UnderwritingReporter` Create a underwriting reporter.

### generate_underwriting_summary
 `generate_underwriting_summary(underwriting_engine: Any) -> Dict[str, Any]` Generate underwriting summary report.

### generate_portfolio_report
 `generate_portfolio_report(underwriting_engine: Any) -> Dict[str, Any]` Generate portfolio analysis report.

### generate_claims_report
 `generate_claims_report(underwriting_engine: Any) -> Dict[str, Any]` Generate claims analysis report.

### validate_underwriting_application
 `validate_underwriting_application(application_data: Dict[str, Any]) -> ValidationResult` Validate underwriting application data.

### validate_policy_data
 `validate_policy_data(policy_data: Dict[str, Any]) -> ValidationResult` Validate policy data.

### validate_claim_data
 `validate_claim_data(claim_data: Dict[str, Any]) -> ValidationResult` Validate claim data.

## Capabilities

- **14 classes** for core functionality
- **12 functions** for utility operations

## Integration

- **Location**: `src/geo_infer_risk/underwriting/utils`
- **Type**: Directory Node
