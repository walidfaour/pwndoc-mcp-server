# Testing

Guide for running and writing tests for PwnDoc MCP Server.

## Running Tests

### Prerequisites

Install development dependencies:

```bash
pip install pwndoc-mcp-server[dev]
# or
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=pwndoc_mcp_server --cov-report=html
open htmlcov/index.html
```

### Run Specific Tests

```bash
# Single file
pytest tests/test_config.py

# Single test class
pytest tests/test_config.py::TestPwnDocConfig

# Single test
pytest tests/test_config.py::TestPwnDocConfig::test_default_values

# By keyword
pytest -k "authentication"
```

### Verbose Output

```bash
pytest -v
pytest -vv  # Even more verbose
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_config.py       # Configuration tests
├── test_client.py       # API client tests
├── test_server.py       # MCP server tests
├── test_cli.py          # CLI tests
└── test_logging.py      # Logging tests
```

## Writing Tests

### Basic Test

```python
from pwndoc_mcp_server.config import PwnDocConfig

def test_config_default_values():
    config = PwnDocConfig()
    
    assert config.url == ""
    assert config.timeout == 30
    assert config.verify_ssl is True
```

### Using Fixtures

```python
import pytest

@pytest.fixture
def sample_config():
    return PwnDocConfig(
        url="https://test.pwndoc.com",
        token="test-token"
    )

def test_config_is_valid(sample_config):
    assert sample_config.is_valid() is True
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_client_list_audits(mock_client):
    mock_client.list_audits.return_value = [{"_id": "123", "name": "Test"}]
    
    result = await mock_client.list_audits()
    
    assert len(result) == 1
    assert result[0]["name"] == "Test"
```

### Mocking

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_authenticate():
    with patch("pwndoc_mcp_server.client.httpx.AsyncClient") as mock:
        mock_instance = AsyncMock()
        mock.return_value.__aenter__.return_value = mock_instance
        mock_instance.post.return_value.json.return_value = {
            "status": "success",
            "datas": {"token": "jwt-token"}
        }
        
        client = PwnDocClient(config)
        result = await client.authenticate()
        
        assert result is True
```

### Testing CLI

```python
from typer.testing import CliRunner
from pwndoc_mcp_server.cli import app

def test_version_command():
    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    
    assert result.exit_code == 0
    assert "pwndoc-mcp-server" in result.stdout
```

## Fixtures Reference

### conftest.py Fixtures

| Fixture | Description |
|---------|-------------|
| `clean_environment` | Clears PWNDOC_* env vars |
| `temp_dir` | Temporary directory |
| `temp_config_file` | Temp config file path |
| `mock_audit` | Sample audit data |
| `mock_finding` | Sample finding data |
| `mock_client` | Sample client data |
| `mock_company` | Sample company data |
| `mock_user` | Sample user data |
| `mock_statistics` | Sample statistics |
| `cli_runner` | Typer CLI test runner |

### Using Mock Data

```python
def test_audit_processing(mock_audit):
    # mock_audit is a dict with realistic audit data
    assert mock_audit["name"] == "Test Pentest Q4 2024"
    assert mock_audit["auditType"] == "Web Application"
```

## Integration Tests

### With Real PwnDoc (Optional)

```python
import pytest
import os

@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("PWNDOC_TEST_URL"),
    reason="Integration tests require PWNDOC_TEST_URL"
)
async def test_real_connection():
    config = PwnDocConfig(
        url=os.getenv("PWNDOC_TEST_URL"),
        username=os.getenv("PWNDOC_TEST_USER"),
        password=os.getenv("PWNDOC_TEST_PASS")
    )
    
    async with PwnDocClient(config) as client:
        await client.authenticate()
        audits = await client.list_audits()
        assert isinstance(audits, list)
```

Run integration tests:

```bash
PWNDOC_TEST_URL=https://test.pwndoc.com \
PWNDOC_TEST_USER=testuser \
PWNDOC_TEST_PASS=testpass \
pytest -m integration
```

## Test Categories

### Unit Tests

Test individual functions/methods in isolation:

```python
def test_rate_limiter_acquire():
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    
    for _ in range(5):
        assert limiter.acquire() is True
    
    assert limiter.acquire() is False
```

### Functional Tests

Test complete features:

```python
@pytest.mark.asyncio
async def test_create_and_delete_audit():
    # Create
    result = await server.handle_call_tool("create_audit", {
        "name": "Test Audit",
        "audit_type": "Web",
        "language": "en"
    })
    audit_id = json.loads(result)["_id"]
    
    # Delete
    await server.handle_call_tool("delete_audit", {"audit_id": audit_id})
```

### CLI Tests

Test command-line interface:

```python
def test_config_init_creates_file(runner, temp_dir):
    os.environ["PWNDOC_CONFIG_FILE"] = f"{temp_dir}/config.yaml"
    
    result = runner.invoke(app, ["config", "init"], input="url\nuser\npass\n")
    
    assert result.exit_code == 0
    assert os.path.exists(f"{temp_dir}/config.yaml")
```

## CI/CD Testing

Tests run automatically on GitHub Actions:

```yaml
# .github/workflows/ci.yml
test:
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      os: [ubuntu-latest, macos-latest, windows-latest]
      python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - run: pip install -e ".[dev]"
    - run: pytest --cov
```

## Code Quality

### Linting

```bash
ruff check .
ruff check --fix .
```

### Formatting

```bash
black .
black --check .
```

### Type Checking

```bash
mypy src/
```

### All Checks

```bash
# Run all quality checks
ruff check .
black --check .
mypy src/
pytest --cov
```

## Coverage Goals

| Module | Target |
|--------|--------|
| config | 90% |
| client | 85% |
| server | 80% |
| cli | 75% |
| logging | 80% |

View coverage report:

```bash
pytest --cov=pwndoc_mcp_server --cov-report=term-missing
```
