# CarbonCue GitHub Action

Carbon-aware CI/CD workflows based on Green Software Foundation (GSF) principles.

## Overview

The CarbonCue GitHub Action automatically calculates and reports carbon savings for your workflows. It measures carbon intensity and provides recommendations on whether to run, defer, or warn about high-carbon execution times.

## Features

- 🌍 **Real-time Carbon Data** - Uses Electricity Maps and GSF Carbon-Aware SDK
- 📊 **SCI Score Calculation** - Computes Software Carbon Intensity per GSF spec
- ⚡ **Simple Mode Choice** - immediate, defer, or hybrid (default)
- 📈 **Workflow Summaries** - Beautiful reports in GitHub Actions UI
- 🎯 **Configurable Thresholds** - Set your own carbon intensity limits

## Usage

### Basic Usage

```yaml
name: Carbon-Aware Build
on: [push, pull_request]

jobs:
  carbon-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: carboncue/action@v1
        with:
          mode: 'hybrid' # Simple choice

      - name: Run Tests
        run: npm test
```

### Defer Mode (Skip on High Carbon)

```yaml
- name: Carbon-Aware Deployment
  uses: carboncue/action@v1
  with:
    mode: 'defer'
    carbon-threshold: '250'
    functional-unit-type: 'deployments'
```

If carbon intensity exceeds 250 gCO2eq/kWh, the workflow will fail with a warning to defer.

### Immediate Mode (Always Run, Report Only)

```yaml
- name: Carbon Tracking
  uses: carboncue/action@v1
  with:
    mode: 'immediate'
```

Always runs but provides carbon data for tracking and reporting.

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|

| `mode` | Simple choice: immediate \| defer \| hybrid | No | `hybrid` |
| `carbon-threshold` | Carbon intensity threshold (gCO2eq/kWh) | No | `300` |
| `functional-unit` | Number of functional units | No | `1` |
| `functional-unit-type` | Type of unit (builds, deployments, requests) | No | `builds` |
| `electricity-maps-api-key` | API key for real-time data | No | `` |

## Outputs

| Output | Description |
|--------|-------------|
| `carbon-intensity` | Current carbon intensity (gCO2eq/kWh) |
| `sci-score` | Software Carbon Intensity score |
| `recommendation` | Action recommendation (run, defer, warning) |
| `timestamp` | Measurement timestamp |

## Modes Explained

### Immediate Mode
- **Behavior**: Always runs, reports carbon data
- **Use Case**: Tracking and monitoring without blocking workflows
- **Example**: Non-critical builds, documentation updates

### Defer Mode
- **Behavior**: Fails if carbon intensity > threshold
- **Use Case**: Carbon-critical deployments that can be postponed
- **Example**: Non-urgent production deployments, batch processing

### Hybrid Mode (Default)
- **Behavior**: Warns if carbon intensity is high but continues
- **Use Case**: Important workflows that should run but with visibility
- **Example**: Pull request checks, scheduled builds

## Using Outputs

```yaml
- name: Check Carbon
  id: carbon
  uses: carboncue/action@v1
  with:
    mode: 'hybrid'

- name: Conditional Deployment
  if: steps.carbon.outputs.recommendation == 'run'
  run: |
    echo "Carbon intensity: ${{ steps.carbon.outputs.carbon-intensity }}"
    echo "SCI Score: ${{ steps.carbon.outputs.sci-score }}"
    # Deploy only if recommended
    ./deploy.sh
```

## Configuration with API Keys

For real-time carbon data, set the Electricity Maps API key:

```yaml
- uses: carboncue/action@v1
  with:
    electricity-maps-api-key: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}
    mode: 'hybrid'
```

Store the API key in GitHub Secrets.

## Examples

### Carbon-Aware Testing

```yaml
name: Smart Tests
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Carbon Check
        id: carbon
        uses: carboncue/action@v1
        with:
          mode: 'hybrid'

      - name: Run Tests
        run: |
          if [ "${{ steps.carbon.outputs.recommendation }}" = "run" ]; then
            # Run full test suite on low carbon
            npm test -- --coverage
          else
            # Run critical tests only on high carbon
            npm test -- --testPathPattern=critical
          fi
```

## Dashboard Integration

View your carbon metrics in the CarbonCue dashboard by visiting `https://dashboard.carboncue.dev` and connecting your GitHub repository.

## License

MIT License - see LICENSE file for details.

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for development guidelines.
