# Changelog

All notable changes to the CarbonCue project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-19

### Added

#### CarbonCue SDK (`carboncue-sdk`)
- Core Python SDK for carbon-aware computing
- `CarbonCueClient` for querying carbon intensity data
- `SCICalculator` for Software Carbon Intensity calculations
- Multi-cloud provider support (AWS, Azure, GCP, DigitalOcean, and others)
- Integration with Electricity Maps API
- Async/await support with httpx
- Comprehensive data models with Pydantic
- Configuration management via environment variables
- Full test coverage (unit, integration, and contract tests)

#### CarbonCue CLI (`carboncue-cli`)
- Terminal interface for carbon-aware development
- `carboncue check` - Real-time carbon intensity checker for cloud regions
- `carboncue sci` - SCI score calculator with detailed breakdowns
- `carboncue config` - Configuration viewer
- Beautiful rich terminal output with color-coded status indicators
- Multi-cloud support (AWS, Azure, GCP, DigitalOcean, others)
- Environment configuration via `.env` files
- Smart recommendations based on carbon intensity levels
- Async operations with loading indicators

#### CarbonCue GitHub Action (`carboncue`)
- GitHub Action for carbon-aware CI/CD workflows
- Check carbon intensity before running workflows
- Gate deployments based on carbon intensity thresholds
- Multi-cloud region support
- JSON output mode for advanced workflows
- Composite action architecture

### Documentation
- Comprehensive README files for SDK, CLI, and Action
- Contributing guidelines (CONTRIBUTING.md)
- MIT License
- Package-specific changelogs
- API documentation and usage examples

### Infrastructure
- Unified GitHub Actions publish workflow
- Tag-based publishing (`sdk-v*`, `cli-v*`, `v*`, `v*-all`)
- Automated PyPI publishing for SDK and CLI
- Automated GitHub Marketplace publishing for Action
- CI workflow with automated testing
- 93% test coverage across the project

## [Unreleased]

### Planned
- Additional cloud provider support
- Historical carbon data trends
- Carbon budgeting features
- Webhook integrations
- Dashboard UI

---

**Legend:**
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities
