# BIAN v14 Reference Set

This directory is for generated BIAN v14 reference artifacts:

- `bo-classes.md`
- `bo-classes-detail.md`
- `enumerations.md`
- `hierarchy.md`

Generate with:

```powershell
python references/industry_standards/bian/extract-references.py --version 14.0.0
python references/industry_standards/bian/extract-references.py --version 14.0.0 --fetch-classes
```

Use this version by default for new modelling work.
