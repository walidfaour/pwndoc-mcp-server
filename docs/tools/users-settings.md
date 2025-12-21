# Users & Settings Tools

Tools for user management and system configuration.

## User Management

### list_users

List all users in the system (admin only).

### Parameters

None.

### Examples

> "Show me all users"

> "List team members"

### Response

```json
[
  {
    "_id": "507f1f77bcf86cd799439001",
    "username": "pentester1",
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "role": "user",
    "enabled": true
  }
]
```

---

### get_user

Get details for a specific user by username.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | string | Yes | The username |

### Examples

> "Show me info about user pentester1"

---

### get_current_user

Get authenticated user's information.

### Parameters

None.

### Examples

> "What's my user profile?"

> "Who am I logged in as?"

---

### create_user

Create a new user (admin only).

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | string | Yes | Username |
| `firstname` | string | Yes | First name |
| `lastname` | string | Yes | Last name |
| `password` | string | Yes | Password |
| `email` | string | No | Email address |
| `phone` | string | No | Phone number |
| `role` | string | No | Role (admin, user, etc.) |

### Examples

> "Create a new user account for Jane Smith"

---

### update_user

Update a user's information (admin only).

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | The user ID |
| `username` | string | No | New username |
| `firstname` | string | No | New first name |
| `lastname` | string | No | New last name |
| `email` | string | No | New email |
| `phone` | string | No | New phone |
| `role` | string | No | New role |
| `enabled` | boolean | No | Enable/disable user |

### Examples

> "Disable user pentester2"

> "Change John's role to admin"

---

### update_current_user

Update your own profile.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `firstname` | string | No | New first name |
| `lastname` | string | No | New last name |
| `email` | string | No | New email |
| `phone` | string | No | New phone |
| `username` | string | No | New username |
| `current_password` | string | No* | Current password (required for password change) |
| `new_password` | string | No | New password |
| `confirm_password` | string | No | Confirm new password |

### Examples

> "Update my email to newemail@example.com"

---

### list_reviewers

List users who can be assigned as reviewers.

### Parameters

None.

### Examples

> "Who can review audits?"

---

## Two-Factor Authentication

### get_totp_status

Get TOTP (2FA) status for current user.

### Parameters

None.

### Examples

> "Is 2FA enabled for my account?"

---

### setup_totp

Set up TOTP (2FA) for current user.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `totp_token` | string | Yes | TOTP token to verify setup |

### Examples

> "Enable 2FA for my account"

---

### disable_totp

Disable TOTP (2FA) for current user.

### Parameters

None.

### Examples

> "Disable 2FA for my account"

---

## System Settings

### get_settings

Get system settings (admin only).

### Parameters

None.

### Examples

> "Show me the system configuration"

---

### get_public_settings

Get publicly accessible settings.

### Parameters

None.

---

### update_settings

Update system settings (admin only).

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `settings` | object | Yes | Settings object to update |

### Examples

> "Update the default report template"

---

### export_settings

Export all settings for backup.

### Parameters

None.

### Examples

> "Export system settings"

---

### revert_settings

Revert settings to defaults.

### Parameters

None.

### Examples

> "Reset settings to defaults"

⚠️ **Warning**: This will overwrite all custom settings.

---

## Configuration Tools

### list_languages

List all configured languages.

### Parameters

None.

---

### list_audit_types

List all audit types.

### Parameters

None.

### Examples

> "What types of audits can I create?"

---

### list_vulnerability_types

List all vulnerability types.

### Parameters

None.

---

### list_vulnerability_categories

List all vulnerability categories.

### Parameters

None.

---

### list_sections

List all section definitions.

### Parameters

None.

---

### list_custom_fields

List all custom field definitions.

### Parameters

None.

---

### list_roles

List all user roles.

### Parameters

None.

### Examples

> "What roles are available?"

---

## Usage Patterns

### Team Management

```
1. list_users → See current team
2. create_user → Add new members
3. update_user → Adjust roles
4. list_reviewers → Assign reviewers
```

### Security Hardening

```
1. get_totp_status → Check 2FA
2. setup_totp → Enable 2FA
3. update_current_user → Strong password
```

### System Administration

```
1. get_settings → Review config
2. update_settings → Apply changes
3. export_settings → Backup
```

---

## Role Permissions

| Role | Create Audit | Edit Findings | Manage Users | System Config |
|------|--------------|---------------|--------------|---------------|
| admin | ✓ | ✓ | ✓ | ✓ |
| user | ✓ | ✓ | ✗ | ✗ |
| reviewer | ✗ | Review only | ✗ | ✗ |
