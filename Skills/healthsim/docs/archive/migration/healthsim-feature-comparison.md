# HealthSim Feature Comparison: Current vs. Skills-First Architecture

This document compares features from the current Python-library HealthSim architecture against the proposed conversation-first Skills architecture.

---

## Feature Comparison Matrix

### Legend
- ✅ **Available** - Feature is fully supported
- ⚠️ **Partial** - Feature available with limitations or different approach
- ❌ **Not Available** - Feature not supported in this architecture
- 🔄 **Different** - Feature exists but implemented differently

---

## 1. Data Generation Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **Single entity generation** | ✅ `generator.generate_one()` | ✅ Claude generates directly | Claude uses SKILL.md + cohort knowledge to produce JSON |
| **Batch generation (10-100)** | ✅ `generator.generate_batch()` | ✅ Claude + iteration | Claude can generate iteratively; may be slower |
| **Large cohort generation (1000+)** | ✅ `CohortGenerator` class | ⚠️ MCP tool required | `batch_generate` MCP tool handles scale; Claude designs, tool executes |
| **Reproducibility (seed-based)** | ✅ `SeedManager` class | ⚠️ Script-based | Scripts can accept seed parameter; Claude generation is non-deterministic |
| **Weighted distributions** | ✅ `WeightedChoice` class | ⚠️ Described in cohort | Claude follows distribution guidance in cohort files; less precise |
| **Constraint satisfaction** | ✅ `CohortConstraints` class | ⚠️ Conversational | User specifies constraints in conversation; Claude attempts to satisfy |
| **Progress tracking** | ✅ `CohortProgress` callbacks | ⚠️ MCP tool only | Batch MCP tool can report progress; single generation is immediate |

**Assessment**: For typical development/testing use (tens to hundreds of entities), Skills-first is adequate. For large-scale reproducible cohorts with precise distributions, some capability is reduced unless MCP tools implement sophisticated generation logic.

---

## 2. Data Model Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **Typed data models** | ✅ Pydantic classes | 🔄 JSON schemas | Schemas in `references/canonical-model.md`; Claude follows schema |
| **Field validation** | ✅ Pydantic validators | 🔄 Script validation | `validate_*.py` scripts check structure and values |
| **Nested relationships** | ✅ Model references | ✅ JSON references | Claude generates with proper ID references |
| **Required fields** | ✅ Pydantic required | ⚠️ Schema + script | Schema documents required fields; script validates |
| **Default values** | ✅ Pydantic defaults | ⚠️ Cohort defaults | Cohorts specify typical values; Claude applies |
| **Custom types** | ✅ Custom Pydantic types | ❌ Not available | Standard JSON types only |
| **Model inheritance** | ✅ Python inheritance | ❌ Not applicable | Flat JSON structures; no inheritance concept |
| **IDE autocomplete** | ✅ Type hints | ❌ Not applicable | No code to autocomplete |

**Assessment**: Loss of Pydantic's runtime type safety and IDE support. However, for conversation-first usage, users don't interact with models directly. Validation scripts provide comparable runtime checks.

---

## 3. Validation Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **Structural validation** | ✅ `StructuralValidator` | ✅ `validate_*.py` script | Script checks required fields, types, references |
| **Clinical plausibility** | ✅ `ClinicalValidator` | ⚠️ Claude + script | Claude applies domain knowledge; script catches obvious errors |
| **Temporal consistency** | ✅ `TemporalValidator` | ✅ Script-based | Script validates event ordering, date logic |
| **Code validation (ICD, CPT)** | ✅ Reference data lookup | ⚠️ CSV + script | Scripts validate against `references/*.csv` files |
| **Age-appropriate conditions** | ✅ Clinical rules | ⚠️ Cohort knowledge | Claude applies rules from cohort files |
| **Medication-diagnosis coherence** | ✅ Clinical rules | ⚠️ Cohort knowledge | Claude uses clinical patterns in cohorts |
| **Lab value ranges** | ✅ Range validators | ⚠️ Cohort + script | Cohorts specify ranges; scripts can validate |
| **Cross-field validation** | ✅ Composite validators | ⚠️ Script logic | Scripts implement cross-field checks |
| **Validation error messages** | ✅ `ValidationResult` | ✅ Script output | Scripts return structured error messages |
| **Composable validators** | ✅ Chain validators | ⚠️ Script sequence | Run multiple scripts; less elegant |

**Assessment**: Validation capability is preserved but distributed between Claude (domain reasoning) and scripts (deterministic checks). Complex cross-field validation may require more script logic. Edge cases that Pydantic would catch at model creation time now caught later by validation scripts.

---

