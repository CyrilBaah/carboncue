# Multi-Region Deployment Example

This example demonstrates how to implement carbon-aware multi-region deployment strategies using CarbonCue across different cloud providers.

## Overview

Multi-region carbon-aware deployments allow you to:
- Deploy to the region with lowest carbon intensity
- Implement failover based on carbon thresholds
- Load balance across regions considering both performance and carbon impact
- Optimize global application footprint for sustainability

## GitHub Actions Examples

### Best Region Selection

```yaml
name: Carbon-Optimized Multi-Region Deployment

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  find-best-region:
    runs-on: ubuntu-latest
    outputs:
      best-region: ${{ steps.select-region.outputs.best-region }}
      carbon-intensity: ${{ steps.select-region.outputs.carbon-intensity }}
      all-regions-data: ${{ steps.select-region.outputs.all-regions-data }}
    steps:
      - name: Select Best Region
        id: select-region
        run: |
          declare -a regions=(
            "us-east-1"
            "us-west-2"
            "eu-west-1"
            "eu-north-1"
            "ap-southeast-1"
            "ap-northeast-1"
          )

          best_region=""
          lowest_intensity=999999
          all_data="["

          for region in "${regions[@]}"; do
            echo "Checking region: $region"

            # Get carbon intensity (using curl to simulate API call)
            intensity_result=$(curl -s -X GET \
              "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=$region" \
              -H "auth-token: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}" || echo '{"carbonIntensity":500}')

            intensity=$(echo "$intensity_result" | jq -r '.carbonIntensity // 500')

            echo "Region $region: $intensity gCO2eq/kWh"

            # Track best region
            if (( $(echo "$intensity < $lowest_intensity" | bc -l) )); then
              lowest_intensity=$intensity
              best_region=$region
            fi

            # Collect all data
            if [ "$all_data" != "[" ]; then
              all_data+=","
            fi
            all_data+="{\"region\":\"$region\",\"intensity\":$intensity}"
          done

          all_data+="]"

          echo "best-region=$best_region" >> $GITHUB_OUTPUT
          echo "carbon-intensity=$lowest_intensity" >> $GITHUB_OUTPUT
          echo "all-regions-data=$all_data" >> $GITHUB_OUTPUT

          echo "🌍 Best region: $best_region ($lowest_intensity gCO2eq/kWh)"

  deploy-to-best-region:
    needs: find-best-region
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Carbon Intensity
        run: |
          INTENSITY=${{ needs.find-best-region.outputs.carbon-intensity }}
          THRESHOLD=300

          if (( $(echo "$INTENSITY > $THRESHOLD" | bc -l) )); then
            echo "❌ Carbon intensity ($INTENSITY) exceeds threshold ($THRESHOLD)"
            echo "Delaying deployment until intensity improves"
            exit 1
          else
            echo "✅ Carbon intensity ($INTENSITY) within threshold ($THRESHOLD)"
          fi

      - name: Deploy to Selected Region
        run: |
          REGION=${{ needs.find-best-region.outputs.best-region }}
          echo "🚀 Deploying to region: $REGION"
          echo "🌱 Carbon intensity: ${{ needs.find-best-region.outputs.carbon-intensity }} gCO2eq/kWh"

          # Your deployment commands here
          # Example: terraform apply -var="region=$REGION"
          # Example: aws configure set region $REGION && sam deploy

      - name: Update DNS/Load Balancer
        run: |
          REGION=${{ needs.find-best-region.outputs.best-region }}
          echo "🔄 Updating traffic routing to $REGION"
          # Update load balancer or DNS to point to new region
          # Example: aws route53 change-resource-record-sets ...

  notify-deployment:
    needs: [find-best-region, deploy-to-best-region]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Send Notification
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              "text": "Multi-Region Deployment Complete",
              "attachments": [
                {
                  "color": "${{ job.status == 'success' && 'good' || 'danger' }}",
                  "fields": [
                    {
                      "title": "Selected Region",
                      "value": "${{ needs.find-best-region.outputs.best-region }}",
                      "short": true
                    },
                    {
                      "title": "Carbon Intensity",
                      "value": "${{ needs.find-best-region.outputs.carbon-intensity }} gCO2eq/kWh",
                      "short": true
                    },
                    {
                      "title": "Status",
                      "value": "${{ job.status }}",
                      "short": true
                    }
                  ]
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Multi-Cloud Deployment

```yaml
name: Multi-Cloud Carbon-Aware Deployment

