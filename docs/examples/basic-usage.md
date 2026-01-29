# Basic Usage Examples

## Simple Carbon Intensity Check

The most basic use case - checking current carbon intensity:

```python
import asyncio
from carboncue_sdk import CarbonClient

async def main():
    async with CarbonClient() as client:
        intensity = await client.get_current_intensity(
            region="us-west-2",
            provider="aws"
        )
        
        print(f"🌍 Carbon Intensity Report")
        print(f"   Region: {intensity.region}")
        print(f"   Carbon: {intensity.carbon_intensity} gCO2eq/kWh")
        print(f"   Renewable: {intensity.renewable_percentage}%")
        print(f"   Fossil Fuel: {intensity.fossil_fuel_percentage}%")

asyncio.run(main())
```

**Output:**
```
🌍 Carbon Intensity Report
   Region: us-west-2
   Carbon: 285.3 gCO2eq/kWh
   Renewable: 45.2%
   Fossil Fuel: 54.8%
```

## Calculate SCI for a Web Service

Calculate the Software Carbon Intensity score for a web API:

```python
from carboncue_sdk import CarbonClient

def calculate_api_sci():
    client = CarbonClient()
    
    # Metrics from your service
    operational_emissions = 150.0  # gCO2eq from energy
    embodied_emissions = 75.0      # gCO2eq from hardware
    total_requests = 10_000        # Requests processed
    
    sci = client.calculate_sci(
        operational_emissions=operational_emissions,
        embodied_emissions=embodied_emissions,
        functional_unit=total_requests,
        functional_unit_type="requests",
        region="us-west-2"
    )
    
    print(f"📊 SCI Score: {sci.score:.6f} gCO2eq per request")
    print(f"   Total Emissions: {sci.operational_emissions + sci.embodied_emissions} gCO2eq")
    print(f"   Functional Units: {sci.functional_unit:,} {sci.functional_unit_type}")

calculate_api_sci()
```

**Output:**
```
📊 SCI Score: 0.022500 gCO2eq per request
   Total Emissions: 225.0 gCO2eq
   Functional Units: 10,000 requests
```

## Compare Multiple Regions

Find the greenest cloud region:

```python
import asyncio
from carboncue_sdk import CarbonClient

async def compare_regions():
    regions = [
        ("us-west-2", "aws"),
        ("us-east-1", "aws"),
        ("eu-west-1", "aws"),
    ]
    
    async with CarbonClient() as client:
        print("🌍 Comparing Cloud Regions\n")
        
        results = []
        for region, provider in regions:
            intensity = await client.get_current_intensity(region, provider)
            results.append((region, intensity.carbon_intensity))
            print(f"   {region}: {intensity.carbon_intensity} gCO2eq/kWh")
        
        # Find greenest
        greenest = min(results, key=lambda x: x[1])
        print(f"\n✅ Greenest region: {greenest[0]} ({greenest[1]} gCO2eq/kWh)")

asyncio.run(compare_regions())
```

## Check Multiple Providers

Compare carbon intensity across different cloud providers:

```python
import asyncio
from carboncue_sdk import CarbonClient, InvalidRegionError

async def compare_providers():
    # Similar regions across providers
    regions = [
        ("us-west-2", "aws"),      # Oregon
        ("westus2", "azure"),      # Washington
        ("us-west1", "gcp"),       # Oregon
    ]
    
    async with CarbonClient() as client:
        print("☁️  Comparing Cloud Providers (West Coast US)\n")
        
        for region, provider in regions:
            try:
                intensity = await client.get_current_intensity(region, provider)
                print(f"   {provider.upper():8} ({region:12}): {intensity.carbon_intensity:6.1f} gCO2eq/kWh")
            except InvalidRegionError:
                print(f"   {provider.upper():8} ({region:12}): Not available")

asyncio.run(compare_providers())
```

## Carbon-Aware Batch Processing

Defer batch jobs when carbon intensity is high:

```python
import asyncio
from datetime import datetime
from carboncue_sdk import CarbonClient

async def should_run_batch_job(threshold: float = 300.0) -> bool:
    """Check if we should run a batch job based on carbon intensity."""
    async with CarbonClient() as client:
        intensity = await client.get_current_intensity("us-west-2", "aws")
        
        print(f"⚡ Current carbon intensity: {intensity.carbon_intensity} gCO2eq/kWh")
        print(f"📏 Threshold: {threshold} gCO2eq/kWh")
        
        if intensity.carbon_intensity <= threshold:
            print("✅ Carbon intensity is acceptable - running job")
            return True
        else:
            print("⏸️  Carbon intensity too high - deferring job")
            return False

async def run_batch_job():
    """Execute batch job only when carbon intensity is low."""
    if await should_run_batch_job(threshold=250.0):
        print(f"🚀 Starting batch job at {datetime.now()}")
        # Your batch processing logic here
        print("✅ Batch job completed")
    else:
        print("💤 Job deferred - will retry later")

asyncio.run(run_batch_job())
```

## With Error Handling

Production-ready example with comprehensive error handling:

```python
import asyncio
from carboncue_sdk import (
    CarbonClient,
    AuthenticationError,
    RateLimitError,
    InvalidRegionError,
    DataNotAvailableError,
)

async def get_carbon_intensity_safe(region: str, provider: str = "aws"):
    """Safely get carbon intensity with error handling."""
    try:
        async with CarbonClient() as client:
            intensity = await client.get_current_intensity(region, provider)
            return {
                "success": True,
                "region": intensity.region,
                "carbon_intensity": intensity.carbon_intensity,
                "renewable_pct": intensity.renewable_percentage,
            }
    
    except AuthenticationError:
        return {
            "success": False,
            "error": "Authentication failed - check API key"
        }
    
    except InvalidRegionError as e:
        return {
            "success": False,
            "error": f"Invalid region: {e}"
        }
    
    except RateLimitError:
        return {
            "success": False,
            "error": "Rate limit exceeded - try again later"
        }
    
    except DataNotAvailableError:
        return {
            "success": False,
            "error": "Carbon data not available for this region"
        }

# Usage
result = asyncio.run(get_carbon_intensity_safe("us-west-2", "aws"))
if result["success"]:
    print(f"✅ {result['region']}: {result['carbon_intensity']} gCO2eq/kWh")
else:
    print(f"❌ Error: {result['error']}")
```

## CLI Examples

### Check Current Carbon Intensity

```bash
# Check AWS region
carboncue check --region us-west-2 --provider aws

# Check with specific API key
carboncue check --region eu-west-1 --provider aws --api-key "your-key"

# Output:
# 🌍 Carbon Intensity for us-west-2 (AWS)
#    Carbon Intensity: 285.3 gCO2eq/kWh
#    Renewable: 45.2%
#    Data Source: ElectricityMaps
```

### Calculate SCI Score

```bash
carboncue sci \
  --operational 100 \
  --embodied 50 \
  --functional-unit 1000 \
  --unit-type requests \
  --region us-west-2

# Output:
# 📊 SCI Score: 0.150000 gCO2eq per request
#    Operational: 100.0 gCO2eq
#    Embodied: 50.0 gCO2eq
#    Total: 150.0 gCO2eq
```

### List Supported Regions

```bash
# List AWS regions
carboncue regions --provider aws

# List all providers
carboncue providers
```

## Next Steps

- [Custom Thresholds Example](custom-thresholds.md)
- [Multi-Region Example](multi-region.md)
- [SDK Guide](../guides/sdk.md)
- [API Reference](../reference/carboncue_sdk/)
