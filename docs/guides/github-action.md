# GitHub Action Guide

## Overview

The CarbonCue GitHub Action helps you gate your CI/CD workflows based on carbon intensity thresholds, enabling carbon-aware development practices.

## Features

- **Carbon Intensity Gating** - Automatically pass/fail workflows based on current carbon intensity
- **Threshold Configuration** - Set custom carbon intensity thresholds for different regions
- **Multi-Cloud Support** - Works with AWS, Azure, GCP, and other cloud providers
- **SCI Reporting** - Generate Software Carbon Intensity reports for your builds

## Basic Setup

Add the following to your GitHub workflow file (`.github/workflows/your-workflow.yml`):

```yaml
name: Carbon-Aware CI

on: [push, pull_request]

jobs:
  carbon-gate:
    runs-on: ubuntu-latest
    steps:
      - name: Carbon Intensity Check
        uses: CyrilBaah/carboncue@v1
        with:
          region: 'us-east-1'
          threshold: 300
          fail-on-high-carbon: true
        env:
          ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}
```

## Configuration Options

### Required Inputs

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `region` | Cloud region to check carbon intensity for | Yes | - |

### Optional Inputs

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `threshold` | Carbon intensity threshold (gCO2eq/kWh) | No | 400 |
| `fail-on-high-carbon` | Fail the workflow if threshold is exceeded | No | `false` |
| `output-format` | Output format: `json`, `table`, or `summary` | No | `summary` |
| `include-forecast` | Include 24-hour carbon intensity forecast | No | `false` |

### Environment Variables

- `ELECTRICITY_MAPS_API_KEY` - Required API key from Electricity Maps

## Examples

### Basic Carbon Gating

```yaml
- name: Carbon Check
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'eu-west-1'
    threshold: 250
    fail-on-high-carbon: true
```

### Multi-Region Check

```yaml
- name: Check Multiple Regions
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'us-west-2'
    threshold: 300
    output-format: 'json'
    include-forecast: true
```

### Development vs Production Thresholds

```yaml
- name: Carbon Gate (Production)
  if: github.ref == 'refs/heads/main'
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'us-east-1'
    threshold: 200
    fail-on-high-carbon: true

- name: Carbon Check (Development)
  if: github.ref != 'refs/heads/main'
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'us-east-1'
    threshold: 400
    fail-on-high-carbon: false
```

## Output

The action provides the following outputs:

- `carbon-intensity` - Current carbon intensity value
- `threshold-exceeded` - Boolean indicating if threshold was exceeded
- `region` - The region that was checked
- `forecast` - 24-hour forecast data (if enabled)

### Using Outputs

```yaml
- name: Carbon Check
  id: carbon-gate
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'us-east-1'
    threshold: 300

- name: Report Results
  run: |
    echo "Carbon Intensity: ${{ steps.carbon-gate.outputs.carbon-intensity }}"
    echo "Threshold Exceeded: ${{ steps.carbon-gate.outputs.threshold-exceeded }}"
```

## Best Practices

### 1. Set Appropriate Thresholds

Choose thresholds based on your region and sustainability goals:

- **Strict**: 150-200 gCO2eq/kWh
- **Moderate**: 300-400 gCO2eq/kWh
- **Permissive**: 500+ gCO2eq/kWh

### 2. Use Different Thresholds by Environment

```yaml
- name: Set Carbon Threshold
  id: set-threshold
  run: |
    if [ "${{ github.ref }}" == "refs/heads/main" ]; then
      echo "threshold=200" >> $GITHUB_OUTPUT
    else
      echo "threshold=400" >> $GITHUB_OUTPUT
    fi

- name: Carbon Gate
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'us-east-1'
    threshold: ${{ steps.set-threshold.outputs.threshold }}
```

### 3. Handle API Failures Gracefully

```yaml
- name: Carbon Check
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'us-east-1'
    threshold: 300
  continue-on-error: true
  id: carbon-check

- name: Handle Failure
  if: failure() && steps.carbon-check.outcome == 'failure'
  run: echo "Carbon check failed, but continuing workflow"
```

### 4. Schedule Carbon-Aware Deployments

```yaml
name: Carbon-Aware Deployment

on:
  schedule:
    - cron: '0 */2 * * *'  # Check every 2 hours
  workflow_dispatch:

jobs:
  deploy-if-low-carbon:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Carbon Intensity Check
        uses: CyrilBaah/carboncue@v1
        with:
          region: 'eu-west-1'
          threshold: 200
          fail-on-high-carbon: true

      - name: Deploy Application
        if: success()
        run: echo "Deploying during low carbon period"
```

## Troubleshooting

### Common Issues

1. **API Key Missing**
   ```
   Error: ELECTRICITY_MAPS_API_KEY environment variable not set
   ```
   Solution: Add your API key to GitHub Secrets

2. **Invalid Region**
   ```
   Error: Region 'invalid-region' not found
   ```
   Solution: Use a valid cloud region identifier

3. **API Rate Limits**
   ```
   Error: API rate limit exceeded
   ```
   Solution: Use caching or reduce check frequency

### Debug Mode

Enable debug logging:

```yaml
- name: Carbon Check (Debug)
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'us-east-1'
    threshold: 300
  env:
    ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}
    CARBONCUE_DEBUG: 'true'
```

## Integration with Other Actions

### Slack Notifications

```yaml
- name: Carbon Check
  id: carbon
  uses: CyrilBaah/carboncue@v1
  with:
    region: 'us-east-1'
    threshold: 300

- name: Notify Slack
  if: steps.carbon.outputs.threshold-exceeded == 'true'
  uses: 8398a7/action-slack@v3
  with:
    status: custom
    custom_payload: |
      {
        text: "High carbon intensity detected: ${{ steps.carbon.outputs.carbon-intensity }} gCO2eq/kWh"
      }
```

### Create Issues for High Carbon

```yaml
- name: Create Issue for High Carbon
  if: steps.carbon.outputs.threshold-exceeded == 'true'
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'High Carbon Intensity Detected',
        body: `Carbon intensity of ${{ steps.carbon.outputs.carbon-intensity }} gCO2eq/kWh exceeds threshold of ${{ inputs.threshold }} in region ${{ inputs.region }}.`
      })
```
