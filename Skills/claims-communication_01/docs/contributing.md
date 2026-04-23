# Contributing to HealthSim Products

Thank you for contributing to HealthSim! This guide applies to all HealthSim products (PatientSim, MemberSim, RxMemberSim) and the shared healthsim-common repository.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- pip and venv

### Initial Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/[repository].git
cd [repository]

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 2. Make Changes

Write clean, well-documented code:

```python
def generate_entity(
    age_range: tuple[int, int] = (18, 85),
    gender: Optional[Gender] = None
) -> Entity:
    """Generate a synthetic entity with realistic demographics.

    Args:
        age_range: Minimum and maximum age (inclusive)
        gender: Entity gender, or None for random

    Returns:
        Entity with demographics and relevant data

    Raises:
        ValueError: If age_range is invalid

    Example:
        >>> gen = EntityGenerator(seed=42)
        >>> entity = gen.generate_entity(age_range=(60, 75))
        >>> 60 <= entity.age <= 75
        True
    """
```

### 3. Write Tests

All new code needs tests:

```python
def test_entity_generation_with_age_range():
    """Test entity generation respects age range."""
    generator = EntityGenerator(seed=42)
    entity = generator.generate_entity(age_range=(60, 70))

    assert 60 <= entity.age <= 70


def test_entity_generation_invalid_age_range():
    """Test entity generation rejects invalid age range."""
    generator = EntityGenerator()

    with pytest.raises(ValueError, match="Invalid age range"):
        generator.generate_entity(age_range=(70, 60))  # max < min
```

**Test coverage requirements:**
- New features: 90%+ coverage
- Bug fixes: Add test reproducing bug
- All tests must pass

### 4. Run Quality Checks

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/ --fix

# Type check
mypy src/

# Run all tests
pytest

# Check coverage
pytest --cov=src --cov-report=html

# Run pre-commit checks
pre-commit run --all-files
```

**All checks must pass before PR.**

### 5. Commit Changes

Follow conventional commit format:

```bash
git commit -m "feat: add new export format"
git commit -m "fix: correct validation formula"
git commit -m "docs: add developer guide for MCP tools"
git commit -m "test: add tests for transformer"
```

**Commit types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Refactoring
- `style:` - Formatting
- `chore:` - Maintenance

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create Pull Request on GitHub.

## Code Standards

### Python Style

- **Line length:** 100 characters
- **Formatter:** Black
- **Linter:** Ruff
- **Type hints:** Required for public APIs
- **Docstrings:** Google style

### Example

```python
from typing import Optional
from datetime import date

class Entity:
    """Synthetic entity with demographics and relevant data.

    Attributes:
        id: Unique identifier
        given_name: Entity's first name
        family_name: Entity's last name
        birth_date: Date of birth
        gender: Gender (M/F/O/U)
    """

    def __init__(
        self,
        id: str,
        given_name: str,
        family_name: str,
        birth_date: date,
        gender: str
    ):
        """Initialize entity.

        Args:
            id: Unique identifier
            given_name: First name
            family_name: Last name
            birth_date: Date of birth
            gender: Gender code

        Raises:
            ValueError: If gender is invalid
        """
        self.id = id
        # ... initialization

    @property
    def age(self) -> int:
        """Calculate current age from birth date.

        Returns:
            Age in years
        """
        today = date.today()
        return today.year - self.birth_date.year
```

## Testing Standards

### Test Structure

```
tests/
├── core/
│   ├── test_entity.py
│   ├── test_generator.py
│   └── test_models.py
├── formats/
│   ├── test_format1.py
│   ├── test_format2.py
│   └── test_format3.py
└── validation/
    ├── test_rules.py
    └── test_format.py
```

### Test Naming

```python
def test_feature_normal_case():
    """Test feature with typical inputs."""

def test_feature_edge_case():
    """Test feature with boundary values."""

def test_feature_invalid_input():
    """Test feature rejects invalid input."""
```

### Fixtures

```python
import pytest

@pytest.fixture
def sample_entity():
    """Provide sample entity for testing."""
    return Entity(
        id="TEST123",
        given_name="John",
        family_name="Doe",
        birth_date=date(1960, 1, 15),
        gender="M"
    )


