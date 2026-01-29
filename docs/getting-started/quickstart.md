# Quick Start Guide

This guide will walk you through your first carbon-aware workflow using CarbonCue.

## SDK Quick Start

!!! info "API Key Requirement"
    - ✅ **SCI calculations** work without an API key
    - ⚠️ **Carbon intensity checks** require an API key from [Electricity Maps](https://www.electricitymap.org/)
    
    Set your API key: `export CARBONCUE_ELECTRICITY_MAPS_API_KEY="your-key"`

### Calculate SCI Score (No API Key Needed)

```python
from carboncue_sdk import CarbonClient

def calculate_software_carbon_intensity():
    # ✅ No API key needed for SCI calculations
    client = CarbonClient()
    
    # Calculate SCI score
    # SCI = (Operational + Embodied) / Functional Units
    sci = client.calculate_sci(
        operational_emissions=100.0,  # gCO2eq from energy use
        embodied_emissions=50.0,      # gCO2eq from hardware
        functional_unit=1000,          # Number of requests
        functional_unit_type="requests",
        region="us-west-2"
    )
    
    print(f"SCI Score: {sci.score:.4f} gCO2eq per request")
    print(f"Total Emissions: {sci.operational_emissions + sci.embodied_emissions} gCO2eq")

calculate_software_carbon_intensity()
```

### Basic Carbon Intensity Check (Requires API Key)

```python
import asyncio
from carboncue_sdk import CarbonClient

async def check_carbon_intensity():
    # ⚠️ Requires CARBONCUE_ELECTRICITY_MAPS_API_KEY environment variable
    async with CarbonClient() as client:
        # Get current carbon intensity for AWS us-west-2
        intensity = await client.get_current_intensity(
            region="us-west-2",
            provider="aws"
        )
        
        print(f"Region: {intensity.region}")
        print(f"Carbon Intensity: {intensity.carbon_intensity} gCO2eq/kWh")
        print(f"Renewable: {intensity.renewable_percentage}%")
        print(f"Data Source: {intensity.source}")

asyncio.run(check_carbon_intensity())
```

calculate_software_carbon_intensity()
```

### Custom Configuration

```python
from carboncue_sdk import CarbonClient, CarbonConfig

# Custom configuration
config = CarbonConfig(
    electricity_maps_api_key="your-key-here",
    enable_caching=True,
    cache_ttl_seconds=600,  # 10 minutes
    request_timeout=30
)

async with CarbonClient(config=config) as client:
    intensity = await client.get_current_intensity("eu-west-1", "aws")
    print(f"EU West Carbon Intensity: {intensity.carbon_intensity}")
```

## CLI Quick Start

### Check Current Carbon Intensity

```bash
# Check AWS region
carboncue check --region us-west-2 --provider aws

# Check Azure region
carboncue check --region eastus --provider azure

# Check GCP region
carboncue check --region us-west1 --provider gcp
```

### Calculate SCI Score

```bash
carboncue sci \
  --operational 100 \
  --embodied 50 \
  --functional-unit 1000 \
  --unit-type requests \
  --region us-west-2
```

### List Supported Regions

```bash
# List all AWS regions
carboncue regions --provider aws

# List all providers
carboncue providers
```

## GitHub Action Quick Start

### Basic Workflow

Create `.github/workflows/carbon-aware.yml`:

```yaml
name: Carbon-Aware CI

on: [push, pull_request]

jobs:
  carbon-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Carbon Intensity
        uses: CyrilBaah/carboncue@v1.0.0
        env:
          CARBONCUE_ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}
        with:
          region: us-west-2
          cloud-provider: aws
          threshold: 300
      
      - name: Run Tests (Carbon-Aware)
        run: |
          npm test
```

### Defer on High Carbon

This workflow will fail if carbon intensity is too high:

```yaml
name: Carbon-Aware Deployment

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Carbon Before Deploy
        uses: CyrilBaah/carboncue@v1.0.0
        env:
          CARBONCUE_ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}
        with:
          region: us-west-2
          cloud-provider: aws
          threshold: 250
          fail-on-threshold: true
      
      - name: Deploy to Production
        run: |
          echo "Deploying with low carbon intensity"
          # Your deployment commands
```

## Error Handling

### SDK

```python
import asyncio
from carboncue_sdk import (
    CarbonClient,
    InvalidRegionError,
    AuthenticationError,
    RateLimitError
)

async def robust_carbon_check():
    async with CarbonClient() as client:
        try:
            intensity = await client.get_current_intensity(
                region="us-west-2",
                provider="aws"
            )
            print(f"Success: {intensity.carbon_intensity} gCO2eq/kWh")
        
        except AuthenticationError:
            print("Error: Invalid or missing API key")
        
        except InvalidRegionError as e:
            print(f"Error: {e}")
        
        except RateLimitError:
            print("Error: API rate limit exceeded, try again later")

asyncio.run(robust_carbon_check())
```

## Next Steps

- [Configuration Guide](configuration.md) - Detailed configuration options
- [SDK Guide](../guides/sdk.md) - Advanced SDK usage
- [CLI Guide](../guides/cli.md) - CLI command reference
- [GitHub Action Guide](../guides/github-action.md) - Action configuration
- [API Reference](../reference/carboncue_sdk/) - Complete API documentation
