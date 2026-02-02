# Region Mapping Guide

## Overview

CarbonCue provides comprehensive region mapping for major cloud providers, allowing you to get carbon intensity data for your specific deployment regions. This guide covers how regions are mapped and how to work with them effectively.

## Supported Cloud Providers

### Amazon Web Services (AWS)

CarbonCue supports all major AWS regions with mapping to their corresponding electricity grid regions:

| AWS Region | Location | Grid Region | Typical Carbon Intensity* |
|------------|----------|-------------|---------------------------|
| `us-east-1` | N. Virginia | PJM | 250-400 gCO2eq/kWh |
| `us-east-2` | Ohio | PJM | 280-420 gCO2eq/kWh |
| `us-west-1` | N. California | CAISO | 180-300 gCO2eq/kWh |
| `us-west-2` | Oregon | BPAT | 150-250 gCO2eq/kWh |
| `eu-west-1` | Ireland | IE | 200-350 gCO2eq/kWh |
| `eu-west-2` | London | GB | 180-320 gCO2eq/kWh |
| `eu-west-3` | Paris | FR | 50-150 gCO2eq/kWh |
| `eu-central-1` | Frankfurt | DE | 250-450 gCO2eq/kWh |
| `eu-north-1` | Stockholm | SE | 30-80 gCO2eq/kWh |
| `ap-southeast-1` | Singapore | SG | 400-500 gCO2eq/kWh |
| `ap-southeast-2` | Sydney | AU-NSW | 600-800 gCO2eq/kWh |
| `ap-northeast-1` | Tokyo | JP | 450-550 gCO2eq/kWh |
| `ap-northeast-2` | Seoul | KR | 400-500 gCO2eq/kWh |
| `ap-south-1` | Mumbai | IN-WE | 700-900 gCO2eq/kWh |

*Typical ranges - actual values vary by time of day and season

### Microsoft Azure

| Azure Region | Location | Grid Region | Typical Carbon Intensity* |
|--------------|----------|-------------|---------------------------|
| `eastus` | East US | PJM | 250-400 gCO2eq/kWh |
| `eastus2` | East US 2 | PJM | 250-400 gCO2eq/kWh |
| `westus` | West US | CAISO | 180-300 gCO2eq/kWh |
| `westus2` | West US 2 | BPAT | 150-250 gCO2eq/kWh |
| `westus3` | West US 3 | CAISO | 180-300 gCO2eq/kWh |
| `centralus` | Central US | MISO | 350-500 gCO2eq/kWh |
| `northeurope` | North Europe | IE | 200-350 gCO2eq/kWh |
| `westeurope` | West Europe | NL | 250-400 gCO2eq/kWh |
| `francecentral` | France Central | FR | 50-150 gCO2eq/kWh |
| `germanywestcentral` | Germany West Central | DE | 250-450 gCO2eq/kWh |
| `norwayeast` | Norway East | NO-1 | 20-50 gCO2eq/kWh |
| `swedencentral` | Sweden Central | SE | 30-80 gCO2eq/kWh |
| `uksouth` | UK South | GB | 180-320 gCO2eq/kWh |
| `southeastasia` | Southeast Asia | SG | 400-500 gCO2eq/kWh |
| `eastasia` | East Asia | HK | 600-700 gCO2eq/kWh |
| `australiaeast` | Australia East | AU-NSW | 600-800 gCO2eq/kWh |
| `japaneast` | Japan East | JP | 450-550 gCO2eq/kWh |
| `koreacentral` | Korea Central | KR | 400-500 gCO2eq/kWh |
| `centralindia` | Central India | IN-WE | 700-900 gCO2eq/kWh |

### Google Cloud Platform (GCP)

