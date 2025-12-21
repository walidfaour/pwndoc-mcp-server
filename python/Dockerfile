FROM python:3.11-slim

LABEL org.opencontainers.image.title="PwnDoc MCP Server"
LABEL org.opencontainers.image.description="MCP Server for PwnDoc - AI-Powered Penetration Testing Documentation"
LABEL org.opencontainers.image.source="https://github.com/walidfaour/pwndoc-mcp-server"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install --no-cache-dir .

# Create non-root user
RUN useradd -m -u 1000 pwndoc && chown -R pwndoc:pwndoc /app
USER pwndoc

# Environment
ENV PYTHONUNBUFFERED=1

# Use CLI entrypoint (identical to pip-installed behavior)
ENTRYPOINT ["pwndoc-mcp"]
CMD ["serve"]
