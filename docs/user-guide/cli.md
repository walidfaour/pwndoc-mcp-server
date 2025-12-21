# Command Line Interface

PwnDoc MCP Server includes a powerful CLI for managing configuration, testing connections, and querying tools directly.

## Installation

The CLI is included with the `[cli]` or `[all]` extras:

```bash
pip install pwndoc-mcp-server[cli]
```

## Commands Overview

```bash
pwndoc-mcp --help
```

```
Usage: pwndoc-mcp [OPTIONS] COMMAND [ARGS]...

  PwnDoc MCP Server - AI-powered pentest documentation

Options:
  --version  Show version
  --help     Show this message

Commands:
  serve    Start the MCP server
  config   Manage configuration
  test     Test PwnDoc connection
  tools    List available tools
  query    Query a tool directly
  version  Show version information
```

## serve

Start the MCP server for use with Claude Desktop or other MCP clients.

```bash
pwndoc-mcp serve [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--transport` | Transport type: `stdio` or `sse` | `stdio` |
| `--port` | Port for SSE transport | `8080` |
| `--host` | Host for SSE transport | `0.0.0.0` |

### Examples

```bash
# Default stdio transport (for Claude Desktop)
pwndoc-mcp serve

# SSE transport on custom port
pwndoc-mcp serve --transport sse --port 9000

# With debug logging
PWNDOC_LOG_LEVEL=DEBUG pwndoc-mcp serve
```

## config

Manage server configuration.

### config init

Interactive configuration wizard:

```bash
pwndoc-mcp config init
```

Output:
```
PwnDoc MCP Server Configuration Wizard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Enter PwnDoc URL: https://pwndoc.example.com
Enter username: pentester
Enter password: ********

Testing connection...
✓ Connected successfully!

Configuration saved to: ~/.pwndoc-mcp/config.yaml
```

### config show

Display current configuration (secrets masked):

```bash
pwndoc-mcp config show
```

Output:
```
PwnDoc MCP Server Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

URL:         https://pwndoc.example.com
Username:    pentester
Password:    ***
Verify SSL:  true
Timeout:     30s

Config File: /home/user/.pwndoc-mcp/config.yaml
```

### config set

Update individual settings:

```bash
pwndoc-mcp config set <key> <value>
```

Examples:
```bash
pwndoc-mcp config set url https://new-pwndoc.com
pwndoc-mcp config set timeout 60
pwndoc-mcp config set log_level DEBUG
```

### config path

Show configuration file path:

```bash
pwndoc-mcp config path
```

## test

Test connection to PwnDoc server:

```bash
pwndoc-mcp test [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--verbose` | Show detailed output |

### Examples

```bash
# Basic test
pwndoc-mcp test

# Verbose test
pwndoc-mcp test --verbose
```

Output:
```
Testing PwnDoc Connection
━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Configuration loaded
✓ Connected to https://pwndoc.example.com
✓ Authenticated as: pentester (role: user)
✓ API responsive

Connection successful!
```

## tools

List all available MCP tools:

```bash
pwndoc-mcp tools [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | Output format: `table`, `json`, `simple` | `table` |
| `--category` | Filter by category | (all) |

### Examples

```bash
# Table format (default)
pwndoc-mcp tools

# JSON format
pwndoc-mcp tools --format json

# Filter by category
pwndoc-mcp tools --category audit
```

Output:
```
Available PwnDoc Tools (50)
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Audit Management
  list_audits          List all audits
  get_audit            Get audit details
  create_audit         Create new audit
  ...

Finding Management
  get_audit_findings   Get findings from audit
  create_finding       Create new finding
  ...
```

## query

Execute a tool directly from the command line:

```bash
pwndoc-mcp query <tool_name> [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--params` | JSON parameters for the tool |
| `--format` | Output format: `json`, `table`, `raw` |

### Examples

```bash
# List all audits
pwndoc-mcp query list_audits

# Get specific audit
pwndoc-mcp query get_audit --params '{"audit_id": "507f1f77bcf86cd799439011"}'

# Search findings
pwndoc-mcp query search_findings --params '{"severity": "Critical"}'

# Get statistics
pwndoc-mcp query get_statistics

# Create a finding
pwndoc-mcp query create_finding --params '{
  "audit_id": "507f1f77bcf86cd799439011",
  "title": "SQL Injection in Login",
  "severity": "Critical",
  "description": "The login form is vulnerable..."
}'
```

Output formats:

```bash
# JSON output (default for programmatic use)
pwndoc-mcp query list_audits --format json

# Table output (human readable)
pwndoc-mcp query list_audits --format table

# Raw output
pwndoc-mcp query list_audits --format raw
```

## version

Show version information:

```bash
pwndoc-mcp version
```

Output:
```
pwndoc-mcp-server 1.0.0
Python 3.11.5
Platform: Linux-5.15.0-x86_64
```

## Environment Variables

Override configuration via environment:

```bash
# Connection
export PWNDOC_URL="https://pwndoc.example.com"
export PWNDOC_USERNAME="pentester"
export PWNDOC_PASSWORD="secret"

# Or token auth
export PWNDOC_TOKEN="eyJhbGci..."

# Settings
export PWNDOC_VERIFY_SSL="true"
export PWNDOC_TIMEOUT="30"
export PWNDOC_LOG_LEVEL="DEBUG"
export PWNDOC_LOG_FILE="/var/log/pwndoc-mcp.log"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | Authentication error |
| 4 | Connection error |

## Scripting Examples

### Batch Query

```bash
#!/bin/bash
# Export critical findings to JSON

pwndoc-mcp query search_findings \
  --params '{"severity": "Critical"}' \
  --format json > critical_findings.json
```

### Pipeline with jq

```bash
# Count audits by status
pwndoc-mcp query list_audits --format json | \
  jq -r '.[].state' | sort | uniq -c
```

### Automated Reports

```bash
#!/bin/bash
# Generate reports for all completed audits

for audit_id in $(pwndoc-mcp query list_audits --format json | jq -r '.[] | select(.state=="Completed") | ._id'); do
  echo "Generating report for $audit_id"
  pwndoc-mcp query generate_audit_report --params "{\"audit_id\": \"$audit_id\"}"
done
```

## Next Steps

- [Claude Desktop Integration](claude-desktop.md)
- [Docker Deployment](docker.md)
- [Tool Reference](../tools/overview.md)
