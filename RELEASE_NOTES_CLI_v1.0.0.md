# CarbonCue CLI v1.0.0 - Release Notes

## 🎉 First Stable Release!

We're excited to announce the first stable release of **CarbonCue CLI** - a terminal interface for carbon-aware development based on Green Software Foundation (GSF) principles.

## 📦 Installation

```bash
pip install carboncue-cli
```

## ✨ What's New

### Core Commands

#### 🔍 `carboncue check` - Carbon Intensity Checker
Get real-time carbon intensity data for cloud regions:
```bash
carboncue check --region us-west-2 --provider aws
carboncue check -r westeurope -p azure
```

**Features:**
- ✅ Multi-cloud support (AWS, Azure, GCP, DigitalOcean, others)
- ✅ Real-time data from Electricity Maps API
- ✅ Beautiful rich terminal output
- ✅ Color-coded status indicators (green/yellow/red)
- ✅ Fossil fuel & renewable percentage display

#### 📊 `carboncue sci` - SCI Score Calculator
Calculate Software Carbon Intensity per GSF specification:
```bash
carboncue sci -o 100 -m 50 -r 1000 -t requests --region us-west-2
```

**Features:**
- ✅ GSF compliant formula: `SCI = (O + M) / R`
- ✅ Operational emissions (O) tracking
- ✅ Embodied emissions (M) calculation  
- ✅ Functional unit (R) normalization
- ✅ Detailed breakdown with actionable recommendations

#### ⚙️ `carboncue config` - Configuration Viewer
Display current settings and environment configuration.

### 🎨 User Experience

- 🌈 **Beautiful Terminal UI** - Rich library integration for gorgeous output
- 🎯 **Smart Recommendations** - Contextual advice based on carbon intensity levels
- ⚡ **Fast & Responsive** - Async operations with loading indicators
- 📝 **Clear Error Messages** - Helpful guidance when things go wrong

### 🔧 Configuration Options

Environment variables or `.env` file:
```bash
CARBONCUE_ELECTRICITY_MAPS_API_KEY=your_api_key
CARBONCUE_DEFAULT_REGION=us-west-2
CARBONCUE_DEFAULT_CLOUD_PROVIDER=aws
```

## 🌍 Use Cases

### Development
```bash
# Check before running intensive tasks
carboncue check -r us-east-1 -p aws
```

### CI/CD Integration
```bash
# Conditional testing based on carbon intensity
INTENSITY=$(carboncue check -r us-west-2 -p aws --json | jq '.carbon_intensity')
if [ $INTENSITY -lt 200 ]; then
  pytest  # Run full suite
else
  pytest -m critical  # Run only critical tests
fi
```

### Monitoring
```bash
# Continuous carbon monitoring
while true; do
  carboncue check -r us-west-2 -p aws
  sleep 3600
done
```

## 📚 Documentation

- [README](https://github.com/CyrilBaah/carboncue/blob/master/packages/cli/README.md) - Comprehensive usage guide
- [CHANGELOG](https://github.com/CyrilBaah/carboncue/blob/master/packages/cli/CHANGELOG.md) - Detailed change history

## 🛠️ Technical Specifications

- **Python**: >= 3.11
- **License**: MIT
- **Package**: `carboncue-cli`
- **Command**: `carboncue`

### Dependencies
- `carboncue-sdk` >= 0.1.0 - Core carbon calculation SDK
- `click` >= 8.1.8 - CLI framework
- `rich` >= 13.9.4 - Terminal formatting
- `python-dotenv` >= 1.0.1 - Environment configuration

## 🚀 Quick Start

```bash
# Install
pip install carboncue-cli

# Check carbon intensity
carboncue check --region us-west-2 --provider aws

# Calculate SCI score
carboncue sci -o 100 -m 50 -r 1000 -t requests

# View config
carboncue config
```

## 🙏 Acknowledgments

Built on [Green Software Foundation](https://greensoftware.foundation/) principles and methodologies.

## 📝 Notes for PyPI Publication

### Pre-release Checklist
- ✅ Package builds successfully (`python -m build`)
- ✅ All dependencies specified in `pyproject.toml`
- ✅ README.md with comprehensive documentation
- ✅ MIT License included
- ✅ Version set to 1.0.0 in `pyproject.toml`
- ✅ Entry point configured (`carboncue` command)
- ✅ Python >= 3.11 requirement specified

### PyPI Publishing Steps

1. **Set up PyPI Trusted Publishing** (recommended):
   - Go to https://pypi.org/manage/account/publishing/
   - Add trusted publisher for `CyrilBaah/carboncue`
   - Workflow: `publish-cli.yml`
   - Environment: Not required (leave empty)

2. **Create the Release**:
   - Tag format: `cli-v1.0.0`
   - This will automatically trigger the publish workflow
   - The workflow will build and publish to PyPI

3. **Manual Publishing** (alternative):
   ```bash
   cd packages/cli
   python -m build
   twine upload dist/*
   ```

### What Happens Next?

Once you publish this release with tag `cli-v1.0.0`:
1. ✅ GitHub Actions workflow triggers automatically
2. ✅ Package is built in isolated environment
3. ✅ Artifacts are verified
4. ✅ Published to PyPI using trusted publishing
5. ✅ Users can `pip install carboncue-cli`

## 🔗 Links

- **PyPI**: https://pypi.org/project/carboncue-cli/ (after publication)
- **GitHub**: https://github.com/CyrilBaah/carboncue
- **Issues**: https://github.com/CyrilBaah/carboncue/issues
- **Discussions**: https://github.com/CyrilBaah/carboncue/discussions

---

**Ready to reduce your software's carbon footprint? Install CarbonCue CLI today!** 🌱
