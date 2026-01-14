# Contributing to CarbonCue

Thank you for your interest in contributing to CarbonCue! This guide will help you get started.

## Code of Conduct

Be respectful, inclusive, and collaborative. We're all working towards reducing software carbon emissions.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- pip

### Getting Started

```bash
# Clone repository
git clone https://github.com/CyrilBaah/carboncue.git
cd carboncue

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## Constitution Compliance

All contributions MUST adhere to the [CarbonCue Constitution](.specify/memory/constitution.md). Key principles:

### I. Code Quality Excellence (NON-NEGOTIABLE)
- Clean, readable, production-grade code
- Follow Python idioms and PEP 8
- No magic numbers, unused imports, or commented-out code
- Functions should be single-purpose (<50 lines)

### II. Testing Standards (NON-NEGOTIABLE)
- **Write tests FIRST** (Test-Driven Development)
- All features require tests before implementation
- Minimum 80% code coverage
- Unit + integration + contract tests

### III. Latest Package Versions
- Use latest stable versions of all dependencies
- Update within 30 days for security patches
- Document any version constraints

### IV. Context7 Documentation
- Update documentation with code changes
- Include examples and use cases
- Document non-obvious decisions

### V. Prefer Existing Solutions
- Search for existing libraries before writing custom code
- Justify any custom implementations
- Reuse code within the project

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b 042-feature-description
```

Branch naming: `###-feature-description` (e.g., `001-electricity-maps-integration`)

### 2. Write Tests First (TDD)

```python
# tests/unit/test_new_feature.py
def test_new_feature():
    """Test description."""
    # Arrange
    client = CarbonClient()

    # Act
    result = client.new_feature()

    # Assert
    assert result.is_valid()
```

Run and verify tests fail:
```bash
pytest tests/unit/test_new_feature.py
```

### 3. Implement Feature

Only after tests are written and failing, implement the feature:

```python
# packages/sdk/src/carboncue_sdk/client.py
def new_feature(self) -> Result:
    """Implementation."""
    pass
```

### 4. Verify Tests Pass

```bash
pytest tests/unit/test_new_feature.py
```

### 5. Code Quality Checks

```bash
# Lint
ruff check .

# Format
black .

# Type check
mypy packages/

# Full test suite
pytest
```

### 6. Commit Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add electricity maps integration

- Implement real-time carbon intensity API
- Add caching layer with 5-minute TTL
- Include comprehensive tests (unit + integration)
- Update documentation with usage examples

Refs: #42"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `test:` - Adding tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `chore:` - Maintenance tasks

### 7. Push and Create Pull Request

```bash
git push origin 042-feature-description
```

Create a pull request on GitHub with:
- Clear title and description
- Reference to related issues
- Testing evidence
- Constitution compliance checklist

## Pull Request Checklist

Before submitting, verify:

- [ ] **Tests written first** (TDD followed)
- [ ] **All tests passing** (pytest)
- [ ] **Code coverage ≥ 80%** (pytest --cov)
- [ ] **Linting passed** (ruff check)
- [ ] **Formatting correct** (black)
- [ ] **Type hints added** (mypy)
- [ ] **Documentation updated** (README, docstrings)
- [ ] **Dependencies up-to-date** (latest stable versions)
- [ ] **No custom code** where libraries exist
- [ ] **Constitution compliance verified**

## Testing Guidelines

### Test Structure

```
tests/
├── unit/              # Fast, isolated tests
├── integration/       # API and system tests
└── contract/          # Data model contracts
```

### Running Tests

```bash
# All tests
pytest

# Specific category
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/

# With coverage
pytest --cov=packages --cov-report=html

# Specific test
pytest tests/unit/test_client.py::test_calculate_sci
```

### Writing Good Tests

```python
def test_feature_scenario() -> None:
    """Test <specific scenario> <expected outcome>.

    Given <initial state>
    When <action>
    Then <expected result>
    """
    # Arrange
    setup_code()

    # Act
    result = function_under_test()

    # Assert
    assert result == expected
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use docstrings (Google style)

```python
def calculate_sci(
    operational_emissions: float,
    embodied_emissions: float,
    functional_unit: float,
) -> SCIScore:
    """Calculate Software Carbon Intensity score.

    Args:
        operational_emissions: Energy-based emissions in gCO2eq
        embodied_emissions: Hardware-based emissions in gCO2eq
        functional_unit: Number of functional units

    Returns:
        Calculated SCI score with breakdown

    Raises:
        ValueError: If functional_unit <= 0
    """
    if functional_unit <= 0:
        raise ValueError("Functional unit must be positive")

    return SCIScore(
        score=(operational_emissions + embodied_emissions) / functional_unit,
        operational_emissions=operational_emissions,
        embodied_emissions=embodied_emissions,
        functional_unit=functional_unit,
    )
```

## Documentation

Update documentation for all changes:

- **README.md** - User-facing changes
- **Docstrings** - All public APIs
- **Examples** - Working code samples
- **CHANGELOG.md** - Version history

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release branch: `release/v1.2.3`
4. Run full test suite
5. Create GitHub release with notes
6. Build and publish to PyPI

## Questions?

- Open an issue for bugs or feature requests
- Join discussions for questions
- Review existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
