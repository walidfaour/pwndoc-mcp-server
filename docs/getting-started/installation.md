# Installation

PwnDoc MCP Server can be installed through multiple methods depending on your platform and preferences.

## Recommended: pip (Python Package)

The easiest way to install on any platform with Python:

```bash
# Basic installation
pip install pwndoc-mcp-server

# With CLI support (recommended)
pip install pwndoc-mcp-server[cli]

# With SSE transport support
pip install pwndoc-mcp-server[sse]

# Full installation with all features
pip install pwndoc-mcp-server[all]

# Development installation
pip install pwndoc-mcp-server[dev]
```

### Verify Installation

```bash
pwndoc-mcp --version
pwndoc-mcp --help
```

## Docker

Pull the official image:

```bash
docker pull ghcr.io/walidfaour/pwndoc-mcp-server:latest
```

Or build from source:

```bash
git clone https://github.com/walidfaour/pwndoc-mcp-server.git
cd pwndoc-mcp-server
docker build -t pwndoc-mcp-server .
```

### Run with Docker

```bash
docker run -it --rm \
  -e PWNDOC_URL=https://your-pwndoc-instance.com \
  -e PWNDOC_USERNAME=your-username \
  -e PWNDOC_PASSWORD=your-password \
  ghcr.io/walidfaour/pwndoc-mcp-server
```

## Standalone Binary

Download pre-compiled binaries from [GitHub Releases](https://github.com/walidfaour/pwndoc-mcp-server/releases):

### Linux (x64)

```bash
wget https://github.com/walidfaour/pwndoc-mcp-server/releases/latest/download/pwndoc-mcp-server-linux-x64
chmod +x pwndoc-mcp-server-linux-x64
sudo mv pwndoc-mcp-server-linux-x64 /usr/local/bin/pwndoc-mcp
```

### macOS (x64)

```bash
curl -LO https://github.com/walidfaour/pwndoc-mcp-server/releases/latest/download/pwndoc-mcp-server-macos-x64
chmod +x pwndoc-mcp-server-macos-x64
sudo mv pwndoc-mcp-server-macos-x64 /usr/local/bin/pwndoc-mcp
```

### Windows (x64)

Download `pwndoc-mcp-server-windows-x64.exe` from the releases page and add to your PATH.

## System Packages

### Debian/Ubuntu (apt)

```bash
# Download the .deb package
wget https://github.com/walidfaour/pwndoc-mcp-server/releases/latest/download/pwndoc-mcp-server_1.0.2_amd64.deb

# Install
sudo dpkg -i pwndoc-mcp-server_1.0.2_amd64.deb

# Or with apt (handles dependencies)
sudo apt install ./pwndoc-mcp-server_1.0.2_amd64.deb
```

### RHEL/Fedora/CentOS (yum/dnf)

```bash
# Download the .rpm package
wget https://github.com/walidfaour/pwndoc-mcp-server/releases/latest/download/pwndoc-mcp-server-1.0.2-1.x86_64.rpm

# Install with yum
sudo yum localinstall pwndoc-mcp-server-1.0.2-1.x86_64.rpm

# Or with dnf
sudo dnf install ./pwndoc-mcp-server-1.0.2-1.x86_64.rpm
```

### Homebrew (macOS)

```bash
# Add the tap
brew tap walidfaour/pwndoc

# Install
brew install pwndoc-mcp-server
```

### Scoop (Windows)

```powershell
# Add the bucket
scoop bucket add pwndoc https://github.com/walidfaour/scoop-pwndoc

# Install
scoop install pwndoc-mcp-server
```

## From Source

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Steps

```bash
# Clone the repository
git clone https://github.com/walidfaour/pwndoc-mcp-server.git
cd pwndoc-mcp-server

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev]"

# Verify installation
pwndoc-mcp --version
```

## Requirements

### Runtime Requirements

| Requirement | Minimum Version |
|-------------|-----------------|
| Python | 3.8+ |
| PwnDoc | 3.0+ |

### Python Dependencies

Automatically installed via pip:

- `httpx` - Async HTTP client
- `pyyaml` - YAML configuration
- `typer` - CLI framework (with `[cli]`)
- `rich` - Terminal formatting (with `[cli]`)
- `aiohttp` - SSE transport (with `[sse]`)

## Next Steps

After installation:

1. [Configure your connection](configuration.md)
2. [Quick start guide](quick-start.md)
3. [Set up Claude Desktop integration](../user-guide/claude-desktop.md)