on:
  workflow_dispatch:
    inputs:
      deployment_urgency:
        description: 'Deployment urgency level'
        type: choice
        options:
          - 'low'
          - 'medium'
          - 'high'
        default: 'medium'

jobs:
  check-all-clouds:
    runs-on: ubuntu-latest
    outputs:
      aws-best: ${{ steps.check-clouds.outputs.aws-best }}
      azure-best: ${{ steps.check-clouds.outputs.azure-best }}
      gcp-best: ${{ steps.check-clouds.outputs.gcp-best }}
      overall-best: ${{ steps.check-clouds.outputs.overall-best }}
    steps:
      - name: Check All Cloud Regions
        id: check-clouds
        run: |
          # Set thresholds based on urgency
          case "${{ github.event.inputs.deployment_urgency }}" in
            "low")
              THRESHOLD=200
              ;;
            "medium")
              THRESHOLD=300
              ;;
            "high")
              THRESHOLD=500
              ;;
          esac

          echo "Using threshold: $THRESHOLD gCO2eq/kWh"

          # AWS regions
          aws_regions=("us-east-1" "us-west-2" "eu-west-1" "eu-north-1")
          aws_best=""
          aws_lowest=999999

          # Azure regions
          azure_regions=("eastus" "westus2" "northeurope" "swedencentral")
          azure_best=""
          azure_lowest=999999

          # GCP regions
          gcp_regions=("us-central1" "us-west1" "europe-west1" "europe-north1")
          gcp_best=""
          gcp_lowest=999999

          overall_best=""
          overall_lowest=999999

          # Function to check region
          check_region() {
            local region=$1
            local provider=$2

            # Simulate carbon intensity check
            # In real implementation, use CarbonCue API
            intensity=$(shuf -i 100-600 -n 1)  # Random for demo

            echo "$provider $region: $intensity gCO2eq/kWh"
            echo "$intensity"
          }

          # Check AWS regions
          for region in "${aws_regions[@]}"; do
            intensity=$(check_region $region "AWS")
            if (( $(echo "$intensity < $aws_lowest" | bc -l) )); then
              aws_lowest=$intensity
              aws_best="$region ($intensity)"
            fi
            if (( $(echo "$intensity < $overall_lowest" | bc -l) )); then
              overall_lowest=$intensity
              overall_best="AWS:$region ($intensity)"
            fi
          done

          # Check Azure regions
          for region in "${azure_regions[@]}"; do
            intensity=$(check_region $region "Azure")
            if (( $(echo "$intensity < $azure_lowest" | bc -l) )); then
              azure_lowest=$intensity
              azure_best="$region ($intensity)"
            fi
            if (( $(echo "$intensity < $overall_lowest" | bc -l) )); then
              overall_lowest=$intensity
              overall_best="Azure:$region ($intensity)"
            fi
          done

          # Check GCP regions
          for region in "${gcp_regions[@]}"; do
            intensity=$(check_region $region "GCP")
            if (( $(echo "$intensity < $gcp_lowest" | bc -l) )); then
              gcp_lowest=$intensity
              gcp_best="$region ($intensity)"
            fi
            if (( $(echo "$intensity < $overall_lowest" | bc -l) )); then
              overall_lowest=$intensity
              overall_best="GCP:$region ($intensity)"
            fi
          done

          echo "aws-best=$aws_best" >> $GITHUB_OUTPUT
          echo "azure-best=$azure_best" >> $GITHUB_OUTPUT
          echo "gcp-best=$gcp_best" >> $GITHUB_OUTPUT
          echo "overall-best=$overall_best" >> $GITHUB_OUTPUT

          echo "🏆 Overall best: $overall_best"

  deploy-to-best:
    needs: check-all-clouds
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Parse Best Region
        id: parse
        run: |
          BEST="${{ needs.check-all-clouds.outputs.overall-best }}"

          # Extract provider and region
          PROVIDER=$(echo "$BEST" | cut -d':' -f1)
          REGION_AND_INTENSITY=$(echo "$BEST" | cut -d':' -f2)
          REGION=$(echo "$REGION_AND_INTENSITY" | sed 's/ (.*)//')
          INTENSITY=$(echo "$REGION_AND_INTENSITY" | sed 's/.*(\([0-9]*\)).*/\1/')

          echo "provider=$PROVIDER" >> $GITHUB_OUTPUT
          echo "region=$REGION" >> $GITHUB_OUTPUT
          echo "intensity=$INTENSITY" >> $GITHUB_OUTPUT

          echo "Deploying to $PROVIDER region $REGION ($INTENSITY gCO2eq/kWh)"

      - name: Deploy to AWS
        if: steps.parse.outputs.provider == 'AWS'
        run: |
          echo "🚀 Deploying to AWS region: ${{ steps.parse.outputs.region }}"
          # AWS deployment commands
          # aws configure set region ${{ steps.parse.outputs.region }}
          # sam deploy --region ${{ steps.parse.outputs.region }}

      - name: Deploy to Azure
        if: steps.parse.outputs.provider == 'Azure'
        run: |
          echo "🚀 Deploying to Azure region: ${{ steps.parse.outputs.region }}"
          # Azure deployment commands
          # az configure --defaults location=${{ steps.parse.outputs.region }}
          # az deployment group create --resource-group myRG --template-file template.json

      - name: Deploy to GCP
        if: steps.parse.outputs.provider == 'GCP'
        run: |
          echo "🚀 Deploying to GCP region: ${{ steps.parse.outputs.region }}"
          # GCP deployment commands
          # gcloud config set compute/region ${{ steps.parse.outputs.region }}
          # gcloud run deploy myapp --region ${{ steps.parse.outputs.region }}
