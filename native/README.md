# PwnDoc MCP Server - Native C++

Lightweight C++ implementation compiling to a single portable binary (~5MB).

See the [main README](../README.md) for complete documentation.

## Quick Start

```bash
# Download from releases
curl -LO https://github.com/walidfaour/pwndoc-mcp-server/releases/latest/download/pwndoc-mcp-linux-x64
chmod +x pwndoc-mcp-linux-x64

# Configure & run
export PWNDOC_URL="https://your-pwndoc.com"
export PWNDOC_TOKEN="your-token"
./pwndoc-mcp-linux-x64
```

## Building from Source

### Prerequisites

- CMake 3.16+
- C++17 compiler (GCC 9+, Clang 10+, MSVC 2019+)
- libcurl development headers
- nlohmann-json

### Build

```bash
# Linux/macOS
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# Windows
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
```

## Project Structure

```
native/
├── src/
│   ├── main.cpp         # Entry point
│   ├── server.cpp/hpp   # MCP server
│   ├── client.cpp/hpp   # PwnDoc API client
│   ├── config.cpp/hpp   # Configuration
│   └── tools.cpp/hpp    # Tool definitions
├── include/             # Headers
└── CMakeLists.txt       # Build config
```
