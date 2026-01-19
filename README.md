# CarbonCue

**Carbon-Aware GitHub Action, CLI, and SDK for sustainable software development**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI - SDK](https://img.shields.io/pypi/v/carboncue-sdk?label=SDK&color=blue)](https://pypi.org/project/carboncue-sdk/)
[![PyPI - CLI](https://img.shields.io/pypi/v/carboncue-cli?label=CLI&color=blue)](https://pypi.org/project/carboncue-cli/)
[![GitHub Action](https://img.shields.io/badge/GitHub%20Action-v1.0.0-green)](https://github.com/marketplace/actions/carboncue)
[![Tests](https://github.com/CyrilBaah/carboncue/actions/workflows/ci.yml/badge.svg)](https://github.com/CyrilBaah/carboncue/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Overview

CarbonCue helps developers measure and reduce the carbon footprint of their software by integrating carbon-awareness into development workflows. It provides real-time carbon intensity data and calculates Software Carbon Intensity (SCI) scores for cloud regions.

## Features

- 🎯 **GitHub Action** - Gate CI/CD workflows based on carbon intensity thresholds
- 💻 **CLI** - Terminal interface for carbon-aware development with real-time intensity checking
- 🔧 **SDK** - Python library for integrating carbon-awareness into applications
- ☁️ **Multi-Cloud** - Support for AWS, Azure, GCP, DigitalOcean, and more
- 📊 **SCI Calculator** - Software Carbon Intensity calculations
- 🌍 **Real-Time Data** - Live carbon intensity from Electricity Maps API

## Quick Start

### GitHub Action

Add to your workflow to gate deployments based on carbon intensity:

```yaml
name: Carbon-Aware Deployment
on: [push, pull_request]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Carbon Intensity
        uses: CyrilBaah/carboncue@v1.0.0
        with:
          region: us-west-2
          cloud-provider: aws
          threshold: 200
      
      - name: Deploy
        run: echo "Deploying with low carbon intensity!"
```

### CLI

```bash
# Install
pip install carboncue-cli

# Check current carbon intensity
carboncue check --region us-west-2 --provider aws

# Calculate SCI score
carboncue sci -o 100 -m 50 -r 1000 -t requests --region us-west-2
```

### SDK

```python
from carboncue_sdk import CarbonCueClient, SCICalculator

# Check carbon intensity
async with CarbonCueClient() as client:
    intensity = await client.get_carbon_intensity(
        region="us-west-2",
        cloud_provider="aws"
    )
    print(f"Current: {intensity.carbon_intensity} gCO2eq/kWh")

# Calculate SCI score
calculator = SCICalculator()
sci = calculator.calculate(
    operational_emissions=100,
    embodied_emissions=50,
    functional_unit=1000
)
print(f"SCI Score: {sci.score}")
```

## Architecture

```
carboncue/
├── packages/
│   ├── sdk/          # Core Python SDK (PyPI: carboncue-sdk)
│   ├── cli/          # Terminal interface (PyPI: carboncue-cli)
│   └── action/       # GitHub Action (Marketplace: carboncue)
├── tests/            # Comprehensive test suite (93% coverage)
└── docs/             # Documentation
```

## Installation

**SDK:**
```bash
pip install carboncue-sdk
```

**CLI:**
```bash
pip install carboncue-cli
```

**GitHub Action:**
```yaml
- uses: CyrilBaah/carboncue@v1.0.0
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

CarbonCue uses the Software Carbon Intensity (SCI) specification:

```
SCI = (O + M) / R

Where:
O = Operational emissions (energy × carbon intensity)
M = Embodied emissions (hardware manufacturing impact)
R = Functional unit (requests, users, transactions, etc.)
```

## Data Sources

- **Electricity Maps API** - Real-time grid carbon intensity data
- **Multi-Cloud Support** - AWS, Azure, GCP, DigitalOcean, and other providers

## Constitution Compliance

This project follows the [CarbonCue Constitution](.specify/memory/constitution.md):

- ✅ Code Quality Excellence - Clean, maintainable, production-grade code
- ✅ Testing Standards - TDD with 80%+ coverage
- ✅ UX Consistency - Intuitive interfaces across all components
- ✅ Latest Packages - Up-to-date dependencies for security
- ✅ Context7 Documentation - AI-agent friendly documentation
- ✅ Proven Libraries - Leverages Electricity Maps and established tools

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## Links

- **SDK on PyPI**: https://pypi.org/project/carboncue-sdk/
- **CLI on PyPI**: https://pypi.org/project/carboncue-cli/
- **GitHub Action**: https://github.com/marketplace/actions/carboncue
- **Documentation**: [packages/sdk](packages/sdk/), [packages/cli](packages/cli/), [packages/action](packages/action/)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.
