# CarbonCue SDK

Core Python SDK for carbon-aware computing based on Green Software Foundation (GSF) principles.

## Features

- 🌍 Real-time carbon intensity data from Electricity Maps
- 📊 SCI (Software Carbon Intensity) score calculation per GSF specification
- ⚡ Async/await support for high-performance applications
- 🔌 Extensible API client architecture
- 💾 Built-in caching to reduce API calls
- 🎯 Type-safe with Pydantic models

## Installation

```bash
pip install carboncue-sdk
```

## Quick Start

```python
import asyncio
from carboncue_sdk import CarbonClient

async def main():
    async with CarbonClient() as client:
        # Get current carbon intensity
        intensity = await client.get_current_intensity(
            region="us-west-2",
            provider="aws"
        )
        print(f"Current intensity: {intensity.carbon_intensity} gCO2eq/kWh")

        # Calculate SCI score
        sci = client.calculate_sci(
            operational_emissions=100.0,  # gCO2eq from energy usage
            embodied_emissions=50.0,      # gCO2eq from hardware
            functional_unit=1000,         # Number of requests
            functional_unit_type="requests",
            region="us-west-2"
        )
        print(f"SCI Score: {sci.score} gCO2eq/request")

asyncio.run(main())
```

## Configuration

Set environment variables with `CARBONCUE_` prefix:

```bash
export CARBONCUE_ELECTRICITY_MAPS_API_KEY=your_api_key
export CARBONCUE_DEFAULT_REGION=us-west-2
export CARBONCUE_CACHE_TTL_SECONDS=300
```

Or use a `.env` file:

```env
CARBONCUE_ELECTRICITY_MAPS_API_KEY=your_api_key
CARBONCUE_DEFAULT_REGION=us-west-2
```

## SCI Calculation

Implements the GSF Software Carbon Intensity specification:

```
SCI = (O + M) / R

Where:
  O = Operational emissions (energy consumption × carbon intensity)
  M = Embodied emissions (hardware manufacturing & infrastructure)
  R = Functional unit (requests, users, transactions, etc.)
```

## API Reference

### CarbonClient

Main client for carbon-awareness operations.

**Methods:**
- `get_current_intensity(region, provider)` - Get real-time carbon intensity
- `calculate_sci(...)` - Calculate SCI score per GSF spec
- `close()` - Cleanup resources

### Models

- `CarbonIntensity` - Carbon intensity data with timestamp
- `SCIScore` - Complete SCI calculation result
- `Region` - Cloud region information
- `EmissionsBreakdown` - Detailed emissions breakdown

## Development

```bash
# Install in development mode
cd packages/sdk
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/
```

## License

MIT License - see LICENSE file for details.
