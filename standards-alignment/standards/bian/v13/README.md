# BIAN v13 Reference Set

This directory is for generated BIAN v13 reference artifacts:

- `bo-classes.md`
- `bo-classes-detail.md`
- `enumerations.md`
- `hierarchy.md`

Generate with:

```powershell
python references/industry_standards/bian/extract-references.py --version 13.0.0
```

Legacy flat files under the parent `bian/` directory may still exist during migration.
Prefer this folder for new version-aware workflows.
