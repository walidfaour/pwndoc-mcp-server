# PwnDoc MCP Server Documentation

Welcome to the PwnDoc MCP Server documentation!

**Live documentation**: [walidfaour.github.io/pwndoc-mcp-server](https://walidfaour.github.io/pwndoc-mcp-server)

## Quick Start

```bash
# Install
pip install pwndoc-mcp-server

# Configure
export PWNDOC_URL="https://your-pwndoc.com"
export PWNDOC_TOKEN="your-jwt-token"

# Test connection
pwndoc-mcp test

# Start server
pwndoc-mcp serve
```

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_URL": "https://your-pwndoc.com",
        "PWNDOC_TOKEN": "your-token"
      }
    }
  }
}
```

## Documentation Sections

### Getting Started
- [Installation](getting-started/installation.md)
- [Quick Start](getting-started/quick-start.md)
- [Configuration](getting-started/configuration.md)

### User Guide
- [CLI Usage](user-guide/cli.md)
- [Claude Desktop Integration](user-guide/claude-desktop.md)
- [Docker Deployment](user-guide/docker.md)
- [Logging](user-guide/logging.md)

### Tools Reference
- [Overview](tools/overview.md)
- [Audits](tools/audits.md)
- [Findings](tools/findings.md)
- [Vulnerabilities](tools/vulnerabilities.md)
- [Clients & Companies](tools/clients-companies.md)
- [Users & Settings](tools/users-settings.md)
- [Reports & Statistics](tools/reports-statistics.md)

### Development
- [Contributing](development/contributing.md)
- [Building from Source](development/building.md)
- [Testing](development/testing.md)
- [API Reference](development/api-reference.md)

### Resources
- [Troubleshooting](resources/troubleshooting.md)
- [FAQ](resources/faq.md)

## Setting Up GitHub Pages

To deploy this documentation to GitHub Pages:

1. Go to your repository Settings → Pages
2. Under "Source", select "Deploy from a branch"
3. Select the `main` branch and `/docs` folder
4. Click Save

The documentation will be available at `https://walidfaour.github.io/pwndoc-mcp-server/`

Alternatively, the repository includes a GitHub Actions workflow (`.github/workflows/docs.yml`) that automatically deploys documentation on push to main.

## License

MIT License - see [LICENSE](../LICENSE)
