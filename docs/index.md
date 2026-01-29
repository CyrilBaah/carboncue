# CarbonCue Documentation

**Carbon-Aware GitHub Action, CLI, and SDK for sustainable software development**

![CarbonCue Logo](https://img.shields.io/badge/Carbon-Aware-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Overview

CarbonCue helps developers measure and reduce the carbon footprint of their software by integrating carbon-awareness into development workflows. It provides real-time carbon intensity data and calculates Software Carbon Intensity (SCI) scores for cloud regions.

## Features

- 🎯 **GitHub Action** - Gate CI/CD workflows based on carbon intensity thresholds
- 💻 **CLI** - Terminal interface for carbon-aware development with real-time intensity checking
- 🔧 **SDK** - Python library for integrating carbon-awareness into applications
- ☁️ **Multi-Cloud** - Support for AWS, Azure, GCP, DigitalOcean, and more
- 📊 **SCI Calculator** - Software Carbon Intensity calculations per GSF specification
- 🌍 **Real-Time Data** - Live carbon intensity from Electricity Maps API

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quickstart.md)
- [API Reference](reference/carboncue_sdk/)
- [GitHub Repository](https://github.com/CyrilBaah/carboncue)

## How It Works

CarbonCue integrates with the [Electricity Maps API](https://www.electricitymap.org/) to fetch real-time carbon intensity data for different regions. It then:

1. Maps your cloud provider region (e.g., `us-west-2`) to the corresponding electrical grid zone
2. Fetches current carbon intensity in gCO2eq/kWh
3. Calculates your Software Carbon Intensity (SCI) score
4. Helps you make carbon-aware decisions about when and where to run workloads

## Green Software Foundation

CarbonCue is built on [Green Software Foundation](https://greensoftware.foundation/) principles:

- **Carbon Awareness**: Run software when and where electricity is cleanest
- **Energy Efficiency**: Optimize code to use less energy
- **Carbon Measurement**: Calculate the SCI score for your software

## Getting Started

=== "GitHub Action"

    ```yaml
    name: Carbon-Aware Deployment
    on: [push, pull_request]

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          
          - name: Check Carbon Intensity
            uses: CyrilBaah/carboncue@v1.0.0
            with:
              region: us-west-2
              cloud-provider: aws
              threshold: 200
          
          - name: Deploy
            run: echo "Deploying with low carbon intensity!"
    ```

=== "CLI"

    ```bash
    # Install
    pip install carboncue-cli

    # Check current carbon intensity
    carboncue check --region us-west-2 --provider aws

    # Calculate SCI score
    carboncue sci -o 100 -m 50 -r 1000 --region us-west-2
    ```

=== "SDK"

    ```python
    import asyncio
    from carboncue_sdk import CarbonClient

    async def main():
        # Note: Set CARBONCUE_ELECTRICITY_MAPS_API_KEY for real-time data
        async with CarbonClient() as client:
            # Check carbon intensity (requires API key)
            intensity = await client.get_current_intensity(
                region="us-west-2",
                provider="aws"
            )
            print(f"Current: {intensity.carbon_intensity} gCO2eq/kWh")

        # Calculate SCI score (no API key needed)
        client = CarbonClient()
        sci = client.calculate_sci(
                operational_emissions=100,
                embodied_emissions=50,
                functional_unit=1000
            )
            print(f"SCI Score: {sci.score}")

    asyncio.run(main())
    ```

## Support

- [GitHub Issues](https://github.com/CyrilBaah/carboncue/issues)
- [Discussions](https://github.com/CyrilBaah/carboncue/discussions)
- [Contributing Guide](CONTRIBUTING.md)

## License

CarbonCue is released under the [MIT License](https://opensource.org/licenses/MIT).
