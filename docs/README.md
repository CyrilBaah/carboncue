# CarbonCue Documentation

Welcome to the CarbonCue documentation! This documentation is built with MkDocs and provides comprehensive guides and API references.

## Local Development

### Build Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Serve documentation locally with auto-reload
mkdocs serve

# Build static documentation
mkdocs build
```

### Documentation Structure

```
docs/
├── index.md                    # Home page
├── getting-started/
│   ├── installation.md         # Installation guide
│   ├── quickstart.md           # Quick start tutorial
│   └── configuration.md        # Configuration options
├── guides/
│   ├── github-action.md        # GitHub Action guide
│   ├── cli.md                  # CLI usage guide
│   ├── sdk.md                  # SDK integration guide
│   └── regions.md              # Region mapping guide
├── examples/
│   ├── basic-usage.md          # Basic examples
│   ├── custom-thresholds.md    # Custom threshold examples
│   └── multi-region.md         # Multi-region examples
└── reference/                  # Auto-generated API docs
```

## Contributing to Documentation

### Writing Guidelines

- Use clear, concise language
- Include code examples for all features
- Use admonitions for warnings and notes
- Test all code examples
- Follow the existing structure

### Code Examples

All code examples should be:
- **Runnable**: Can be copy-pasted and executed
- **Complete**: Include all necessary imports
- **Explained**: Include comments where needed
- **Tested**: Verify they work before committing

### Building

Documentation is automatically generated from:
- Markdown files in `docs/`
- Docstrings in Python source code
- Type hints and annotations

## Deployment

Documentation is automatically deployed to GitHub Pages on push to main:

```yaml
# .github/workflows/docs.yml
- name: Deploy to GitHub Pages
  run: mkdocs gh-deploy --force
```

## Links

- [Live Documentation](https://carboncue.dev)
- [GitHub Repository](https://github.com/CyrilBaah/carboncue)
- [API Reference](https://carboncue.dev/reference/)


# Calculate SCI score
carboncue sci --operations 100 --materials 50 --functional-unit 1000
```

#### SDK

```python
from carboncue_sdk import CarbonClient

async with CarbonClient() as client:
    intensity = await client.get_current_intensity("us-west-2")
    print(f"Carbon: {intensity.carbon_intensity} gCO2eq/kWh")
```

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────┐
│                  CarbonCue System                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ GitHub Action│  │   CLI    │  │  Dashboard   │  │
│  └──────┬───────┘  └────┬─────┘  └──────┬───────┘  │
│         │               │               │          │
│         └───────────────┴───────────────┘          │
│                         │                          │
│                    ┌────▼─────┐                    │
│                    │   SDK    │                    │
│                    └────┬─────┘                    │
│                         │                          │
│         ┌───────────────┴───────────────┐          │
│         │                               │          │
│    ┌────▼─────────┐           ┌────────▼──────┐   │
│    │Electricity   │           │ GSF Carbon    │   │
│    │Maps API      │           │ Aware SDK     │   │
│    └──────────────┘           └───────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Request** → GitHub Action / CLI / SDK
2. **SDK** → Electricity Maps or GSF Carbon-Aware SDK
3. **API Response** → Carbon intensity data
4. **SDK** → Calculate SCI score
5. **Result** → Report to user

## API Reference

### CarbonClient

Main client for carbon-awareness operations.

```python
from carboncue_sdk import CarbonClient

client = CarbonClient(config=optional_config)
```

#### Methods

##### `get_current_intensity(region, provider)`

Get real-time carbon intensity for a region.

**Parameters:**
- `region` (str): Cloud region code (e.g., "us-west-2")
- `provider` (str): Cloud provider ("aws", "azure", "gcp", etc.)

**Returns:** `CarbonIntensity` - Current carbon data

**Example:**
```python
intensity = await client.get_current_intensity("us-west-2", "aws")
print(f"Intensity: {intensity.carbon_intensity} gCO2eq/kWh")
```

##### `calculate_sci(...)`

Calculate Software Carbon Intensity (SCI) score per GSF specification.

