# PwnDoc MCP Server - Python

Full-featured Python implementation with pip, Docker, and comprehensive CLI.

See the [main README](../README.md) for complete documentation.

## Quick Start

```bash
# Install
pip install pwndoc-mcp-server[cli]

# Configure
export PWNDOC_URL="https://your-pwndoc.com"
export PWNDOC_TOKEN="your-token"

# Test
pwndoc-mcp test

# Run
pwndoc-mcp serve
```

## Development

```bash
# Install dev dependencies
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=pwndoc_mcp_server --cov-report=html

# Linting
ruff check src/
black --check src/
mypy src/
```

## Project Structure

```
python/
├── src/pwndoc_mcp_server/
│   ├── __init__.py           # Package init
│   ├── server.py             # MCP server (89 tools)
│   ├── client.py             # PwnDoc API client
│   ├── config.py             # Configuration
│   ├── cli.py                # Rich CLI
│   └── logging_config.py     # Logging
├── tests/                    # Test suite
├── pyproject.toml            # Package config
├── Dockerfile                # Docker build
├── docker-compose.yml        # Docker Compose
└── pytest.ini                # Pytest config
```
