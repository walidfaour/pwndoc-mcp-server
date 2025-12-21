# Building from Source

Guide for building PwnDoc MCP Server from source code.

## Prerequisites

- Python 3.8 or higher
- pip
- git
- (Optional) Docker for container builds
- (Optional) Nuitka for binary compilation

## Clone Repository

```bash
git clone https://github.com/walidfaour/pwndoc-mcp-server.git
cd pwndoc-mcp-server
```

## Development Setup

### Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Install in Development Mode

```bash
# Install with all development dependencies
pip install -e ".[dev]"
```

This installs:
- Core dependencies (httpx, pyyaml)
- CLI dependencies (typer, rich)
- SSE dependencies (aiohttp)
- Dev tools (pytest, black, ruff, mypy)

### Verify Installation

```bash
pwndoc-mcp --version
python -c "import pwndoc_mcp_server; print(pwndoc_mcp_server.__version__)"
```

## Project Structure

```
pwndoc-mcp-server/
├── src/
│   └── pwndoc_mcp_server/
│       ├── __init__.py      # Package exports
│       ├── cli.py           # CLI commands
│       ├── client.py        # PwnDoc API client
│       ├── config.py        # Configuration management
│       ├── logging_config.py # Logging setup
│       └── server.py        # MCP server
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_cli.py
│   ├── test_client.py
│   ├── test_config.py
│   ├── test_logging.py
│   └── test_server.py
├── docs/                    # Documentation
├── assets/                  # Logo and branding
├── debian/                  # Debian packaging
├── rpm/                     # RPM packaging
├── packaging/               # Homebrew, Scoop
├── pyproject.toml           # Build configuration
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Building

### Python Package

```bash
# Install build tools
pip install build

# Build wheel and sdist
python -m build

# Output in dist/
ls dist/
# pwndoc_mcp_server-1.0.2-py3-none-any.whl
# pwndoc_mcp_server-1.0.2.tar.gz
```

### Docker Image

```bash
# Build standard image
docker build -t pwndoc-mcp-server .

# Build with tag
docker build -t pwndoc-mcp-server:1.0.2 .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t pwndoc-mcp-server .
```

### Standalone Binary (Nuitka)

```bash
# Install Nuitka
pip install nuitka

# Build standalone binary
python -m nuitka \
  --standalone \
  --onefile \
  --output-filename=pwndoc-mcp-server \
  --include-package=pwndoc_mcp_server \
  src/pwndoc_mcp_server/cli.py

# Output: pwndoc-mcp-server (or .exe on Windows)
```

### Debian Package

```bash
# Install build dependencies
sudo apt install dpkg-dev debhelper

# Build .deb
dpkg-buildpackage -us -uc -b

# Output: ../pwndoc-mcp-server_1.0.2_amd64.deb
```

### RPM Package

```bash
# Install build dependencies
sudo dnf install rpm-build

# Build .rpm
rpmbuild -bb rpm/pwndoc-mcp-server.spec

# Output: ~/rpmbuild/RPMS/x86_64/pwndoc-mcp-server-1.0.2-1.x86_64.rpm
```

## Running Tests

### All Tests

```bash
pytest
```

### With Coverage

```bash
pytest --cov=pwndoc_mcp_server --cov-report=html
open htmlcov/index.html
```

### Specific Tests

```bash
# Single file
pytest tests/test_config.py

# Single test
pytest tests/test_config.py::TestPwnDocConfig::test_default_values

# By marker
pytest -m "not slow"
```

### Test with Different Python Versions

```bash
# Using tox
pip install tox
tox

# Or manually
python3.8 -m pytest
python3.11 -m pytest
```

## Code Quality

### Linting

```bash
# Run ruff linter
ruff check src/

# Auto-fix issues
ruff check --fix src/
```

### Formatting

```bash
# Check formatting
black --check src/

# Apply formatting
black src/
```

### Type Checking

```bash
mypy src/pwndoc_mcp_server/
```

### All Checks

```bash
# Run all quality checks
ruff check src/
black --check src/
mypy src/pwndoc_mcp_server/
pytest
```

## Continuous Integration

The project uses GitHub Actions for CI/CD:

```yaml
# .github/workflows/ci.yml
# Runs on every push/PR:
# - Linting (ruff, black)
# - Type checking (mypy)
# - Tests (pytest) on Python 3.8-3.12
# - Build verification
```

## Release Process

### Version Bump

1. Update version in `src/pwndoc_mcp_server/__init__.py`
2. Update CHANGELOG.md
3. Commit: `git commit -m "Bump version to 1.1.0"`
4. Tag: `git tag v1.1.0`
5. Push: `git push && git push --tags`

### Automated Release

When a tag is pushed:
1. CI builds all artifacts
2. Creates GitHub Release
3. Publishes to PyPI
4. Pushes Docker image to ghcr.io

### Manual PyPI Publish

```bash
# Build
python -m build

# Upload to PyPI
twine upload dist/*
```

## Development Workflow

### Feature Development

```bash
# Create feature branch
git checkout -b feature/new-tool

# Make changes
# ...

# Run tests
pytest

# Format and lint
black src/
ruff check --fix src/

# Commit
git commit -m "Add new tool for X"

# Push and create PR
git push -u origin feature/new-tool
```

### Adding a New Tool

1. Add tool definition in `server.py`:
   ```python
   TOOL_DEFINITIONS.append({
       "name": "new_tool",
       "description": "...",
       "inputSchema": {...}
   })
   ```

2. Add handler method:
   ```python
   async def handle_new_tool(self, params):
       # Implementation
   ```

3. Add to tool dispatcher:
   ```python
   "new_tool": self.handle_new_tool
   ```

4. Add tests in `test_server.py`

5. Document in `docs/tools/`

## Troubleshooting

### Import Errors

```bash
# Reinstall in dev mode
pip install -e ".[dev]" --force-reinstall
```

### Test Failures

```bash
# Run with verbose output
pytest -v --tb=long
```

### Build Issues

```bash
# Clean build artifacts
rm -rf build/ dist/ *.egg-info

# Rebuild
python -m build
```