| GCP Region | Location | Grid Region | Typical Carbon Intensity* |
|------------|----------|-------------|---------------------------|
| `us-central1` | Iowa | MISO | 350-500 gCO2eq/kWh |
| `us-east1` | South Carolina | SERC | 300-450 gCO2eq/kWh |
| `us-east4` | Northern Virginia | PJM | 250-400 gCO2eq/kWh |
| `us-west1` | Oregon | BPAT | 150-250 gCO2eq/kWh |
| `us-west2` | Los Angeles | CAISO | 180-300 gCO2eq/kWh |
| `us-west3` | Salt Lake City | PACE | 400-600 gCO2eq/kWh |
| `us-west4` | Las Vegas | NEVP | 350-500 gCO2eq/kWh |
| `europe-west1` | Belgium | BE | 200-350 gCO2eq/kWh |
| `europe-west2` | London | GB | 180-320 gCO2eq/kWh |
| `europe-west3` | Frankfurt | DE | 250-450 gCO2eq/kWh |
| `europe-west4` | Netherlands | NL | 250-400 gCO2eq/kWh |
| `europe-west6` | Zurich | CH | 100-200 gCO2eq/kWh |
| `europe-north1` | Finland | FI | 80-150 gCO2eq/kWh |
| `asia-southeast1` | Singapore | SG | 400-500 gCO2eq/kWh |
| `asia-southeast2` | Jakarta | ID | 600-800 gCO2eq/kWh |
| `asia-east1` | Taiwan | TW | 500-600 gCO2eq/kWh |
| `asia-east2` | Hong Kong | HK | 600-700 gCO2eq/kWh |
| `asia-northeast1` | Tokyo | JP | 450-550 gCO2eq/kWh |
| `asia-northeast2` | Osaka | JP | 450-550 gCO2eq/kWh |
| `asia-northeast3` | Seoul | KR | 400-500 gCO2eq/kWh |
| `asia-south1` | Mumbai | IN-WE | 700-900 gCO2eq/kWh |
| `australia-southeast1` | Sydney | AU-NSW | 600-800 gCO2eq/kWh |
| `australia-southeast2` | Melbourne | AU-VIC | 650-850 gCO2eq/kWh |

### DigitalOcean

| DigitalOcean Region | Location | Grid Region | Typical Carbon Intensity* |
|---------------------|----------|-------------|---------------------------|
| `nyc1`, `nyc3` | New York | NYISO | 200-350 gCO2eq/kWh |
| `sfo1`, `sfo2`, `sfo3` | San Francisco | CAISO | 180-300 gCO2eq/kWh |
| `tor1` | Toronto | IESO | 100-200 gCO2eq/kWh |
| `lon1` | London | GB | 180-320 gCO2eq/kWh |
| `fra1` | Frankfurt | DE | 250-450 gCO2eq/kWh |
| `ams2`, `ams3` | Amsterdam | NL | 250-400 gCO2eq/kWh |
| `sgp1` | Singapore | SG | 400-500 gCO2eq/kWh |
| `blr1` | Bangalore | IN-SO | 700-900 gCO2eq/kWh |

### Other Providers

CarbonCue also supports regions for:
- **Alibaba Cloud**: Major regions in China, Asia-Pacific, Europe, and North America
- **IBM Cloud**: Global regions mapped to local electricity grids
- **Oracle Cloud**: OCI regions with carbon intensity data
- **Linode**: Global data center locations
- **Vultr**: Worldwide presence with grid mapping

## Region Selection Best Practices

### 1. Choose Low-Carbon Regions

Prioritize regions with consistently low carbon intensity:

**Best Options:**
- **Norway** (`norwayeast`, `europe-north1`): ~20-50 gCO2eq/kWh (hydroelectric)
- **Sweden** (`eu-north-1`, `swedencentral`): ~30-80 gCO2eq/kWh (hydroelectric + nuclear)
- **France** (`eu-west-3`, `francecentral`): ~50-150 gCO2eq/kWh (nuclear)
- **Switzerland** (`europe-west6`): ~100-200 gCO2eq/kWh (hydroelectric + nuclear)
- **Canada** (`ca-central-1`, `tor1`): ~100-200 gCO2eq/kWh (hydroelectric)

**Good Options:**
- **Oregon** (`us-west-2`, `us-west1`): ~150-250 gCO2eq/kWh (hydroelectric + wind)
- **Ireland** (`eu-west-1`, `northeurope`): ~200-350 gCO2eq/kWh (wind + gas)
- **UK** (`eu-west-2`, `uksouth`): ~180-320 gCO2eq/kWh (wind + nuclear)

**Avoid When Possible:**
- **Australia** (`ap-southeast-2`): ~600-800 gCO2eq/kWh (coal-heavy)
- **India** (`ap-south-1`): ~700-900 gCO2eq/kWh (coal-heavy)
- **Germany** (`eu-central-1`): ~250-450 gCO2eq/kWh (coal + renewable mix)

### 2. Consider Time-of-Day Variations

Carbon intensity varies significantly by time of day:

```python
# Example: Check different times for optimal deployment
import carboncue_sdk as cc

client = cc.CarbonCueClient()

# Check current intensity
current = client.get_carbon_intensity('us-west-2')

# Get 24-hour forecast
forecast = client.get_carbon_forecast('us-west-2', hours=24)

# Find lowest intensity window
best_time = min(forecast, key=lambda x: x.intensity)
print(f"Best deployment time: {best_time.datetime} ({best_time.intensity} gCO2eq/kWh)")
```

### 3. Multi-Region Strategies

Implement intelligent region selection:

```python
# Find the best region among options
regions = ['us-west-2', 'eu-north-1', 'ap-southeast-2']
best_region = None
lowest_intensity = float('inf')

for region in regions:
    try:
        intensity = client.get_carbon_intensity(region)
        if intensity.value < lowest_intensity:
            lowest_intensity = intensity.value
            best_region = region
    except Exception as e:
        print(f"Error checking {region}: {e}")

print(f"Deploy to {best_region} (intensity: {lowest_intensity})")
```

