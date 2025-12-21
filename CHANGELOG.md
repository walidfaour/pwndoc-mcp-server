# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- WebSocket transport support
- Caching layer for frequently accessed data
- Prometheus metrics endpoint
- SSE heartbeat support

## [1.0.0] - 2024-12-20

### Added
- Initial release of PwnDoc MCP Server
- Complete MCP implementation with 50+ tools
- Support for all PwnDoc API endpoints:
  - Audit management (CRUD, reports, approval)
  - Finding management (CRUD, search, move)
  - Client and company management
  - Vulnerability template management
  - User management
  - Settings and configuration
- Multiple transport support:
  - stdio (for Claude Desktop)
  - SSE (for web clients)
- Authentication methods:
  - Username/password with JWT
  - Pre-configured JWT tokens
  - Automatic token refresh
- Configuration options:
  - Environment variables
  - YAML configuration file
  - JSON configuration file
  - CLI arguments
- CLI features:
  - Interactive configuration wizard
  - Connection testing
  - Direct tool queries
  - Tool listing
- Logging:
  - Console output with colors
  - File logging with rotation
  - JSON structured logging
  - Configurable log levels
- Rate limiting:
  - Sliding window rate limiter
  - Configurable limits
- Error handling:
  - Automatic retries with exponential backoff
  - Comprehensive error types
- Cross-platform support:
  - Linux (x64, arm64)
  - macOS (x64, arm64)
  - Windows (x64)
- Distribution methods:
  - PyPI package
  - Docker images
  - Standalone binaries
  - Debian packages (.deb)
  - RPM packages (.rpm)
- Documentation:
  - Comprehensive README
  - GitBook documentation
  - API reference
  - Configuration guide

### Security
- No hardcoded credentials
- Environment variable support for secrets
- Secure configuration file permissions (600)
- SSL/TLS verification (configurable)

## [0.1.0] - 2024-12-15

### Added
- Initial prototype
- Basic MCP server implementation
- Core PwnDoc API integration

---

## Version History Summary

| Version | Date | Highlights |
|---------|------|------------|
| 1.0.0 | 2024-12-20 | Initial stable release |
| 0.1.0 | 2024-12-15 | Prototype |

## Upgrade Guide

### Upgrading to 1.0.0

If upgrading from the prototype (0.1.0):

1. **Configuration**: Move from hardcoded values to environment variables
   ```bash
   export PWNDOC_URL="https://your-server.com"
   export PWNDOC_USERNAME="your-username"
   export PWNDOC_PASSWORD="your-password"
   ```

2. **Claude Desktop**: Update your `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "pwndoc": {
         "command": "pwndoc-mcp",
         "args": ["serve"],
         "env": {
           "PWNDOC_URL": "...",
           "PWNDOC_USERNAME": "...",
           "PWNDOC_PASSWORD": "..."
         }
       }
     }
   }
   ```

3. **Dependencies**: Update package:
   ```bash
   pip install --upgrade pwndoc-mcp-server
   ```

---

[Unreleased]: https://github.com/walidfaour/pwndoc-mcp-server/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/walidfaour/pwndoc-mcp-server/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/walidfaour/pwndoc-mcp-server/releases/tag/v0.1.0
