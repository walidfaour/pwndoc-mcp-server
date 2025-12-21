"""
Pytest configuration and fixtures for PwnDoc MCP Server tests.
"""

import os
import shutil
import tempfile
from typing import Any, Dict, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ============================================================================
# Environment Fixtures
# ============================================================================


@pytest.fixture(autouse=True)
def clean_environment() -> Generator[None, None, None]:
    """Clean environment variables before each test."""
    env_vars = [
        "PWNDOC_URL",
        "PWNDOC_USERNAME",
        "PWNDOC_PASSWORD",
        "PWNDOC_TOKEN",
        "PWNDOC_VERIFY_SSL",
        "PWNDOC_TIMEOUT",
        "PWNDOC_MAX_RETRIES",
        "PWNDOC_LOG_LEVEL",
        "PWNDOC_LOG_FILE",
        "PWNDOC_CONFIG_FILE",
    ]
    # Store original values
    original = {k: os.environ.get(k) for k in env_vars}

    # Clear all
    for var in env_vars:
        os.environ.pop(var, None)

    yield

    # Restore original values
    for var, value in original.items():
        if value is not None:
            os.environ[var] = value
        else:
            os.environ.pop(var, None)


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for tests."""
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath, ignore_errors=True)


@pytest.fixture
def temp_config_file(temp_dir: str) -> str:
    """Create a temporary config file."""
    config_path = os.path.join(temp_dir, "config.yaml")
    return config_path


# ============================================================================
# Mock Data Fixtures
# ============================================================================


@pytest.fixture
def mock_audit() -> Dict[str, Any]:
    """Sample audit data."""
    return {
        "_id": "507f1f77bcf86cd799439011",
        "name": "Test Pentest Q4 2024",
        "auditType": "Web Application",
        "language": "en",
        "state": "In Progress",
        "creator": {
            "_id": "507f1f77bcf86cd799439001",
            "username": "pentester1",
            "firstname": "John",
            "lastname": "Doe",
        },
        "collaborators": [],
        "reviewers": [],
        "client": {
            "_id": "507f1f77bcf86cd799439021",
            "email": "client@example.com",
            "firstname": "Jane",
            "lastname": "Smith",
        },
        "company": {"_id": "507f1f77bcf86cd799439031", "name": "Acme Corp", "shortName": "ACME"},
        "date_start": "2024-10-01T00:00:00.000Z",
        "date_end": "2024-10-31T00:00:00.000Z",
        "scope": ["https://app.example.com", "https://api.example.com", "192.168.1.0/24"],
        "findings": [],
        "sections": [],
        "createdAt": "2024-09-15T10:00:00.000Z",
        "updatedAt": "2024-10-20T15:30:00.000Z",
    }


@pytest.fixture
def mock_finding() -> Dict[str, Any]:
    """Sample finding data."""
    return {
        "_id": "507f1f77bcf86cd799439041",
        "title": "SQL Injection in Login Form",
        "vulnType": "Injection",
        "description": "The login form is vulnerable to SQL injection attacks.",
        "observation": "Parameter 'username' accepts SQL metacharacters.",
        "remediation": "Use parameterized queries or prepared statements.",
        "poc": "' OR '1'='1' --",
        "scope": "https://app.example.com/login",
        "cvssv3": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "cvssScore": 9.8,
        "severity": "Critical",
        "priority": 1,
        "remediation_complexity": 2,
        "status": 1,
        "category": "Web Application",
        "references": [
            "https://owasp.org/www-community/attacks/SQL_Injection",
            "https://cwe.mitre.org/data/definitions/89.html",
        ],
        "customFields": [],
    }


@pytest.fixture
def mock_client() -> Dict[str, Any]:
    """Sample client data."""
    return {
        "_id": "507f1f77bcf86cd799439021",
        "email": "client@example.com",
        "firstname": "Jane",
        "lastname": "Smith",
        "phone": "+1-555-123-4567",
        "cell": "+1-555-987-6543",
        "title": "Security Manager",
        "company": {"_id": "507f1f77bcf86cd799439031", "name": "Acme Corp"},
    }


@pytest.fixture
def mock_company() -> Dict[str, Any]:
    """Sample company data."""
    return {
        "_id": "507f1f77bcf86cd799439031",
        "name": "Acme Corporation",
        "shortName": "ACME",
        "logo": "",
    }


@pytest.fixture
def mock_vulnerability() -> Dict[str, Any]:
    """Sample vulnerability template data."""
    return {
        "_id": "507f1f77bcf86cd799439051",
        "cvssv3": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "priority": 1,
        "remediationComplexity": 2,
        "category": "Web Application",
        "details": [
            {
                "locale": "en",
                "title": "SQL Injection",
                "vulnType": "Injection",
                "description": "SQL injection vulnerability template.",
                "observation": "SQL metacharacters accepted in input.",
                "remediation": "Use parameterized queries.",
                "references": ["https://owasp.org/"],
            }
        ],
    }


@pytest.fixture
def mock_user() -> Dict[str, Any]:
    """Sample user data."""
    return {
        "_id": "507f1f77bcf86cd799439001",
        "username": "pentester1",
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-111-2222",
        "role": "user",
        "enabled": True,
        "totpEnabled": False,
    }


@pytest.fixture
def mock_template() -> Dict[str, Any]:
    """Sample report template data."""
    return {"_id": "507f1f77bcf86cd799439061", "name": "Standard Pentest Report", "ext": "docx"}


@pytest.fixture
def mock_statistics() -> Dict[str, Any]:
    """Sample statistics data."""
    return {
        "totalAudits": 81,
        "auditsByStatus": {"In Progress": 15, "Completed": 60, "Draft": 6},
        "totalFindings": 423,
        "findingsBySeverity": {"Critical": 28, "High": 95, "Medium": 187, "Low": 89, "Info": 24},
        "totalClients": 12,
        "totalCompanies": 8,
        "totalUsers": 23,
        "recentAudits": [],
    }


# ============================================================================
# Mock Client Fixtures
# ============================================================================


@pytest.fixture
def mock_pwndoc_client():
    """Create a mock PwnDoc client."""
    with patch("pwndoc_mcp_server.client.PwnDocClient") as MockClient:
        client = AsyncMock()
        MockClient.return_value = client

        # Setup default responses
        client.authenticate = AsyncMock(return_value=True)
        client.list_audits = AsyncMock(return_value=[])
        client.get_audit = AsyncMock(return_value={})
        client.list_clients = AsyncMock(return_value=[])
        client.list_companies = AsyncMock(return_value=[])
        client.list_vulnerabilities = AsyncMock(return_value=[])
        client.list_users = AsyncMock(return_value=[])
        client.get_statistics = AsyncMock(return_value={})

        yield client


@pytest.fixture
def mock_httpx_client():
    """Create a mock httpx async client."""
    with patch("httpx.AsyncClient") as MockAsyncClient:
        client = AsyncMock()
        MockAsyncClient.return_value.__aenter__ = AsyncMock(return_value=client)
        MockAsyncClient.return_value.__aexit__ = AsyncMock(return_value=None)
        yield client


# ============================================================================
# Response Fixtures
# ============================================================================


@pytest.fixture
def mock_auth_response() -> Dict[str, Any]:
    """Mock authentication response."""
    return {
        "status": "success",
        "datas": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token",
            "username": "pentester1",
            "role": "user",
        },
    }


@pytest.fixture
def mock_list_response(mock_audit: Dict[str, Any]) -> Dict[str, Any]:
    """Mock list response."""
    return {"status": "success", "datas": [mock_audit]}


@pytest.fixture
def mock_single_response(mock_audit: Dict[str, Any]) -> Dict[str, Any]:
    """Mock single item response."""
    return {"status": "success", "datas": mock_audit}


@pytest.fixture
def mock_error_response() -> Dict[str, Any]:
    """Mock error response."""
    return {"status": "error", "datas": "An error occurred"}


# ============================================================================
# CLI Fixtures
# ============================================================================


@pytest.fixture
def cli_runner():
    """Create a CLI test runner."""
    from typer.testing import CliRunner

    return CliRunner()


# ============================================================================
# Server Fixtures
# ============================================================================


@pytest.fixture
def mock_mcp_server():
    """Create a mock MCP server context."""
    with patch("pwndoc_mcp_server.server.Server") as MockServer:
        server = MagicMock()
        MockServer.return_value = server
        yield server


# ============================================================================
# Async Helpers
# ============================================================================


@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
