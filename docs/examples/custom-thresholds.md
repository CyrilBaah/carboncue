# Custom Thresholds Example

This example demonstrates how to set up custom carbon intensity thresholds for different environments and use cases.

## Overview

Custom thresholds allow you to:
- Set different limits for development vs production
- Implement time-based threshold adjustments
- Create region-specific thresholds
- Build flexible carbon-aware deployment policies

## GitHub Action Examples

### Environment-Based Thresholds

```yaml
name: Environment-Specific Carbon Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  carbon-gate:
    runs-on: ubuntu-latest
    steps:
      - name: Set Carbon Threshold
        id: threshold
        run: |
          # Production: stricter threshold
          if [ "${{ github.ref }}" == "refs/heads/main" ]; then
            echo "threshold=200" >> $GITHUB_OUTPUT
            echo "environment=production" >> $GITHUB_OUTPUT
          # Development: more permissive
          elif [ "${{ github.ref }}" == "refs/heads/develop" ]; then
            echo "threshold=350" >> $GITHUB_OUTPUT
            echo "environment=development" >> $GITHUB_OUTPUT
          # Pull requests: informational only
          else
            echo "threshold=500" >> $GITHUB_OUTPUT
            echo "environment=pull-request" >> $GITHUB_OUTPUT
          fi

      - name: Carbon Intensity Check
        uses: CyrilBaah/carboncue@v1
        with:
          region: 'us-east-1'
          threshold: ${{ steps.threshold.outputs.threshold }}
          fail-on-high-carbon: ${{ steps.threshold.outputs.environment == 'production' }}
        env:
          ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}

      - name: Report Results
        run: |
          echo "Environment: ${{ steps.threshold.outputs.environment }}"
          echo "Threshold: ${{ steps.threshold.outputs.threshold }} gCO2eq/kWh"
```

### Time-Based Thresholds

```yaml
name: Time-Aware Carbon Gates

on:
  schedule:
    - cron: '0 */2 * * *'  # Every 2 hours
  workflow_dispatch:

jobs:
  time-based-deployment:
    runs-on: ubuntu-latest
    steps:
      - name: Calculate Time-Based Threshold
        id: threshold
        run: |
          HOUR=$(date +%H)
          DAY_OF_WEEK=$(date +%u)

          # Business hours (9-17, Mon-Fri): lower threshold
          if [ $DAY_OF_WEEK -le 5 ] && [ $HOUR -ge 9 ] && [ $HOUR -le 17 ]; then
            echo "threshold=150" >> $GITHUB_OUTPUT
            echo "period=business-hours" >> $GITHUB_OUTPUT
          # Evening/early morning: moderate threshold
          elif [ $HOUR -ge 18 ] || [ $HOUR -le 8 ]; then
            echo "threshold=250" >> $GITHUB_OUTPUT
            echo "period=off-peak" >> $GITHUB_OUTPUT
          # Weekends: more permissive
          else
            echo "threshold=300" >> $GITHUB_OUTPUT
            echo "period=weekend" >> $GITHUB_OUTPUT
          fi

      - name: Carbon Check with Time-Based Threshold
        uses: CyrilBaah/carboncue@v1
        with:
          region: 'eu-west-1'
          threshold: ${{ steps.threshold.outputs.threshold }}
          fail-on-high-carbon: true
        env:
          ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}

      - name: Deploy if Carbon OK
        if: success()
        run: |
          echo "Deploying during ${{ steps.threshold.outputs.period }}"
          echo "Threshold used: ${{ steps.threshold.outputs.threshold }}"
          # Your deployment commands here
```

### Region-Specific Thresholds