```

### Rolling Multi-Region Update

```yaml
name: Carbon-Aware Rolling Deployment

on:
  push:
    branches: [main]

jobs:
  prepare-deployment:
    runs-on: ubuntu-latest
    outputs:
      regions-matrix: ${{ steps.prepare.outputs.regions-matrix }}
    steps:
      - name: Prepare Region Matrix
        id: prepare
        run: |
          # Define regions in order of preference (cleanest first)
          REGIONS='[
            {"region": "eu-north-1", "provider": "aws", "threshold": 100},
            {"region": "norwayeast", "provider": "azure", "threshold": 100},
            {"region": "us-west-2", "provider": "aws", "threshold": 200},
            {"region": "europe-west6", "provider": "gcp", "threshold": 200},
            {"region": "francecentral", "provider": "azure", "threshold": 150},
            {"region": "eu-west-1", "provider": "aws", "threshold": 300},
            {"region": "us-east-1", "provider": "aws", "threshold": 350}
          ]'

          echo "regions-matrix=$REGIONS" >> $GITHUB_OUTPUT

  rolling-deployment:
    needs: prepare-deployment
    runs-on: ubuntu-latest
    strategy:
      matrix:
        region: ${{ fromJson(needs.prepare-deployment.outputs.regions-matrix) }}
      max-parallel: 2  # Deploy to 2 regions at a time
      fail-fast: false
    steps:
      - uses: actions/checkout@v4

      - name: Check Carbon Intensity
        id: carbon-check
        uses: CyrilBaah/carboncue@v1
        with:
          region: ${{ matrix.region.region }}
          threshold: ${{ matrix.region.threshold }}
          fail-on-high-carbon: false  # Don't fail, just report
        env:
          ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}

      - name: Deploy if Carbon Acceptable
        if: steps.carbon-check.outputs.threshold-exceeded != 'true'
        run: |
          echo "✅ Deploying to ${{ matrix.region.provider }}:${{ matrix.region.region }}"
          echo "Carbon intensity: ${{ steps.carbon-check.outputs.carbon-intensity }} gCO2eq/kWh"

          # Your deployment logic here based on provider
          case "${{ matrix.region.provider }}" in
            "aws")
              echo "AWS deployment to ${{ matrix.region.region }}"
              ;;
            "azure")
              echo "Azure deployment to ${{ matrix.region.region }}"
              ;;
            "gcp")
              echo "GCP deployment to ${{ matrix.region.region }}"
              ;;
          esac

      - name: Skip High Carbon Region
        if: steps.carbon-check.outputs.threshold-exceeded == 'true'
        run: |
          echo "⏭️  Skipping ${{ matrix.region.provider }}:${{ matrix.region.region }}"
          echo "Carbon intensity too high: ${{ steps.carbon-check.outputs.carbon-intensity }} gCO2eq/kWh"
          echo "Threshold: ${{ matrix.region.threshold }} gCO2eq/kWh"

      - name: Update Load Balancer
        if: steps.carbon-check.outputs.threshold-exceeded != 'true'
        run: |
          echo "🔄 Adding ${{ matrix.region.region }} to load balancer"
          # Update global load balancer configuration
