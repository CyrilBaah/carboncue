# CarbonCue CLI v1.0.0 - PyPI Release

## 🎉 Initial Release

We're excited to announce the first stable release of **CarbonCue CLI** - a terminal interface for carbon-aware development!

## 📦 Installation

```bash
pip install carboncue-cli
```

## ✨ What's Included

### Core Features
- **Carbon Intensity Checking**: Monitor real-time grid carbon intensity for your region
- **Rich Terminal Output**: Beautiful, formatted displays using Rich library
- **Easy Configuration**: Support for `.env` files via python-dotenv
- **Seamless SDK Integration**: Built on top of the CarbonCue SDK

### Command-Line Interface
```bash
# Check current carbon intensity
carboncue check --region us-west-2

# Configure your API key
carboncue config --api-key YOUR_API_KEY
```

## 🔧 Technical Details

### Dependencies
- **carboncue-sdk** (>=0.1.0) - Core SDK functionality
- **click** (>=8.1.8) - Robust CLI framework
- **rich** (>=13.9.4) - Beautiful terminal formatting
- **python-dotenv** (>=1.0.1) - Environment configuration

### Requirements
- Python 3.11 or higher
- MIT Licensed

### Package Structure
- Built with **Hatchling** build backend
- Proper PyPI metadata and classifiers
- Entry point: `carboncue` command
- Comprehensive test coverage (unit, integration, contract tests)

## 🚀 Getting Started

1. **Install the CLI**:
   ```bash
   pip install carboncue-cli
   ```

2. **Set up your configuration** (optional):
   ```bash
   export CARBONCUE_API_KEY=your_api_key_here
   # or create a .env file
   ```

3. **Start using carbon-aware workflows**:
   ```bash
   carboncue check --region us-west-2
   ```

## 📊 Use Cases

- **Pre-commit Checks**: Verify carbon intensity before running resource-intensive builds
- **CI/CD Integration**: Make deployment decisions based on grid carbon levels
- **Developer Awareness**: Build carbon consciousness into daily workflows
- **Reporting**: Generate carbon metrics for sustainability reports

## 🌱 Green Software Foundation Alignment

CarbonCue CLI follows [Green Software Foundation](https://greensoftware.foundation/) principles:
- Real-time carbon intensity data
- Software Carbon Intensity (SCI) score support
- Energy-efficient development practices
- Carbon-aware decision making

## 🔗 Related Packages

- **CarbonCue SDK**: [carboncue-sdk](https://pypi.org/project/carboncue-sdk/) - Python library
- **CarbonCue Action**: GitHub Action for CI/CD workflows
- **CarbonCue Dashboard**: Web-based carbon monitoring

## 📝 Checklist for PyPI Release

### ✅ Completed
- [x] Package builds successfully (`python -m build`)
- [x] All tests passing (unit, integration, contract)
- [x] Proper version number (1.0.0)
- [x] README.md with usage instructions
- [x] CHANGELOG.md created
- [x] MIT License included
- [x] Dependencies properly specified
- [x] Entry points configured (`carboncue` command)
- [x] Python version requirement (>=3.11)
- [x] Build backend configured (Hatchling)
- [x] Package metadata complete

### 📋 Pre-Release Steps

Before publishing to PyPI, ensure:

1. **Test the build locally**:
   ```bash
   cd packages/cli
   python -m build
   pip install dist/carboncue_cli-1.0.0-py3-none-any.whl
   carboncue --help
   ```

2. **Test on TestPyPI first** (recommended):
   ```bash
   python -m twine upload --repository testpypi dist/*
   pip install --index-url https://test.pypi.org/simple/ carboncue-cli
   ```

3. **Create GitHub release**:
   - Tag: `cli-v1.0.0`
   - Title: `CarbonCue CLI v1.0.0`
   - Include release notes
   - Attach built distributions

4. **Publish to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```

5. **Verify installation**:
   ```bash
   pip install carboncue-cli
   carboncue --version
   ```

## 🎯 Next Steps

After successful PyPI publication:
- [ ] Update main README with PyPI badges
- [ ] Announce on social media / developer communities
- [ ] Create documentation site
- [ ] Add PyPI version badge to repository
- [ ] Monitor PyPI download statistics
- [ ] Set up automated releases via GitHub Actions

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](../../LICENSE) for details.

## 🙏 Acknowledgments

Built following Green Software Foundation principles and best practices for sustainable software development.

---

**Ready to make your development workflow carbon-aware? Install now:**
```bash
pip install carboncue-cli
```
