# CarbonCue CLI

Terminal interface for carbon-aware development.

## Installation

```bash
pip install carboncue-cli
```

## Commands

### Check Carbon Intensity

Get current carbon intensity for a cloud region:

```bash
# AWS US West 2
carboncue check --region us-west-2 --provider aws

# Azure West Europe
carboncue check --region westeurope --provider azure

# Short form
carboncue check -r us-east-1 -p aws
```

### Calculate SCI Score

Calculate Software Carbon Intensity (SCI) score per GSF specification:

```bash
carboncue sci \
  --operations 100 \
  --materials 50 \
  --functional-unit 1000 \
  --unit-type requests \
  --region us-west-2

# Short form
carboncue sci -o 100 -m 50 -r 1000 -t requests
```

**Parameters:**
- `--operations, -o`: Operational emissions in gCO2eq (energy usage)
- `--materials, -m`: Embodied emissions in gCO2eq (hardware)
- `--functional-unit, -r`: Number of functional units
- `--unit-type, -t`: Type of functional unit (requests, users, transactions, etc.)
- `--region`: Cloud region (default: us-west-2)
- `--provider, -p`: Cloud provider (aws, azure, gcp, etc.)

### View Configuration

```bash
carboncue config
```

## Configuration

Set environment variables:

```bash
export CARBONCUE_ELECTRICITY_MAPS_API_KEY=your_api_key
export CARBONCUE_DEFAULT_REGION=us-west-2
export CARBONCUE_DEFAULT_CLOUD_PROVIDER=aws
```

Or create a `.env` file in your project:

```env
CARBONCUE_ELECTRICITY_MAPS_API_KEY=your_api_key
CARBONCUE_DEFAULT_REGION=us-west-2
```

## Examples

### CI/CD Integration

```bash
# Check if carbon intensity is low before running expensive tests
INTENSITY=$(carboncue check -r us-west-2 -p aws --json | jq '.carbon_intensity')
if [ $INTENSITY -lt 200 ]; then
  echo "Low carbon intensity - running full test suite"
  pytest
else
  echo "High carbon intensity - deferring non-critical tests"
  pytest -m critical
fi
```

### Monitoring Scripts

```bash
#!/bin/bash
# monitor-carbon.sh - Check carbon intensity every hour

while true; do
  carboncue check -r us-west-2 -p aws
  sleep 3600
done
```

## Output Formats

All commands support rich terminal output with colors and tables for better readability.

## License

MIT License - see LICENSE file for details.
