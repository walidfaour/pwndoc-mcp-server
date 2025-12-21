# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in PwnDoc MCP Server, please report it responsibly.

### DO NOT

- Open a public GitHub issue
- Post details on social media
- Exploit the vulnerability

### DO

1. **Email**: Send details to security@walidfaour.com
2. **Encrypt**: Use our PGP key if possible (see below)
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

| Timeframe | Action |
|-----------|--------|
| 24 hours  | Acknowledgment of your report |
| 48 hours  | Initial assessment and severity rating |
| 7 days    | Detailed response with remediation plan |
| 30 days   | Fix released (for critical issues) |
| 90 days   | Public disclosure (coordinated) |

### Severity Ratings

| Severity | Description | Response Time |
|----------|-------------|---------------|
| Critical | RCE, credential exposure, data breach | 24-48 hours |
| High     | Authentication bypass, privilege escalation | 7 days |
| Medium   | Information disclosure, DoS | 14 days |
| Low      | Minor issues, hardening | 30 days |

## Security Best Practices

When using PwnDoc MCP Server:

### Configuration

```yaml
# ✅ Good: Use environment variables for secrets
# Set PWNDOC_PASSWORD in environment, not in config file

# ❌ Bad: Don't commit credentials
# password: "my_secret_password"
```

### File Permissions

```bash
# Secure your configuration
chmod 600 ~/.pwndoc-mcp/config.yaml

# Secure log files
chmod 640 /var/log/pwndoc-mcp/*.log
```

### Network Security

- Always use HTTPS for PwnDoc connections
- Use `verify_ssl: true` in production
- Consider network segmentation
- Use firewall rules to restrict access

### Authentication

- Use strong, unique passwords
- Rotate credentials regularly
- Consider using token-based auth with short expiry
- Enable 2FA on PwnDoc if available

### Docker Security

```yaml
# docker-compose.yml security options
security_opt:
  - no-new-privileges:true
read_only: true
user: "1000:1000"
```

### Logging

- Don't log sensitive data
- Rotate logs regularly
- Monitor for suspicious activity
- Use centralized logging in production

## Known Security Considerations

### Credential Storage

- Credentials in config files should have restricted permissions (600)
- Environment variables are preferred over file-based storage
- Token refresh is handled automatically; old tokens are not stored

### API Communication

- All API calls use HTTPS by default
- SSL verification is enabled by default
- Self-signed certificates require explicit `verify_ssl: false`

### Rate Limiting

- Built-in rate limiting prevents accidental DoS
- Configurable limits for different environments
- Automatic backoff on 429 responses

### Error Handling

- Errors are logged without sensitive data
- Stack traces don't expose credentials
- Failed auth attempts are rate-limited

## Dependency Security

We regularly update dependencies and use:

- `pip-audit` for Python vulnerability scanning
- Dependabot for automated updates
- Regular security reviews

### Checking for Vulnerabilities

```bash
# Install pip-audit
pip install pip-audit

# Scan dependencies
pip-audit

# Check specific package
pip-audit --requirement requirements.txt
```

## PGP Key

For encrypted communications:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----
[PGP key would be here in production]
-----END PGP PUBLIC KEY BLOCK-----
```

## Bug Bounty

We don't currently have a formal bug bounty program, but we recognize security researchers in our:

- Security advisories
- Release notes
- Hall of Fame (SECURITY.md)

## Security Hall of Fame

We thank the following researchers for their responsible disclosures:

*No entries yet - be the first!*

## Contact

- Security issues: security@walidfaour.com
- General questions: https://github.com/walidfaour/pwndoc-mcp-server/discussions
- Documentation: https://walidfaour.github.io/pwndoc-mcp-server

---

*This security policy is reviewed quarterly and updated as needed.*