```

## CLI Scripts

### Multi-Region Comparison Script

```bash
#!/bin/bash

# Multi-region carbon intensity comparison
compare_regions() {
    local regions=("$@")
    local results=()

    echo "🌍 Comparing carbon intensity across regions..."
    echo "================================================="

    # Header
    printf "%-20s %-15s %-10s %-15s\n" "Region" "Provider" "Intensity" "Status"
    printf "%-20s %-15s %-10s %-15s\n" "------" "--------" "---------" "------"

    for region in "${regions[@]}"; do
        # Determine provider from region name
        if [[ $region =~ ^us-|^eu-|^ap- ]]; then
            provider="AWS"
        elif [[ $region =~ eastus|westus|northeurope ]]; then
            provider="Azure"
        elif [[ $region =~ central1|west1|europe- ]]; then
            provider="GCP"
        else
            provider="Unknown"
        fi

        # Check carbon intensity
        result=$(carboncue check --region "$region" --format json 2>/dev/null)

        if [ $? -eq 0 ]; then
            intensity=$(echo "$result" | jq -r '.carbon_intensity')
            status=$(echo "$result" | jq -r '.status')

            # Color code the status
            case $status in
                "low") status_display="🟢 $status" ;;
                "moderate") status_display="🟡 $status" ;;
                "high") status_display="🔴 $status" ;;
                *) status_display="⚪ $status" ;;
            esac

            printf "%-20s %-15s %-10s %-15s\n" "$region" "$provider" "${intensity}" "$status_display"

            # Store for sorting
            results+=("$intensity:$region:$provider:$status")
        else
            printf "%-20s %-15s %-10s %-15s\n" "$region" "$provider" "ERROR" "❌ Failed"
        fi
    done

    echo ""
    echo "🏆 Best regions (sorted by carbon intensity):"
    echo "=============================================="

    # Sort by intensity and show top 3
    IFS=$'\n' sorted=($(sort -n <<<"${results[*]}"))

    for i in {0..2}; do
        if [ $i -lt ${#sorted[@]} ]; then
            IFS=':' read -r intensity region provider status <<< "${sorted[$i]}"
            echo "$((i+1)). $provider:$region - $intensity gCO2eq/kWh ($status)"
        fi
    done
}

# Example usage
AWS_REGIONS=(
    "us-east-1" "us-east-2" "us-west-1" "us-west-2"
    "eu-west-1" "eu-west-2" "eu-west-3" "eu-central-1" "eu-north-1"
    "ap-southeast-1" "ap-southeast-2" "ap-northeast-1" "ap-northeast-2"
)

AZURE_REGIONS=(
    "eastus" "eastus2" "westus" "westus2" "westus3" "centralus"
    "northeurope" "westeurope" "francecentral" "germanywestcentral"
    "norwayeast" "swedencentral" "uksouth"
    "southeastasia" "eastasia" "australiaeast" "japaneast" "koreacentral"
)

GCP_REGIONS=(
    "us-central1" "us-east1" "us-east4" "us-west1" "us-west2" "us-west3"
    "europe-west1" "europe-west2" "europe-west3" "europe-west4" "europe-west6"
    "europe-north1" "asia-southeast1" "asia-southeast2" "asia-east1"
    "asia-northeast1" "asia-northeast2" "asia-south1" "australia-southeast1"
)

# Compare specific regions
echo "Comparing top AWS regions..."
compare_regions "${AWS_REGIONS[@]:0:8}"

echo -e "\n"
echo "Comparing top Azure regions..."
compare_regions "${AZURE_REGIONS[@]:0:8}"

echo -e "\n"
echo "Comparing top GCP regions..."
compare_regions "${GCP_REGIONS[@]:0:8}"
```

### Deployment Decision Script

```bash
#!/bin/bash

# Intelligent multi-region deployment decision
deploy_to_best_region() {
    local app_name=$1
    local environment=${2:-"production"}
    local max_regions=${3:-3}

    # Define region candidates by environment
    case $environment in
        "production")
            candidates=(
                "eu-north-1:aws:100"      # Sweden - very clean
                "norwayeast:azure:80"     # Norway - hydroelectric
                "us-west-2:aws:150"       # Oregon - clean hydro
                "francecentral:azure:120" # France - nuclear
                "europe-west6:gcp:150"    # Switzerland - clean
            )
            ;;
        "staging")
            candidates=(
                "us-west-2:aws:200"
                "eu-west-1:aws:250"
                "europe-west1:gcp:250"
                "westus2:azure:200"
                "northeurope:azure:250"
            )
            ;;
        "development")
            candidates=(
                "us-east-1:aws:350"
                "eastus:azure:350"
                "us-central1:gcp:350"
                "eu-central-1:aws:350"
            )
            ;;
    esac

    echo "🚀 Finding best regions for $app_name ($environment)"
    echo "===================================================="

    local deployed_count=0
    local successful_regions=()

    for candidate in "${candidates[@]}"; do
        if [ $deployed_count -ge $max_regions ]; then
            break
        fi

        IFS=':' read -r region provider threshold <<< "$candidate"

        echo "Checking $provider:$region (threshold: ${threshold})..."

        # Check carbon intensity
        result=$(carboncue check --region "$region" --threshold "$threshold" --format json 2>/dev/null)

        if [ $? -eq 0 ]; then
            intensity=$(echo "$result" | jq -r '.carbon_intensity')
            exceeded=$(echo "$result" | jq -r '.threshold_exceeded')

            if [ "$exceeded" == "false" ]; then
                echo "✅ $provider:$region - $intensity gCO2eq/kWh (within threshold)"

                # Simulate deployment
                echo "   Deploying $app_name to $provider:$region..."

                case $provider in
                    "aws")
                        deploy_to_aws "$region" "$app_name"
                        ;;
                    "azure")
                        deploy_to_azure "$region" "$app_name"
                        ;;
                    "gcp")
                        deploy_to_gcp "$region" "$app_name"
                        ;;
                esac

                if [ $? -eq 0 ]; then
                    successful_regions+=("$provider:$region:$intensity")
                    deployed_count=$((deployed_count + 1))
                    echo "   ✅ Deployment successful"
                else
                    echo "   ❌ Deployment failed"
                fi
            else
                echo "⏭️  $provider:$region - $intensity gCO2eq/kWh (exceeds threshold: ${threshold})"
            fi
        else
            echo "❌ $provider:$region - Failed to get carbon data"
        fi

        echo ""
    done

    echo "📊 Deployment Summary"
    echo "===================="
    echo "Regions deployed: $deployed_count"

    for region_info in "${successful_regions[@]}"; do
        IFS=':' read -r provider region intensity <<< "$region_info"
        echo "  - $provider:$region ($intensity gCO2eq/kWh)"
    done

    if [ $deployed_count -eq 0 ]; then
        echo "⚠️  No suitable regions found. Consider:"
        echo "   - Raising thresholds for $environment"
        echo "   - Scheduling deployment for later"
        echo "   - Using carbon offset mechanisms"
        return 1
    fi

    return 0
}

