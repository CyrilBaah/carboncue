# Configuration

CarbonCue can be configured through environment variables, configuration files, or programmatically.

## API Key Requirement

**Important:** The API key is only required if you use `get_current_intensity()` to fetch real-time carbon data.

**Works without API key:**
- `calculate_sci()` - SCI score calculations
- `RegionMapper` utilities - Region mapping
- All model classes

**Requires API key:**
- `get_current_intensity()` - Real-time carbon intensity data

If you try to use `get_current_intensity()` without an API key, you'll get: `AuthenticationError: "Electricity Maps API key not configured."`

## Environment Variables

All configuration options can be set via environment variables with the `CARBONCUE_` prefix:

| Variable | Description | Default |
|----------|-------------|---------|
| `CARBONCUE_ELECTRICITY_MAPS_API_KEY` | Electricity Maps API key (required for `get_current_intensity()`) | None |
| `CARBONCUE_ELECTRICITY_MAPS_BASE_URL` | API base URL | `https://api.electricitymap.org/v3` |
| `CARBONCUE_DEFAULT_REGION` | Default cloud region | `us-west-2` |
| `CARBONCUE_DEFAULT_CLOUD_PROVIDER` | Default cloud provider | `aws` |
| `CARBONCUE_REQUEST_TIMEOUT` | HTTP request timeout (seconds) | `30` |
| `CARBONCUE_MAX_RETRIES` | Maximum API retry attempts | `3` |
| `CARBONCUE_CACHE_TTL_SECONDS` | Cache time-to-live (seconds) | `300` (5 min) |
| `CARBONCUE_ENABLE_CACHING` | Enable response caching | `true` |

### Setting Environment Variables

=== "Linux/macOS"

    ```bash
    export CARBONCUE_ELECTRICITY_MAPS_API_KEY="your-key"
    export CARBONCUE_CACHE_TTL_SECONDS=600
    export CARBONCUE_ENABLE_CACHING=true
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:CARBONCUE_ELECTRICITY_MAPS_API_KEY="your-key"
    $env:CARBONCUE_CACHE_TTL_SECONDS=600
    ```

=== ".env File"

    Create a `.env` file in your project root:

    ```bash
    CARBONCUE_ELECTRICITY_MAPS_API_KEY=your-key-here
    CARBONCUE_CACHE_TTL_SECONDS=600
    CARBONCUE_ENABLE_CACHING=true
    CARBONCUE_DEFAULT_REGION=eu-west-1
    CARBONCUE_DEFAULT_CLOUD_PROVIDER=aws
    ```

## Programmatic Configuration

### SDK Configuration

```python
from carboncue_sdk import CarbonClient, CarbonConfig

# Create custom configuration
config = CarbonConfig(
    electricity_maps_api_key="your-api-key",
    electricity_maps_base_url="https://api.electricitymap.org/v3",
    default_region="eu-west-1",
    default_cloud_provider="azure",
    request_timeout=60,
    max_retries=5,
    cache_ttl_seconds=600,  # 10 minutes
    enable_caching=True
)

# Use configuration
async with CarbonClient(config=config) as client:
    intensity = await client.get_current_intensity("eastus", "azure")
```

### Load from .env File

```python
from carboncue_sdk import CarbonClient, CarbonConfig
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Config will automatically read from environment
client = CarbonClient()
```

## Cloud Provider Configuration

### Supported Providers

CarbonCue supports the following cloud providers:

- **AWS** (Amazon Web Services)
- **Azure** (Microsoft Azure)
- **GCP** (Google Cloud Platform)
- **DigitalOcean**

### Region Mapping

Each cloud provider region is mapped to an Electricity Maps zone. For example:

```python
from carboncue_sdk import RegionMapper

# Get zone for AWS region
zone = RegionMapper.get_zone_id("us-west-2", "aws")
print(zone)  # US-NW-PACW

# Get all supported AWS regions
regions = RegionMapper.get_supported_regions("aws")
print(regions)

# Get all supported providers
providers = RegionMapper.get_supported_providers()
print(providers)
```

See the [Region Mapping Guide](../guides/regions.md) for complete region lists.

## Caching Configuration

### Enable/Disable Caching

```python
from carboncue_sdk import CarbonConfig

# Disable caching for real-time data
config = CarbonConfig(enable_caching=False)

# Enable with custom TTL
config = CarbonConfig(
    enable_caching=True,
    cache_ttl_seconds=300  # 5 minutes
)
```

### Cache Behavior

- Cache keys are based on `provider:region`
- Cached values expire after `cache_ttl_seconds`
- Cache is in-memory and cleared when client is closed
- Useful for reducing API calls and costs

## Error Handling Configuration

### Retry Configuration

```python
config = CarbonConfig(
    max_retries=5,           # Retry failed requests up to 5 times
    request_timeout=45       # 45 second timeout per request
)
```

### Timeout Behavior

- Default timeout: 30 seconds
- Applies to each HTTP request
- Adjust based on your network conditions

## GitHub Action Configuration

Configure the action through workflow inputs:

```yaml
- uses: CyrilBaah/carboncue@v1.0.0
  env:
    CARBONCUE_ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}
  with:
    region: us-west-2
    cloud-provider: aws
    threshold: 300
    fail-on-threshold: true
    cache-enabled: true
```

## CLI Configuration

CLI reads from environment variables or accepts flags:

```bash
# Using environment variables
export CARBONCUE_ELECTRICITY_MAPS_API_KEY="your-key"
carboncue check --region us-west-2

# Using flags
carboncue check \
  --region us-west-2 \
  --provider aws \
  --api-key "your-key"
```

## Best Practices

### API Key Security

!!! warning "Never commit API keys"
    - Use environment variables or secrets management
    - Don't hardcode keys in source code
    - Use GitHub Secrets for Actions

### Caching Strategy

- **Enable caching** for batch jobs and scheduled tasks
- **Disable caching** for real-time monitoring
- Adjust TTL based on how fresh data needs to be

### Region Selection

- Choose regions closest to your users
- Consider regions with higher renewable energy
- Use region mapping to understand grid zones

## Next Steps

- [Quick Start Guide](quickstart.md)
- [SDK Integration Guide](../guides/sdk.md)
- [API Reference](../reference/carboncue_sdk/)
