# PwnDoc MCP Server

<p align="center">
  <img src="assets/banner.svg" alt="PwnDoc MCP Server Banner" width="800">
</p>

<p align="center">
  <strong>Model Context Protocol server for PwnDoc pentest documentation</strong>
</p>

<p align="center">
  <a href="https://github.com/walidfaour/pwndoc-mcp-server/actions"><img src="https://img.shields.io/github/actions/workflow/status/walidfaour/pwndoc-mcp-server/ci.yml?style=flat-square" alt="Build Status"></a>
  <a href="https://pypi.org/project/pwndoc-mcp-server/"><img src="https://img.shields.io/pypi/v/pwndoc-mcp-server?style=flat-square" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/pwndoc-mcp-server/"><img src="https://img.shields.io/pypi/pyversions/pwndoc-mcp-server?style=flat-square" alt="Python Versions"></a>
  <a href="https://github.com/walidfaour/pwndoc-mcp-server/blob/main/LICENSE"><img src="https://img.shields.io/github/license/walidfaour/pwndoc-mcp-server?style=flat-square" alt="License"></a>
  <a href="https://walidfaour.github.io/pwndoc-mcp-server"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue?style=flat-square" alt="Documentation"></a>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#%EF%B8%8F-configuration">Configuration</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-documentation">Documentation</a>
</p>

---

## 🎯 Overview

