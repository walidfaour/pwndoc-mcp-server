# API Reference

Programmatic interface for PwnDoc MCP Server.

## Installation

```python
pip install pwndoc-mcp-server
```

## Core Classes

### PwnDocConfig

Configuration management for the client and server.

```python
from pwndoc_mcp_server import PwnDocConfig

# Create with parameters
config = PwnDocConfig(
    url="https://pwndoc.example.com",
    username="admin",
    password="secret",
    verify_ssl=True,
    timeout=30,
    max_retries=3,
    log_level="INFO"
)

# Or with token
config = PwnDocConfig(
    url="https://pwndoc.example.com",
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
)

# Validate
if config.is_valid():
    print("Configuration is valid")

# Convert to dict
config_dict = config.to_dict()
config_dict_no_secrets = config.to_dict(include_secrets=False)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | "" | PwnDoc instance URL |
| `username` | str | "" | Authentication username |
| `password` | str | "" | Authentication password |
| `token` | str | "" | JWT token (alternative to username/password) |
| `verify_ssl` | bool | True | Verify SSL certificates |
| `timeout` | int | 30 | Request timeout in seconds |
| `max_retries` | int | 3 | Max retry attempts |
| `log_level` | str | "INFO" | Logging level |
| `log_file` | str | "" | Log file path |

---

### PwnDocClient

Async HTTP client for PwnDoc API.

```python
from pwndoc_mcp_server import PwnDocClient, PwnDocConfig

config = PwnDocConfig(url="https://pwndoc.example.com", token="...")

# As context manager (recommended)
async with PwnDocClient(config) as client:
    audits = await client.list_audits()
    
# Manual lifecycle
client = PwnDocClient(config)
await client.authenticate()
audits = await client.list_audits()
await client.close()
```

#### Methods

##### Authentication

```python
await client.authenticate() -> bool
```

##### Audits

```python
await client.list_audits(finding_title: str = None) -> List[Dict]
await client.get_audit(audit_id: str) -> Dict
await client.get_audit_general(audit_id: str) -> Dict
await client.create_audit(name: str, audit_type: str, language: str) -> Dict
await client.update_audit_general(audit_id: str, **kwargs) -> Dict
await client.delete_audit(audit_id: str) -> Dict
await client.generate_audit_report(audit_id: str) -> bytes
```

##### Findings

```python
await client.get_audit_findings(audit_id: str) -> List[Dict]
await client.get_finding(audit_id: str, finding_id: str) -> Dict
await client.create_finding(audit_id: str, title: str, **kwargs) -> Dict
await client.update_finding(audit_id: str, finding_id: str, **kwargs) -> Dict
await client.delete_finding(audit_id: str, finding_id: str) -> Dict
await client.search_findings(**filters) -> List[Dict]
await client.get_all_findings_with_context(**options) -> List[Dict]
```

##### Clients & Companies

```python
await client.list_clients() -> List[Dict]
await client.create_client(**kwargs) -> Dict
await client.update_client(client_id: str, **kwargs) -> Dict
await client.delete_client(client_id: str) -> Dict

await client.list_companies() -> List[Dict]
await client.create_company(**kwargs) -> Dict
await client.update_company(company_id: str, **kwargs) -> Dict
await client.delete_company(company_id: str) -> Dict
```

##### Vulnerabilities

```python
await client.list_vulnerabilities() -> List[Dict]
await client.get_vulnerabilities_by_locale(locale: str = "en") -> List[Dict]
await client.create_vulnerability(**kwargs) -> Dict
await client.update_vulnerability(vuln_id: str, **kwargs) -> Dict
await client.delete_vulnerability(vuln_id: str) -> Dict
```

##### Users & Settings

```python
await client.list_users() -> List[Dict]
await client.get_user(username: str) -> Dict
await client.get_current_user() -> Dict
await client.get_statistics() -> Dict
await client.get_settings() -> Dict
```

---

### PwnDocMCPServer

MCP server implementation.

```python
from pwndoc_mcp_server import PwnDocMCPServer, PwnDocConfig

