# SDK Integration Guide

This guide covers advanced usage of the CarbonCue SDK for integrating carbon-awareness into your Python applications.

## Overview

The CarbonCue SDK provides:

- **Real-time carbon intensity data** from Electricity Maps
- **SCI score calculation** per GSF specification
- **Region mapping** for multi-cloud environments
- **Caching and error handling** for production use

## Installation

```bash
pip install carboncue-sdk
```

## Basic Usage

### Async Context Manager (Recommended)

```python
import asyncio
from carboncue_sdk import CarbonClient

async def main():
    async with CarbonClient() as client:
        intensity = await client.get_current_intensity(
            region="us-west-2",
            provider="aws"
        )
        print(f"Carbon Intensity: {intensity.carbon_intensity} gCO2eq/kWh")

asyncio.run(main())
```

### Manual Client Management

```python
import asyncio
from carboncue_sdk import CarbonClient

async def main():
    client = CarbonClient()
    
    # Must enter context before making API calls
    await client.__aenter__()
    
    try:
        intensity = await client.get_current_intensity("us-west-2", "aws")
        print(intensity.carbon_intensity)
    finally:
        await client.close()

asyncio.run(main())
```

## Working with Carbon Intensity

### Get Current Intensity

```python
from carboncue_sdk import CarbonClient, InvalidRegionError

async with CarbonClient() as client:
    try:
        # AWS region
        aws_intensity = await client.get_current_intensity("us-west-2", "aws")
        
        # Azure region
        azure_intensity = await client.get_current_intensity("eastus", "azure")
        
        # GCP region
        gcp_intensity = await client.get_current_intensity("us-west1", "gcp")
        
    except InvalidRegionError as e:
        print(f"Region not supported: {e}")
```

### Access Intensity Data

```python
intensity = await client.get_current_intensity("us-west-2", "aws")

print(f"Region: {intensity.region}")
print(f"Carbon Intensity: {intensity.carbon_intensity} gCO2eq/kWh")
print(f"Timestamp: {intensity.timestamp}")
print(f"Fossil Fuel %: {intensity.fossil_fuel_percentage}")
print(f"Renewable %: {intensity.renewable_percentage}")
print(f"Data Source: {intensity.source}")
```

## Calculating SCI Scores

### Basic SCI Calculation

```python
from carboncue_sdk import CarbonClient

client = CarbonClient()

# Calculate Software Carbon Intensity
# SCI = (O + M) / R
# O = Operational emissions (energy use)
# M = Embodied emissions (hardware manufacturing)
# R = Functional units (requests, users, etc.)

sci = client.calculate_sci(
    operational_emissions=100.0,   # gCO2eq
    embodied_emissions=50.0,       # gCO2eq
    functional_unit=1000,          # number of units
    functional_unit_type="requests",
    region="us-west-2"
)

print(f"SCI Score: {sci.score} gCO2eq per request")
print(f"Operational: {sci.operational_emissions} gCO2eq")
print(f"Embodied: {sci.embodied_emissions} gCO2eq")
```

### Real-World Example

```python
import asyncio
from carboncue_sdk import CarbonClient

async def calculate_api_carbon_footprint():
    """Calculate carbon footprint for an API endpoint."""
    
    async with CarbonClient() as client:
        # Get current carbon intensity
        intensity = await client.get_current_intensity("us-west-2", "aws")
        
        # API metrics
        energy_per_request = 0.0001  # kWh per request
        requests_processed = 1_000_000
        server_embodied = 1000.0  # gCO2eq from server hardware
        
        # Calculate operational emissions
        total_energy = energy_per_request * requests_processed
        operational = total_energy * intensity.carbon_intensity
        
        # Calculate SCI
        sci = client.calculate_sci(
            operational_emissions=operational,
            embodied_emissions=server_embodied,
            functional_unit=requests_processed,
            functional_unit_type="requests",
            region="us-west-2"
        )
        
        print(f"📊 API Carbon Footprint Report")
        print(f"   Region: {intensity.region}")
        print(f"   Grid Intensity: {intensity.carbon_intensity} gCO2eq/kWh")
        print(f"   Total Requests: {requests_processed:,}")
        print(f"   SCI Score: {sci.score:.6f} gCO2eq per request")
        print(f"   Total Emissions: {operational + server_embodied:.2f} gCO2eq")

asyncio.run(calculate_api_carbon_footprint())
```

## Region Mapping

### Get Zone Information