```yaml
name: Multi-Region Carbon Gates

on:
  workflow_dispatch:
    inputs:
      target_region:
        description: 'Target deployment region'
        required: true
        type: choice
        options:
          - 'us-east-1'
          - 'us-west-2'
          - 'eu-west-1'
          - 'eu-north-1'
          - 'ap-southeast-1'

jobs:
  region-specific-gate:
    runs-on: ubuntu-latest
    steps:
      - name: Set Region-Specific Threshold
        id: threshold
        run: |
          case "${{ github.event.inputs.target_region }}" in
            "us-east-1")
              echo "threshold=300" >> $GITHUB_OUTPUT  # Coal-heavy grid
              echo "rationale=Coal-heavy PJM grid" >> $GITHUB_OUTPUT
              ;;
            "us-west-2")
              echo "threshold=200" >> $GITHUB_OUTPUT  # Clean hydroelectric
              echo "rationale=Clean Pacific Northwest hydro" >> $GITHUB_OUTPUT
              ;;
            "eu-west-1")
              echo "threshold=250" >> $GITHUB_OUTPUT  # Wind-heavy Ireland
              echo "rationale=Wind-heavy Irish grid" >> $GITHUB_OUTPUT
              ;;
            "eu-north-1")
              echo "threshold=100" >> $GITHUB_OUTPUT  # Very clean Swedish grid
              echo "rationale=Very clean Swedish hydro/nuclear" >> $GITHUB_OUTPUT
              ;;
            "ap-southeast-1")
              echo "threshold=400" >> $GITHUB_OUTPUT  # High-carbon Singapore
              echo "rationale=High-carbon Singapore grid" >> $GITHUB_OUTPUT
              ;;
            *)
              echo "threshold=350" >> $GITHUB_OUTPUT  # Default
              echo "rationale=Default threshold" >> $GITHUB_OUTPUT
              ;;
          esac

      - name: Carbon Gate for Region
        uses: CyrilBaah/carboncue@v1
        with:
          region: ${{ github.event.inputs.target_region }}
          threshold: ${{ steps.threshold.outputs.threshold }}
          fail-on-high-carbon: true
        env:
          ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}

      - name: Deploy to Region
        if: success()
        run: |
          echo "Deploying to ${{ github.event.inputs.target_region }}"
          echo "Threshold: ${{ steps.threshold.outputs.threshold }} (${{ steps.threshold.outputs.rationale }})"
```

## CLI Examples

### Dynamic Threshold Script

```bash
#!/bin/bash

set_dynamic_threshold() {
    local region=$1
    local environment=${2:-"development"}

    # Base thresholds by region (gCO2eq/kWh)
    case $region in
        "us-west-2"|"eu-north-1"|"norwayeast")
            base_threshold=150  # Clean regions
            ;;
        "eu-west-1"|"us-east-1"|"eu-west-2")
            base_threshold=300  # Moderate regions
            ;;
        "ap-southeast-1"|"ap-south-1"|"australia-southeast1")
            base_threshold=500  # High-carbon regions
            ;;
        *)
            base_threshold=350  # Default
            ;;
    esac

    # Adjust for environment
    case $environment in
        "production")
            threshold=$((base_threshold * 80 / 100))  # 20% stricter
            ;;
        "staging")
            threshold=$base_threshold  # Use base
            ;;
        "development")
            threshold=$((base_threshold * 120 / 100))  # 20% more permissive
            ;;
    esac

    echo $threshold
}

# Usage examples
REGION="us-west-2"
ENVIRONMENT="production"

THRESHOLD=$(set_dynamic_threshold $REGION $ENVIRONMENT)

echo "Region: $REGION"
echo "Environment: $ENVIRONMENT"
echo "Threshold: $THRESHOLD gCO2eq/kWh"

# Check with dynamic threshold
if carboncue check --region $REGION --threshold $THRESHOLD --fail-on-high; then
    echo "✅ Carbon intensity acceptable for deployment"
    # Proceed with deployment
else
    echo "❌ Carbon intensity too high for $ENVIRONMENT deployment"
    exit 1
fi
```

### Seasonal Threshold Adjustments

```bash
#!/bin/bash

get_seasonal_threshold() {
    local base_threshold=$1
    local month=$(date +%m)

    # Adjust thresholds based on seasonal patterns
    case $month in
        12|01|02)  # Winter - higher heating demand
            multiplier=1.2
            season="winter"
            ;;
        06|07|08)  # Summer - higher cooling demand
            multiplier=1.1
            season="summer"
            ;;
        03|04|05|09|10|11)  # Spring/Fall - moderate demand
            multiplier=1.0
            season="spring/fall"
            ;;
    esac

    adjusted_threshold=$(echo "$base_threshold * $multiplier" | bc -l | cut -d'.' -f1)

    echo "Season: $season (month $month)"
    echo "Multiplier: $multiplier"
    echo "Adjusted threshold: $adjusted_threshold gCO2eq/kWh"

    echo $adjusted_threshold
}

# Example usage
BASE_THRESHOLD=300
SEASONAL_THRESHOLD=$(get_seasonal_threshold $BASE_THRESHOLD)

carboncue check --region eu-west-1 --threshold $SEASONAL_THRESHOLD
```