config = PwnDocConfig(url="...", token="...")

# Create server
server = PwnDocMCPServer(config, transport="stdio")

# Run server (blocking)
server.run()

# Or use async
await server.run_async()
```

#### Methods

```python
# Get available tools
tools = await server.handle_list_tools() -> List[Dict]

# Call a tool
result = await server.handle_call_tool(
    tool_name: str,
    arguments: Dict
) -> str

# Handle MCP protocol messages
response = await server.handle_message(message: Dict) -> Dict
```

---

## Configuration Functions

### load_config

Load configuration from environment and/or file.

```python
from pwndoc_mcp_server import load_config

# Auto-detect from environment and default file
config = load_config()

# From specific file
config = load_config(config_file="/path/to/config.yaml")
```

### save_config

Save configuration to file.

```python
from pwndoc_mcp_server import save_config

save_config(config, "/path/to/config.yaml")
```

### get_config_path

Get the configuration file path.

```python
from pwndoc_mcp_server import get_config_path

path = get_config_path()  # ~/.pwndoc-mcp/config.yaml
```

---

## Logging

### setup_logging

Configure logging.

```python
from pwndoc_mcp_server import setup_logging

# Basic setup
logger = setup_logging()

# With options
logger = setup_logging(
    level="DEBUG",
    log_file="/var/log/pwndoc-mcp.log",
    log_format="json",
    max_bytes=10 * 1024 * 1024,
    backup_count=5
)
```

### get_logger

Get a logger instance.

```python
from pwndoc_mcp_server import get_logger

logger = get_logger("my.module")
logger.info("Hello")
```

---

## Exceptions

### PwnDocError

Base exception for all PwnDoc errors.

```python
from pwndoc_mcp_server import PwnDocError

try:
    await client.get_audit("invalid-id")
except PwnDocError as e:
    print(f"Error: {e}")
    print(f"Status code: {e.status_code}")
```

### AuthenticationError

Authentication failures.

```python
from pwndoc_mcp_server import AuthenticationError

try:
    await client.authenticate()
except AuthenticationError as e:
    print("Invalid credentials")
```

### RateLimitError

Rate limit exceeded.

```python
from pwndoc_mcp_server import RateLimitError

try:
    await client.list_audits()
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
```

### NotFoundError

Resource not found.

```python
from pwndoc_mcp_server import NotFoundError

try:
    await client.get_audit("nonexistent")
except NotFoundError:
    print("Audit not found")
```

---

## Complete Example

```python
import asyncio
from pwndoc_mcp_server import (
    PwnDocConfig,
    PwnDocClient,
    setup_logging,
    AuthenticationError,
    NotFoundError,
)

async def main():
    # Setup logging
    setup_logging(level="INFO")
    
    # Create config
    config = PwnDocConfig(
        url="https://pwndoc.example.com",
        username="admin",
        password="secret"
    )
    
    if not config.is_valid():
        print("Invalid configuration")
        return
    
    # Use client
    async with PwnDocClient(config) as client:
        try:
            # Authenticate
            await client.authenticate()
            print("Authenticated successfully")
            
            # List audits
            audits = await client.list_audits()
            print(f"Found {len(audits)} audits")
            
            # Get statistics
            stats = await client.get_statistics()
            print(f"Total findings: {stats['totalFindings']}")
            
            # Search findings
            critical = await client.search_findings(severity="Critical")
            print(f"Critical findings: {len(critical)}")
            
        except AuthenticationError:
            print("Authentication failed")
        except NotFoundError as e:
            print(f"Not found: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Type Hints

The package includes full type hints:

```python
from pwndoc_mcp_server.client import PwnDocClient
from pwndoc_mcp_server.config import PwnDocConfig
from typing import List, Dict, Any

async def get_audits(client: PwnDocClient) -> List[Dict[str, Any]]:
    return await client.list_audits()
```

Use with mypy:

```bash
mypy your_script.py
```
