# Troubleshooting

Common issues and solutions for PwnDoc MCP Server.

## Connection Issues

### "Connection refused" or "Cannot connect"

**Symptoms:**
- `ConnectionRefusedError`
- `Connection timeout`
- CLI test fails

**Solutions:**

1. **Verify PwnDoc URL**
   ```bash
   curl https://your-pwndoc.com/api/users/me
   ```

2. **Check network connectivity**
   ```bash
   ping your-pwndoc.com
   traceroute your-pwndoc.com
   ```

3. **Verify firewall rules**
   - Ensure port 443 (or your custom port) is open
   - Check VPN connection if required

4. **Test with correct protocol**
   ```bash
   # Try both
   curl http://your-pwndoc.com/api/users/me
   curl https://your-pwndoc.com/api/users/me
   ```

### SSL Certificate Errors

**Symptoms:**
- `SSL: CERTIFICATE_VERIFY_FAILED`
- `SSL handshake failed`

**Solutions:**

1. **Self-signed certificates (development only)**
   ```bash
   export PWNDOC_VERIFY_SSL=false
   ```

2. **Add custom CA**
   ```bash
   export SSL_CERT_FILE=/path/to/ca-bundle.crt
   ```

3. **Update certificates**
   ```bash
   # macOS
   brew install ca-certificates
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install ca-certificates
   ```

## Authentication Issues

### "Authentication failed"

**Symptoms:**
- `401 Unauthorized`
- `Invalid credentials`
- Token errors

**Solutions:**

1. **Verify credentials**
   ```bash
   # Test login directly
   curl -X POST https://your-pwndoc.com/api/users/login \
     -H "Content-Type: application/json" \
     -d '{"username": "your-user", "password": "your-pass"}'
   ```

2. **Check for typos**
   ```bash
   pwndoc-mcp config show  # Review settings
   ```

3. **Token expired**
   ```bash
   # Get new token
   pwndoc-mcp config init
   ```

4. **User account issues**
   - Verify account is enabled in PwnDoc
   - Check role permissions

### "Token refresh failed"

**Solutions:**

1. Re-authenticate:
   ```bash
   pwndoc-mcp config init
   ```

2. Use username/password instead of token:
   ```bash
   unset PWNDOC_TOKEN
   export PWNDOC_USERNAME=your-user
   export PWNDOC_PASSWORD=your-pass
   ```

## Claude Desktop Issues

### Tools Not Appearing

**Symptoms:**
- PwnDoc tools not listed in Claude
- "No tools available"

**Solutions:**

1. **Verify config file syntax**
   ```bash
   # Check JSON is valid
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python -m json.tool
   ```

2. **Check pwndoc-mcp is in PATH**
   ```bash
   which pwndoc-mcp
   pwndoc-mcp --version
   ```

3. **Test server manually**
   ```bash
   pwndoc-mcp serve
   ```

4. **Restart Claude Desktop completely**
   - macOS: Cmd+Q then reopen
   - Windows: Right-click tray icon → Quit

5. **Check Claude Desktop logs**
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/main.log
   ```

### "Server failed to start"

**Solutions:**

1. **Use full path to executable**
   ```json
   {
     "mcpServers": {
       "pwndoc": {
         "command": "/usr/local/bin/pwndoc-mcp",
         "args": ["serve"]
       }
     }
   }
   ```

2. **Check for Python issues**
   ```bash
   python -c "import pwndoc_mcp_server"
   ```

3. **Enable debug logging**
   ```json
   {
     "mcpServers": {
       "pwndoc": {
         "command": "pwndoc-mcp",
         "args": ["serve"],
         "env": {
           "PWNDOC_LOG_LEVEL": "DEBUG",
           "PWNDOC_LOG_FILE": "/tmp/pwndoc-mcp.log"
         }
       }
     }
   }
   ```

## CLI Issues

### "Command not found"

**Solutions:**

1. **Install with CLI extras**
   ```bash
   pip install pwndoc-mcp-server[cli]
   ```

2. **Check PATH**
   ```bash
   echo $PATH
   pip show pwndoc-mcp-server  # Check install location
   ```

3. **Use python -m**
   ```bash
   python -m pwndoc_mcp_server.cli --help
   ```

### Import Errors

**Symptoms:**
- `ModuleNotFoundError`
- `ImportError`

**Solutions:**

1. **Reinstall**
   ```bash
   pip uninstall pwndoc-mcp-server
   pip install pwndoc-mcp-server[all]
   ```

2. **Check Python version**
   ```bash
   python --version  # Must be 3.8+
   ```

3. **Virtual environment issues**
   ```bash
   # Ensure venv is activated
   source venv/bin/activate
   pip install pwndoc-mcp-server[all]
   ```

## Docker Issues

### Container Won't Start

**Solutions:**

1. **Check logs**
   ```bash
   docker logs <container_id>
   ```

2. **Verify environment variables**
   ```bash
   docker run -it --rm ghcr.io/walidfaour/pwndoc-mcp-server:latest env | grep PWNDOC
   ```

3. **Test connectivity from container**
   ```bash
   docker run -it --rm ghcr.io/walidfaour/pwndoc-mcp-server:latest \
     curl -v https://your-pwndoc.com
   ```

### Can't Connect to Local PwnDoc

**Solutions:**

1. **Use host.docker.internal**
   ```bash
   docker run -e PWNDOC_URL=http://host.docker.internal:8443 ...
   ```

2. **Use host network**
   ```bash
   docker run --network host -e PWNDOC_URL=http://localhost:8443 ...
   ```

## API/Tool Errors

### "Rate limit exceeded"

**Solutions:**

1. **Wait and retry** - Rate limits reset after 60 seconds

2. **Reduce request frequency** in your workflow

3. **Use batch tools** like `get_all_findings_with_context`

### "Not found" Errors

**Solutions:**

1. **Verify ID exists**
   ```bash
   pwndoc-mcp query list_audits  # Get valid IDs
   ```

2. **Check permissions** - User may not have access to resource

### Timeout Errors

**Solutions:**

1. **Increase timeout**
   ```bash
   export PWNDOC_TIMEOUT=120
   ```

2. **Check PwnDoc server load**

3. **Use pagination** for large datasets

## Debug Mode

Enable comprehensive logging:

```bash
export PWNDOC_LOG_LEVEL=DEBUG
export PWNDOC_LOG_FILE=/tmp/pwndoc-mcp-debug.log
pwndoc-mcp test --verbose
```

Then check the log:
```bash
tail -f /tmp/pwndoc-mcp-debug.log
```

## Getting Help

If issues persist:

1. **Search existing issues**: [GitHub Issues](https://github.com/walidfaour/pwndoc-mcp-server/issues)

2. **Open a new issue** with:
   - Error message
   - Debug logs
   - Environment details
   - Steps to reproduce

3. **Community discussions**: [GitHub Discussions](https://github.com/walidfaour/pwndoc-mcp-server/discussions)