## SDK Examples

### Adaptive Threshold Class

```python
import carboncue_sdk as cc
from datetime import datetime, time
from typing import Dict, Optional

class AdaptiveThresholdManager:
    """Manages dynamic carbon intensity thresholds based on various factors."""

    def __init__(self, client: cc.CarbonCueClient):
        self.client = client

        # Base thresholds by region type
        self.region_thresholds = {
            'clean': 150,      # Hydro/nuclear regions
            'moderate': 300,   # Mixed grids
            'dirty': 500       # Coal-heavy grids
        }

        # Environment multipliers
        self.environment_multipliers = {
            'production': 0.8,    # 20% stricter
            'staging': 1.0,       # Base threshold
            'development': 1.3    # 30% more permissive
        }

        # Time-of-day adjustments
        self.time_adjustments = {
            'business_hours': 0.9,  # 10% stricter during peak
            'evening': 1.0,         # Base
            'night': 1.1           # 10% more permissive
        }

    def get_region_category(self, region: str) -> str:
        """Categorize region by carbon intensity profile."""
        clean_regions = [
            'eu-north-1', 'norwayeast', 'swedencentral',
            'us-west-2', 'us-west1', 'francecentral'
        ]

        dirty_regions = [
            'ap-southeast-2', 'ap-south-1', 'centralindia',
            'australiaeast', 'australiasoutheast1'
        ]

        if region in clean_regions:
            return 'clean'
        elif region in dirty_regions:
            return 'dirty'
        else:
            return 'moderate'

    def get_time_period(self) -> str:
        """Determine current time period."""
        now = datetime.now().time()

        if time(9, 0) <= now <= time(17, 0):
            return 'business_hours'
        elif time(18, 0) <= now <= time(23, 59):
            return 'evening'
        else:
            return 'night'

    def calculate_threshold(self,
                          region: str,
                          environment: str = 'development',
                          custom_base: Optional[int] = None) -> int:
        """Calculate adaptive threshold based on multiple factors."""

        # Get base threshold
        if custom_base:
            base = custom_base
        else:
            region_category = self.get_region_category(region)
            base = self.region_thresholds[region_category]

        # Apply environment multiplier
        env_multiplier = self.environment_multipliers.get(environment, 1.0)

        # Apply time-of-day adjustment
        time_period = self.get_time_period()
        time_multiplier = self.time_adjustments.get(time_period, 1.0)

        # Calculate final threshold
        threshold = int(base * env_multiplier * time_multiplier)

        return threshold

    def should_deploy(self,
                     region: str,
                     environment: str = 'development',
                     custom_threshold: Optional[int] = None) -> Dict:
        """Determine if deployment should proceed based on carbon intensity."""

        try:
            # Get current carbon intensity
            intensity_data = self.client.get_carbon_intensity(region)
            current_intensity = intensity_data.value

            # Calculate threshold
            if custom_threshold:
                threshold = custom_threshold
            else:
                threshold = self.calculate_threshold(region, environment)

            # Make decision
            should_proceed = current_intensity <= threshold

            return {
                'should_deploy': should_proceed,
                'current_intensity': current_intensity,
                'threshold': threshold,
                'region': region,
                'environment': environment,
                'margin': threshold - current_intensity,
                'time_period': self.get_time_period(),
                'region_category': self.get_region_category(region),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'should_deploy': False,
                'error': str(e),
                'region': region,
                'environment': environment,
                'timestamp': datetime.now().isoformat()
            }

# Usage example
def main():
    client = cc.CarbonCueClient()
    threshold_manager = AdaptiveThresholdManager(client)

    # Check deployment readiness
    result = threshold_manager.should_deploy(
        region='us-east-1',
        environment='production'
    )

    print(f"Should deploy: {result['should_deploy']}")
    print(f"Current intensity: {result['current_intensity']} gCO2eq/kWh")
    print(f"Threshold: {result['threshold']} gCO2eq/kWh")
    print(f"Margin: {result['margin']} gCO2eq/kWh")

    if result['should_deploy']:
        print("✅ Proceeding with deployment")
        # Your deployment logic here
    else:
        print("❌ Delaying deployment due to high carbon intensity")

        # Maybe schedule for later?
        forecast = client.get_carbon_forecast(result['region'], hours=24)
        best_time = min(forecast, key=lambda x: x.intensity)
        print(f"💡 Best deployment window: {best_time.datetime}")

if __name__ == "__main__":
    main()
```

