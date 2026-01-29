.PHONY: help install install-dev test test-unit test-integration test-contract lint format type-check clean build publish-test publish init

# Variables
PYTHON := python
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy

help: ## Show this help message
	@echo "CarbonCue - Carbon-Aware Development Tools"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

init: ## Initialize project (first-time setup)
	@echo "🔧 Initializing CarbonCue project..."
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	pre-commit install
	@echo "✅ Project initialized! Run 'make test' to verify."

install: ## Install production dependencies
	@echo "📦 Installing CarbonCue..."
	$(PIP) install --upgrade pip
	$(PIP) install -e .

install-dev: ## Install development dependencies
	@echo "📦 Installing development dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	pre-commit install

test: ## Run all tests
	@echo "🧪 Running all tests..."
	$(PYTEST) tests/ -v --cov=packages --cov-report=term-missing --cov-report=html

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	$(PYTEST) tests/unit/ -v

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	$(PYTEST) tests/integration/ -v

test-contract: ## Run contract tests only
	@echo "🧪 Running contract tests..."
	$(PYTEST) tests/contract/ -v

test-watch: ## Run tests in watch mode
	@echo "🧪 Running tests in watch mode..."
	$(PYTEST) tests/ -v --cov=packages -f

lint: ## Run linting checks
	@echo "🔍 Running linters..."
	$(RUFF) check packages/ tests/
	$(BLACK) --check packages/ tests/

format: ## Format code with black and ruff
	@echo "✨ Formatting code..."
	$(BLACK) packages/ tests/
	$(RUFF) check --fix packages/ tests/

type-check: ## Run type checking with mypy
	@echo "🔍 Running type checks..."
	$(MYPY) packages/sdk/src packages/cli/src

check: lint type-check test ## Run all checks (lint, type-check, test)
	@echo "✅ All checks passed!"

docs-serve: ## Serve documentation locally with auto-reload
	@echo "📚 Serving documentation at http://127.0.0.1:8000"
	mkdocs serve

docs-build: ## Build documentation static site
	@echo "📚 Building documentation..."
	mkdocs build

docs-deploy: ## Deploy documentation to GitHub Pages
	@echo "📚 Deploying documentation to GitHub Pages..."
	mkdocs gh-deploy --force

clean: ## Clean build artifacts and cache
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned!"

build: clean ## Build distribution packages
	@echo "📦 Building packages..."
	$(PYTHON) -m build

publish-test: build ## Publish to TestPyPI
	@echo "📤 Publishing to TestPyPI..."
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish: build ## Publish to PyPI (production)
	@echo "📤 Publishing to PyPI..."
	@echo "⚠️  This will publish to production PyPI!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(PYTHON) -m twine upload dist/*; \
	else \
		echo "❌ Publish cancelled."; \
	fi

pre-commit: ## Run pre-commit hooks on all files
	@echo "🔍 Running pre-commit hooks..."
	pre-commit run --all-files

action-test: ## Test GitHub Action locally
	@echo "🎬 Testing GitHub Action..."
	@echo "Note: This requires 'act' to be installed (brew install act)"
	@which act > /dev/null || (echo "❌ 'act' not found. Install with: brew install act" && exit 1)
	act -j test-action

version-bump-patch: ## Bump patch version (0.1.0 -> 0.1.1)
	@echo "📈 Bumping patch version..."
	@current=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	new=$$(echo $$current | awk -F. '{$$3=$$3+1; print $$1"."$$2"."$$3}'); \
	sed -i.bak "s/version = \"$$current\"/version = \"$$new\"/" pyproject.toml && rm pyproject.toml.bak; \
	echo "Version bumped: $$current -> $$new"

version-bump-minor: ## Bump minor version (0.1.0 -> 0.2.0)
	@echo "📈 Bumping minor version..."
	@current=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	new=$$(echo $$current | awk -F. '{$$2=$$2+1; $$3=0; print $$1"."$$2"."$$3}'); \
	sed -i.bak "s/version = \"$$current\"/version = \"$$new\"/" pyproject.toml && rm pyproject.toml.bak; \
	echo "Version bumped: $$current -> $$new"

version-bump-major: ## Bump major version (0.1.0 -> 1.0.0)
	@echo "📈 Bumping major version..."
	@current=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	new=$$(echo $$current | awk -F. '{$$1=$$1+1; $$2=0; $$3=0; print $$1"."$$2"."$$3}'); \
	sed -i.bak "s/version = \"$$current\"/version = \"$$new\"/" pyproject.toml && rm pyproject.toml.bak; \
	echo "Version bumped: $$current -> $$new"

# Quick commands for common workflows
dev: install-dev ## Alias for install-dev
qa: check ## Alias for check (quality assurance)

# Show current version
version: ## Show current version
	@grep '^version = ' pyproject.toml | cut -d'"' -f2
