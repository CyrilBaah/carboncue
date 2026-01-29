# Installation

## Requirements

- Python 3.11 or higher
- pip package manager

## Installation Options

### SDK Only

For integrating carbon-awareness into your Python applications:

```bash
pip install carboncue-sdk
```

### CLI Tool

For terminal usage and carbon checks:

```bash
pip install carboncue-cli
```

The CLI automatically includes the SDK as a dependency.

### Development Installation

For contributing to CarbonCue:

```bash
# Clone the repository
git clone https://github.com/CyrilBaah/carboncue.git
cd carboncue

# Install with development dependencies
pip install -e ".[dev,docs]"

# Install pre-commit hooks
pre-commit install
```

### GitHub Action

No installation required! Simply reference the action in your workflow:

```yaml
- uses: CyrilBaah/carboncue@v1.0.0
```

## Verify Installation

### SDK

```python
import carboncue_sdk
print(carboncue_sdk.__version__)
```

### CLI

```bash
carboncue --version
```

## Configuration

### API Key Requirement

CarbonCue has **different requirements** depending on which features you use:

- ✅ **No API key needed** for SCI calculations (`calculate_sci()`)
- ✅ **No API key needed** for region mapping utilities
- ⚠️ **API key required** for real-time carbon intensity data (`get_current_intensity()`)

### Get an API Key

1. Visit [Electricity Maps](https://www.electricitymap.org/)
2. Sign up for a free or paid account
3. Generate an API key from your dashboard

### Set Environment Variable

=== "Linux/macOS"

    ```bash
    export CARBONCUE_ELECTRICITY_MAPS_API_KEY="your-api-key-here"
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:CARBONCUE_ELECTRICITY_MAPS_API_KEY="your-api-key-here"
    ```

=== ".env file"

    Create a `.env` file in your project root:

    ```bash
    CARBONCUE_ELECTRICITY_MAPS_API_KEY=your-api-key-here
    ```

### For GitHub Actions

Add the API key as a repository secret:

1. Go to your repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `ELECTRICITY_MAPS_API_KEY`
4. Value: Your API key
5. Use in workflow:

```yaml
- uses: CyrilBaah/carboncue@v1.0.0
  env:
    CARBONCUE_ELECTRICITY_MAPS_API_KEY: ${{ secrets.ELECTRICITY_MAPS_API_KEY }}
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Configuration Options](configuration.md)
- [API Reference](../reference/carboncue_sdk/)
