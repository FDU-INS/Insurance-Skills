---
name: norvidize
description: Extract and audit claims for norvid tracking system
---

# Norvidize Skill

<<<<<<< HEAD
Extract claims from documentation, code, and tests into a claim tracking system
based on multicomputational irreducibility -- claims that cannot be reduced to
simpler forms without losing verification guarantees.
=======
Extract claims from documentation, code, and tests into the norvid claim tracking system.
>>>>>>> origin/main

## When to Use

- After completing a significant feature
- When auditing documentation accuracy
- Before releases to ensure claims match reality
- When docs/tests/specs diverge from implementation

<<<<<<< HEAD
=======
## Claim Registry Location

```
crates/basin-norvid/src/claims.rs
```

>>>>>>> origin/main
## Assurance Levels (lowest to highest)

| Level | Meaning | Evidence Required |
|-------|---------|-------------------|
| Mentioned | Just referenced somewhere | Any doc |
<<<<<<< HEAD
| Designed | Has design doc | Design markdown |
| Specified | Has formal spec | Spec file |
| Implemented | Code exists | Source file + symbol |
| Tested | Has passing tests | Test file + test name |
| Proven | Has formal proof | Proof file + theorem |
=======
| Designed | Has design doc | docs/design/*.md |
| Specified | Has sigil spec | *.sigil file |
| Implemented | Code exists | Rust file + symbol |
| Tested | Has passing tests | Test file + test name |
| Proven | Has Lean proof | Lean file + theorem |
>>>>>>> origin/main

## Claim Categories

- **Feature**: User-visible functionality
- **Property**: System guarantee (linearizability, durability)
- **Guarantee**: Promise to users
- **Optimization**: Performance improvement
- **Invariant**: Internal system invariant
- **Decision**: Architectural choice with rationale
- **Omission**: Deliberate non-feature

<<<<<<< HEAD
## Covariant Claim Structure

Claims form a presheaf over the assurance poset: higher assurance levels
pull back evidence from lower levels. A Tested claim covariantly transports
its Designed evidence forward.

```
Mentioned -> Designed -> Specified -> Implemented -> Tested -> Proven
```

Each arrow preserves evidence (covariant functor from assurance levels to evidence sets).
=======
## Evidence Types

```rust
// Documentation
Evidence::doc("docs/CLAIMS.md")

// Rust implementation
Evidence::rust("crates/foo/src/bar.rs", "SymbolName")

// Test file
Evidence::test("crates/foo/src/bar.rs", "test_prefix")

// Sigil specification
Evidence::sigil("sigil/specs/foo.sigil")

// External (benchmark, paper)
Evidence::external("benchmarks/harnesses/redis/src/main.rs")
```

## Adding Claims

```rust
registry.register(
    Claim::new("CLM_UNIQUE_ID", "Short description")
        .with_category(Category::Feature)
        .with_component(Component::Slate)
        .with_assurance(Assurance::Implemented)
        .with_evidence(Assurance::Designed, Evidence::doc("docs/design/foo.md"))
        .with_evidence(Assurance::Implemented, Evidence::rust("crates/slate/src/lib.rs", "FooStruct"))
);
```
>>>>>>> origin/main

## Extraction Process

### 1. Find Candidate Claims

<<<<<<< HEAD
Scan sources for claim candidates:

```bash
grep -r "CLAIM\|GUARANTEE\|INVARIANT" docs/
grep -r "#\[test\]" -A 2 src/ | grep "fn test_"
grep -r "ops/s\|latency\|throughput" docs/
```

### 2. Categorize by Irreducibility

- **Irreducible claims**: Cannot be verified by simpler means (need full test execution)
- **Reducible claims**: Can be statically verified (type checking, linting)
- **Compositional claims**: Verified by composing sub-claim verifications

### 3. Verify Evidence Paths

Before adding at Tested/Implemented level, verify paths exist.

### 4. Downgrade Strategy

If evidence path is uncertain, downgrade assurance level.
Upgrade later when evidence is confirmed.

## Anti-Patterns

- Don't add Tested claims without verifying paths
- Don't skip Designed level -- even Tested claims should have design evidence
- Don't guess component names
=======
Scan these sources for claim candidates:

```bash
# Explicit claims in docs
grep -r "CLM-\|CLAIM\|GUARANTEE\|INVARIANT" docs/

# Test names suggest guarantees
grep -r "#\[test\]" -A 2 crates/ | grep "fn test_"

# Performance claims
grep -r "ops/s\|latency\|throughput" docs/

# Sigil specs
find sigil/ -name "*.sigil" -exec grep -l "claim\|invariant\|property" {} \;
```

### 2. Categorize and Deduplicate

Group into tiers:
- **Tier 1 (SPEC_*)**: Claims with sigil specs - highest value
- **Tier 2 (TEST_*)**: Claims with test evidence
- **Tier 3**: Design-level claims (docs only)

### 3. Verify Evidence Paths

Before adding at Tested/Implemented level, verify paths exist:

```bash
# Check file exists
test -f "crates/basin-redis/src/crdt.rs" && echo "OK"

# Check symbol exists
grep -l "EntityStore" crates/basin-meta/src/indexes/*.rs
```

### 4. Add to Registry

Add claims to `claims.rs` in appropriate section:
- SPEC_* claims near line 1720
- TEST_* claims after specs
- PERF_* claims in performance section
- Product claims (CLM_STASH, etc.) with products

## CI Verification

The CI test filters claims at Tested/Proven level and verifies:
1. Evidence file exists
2. Symbol/test found in file

```bash
# Run verification
graft test -p basin-norvid test_all_claims_verified
```

## Common Path Mappings

| Old/Wrong Path | Correct Path |
|----------------|--------------|
| `crates/stash/` | `crates/basin-redis/` |
| `crates/shelf/` | `crates/basin-mesh/` or `crates/spool-core/` |
| `crates/basin-jepsen/` | `tests/basin-jepsen/` |
| `products/nfs/tests/` | `crates/nfs/tests/` |

## Downgrade Strategy

If evidence path is uncertain, downgrade to Designed level:

```rust
// Was Tested but can't verify path
.with_assurance(Assurance::Designed)
.with_evidence(Assurance::Designed, Evidence::doc("docs/CLAIMS.md"))
```

Upgrade later when evidence is confirmed.

## Parallel Audit Pattern

For bulk verification, spawn sonnet agents:

```
Task: Audit PERF_* claims
- Check benchmark files exist
- Verify they actually measure what claim says
- Report which claims have valid evidence

Task: Audit product claims (CLM_STASH, etc.)
- Find actual test locations
- Verify symbol names
- Report path corrections needed
```

## Anti-Patterns

- **Don't add Tested claims without verifying paths** - CI will fail
- **Don't embed large values in claim IDs** - Keep IDs short like `CLM_STASH`
- **Don't skip Designed level** - Even Tested claims should have design evidence
- **Don't guess component names** - Check `Component` enum in identity.rs

## Quick Reference

```bash
# Find existing claims
grep -n "Claim::new" crates/basin-norvid/src/claims.rs | head -20

# Check CI status
graft test -p basin-norvid test_all_claims_verified 2>&1 | grep -E "FAILED|passed"

# Find test files for a crate
find crates/basin-meta -name "*.rs" -exec grep -l "#\[test\]" {} \;

# Count claims by category
grep -E "Category::" crates/basin-norvid/src/claims.rs | sort | uniq -c
```
>>>>>>> origin/main
