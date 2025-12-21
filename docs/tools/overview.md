# Tool Reference Overview

PwnDoc MCP Server provides **90 MCP tools** with complete coverage of the PwnDoc API (all 92 endpoints except 2 internal auth endpoints).

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| [Audit Management](audits.md) | 13 | Create, read, update, delete audits + sections |
| [Finding Management](findings.md) | 9 | Manage vulnerabilities within audits |
| [Client & Company](clients-companies.md) | 8 | Manage clients and companies |
| [Vulnerability Templates](vulnerabilities.md) | 9 | Reusable vulnerability library + updates |
| [Users & Authentication](users-settings.md) | 11 | User management + TOTP/2FA |
| Data Types & Configuration | 22 | Languages, audit types, sections, custom fields |
| Settings & Templates | 10 | System settings, report templates |
| Images | 4 | Image management |
| [Reports & Statistics](reports-statistics.md) | 4 | Generate reports and view metrics |

## Quick Reference

### Audit Management (13 tools)

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
| `get_audit_sections` | Get audit sections content |
| `update_audit_sections` | Update audit sections content |
| `toggle_audit_approval` | Toggle approval status |
| `update_review_status` | Set review ready status |
| `generate_audit_report` | Generate DOCX report |

### Finding Management (9 tools)

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
| `get_all_findings_with_context` | Get all findings with full audit context (CWE, OWASP, HTML stripping) |

### Client & Company (8 tools)

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

### Vulnerability Templates (9 tools)

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

### Users & Authentication (11 tools)

| Tool | Description |
|------|-------------|
| `list_users` | List all users (admin only) |
| `get_user` | Get user by username |
| `get_current_user` | Get authenticated user info |
| `create_user` | Create new user (admin only) |
| `update_user` | Update user (admin only) |
| `update_current_user` | Update own profile |
| `list_reviewers` | List available reviewers |
| `get_totp_status` | Get TOTP (2FA) status |
| `setup_totp` | Setup TOTP (2FA) |
| `disable_totp` | Disable TOTP (2FA) |

### Data Types & Configuration (22 tools)

**Languages (4 tools)**
- `list_languages` - List configured languages
- `create_language` - Create new language
- `update_language` - Update language
- `delete_language` - Delete language

**Audit Types (4 tools)**
- `list_audit_types` - List audit types
- `create_audit_type` - Create new audit type
- `update_audit_type` - Update audit type
- `delete_audit_type` - Delete audit type

**Vulnerability Types (4 tools)**
- `list_vulnerability_types` - List vulnerability types
- `create_vulnerability_type` - Create new vulnerability type
- `update_vulnerability_type` - Update vulnerability type
- `delete_vulnerability_type` - Delete vulnerability type

**Vulnerability Categories (4 tools)**
- `list_vulnerability_categories` - List categories
- `create_vulnerability_category` - Create new category
- `update_vulnerability_category` - Update category
- `delete_vulnerability_category` - Delete category

**Sections (4 tools)**
- `list_sections` - List section definitions
- `create_section` - Create new section
- `update_section` - Update section
- `delete_section` - Delete section

**Custom Fields (4 tools)**
- `list_custom_fields` - List custom field definitions
- `create_custom_field` - Create new custom field
- `update_custom_field` - Update custom field
- `delete_custom_field` - Delete custom field

### Settings & Templates (10 tools)

| Tool | Description |
|------|-------------|
| `get_settings` | Get system settings |
| `get_public_settings` | Get public settings |
| `update_settings` | Update system settings |
| `export_settings` | Export all settings |
| `import_settings` | Import/revert settings |
| `list_templates` | List report templates |
| `create_template` | Create new template |
| `update_template` | Update template |
| `delete_template` | Delete template |
| `download_template` | Download template file |

### Images (4 tools)

| Tool | Description |
|------|-------------|
| `get_image` | Get image metadata |
| `download_image` | Download image file |
| `upload_image` | Upload image to audit |
| `delete_image` | Delete image |

### Reports & Statistics (4 tools)

| Tool | Description |
|------|-------------|
| `generate_audit_report` | Generate DOCX report |
| `get_statistics` | Get comprehensive statistics |
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
