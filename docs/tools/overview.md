# Tool Reference Overview

PwnDoc MCP Server provides 50+ tools organized into logical categories. This page provides an overview of all available tools.

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| [Audit Management](audits.md) | 12 | Create, read, update, delete audits |
| [Finding Management](findings.md) | 8 | Manage vulnerabilities within audits |
| [Client & Company](clients-companies.md) | 8 | Manage clients and companies |
| [Vulnerability Templates](vulnerabilities.md) | 10 | Reusable vulnerability library |
| [Users & Settings](users-settings.md) | 12 | User management and system config |
| [Reports & Statistics](reports-statistics.md) | 4 | Generate reports and view metrics |

## Quick Reference

### Audit Management

| Tool | Description |
|------|-------------|
| `list_audits` | List all audits, optionally filter by finding title |
| `get_audit` | Get complete audit details including findings |
| `get_audit_general` | Get audit metadata (name, dates, client) |
| `create_audit` | Create a new audit |
| `update_audit_general` | Update audit information |
| `delete_audit` | Delete an audit permanently |
| `get_audit_network` | Get network configuration |
| `update_audit_network` | Update network settings |
| `toggle_audit_approval` | Toggle approval status |
| `update_audit_review_status` | Set review ready status |
| `get_audit_section` | Get a specific section |
| `update_audit_section` | Update section content |

### Finding Management

| Tool | Description |
|------|-------------|
| `get_audit_findings` | Get all findings from an audit |
| `get_finding` | Get detailed finding information |
| `create_finding` | Create a new finding |
| `update_finding` | Update an existing finding |
| `delete_finding` | Delete a finding |
| `sort_findings` | Reorder findings in an audit |
| `move_finding` | Move finding between audits |
| `search_findings` | Search findings across all audits |
| `get_all_findings_with_context` | Get all findings with full audit context |

### Client & Company

| Tool | Description |
|------|-------------|
| `list_clients` | List all clients |
| `create_client` | Create a new client |
| `update_client` | Update client information |
| `delete_client` | Delete a client |
| `list_companies` | List all companies |
| `create_company` | Create a new company |
| `update_company` | Update company information |
| `delete_company` | Delete a company |

### Vulnerability Templates

| Tool | Description |
|------|-------------|
| `list_vulnerabilities` | List all vulnerability templates |
| `get_vulnerabilities_by_locale` | Get templates for specific language |
| `create_vulnerability` | Create new template |
| `update_vulnerability` | Update existing template |
| `delete_vulnerability` | Delete a template |
| `bulk_delete_vulnerabilities` | Delete multiple templates |
| `export_vulnerabilities` | Export all templates |
| `create_vulnerability_from_finding` | Create template from finding |
| `get_vulnerability_updates` | Check for template updates |
| `merge_vulnerability` | Merge template with updates |

### Users & Settings

| Tool | Description |
|------|-------------|
| `list_users` | List all users (admin only) |
| `get_user` | Get user by username |
| `get_current_user` | Get authenticated user info |
| `create_user` | Create new user (admin only) |
| `update_user` | Update user (admin only) |
| `update_current_user` | Update own profile |
| `list_reviewers` | List available reviewers |
| `get_settings` | Get system settings |
| `update_settings` | Update system settings |
| `get_public_settings` | Get public settings |
| `export_settings` | Export all settings |
| `revert_settings` | Revert to defaults |

### Reports & Statistics

| Tool | Description |
|------|-------------|
| `generate_audit_report` | Generate DOCX report |
| `get_statistics` | Get comprehensive statistics |
| `list_templates` | List report templates |
| `download_template` | Download template file |

### Configuration Management

| Tool | Description |
|------|-------------|
| `list_languages` | List configured languages |
| `list_audit_types` | List audit types |
| `list_vulnerability_types` | List vulnerability types |
| `list_vulnerability_categories` | List vulnerability categories |
| `list_sections` | List section definitions |
| `list_custom_fields` | List custom field definitions |
| `list_roles` | List user roles |

## Special Tools

### get_all_findings_with_context

This powerful tool retrieves ALL findings from ALL audits in a single request, including:

- Finding details (title, description, severity, CVSS)
- Parent audit information (name, client, company, dates)
- Team members and scope
- CWE references

**Use case**: Cross-audit analysis, vulnerability trending, compliance reporting.

```
"What are the most common vulnerabilities across all our pentests this year?"
```

### search_findings

Search findings across all audits by:

- Title keyword
- Severity (Critical, High, Medium, Low)
- Category
- Status

**Use case**: Finding similar vulnerabilities, pattern analysis.

```
"Find all high-severity findings related to authentication"
```

## Tool Usage Patterns

### Single Audit Operations

```
1. list_audits → Find audit ID
2. get_audit → Get full details
3. get_audit_findings → View findings
4. update_finding → Modify as needed
```

### Cross-Audit Analysis

```
1. get_all_findings_with_context → Get everything
2. Filter/analyze in Claude
3. Generate insights
```

### Documentation Workflow

```
1. list_audits → Select audit
2. get_audit → Review details
3. update_audit_section → Update narrative
4. generate_audit_report → Create report
```

## Next Steps

- [Audit Management Tools](audits.md)
- [Finding Management Tools](findings.md)
- [Client & Company Tools](clients-companies.md)