PwnDoc MCP Server enables AI assistants to interact with your PwnDoc penetration testing documentation system through the [Model Context Protocol](https://modelcontextprotocol.io/). Query audits, manage findings, generate reports, and more—all through natural language.

### Two Implementations

| Version | Best For | Size | Install |
|---------|----------|------|---------|
| [**Python**](#python-installation) | Most users, extensibility | ~50MB | `pip install pwndoc-mcp-server` |
| [**Native C++**](#native-installation) | Portability, minimal deps | ~5MB | [Download binary](https://github.com/walidfaour/pwndoc-mcp-server/releases) |

## ✨ Features

- 🔌 **89 MCP Tools** - Complete coverage of PwnDoc API
- 🔐 **Secure Authentication** - JWT tokens with auto-refresh
- ⚡ **Rate Limiting** - Built-in protection for API limits
- 📊 **Comprehensive Logging** - Debug, file, and JSON logging
- 🌍 **Cross-Platform** - Linux, macOS, Windows support
- 🐳 **Docker Ready** - Pre-built container images
- 📦 **Multiple Installation Methods** - pip, apt, yum, binaries
- 🚀 **Native Binary** - Optional C++ implementation for portability

## 📥 Installation

### Python Installation

```bash
# Basic installation
pip install pwndoc-mcp-server

# With CLI enhancements
pip install pwndoc-mcp-server[cli]

# With all features
pip install pwndoc-mcp-server[all]
```

**Kali Linux Users:** If you encounter errors during installation, use a virtual environment:

```bash
sudo apt update
sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pwndoc-mcp-server
```

### Native Installation

Download pre-built binaries from [Releases](https://github.com/walidfaour/pwndoc-mcp-server/releases):

| Platform | Binary |
|----------|--------|
| Linux x64 | `pwndoc-mcp-linux-x64` |
| macOS x64 | `pwndoc-mcp-macos-x64` |
| macOS ARM | `pwndoc-mcp-macos-arm64` |
| Windows | `pwndoc-mcp-windows-x64.exe` |

```bash
# Linux/macOS
curl -LO https://github.com/walidfaour/pwndoc-mcp-server/releases/latest/download/pwndoc-mcp-linux-x64
chmod +x pwndoc-mcp-linux-x64
./pwndoc-mcp-linux-x64
```

### Installation Matrix

| Platform | Method | Command |
|----------|--------|---------|
| **Any** | pip | `pip install pwndoc-mcp-server` |
| **Any** | pipx | `pipx install pwndoc-mcp-server` |
| **Linux (Debian/Ubuntu)** | apt | `sudo apt install pwndoc-mcp-server` |
| **Linux (RHEL/CentOS)** | yum | `sudo yum install pwndoc-mcp-server` |
| **macOS** | Homebrew | `brew install pwndoc-mcp-server` |
| **Windows** | Scoop | `scoop install pwndoc-mcp-server` |
| **Any** | Docker | `docker pull ghcr.io/walidfaour/pwndoc-mcp-server` |
| **Any** | Binary | [Download from Releases](https://github.com/walidfaour/pwndoc-mcp-server/releases) |

### From Source

```bash
# Python
git clone https://github.com/walidfaour/pwndoc-mcp-server.git
cd pwndoc-mcp-server/python
pip install -e .[dev]

# Native C++
cd ../native
mkdir build && cd build
cmake .. && make
```

## ⚙️ Configuration

### Quick Start (Interactive Setup)

```bash
pwndoc-mcp config init
```

The interactive wizard will guide you through configuration and support both authentication methods.

### Authentication Methods

You can authenticate using **environment variables**, **config file**, or **CLI arguments**.

**Option 1: Username/Password (Recommended)**
- ✅ Automatically handles token generation and refresh
- ✅ No manual token management required
- ✅ **Preferred** when both credentials and token are provided

```bash
# Environment variables
export PWNDOC_URL="https://pwndoc.example.com"
export PWNDOC_USERNAME="your-username"
export PWNDOC_PASSWORD="your-password"

# Or CLI arguments
pwndoc-mcp serve --url https://pwndoc.example.com --username user --password pass
pwndoc-mcp test --url https://pwndoc.example.com -u user -p pass
```

**Option 2: Pre-authenticated Token**
- Use if you have a JWT token
- ⚠️ Requires manual renewal when expired
- Only used if username/password not provided

```bash
# Environment variables
export PWNDOC_URL="https://pwndoc.example.com"
export PWNDOC_TOKEN="your-jwt-token"

# Or CLI arguments
pwndoc-mcp serve --url https://pwndoc.example.com --token your-jwt-token
```

**Authentication Priority:**
When multiple methods are configured, the system uses this priority:
1. **Username/Password** (if both provided) → automatic token refresh ✅
2. **Token** (if username/password not provided) → manual renewal required ⚠️

This means if you set all three (URL + username/password + token), it will use username/password and ignore the token.

### Configuration File

Create `~/.pwndoc-mcp/config.yaml`:

```yaml
url: https://pwndoc.example.com
username: your-username
password: your-password
verify_ssl: true
timeout: 30
```

## 🖥️ Claude Desktop Integration

### Automatic Installation (Recommended)

```bash
# Configure your PwnDoc credentials
pwndoc-mcp config init

# Automatically install for Claude Desktop
pwndoc-mcp claude-install

# Check installation status
pwndoc-mcp claude-status
```

This will automatically update the appropriate MCP configuration file:
- **Linux**: `~/.config/claude/mcp_servers.json`
- **macOS**: `~/Library/Application Support/Claude/mcp_servers.json`
- **Windows**: `%APPDATA%\Claude\mcp_servers.json`

### Manual Installation

Alternatively, manually add to your Claude Desktop configuration (`claude_desktop_config.json`):

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

### Using Python (pip)

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "pwndoc-mcp",
      "args": ["serve"],
      "env": {
        "PWNDOC_URL": "https://pwndoc.example.com",
        "PWNDOC_USERNAME": "your-username",
        "PWNDOC_PASSWORD": "your-password"
      }
    }
  }
}
```

### Using Native Binary

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "/path/to/pwndoc-mcp-linux-x64",
      "env": {
        "PWNDOC_URL": "https://pwndoc.example.com",
        "PWNDOC_TOKEN": "your-token"
      }
    }
  }
}
```

### Using Docker

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "docker",
      "args": ["run", "-i", "--rm",
        "-e", "PWNDOC_URL=https://pwndoc.example.com",
        "-e", "PWNDOC_TOKEN=your-token",
        "ghcr.io/walidfaour/pwndoc-mcp-server:latest"
      ]
    }
  }
}
```

## 🚀 Usage

### CLI Commands

```bash
# Test connection
pwndoc-mcp test

# List available tools
pwndoc-mcp tools

# Start MCP server
pwndoc-mcp serve

# Interactive config setup
pwndoc-mcp config init

