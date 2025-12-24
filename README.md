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

Both implementations have **complete feature parity** - all features work identically.

| Version | Best For | Size | Install |
|---------|----------|------|---------|
| [**Python**](#python-installation) | Most users, extensibility | ~50MB | `pip install pwndoc-mcp-server` |
| [**Native C++**](#native-installation) | Performance, minimal deps | ~5MB | [Download binary](https://github.com/walidfaour/pwndoc-mcp-server/releases) |

## ✨ Features

- 🔌 **90 MCP Tools** - Complete coverage of PwnDoc API (all endpoints)
- 🔐 **Secure Authentication** - JWT tokens with auto-refresh (both implementations)
- ⚡ **Rate Limiting** - Built-in sliding window rate limiter (both implementations)
- 🔄 **Automatic Retries** - Exponential backoff for failed requests (both implementations)
- 📊 **Comprehensive Logging** - Debug, file, and JSON logging (both implementations)
- 🌍 **Cross-Platform** - Linux, macOS, Windows support
- 🐳 **Docker Ready** - Pre-built container images


Tip: Use `pwndoc-mcp tools` to list all available tools with descriptions.

[Full tool documentation →](./tools/overview/)


## 📖 Documentation

- GitHub Pages: walidfaour.github.io/pwndoc-mcp-server
- See the full docs in the `docs/` directory or on the GitHub Pages site.
