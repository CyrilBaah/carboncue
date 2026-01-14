# CarbonCue

**Carbon-Aware GitHub Action, CLI, Dashboard, and SDK based on Green Software Foundation (GSF) principles**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Overview

CarbonCue helps developers measure and reduce the carbon footprint of their software by integrating carbon-awareness into development workflows. Built on [Green Software Foundation](https://greensoftware.foundation/) principles, it provides real-time carbon intensity data and calculates Software Carbon Intensity (SCI) scores.

## Features

- 🎯 **GitHub Action** - Automatically calculate and report carbon savings in CI/CD pipelines
- 💻 **CLI** - Terminal interface for carbon-aware development
- 📊 **Dashboard** - Real-time grid carbon intensity and SCI score calculator
- 🔧 **SDK** - Python library for integrating carbon-awareness into applications
- 📚 **GSF-Aligned** - Follows Green Software Foundation standards and methodologies

## Quick Start

### GitHub Action (Primary Focus)

Add to your workflow:

```yaml
name: Carbon Check
on: [push, pull_request]

jobs:
  carbon-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: carboncue/action@v1
        with:
          mode: 'hybrid'
```

### CLI

```bash
# Install
pip install carboncue-cli

# Check current carbon intensity
carboncue check --region us-west-2

# Calculate SCI score
carboncue sci --provider aws --region us-west-2
```

### SDK

```python
from carboncue_sdk import CarbonClient

client = CarbonClient()
intensity = await client.get_current_intensity(region="us-west-2")
sci_score = client.calculate_sci(operations=100, materials=50, functional_unit=1000)
```

## Architecture

```
carboncue/
├── packages/
│   ├── sdk/          # Core logic (Electricity Maps, GSF Carbon-Aware SDK)
│   ├── cli/          # Terminal interface
│   └── action/       # GitHub Action wrapper
├── dashboard/        # Web UI for real-time stats
├── docs/             # GSF-style documentation
└── tests/            # Comprehensive test suite
```

## Development

```bash
# Clone repository
git clone https://github.com/CyrilBaah/carboncue.git
cd carboncue

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint and format
ruff check .
black .
mypy packages/
```

## Carbon Intensity Formula

CarbonCue uses the GSF Software Carbon Intensity (SCI) specification:

```
SCI = (O + M) / R

Where:
O = Operational emissions (energy × carbon intensity)
M = Embodied emissions (hardware manufacturing impact)
R = Functional unit (requests, users, transactions, etc.)
```

## Data Sources

- **Electricity Maps API** - Real-time grid carbon intensity
- **GSF Carbon-Aware SDK** - Carbon-aware scheduling and forecasting
- **Cloud Provider APIs** - Region-specific infrastructure data

## Constitution Compliance

This project follows the [CarbonCue Constitution](.specify/memory/constitution.md):

- ✅ Code Quality Excellence - Clean, maintainable, production-grade code
- ✅ Testing Standards - TDD with 80%+ coverage
- ✅ UX Consistency - Intuitive interfaces across all components
- ✅ Latest Packages - Up-to-date dependencies for security
- ✅ Context7 Documentation - AI-agent friendly documentation
- ✅ Existing Solutions - Leverages GSF SDK, Electricity Maps, proven libraries

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.
