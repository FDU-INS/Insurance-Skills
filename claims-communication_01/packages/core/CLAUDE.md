# HealthSim Core - Claude Context

This package provides the shared Python foundation for the HealthSim product family.

## Package Structure

```
packages/core/
├── src/healthsim/         # Source code
│   ├── __init__.py        # Package exports
│   ├── person.py          # Person entity model
│   ├── generation.py      # Faker-based generators
│   ├── formats.py         # Output format utilities
│   ├── validation.py      # Validation rules
│   ├── temporal.py        # Date/time utilities
│   ├── config.py          # Configuration management
│   ├── benefits/          # Benefits processing
│   │   └── accumulators.py
│   ├── dimensional/       # Star schema transformers
│   │   ├── base.py
│   │   ├── dim_date.py
│   │   └── duckdb_writer.py
│   └── state/             # State management
│       ├── entity.py
│       ├── session.py
│       ├── workspace.py
│       └── provenance.py
├── tests/                 # Test suite (476 tests)
└── pyproject.toml         # Package configuration
```

## Key Exports

- `Person` - Base person entity with demographics
- `generate_person()` - Create realistic synthetic persons
- `BenefitAccumulator` - Track deductibles, OOP, etc.
- `DimensionalTransformer` - Star schema conversion
- `Session`, `Workspace` - State management

## Testing

```bash
cd packages/core
pytest  # 476 tests
```

## Dependencies

- faker - Realistic data generation
- pydantic - Data validation
- duckdb - Embedded analytics
- pandas - Data manipulation

## Related Packages

- `packages/patientsim/` - Clinical simulation
- `packages/membersim/` - Claims simulation
- `packages/rxmembersim/` - Pharmacy simulation
