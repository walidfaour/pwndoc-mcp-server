# Reports & Statistics Tools

Tools for generating reports and viewing metrics.

## Report Generation

### generate_audit_report

Generate and download the audit report as DOCX.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audit_id` | string | Yes | The audit ID |

### Examples

> "Generate the report for the Acme Corp audit"

> "Create the pentest report for audit 507f1f77bcf86cd799439011"

### How It Works

1. Tool requests report generation from PwnDoc
2. PwnDoc processes the audit data
3. Applies the configured report template
4. Returns DOCX file content

### Report Contents

Generated reports typically include:
- Executive summary
- Scope and methodology
- Findings (sorted by severity)
- Remediation recommendations
- Technical appendices

---

## Template Management

### list_templates

List all available report templates.

### Parameters

None.

### Examples

> "What report templates are available?"

> "Show me the template options"

### Response

```json
[
  {
    "_id": "507f1f77bcf86cd799439061",
    "name": "Standard Pentest Report",
    "ext": "docx"
  },
  {
    "_id": "507f1f77bcf86cd799439062",
    "name": "Executive Summary Only",
    "ext": "docx"
  }
]
```

---

### download_template

Download a report template file.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `template_id` | string | Yes | The template ID |

### Examples

> "Download the standard pentest template"

---

## Statistics

### get_statistics

Get comprehensive statistics about audits, findings, clients, and more.

### Parameters

None.

### Examples

> "Show me overall statistics"

> "Give me a dashboard overview"

> "What are our pentest metrics?"

### Response

```json
{
  "totalAudits": 81,
  "auditsByStatus": {
    "In Progress": 15,
    "Completed": 60,
    "Draft": 6
  },
  "totalFindings": 423,
  "findingsBySeverity": {
    "Critical": 28,
    "High": 95,
    "Medium": 187,
    "Low": 89,
    "Info": 24
  },
  "totalClients": 12,
  "totalCompanies": 8,
  "totalUsers": 23,
  "recentAudits": [...]
}
```

---

## Analysis Examples

### Severity Distribution

> "What's the breakdown of findings by severity?"

Claude can use `get_statistics` to show:
- Critical: 28 (6.6%)
- High: 95 (22.5%)
- Medium: 187 (44.2%)
- Low: 89 (21.0%)
- Info: 24 (5.7%)

### Audit Progress

> "How many audits are in progress vs completed?"

### Team Productivity

> "How many findings per audit on average?"

Calculate: totalFindings / totalAudits = 423 / 81 = 5.2 findings per audit

---

## Advanced Analysis

For deeper analysis, combine with other tools:

### Trend Analysis

```
1. get_all_findings_with_context → All data
2. Filter by date ranges
3. Compare periods
```

> "How do our Q3 findings compare to Q4?"

### Client Risk Assessment

```
1. list_audits → Filter by client
2. get_audit_findings → For each audit
3. Aggregate by severity
```

> "Which client has the most critical findings?"

### Vulnerability Patterns

```
1. search_findings → By category
2. Group and count
3. Identify trends
```

> "What are the most common vulnerability types?"

---

## Reporting Workflows

### Standard Report Generation

```
1. list_audits → Find completed audit
2. get_audit → Verify completeness
3. list_templates → Choose template
4. update_audit_general → Set template
5. generate_audit_report → Create report
```

### Executive Dashboard

```
1. get_statistics → Overall metrics
2. list_audits → Recent audits
3. search_findings → Critical findings
4. Summarize for executives
```

### Compliance Reporting

```
1. get_all_findings_with_context → All data
2. Filter by date range
3. Group by compliance requirement
4. Generate summary
```

---

## Best Practices

### Before Generating Reports

1. **Verify audit completion**
   - All findings documented
   - Sections written
   - Review completed

2. **Check template**
   - Correct template assigned
   - Template up to date

3. **Validate data**
   - CVSS scores present
   - Remediation provided
   - References included

### Report Quality

- Use consistent severity ratings
- Include actionable remediation
- Provide clear evidence/POC
- Reference industry standards

### Statistics Usage

- Track trends over time
- Benchmark against industry
- Identify training needs
- Measure team performance
