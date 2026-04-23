# PopulationSim v2.0 - Sessions 5-8 Super-Prompt
## Cross-Product Integration with Embedded Data

**Version**: 1.0  
**Created**: 2024-12-23  
**Status**: Ready for Execution

---

## Pre-Flight Checklist

- [ ] Sessions 1-4 complete (verified by audit)
- [ ] Smoke tests pass (37/37)
- [ ] Data package accessible at `skills/populationsim/data/`
- [ ] Git working tree clean

---

## Session 5: PatientSim Integration

### Objective
Update PatientSim skills to use real population data for demographics, condition prevalence, and SDOH factors.

### Files to Update

1. **skills/patientsim/SKILL.md**
   - Add "PopulationSim Data Integration" section
   - Add trigger phrases for data-driven patient generation
   - Reference embedded data package

2. **Create: skills/patientsim/data-integration.md** (NEW)
   - Pattern for generating patients from real demographic data
   - CDC PLACES condition prevalence integration
   - SVI/ADI-driven SDOH factor assignment

3. **Update existing skills** with data lookup patterns:
   - diabetes-management.md - Use PLACES diabetes prevalence
   - heart-failure.md - Use PLACES CHD prevalence
   - behavioral-health.md - Use PLACES depression prevalence
   - chronic-kidney-disease.md - Use PLACES CKD prevalence

### Integration Pattern

```markdown
## PopulationSim Data Integration

When generating patients for [condition], use PopulationSim embedded data:

1. **Location Selection**: Query `data/county/places_county_2024.csv` for [condition] prevalence
2. **Demographics**: Use `data/county/svi_county_2022.csv` for race/ethnicity distribution
3. **SDOH Factors**: Query `data/tract/svi_tract_2022.csv` for vulnerability indicators
4. **Condition Assignment**: Weight by PLACES prevalence rates

### Example Data Lookup
```
County: Harris County, TX (FIPS: 48201)
Diabetes Prevalence: 13.2% (crude), 12.1% (age-adjusted)
SVI Overall: 0.633 (high vulnerability)
```
```

### Deliverables
- [ ] SKILL.md updated with data integration section
- [ ] data-integration.md created (new skill)
- [ ] 4 condition skills updated with PLACES references
- [ ] Test: Generate 3 sample patients using data-driven approach

---

## Session 6: MemberSim + RxMemberSim Integration

### Objective
Update claims generation to use real demographics and prevalence data.

### Files to Update

**MemberSim:**
1. **skills/membersim/SKILL.md**
   - Add "PopulationSim Data Integration" section
   - Risk stratification based on real SVI data

2. **skills/membersim/enrollment-eligibility.md**
   - Generate member demographics from tract-level data
   - Plan selection influenced by SVI economic indicators

3. **skills/membersim/value-based-care.md**
   - Risk adjustment using real prevalence data
   - Quality measure benchmarks from PLACES

**RxMemberSim:**
4. **skills/rxmembersim/SKILL.md**
   - Add "PopulationSim Data Integration" section

5. **skills/rxmembersim/retail-pharmacy.md**
   - Adherence patterns influenced by ADI
   - Geographic access based on tract data

### Deliverables
- [ ] MemberSim SKILL.md updated
- [ ] 2 MemberSim skills updated
- [ ] RxMemberSim SKILL.md updated
- [ ] 1 RxMemberSim skill updated
- [ ] Test: Generate member with data-driven demographics

---

## Session 7: TrialSim Integration

### Objective
Update trial site selection and recruitment to use real population data.

### Files to Update

1. **skills/trialsim/SKILL.md**
   - Add "PopulationSim Data Integration" section
   - Site feasibility using real demographics

2. **skills/trialsim/recruitment-enrollment.md**
   - Enrollment projections from PLACES prevalence
   - Diversity planning from SVI demographics

3. **skills/trialsim/domains/demographics-dm.md**
   - Generate DM domain data from real distributions

4. **skills/populationsim/trial-support/site-feasibility.md**
   - Ensure bidirectional integration pattern

### Deliverables
- [ ] TrialSim SKILL.md updated
- [ ] recruitment-enrollment.md updated
- [ ] demographics-dm.md updated
- [ ] Trial support skills verified
- [ ] Test: Site feasibility query with real data

---

## Session 8: Documentation + Examples

### Objective
Update hello-healthsim and architecture docs with data-first approach.

### Files to Update

1. **hello-healthsim/examples/populationsim-examples.md**
   - Add data-first generation examples
   - Cross-product integration examples

2. **hello-healthsim/examples/cross-domain-examples.md**
   - Add PopulationSim → PatientSim flow
   - Add PopulationSim → MemberSim flow
   - Add PopulationSim → TrialSim flow

3. **hello-healthsim/populationsim/** (existing files)
   - Update with v2.0 data package references
   - Add embedded data lookup examples

4. **docs/HEALTHSIM-ARCHITECTURE-GUIDE.md**
   - Add PopulationSim v2.0 data architecture section
   - Update data flow diagrams

5. **Update smoke_test.py**
   - Add PopulationSim data package tests
   - Add cross-product integration tests

### Deliverables
- [ ] populationsim-examples.md updated
- [ ] cross-domain-examples.md updated
- [ ] hello-healthsim/populationsim/* updated
- [ ] Architecture guide updated
- [ ] Smoke test extended
- [ ] All tests pass

---

## Quality Gates (Between Each Session)

### 1. Audit Checklist
- [ ] All planned files created/updated
- [ ] YAML frontmatter present in all skills
- [ ] Data lookup patterns consistent
- [ ] Cross-references resolve

### 2. Test Execution
- [ ] Run smoke_test.py
- [ ] Verify no regressions
- [ ] Test new functionality manually

### 3. Documentation
- [ ] CHANGELOG.md updated
- [ ] Affected READMEs updated
- [ ] Roadmap audit updated

### 4. Commit & Sync
- [ ] Stage changes
- [ ] Commit with descriptive message
- [ ] Push to origin

---

## Post-Flight Checklist (After All Sessions)

- [ ] All 4 sessions complete
- [ ] Smoke tests pass (extended)
- [ ] CHANGELOG comprehensive
- [ ] Roadmap audit shows all sessions complete
- [ ] Git history clean with meaningful commits