### Threshold Configuration Management

```python
import json
from pathlib import Path
from typing import Dict, Any

class ThresholdConfig:
    """Manage threshold configurations for different scenarios."""

    def __init__(self, config_path: str = "carbon_thresholds.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load threshold configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Default threshold configuration."""
        return {
            "environments": {
                "production": {
                    "base_threshold": 250,
                    "strict_mode": True,
                    "regions": {
                        "us-west-2": 200,
                        "eu-north-1": 100,
                        "eu-west-1": 250
                    }
                },
                "staging": {
                    "base_threshold": 350,
                    "strict_mode": False,
                    "regions": {}
                },
                "development": {
                    "base_threshold": 450,
                    "strict_mode": False,
                    "regions": {}
                }
            },
            "schedules": {
                "business_hours": {
                    "multiplier": 0.8,
                    "hours": [9, 10, 11, 12, 13, 14, 15, 16, 17]
                },
                "off_peak": {
                    "multiplier": 1.2,
                    "hours": [22, 23, 0, 1, 2, 3, 4, 5, 6]
                }
            },
            "alerts": {
                "slack_webhook": None,
                "email_notifications": False
            }
        }

    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_threshold(self, environment: str, region: str = None) -> int:
        """Get threshold for specific environment and region."""
        env_config = self.config["environments"].get(environment, {})

        # Check for region-specific threshold
        if region and region in env_config.get("regions", {}):
            return env_config["regions"][region]

        # Fall back to base threshold
        return env_config.get("base_threshold", 400)

    def set_threshold(self, environment: str, threshold: int, region: str = None):
        """Set threshold for environment/region."""
        if environment not in self.config["environments"]:
            self.config["environments"][environment] = {"base_threshold": 400, "regions": {}}

        if region:
            self.config["environments"][environment].setdefault("regions", {})[region] = threshold
        else:
            self.config["environments"][environment]["base_threshold"] = threshold

        self.save_config()

# Example usage
def setup_custom_thresholds():
    """Example of setting up custom threshold configuration."""

    config = ThresholdConfig()

    # Set production thresholds
    config.set_threshold("production", 200)  # Base production threshold
    config.set_threshold("production", 150, "eu-north-1")  # Stricter for clean region
    config.set_threshold("production", 300, "ap-southeast-1")  # More permissive for dirty region

    # Set development thresholds
    config.set_threshold("development", 450)

    print("Custom thresholds configured:")
    print(f"Production base: {config.get_threshold('production')}")
    print(f"Production EU North: {config.get_threshold('production', 'eu-north-1')}")
    print(f"Development: {config.get_threshold('development')}")

if __name__ == "__main__":
    setup_custom_thresholds()
```

## Best Practices

### 1. Start Conservative

Begin with stricter thresholds and relax them as needed:

```yaml
# Start with low thresholds
production_threshold: 200
staging_threshold: 300
development_threshold: 400
```

### 2. Monitor and Adjust

Track threshold hit rates and adjust accordingly:

```bash
# Check threshold success rate over time
carboncue check --region us-east-1 --threshold 300 --format json | \
jq '.threshold_exceeded' | \
sort | uniq -c
```

### 3. Regional Considerations

Account for regional grid characteristics:

- **Clean grids**: Lower thresholds (100-200)
- **Mixed grids**: Moderate thresholds (250-350)
- **Dirty grids**: Higher thresholds (400-600)

### 4. Business Impact Balance

Balance carbon goals with business needs:

```python
# Progressive threshold enforcement
if environment == 'production' and is_critical_deployment:
    threshold *= 1.5  # Relax for critical deployments
elif environment == 'production' and is_scheduled_maintenance:
    threshold *= 0.8  # Stricter for planned work
```

### 5. Seasonal Adjustments

Consider seasonal electricity patterns:

- **Winter**: Higher thresholds (heating demand)
- **Summer**: Moderate increase (cooling demand)
- **Spring/Fall**: Base thresholds

This approach ensures your carbon-aware deployment strategy adapts to real-world conditions while maintaining sustainability goals.
