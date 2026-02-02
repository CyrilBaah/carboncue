# CLI Usage Guide

## Overview

The CarbonCue CLI provides a command-line interface for checking carbon intensity, calculating SCI scores, and integrating carbon-awareness into your development workflow.

## Installation

```bash
pip install carboncue-cli
```

Or install from source:

```bash
git clone https://github.com/CyrilBaah/carboncue.git
cd carboncue/packages/cli
pip install -e .
```

## Basic Usage

### Check Carbon Intensity

Get current carbon intensity for a region:

```bash
carboncue check --region us-east-1
```

Output:
```
Region: us-east-1
Carbon Intensity: 285 gCO2eq/kWh
Status: MODERATE
Last Updated: 2026-02-02T10:30:00Z
```

### Check with Threshold

```bash
carboncue check --region eu-west-1 --threshold 200
```

Output:
```
Region: eu-west-1
Carbon Intensity: 156 gCO2eq/kWh
Status: LOW (✓ Below threshold of 200)
Last Updated: 2026-02-02T10:30:00Z
```

### Get Forecast

View 24-hour carbon intensity forecast:

```bash
carboncue forecast --region us-west-2
```

## Commands

### `check`

Check current carbon intensity for a region.

```bash
carboncue check [OPTIONS]
```

**Options:**
- `--region, -r` (required): Cloud region to check
- `--threshold, -t`: Carbon intensity threshold (default: 400)
- `--format, -f`: Output format: `table`, `json`, `csv` (default: table)
- `--fail-on-high`: Exit with error code if threshold exceeded

**Examples:**

```bash
# Basic check
carboncue check --region us-east-1

# With threshold and JSON output
carboncue check --region eu-central-1 --threshold 250 --format json

# Fail if threshold exceeded (useful in scripts)
carboncue check --region ap-southeast-1 --threshold 300 --fail-on-high
```

### `forecast`

Get 24-hour carbon intensity forecast.

```bash
carboncue forecast [OPTIONS]
```

**Options:**
- `--region, -r` (required): Cloud region to forecast
- `--hours`: Number of hours to forecast (default: 24, max: 168)
- `--format, -f`: Output format: `table`, `json`, `csv`, `chart` (default: table)
- `--threshold, -t`: Highlight values above threshold

**Examples:**

```bash
# Basic forecast
carboncue forecast --region us-west-2

# 48-hour forecast with chart
carboncue forecast --region eu-west-1 --hours 48 --format chart

# Show only next 8 hours
carboncue forecast --region ap-northeast-1 --hours 8
```

### `regions`

List supported regions and their current status.

```bash
carboncue regions [OPTIONS]
```

**Options:**
- `--provider, -p`: Filter by cloud provider: `aws`, `azure`, `gcp`, `digitalocean`
- `--format, -f`: Output format: `table`, `json`, `csv` (default: table)
- `--threshold, -t`: Show threshold status for each region

**Examples:**

```bash
# List all regions
carboncue regions

# AWS regions only
carboncue regions --provider aws

# Show with threshold status
carboncue regions --threshold 300 --format table
```

### `sci`

Calculate Software Carbon Intensity (SCI) score.

```bash
carboncue sci [OPTIONS]
```

**Options:**
- `--energy, -e` (required): Energy consumption in kWh
- `--region, -r` (required): Cloud region
- `--embodied`: Embodied emissions in gCO2eq (default: 0)
- `--functional-unit, -f`: Functional unit for calculation (default: 1)
- `--format`: Output format: `table`, `json` (default: table)

**Examples:**

```bash
# Basic SCI calculation
carboncue sci --energy 0.5 --region us-east-1

# With embodied emissions
carboncue sci --energy 1.2 --region eu-west-1 --embodied 100

# Per 1000 requests
carboncue sci --energy 2.5 --region ap-southeast-1 --functional-unit 1000
```

### `config`

Manage CLI configuration.

```bash
carboncue config [SUBCOMMAND]
```

**Subcommands:**
- `set`: Set configuration value
- `get`: Get configuration value
- `list`: List all configuration
- `reset`: Reset to defaults

**Examples:**

```bash
# Set default region
carboncue config set default_region us-west-2

# Set API key
carboncue config set api_key your_electricity_maps_api_key

# Set default threshold
carboncue config set default_threshold 300

# View current config
carboncue config list
```

## Configuration

### Configuration File

CarbonCue stores configuration in `~/.carboncue/config.yml`:

```yaml
api_key: your_electricity_maps_api_key
default_region: us-east-1
default_threshold: 400
default_format: table
cache_ttl: 300  # seconds
```

### Environment Variables

Override configuration with environment variables:

- `CARBONCUE_API_KEY`: Electricity Maps API key
- `CARBONCUE_DEFAULT_REGION`: Default region
- `CARBONCUE_DEFAULT_THRESHOLD`: Default threshold
- `CARBONCUE_CACHE_TTL`: Cache time-to-live in seconds

### API Key Setup

