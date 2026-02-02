# Changelog

All notable changes to the CarbonCue project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-29

### Added

#### Real Electricity Maps API Integration ⚡
- **Complete API integration** replacing mock data with real-time carbon intensity from Electricity Maps
- `RegionMapper` utility for mapping cloud regions to Electricity Maps zones
  - Support for 54 regions across 4 cloud providers (AWS, Azure, GCP, DigitalOcean)
  - Automatic region-to-zone translation (e.g., `us-west-2` → `US-NW-PACW`)
- Comprehensive error handling with custom exceptions:
  - `InvalidRegionError` - Invalid cloud region specified
  - `InvalidProviderError` - Invalid cloud provider specified
  - `AuthenticationError` - API authentication failures
  - `RateLimitError` - API rate limit handling
  - `DataNotAvailableError` - Missing data for specific regions
  - `APIError` - General API communication errors
- HTTP client improvements:
  - Proper status code handling (401, 404, 429, 500)
  - Configurable request timeout and retry logic
  - Response caching with configurable TTL (default: 5 minutes)

#### Professional Documentation with MkDocs 📚
- **Complete documentation site** using MkDocs with Material theme
- Auto-generated API reference from Python docstrings using mkdocstrings
- Comprehensive guides:
  - Installation guide with multiple installation methods
  - Quick start tutorial with SDK, CLI, and GitHub Action examples
  - Configuration reference with all environment variables
  - SDK integration guide with advanced patterns
  - 15+ complete, runnable code examples
- Documentation features:
  - Beautiful Material theme with light/dark mode toggle
  - Full-text search functionality
  - Syntax highlighting with copy-to-clipboard
  - Responsive navigation
  - Code annotations and admonitions
- Documentation structure:
  - Getting Started section (installation, quickstart, configuration)
  - User Guides (SDK, CLI, GitHub Action, region mapping)
  - API Reference (auto-generated)
  - Examples (basic usage, custom thresholds, multi-region)
- Makefile targets: `make docs-serve`, `make docs-build`, `make docs-deploy`

### Changed

- **SDK Client** (`CarbonClient.get_current_intensity()`):
  - Now fetches real data from Electricity Maps API instead of returning mock values
  - Returns `source="ElectricityMaps"` instead of `source="mock"`
  - Requires `CARBONCUE_ELECTRICITY_MAPS_API_KEY` environment variable
- Updated `CarbonIntensity` model to include real fossil fuel and renewable percentages
- Enhanced test suite with 17 comprehensive unit tests for SDK client
- Test coverage increased to **92%** (up from 93% - more comprehensive testing)

### Fixed

- Error handling logic for distinguishing between invalid regions and invalid providers
- Cache key generation for proper cache isolation between regions/providers

### Infrastructure

- Added `docs` optional dependency group in `pyproject.toml`
- New dependencies: `mkdocs`, `mkdocs-material`, `mkdocstrings[python]`, `mkdocs-gen-files`
- Created 10 new files for API integration and documentation
- Updated 6 existing files with improved functionality

### Documentation Files Added

- `mkdocs.yml` - MkDocs configuration
- `docs/index.md` - Documentation home page
- `docs/gen_ref_pages.py` - API reference generator
- `docs/getting-started/installation.md`
- `docs/getting-started/quickstart.md`
- `docs/getting-started/configuration.md`
- `docs/guides/sdk.md`
- `docs/examples/basic-usage.md`
- `IMPLEMENTATION_SUMMARY.md` - Implementation details

### Breaking Changes

⚠️ **API Key Required for Real Carbon Data**: The `get_current_intensity()` method now requires a valid Electricity Maps API key. Set `CARBONCUE_ELECTRICITY_MAPS_API_KEY` environment variable or it will raise `AuthenticationError`.

**Note:** This only affects real-time carbon intensity fetching. Other features work without an API key:
- ✅ `calculate_sci()` - SCI score calculation (no API key needed)
- ✅ `RegionMapper` utilities (no API key needed)
- ❌ `get_current_intensity()` - **Requires API key**

### Migration Guide

**If you ONLY use `calculate_sci()`:** No changes needed! Your code works exactly the same.

```python
# ✅ Works without API key (v1.0.0 and v1.1.0)
client = CarbonClient()
sci = client.calculate_sci(
    operational_emissions=100.0,
    embodied_emissions=50.0,
    functional_unit=1000
)
```

**If you use `get_current_intensity()`:** You now need an API key for real data.

**Before (v1.0.0):**
```python
async with CarbonClient() as client:
    intensity = await client.get_current_intensity("us-west-2", "aws")
    # Returned mock data without API key
```

**After (v1.1.0):**
```bash
# Set API key first (get free key from electricitymap.org)
export CARBONCUE_ELECTRICITY_MAPS_API_KEY="your-api-key-here"
```

```python
async with CarbonClient() as client:
    intensity = await client.get_current_intensity("us-west-2", "aws")
    # Returns real data from Electricity Maps ✨
    # intensity.source == "ElectricityMaps"
```

### Acknowledgments

This release brings CarbonCue from a well-structured prototype to a production-ready tool with real carbon data and professional documentation. Special thanks to the Electricity Maps team for providing the carbon intensity API.

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
