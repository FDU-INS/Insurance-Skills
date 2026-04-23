---
name: t81_policy_checker
description: Check Axion policy compliance for T81 operations and decisions
metadata:
  openclaw:
    os: ["darwin", "linux"]
    requires:
      bins: ["t81"]
---

# T81 Policy Checker Skill

This skill evaluates Axion policies for T81 operations, providing deterministic policy validation and compliance checking.

## Usage

When the user needs to validate operations against T81's Axion governance policies, use this skill to perform policy evaluation.

### Commands

**Check policy compliance:**
```
check <operation> <resource> [--policy <policy_file>] [--context <context_file>]
```

**Validate policy syntax:**
```
validate-policy <policy_file> [--strict]
```

**Test policy rules:**
```
test-rule <policy_file> <rule_name> [--test-data <data_file>]
```

**List available policies:**
```
list-policies [--canonfs-root <path>]
```

**Simulate policy decision:**
```
simulate <operation> <resource> [--policy <policy_file>] [--dry-run]
```

### Examples

```bash
# Check if import operation is allowed
check import model.t81w --policy security.apl

# Validate policy file syntax
validate-policy ./policies/secure_model.apl --strict

# Test specific rule with test data
test-rule security.apl allow_model_import --test-data test_cases.json

# List all policies in CanonFS
list-policies --canonfs-root ~/.t81_canonfs

# Simulate policy decision without execution
simulate inference neural_net.t81w --policy inference.apl --dry-run
```

### Policy Operations

**Supported Operations:**
- `import` - Import files into CanonFS
- `export` - Export files from CanonFS  
- `execute` - Run T81VM operations
- `inference` - Perform AI inference
- `bundle_create` - Create decision bundles
- `bundle_consume` - Consume decision bundles

**Policy Context:**
Policy evaluation can include context from:
- User identity and permissions
- Resource metadata and hashes
- Temporal constraints and conditions
- Environment variables and system state

### Output Format

**Policy Allow:**
```json
{
  "decision": "allow",
  "operation": "import",
  "resource": "model.t81w",
  "policy": "security.apl",
  "reason": "approved_model_hash",
  "timestamp": "2026-04-04T15:30:00Z",
  "policy_hash": "CanonHash81..."
}
```

**Policy Deny:**
```json
{
  "decision": "deny",
  "operation": "execute", 
  "resource": "untrusted_code.tisc",
  "policy": "security.apl",
  "reason": "unapproved_code_hash",
  "timestamp": "2026-04-04T15:30:00Z",
  "policy_hash": "CanonHash81...",
  "suggestions": [
    "Get code approved through security review",
    "Use approved code from trusted repository"
  ]
}
```

### Policy Language Features

**Axion Policy Syntax:**
```apl
# Allow model inference for approved hashes
allow inference if model.hash in approved_models;

# Deny execution during maintenance windows
deny execute if time in maintenance_hours;

# Conditional resource access
allow export if user.role in ["admin", "auditor"] 
          and resource.classification <= "secret";
```

**Policy Evaluation:**
- Deterministic rule evaluation
- No runtime ambiguity or heuristics
- Complete audit trail for decisions
- Cryptographic policy verification

### Error Handling

- Clear error messages for policy syntax issues
- Detailed explanations for policy denials
- Suggestions for policy remediation
- Validation of policy file integrity

### Security Notes

- Policy files are stored immutably in CanonFS
- Policy evaluation is deterministic and reproducible
- All policy decisions are logged for audit
- Policy changes require proper governance

### Integration

This skill wraps T81's Axion policy engine and provides standardized access to policy validation APIs.