# Deployment functions (examples)
deploy_to_aws() {
    local region=$1
    local app_name=$2

    echo "   AWS deployment commands for $region:"
    echo "     aws configure set region $region"
    echo "     sam deploy --stack-name $app_name-$region"

    # Simulate success/failure
    return 0
}

deploy_to_azure() {
    local region=$1
    local app_name=$2

    echo "   Azure deployment commands for $region:"
    echo "     az configure --defaults location=$region"
    echo "     az deployment group create --name $app_name-$region"

    return 0
}

deploy_to_gcp() {
    local region=$1
    local app_name=$2

    echo "   GCP deployment commands for $region:"
    echo "     gcloud config set compute/region $region"
    echo "     gcloud run deploy $app_name --region $region"

    return 0
}

# Example usage
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <app-name> [environment] [max-regions]"
    echo "Example: $0 myapp production 2"
    exit 1
fi

deploy_to_best_region "$1" "$2" "$3"
```

## SDK Implementation

### Multi-Region Manager

```python
import asyncio
import carboncue_sdk as cc
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    DIGITAL_OCEAN = "digitalocean"

@dataclass
class RegionCandidate:
    region: str
    provider: CloudProvider
    threshold: int
    priority: int = 1  # Lower = higher priority

@dataclass
class DeploymentResult:
    region: str
    provider: CloudProvider
    carbon_intensity: float
    deployment_success: bool
    timestamp: str

