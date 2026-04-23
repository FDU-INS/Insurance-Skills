# BIAN (Banking Industry Architecture Network) - Standard Guidance

## Overview

Use BIAN Business Object Model (BOM) references when modelling banking domains.
For MD-DDL mapping, focus on Business Objects and Enumerations.
Do not cite Service Domain API pages as entity references.

This directory now supports side-by-side BIAN versions:

Version | Purpose | Path
--- | --- | ---
v13 | Current production mapping baseline | `v13/`
v14 | Planned default when source snapshots are available | `v14/`

## Version Selection Rules

1. Use v13 for current modelling until v14 snapshots are published and extracted.
2. Use v14 only when required raw snapshots and generated references are available.
3. If a model is sensitive to release semantics, state the version in notes.
4. Keep MD-DDL reference URLs version-agnostic unless strict version specificity is required.

Recommended reference URL style in model outputs:

- `https://bian-modelapi-v4.azurewebsites.net/BOClassByName/{ExactBianName}`

Use version-scoped endpoints only during lookup or extraction workflows.

## Local Reference Files

Each version folder should contain generated indexes:

- `bo-classes.md`
- `bo-classes-detail.md`
- `enumerations.md`
- `hierarchy.md`

Use local files first. API lookup is fallback for unresolved details only.

## Deterministic Lookup Process

1. Pick target BIAN version (v13 default — see Version Selection Rules above).
2. Search `v{n}/bo-classes.md` for exact/near class candidates.
3. Validate inheritance and attributes in `v{n}/bo-classes-detail.md` when available.
4. Use `v{n}/hierarchy.md` to verify taxonomy context.
5. If still unresolved, use API fallback with explicit version:
   - `GET https://bian-modelapi-v4.azurewebsites.net/BOClassByName/{ExactBianName}/BIAN/{version}`
6. For enums, resolve with `v{n}/enumerations.md` first, then optional API fallback:
   - `GET https://bian-modelapi-v4.azurewebsites.net/BOEnumerationByName/{ExactEnumName}/BIAN/{version}`

## Mapping Quality Rules

Signal | Action
--- | ---
Exact semantic fit | Reference directly
Specialisation of BIAN concept | Reference parent and note specialisation
Partial overlap | Reference with explicit qualification (`Partial alignment`)
No convincing counterpart | Leave blank or use `# TODO: No BIAN BOM mapping confirmed yet`

Never fabricate URLs. If unresolved, say unresolved.

## Party / PartyRole Pattern

Critical BIAN pattern:

- Party = subject identity (person or organisation)
- PartyRole = business capacity (customer, merchant, payer, etc.)

Use this split when role lifecycle, ownership, or governance differs from identity.

## Generation Workflow

Raw source datasets live under:

- `references/industry_standards/bian/v13/`
- `references/industry_standards/bian/v14/`

Record provenance in:

- `references/industry_standards/bian/source-manifest.md`

Acquire or refresh raw snapshots first:

```powershell
powershell -ExecutionPolicy Bypass -File .\references\industry_standards\bian\download-snapshots.ps1 -Version 14.0.0
```

Generate references:

```powershell
python references/industry_standards/bian/extract-references.py --version 14.0.0
python references/industry_standards/bian/extract-references.py --version 14.0.0 --fetch-classes
python references/industry_standards/bian/extract-references.py --version 13.0.0
```

Use `--output-mode flat` only for legacy compatibility tasks.

Availability note (2026-03-08): `bian-modelapi-v4` currently exposes empty list
payloads for `BIAN/14.0.0` across required BOM list endpoints. Keep v13
references active for production alignment until v14 snapshots are populated.

## Resources

- [BIAN Website](https://bian.org)
- [BIAN Public GitHub Releases](https://github.com/bian-official/public)
- [BIAN Model API](https://bian-modelapi-v4.azurewebsites.net/)
