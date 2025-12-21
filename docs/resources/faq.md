# Frequently Asked Questions

## General

### What is PwnDoc MCP Server?

PwnDoc MCP Server is a Model Context Protocol (MCP) server that connects AI assistants like Claude to your PwnDoc penetration testing documentation platform. It allows you to query, create, and manage pentests using natural language.

### What is MCP?

The Model Context Protocol (MCP) is an open standard developed by Anthropic for connecting AI assistants to external tools and data sources. Learn more at [modelcontextprotocol.io](https://modelcontextprotocol.io).

### Which AI assistants are supported?

Currently supported:
- **Claude Desktop** (primary target)
- Any MCP-compatible client

### What PwnDoc versions are supported?

PwnDoc MCP Server is tested with:
- PwnDoc 3.x (recommended)
- PwnDoc 2.x (limited support)

### Is this official?

No, this is a community project. It is not affiliated with or endorsed by PwnDoc or Anthropic.

## Installation

### Which Python version do I need?

Python 3.8 or higher is required. We recommend Python 3.11+ for best performance.

### Can I use this without Python?

Yes! We provide:
- **Standalone binaries** for Linux, macOS, and Windows
- **Docker images** that don't require Python
- **System packages** (.deb, .rpm)

### How do I update to the latest version?

```bash
# pip
pip install --upgrade pwndoc-mcp-server

# Docker
docker pull ghcr.io/walidfaour/pwndoc-mcp-server:latest

# Homebrew
brew upgrade pwndoc-mcp-server
```

## Configuration

### Where is the configuration file stored?

Default locations:
- **Linux/macOS**: `~/.pwndoc-mcp/config.yaml`
- **Windows**: `%USERPROFILE%\.pwndoc-mcp\config.yaml`

### Should I use token or password authentication?

**Token authentication is recommended** because:
- Tokens can be revoked without changing your password
- Tokens can have limited scope
- Tokens don't expose your main credentials

### How do I get a JWT token?

1. Log into PwnDoc web interface
2. Go to Profile/Settings
3. Generate API token
4. Copy and use in configuration

### Can I connect to multiple PwnDoc instances?

Yes! Configure multiple servers in Claude Desktop:

```json
{
  "mcpServers": {
    "pwndoc-prod": { ... },
    "pwndoc-dev": { ... }
  }
}
```

## Usage

### What can I ask Claude to do?

Examples:
- "List all audits for Acme Corp"
- "Find critical vulnerabilities across all pentests"
- "Create a finding for SQL injection in the login page"
- "Generate the report for the completed audit"
- "What are the most common vulnerability types this quarter?"

### How many tools are available?

50+ tools covering:
- Audit management (12 tools)
- Finding management (9 tools)
- Client/Company management (8 tools)
- Vulnerability templates (10 tools)
- Users and settings (12 tools)
- Reports and statistics (4+ tools)

### Can I create findings with Claude?

Yes! Example:
> "Create a high-severity finding for XSS in the user profile page for the Acme Corp audit"

### Can I generate reports?

Yes! Example:
> "Generate the report for audit [audit-name]"

The report will be created as a DOCX file.

### Does Claude have access to all my audits?

Claude can access any audit that your PwnDoc user account can access. The same permissions apply.

## Security

### Is my data sent to Anthropic?

When using Claude, your queries and PwnDoc data are processed by Anthropic's servers according to their privacy policy. The MCP server itself doesn't send data anywhere except your PwnDoc instance.

### Are my credentials stored securely?

- Config files are created with 600 permissions (user-only read/write)
- Passwords are never logged
- We recommend using environment variables for CI/CD

### Can I use this in production?

Yes, but consider:
- Use token authentication
- Enable SSL verification
- Review access logs
- Limit user permissions in PwnDoc

### Is the connection encrypted?

Yes, if your PwnDoc instance uses HTTPS. Always use HTTPS in production.

## Troubleshooting

### Claude says "No tools available"

1. Check Claude Desktop config syntax
2. Verify `pwndoc-mcp` is in PATH
3. Restart Claude Desktop completely
4. Test with `pwndoc-mcp serve` manually

### "Authentication failed" error

1. Verify credentials with `pwndoc-mcp test`
2. Check if account is enabled in PwnDoc
3. Try re-running `pwndoc-mcp config init`

### Connection timeout

1. Increase timeout: `export PWNDOC_TIMEOUT=60`
2. Check network connectivity
3. Verify PwnDoc server is running

### See more issues

Check our [Troubleshooting Guide](troubleshooting.md)

## Development

### Can I contribute?

Yes! See our [Contributing Guide](https://github.com/walidfaour/pwndoc-mcp-server/blob/main/CONTRIBUTING.md).

### How do I run tests?

```bash
git clone https://github.com/walidfaour/pwndoc-mcp-server.git
cd pwndoc-mcp-server
pip install -e ".[dev]"
pytest
```

### Can I add custom tools?

Not currently, but you can:
1. Fork the repository
2. Add tools in `src/pwndoc_mcp_server/server.py`
3. Submit a pull request

### Where can I report bugs?

Open an issue at [GitHub Issues](https://github.com/walidfaour/pwndoc-mcp-server/issues)

## Pricing & Licensing

### Is this free?

Yes! PwnDoc MCP Server is open source under the MIT license.

### Can I use this commercially?

Yes, the MIT license allows commercial use.

### Do I need a Claude subscription?

You need access to Claude Desktop or another MCP-compatible client. Check Anthropic's pricing for Claude access.
