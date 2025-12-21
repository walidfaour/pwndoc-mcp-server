# Claude Desktop Integration

This guide covers setting up PwnDoc MCP Server with Claude Desktop for seamless AI-powered pentest documentation.

## Prerequisites

- [Claude Desktop](https://claude.ai/download) installed
- PwnDoc MCP Server installed (`pip install pwndoc-mcp-server[all]`)
- Valid PwnDoc credentials

## Configuration File Location

Claude Desktop stores its configuration at:

| Platform | Path |
|----------|------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

## Basic Setup

### 1. Create or Edit Configuration

Open the Claude Desktop config file and add the PwnDoc server:

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_URL": "https://your-pwndoc-instance.com",
        "PWNDOC_USERNAME": "your-username",
        "PWNDOC_PASSWORD": "your-password"
      }
    }
  }
}
```

### 2. Using Token Authentication (Recommended)

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_URL": "https://your-pwndoc-instance.com",
        "PWNDOC_TOKEN": "your-jwt-token"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop for changes to take effect.

### 4. Verify Connection

Look for "pwndoc" in the tools panel, or ask Claude:

> "What PwnDoc tools do you have access to?"

## Advanced Configurations

### Using Docker

If you prefer Docker:

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "PWNDOC_URL=https://your-pwndoc.com",
        "-e", "PWNDOC_TOKEN=your-token",
        "ghcr.io/walidfaour/pwndoc-mcp-server:latest"
      ]
    }
  }
}
```

### Using Standalone Binary

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "/usr/local/bin/pwndoc-mcp-server",
      "args": [],
      "env": {
        "PWNDOC_URL": "https://your-pwndoc.com",
        "PWNDOC_TOKEN": "your-token"
      }
    }
  }
}
```

### With Custom Config File

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_CONFIG_FILE": "/path/to/custom/config.yaml"
      }
    }
  }
}
```

### Debug Mode

Enable debug logging:

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_URL": "https://your-pwndoc.com",
        "PWNDOC_TOKEN": "your-token",
        "PWNDOC_LOG_LEVEL": "DEBUG",
        "PWNDOC_LOG_FILE": "/tmp/pwndoc-mcp.log"
      }
    }
  }
}
```

### Multiple PwnDoc Instances

Connect to multiple PwnDoc servers:

```json
{
  "mcpServers": {
    "pwndoc-prod": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_URL": "https://pwndoc.production.com",
        "PWNDOC_TOKEN": "prod-token"
      }
    },
    "pwndoc-dev": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_URL": "https://pwndoc.dev.local",
        "PWNDOC_TOKEN": "dev-token"
      }
    }
  }
}
```

## Usage Examples

Once connected, you can ask Claude natural language questions:

### Audit Management

> "Show me all audits for Acme Corp"

> "What's the status of the Q4 web application pentest?"

> "Create a new audit called 'Mobile App Assessment 2024' for Client XYZ"

### Finding Analysis

> "List all critical findings across my audits"

> "Find SQL injection vulnerabilities in the e-commerce audit"

> "What are the most common vulnerability types this quarter?"

### Documentation

> "Generate the report for the completed infrastructure assessment"

> "Summarize the findings from audit [audit-id]"

> "Update the executive summary section of the current audit"

### Cross-Audit Insights

> "Compare vulnerability trends between Q3 and Q4"

> "Which clients have the most critical findings?"

> "Show me all unremediated high-severity findings"

## Troubleshooting

### Tools Not Appearing

1. **Check config syntax**: Validate JSON is correctly formatted
2. **Verify path**: Ensure `pwndoc-mcp` is in your PATH
3. **Test manually**: Run `pwndoc-mcp serve` in terminal
4. **Restart Claude**: Fully quit and reopen Claude Desktop

### Authentication Errors

```bash
# Test credentials outside Claude
pwndoc-mcp test
```

### Connection Issues

```bash
# Test PwnDoc connectivity
curl https://your-pwndoc.com/api/users/me -H "Authorization: Bearer $TOKEN"
```

### View Logs

Check the debug log:

```bash
tail -f /tmp/pwndoc-mcp.log
```

### Check Claude Desktop Logs

| Platform | Log Location |
|----------|--------------|
| macOS | `~/Library/Logs/Claude/` |
| Windows | `%APPDATA%\Claude\logs\` |
| Linux | `~/.config/Claude/logs/` |

## Security Best Practices

### 1. Use Token Authentication

Prefer JWT tokens over username/password when possible.

### 2. Secure Config File

```bash
chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### 3. Environment Variables

Use environment variables instead of hardcoding credentials:

```bash
# In your shell profile
export PWNDOC_TOKEN="your-token"
```

Then in config:

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "pwndoc-mcp",
      "args": ["serve"]
    }
  }
}
```

### 4. Audit Access

Regularly review PwnDoc access logs and API usage.

## Next Steps

- [CLI Usage Guide](cli.md)
- [Docker Deployment](docker.md)
- [Tool Reference](../tools/overview.md)
