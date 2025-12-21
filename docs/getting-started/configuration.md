# Configuration

PwnDoc MCP Server supports multiple configuration methods, with a clear priority order.

## Configuration Priority

Settings are loaded in this order (later sources override earlier):

1. **Default values** (built-in)
2. **Configuration file** (`~/.pwndoc-mcp/config.yaml`)
3. **Environment variables** (`PWNDOC_*`)
4. **CLI arguments** (`--url`, `--token`, etc.)

## Interactive Setup (Recommended)

The easiest way to configure:

```bash
pwndoc-mcp config init
```

This wizard will:
1. Prompt for your PwnDoc URL
2. Ask for username and password
3. Test the connection
4. Save configuration securely

## Environment Variables

Set environment variables for configuration:

```bash
# Required: PwnDoc instance URL
export PWNDOC_URL="https://pwndoc.yourcompany.com"

# Authentication (choose one method):

# Method 1: Username and password
export PWNDOC_USERNAME="your-username"
export PWNDOC_PASSWORD="your-password"

# Method 2: JWT token (if you have one)
export PWNDOC_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6..."

# Optional settings
export PWNDOC_VERIFY_SSL="true"          # SSL verification (default: true)
export PWNDOC_TIMEOUT="30"                # Request timeout in seconds
export PWNDOC_MAX_RETRIES="3"             # Max retry attempts
export PWNDOC_LOG_LEVEL="INFO"            # DEBUG, INFO, WARNING, ERROR
export PWNDOC_LOG_FILE="/var/log/pwndoc-mcp.log"  # Log file path
```

### Loading from .env File

Create a `.env` file in your working directory:

```bash
# .env
PWNDOC_URL=https://pwndoc.yourcompany.com
PWNDOC_USERNAME=pentester
PWNDOC_PASSWORD=secret123
PWNDOC_LOG_LEVEL=DEBUG
```

## Configuration File

### Default Location

- **Linux/macOS**: `~/.pwndoc-mcp/config.yaml`
- **Windows**: `%USERPROFILE%\.pwndoc-mcp\config.yaml`

### Custom Location

```bash
export PWNDOC_CONFIG_FILE="/path/to/custom/config.yaml"
```

### YAML Format

```yaml
# ~/.pwndoc-mcp/config.yaml

# PwnDoc instance URL (required)
url: https://pwndoc.yourcompany.com

# Authentication
username: pentester
password: your-secure-password

# Or use token authentication
# token: eyJhbGciOiJIUzI1NiIsInR5cCI6...

# Connection settings
verify_ssl: true
timeout: 30
max_retries: 3

# Logging
log_level: INFO
log_file: ~/.pwndoc-mcp/logs/server.log
```

### JSON Format

```json
{
  "url": "https://pwndoc.yourcompany.com",
  "username": "pentester",
  "password": "your-secure-password",
  "verify_ssl": true,
  "timeout": 30,
  "max_retries": 3,
  "log_level": "INFO"
}
```

## Configuration Options Reference

| Option | Environment Variable | Default | Description |
|--------|---------------------|---------|-------------|
| `url` | `PWNDOC_URL` | (required) | PwnDoc instance URL |
| `username` | `PWNDOC_USERNAME` | `""` | Username for authentication |
| `password` | `PWNDOC_PASSWORD` | `""` | Password for authentication |
| `token` | `PWNDOC_TOKEN` | `""` | JWT token (alternative to username/password) |
| `verify_ssl` | `PWNDOC_VERIFY_SSL` | `true` | Verify SSL certificates |
| `timeout` | `PWNDOC_TIMEOUT` | `30` | Request timeout in seconds |
| `max_retries` | `PWNDOC_MAX_RETRIES` | `3` | Maximum retry attempts |
| `log_level` | `PWNDOC_LOG_LEVEL` | `INFO` | Logging level |
| `log_file` | `PWNDOC_LOG_FILE` | `""` | Log file path (empty = console only) |

## Managing Configuration

### View Current Configuration

```bash
pwndoc-mcp config show
```

Output (passwords masked):

```
PwnDoc MCP Server Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

URL:         https://pwndoc.yourcompany.com
Username:    pentester
Password:    ***
Token:       ***
Verify SSL:  true
Timeout:     30s
Max Retries: 3
Log Level:   INFO
Log File:    (none)

Config File: /home/user/.pwndoc-mcp/config.yaml
```

### Show Config File Path

```bash
pwndoc-mcp config path
```

### Update Individual Settings

```bash
pwndoc-mcp config set url https://new-pwndoc.com
pwndoc-mcp config set timeout 60
pwndoc-mcp config set log_level DEBUG
```

## Security Best Practices

### File Permissions

Config files are automatically created with secure permissions (600 on Unix):

```bash
chmod 600 ~/.pwndoc-mcp/config.yaml
```

### Secrets Management

**Don't commit credentials to version control!**

Use environment variables for CI/CD:

```yaml
# GitHub Actions example
env:
  PWNDOC_URL: ${{ secrets.PWNDOC_URL }}
  PWNDOC_TOKEN: ${{ secrets.PWNDOC_TOKEN }}
```

### Token vs Password Authentication

Prefer token authentication when possible:

1. Tokens can be scoped to specific permissions
2. Tokens can be revoked without changing password
3. Tokens don't expose your main credentials

## Troubleshooting

### Test Connection

```bash
pwndoc-mcp test
```

Successful output:

```
✓ Configuration loaded
✓ Connected to https://pwndoc.yourcompany.com
✓ Authenticated as: pentester (role: user)
✓ API version: 3.2.1

Connection successful!
```

### Common Issues

**SSL Certificate Errors**

```bash
# Temporary (not recommended for production)
export PWNDOC_VERIFY_SSL=false
```

**Authentication Failures**

```bash
# Check credentials
pwndoc-mcp test --verbose

# Enable debug logging
export PWNDOC_LOG_LEVEL=DEBUG
pwndoc-mcp test
```

**Connection Timeouts**

```bash
# Increase timeout
export PWNDOC_TIMEOUT=60
```

## Next Steps

- [Quick Start Guide](quick-start.md)
- [Claude Desktop Integration](../user-guide/claude-desktop.md)