1. Get API key from [Electricity Maps](https://www.electricitymaps.com/free-tier-api)
2. Set via config:
   ```bash
   carboncue config set api_key YOUR_API_KEY
   ```
3. Or via environment variable:
   ```bash
   export CARBONCUE_API_KEY=YOUR_API_KEY
   ```

## Output Formats

### Table (Default)

```
Region          Carbon Intensity    Status    Last Updated
us-east-1       285 gCO2eq/kWh     MODERATE  2026-02-02T10:30:00Z
```

### JSON

```json
{
  "region": "us-east-1",
  "carbon_intensity": 285,
  "threshold": 400,
  "status": "moderate",
  "threshold_exceeded": false,
  "last_updated": "2026-02-02T10:30:00Z"
}
```

### CSV

```csv
region,carbon_intensity,status,last_updated
us-east-1,285,moderate,2026-02-02T10:30:00Z
```

## Scripting and Automation

### Exit Codes

- `0`: Success
- `1`: General error
- `2`: API error
- `3`: Threshold exceeded (when using `--fail-on-high`)

### Shell Scripts

```bash
#!/bin/bash

# Check if deployment should proceed
if carboncue check --region us-east-1 --threshold 250 --fail-on-high; then
    echo "Carbon intensity is low, proceeding with deployment"
    ./deploy.sh
else
    echo "Carbon intensity too high, skipping deployment"
    exit 1
fi
```

### JSON Parsing

```bash
# Get carbon intensity value
CARBON_INTENSITY=$(carboncue check --region us-east-1 --format json | jq '.carbon_intensity')

if [ "$CARBON_INTENSITY" -lt 200 ]; then
    echo "Low carbon intensity: $CARBON_INTENSITY"
fi
```

### Scheduled Checks

Add to crontab for regular monitoring:

```bash
# Check every hour and log results
0 * * * * carboncue check --region us-east-1 --format json >> /var/log/carbon-intensity.log
```

## Integration Examples

### Docker

Create a Docker image that includes carbon checks:

```dockerfile
FROM python:3.11-slim

RUN pip install carboncue-cli

COPY check-carbon.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/check-carbon.sh

ENV CARBONCUE_API_KEY=""
ENV CARBONCUE_DEFAULT_REGION="us-east-1"

CMD ["check-carbon.sh"]
```

### Makefile

```makefile
.PHONY: deploy-if-low-carbon
deploy-if-low-carbon:
	@echo "Checking carbon intensity..."
	@carboncue check --region $(REGION) --threshold 300 --fail-on-high
	@echo "Carbon intensity OK, deploying..."
	@./deploy.sh

.PHONY: carbon-report
carbon-report:
	@echo "Generating carbon report..."
	@carboncue regions --format json > carbon-report.json
	@carboncue forecast --region us-east-1 --format csv > forecast.csv
```

### GitHub Actions

```yaml
- name: Check Carbon Intensity
  run: |
    carboncue check --region us-east-1 --threshold 300 --format json > carbon-check.json
    cat carbon-check.json
  env:
    CARBONCUE_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}
```

## Advanced Usage

### Custom Thresholds by Time

```bash
#!/bin/bash

# Lower threshold during business hours
HOUR=$(date +%H)
if [ "$HOUR" -ge 9 ] && [ "$HOUR" -le 17 ]; then
    THRESHOLD=200
else
    THRESHOLD=400
fi

carboncue check --region eu-west-1 --threshold $THRESHOLD --fail-on-high
```

### Multi-Region Comparison

```bash
#!/bin/bash

REGIONS=("us-east-1" "us-west-2" "eu-west-1" "ap-southeast-1")

echo "Region,Carbon Intensity,Status" > multi-region-report.csv

for region in "${REGIONS[@]}"; do
    result=$(carboncue check --region "$region" --format json)
    intensity=$(echo "$result" | jq -r '.carbon_intensity')
    status=$(echo "$result" | jq -r '.status')
    echo "$region,$intensity,$status" >> multi-region-report.csv
done

echo "Multi-region carbon intensity report generated"
```

### Notification Integration

```bash
#!/bin/bash

# Check carbon intensity and send Slack notification if high
result=$(carboncue check --region us-east-1 --threshold 300 --format json)
intensity=$(echo "$result" | jq -r '.carbon_intensity')
exceeded=$(echo "$result" | jq -r '.threshold_exceeded')

if [ "$exceeded" = "true" ]; then
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"High carbon intensity detected: ${intensity} gCO2eq/kWh\"}" \
        $SLACK_WEBHOOK_URL
fi
```

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   Error: API key not found. Set CARBONCUE_API_KEY environment variable or use 'carboncue config set api_key YOUR_KEY'
   ```

2. **Invalid Region**
   ```
   Error: Region 'invalid-region' not found. Use 'carboncue regions' to see available regions.
   ```

3. **Network Issues**
   ```
   Error: Failed to fetch carbon intensity data. Check your internet connection.
   ```

4. **Rate Limiting**
   ```
   Error: API rate limit exceeded. Try again in a few minutes.
   ```

### Debug Mode

Enable debug logging:

```bash
export CARBONCUE_LOG_LEVEL=DEBUG
carboncue check --region us-east-1
```

### Cache Issues

Clear the cache:

```bash
rm -rf ~/.carboncue/cache/
```

Or disable caching:

```bash
export CARBONCUE_CACHE_TTL=0
```