## 4. Output Format Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **FHIR R4 export** | ✅ `FHIRTransformer` | ✅ `export_fhir.py` | Script transforms canonical JSON to FHIR |
| **HL7v2 messages** | ✅ `HL7v2Generator` | ✅ `export_hl7v2.py` | Script generates pipe-delimited messages |
| **X12 EDI (837, 835, 834)** | ✅ `X12Transformer` | ✅ `export_x12_*.py` | Scripts for each transaction type |
| **NCPDP telecom** | ✅ `NCPDPGenerator` | ✅ `export_ncpdp.py` | Script generates NCPDP format |
| **MIMIC-III schema** | ✅ `MIMICTransformer` | ⚠️ Script + SQL | Script maps to MIMIC tables |
| **Parquet files** | ✅ DataFrame export | ✅ `export_parquet.py` | Script writes Parquet format |
| **JSON (canonical)** | ✅ Native | ✅ Native | Claude outputs JSON directly |
| **CSV export** | ✅ DataFrame export | ✅ Script or MCP | Simple transformation |
| **Custom formats** | ✅ Extend Transformer | ✅ Add new script | Create new `export_*.py` script |
| **Format validation** | ✅ Format-specific | ⚠️ External tools | Use FHIR validator, EDI parsers externally |
| **Streaming output** | ✅ Generator patterns | ❌ Not available | Scripts produce complete output |

**Assessment**: All major healthcare formats supported through scripts. Format transformation is actually well-suited to deterministic scripts. The main loss is streaming/incremental output for very large datasets.

---

## 5. Cohort & Domain Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **Pre-built clinical cohorts** | ✅ Skills + Generator | ✅ `skills/*.md` | Richer cohort descriptions possible |
| **Custom cohorts** | ✅ Create Skill + code | ✅ Create `skills/*.md` | Easier to create (markdown vs. Python) |
| **Cohort variations** | ✅ Skill variations | ✅ Documented in cohort | Claude selects appropriate variation |
| **Multi-event patient journeys** | ✅ Timeline class | ✅ Cohort event patterns | Cohorts describe event sequences |
| **Temporal progression** | ✅ Generator logic | ⚠️ Claude reasoning | Claude follows cohort timeline patterns |
| **Disease progression models** | ✅ Clinical logic | ⚠️ Cohort knowledge | Cohorts describe progression; less deterministic |
| **Quality measure alignment** | ✅ Skill guidance | ✅ Cohort guidance | Cohorts include measure-relevant data points |
| **Reference data (codes)** | ✅ Python modules | ✅ `references/*.csv` | CSV files with code lookups |
| **Clinical guidelines** | ✅ Encoded in Skills | ✅ `references/*.md` | Guidelines as readable markdown |

**Assessment**: Cohort and domain knowledge is potentially *better* in Skills-first because markdown is more expressive than code comments. Subject matter experts can contribute cohorts without Python knowledge. The tradeoff is less deterministic execution of complex disease progression models.

---

## 6. Integration & Persistence Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **Databricks export** | ✅ Native integration | ✅ CLI-based | Conversation-first: Claude generates SQL, executes via `databricks sql -e` CLI |
| **Database loading** | ✅ SQLAlchemy patterns | ✅ SQL generation | Claude generates INSERT statements; CLI or script executes |
| **File system export** | ✅ Native | ✅ Script + MCP | Scripts write files; MCP for batch |
| **API integration** | ✅ Python SDK patterns | ⚠️ MCP tools | MCP tools wrap external APIs |
| **Streaming pipelines** | ✅ Generator yields | ❌ Not available | Batch-oriented only |
| **Delta Lake support** | ✅ Native | ✅ MCP tool | Part of Databricks integration |
| **Unity Catalog** | ✅ Native | ✅ MCP tool | Part of Databricks integration |

**Assessment**: Persistence capabilities preserved through MCP tools. Streaming/pipeline patterns not available - this is a genuine limitation for enterprise ETL cohorts.

---

## 7. Developer Experience Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **IDE support** | ✅ Full (VS Code, PyCharm) | ⚠️ Markdown only | Skill files are markdown; no code completion |
| **Type checking** | ✅ mypy, pyright | ❌ Not available | No typed code |
| **Unit testing** | ✅ pytest | ⚠️ Script testing | Scripts can be unit tested |
| **Debugging** | ✅ Python debugger | ⚠️ Print/log debugging | Scripts can have debug output |
| **Documentation** | ✅ Docstrings + Sphinx | ✅ Markdown native | Skills *are* documentation |
| **Version control** | ✅ Git | ✅ Git | Markdown files version well |
| **Code review** | ✅ Standard PR flow | ✅ Standard PR flow | Markdown PRs are reviewable |
| **Dependency management** | ✅ pip/poetry | ⚠️ Minimal deps | Scripts have deps; Skills have none |
| **Package distribution** | ✅ PyPI | ⚠️ Git clone or .skill packages | Different distribution model |