# Claude Desktop integration
pwndoc-mcp claude-install   # Install MCP config for Claude
pwndoc-mcp claude-status    # Check installation status
pwndoc-mcp claude-uninstall # Remove MCP config
```

### Docker

```bash
docker run -it --rm \
  -e PWNDOC_URL="https://pwndoc.example.com" \
  -e PWNDOC_TOKEN="your-token" \
  ghcr.io/walidfaour/pwndoc-mcp-server:latest
```

## 🔧 Available Tools (89)

### Audits (15 tools)
`list_audits` `get_audit` `create_audit` `update_audit` `delete_audit` `get_audit_types` `create_audit_type` `update_audit_type` `delete_audit_type` `generate_audit_report` `get_audit_network` `update_audit_network` `sort_audit_findings` `update_audit_sorting` `move_audit_finding`

### Findings (12 tools)
`list_findings` `get_finding` `create_finding` `update_finding` `delete_finding` `search_findings` `get_finding_categories` `create_finding_category` `update_finding_category` `delete_finding_category` `import_findings` `export_findings`

### Vulnerabilities (8 tools)
`list_vulnerabilities` `get_vulnerability` `create_vulnerability` `update_vulnerability` `delete_vulnerability` `merge_vulnerability` `get_vulnerability_updates` `import_vulnerabilities`

### Clients & Companies (12 tools)
`list_clients` `get_client` `create_client` `update_client` `delete_client` `get_client_audits` `list_companies` `get_company` `create_company` `update_company` `delete_company` `get_company_stats`

### Users & Settings (16 tools)
`list_users` `get_user` `create_user` `update_user` `delete_user` `get_current_user` `update_current_user` `change_password` `get_settings` `update_settings` `get_reviews` `export_reviews` `list_languages` `create_language` `update_language` `delete_language`

### Templates (10 tools)
`list_templates` `get_template` `create_template` `update_template` `delete_template` `list_sections` `create_section` `update_section` `delete_section` `get_custom_fields`

### Images & Data (10 tools)
`upload_image` `get_image` `download_image` `delete_image` `get_statistics` `get_cvss_scores` `backup_data` `restore_data` `export_data` `import_data`

### Collaboration (6 tools)
`list_comments` `create_comment` `update_comment` `delete_comment` `get_audit_history` `get_finding_history`

[Full tool documentation →](https://walidfaour.github.io/pwndoc-mcp-server/tools)

## 📖 Documentation

- **GitHub Pages**: [walidfaour.github.io/pwndoc-mcp-server](https://walidfaour.github.io/pwndoc-mcp-server)
- **Repository docs**: [docs/](./docs/)

Quick links:
- [Getting Started Guide](https://walidfaour.github.io/pwndoc-mcp-server/getting-started/quick-start)
- [Configuration Reference](https://walidfaour.github.io/pwndoc-mcp-server/getting-started/configuration)
- [Tool Reference](https://walidfaour.github.io/pwndoc-mcp-server/tools/overview)
- [Docker Deployment](https://walidfaour.github.io/pwndoc-mcp-server/user-guide/docker)

## 📁 Project Structure

```
pwndoc-mcp-server/
├── python/                   # Python implementation
│   ├── src/pwndoc_mcp_server/
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── native/                   # C++ implementation
│   ├── src/
│   ├── include/
│   └── CMakeLists.txt
├── docs/                     # Documentation
├── assets/                   # Branding assets
├── debian/                   # Debian packaging
├── rpm/                      # RPM packaging
├── packaging/                # Homebrew/Scoop
└── .github/                  # CI/CD workflows
```

## 🔒 Security

See [SECURITY.md](SECURITY.md) for reporting vulnerabilities.

**Important:** This tool handles sensitive penetration testing data. Use only on authorized systems.

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# First, configure git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Clone and setup
git clone https://github.com/walidfaour/pwndoc-mcp-server.git
cd pwndoc-mcp-server/python
pip install -e .[dev]
pytest
```

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [PwnDoc](https://github.com/pwndoc/pwndoc) - The penetration testing documentation platform
- **Walid Faour** - security@walidfaour.com

---

<p align="center">
  Made with ❤️ by Walid Faour
</p>
