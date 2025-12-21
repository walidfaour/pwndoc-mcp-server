# Contributing to PwnDoc MCP Server

First off, thank you for considering contributing to PwnDoc MCP Server! It's people like you that make this tool better for the security community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A PwnDoc instance for testing (optional, mocks available)

### Quick Start

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/pwndoc-mcp-server.git
cd pwndoc-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linters
ruff check .
black --check .
mypy src/
```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs. **actual behavior**
- **Environment details** (OS, Python version, PwnDoc version)
- **Error messages** or logs (sanitize any credentials!)
- **Screenshots** if applicable

### Suggesting Features

Feature requests are welcome! Please:

1. Check if the feature has already been requested
2. Describe the use case and benefit
3. Explain how it would work
4. Consider if it fits the project scope

### Code Contributions

#### Good First Issues

Look for issues labeled `good first issue` - these are great starting points.

#### What We Need

- Bug fixes
- New PwnDoc API endpoint support
- Documentation improvements
- Test coverage improvements
- Performance optimizations
- Platform compatibility fixes

## Development Setup

### Git Configuration

First, configure your Git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Full Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pwndoc-mcp-server.git
cd pwndoc-mcp-server

# Add upstream remote
git remote add upstream https://github.com/walidfaour/pwndoc-mcp-server.git

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install all development dependencies
pip install -e ".[all,dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
pytest
ruff check .
black --check .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pwndoc_mcp_server --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::test_authentication

# Run with verbose output
pytest -v
```

### Running Linters

```bash
# Check code style
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
black .

# Check types
mypy src/

# Run all checks
pre-commit run --all-files
```

## Pull Request Process

### Before Submitting

1. **Update your fork** with the latest upstream changes
2. **Create a feature branch** from `main`
3. **Write tests** for new functionality
4. **Update documentation** if needed
5. **Run all tests and linters**
6. **Update CHANGELOG.md** if applicable

### Branch Naming

Use descriptive branch names:
- `feature/add-bulk-export`
- `fix/authentication-retry`
- `docs/improve-installation-guide`
- `refactor/client-error-handling`

### Submitting

1. Push your branch to your fork
2. Open a Pull Request against `main`
3. Fill out the PR template completely
4. Link any related issues
5. Wait for review

### Review Process

- Maintainers will review within 48 hours
- Address feedback promptly
- Once approved, a maintainer will merge

## Style Guidelines

### Python Code Style

We use:
- **Black** for code formatting (line length: 100)
- **Ruff** for linting
- **isort** for import sorting
- **mypy** for type checking

```python
# Good: Type hints, docstrings, clear naming
async def get_audit_findings(
    self,
    audit_id: str,
    *,
    include_failed: bool = False,
) -> list[dict[str, Any]]:
    """
    Retrieve all findings for a specific audit.

    Args:
        audit_id: The MongoDB ObjectId of the audit.
        include_failed: Whether to include failed findings.

    Returns:
        List of finding dictionaries with full details.

    Raises:
        NotFoundError: If the audit doesn't exist.
        AuthenticationError: If not authenticated.
    """
    ...
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Keep README updated
- Document breaking changes

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change that neither fixes nor adds
- `perf`: Performance improvement
- `test`: Adding or fixing tests
- `chore`: Build process, dependencies, etc.

### Examples

```
feat(client): add bulk finding export endpoint

fix(auth): handle token refresh on 401 response

docs(readme): add Docker installation section

test(server): add integration tests for SSE transport
```

## Security

If you discover a security vulnerability, please follow our [Security Policy](SECURITY.md) instead of opening a public issue.

## Questions?

- Open a [Discussion](https://github.com/walidfaour/pwndoc-mcp-server/discussions)
- Check the [Documentation](https://walidfaour.github.io/pwndoc-mcp-server)

## Recognition

Contributors are recognized in:
- Release notes
- CONTRIBUTORS.md
- Project documentation

Thank you for contributing! 🎉