```python
from carboncue_sdk import RegionMapper, InvalidRegionError, InvalidProviderError

try:
    # Map cloud region to Electricity Maps zone
    zone_id = RegionMapper.get_zone_id("us-west-2", "aws")
    print(f"AWS us-west-2 maps to zone: {zone_id}")
    
except InvalidRegionError:
    print("Region not supported")
except InvalidProviderError:
    print("Provider not supported")
```

### List Supported Regions

```python
from carboncue_sdk import RegionMapper

# Get all AWS regions
aws_regions = RegionMapper.get_supported_regions("aws")
print(f"Supported AWS regions: {', '.join(aws_regions)}")

# Get all providers
providers = RegionMapper.get_supported_providers()
print(f"Supported providers: {', '.join(providers)}")
```

## Error Handling

### Handle All Exceptions

```python
import asyncio
from carboncue_sdk import (
    CarbonClient,
    CarbonCueError,
    APIError,
    AuthenticationError,
    RateLimitError,
    InvalidRegionError,
    InvalidProviderError,
    DataNotAvailableError
)

async def robust_carbon_check(region: str, provider: str):
    async with CarbonClient() as client:
        try:
            intensity = await client.get_current_intensity(region, provider)
            return intensity
            
        except AuthenticationError:
            print("❌ Authentication failed. Check your API key.")
            return None
            
        except InvalidRegionError as e:
            print(f"❌ Invalid region: {e}")
            return None
            
        except InvalidProviderError as e:
            print(f"❌ Invalid provider: {e}")
            return None
            
        except RateLimitError:
            print("⏸️  Rate limit exceeded. Please try again later.")
            return None
            
        except DataNotAvailableError:
            print("📊 Carbon data not available for this region.")
            return None
            
        except APIError as e:
            print(f"🌐 API error: {e}")
            return None
            
        except CarbonCueError as e:
            print(f"❌ CarbonCue error: {e}")
            return None

result = asyncio.run(robust_carbon_check("us-west-2", "aws"))
```

## Advanced Configuration

### Custom Configuration

```python
from carboncue_sdk import CarbonClient, CarbonConfig

config = CarbonConfig(
    electricity_maps_api_key="your-api-key",
    enable_caching=True,
    cache_ttl_seconds=600,  # 10 minutes
    request_timeout=60,
    max_retries=5
)

async with CarbonClient(config=config) as client:
    intensity = await client.get_current_intensity("eu-west-1", "aws")
```

### Disable Caching for Real-Time Data

```python
config = CarbonConfig(enable_caching=False)
client = CarbonClient(config=config)

# Every call fetches fresh data
async with client:
    intensity1 = await client.get_current_intensity("us-west-2", "aws")
    intensity2 = await client.get_current_intensity("us-west-2", "aws")
    # Both calls hit the API
```

## Integration Patterns

### Carbon-Aware Task Scheduling

```python
import asyncio
from carboncue_sdk import CarbonClient

async def should_run_task(threshold: float = 300.0) -> bool:
    """Determine if carbon intensity is low enough to run a task."""
    async with CarbonClient() as client:
        intensity = await client.get_current_intensity("us-west-2", "aws")
        return intensity.carbon_intensity < threshold

async def carbon_aware_task():
    """Run task only when carbon intensity is acceptable."""
    if await should_run_task(threshold=250.0):
        print("✅ Running task - carbon intensity is low")
        # Execute your task here
    else:
        print("⏸️  Deferring task - carbon intensity too high")

asyncio.run(carbon_aware_task())
```

### Multi-Region Selection

```python
import asyncio
from carboncue_sdk import CarbonClient

async def find_greenest_region(regions: list[tuple[str, str]]) -> tuple[str, float]:
    """Find the region with lowest carbon intensity."""
    async with CarbonClient() as client:
        results = []
        
        for region, provider in regions:
            try:
                intensity = await client.get_current_intensity(region, provider)
                results.append((region, intensity.carbon_intensity))
            except Exception as e:
                print(f"Skipping {region}: {e}")
        
        # Return region with lowest intensity
        return min(results, key=lambda x: x[1])

regions_to_check = [
    ("us-west-2", "aws"),
    ("us-east-1", "aws"),
    ("eu-west-1", "aws"),
]

greenest, intensity = asyncio.run(find_greenest_region(regions_to_check))
print(f"Greenest region: {greenest} ({intensity} gCO2eq/kWh)")
```

## Next Steps

- [Configuration Guide](../getting-started/configuration.md)
- [API Reference](../reference/carboncue_sdk/)
- [Examples](../examples/basic-usage.md)