**Parameters:**
- `operational_emissions` (float): Energy-based emissions (gCO2eq)
- `embodied_emissions` (float): Hardware-based emissions (gCO2eq)
- `functional_unit` (float): Number of functional units
- `functional_unit_type` (str): Type of unit (default: "requests")
- `region` (str): Computation region

**Returns:** `SCIScore` - Complete SCI calculation

**Example:**
```python
sci = client.calculate_sci(
    operational_emissions=100.0,
    embodied_emissions=50.0,
    functional_unit=1000,
    functional_unit_type="requests"
)
print(f"SCI: {sci.score} gCO2eq/request")
```

### Data Models

#### CarbonIntensity

```python
@dataclass(frozen=True)
class CarbonIntensity:
    region: str
    carbon_intensity: float  # gCO2eq/kWh
    fossil_fuel_percentage: Optional[float]
    renewable_percentage: Optional[float]
    timestamp: datetime
    source: str
```

#### SCIScore

```python
@dataclass(frozen=True)
class SCIScore:
    score: float  # gCO2eq per functional unit
    operational_emissions: float
    embodied_emissions: float
    functional_unit: float
    functional_unit_type: str
    region: str
    timestamp: datetime
```

## Green Software Foundation Principles

CarbonCue implements GSF standards:

### Software Carbon Intensity (SCI)

```
SCI = (O + M) / R

Where:
  O = Operational emissions (runtime energy × carbon intensity)
  M = Embodied emissions (hardware manufacturing impact)
  R = Functional unit (requests, users, builds, etc.)
```

**Example Calculation:**

```python
# 100 gCO2eq from compute
# 50 gCO2eq from hardware amortization
# 1000 requests processed
SCI = (100 + 50) / 1000 = 0.15 gCO2eq/request
```

### Carbon-Aware Computing

Execute workloads when and where carbon intensity is lowest:

- **When**: Time-shift non-urgent workloads to low-carbon hours
- **Where**: Region-shift to locations with cleaner grids
- **What**: Scale down non-critical services during high-carbon periods

## Configuration

### Environment Variables

```bash
# Required for real-time data
export CARBONCUE_ELECTRICITY_MAPS_API_KEY=your_key

# Optional configuration
export CARBONCUE_DEFAULT_REGION=us-west-2
export CARBONCUE_DEFAULT_CLOUD_PROVIDER=aws
export CARBONCUE_CACHE_TTL_SECONDS=300
export CARBONCUE_ENABLE_CACHING=true
```

### Configuration File

Create `.carboncue.toml`:

```toml
[carboncue]
default_region = "us-west-2"
default_cloud_provider = "aws"
cache_ttl_seconds = 300

[carboncue.api]
electricity_maps_api_key = "your_key"
request_timeout = 30
max_retries = 3
```

## Best Practices

### 1. Defer Non-Critical Workloads

```yaml
- name: Carbon-Aware Deploy
  uses: carboncue/action@v1
  with:
    mode: 'defer'
    carbon-threshold: '200'
```

### 2. Time-Shift Batch Jobs

Run during low-carbon hours (often at night when renewable energy is high).

### 3. Multi-Region Deployments

Deploy to regions with lower carbon intensity:

```python
regions = ["us-west-2", "eu-north-1", "ca-central-1"]
best_region = min(
    regions,
    key=lambda r: await client.get_current_intensity(r)
)
```

### 4. Monitor and Report

Track SCI scores over time to measure improvements.

## Troubleshooting

### API Key Not Working

```bash
# Verify key is set
echo $CARBONCUE_ELECTRICITY_MAPS_API_KEY

# Test with CLI
carboncue config
```

### High Carbon Intensity Readings

- Check if region code is correct
- Verify cloud provider matches
- Compare with external sources

### Tests Failing

```bash
# Run with verbose output
pytest -v

# Check specific test
pytest tests/unit/test_client.py -v

# With coverage
pytest --cov=packages --cov-report=html
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](../LICENSE) for details.
