# Logging & Debugging

PwnDoc MCP Server includes comprehensive logging for troubleshooting and monitoring.

## Log Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `DEBUG` | Detailed diagnostic information | Development, troubleshooting |
| `INFO` | General operational messages | Normal operation |
| `WARNING` | Potential issues | Monitoring |
| `ERROR` | Error conditions | Problem investigation |
| `CRITICAL` | Severe errors | System failures |

## Configuration

### Environment Variable

```bash
export PWNDOC_LOG_LEVEL=DEBUG
```

### Config File

```yaml
# ~/.pwndoc-mcp/config.yaml
log_level: DEBUG
log_file: /var/log/pwndoc-mcp/server.log
```

### CLI Flag

```bash
pwndoc-mcp serve --log-level DEBUG
```

## Log Output

### Console Output

By default, logs go to stderr with colored output:

```
2024-12-20 10:30:45 INFO     Server starting...
2024-12-20 10:30:45 INFO     Connected to PwnDoc at https://pwndoc.example.com
2024-12-20 10:30:46 DEBUG    Authenticated as: pentester
2024-12-20 10:30:47 INFO     MCP server ready
```

### File Output

Enable file logging:

```bash
export PWNDOC_LOG_FILE=/var/log/pwndoc-mcp/server.log
```

Features:
- Automatic log rotation (10MB max, 5 backups)
- UTF-8 encoding
- Atomic writes

### JSON Format

For log aggregation systems:

```bash
export PWNDOC_LOG_FORMAT=json
```

Output:
```json
{"timestamp": "2024-12-20T10:30:45.123Z", "level": "INFO", "message": "Server starting...", "module": "server"}
```

## Debug Mode

Enable comprehensive debugging:

```bash
# Full debug mode
export PWNDOC_LOG_LEVEL=DEBUG
export PWNDOC_LOG_FILE=/tmp/pwndoc-debug.log

# Run server
pwndoc-mcp serve
```

### What DEBUG Level Shows

- All HTTP requests and responses
- Authentication flow details
- Token refresh operations
- Tool invocations and parameters
- Timing information
- Rate limiter state

Example DEBUG output:

```
DEBUG    HTTP Request: GET /api/audits
DEBUG    Headers: {'Authorization': 'Bearer eyJ...', 'Content-Type': 'application/json'}
DEBUG    Response: 200 OK (245ms)
DEBUG    Response body: [{"_id": "507f1f77bcf86cd799439011", ...}]
DEBUG    Tool 'list_audits' completed in 251ms
```

## Log Locations

### Default Paths

| Platform | Console | File (if enabled) |
|----------|---------|-------------------|
| Linux | stderr | `~/.pwndoc-mcp/logs/server.log` |
| macOS | stderr | `~/Library/Logs/pwndoc-mcp/server.log` |
| Windows | stderr | `%LOCALAPPDATA%\pwndoc-mcp\logs\server.log` |

### Docker

```yaml
# docker-compose.yml
services:
  pwndoc-mcp:
    volumes:
      - ./logs:/var/log/pwndoc-mcp
    environment:
      - PWNDOC_LOG_FILE=/var/log/pwndoc-mcp/server.log
```

## Viewing Logs

### Real-time Monitoring

```bash
# Follow log file
tail -f /var/log/pwndoc-mcp/server.log

# With filtering
tail -f /var/log/pwndoc-mcp/server.log | grep ERROR

# Pretty print JSON logs
tail -f /var/log/pwndoc-mcp/server.log | jq .
```

### Search Logs

```bash
# Find errors
grep ERROR /var/log/pwndoc-mcp/server.log

# Find specific audit
grep "507f1f77bcf86cd799439011" /var/log/pwndoc-mcp/server.log

# Count requests
grep "HTTP Request" /var/log/pwndoc-mcp/server.log | wc -l
```

## Sensitive Data

### What's NOT Logged

- Passwords (never logged)
- Full JWT tokens (only first/last 4 chars)
- Response bodies containing credentials

### What IS Logged (DEBUG only)

- Usernames
- Audit IDs and names
- Finding titles
- API endpoints called

### Redaction

Sensitive fields are automatically redacted:

```
DEBUG    Config loaded: url=https://pwndoc.com, username=pentester, password=***, token=eyJh...XYZ
```

## Claude Desktop Logs

When debugging Claude Desktop integration:

### macOS

```bash
# Claude Desktop logs
tail -f ~/Library/Logs/Claude/main.log

# MCP-specific logs
tail -f ~/Library/Logs/Claude/mcp.log
```

### Windows

```powershell
Get-Content "$env:APPDATA\Claude\logs\main.log" -Wait
```

### Linux

```bash
tail -f ~/.config/Claude/logs/main.log
```

## Common Log Patterns

### Successful Connection

```
INFO     Loading configuration...
INFO     Configuration valid
INFO     Connecting to https://pwndoc.example.com
INFO     Authentication successful (user: pentester, role: user)
INFO     MCP server ready on stdio transport
```

### Authentication Failure

```
INFO     Connecting to https://pwndoc.example.com
ERROR    Authentication failed: Invalid credentials
ERROR    HTTP 401: {"status": "error", "datas": "Invalid credentials"}
```

### Rate Limiting

```
WARNING  Rate limit approaching (45/50 requests in window)
WARNING  Rate limit exceeded, waiting 15s before retry
INFO     Rate limit reset, resuming requests
```

### Network Error

```
ERROR    Connection failed: ConnectionRefusedError
ERROR    Retry 1/3 in 2s...
ERROR    Retry 2/3 in 4s...
ERROR    Retry 3/3 in 8s...
CRITICAL All retries exhausted, giving up
```

## Log Rotation

### Automatic Rotation

Default settings:
- Max file size: 10 MB
- Backup count: 5
- Naming: `server.log`, `server.log.1`, `server.log.2`, etc.

### Custom Rotation

```yaml
# config.yaml
log_file: /var/log/pwndoc-mcp/server.log
log_max_bytes: 52428800  # 50 MB
log_backup_count: 10
```

### External Rotation (logrotate)

```
# /etc/logrotate.d/pwndoc-mcp
/var/log/pwndoc-mcp/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 pwndoc pwndoc
}
```

## Integration with Log Systems

### Syslog

```bash
# Forward to syslog
pwndoc-mcp serve 2>&1 | logger -t pwndoc-mcp
```

### Systemd Journal

```bash
# View with journalctl
journalctl -u pwndoc-mcp -f
```

### Elasticsearch/Logstash

Use JSON format and ship with Filebeat:

```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    paths:
      - /var/log/pwndoc-mcp/*.log
    json.keys_under_root: true
```

## Performance Considerations

### Log Level Impact

| Level | Performance Impact |
|-------|-------------------|
| ERROR | Minimal |
| WARNING | Minimal |
| INFO | Low |
| DEBUG | Moderate (not for production) |

### Recommendations

- **Production**: Use `INFO` level with file output
- **Development**: Use `DEBUG` level
- **Troubleshooting**: Temporarily enable `DEBUG`
