# Audit Management Tools

Tools for managing penetration test audits in PwnDoc.

## list_audits

List all audits, optionally filtered by finding title.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `finding_title` | string | No | Filter audits containing findings with this title |

### Examples

**List all audits:**
> "Show me all audits"

**Filter by finding:**
> "Find audits that have SQL injection findings"

### Response

```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "name": "Acme Corp Web App Pentest Q4",
    "auditType": "Web Application",
    "state": "In Progress",
    "client": {"firstname": "John", "lastname": "Doe"},
    "company": {"name": "Acme Corporation"},
    "date_start": "2024-10-01",
    "date_end": "2024-10-31"
  }
]
```

---

## get_audit

Get complete audit details including all findings, scope, and sections.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID (MongoDB ObjectId) |

### Examples

> "Show me the details of audit 507f1f77bcf86cd799439011"

> "Get the full information for the Acme Corp pentest"

### Response

Complete audit object with findings, sections, collaborators, and all metadata.

---

## get_audit_general

Get general audit information (name, dates, client) without findings.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |

### Examples

> "What are the dates for the Acme audit?"

> "Who is the client for audit 507f1f77bcf86cd799439011?"

---

## create_audit

Create a new audit/pentest.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Audit name |
| `audit_type` | string | Yes | Type of audit (e.g., "Web Application") |
| `language` | string | Yes | Language code (e.g., "en") |

### Examples

> "Create a new web application pentest called 'Mobile Banking Assessment 2024'"

> "Start a new audit for infrastructure testing in English"

### Response

```json
{
  "_id": "507f1f77bcf86cd799439012",
  "name": "Mobile Banking Assessment 2024",
  "auditType": "Web Application",
  "language": "en"
}
```

---

## update_audit_general

Update audit general information.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `name` | string | No | New audit name |
| `client` | string | No | Client ID |
| `company` | string | No | Company ID |
| `date_start` | string | No | Start date (ISO format) |
| `date_end` | string | No | End date (ISO format) |
| `scope` | array | No | Scope items |
| `template` | string | No | Report template ID |
| `location` | string | No | Audit location |

### Examples

> "Update the end date of audit X to December 31st"

> "Add app.example.com to the scope of the current audit"

---

## delete_audit

Permanently delete an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID to delete |

### Examples

> "Delete the test audit 507f1f77bcf86cd799439011"

⚠️ **Warning**: This action is irreversible.

---

## generate_audit_report

Generate and download the audit report as DOCX.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |

### Examples

> "Generate the report for the completed Acme audit"

> "Create the pentest report for audit 507f1f77bcf86cd799439011"

### Response

Binary DOCX file content.

---

## get_audit_network

Get network configuration for an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |

---

## update_audit_network

Update network information for an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `network_data` | object | Yes | Network configuration data |

---

## toggle_audit_approval

Toggle the approval status of an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |

### Examples

> "Approve the Acme Corp audit"

> "Toggle approval for audit 507f1f77bcf86cd799439011"

---

## update_audit_review_status

Set the review ready status of an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `state` | boolean | Yes | Ready for review state |

### Examples

> "Mark the Acme audit as ready for review"

> "Set audit X as not ready for review"

---

## get_audit_section

Get a specific section from an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `section_id` | string | Yes | The section ID |

### Examples

> "Show me the executive summary section of the Acme audit"

---

## update_audit_section

Update a section's content in an audit.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |
| `section_id` | string | Yes | The section ID |
| `text` | string | Yes | New section content |

### Examples

> "Update the executive summary to include a note about critical findings"

> "Add methodology details to the approach section"

---

## Usage Patterns

### Complete Audit Workflow

```
1. create_audit → Create new audit
2. update_audit_general → Set client, dates, scope
3. [Add findings via finding tools]
4. update_audit_section → Write narrative sections
5. update_audit_review_status → Mark ready for review
6. toggle_audit_approval → Approve after review
7. generate_audit_report → Generate final report
```

### Query Examples

**Get audit overview:**
> "Give me a summary of the Acme Corp pentest including client, dates, and finding count"

**Track progress:**
> "What audits are currently in progress?"

**Upcoming deadlines:**
> "Show me audits ending this month"