**Assessment**: Traditional developer tooling (IDE, type checking, debugging) is reduced. However, the target audience is healthcare teams who may prefer readable markdown over Python code. The documentation-as-code benefit is significant.

---

## 8. Extensibility Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **Add new cohort** | ⚠️ Skill + Generator code | ✅ Add `skills/*.md` | Much easier - just write markdown |
| **Add new entity type** | ✅ New Pydantic model | 🔄 Update canonical model | Add to `canonical-model.md` schema |
| **Add new output format** | ✅ New Transformer class | ✅ Add `export_*.py` script | Create new export script |
| **Add reference data** | ✅ Update Python module | ✅ Add CSV file | Add to `references/*.csv` |
| **Add validation rule** | ✅ New Validator | ⚠️ Update script | Add logic to validation script |
| **Add MCP tool** | ✅ Add to server | ✅ Add to server | Same approach |
| **Customize generation** | ✅ Extend Generator | ⚠️ Modify cohort | Less precise control |
| **Plugin architecture** | ✅ Python imports | ❌ Not available | No plugin concept |

**Assessment**: Adding cohorts and reference data is *easier* in Skills-first. Adding validation rules or customizing generation logic is *harder* without Python extension points.

---

## 9. Operations Features

| Feature | Current (Python) | Skills-First | Notes on Skills-First Implementation |
|---------|------------------|--------------|--------------------------------------|
| **CI/CD integration** | ✅ Python test suites | ⚠️ Script tests | Scripts can run in CI; less comprehensive |
| **Monitoring/logging** | ✅ Python logging | ⚠️ Script output | Scripts can log; less structured |
| **Error handling** | ✅ Python exceptions | ⚠️ Script exit codes | Scripts return status; conversation handles errors |
| **Performance profiling** | ✅ cProfile, etc. | ⚠️ Script timing | Less visibility into performance |
| **Resource management** | ✅ Context managers | ⚠️ Script scope | Scripts manage own resources |
| **Parallel execution** | ✅ multiprocessing | ⚠️ MCP tool internal | MCP tools can parallelize internally |

**Assessment**: Operational maturity is reduced. For a development/testing tool (not production runtime), this may be acceptable.

---

## Summary: What's Gained vs. Lost

### Gained in Skills-First

| Benefit | Description |
|---------|-------------|
| **Accessibility** | Non-programmers can use, extend, and contribute |
| **Conversation-native** | Aligns with "Configuration as Conversation" vision |
| **Simpler architecture** | Fewer moving parts, easier to understand |
| **Better documentation** | Skills are self-documenting |
| **Faster cohort creation** | Markdown >> Python for domain experts |
| **Lower barrier to entry** | No pip install, no Python environment |
| **Anthropic alignment** | Follows Claude skill best practices |

### Lost in Skills-First

| Loss | Impact | Mitigation |
|------|--------|------------|
| **Reproducibility** | Non-deterministic generation | Use scripts with seeds for batch; accept variation for single |
| **Precise distributions** | Less control over statistical properties | Document distributions in cohorts; MCP tools can enforce |
| **Type safety** | No compile-time checks | Validation scripts catch errors at runtime |
| **IDE tooling** | No autocomplete, type hints | Tradeoff for accessibility |
| **Complex validation** | Hard to encode intricate rules | Keep essential rules in scripts |
| **Streaming** | No incremental processing | Batch-oriented; acceptable for testing use case |
| **Plugin architecture** | Can't extend via code | Extend via new skills/scripts |
| **Performance profiling** | Less visibility | Accept for dev/test use case |

---

## Recommendation

The Skills-first architecture is **appropriate** for HealthSim given:

1. **Primary use case is development/testing**, not production ETL
2. **Target users include clinical SMEs**, not just developers
3. **"Configuration as Conversation" is a core value proposition**
4. **Cohort creation is a frequent activity** that should be easy

The losses around reproducibility, precise distributions, and streaming are acceptable tradeoffs for the accessibility and simplicity gains.

**Key mitigations to implement:**

1. **Validation scripts must be robust** - They replace Pydantic's runtime checks
2. **MCP tools should handle scale** - Move batch/distribution logic there
3. **Seed support in scripts** - Where reproducibility matters
4. **Good error messages** - Users need clear feedback when generation fails

---

## Next Steps

1. Confirm this tradeoff analysis is acceptable
2. Design the canonical model schemas
3. Create one complete skill (PatientSim) as reference implementation
4. Build validation scripts
5. Build export scripts
6. Build MCP server for batch operations
