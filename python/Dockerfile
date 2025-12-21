FROM python:3.11-slim

LABEL org.opencontainers.image.title="PwnDoc MCP Server"
LABEL org.opencontainers.image.description="MCP Server for PwnDoc - AI-Powered Penetration Testing Documentation"
LABEL org.opencontainers.image.source="https://github.com/walidfaour/pwndoc-mcp-server"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy source
COPY src/ ./src/

# Create non-root user
RUN useradd -m -u 1000 pwndoc && chown -R pwndoc:pwndoc /app
USER pwndoc

# Environment
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m", "pwndoc_mcp_server.server"]
