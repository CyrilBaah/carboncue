# Changelog

All notable changes to the CarbonCue CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-19

### Added
- Initial release of CarbonCue CLI
- Terminal interface for carbon-aware development
- Integration with CarbonCue SDK for carbon intensity data
- Rich terminal output with formatted displays
- Click-based command-line interface
- Support for .env configuration via python-dotenv
- PyPI-ready package structure with proper metadata

### Features
- Check current carbon intensity for regions
- Carbon-aware development workflow integration
- Real-time grid carbon intensity monitoring
- Clean, user-friendly terminal interface

### Dependencies
- carboncue-sdk>=0.1.0 - Core SDK functionality
- click>=8.1.8 - Command-line interface framework
- rich>=13.9.4 - Rich terminal formatting
- python-dotenv>=1.0.1 - Environment configuration

### Development
- pytest>=8.3.4 - Testing framework
- pytest-asyncio>=0.25.2 - Async testing support
- Built with Hatchling build backend
- Requires Python 3.11+

[1.0.0]: https://github.com/CyrilBaah/carboncue/releases/tag/cli-v1.0.0