def test_export(sample_entity):
    """Test export with sample entity."""
    transformer = Transformer()
    result = transformer.transform(sample_entity)
    assert result.id == "TEST123"
```

## Documentation Standards

### Markdown Files

- Clear headings (`#`, `##`, `###`)
- Code blocks with language tags
- Links to related docs
- Examples for all features

### Code Documentation

All public APIs need docstrings:

```python
def generate_entity(
    age_range: tuple[int, int] = (18, 85)
) -> Entity:
    """Generate synthetic entity with demographics.

    Creates an entity with realistic name, address, and relevant data
    appropriate for the specified age range.

    Args:
        age_range: Minimum and maximum age (inclusive).
                   Default (18, 85) covers adult population.

    Returns:
        Entity object with complete demographics and
        randomly generated data.

    Raises:
        ValueError: If min age > max age or ages out of range 0-120.

    Example:
        >>> gen = EntityGenerator(seed=42)
        >>> entity = gen.generate_entity(age_range=(60, 75))
        >>> print(f"{entity.full_name}, age {entity.age}")
        Robert Johnson, age 68
    """
```

## Pull Request Process

### PR Checklist

Before submitting:

- [ ] All tests pass (`pytest`)
- [ ] Code formatted (`black`)
- [ ] Linting passes (`ruff`)
- [ ] Type checking passes (`mypy`)
- [ ] Coverage ≥90% for new code
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for features/fixes)
- [ ] Examples added (if applicable)

### PR Template

```markdown
## Description

Brief description of changes.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing

How was this tested?

## Checklist

- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code formatted and linted
```

### Review Process

1. Automated checks run (CI/CD)
2. Maintainer reviews code
3. Address feedback
4. Approval and merge

## Areas of Contribution

### High Priority

- **New cohorts** (clinical, claims, pharmacy)
- **Export formats** (FHIR, HL7v2, X12, NCPDP)
- **Validation rules** (domain-specific validation)
- **Documentation** (tutorials, examples)

### Medium Priority

- **Performance improvements**
- **Additional MCP tools**
- **Test coverage improvements**
- **Example workflows**

### Welcome Contributions

- Bug reports with reproduction steps
- Documentation improvements
- Example conversations
- Use case guides

## Repository-Specific Guidelines

### healthsim-common Repository

When contributing to healthsim-common:

- **Cohorts**: Add to `skills/[product]/`
- **Formats**: Add to `formats/`
- **References**: Add to `references/`
- **Shared docs**: Add to `docs/`

### Product Repositories

When contributing to PatientSim, MemberSim, or RxMemberSim:

- **Core models**: `src/[product]/core/`
- **Formats**: `src/[product]/formats/`
- **MCP servers**: `src/[product]/mcp/`
- **Validation**: `src/[product]/validation/`

## Getting Help

### Questions

- GitHub Discussions: Ask questions
- GitHub Issues: Report bugs

### Review Requests

Tag maintainers in PR for:
- Architecture and core models
- Export formats and validation
- Documentation and examples

## Code of Conduct

### Our Standards

- **Respectful:** Treat all contributors with respect
- **Collaborative:** Help others learn and grow
- **Constructive:** Provide helpful feedback
- **Patient:** Remember everyone is learning

### Unacceptable Behavior

- Harassment, discrimination, or personal attacks
- Trolling or deliberately unhelpful comments
- Publishing others' private information
- Conduct inappropriate in a professional setting

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

Thank you for making HealthSim better!

## Next Steps

**Ready to contribute?**

1. **Pick an issue:** Check Good First Issues labels
2. **Join discussion:** Introduce yourself in Discussions
3. **Read the guides:**
   - [Architecture](HEALTHSIM-ARCHITECTURE-GUIDE.md) - System design
   - [Extension Philosophy](extensions/philosophy.md) - Adding capabilities
   - [Creating Skills](extensions/skills.md) - Add cohorts
   - [MCP Tools](extensions/mcp-tools.md) - Add MCP tools

**Questions?** Open a Discussion or ask in your PR!

---

## See Also

- [Extension Philosophy](extensions/philosophy.md) - How to extend HealthSim
- [MCP Tools Guide](extensions/mcp-tools.md) - Adding MCP tools
- [Skills Guide](extensions/skills.md) - Adding knowledge
- [Quick Reference](extensions/quick-reference.md) - Fast lookup