class MultiRegionCarbonManager:
    """Manages carbon-aware deployments across multiple regions and providers."""

    def __init__(self, client: cc.CarbonCueClient):
        self.client = client
        self.deployment_results: List[DeploymentResult] = []

    async def find_best_regions(self,
                               candidates: List[RegionCandidate],
                               max_regions: int = 3) -> List[Tuple[RegionCandidate, float]]:
        """Find the best regions based on carbon intensity."""

        results = []

        # Check carbon intensity for all candidates
        for candidate in candidates:
            try:
                intensity_data = await self._get_carbon_intensity_async(candidate.region)
                if intensity_data.value <= candidate.threshold:
                    results.append((candidate, intensity_data.value))
            except Exception as e:
                print(f"Error checking {candidate.provider.value}:{candidate.region}: {e}")
                continue

        # Sort by carbon intensity, then by priority
        results.sort(key=lambda x: (x[1], x[0].priority))

        return results[:max_regions]

    async def _get_carbon_intensity_async(self, region: str):
        """Async wrapper for carbon intensity check."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.get_carbon_intensity,
            region
        )

    def deploy_to_regions(self,
                         regions: List[Tuple[RegionCandidate, float]],
                         app_name: str,
                         deployment_config: Dict) -> List[DeploymentResult]:
        """Deploy application to selected regions."""

        results = []

        for candidate, carbon_intensity in regions:
            print(f"🚀 Deploying to {candidate.provider.value}:{candidate.region}")
            print(f"   Carbon intensity: {carbon_intensity} gCO2eq/kWh")

            try:
                success = self._deploy_to_provider(
                    candidate.provider,
                    candidate.region,
                    app_name,
                    deployment_config
                )

                result = DeploymentResult(
                    region=candidate.region,
                    provider=candidate.provider,
                    carbon_intensity=carbon_intensity,
                    deployment_success=success,
                    timestamp=datetime.now().isoformat()
                )

                results.append(result)
                self.deployment_results.append(result)

            except Exception as e:
                print(f"❌ Deployment failed: {e}")

                result = DeploymentResult(
                    region=candidate.region,
                    provider=candidate.provider,
                    carbon_intensity=carbon_intensity,
                    deployment_success=False,
                    timestamp=datetime.now().isoformat()
                )
                results.append(result)

        return results

    def _deploy_to_provider(self,
                           provider: CloudProvider,
                           region: str,
                           app_name: str,
                           config: Dict) -> bool:
        """Deploy to specific cloud provider."""

        if provider == CloudProvider.AWS:
            return self._deploy_to_aws(region, app_name, config)
        elif provider == CloudProvider.AZURE:
            return self._deploy_to_azure(region, app_name, config)
        elif provider == CloudProvider.GCP:
            return self._deploy_to_gcp(region, app_name, config)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _deploy_to_aws(self, region: str, app_name: str, config: Dict) -> bool:
        """Deploy to AWS region."""
        # Implement AWS deployment logic
        print(f"   AWS SAM deploy to {region}")
        # Example: boto3 operations, CloudFormation, SAM CLI calls
        return True  # Simulate success

    def _deploy_to_azure(self, region: str, app_name: str, config: Dict) -> bool:
        """Deploy to Azure region."""
        # Implement Azure deployment logic
        print(f"   Azure ARM deployment to {region}")
        # Example: Azure SDK operations, ARM template deployment
        return True  # Simulate success

    def _deploy_to_gcp(self, region: str, app_name: str, config: Dict) -> bool:
        """Deploy to GCP region."""
        # Implement GCP deployment logic
        print(f"   GCP Cloud Run deployment to {region}")
        # Example: Google Cloud SDK operations
        return True  # Simulate success

    def get_deployment_summary(self) -> Dict:
        """Get summary of all deployments."""
        successful = [r for r in self.deployment_results if r.deployment_success]
        failed = [r for r in self.deployment_results if not r.deployment_success]

        total_carbon = sum(r.carbon_intensity for r in successful)
        avg_carbon = total_carbon / len(successful) if successful else 0

        return {
            "total_deployments": len(self.deployment_results),
            "successful_deployments": len(successful),
            "failed_deployments": len(failed),
            "average_carbon_intensity": avg_carbon,
            "total_carbon_footprint": total_carbon,
            "regions_deployed": [f"{r.provider.value}:{r.region}" for r in successful]
        }

# Usage example
async def main():
    client = cc.CarbonCueClient()
    manager = MultiRegionCarbonManager(client)

    # Define candidate regions for production deployment
    candidates = [
        RegionCandidate("eu-north-1", CloudProvider.AWS, 100, 1),      # Highest priority
        RegionCandidate("norwayeast", CloudProvider.AZURE, 80, 1),     # Highest priority
        RegionCandidate("us-west-2", CloudProvider.AWS, 200, 2),       # Medium priority
        RegionCandidate("europe-west6", CloudProvider.GCP, 150, 2),    # Medium priority
        RegionCandidate("francecentral", CloudProvider.AZURE, 120, 3), # Lower priority
        RegionCandidate("eu-west-1", CloudProvider.AWS, 300, 4),       # Fallback
    ]

    # Find best regions
    print("🔍 Evaluating regions for carbon-optimized deployment...")
    best_regions = await manager.find_best_regions(candidates, max_regions=3)

    if not best_regions:
        print("❌ No suitable regions found with current thresholds")
        return

    print(f"\n🌍 Selected {len(best_regions)} regions:")
    for candidate, intensity in best_regions:
        print(f"  - {candidate.provider.value}:{candidate.region} ({intensity} gCO2eq/kWh)")

    # Deploy to selected regions
    deployment_config = {
        "container_image": "myapp:latest",
        "memory": "2Gi",
        "cpu": "1000m"
    }

    print("\n🚀 Starting deployments...")
    results = manager.deploy_to_regions(best_regions, "myapp", deployment_config)

    # Summary
    summary = manager.get_deployment_summary()
    print(f"\n📊 Deployment Summary:")
    print(f"   Total deployments: {summary['total_deployments']}")
    print(f"   Successful: {summary['successful_deployments']}")
    print(f"   Average carbon intensity: {summary['average_carbon_intensity']:.1f} gCO2eq/kWh")
    print(f"   Regions deployed: {', '.join(summary['regions_deployed'])}")

if __name__ == "__main__":
    asyncio.run(main())
```

This multi-region approach enables you to automatically deploy to the most carbon-efficient regions while maintaining global application availability and performance.
