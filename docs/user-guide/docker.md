# Docker Deployment

PwnDoc MCP Server is available as a Docker image for containerized deployments.

## Quick Start

```bash
# Pull the image
docker pull ghcr.io/walidfaour/pwndoc-mcp-server:latest

# Run with environment variables
docker run -it --rm \
  -e PWNDOC_URL=https://your-pwndoc.com \
  -e PWNDOC_USERNAME=your-username \
  -e PWNDOC_PASSWORD=your-password \
  ghcr.io/walidfaour/pwndoc-mcp-server
```

## Image Tags

| Tag | Description |
|-----|-------------|
| `latest` | Latest stable release |
| `1.0.8` | Specific version |
| `1.0` | Latest patch of version 1.0 |
| `main` | Latest from main branch |
| `sha-abc1234` | Specific commit |

## Docker Compose

### Basic Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  pwndoc-mcp:
    image: ghcr.io/walidfaour/pwndoc-mcp-server:latest
    environment:
      - PWNDOC_URL=https://your-pwndoc.com
      - PWNDOC_USERNAME=your-username
      - PWNDOC_PASSWORD=your-password
    stdin_open: true
    tty: true
```

### With Configuration File

```yaml
version: '3.8'

services:
  pwndoc-mcp:
    image: ghcr.io/walidfaour/pwndoc-mcp-server:latest
    volumes:
      - ./config.yaml:/home/pwndoc/.pwndoc-mcp/config.yaml:ro
    stdin_open: true
    tty: true
```

### SSE Transport

For web client integration:

```yaml
version: '3.8'

services:
  pwndoc-mcp-sse:
    image: ghcr.io/walidfaour/pwndoc-mcp-server:latest
    command: ["pwndoc-mcp", "serve", "--transport", "sse"]
    ports:
      - "8080:8080"
    environment:
      - PWNDOC_URL=https://your-pwndoc.com
      - PWNDOC_TOKEN=your-jwt-token
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Production Configuration

```yaml
version: '3.8'

services:
  pwndoc-mcp:
    image: ghcr.io/walidfaour/pwndoc-mcp-server:latest
    restart: unless-stopped
    environment:
      - PWNDOC_URL=${PWNDOC_URL}
      - PWNDOC_TOKEN=${PWNDOC_TOKEN}
      - PWNDOC_LOG_LEVEL=INFO
    volumes:
      - pwndoc-logs:/var/log/pwndoc-mcp
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.1'
          memory: 64M
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp

volumes:
  pwndoc-logs:
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PWNDOC_URL` | Yes | PwnDoc instance URL |
| `PWNDOC_USERNAME` | No* | Username for auth |
| `PWNDOC_PASSWORD` | No* | Password for auth |
| `PWNDOC_TOKEN` | No* | JWT token for auth |
| `PWNDOC_VERIFY_SSL` | No | Verify SSL (default: true) |
| `PWNDOC_TIMEOUT` | No | Request timeout (default: 30) |
| `PWNDOC_LOG_LEVEL` | No | Log level (default: INFO) |

*Either username/password or token is required.

## Building from Source

```bash
# Clone repository
git clone https://github.com/walidfaour/pwndoc-mcp-server.git
cd pwndoc-mcp-server

# Build image
docker build -t pwndoc-mcp-server .

# Build with specific Python version
docker build --build-arg PYTHON_VERSION=3.11 -t pwndoc-mcp-server .
```

### Multi-stage Build

The Dockerfile uses multi-stage builds for optimization:

1. **Builder stage**: Installs dependencies in virtual environment
2. **Runtime stage**: Copies only necessary files, runs as non-root user

## Claude Desktop with Docker

Configure Claude Desktop to use the Docker container:

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

### With Docker Compose

```json
{
  "mcpServers": {
    "pwndoc": {
      "command": "docker-compose",
      "args": ["-f", "/path/to/docker-compose.yml", "run", "--rm", "pwndoc-mcp"]
    }
  }
}
```

## Health Checks

The container includes a health check endpoint (SSE mode):

```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.8",
  "pwndoc_connected": true
}
```

## Networking

### Connecting to Local PwnDoc

If PwnDoc runs locally:

```yaml
services:
  pwndoc-mcp:
    image: ghcr.io/walidfaour/pwndoc-mcp-server:latest
    environment:
      - PWNDOC_URL=http://host.docker.internal:8443
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

### Docker Network

Connect to PwnDoc in the same Docker network:

```yaml
services:
  pwndoc:
    image: pwndoc/pwndoc:latest
    networks:
      - pwndoc-net

  pwndoc-mcp:
    image: ghcr.io/walidfaour/pwndoc-mcp-server:latest
    environment:
      - PWNDOC_URL=http://pwndoc:8443
    networks:
      - pwndoc-net

networks:
  pwndoc-net:
```

## Security Considerations

### Running as Non-Root

The image runs as a non-root user (`pwndoc`, UID 1000) by default.

### Read-Only Filesystem

For extra security:

```yaml
services:
  pwndoc-mcp:
    image: ghcr.io/walidfaour/pwndoc-mcp-server:latest
    read_only: true
    tmpfs:
      - /tmp
```

### Secrets Management

Use Docker secrets for credentials:

```yaml
services:
  pwndoc-mcp:
    image: ghcr.io/walidfaour/pwndoc-mcp-server:latest
    environment:
      - PWNDOC_URL=https://pwndoc.example.com
    secrets:
      - pwndoc_token

secrets:
  pwndoc_token:
    file: ./secrets/pwndoc_token.txt
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs pwndoc-mcp

# Run interactively
docker run -it --rm ghcr.io/walidfaour/pwndoc-mcp-server:latest /bin/sh
```

### Connection Issues

```bash
# Test connectivity from container
docker run --rm ghcr.io/walidfaour/pwndoc-mcp-server:latest \
  curl -v https://your-pwndoc.com/api/users/me
```

### SSL Certificate Errors

```yaml
environment:
  - PWNDOC_VERIFY_SSL=false  # Only for development!
```

Or mount your CA certificate:

```yaml
volumes:
  - ./ca-cert.pem:/etc/ssl/certs/custom-ca.pem:ro
```

## Next Steps

- [Claude Desktop Integration](claude-desktop.md)
- [CLI Usage](cli.md)
- [Configuration Reference](../getting-started/configuration.md)
