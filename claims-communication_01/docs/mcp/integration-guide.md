# MCP Integration for HealthSim

This document describes how to use HealthSim products (PatientSim, MemberSim, RxMemberSim) with Claude Code through the Model Context Protocol (MCP).

## Overview

HealthSim products provide MCP servers that expose generation capabilities as tools that can be used directly within Claude Code. This allows you to generate synthetic healthcare data on-demand while coding.

## Setup

### 1. Install with MCP support

```bash
cd /path/to/patientsim  # or membersim, rxmembersim
pip install -e ".[dev]"
```

The MCP SDK (`mcp>=1.0.0`) is included in the core dependencies.

### 2. Configure Claude Code

Add the MCP server to your Claude Code configuration:

**Option A: Project-level configuration** (Recommended)

Create or edit `.claude/mcp_settings.json` in your project:

```json
{
  "mcpServers": {
    "patientsim": {
      "command": "python",
      "args": [
        "-m",
        "patientsim.mcp.generation_server"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/patientsim/src"
      }
    }
  }
}
```

**Option B: Global configuration**

Edit `~/.config/claude-code/mcp_settings.json`:

```json
{
  "mcpServers": {
    "patientsim": {
      "command": "/path/to/patientsim/.venv/bin/python",
      "args": [
        "-m",
        "patientsim.mcp.generation_server"
      ]
    }
  }
}
```

### 3. Restart Claude Code

After adding the configuration, restart Claude Code to load the MCP server.

### 4. Verify Installation

In Claude Code, ask:

> "List the available PatientSim tools"

You should see the following tools:
- `generate_patient`
- `generate_cohort`
- `generate_patient_with_encounter`
- `list_cohorts`

## Available Tools

### 1. generate_patient

Generate a single synthetic patient with demographics.

**Parameters:**
- `age_min` (integer, optional): Minimum age (default: 18)
- `age_max` (integer, optional): Maximum age (default: 85)
- `gender` (string, optional): Gender - "M", "F", "O", or "U"
- `seed` (integer, optional): Random seed for reproducibility
- `format` (string, optional): Output format - "json", "fhir", or "mimic" (default: "json")

**Example:**
```text
Generate a male patient between 50 and 70 years old in FHIR format
```

**Output (json format):**
```json
{
  "mrn": "MRN001234",
  "given_name": "John",
  "family_name": "Smith",
  "full_name": "John Smith",
  "birth_date": "1970-03-15",
  "age": 54,
  "gender": "M",
  "deceased": false,
  "death_date": null
}
```

### 2. generate_cohort

Generate multiple synthetic patients (a cohort).

**Parameters:**
- `count` (integer, required): Number of patients to generate (1-1000)
- `age_min` (integer, optional): Minimum age (default: 18)
- `age_max` (integer, optional): Maximum age (default: 85)
- `gender_distribution` (object, optional): Distribution of genders as percentages
  - `M`: Percentage of male patients
  - `F`: Percentage of female patients
  - `O`: Percentage of other gender patients
  - `U`: Percentage of unknown gender patients
- `seed` (integer, optional): Random seed for reproducibility
- `format` (string, optional): Output format - "json", "fhir", or "mimic"

**Example:**
```text
Generate 100 patients with 60% female and 40% male, ages 65-85
```

**Output:**
```json
{
  "count": 100,
  "patients": [
    {
      "mrn": "MRN001234",
      "given_name": "Jane",
      "family_name": "Doe"
    }
  ]
}
```

### 3. generate_patient_with_encounter

Generate a patient with a complete encounter including admission, diagnoses, labs, and vitals.

**Parameters:**
- `age_min` (integer, optional): Minimum age
- `age_max` (integer, optional): Maximum age
- `gender` (string, optional): "M", "F", "O", or "U"
- `encounter_class` (string, optional): "I" (inpatient), "O" (outpatient), "E" (emergency), "U" (urgent)
- `num_diagnoses` (integer, optional): Number of diagnoses (default: 1-3)
- `num_labs` (integer, optional): Number of lab results (default: 3-8)
- `num_vitals` (integer, optional): Number of vital sign observations (default: 1-5)
- `seed` (integer, optional): Random seed
- `format` (string, optional): "json", "fhir", "hl7v2", or "mimic"

**Example:**
```text
Generate an inpatient sepsis patient with full encounter data in HL7v2 format
```

### 4. list_cohorts

List available cohort templates/skills.

**Parameters:** None

**Example:**
```text
List available patient cohorts
```

## Usage Examples

### Example 1: Generate Test Data for Development

```text
I'm developing a healthcare application. Can you generate 10 test patients
for me in FHIR format with ages between 30 and 60?
```

### Example 2: Create Realistic Encounter for Testing

```text
Generate an emergency department patient with sepsis, including all labs
and vitals, in HL7v2 format for interface testing
```

### Example 3: Generate MIMIC-III Research Dataset

```text
Create a cohort of 50 ICU patients in MIMIC-III format for my research project
```

### Example 4: Reproducible Data Generation

```text
Generate 3 patients with seed 42 for reproducible test data
```

### Example 5: Export and Save FHIR Bundle

```text
Generate 100 patients in FHIR format and save the bundle to patients.json
```

## Output Formats

### JSON Format
Standard PatientSim JSON with all fields included. Best for general development and testing.

### FHIR R4 Format
Full FHIR R4 resources (Patient, Encounter, Condition, Observation). Use for:
- FHIR API testing
- Interoperability testing
- Healthcare integration projects

### HL7v2 Format
Standard HL7v2 pipe-delimited messages (ADT^A01). Use for:
- Interface engine testing
- Legacy system integration
- HL7 message validation

### MIMIC-III Format
MIMIC-III database table format. Use for:
- Research projects
- Database population
- Analytics development

## Troubleshooting

### Server Not Starting

**Issue:** MCP server fails to start

**Solutions:**
1. Verify Python path in configuration is correct
2. Check that PatientSim is installed: `pip list | grep patientsim`
3. Test server manually: `python -m patientsim.mcp.generation_server`
4. Check Claude Code logs for error messages

### Tools Not Appearing

**Issue:** PatientSim tools don't show up in Claude Code

**Solutions:**
1. Restart Claude Code after configuration changes
2. Verify `mcp_settings.json` is valid JSON
3. Check file permissions on config file
4. Ensure PYTHONPATH points to correct location

### Import Errors

**Issue:** Server starts but tools fail with import errors

**Solutions:**
1. Install all dependencies: `pip install -e ".[dev]"`
2. Verify virtual environment is activated
3. Check PYTHONPATH includes `src` directory
4. Try absolute paths in configuration

### Generation Errors

**Issue:** Tool calls succeed but data generation fails

**Solutions:**
1. Check parameter values are within valid ranges
2. Verify gender codes are correct: "M", "F", "O", "U"
3. Ensure encounter_class is valid: "I", "O", "E", "U"
4. Check logs for specific error messages

## Advanced Configuration

### Environment Variables

You can configure the MCP server behavior using environment variables:

```json
{
  "mcpServers": {
    "patientsim": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "env": {
        "PYTHONPATH": "/path/to/patientsim/src",
        "PATIENTSIM_DEFAULT_LOCALE": "en_US",
        "PATIENTSIM_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Using a Virtual Environment

For production use, it's recommended to use a dedicated virtual environment:

```json
{
  "mcpServers": {
    "patientsim": {
      "command": "/path/to/patientsim/.venv/bin/python",
      "args": ["-m", "patientsim.mcp.generation_server"]
    }
  }
}
```

## See Also

- [MCP Configuration Guide](configuration.md)
- [MCP Development Guide](development-guide.md)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
