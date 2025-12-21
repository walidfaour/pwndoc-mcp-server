# Vulnerability Template Tools

Tools for managing the reusable vulnerability template library.

## Overview

Vulnerability templates are pre-defined findings that can be reused across audits. They help maintain consistency and save time when documenting common vulnerabilities.

## list_vulnerabilities

List all vulnerability templates in the library.

### Parameters

None.

### Examples

> "Show me all vulnerability templates"

> "List the vulnerability library"

### Response

```json
[
  {
    "_id": "507f1f77bcf86cd799439051",
    "cvssv3": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    "priority": 1,
    "remediationComplexity": 2,
    "category": "Web Application",
    "details": [...]
  }
]
```

---

## get_vulnerabilities_by_locale

Get vulnerability templates for a specific language.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `locale` | string | No | Language code (default: "en") |

### Examples

> "Show me vulnerability templates in English"

> "Get French vulnerability templates"

---

## create_vulnerability

Create a new vulnerability template.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `details` | object | Yes | Vulnerability details by locale |
| `cvssv3` | string | No | CVSS v3 vector |
| `priority` | integer | No | Priority (1-4) |
| `remediation_complexity` | integer | No | Complexity (1-3) |
| `category` | string | No | Category |
| `status` | integer | No | Status |

### Details Object Structure

```json
{
  "details": [
    {
      "locale": "en",
      "title": "SQL Injection",
      "vulnType": "Injection",
      "description": "SQL injection allows...",
      "observation": "The application accepts...",
      "remediation": "Use parameterized queries...",
      "references": ["https://owasp.org/..."]
    }
  ]
}
```

### Examples

> "Create a new template for Server-Side Request Forgery"

> "Add an IDOR vulnerability template to the library"

---

## update_vulnerability

Update an existing vulnerability template.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vulnerability_id` | string | Yes | The vulnerability ID |
| `details` | object | No | Updated details |
| `cvssv3` | string | No | Updated CVSS |
| `priority` | integer | No | Updated priority |
| `remediation_complexity` | integer | No | Updated complexity |
| `category` | string | No | Updated category |

### Examples

> "Update the XSS template with new remediation guidance"

> "Change the CVSS score for the CSRF template"

---

## delete_vulnerability

Delete a vulnerability template.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vulnerability_id` | string | Yes | The vulnerability ID |

### Examples

> "Remove the deprecated SSLv3 template"

---

## bulk_delete_vulnerabilities

Delete multiple vulnerability templates at once.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vulnerability_ids` | array | Yes | Array of vulnerability IDs |

### Examples

> "Delete all the test templates I created"

---

## export_vulnerabilities

Export all vulnerability templates.

### Parameters

None.

### Examples

> "Export the entire vulnerability library"

### Response

JSON array of all vulnerability templates, suitable for backup or import.

---

## create_vulnerability_from_finding

Create a new template from an existing finding.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `locale` | string | Yes | Language code |
| `title` | string | Yes | Template title |
| `vuln_type` | string | No | Vulnerability type |
| `description` | string | No | Description |
| `observation` | string | No | Observation |
| `remediation` | string | No | Remediation |
| `cvssv3` | string | No | CVSS vector |
| `priority` | integer | No | Priority |
| `remediation_complexity` | integer | No | Complexity |
| `category` | string | No | Category |
| `references` | array | No | References |

### Examples

> "Save this SQL injection finding as a reusable template"

> "Create a template from the API authentication bypass we found"

---

## get_vulnerability_updates

Check if a vulnerability template has available updates.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vulnerability_id` | string | Yes | The vulnerability ID |

### Examples

> "Are there updates for the XSS template?"

---

## merge_vulnerability

Merge a vulnerability template with its updates.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vulnerability_id` | string | Yes | The vulnerability ID |

### Examples

> "Apply the pending updates to the SQL injection template"

---

## Usage Patterns

### Building a Template Library

```
1. create_vulnerability → Add new templates
2. Organize by category
3. Maintain consistent CVSS scoring
4. Include references (CWE, OWASP)
```

### Using Templates in Audits

```
1. get_vulnerabilities_by_locale → Find matching template
2. create_finding → Copy template data to audit
3. update_finding → Customize for specific instance
```

### Template Maintenance

```
1. Review periodically
2. Update CVSS for new attack techniques
3. Refresh remediation guidance
4. Add emerging vulnerability types
```

---

## Best Practices

### Template Structure

- **Title**: Clear, concise vulnerability name
- **Description**: Generic explanation of the vulnerability class
- **Observation**: Template text with placeholders for specifics
- **Remediation**: Actionable, technology-agnostic guidance
- **References**: Link to OWASP, CWE, vendor documentation

### Categorization

Suggested categories:
- Web Application
- API Security
- Mobile Application
- Infrastructure
- Cloud Security
- Authentication
- Authorization
- Cryptography
- Configuration

### CVSS Scoring

- Use CVSS 3.1 vectors
- Score for typical impact, not worst case
- Document assumptions in description
