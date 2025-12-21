# Quick Start

Get up and running with PwnDoc MCP Server in under 5 minutes.

## Prerequisites

- PwnDoc instance (v3.x+) with valid credentials
- Python 3.8+ installed
- Claude Desktop (or other MCP client)

## Step 1: Install

```bash
pip install pwndoc-mcp-server[all]
```

## Step 2: Configure

Run the interactive setup:

```bash
pwndoc-mcp config init
```

Or set environment variables:

```bash
export PWNDOC_URL="https://your-pwndoc.com"
export PWNDOC_USERNAME="your-username"
export PWNDOC_PASSWORD="your-password"
```

## Step 3: Test Connection

```bash
pwndoc-mcp test
```

You should see:

```
✓ Connected to https://your-pwndoc.com
✓ Authenticated as: your-username
Connection successful!
```

## Step 4: Connect to Claude Desktop

Edit Claude's configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the PwnDoc server:

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_URL": "https://your-pwndoc.com",
        "PWNDOC_USERNAME": "your-username",
        "PWNDOC_PASSWORD": "your-password"
      }
    }
  }
}
```

## Step 5: Restart Claude Desktop

Close and reopen Claude Desktop. You should see "pwndoc" in the available tools.

## Step 6: Try It Out!

Start a conversation with Claude:

### List Your Audits

> "Show me all my current audits"

Claude will use the `list_audits` tool and display your pentests.

### Search for Findings

> "Find all SQL injection vulnerabilities across my audits"

Claude will use `search_findings` to locate matches.

### Get Statistics

> "Give me an overview of our pentest statistics"

Claude will use `get_statistics` to show metrics.

### Create a Finding

> "Create a new high-severity finding for XSS in the user profile page for audit [audit-name]"

Claude will use `create_finding` to add it.

## Common Use Cases

### Audit Management

```
"List all audits for Acme Corp"
"Show me the scope for the Q4 web application pentest"
"What's the status of my current audits?"
```

### Finding Analysis

```
"What are the most common vulnerabilities across all audits?"
"Find critical findings that haven't been remediated"
"Show me all findings related to authentication"
```

### Documentation

```
"Generate the report for the completed audit"
"Summarize the findings from the mobile app pentest"
"What are the top 5 risks from the infrastructure assessment?"
```

### Client Management

```
"List all clients"
"Show me contact information for Acme Corp"
"Create a new client for the upcoming engagement"
```

## What's Next?

- [Full Tool Reference](../tools/overview.md) - See all 50+ available tools
- [Claude Desktop Integration](../user-guide/claude-desktop.md) - Advanced configuration
- [Docker Deployment](../user-guide/docker.md) - Container setup
- [CLI Usage](../user-guide/cli.md) - Command line interface

## Troubleshooting

### "Connection refused" Error

Check that your PwnDoc URL is correct and accessible:

```bash
curl https://your-pwndoc.com/api/users/me
```

### "Authentication failed" Error

Verify your credentials:

```bash
pwndoc-mcp test --verbose
```

### Tools Not Showing in Claude

1. Ensure Claude Desktop was restarted
2. Check the config file path is correct
3. Look for errors in Claude Desktop's logs
4. Try running the server manually: `pwndoc-mcp serve`

### Still Having Issues?

- Check [Troubleshooting Guide](../resources/troubleshooting.md)
- Open an [issue on GitHub](https://github.com/walidfaour/pwndoc-mcp-server/issues)
