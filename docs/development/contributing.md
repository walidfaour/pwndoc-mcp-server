# Contributing Guide

Thank you for your interest in contributing to PwnDoc MCP Server!

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A PwnDoc instance for testing (optional)

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/pwndoc-mcp-server.git
cd pwndoc-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev]"

# Verify installation
pwndoc-mcp --version
pytest --version
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

Follow the code style guidelines below.

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pwndoc_mcp_server

# Run specific tests
pytest tests/test_config.py -v
```

### 4. Check Code Quality

```bash
# Linting
ruff check .

# Formatting
black --check .

# Type checking
mypy src/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Description |
|--------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `style:` | Formatting |
| `refactor:` | Code refactoring |
| `test:` | Adding tests |
| `chore:` | Maintenance |

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub.

## Code Style

### Python Style

We follow PEP 8 with these tools:

- **Black** for formatting
- **Ruff** for linting
- **mypy** for type checking

```python
# Good
async def get_audit(self, audit_id: str) -> Dict[str, Any]:
    """Get audit by ID.
    
    Args:
        audit_id: The audit's MongoDB ObjectId.
        
    Returns:
        Audit data as dictionary.
        
    Raises:
        NotFoundError: If audit doesn't exist.
    """
    return await self._request("GET", f"/api/audits/{audit_id}")

# Bad
async def get_audit(self,audit_id):
    return await self._request("GET","/api/audits/"+audit_id)
```

### Docstrings

Use Google-style docstrings:

```python
def create_finding(
    self,
    audit_id: str,
    title: str,
    description: str = "",
    severity: str = "Medium",
) -> Dict[str, Any]:
    """Create a new finding in an audit.
    
    Args:
        audit_id: The parent audit ID.
        title: Finding title.
        description: Detailed description.
        severity: Severity level (Critical, High, Medium, Low).
        
    Returns:
        Created finding data.
        
    Raises:
        NotFoundError: If audit doesn't exist.
        ValidationError: If required fields are missing.
        
    Example:
        >>> finding = await client.create_finding(
        ...     audit_id="123",
        ...     title="SQL Injection",
        ...     severity="Critical"
        ... )
    """
```

### Type Hints

Always use type hints:

```python
from typing import Dict, List, Optional, Any

async def list_audits(
    self,
    finding_title: Optional[str] = None,
) -> List[Dict[str, Any]]:
    ...
```

## Adding New Tools

### 1. Add to Client

```python
# src/pwndoc_mcp_server/client.py

async def new_tool_method(self, param: str) -> Dict[str, Any]:
    """Description of what this does.
    
    Args:
        param: Description of parameter.
        
    Returns:
        Description of return value.
    """
    return await self._request("GET", f"/api/endpoint/{param}")
```

### 2. Add Tool Definition

```python
# src/pwndoc_mcp_server/server.py

TOOL_DEFINITIONS.append({
    "name": "new_tool",
    "description": "Description shown to AI",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param"]
    }
})
```

### 3. Add Handler

```python
# src/pwndoc_mcp_server/server.py

async def handle_call_tool(self, name: str, arguments: Dict) -> str:
    ...
    elif name == "new_tool":
        result = await self.client.new_tool_method(arguments["param"])
        return self._format_result(result)
```

### 4. Add Tests

```python
# tests/test_server.py

@pytest.mark.asyncio
async def test_new_tool(server):
    with patch.object(server.client, "new_tool_method") as mock:
        mock.return_value = {"status": "success"}
        
        result = await server.handle_call_tool("new_tool", {"param": "test"})
        
        assert result is not None
        mock.assert_called_once_with("test")
```

### 5. Update Documentation

Add to `docs/tools/` appropriate category file.

## Testing Guidelines

### Unit Tests

Test individual functions in isolation:

```python
def test_config_validation():
    config = PwnDocConfig(url="https://test.com", token="abc")
    assert config.is_valid() is True
```

### Integration Tests

Test components working together:

```python
@pytest.mark.asyncio
async def test_full_workflow(mock_client):
    # Create audit
    audit = await mock_client.create_audit(...)
    
    # Add finding
    finding = await mock_client.create_finding(audit["_id"], ...)
    
    # Verify
    result = await mock_client.get_audit(audit["_id"])
    assert len(result["findings"]) == 1
```

### Fixtures

Use fixtures for reusable test data:

```python
@pytest.fixture
def sample_finding():
    return {
        "title": "Test Finding",
        "severity": "High",
        "description": "Test description"
    }

def test_finding_creation(sample_finding):
    assert sample_finding["severity"] == "High"
```

## Documentation

### README Updates

Update README.md for:
- New features
- Changed behavior
- New installation methods

### Changelog

Update CHANGELOG.md:

```markdown
## [Unreleased]

### Added
- New `new_tool` for doing X

### Fixed
- Bug in Y when Z
```

### Docstrings

All public functions need docstrings.

## Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow conventional commits
- [ ] PR description explains changes

## Getting Help

- **Questions**: Open a [Discussion](https://github.com/walidfaour/pwndoc-mcp-server/discussions)
- **Bugs**: Open an [Issue](https://github.com/walidfaour/pwndoc-mcp-server/issues)
- **Security**: See [SECURITY.md](https://github.com/walidfaour/pwndoc-mcp-server/blob/main/SECURITY.md)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
