# GEO-INFER-RISK: Agent Capabilities

<div align="center">
  <h3><a href="../README.md">🌍 GEO-INFER Core</a></h3>
  <a href="../AGENTS.md">🤖 Agent Architecture</a> •
  <a href="../README.md#-module-overview">📦 Module Index</a> •
  <a href="./README.md">📚 Module Documentation</a>
</div>

---

## Overview

The **GEO-INFER-RISK** module provides risk assessment capabilities for agents, enabling hazard identification, vulnerability analysis, and risk modeling in geospatial contexts.

## Agent Capabilities

### 1. Hazard Assessment

```python
from geo_infer_risk import HazardAssessor

# Assess natural hazards
assessor = HazardAssessor()

hazards = assessor.assess(
    area=study_region,
    hazard_types=["flood", "earthquake", "wildfire"],
    return_periods=[10, 50, 100, 500])

print(f"Flood zones: {hazards.flood.zone_areas}")
print(f"Seismic hazard: {hazards.earthquake.pga}")```

### 2. Vulnerability Analysis

```python
from geo_infer_risk import VulnerabilityAnalyzer

# Analyze asset vulnerability
vuln = VulnerabilityAnalyzer()

analysis = vuln.analyze(
    assets=building_footprints,
    hazards=hazard_layers,
    factors=["age", "construction", "occupancy"])

print(f"High vulnerability: {analysis.high_risk_count}")
print(f"Estimated loss: ${analysis.expected_loss}M")```

### 3. Risk Modeling

```python
from geo_infer_risk import RiskModeler

# Model risk scenarios
modeler = RiskModeler()

risk = modeler.model(
    hazard=earthquake_scenario,
    exposure=building_inventory,
    vulnerability=fragility_curves)

print(f"Expected casualties: {risk.casualties}")
print(f"Economic loss: ${risk.economic_loss}B")```

### 4. Mitigation Planning

```python
from geo_infer_risk import MitigationPlanner

# Plan risk mitigation
planner = MitigationPlanner()

plan = planner.create(
    risks=identified_risks,
    strategies=["retrofit", "relocation", "insurance"],
    budget=100_000_000)

print(f"Risk reduction: {plan.risk_reduction}%")
print(f"ROI: {plan.benefit_cost_ratio}")```

## Implementation Status

| Feature | Status | Description |
|---------|--------|-------------|
| **Hazard** | ✅ Ready | Multi-hazard assessment |
| **Vulnerability** | ✅ Ready | Asset analysis |
| **Risk Model** | ✅ Ready | Loss estimation |
| **Mitigation** | ✅ Ready | Strategy planning |

### Aspirational Features

- 🔮 **RiskAdvisorAgent**: Autonomous risk guidance
- 🔮 **EarlyWarningAgent**: Real-time alerts

---

This AGENTS.md documents how GEO-INFER-RISK provides risk capabilities for agents.

**Last Updated**: 2026-02-25

**Claude Skill**: See [SKILL.md](./SKILL.md) for quick-reference API examples and integration map.