## Grid Region Mapping

### Understanding Electricity Grids

Cloud regions are mapped to electricity grid operators and balancing areas:

**United States:**
- **CAISO**: California Independent System Operator
- **PJM**: Pennsylvania, Jersey, Maryland Power Pool
- **ERCOT**: Electric Reliability Council of Texas
- **MISO**: Midcontinent Independent System Operator
- **SPP**: Southwest Power Pool
- **NYISO**: New York Independent System Operator
- **ISO-NE**: ISO New England

**Europe:**
- **GB**: Great Britain electricity grid
- **DE**: Germany electricity grid
- **FR**: France electricity grid
- **NL**: Netherlands electricity grid
- **NO**: Norway electricity grid
- **SE**: Sweden electricity grid

**Asia-Pacific:**
- **JP**: Japan electricity grid
- **AU-NSW**: New South Wales, Australia
- **AU-VIC**: Victoria, Australia
- **SG**: Singapore electricity grid
- **HK**: Hong Kong electricity grid

### Grid Characteristics

Different grids have different carbon profiles:

**Low Carbon Grids:**
- **Hydroelectric dominant**: Norway, Sweden (partial), Quebec
- **Nuclear dominant**: France, Ontario
- **Renewable mix**: Denmark, Germany (renewable hours)

**Moderate Carbon Grids:**
- **Gas dominant**: UK, Netherlands, parts of US
- **Mixed sources**: California, Texas (renewable + gas)

**High Carbon Grids:**
- **Coal dominant**: Poland, Australia, India, China
- **Coal + gas**: Germany (peak hours), parts of US Midwest

## Using Region Data

### CLI Usage

```bash
# List all supported regions
carboncue regions

# Filter by provider
carboncue regions --provider aws

# Check specific region
carboncue check --region us-west-2

# Compare multiple regions
for region in us-east-1 us-west-2 eu-west-1; do
    echo "Region: $region"
    carboncue check --region $region
    echo
done
```

### SDK Usage

```python
import carboncue_sdk as cc

client = cc.CarbonCueClient()

# Get all supported regions
regions = client.get_supported_regions()

# Filter by provider
aws_regions = [r for r in regions if r.provider == 'aws']

# Get region details
region_info = client.get_region_info('us-west-2')
print(f"Grid: {region_info.grid_region}")
print(f"Location: {region_info.location}")
print(f"Provider: {region_info.provider}")
```

### GitHub Action Usage

```yaml
# Use environment-specific regions
- name: Set Region
  id: set-region
  run: |
    if [ "${{ github.ref }}" == "refs/heads/main" ]; then
      echo "region=eu-north-1" >> $GITHUB_OUTPUT  # Low carbon for production
    else
      echo "region=us-east-1" >> $GITHUB_OUTPUT   # Closer for development
    fi

- name: Carbon Check
  uses: CyrilBaah/carboncue@v1
  with:
    region: ${{ steps.set-region.outputs.region }}
    threshold: 300
```

## Custom Region Mapping

For private cloud or edge deployments, you can add custom region mappings:

```python
# Custom region mapping
custom_regions = {
    'my-edge-1': {
        'grid_region': 'CAISO',
        'location': 'Custom Edge Location',
        'provider': 'custom'
    }
}

client = cc.CarbonCueClient(custom_regions=custom_regions)
```

## Region Availability

### Real-Time Data

Most regions have real-time carbon intensity data updated every 5-15 minutes.

**High Frequency Updates (5-10 min):**
- United States (all grids)
- United Kingdom
- Germany
- France
- Australia (NEM)

**Medium Frequency Updates (15-30 min):**
- Scandinavia
- Netherlands
- Most of Europe

**Lower Frequency Updates (1-6 hours):**
- Some Asian markets
- Emerging markets
- Smaller grids

### Forecast Data

24-48 hour forecasts are available for most regions:
- US: All major grids
- Europe: Most countries
- Australia: NEM regions
- Asia: Major markets

## Troubleshooting

### Region Not Found

```bash
Error: Region 'invalid-region' not found
```

Use `carboncue regions` to see valid regions or check provider documentation.

### No Data Available

```bash
Warning: No carbon intensity data available for region 'new-region'
```

This can happen with:
- Newly launched cloud regions
- Regions in countries without grid data
- Temporary API outages

### Mapping Issues

If you notice incorrect region mapping:
1. Check the grid operator for your cloud region
2. Verify the electricity market/zone
3. Report issues via GitHub or support channels

The region mapping is continuously updated as cloud providers add new regions and electricity market data becomes available.
