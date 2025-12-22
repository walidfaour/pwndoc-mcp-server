# Finding Management Tools

Tools for managing vulnerabilities and findings within audits.

## get_audit_findings

Get all findings from a specific audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |

### Examples

> "Show me all findings in the Acme Corp audit"

> "List vulnerabilities for audit 507f1f77bcf86cd799439011"

### Response

```json
[
  {
    "_id": "507f1f77bcf86cd799439041",
    "title": "SQL Injection in Login Form",
    "vulnType": "Injection",
    "severity": "Critical",
    "cvssv3": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    "cvssScore": 9.8,
    "status": 1,
    "priority": 1
  }
]
```

---

## get_finding

Get detailed information about a specific finding.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `finding_id` | string | Yes | The finding ID |

### Examples

> "Show me the details of the SQL injection finding"

> "Get the full description and remediation for finding 507f1f77bcf86cd799439041"

### Response

Complete finding object with description, observation, remediation, POC, references, and custom fields.

---

## create_finding

Create a new finding in an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `title` | string | Yes | Finding title |
| `vuln_type` | string | No | Vulnerability type |
| `description` | string | No | Detailed description |
| `observation` | string | No | Observation/evidence |
| `remediation` | string | No | Remediation steps |
| `poc` | string | No | Proof of concept |
| `cvssv3` | string | No | CVSS v3 vector string |
| `severity` | string | No | Severity level |
| `priority` | integer | No | Priority (1-4) |
| `remediation_complexity` | integer | No | Complexity (1-3) |
| `status` | integer | No | Status (0=To Do, 1=Done) |
| `category` | string | No | Category |
| `scope` | string | No | Affected scope/asset |
| `references` | array | No | Reference URLs |

### Examples

> "Create a critical SQL injection finding for the login page in the Acme audit"

> "Add a medium-severity XSS vulnerability to audit X with CVSS 6.1"

### Response

```json
{
  "_id": "507f1f77bcf86cd799439042",
  "title": "SQL Injection in Login Form",
  "severity": "Critical",
  "status": 0
}
```

---

## update_finding

Update an existing finding.

### Parameters

Same as `create_finding`, plus:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `finding_id` | string | Yes | The finding ID to update |

### Examples

> "Update the SQL injection finding to include the new POC"

> "Change the severity of finding X to High"

> "Add OWASP reference to the XSS finding"

---

## delete_finding

Delete a finding from an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `finding_id` | string | Yes | The finding ID to delete |

### Examples

> "Remove the false positive finding from the audit"

⚠️ **Warning**: This action is irreversible.

---

## sort_findings

Reorder findings in an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `finding_order` | array | Yes | Array of finding IDs in desired order |

### Examples

> "Reorder findings to put critical ones first"

---

## move_finding

Move a finding from one audit to another.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | Source audit ID |
| `finding_id` | string | Yes | Finding ID to move |
| `destination_audit_id` | string | Yes | Destination audit ID |

### Examples

> "Move the API authentication finding to the new audit"

---

## search_findings

Search for findings across all audits.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string | No | Search by finding title |
| `severity` | string | No | Filter by severity (Critical, High, Medium, Low) |
| `category` | string | No | Filter by category |
| `status` | string | No | Filter by status |

### Examples

> "Find all SQL injection findings"

> "Search for critical vulnerabilities across all audits"

> "Show me all authentication-related findings"

### Response

```json
[
  {
    "finding": { ... },
    "audit": {
      "_id": "507f1f77bcf86cd799439011",
      "name": "Acme Corp Pentest",
      "client": "Acme Corporation"
    }
  }
]
```

---

## get_all_findings_with_context

Get ALL findings from ALL audits with **comprehensive context and enhanced processing** in a single request.

### What Makes This Tool Special

This is the **most powerful tool** for cross-audit analysis. It automatically:

✅ **Extracts CWE** from customFields (searches for "CWE", "CWE-ID", "CWE ID" labels)
✅ **Extracts OWASP** category from finding categories and customFields
✅ **Strips HTML tags** from descriptions, observations, and remediation
✅ **Builds full team** with creator + collaborators (including roles)
✅ **Includes complete scope URLs** from audit scope
✅ **Provides enhanced audit context** (language, audit type, dates)

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `include_failed` | boolean | No | Include 'Failed' category findings (default: false) |
| `exclude_categories` | array | No | Categories to exclude from results |

### Examples

> "Give me a complete analysis of all vulnerabilities across all pentests"

> "What are the most common CWE classifications this year?"

> "Show me all OWASP Top 10 findings with their teams"

> "Which vulnerabilities are being revalidated across clients?"

### Response

```json
[
  {
    "_id": "finding_id",
    "title": "SQL Injection in Login",
    "category": "OWASP A03:2021 - Injection",
    "severity": "Critical",
    "cvssv3": "9.8",
    "priority": 1,
    "status": "Confirmed",

    "description": "Clean text without HTML tags",
    "observation": "Clean text without HTML tags",
    "remediation": "Clean text without HTML tags",

    "cwe": "CWE-89",
    "owasp": "OWASP A03:2021 - Injection",
    "revalidation": false,
    "references": ["https://..."],
    "customFields": [...],

    "audit": {
      "_id": "audit_id",
      "name": "Acme Corp Pentest Q4 2024",
      "company": "Acme Corporation",
      "client": "security@acme.com",
      "date_start": "2024-10-01",
      "date_end": "2024-10-31",
      "scope": ["https://app.acme.com", "https://api.acme.com"],
      "team": [
        {"username": "alice", "role": "creator"},
        {"username": "bob", "role": "collaborator"},
        {"username": "charlie", "role": "collaborator"}
      ],
      "language": "en",
      "audit_type": "Web Application Pentest"
    }
  }
]
```

### Enhanced Features

**CWE Extraction**
```
Automatically finds CWE from customFields:
- Searches for labels: "CWE", "CWE-ID", "CWE ID"
- Returns the value (e.g., "CWE-89", "CWE-79")
- Returns null if not found
```

**OWASP Extraction**
```
Checks multiple sources:
1. Category field (e.g., "OWASP A03:2021")
2. CustomFields with "owasp" in label
3. Returns first match found
```

**HTML Stripping**
```
Removes all HTML tags and decodes entities from:
- description
- observation
- remediation

Ensures clean text for AI analysis and reporting
```

**Full Team Information**
```
Includes complete team with roles:
- Creator (who initiated the audit)
- Collaborators (all team members)
- Username for each member
```

### Use Cases

- **CWE/OWASP Analysis**: "Show me all CWE-79 findings across clients"
- **Vulnerability trending**: Track common issues over time
- **Client comparisons**: Compare security posture across clients
- **Team metrics**: Analyze findings by team member
- **Compliance reporting**: Generate cross-audit statistics with OWASP mapping
- **Revalidation tracking**: Find all findings marked for revalidation

---

## Usage Patterns

### Creating a Complete Finding

```
1. get_vulnerabilities_by_locale → Find matching template
2. create_finding → Create with template data
3. update_finding → Add specific POC and observations
```

### Cross-Audit Analysis

```
1. get_all_findings_with_context → Get everything
2. Analyze patterns in Claude
3. Generate insights and recommendations
```

### Finding Lifecycle

```
Draft → create_finding (status=0)
Testing → update_finding with observations
Complete → update_finding (status=1)
Report → generate_audit_report
```

---

## Severity Mapping

| Severity | CVSS Score | Priority |
|----------|------------|----------|
| Critical | 9.0 - 10.0 | 1 |
| High | 7.0 - 8.9 | 2 |
| Medium | 4.0 - 6.9 | 3 |
| Low | 0.1 - 3.9 | 4 |
| Info | 0.0 | 5 |

---

## Query Examples

**Find similar vulnerabilities:**
> "Have we seen this type of SQL injection in other pentests?"

**Remediation tracking:**
> "Show me all unremediated critical findings"

**Client-specific:**
> "What vulnerabilities have we found for Acme Corp across all engagements?"

**Statistics:**
> "What percentage of our findings are injection-related?"
