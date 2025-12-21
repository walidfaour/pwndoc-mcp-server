# Client & Company Tools

Tools for managing clients and companies in PwnDoc.

## Client Tools

### list_clients

List all clients in the system.

### Parameters

None.

### Examples

> "Show me all clients"

> "List our pentest clients"

### Response

```json
[
  {
    "_id": "507f1f77bcf86cd799439021",
    "email": "security@acme.com",
    "firstname": "John",
    "lastname": "Smith",
    "phone": "+1-555-123-4567",
    "title": "CISO",
    "company": {
      "_id": "507f1f77bcf86cd799439031",
      "name": "Acme Corporation"
    }
  }
]
```

---

### create_client

Create a new client contact.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | Yes | Client email address |
| `firstname` | string | Yes | First name |
| `lastname` | string | Yes | Last name |
| `phone` | string | No | Phone number |
| `cell` | string | No | Cell phone number |
| `title` | string | No | Job title |
| `company` | string | No | Company ID to associate |

### Examples

> "Create a new client contact for Jane Doe at Acme Corp"

> "Add security@newclient.com as a client"

---

### update_client

Update an existing client's information.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `client_id` | string | Yes | The client ID to update |
| `email` | string | No | New email address |
| `firstname` | string | No | New first name |
| `lastname` | string | No | New last name |
| `phone` | string | No | New phone number |
| `cell` | string | No | New cell phone |
| `title` | string | No | New job title |
| `company` | string | No | New company ID |

### Examples

> "Update John Smith's title to VP of Security"

> "Change the email for client 507f1f77bcf86cd799439021"

---

### delete_client

Delete a client from the system.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `client_id` | string | Yes | The client ID to delete |

### Examples

> "Remove the old client contact"

⚠️ **Warning**: This may affect audits associated with this client.

---

## Company Tools

### list_companies

List all companies in the system.

### Parameters

None.

### Examples

> "Show me all companies"

> "List organizations we've worked with"

### Response

```json
[
  {
    "_id": "507f1f77bcf86cd799439031",
    "name": "Acme Corporation",
    "shortName": "ACME",
    "logo": ""
  }
]
```

---

### create_company

Create a new company.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Company name |
| `short_name` | string | No | Short name/abbreviation |
| `logo` | string | No | Logo image (base64 encoded) |

### Examples

> "Create a new company called TechStart Inc"

> "Add GlobalBank as a new organization"

---

### update_company

Update company information.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `company_id` | string | Yes | The company ID to update |
| `name` | string | No | New company name |
| `short_name` | string | No | New short name |
| `logo` | string | No | New logo (base64) |

### Examples

> "Update Acme's short name to ACM"

> "Change the company name for 507f1f77bcf86cd799439031"

---

### delete_company

Delete a company from the system.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `company_id` | string | Yes | The company ID to delete |

### Examples

> "Remove the test company"

⚠️ **Warning**: This may affect audits and clients associated with this company.

---

## Usage Patterns

### Setting Up a New Engagement

```
1. list_companies → Check if company exists
2. create_company → Create if needed
3. list_clients → Check for existing contacts
4. create_client → Add new contacts
5. create_audit → Create audit with company/client
```

### Client Management

**Find client information:**
> "What's the contact info for Acme Corp?"

**Update after personnel change:**
> "John Smith left Acme, update the primary contact to Jane Doe"

### Company Organization

**Track all work for a company:**
> "List all audits for Acme Corporation"

**Contact lookup:**
> "Who are our contacts at GlobalBank?"

---

## Best Practices

1. **Consistent naming**: Use full company names, create short names for reports
2. **Complete contact info**: Always include email, phone, and title
3. **Company associations**: Link clients to companies for organization
4. **Regular cleanup**: Remove outdated contacts and test data
