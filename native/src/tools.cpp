#include "tools.hpp"
#include <stdexcept>

using json = nlohmann::json;

json get_tool_definitions() {
    return json::array({
        // =====================================================================
        // AUDIT TOOLS (13 tools)
        // =====================================================================
        {
            {"name", "list_audits"},
            {"description", "List all audits/pentests. Can filter by finding title."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"finding_title", {
                        {"type", "string"},
                        {"description", "Filter audits containing findings with this title (optional)"}
                    }}
                }}
            }}
        },
        {
            {"name", "get_audit"},
            {"description", "Get detailed information about a specific audit including all findings, scope, sections, and metadata."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID (MongoDB ObjectId)"}}}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "create_audit"},
            {"description", "Create a new audit/pentest."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"name", {{"type", "string"}, {"description", "Audit name"}}},
                    {"language", {{"type", "string"}, {"description", "Language code (e.g., 'en')"}}},
                    {"audit_type", {{"type", "string"}, {"description", "Type of audit"}}}
                }},
                {"required", json::array({"name", "language", "audit_type"})}
            }}
        },
        {
            {"name", "update_audit_general"},
            {"description", "Update general information of an audit."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"name", {{"type", "string"}, {"description", "Audit name"}}},
                    {"client", {{"type", "string"}, {"description", "Client ID"}}},
                    {"company", {{"type", "string"}, {"description", "Company ID"}}},
                    {"date_start", {{"type", "string"}, {"description", "Start date (ISO format)"}}},
                    {"date_end", {{"type", "string"}, {"description", "End date (ISO format)"}}},
                    {"scope", {
                        {"type", "array"},
                        {"items", {{"type", "string"}}},
                        {"description", "Scope items"}
                    }}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "delete_audit"},
            {"description", "Delete an audit permanently."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID to delete"}}}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "generate_audit_report"},
            {"description", "Generate and download the audit report (DOCX)."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "get_audit_general"},
            {"description", "Get audit general information (dates, client, company, scope)."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "get_audit_network"},
            {"description", "Get audit network information."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "update_audit_network"},
            {"description", "Update audit network information."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"network_data", {{"type", "object"}, {"description", "Network configuration data"}}}
                }},
                {"required", json::array({"audit_id", "network_data"})}
            }}
        },
        {
            {"name", "toggle_audit_approval"},
            {"description", "Toggle audit approval status."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "update_review_status"},
            {"description", "Update audit ready-for-review status."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"state", {{"type", "boolean"}, {"description", "Ready for review state"}}}
                }},
                {"required", json::array({"audit_id", "state"})}
            }}
        },
        {
            {"name", "get_audit_sections"},
            {"description", "Get audit sections content."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "update_audit_sections"},
            {"description", "Update audit sections content."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"sections", {{"type", "object"}, {"description", "Sections data to update"}}}
                }},
                {"required", json::array({"audit_id", "sections"})}
            }}
        },

        // =====================================================================
        // FINDING TOOLS (9 tools)
        // =====================================================================
        {
            {"name", "get_audit_findings"},
            {"description", "Get all findings/vulnerabilities from a specific audit."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}}
                }},
                {"required", json::array({"audit_id"})}
            }}
        },
        {
            {"name", "get_finding"},
            {"description", "Get details of a specific finding in an audit."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"finding_id", {{"type", "string"}, {"description", "The finding ID"}}}
                }},
                {"required", json::array({"audit_id", "finding_id"})}
            }}
        },
        {
            {"name", "create_finding"},
            {"description", "Create a new finding in an audit."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"title", {{"type", "string"}, {"description", "Finding title"}}},
                    {"description", {{"type", "string"}, {"description", "Detailed description"}}},
                    {"observation", {{"type", "string"}, {"description", "Observation/evidence"}}},
                    {"remediation", {{"type", "string"}, {"description", "Remediation steps"}}},
                    {"cvssv3", {{"type", "string"}, {"description", "CVSS v3 score/vector"}}},
                    {"priority", {{"type", "integer"}, {"description", "Priority (1-4)"}}},
                    {"category", {{"type", "string"}, {"description", "Category"}}},
                    {"vuln_type", {{"type", "string"}, {"description", "Vulnerability type"}}},
                    {"poc", {{"type", "string"}, {"description", "Proof of concept"}}},
                    {"scope", {{"type", "string"}, {"description", "Affected scope"}}},
                    {"references", {
                        {"type", "array"},
                        {"items", {{"type", "string"}}},
                        {"description", "References"}
                    }}
                }},
                {"required", json::array({"audit_id", "title"})}
            }}
        },
        {
            {"name", "update_finding"},
            {"description", "Update an existing finding."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"finding_id", {{"type", "string"}, {"description", "The finding ID"}}},
                    {"title", {{"type", "string"}}},
                    {"description", {{"type", "string"}}},
                    {"observation", {{"type", "string"}}},
                    {"remediation", {{"type", "string"}}},
                    {"cvssv3", {{"type", "string"}}},
                    {"priority", {{"type", "integer"}}},
                    {"category", {{"type", "string"}}},
                    {"vuln_type", {{"type", "string"}}},
                    {"poc", {{"type", "string"}}},
                    {"scope", {{"type", "string"}}},
                    {"references", {{"type", "array"}, {"items", {{"type", "string"}}}}}
                }},
                {"required", json::array({"audit_id", "finding_id"})}
            }}
        },
        {
            {"name", "delete_finding"},
            {"description", "Delete a finding from an audit."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"finding_id", {{"type", "string"}, {"description", "The finding ID to delete"}}}
                }},
                {"required", json::array({"audit_id", "finding_id"})}
            }}
        },
        {
            {"name", "search_findings"},
            {"description", "Search for findings across all audits by various criteria."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"title", {{"type", "string"}, {"description", "Search by finding title"}}},
                    {"category", {{"type", "string"}, {"description", "Filter by category"}}},
                    {"severity", {{"type", "string"}, {"description", "Filter by severity (Critical, High, Medium, Low)"}}},
                    {"status", {{"type", "string"}, {"description", "Filter by status"}}}
                }}
            }}
        },
        {
            {"name", "get_all_findings_with_context"},
            {"description", "Get ALL findings from ALL audits with full context (company, dates, team, scope, description, CWE, references) in a single request."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"include_failed", {
                        {"type", "boolean"},
                        {"description", "Include 'Failed' category findings (default: false)"}
                    }},
                    {"exclude_categories", {
                        {"type", "array"},
                        {"items", {{"type", "string"}}},
                        {"description", "Categories to exclude"}
                    }}
                }}
            }}
        },
        {
            {"name", "sort_findings"},
            {"description", "Reorder findings within an audit."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "The audit ID"}}},
                    {"finding_order", {
                        {"type", "array"},
                        {"items", {{"type", "string"}}},
                        {"description", "Ordered array of finding IDs"}
                    }}
                }},
                {"required", json::array({"audit_id", "finding_order"})}
            }}
        },
        {
            {"name", "move_finding"},
            {"description", "Move a finding from one audit to another."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "Source audit ID"}}},
                    {"finding_id", {{"type", "string"}, {"description", "Finding ID to move"}}},
                    {"destination_audit_id", {{"type", "string"}, {"description", "Destination audit ID"}}}
                }},
                {"required", json::array({"audit_id", "finding_id", "destination_audit_id"})}
            }}
        },

        // =====================================================================
        // CLIENT & COMPANY TOOLS (8 tools)
        // =====================================================================
        {
            {"name", "list_clients"},
            {"description", "List all clients."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_client"},
            {"description", "Create a new client."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"firstname", {{"type", "string"}, {"description", "First name"}}},
                    {"lastname", {{"type", "string"}, {"description", "Last name"}}},
                    {"email", {{"type", "string"}, {"description", "Client email"}}},
                    {"phone", {{"type", "string"}, {"description", "Phone number"}}},
                    {"cell", {{"type", "string"}, {"description", "Cell phone"}}},
                    {"title", {{"type", "string"}, {"description", "Job title"}}},
                    {"company", {{"type", "string"}, {"description", "Company ID"}}}
                }},
                {"required", json::array({"email", "firstname", "lastname"})}
            }}
        },
        {
            {"name", "update_client"},
            {"description", "Update an existing client."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"client_id", {{"type", "string"}, {"description", "Client ID"}}},
                    {"firstname", {{"type", "string"}, {"description", "First name"}}},
                    {"lastname", {{"type", "string"}, {"description", "Last name"}}},
                    {"email", {{"type", "string"}, {"description", "Client email"}}},
                    {"phone", {{"type", "string"}, {"description", "Phone number"}}},
                    {"cell", {{"type", "string"}, {"description", "Cell phone"}}},
                    {"title", {{"type", "string"}, {"description", "Job title"}}},
                    {"company", {{"type", "string"}, {"description", "Company ID"}}}
                }},
                {"required", json::array({"client_id"})}
            }}
        },
        {
            {"name", "delete_client"},
            {"description", "Delete a client."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"client_id", {{"type", "string"}, {"description", "Client ID to delete"}}}
                }},
                {"required", json::array({"client_id"})}
            }}
        },
        {
            {"name", "list_companies"},
            {"description", "List all companies."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_company"},
            {"description", "Create a new company."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"name", {{"type", "string"}, {"description", "Company name"}}},
                    {"short_name", {{"type", "string"}, {"description", "Short name/abbreviation"}}},
                    {"logo", {{"type", "string"}, {"description", "Logo (base64)"}}}
                }},
                {"required", json::array({"name"})}
            }}
        },
        {
            {"name", "update_company"},
            {"description", "Update an existing company."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"company_id", {{"type", "string"}, {"description", "Company ID"}}},
                    {"name", {{"type", "string"}, {"description", "Company name"}}},
                    {"short_name", {{"type", "string"}, {"description", "Short name/abbreviation"}}},
                    {"logo", {{"type", "string"}, {"description", "Logo (base64)"}}}
                }},
                {"required", json::array({"company_id"})}
            }}
        },
        {
            {"name", "delete_company"},
            {"description", "Delete a company."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"company_id", {{"type", "string"}, {"description", "Company ID to delete"}}}
                }},
                {"required", json::array({"company_id"})}
            }}
        },

        // =====================================================================
        // VULNERABILITY TEMPLATE TOOLS (10 tools)
        // =====================================================================
        {
            {"name", "list_vulnerabilities"},
            {"description", "List all vulnerability templates in the library."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "get_vulnerabilities_by_locale"},
            {"description", "Get vulnerability templates for a specific language."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"locale", {
                        {"type", "string"},
                        {"description", "Language code (e.g., 'en', 'fr')"},
                        {"default", "en"}
                    }}
                }}
            }}
        },
        {
            {"name", "create_vulnerability"},
            {"description", "Create a new vulnerability template."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"details", {{"type", "object"}, {"description", "Vulnerability details by locale"}}},
                    {"cvssv3", {{"type", "string"}, {"description", "CVSS v3 score"}}},
                    {"priority", {{"type", "integer"}, {"description", "Priority (1-4)"}}},
                    {"remediation_complexity", {{"type", "integer"}, {"description", "Complexity (1-3)"}}},
                    {"category", {{"type", "string"}, {"description", "Category"}}}
                }},
                {"required", json::array({"details"})}
            }}
        },
        {
            {"name", "update_vulnerability"},
            {"description", "Update an existing vulnerability template."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"vuln_id", {{"type", "string"}, {"description", "Vulnerability template ID"}}},
                    {"details", {{"type", "object"}, {"description", "Vulnerability details by locale"}}},
                    {"cvssv3", {{"type", "string"}, {"description", "CVSS v3 score"}}},
                    {"priority", {{"type", "integer"}, {"description", "Priority (1-4)"}}},
                    {"remediation_complexity", {{"type", "integer"}, {"description", "Complexity (1-3)"}}},
                    {"category", {{"type", "string"}, {"description", "Category"}}}
                }},
                {"required", json::array({"vuln_id"})}
            }}
        },
        {
            {"name", "delete_vulnerability"},
            {"description", "Delete a vulnerability template."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"vuln_id", {{"type", "string"}, {"description", "Vulnerability template ID to delete"}}}
                }},
                {"required", json::array({"vuln_id"})}
            }}
        },
        {
            {"name", "bulk_delete_vulnerabilities"},
            {"description", "Delete multiple vulnerability templates at once."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"vuln_ids", {
                        {"type", "array"},
                        {"items", {{"type", "string"}}},
                        {"description", "Array of vulnerability template IDs to delete"}
                    }}
                }},
                {"required", json::array({"vuln_ids"})}
            }}
        },
        {
            {"name", "export_vulnerabilities"},
            {"description", "Export all vulnerability templates."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_vulnerability_from_finding"},
            {"description", "Create a vulnerability template from an existing finding."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "Audit ID"}}},
                    {"finding_id", {{"type", "string"}, {"description", "Finding ID"}}},
                    {"locale", {{"type", "string"}, {"description", "Language code (e.g., 'en')"}}}
                }},
                {"required", json::array({"audit_id", "finding_id"})}
            }}
        },
        {
            {"name", "get_vulnerability_updates"},
            {"description", "Get available vulnerability template updates."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "merge_vulnerability"},
            {"description", "Merge vulnerability template with an update."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"vuln_id", {{"type", "string"}, {"description", "Vulnerability template ID"}}},
                    {"update_id", {{"type", "string"}, {"description", "Update ID to merge"}}}
                }},
                {"required", json::array({"vuln_id", "update_id"})}
            }}
        },

        // =====================================================================
        // USER TOOLS (10 tools)
        // =====================================================================
        {
            {"name", "list_users"},
            {"description", "List all users (admin only)."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "get_current_user"},
            {"description", "Get current authenticated user's info."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "get_user"},
            {"description", "Get user information by username."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"username", {{"type", "string"}, {"description", "Username"}}}
                }},
                {"required", json::array({"username"})}
            }}
        },
        {
            {"name", "create_user"},
            {"description", "Create a new user (admin only)."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"username", {{"type", "string"}, {"description", "Username"}}},
                    {"password", {{"type", "string"}, {"description", "Password"}}},
                    {"firstname", {{"type", "string"}, {"description", "First name"}}},
                    {"lastname", {{"type", "string"}, {"description", "Last name"}}},
                    {"email", {{"type", "string"}, {"description", "Email address"}}},
                    {"role", {{"type", "string"}, {"description", "User role"}}}
                }},
                {"required", json::array({"username", "password", "firstname", "lastname", "email", "role"})}
            }}
        },
        {
            {"name", "update_user"},
            {"description", "Update a user (admin only)."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"user_id", {{"type", "string"}, {"description", "User ID"}}},
                    {"username", {{"type", "string"}, {"description", "Username"}}},
                    {"firstname", {{"type", "string"}, {"description", "First name"}}},
                    {"lastname", {{"type", "string"}, {"description", "Last name"}}},
                    {"email", {{"type", "string"}, {"description", "Email address"}}},
                    {"role", {{"type", "string"}, {"description", "User role"}}}
                }},
                {"required", json::array({"user_id"})}
            }}
        },
        {
            {"name", "update_current_user"},
            {"description", "Update current user's profile."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"firstname", {{"type", "string"}, {"description", "First name"}}},
                    {"lastname", {{"type", "string"}, {"description", "Last name"}}},
                    {"email", {{"type", "string"}, {"description", "Email address"}}},
                    {"password", {{"type", "string"}, {"description", "New password"}}}
                }}
            }}
        },
        {
            {"name", "list_reviewers"},
            {"description", "List all users with reviewer role."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "get_totp_status"},
            {"description", "Get TOTP (2FA) status for current user."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "setup_totp"},
            {"description", "Setup TOTP (2FA) for current user."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "disable_totp"},
            {"description", "Disable TOTP (2FA) for current user."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"token", {{"type", "string"}, {"description", "TOTP token for verification"}}}
                }},
                {"required", json::array({"token"})}
            }}
        },

        // =====================================================================
        // SETTINGS & TEMPLATE TOOLS (10 tools)
        // =====================================================================
        {
            {"name", "list_templates"},
            {"description", "List all report templates."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_template"},
            {"description", "Create/upload a report template."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"name", {{"type", "string"}, {"description", "Template name"}}},
                    {"ext", {{"type", "string"}, {"description", "File extension (e.g., 'docx')"}}},
                    {"file_content", {{"type", "string"}, {"description", "Base64-encoded file content"}}}
                }},
                {"required", json::array({"name", "ext", "file_content"})}
            }}
        },
        {
            {"name", "update_template"},
            {"description", "Update an existing template."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"template_id", {{"type", "string"}, {"description", "Template ID"}}},
                    {"name", {{"type", "string"}, {"description", "Template name"}}},
                    {"ext", {{"type", "string"}, {"description", "File extension"}}},
                    {"file_content", {{"type", "string"}, {"description", "Base64-encoded file content"}}}
                }},
                {"required", json::array({"template_id"})}
            }}
        },
        {
            {"name", "delete_template"},
            {"description", "Delete a report template."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"template_id", {{"type", "string"}, {"description", "Template ID to delete"}}}
                }},
                {"required", json::array({"template_id"})}
            }}
        },
        {
            {"name", "download_template"},
            {"description", "Download a template file."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"template_id", {{"type", "string"}, {"description", "Template ID to download"}}}
                }},
                {"required", json::array({"template_id"})}
            }}
        },
        {
            {"name", "get_settings"},
            {"description", "Get system settings."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "get_public_settings"},
            {"description", "Get public settings (no authentication required)."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "update_settings"},
            {"description", "Update system settings (admin only)."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"settings", {{"type", "object"}, {"description", "Settings to update"}}}
                }},
                {"required", json::array({"settings"})}
            }}
        },
        {
            {"name", "export_settings"},
            {"description", "Export all system settings."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "import_settings"},
            {"description", "Import/revert system settings from export."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"settings", {{"type", "object"}, {"description", "Settings to import"}}}
                }},
                {"required", json::array({"settings"})}
            }}
        },

        // =====================================================================
        // LANGUAGE TOOLS (4 tools)
        // =====================================================================
        {
            {"name", "list_languages"},
            {"description", "List all configured languages."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_language"},
            {"description", "Create a new language."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"language", {{"type", "string"}, {"description", "Language code (e.g., 'en')"}}},
                    {"name", {{"type", "string"}, {"description", "Language name"}}}
                }},
                {"required", json::array({"language", "name"})}
            }}
        },
        {
            {"name", "update_language"},
            {"description", "Update a language."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"language_id", {{"type", "string"}, {"description", "Language ID"}}},
                    {"language", {{"type", "string"}, {"description", "Language code"}}},
                    {"name", {{"type", "string"}, {"description", "Language name"}}}
                }},
                {"required", json::array({"language_id"})}
            }}
        },
        {
            {"name", "delete_language"},
            {"description", "Delete a language."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"language_id", {{"type", "string"}, {"description", "Language ID to delete"}}}
                }},
                {"required", json::array({"language_id"})}
            }}
        },

        // =====================================================================
        // AUDIT TYPE TOOLS (4 tools)
        // =====================================================================
        {
            {"name", "list_audit_types"},
            {"description", "List all audit types."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_audit_type"},
            {"description", "Create a new audit type."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"name", {{"type", "string"}, {"description", "Audit type name"}}},
                    {"templates", {
                        {"type", "array"},
                        {"items", {{"type", "string"}}},
                        {"description", "Template IDs"}
                    }}
                }},
                {"required", json::array({"name"})}
            }}
        },
        {
            {"name", "update_audit_type"},
            {"description", "Update an audit type."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_type_id", {{"type", "string"}, {"description", "Audit type ID"}}},
                    {"name", {{"type", "string"}, {"description", "Audit type name"}}},
                    {"templates", {{"type", "array"}, {"items", {{"type", "string"}}}}}
                }},
                {"required", json::array({"audit_type_id"})}
            }}
        },
        {
            {"name", "delete_audit_type"},
            {"description", "Delete an audit type."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_type_id", {{"type", "string"}, {"description", "Audit type ID to delete"}}}
                }},
                {"required", json::array({"audit_type_id"})}
            }}
        },

        // =====================================================================
        // VULNERABILITY TYPE TOOLS (4 tools)
        // =====================================================================
        {
            {"name", "list_vulnerability_types"},
            {"description", "List all vulnerability types."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_vulnerability_type"},
            {"description", "Create a new vulnerability type."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"name", {{"type", "string"}, {"description", "Vulnerability type name"}}}
                }},
                {"required", json::array({"name"})}
            }}
        },
        {
            {"name", "update_vulnerability_type"},
            {"description", "Update a vulnerability type."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"vuln_type_id", {{"type", "string"}, {"description", "Vulnerability type ID"}}},
                    {"name", {{"type", "string"}, {"description", "Vulnerability type name"}}}
                }},
                {"required", json::array({"vuln_type_id"})}
            }}
        },
        {
            {"name", "delete_vulnerability_type"},
            {"description", "Delete a vulnerability type."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"vuln_type_id", {{"type", "string"}, {"description", "Vulnerability type ID to delete"}}}
                }},
                {"required", json::array({"vuln_type_id"})}
            }}
        },

        // =====================================================================
        // VULNERABILITY CATEGORY TOOLS (4 tools)
        // =====================================================================
        {
            {"name", "list_vulnerability_categories"},
            {"description", "List all vulnerability categories."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_vulnerability_category"},
            {"description", "Create a new vulnerability category."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"name", {{"type", "string"}, {"description", "Category name"}}}
                }},
                {"required", json::array({"name"})}
            }}
        },
        {
            {"name", "update_vulnerability_category"},
            {"description", "Update a vulnerability category."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"category_id", {{"type", "string"}, {"description", "Category ID"}}},
                    {"name", {{"type", "string"}, {"description", "Category name"}}}
                }},
                {"required", json::array({"category_id"})}
            }}
        },
        {
            {"name", "delete_vulnerability_category"},
            {"description", "Delete a vulnerability category."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"category_id", {{"type", "string"}, {"description", "Category ID to delete"}}}
                }},
                {"required", json::array({"category_id"})}
            }}
        },

        // =====================================================================
        // SECTION TOOLS (4 tools)
        // =====================================================================
        {
            {"name", "list_sections"},
            {"description", "List all section definitions."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_section"},
            {"description", "Create a new section definition."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"field", {{"type", "string"}, {"description", "Section field name"}}},
                    {"name", {{"type", "string"}, {"description", "Section display name"}}}
                }},
                {"required", json::array({"field", "name"})}
            }}
        },
        {
            {"name", "update_section"},
            {"description", "Update a section definition."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"section_id", {{"type", "string"}, {"description", "Section ID"}}},
                    {"field", {{"type", "string"}, {"description", "Section field name"}}},
                    {"name", {{"type", "string"}, {"description", "Section display name"}}}
                }},
                {"required", json::array({"section_id"})}
            }}
        },
        {
            {"name", "delete_section"},
            {"description", "Delete a section definition."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"section_id", {{"type", "string"}, {"description", "Section ID to delete"}}}
                }},
                {"required", json::array({"section_id"})}
            }}
        },

        // =====================================================================
        // CUSTOM FIELD TOOLS (4 tools)
        // =====================================================================
        {
            {"name", "list_custom_fields"},
            {"description", "List all custom field definitions."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },
        {
            {"name", "create_custom_field"},
            {"description", "Create a new custom field definition."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"label", {{"type", "string"}, {"description", "Field label"}}},
                    {"field_type", {{"type", "string"}, {"description", "Field type (text, select, etc.)"}}}
                }},
                {"required", json::array({"label", "field_type"})}
            }}
        },
        {
            {"name", "update_custom_field"},
            {"description", "Update a custom field definition."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"field_id", {{"type", "string"}, {"description", "Custom field ID"}}},
                    {"label", {{"type", "string"}, {"description", "Field label"}}},
                    {"field_type", {{"type", "string"}, {"description", "Field type"}}}
                }},
                {"required", json::array({"field_id"})}
            }}
        },
        {
            {"name", "delete_custom_field"},
            {"description", "Delete a custom field definition."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"field_id", {{"type", "string"}, {"description", "Custom field ID to delete"}}}
                }},
                {"required", json::array({"field_id"})}
            }}
        },

        // =====================================================================
        // ROLE TOOLS (1 tool)
        // =====================================================================
        {
            {"name", "list_roles"},
            {"description", "List all user roles."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        },

        // =====================================================================
        // IMAGE TOOLS (4 tools)
        // =====================================================================
        {
            {"name", "get_image"},
            {"description", "Get image metadata."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"image_id", {{"type", "string"}, {"description", "Image ID"}}}
                }},
                {"required", json::array({"image_id"})}
            }}
        },
        {
            {"name", "download_image"},
            {"description", "Download an image file."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"image_id", {{"type", "string"}, {"description", "Image ID to download"}}}
                }},
                {"required", json::array({"image_id"})}
            }}
        },
        {
            {"name", "upload_image"},
            {"description", "Upload an image to an audit."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"audit_id", {{"type", "string"}, {"description", "Audit ID"}}},
                    {"name", {{"type", "string"}, {"description", "Image name"}}},
                    {"value", {{"type", "string"}, {"description", "Base64-encoded image data"}}}
                }},
                {"required", json::array({"audit_id", "name", "value"})}
            }}
        },
        {
            {"name", "delete_image"},
            {"description", "Delete an image."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", {
                    {"image_id", {{"type", "string"}, {"description", "Image ID to delete"}}}
                }},
                {"required", json::array({"image_id"})}
            }}
        },

        // =====================================================================
        // STATISTICS (1 tool)
        // =====================================================================
        {
            {"name", "get_statistics"},
            {"description", "Get comprehensive statistics about audits, findings, clients, and more."},
            {"inputSchema", {
                {"type", "object"},
                {"properties", json::object()}
            }}
        }
    });
}

json execute_tool(PwnDocClient& client, const std::string& name, const json& args) {
    // =========================================================================
    // AUDIT TOOLS
    // =========================================================================
    if (name == "list_audits") {
        return client.get("/api/audits");
    }
    if (name == "get_audit") {
        return client.get("/api/audits/" + args["audit_id"].get<std::string>());
    }
    if (name == "create_audit") {
        json data = {
            {"name", args["name"]},
            {"language", args["language"]},
            {"auditType", args["audit_type"]}
        };
        return client.post("/api/audits", data);
    }
    if (name == "update_audit_general") {
        std::string audit_id = args["audit_id"].get<std::string>();
        json data = args;
        data.erase("audit_id");
        return client.put("/api/audits/" + audit_id + "/general", data);
    }
    if (name == "delete_audit") {
        client.del("/api/audits/" + args["audit_id"].get<std::string>());
        return {{"success", true}, {"message", "Audit deleted"}};
    }
    if (name == "generate_audit_report") {
        return client.get("/api/audits/" + args["audit_id"].get<std::string>() + "/generate");
    }
    if (name == "get_audit_general") {
        return client.get("/api/audits/" + args["audit_id"].get<std::string>() + "/general");
    }
    if (name == "get_audit_network") {
        return client.get("/api/audits/" + args["audit_id"].get<std::string>() + "/network");
    }
    if (name == "update_audit_network") {
        return client.put("/api/audits/" + args["audit_id"].get<std::string>() + "/network", args["network_data"]);
    }
    if (name == "toggle_audit_approval") {
        return client.put("/api/audits/" + args["audit_id"].get<std::string>() + "/toggleApproval", json::object());
    }
    if (name == "update_review_status") {
        return client.put("/api/audits/" + args["audit_id"].get<std::string>() + "/updateReadyForReview", {{"state", args["state"]}});
    }
    if (name == "get_audit_sections") {
        return client.get("/api/audits/" + args["audit_id"].get<std::string>() + "/sections");
    }
    if (name == "update_audit_sections") {
        return client.put("/api/audits/" + args["audit_id"].get<std::string>() + "/sections", args["sections"]);
    }

    // =========================================================================
    // FINDING TOOLS
    // =========================================================================
    if (name == "get_audit_findings") {
        return client.get("/api/audits/" + args["audit_id"].get<std::string>() + "/findings");
    }
    if (name == "get_finding") {
        return client.get("/api/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>());
    }
    if (name == "create_finding") {
        std::string audit_id = args["audit_id"].get<std::string>();
        json data = args;
        data.erase("audit_id");
        return client.post("/api/audits/" + audit_id + "/findings", data);
    }
    if (name == "update_finding") {
        std::string audit_id = args["audit_id"].get<std::string>();
        std::string finding_id = args["finding_id"].get<std::string>();
        json data = args;
        data.erase("audit_id");
        data.erase("finding_id");
        return client.put("/api/audits/" + audit_id + "/findings/" + finding_id, data);
    }
    if (name == "delete_finding") {
        client.del("/api/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>());
        return {{"success", true}, {"message", "Finding deleted"}};
    }
    if (name == "search_findings") {
        // Note: Implemented in Python client as client-side aggregation
        // For now, return basic implementation
        return {{"error", "search_findings not yet implemented in C++ - use Python version"}};
    }
    if (name == "get_all_findings_with_context") {
        // Note: This is a complex aggregation function in Python
        // For now, return placeholder - will be implemented later
        return {{"error", "get_all_findings_with_context not yet implemented in C++ - use Python version"}};
    }
    if (name == "sort_findings") {
        return client.put("/api/audits/" + args["audit_id"].get<std::string>() + "/sortFindings", {{"findings", args["finding_order"]}});
    }
    if (name == "move_finding") {
        return client.post("/api/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>() + "/move/" + args["destination_audit_id"].get<std::string>(), json::object());
    }

    // =========================================================================
    // CLIENT & COMPANY TOOLS
    // =========================================================================
    if (name == "list_clients") {
        return client.get("/api/clients");
    }
    if (name == "create_client") {
        return client.post("/api/clients", args);
    }
    if (name == "update_client") {
        std::string client_id = args["client_id"].get<std::string>();
        json data = args;
        data.erase("client_id");
        return client.put("/api/clients/" + client_id, data);
    }
    if (name == "delete_client") {
        client.del("/api/clients/" + args["client_id"].get<std::string>());
        return {{"success", true}, {"message", "Client deleted"}};
    }
    if (name == "list_companies") {
        return client.get("/api/companies");
    }
    if (name == "create_company") {
        return client.post("/api/companies", args);
    }
    if (name == "update_company") {
        std::string company_id = args["company_id"].get<std::string>();
        json data = args;
        data.erase("company_id");
        return client.put("/api/companies/" + company_id, data);
    }
    if (name == "delete_company") {
        client.del("/api/companies/" + args["company_id"].get<std::string>());
        return {{"success", true}, {"message", "Company deleted"}};
    }

    // =========================================================================
    // VULNERABILITY TEMPLATE TOOLS
    // =========================================================================
    if (name == "list_vulnerabilities") {
        return client.get("/api/vulnerabilities");
    }
    if (name == "get_vulnerabilities_by_locale") {
        std::string locale = args.value("locale", "en");
        return client.get("/api/vulnerabilities/" + locale);
    }
    if (name == "create_vulnerability") {
        return client.post("/api/vulnerabilities", args);
    }
    if (name == "update_vulnerability") {
        std::string vuln_id = args["vuln_id"].get<std::string>();
        json data = args;
        data.erase("vuln_id");
        return client.put("/api/vulnerabilities/" + vuln_id, data);
    }
    if (name == "delete_vulnerability") {
        client.del("/api/vulnerabilities/" + args["vuln_id"].get<std::string>());
        return {{"success", true}, {"message", "Vulnerability deleted"}};
    }
    if (name == "bulk_delete_vulnerabilities") {
        return client.del("/api/vulnerabilities", {{"vulnIds", args["vuln_ids"]}});
    }
    if (name == "export_vulnerabilities") {
        return client.get("/api/vulnerabilities/export");
    }
    if (name == "create_vulnerability_from_finding") {
        return client.post("/api/vulnerabilities/from-finding", args);
    }
    if (name == "get_vulnerability_updates") {
        return client.get("/api/vulnerabilities/updates");
    }
    if (name == "merge_vulnerability") {
        return client.post("/api/vulnerabilities/" + args["vuln_id"].get<std::string>() + "/merge/" + args["update_id"].get<std::string>(), json::object());
    }

    // =========================================================================
    // USER TOOLS
    // =========================================================================
    if (name == "list_users") {
        return client.get("/api/users");
    }
    if (name == "get_current_user") {
        return client.get("/api/users/me");
    }
    if (name == "get_user") {
        return client.get("/api/users/" + args["username"].get<std::string>());
    }
    if (name == "create_user") {
        return client.post("/api/users", args);
    }
    if (name == "update_user") {
        std::string user_id = args["user_id"].get<std::string>();
        json data = args;
        data.erase("user_id");
        return client.put("/api/users/" + user_id, data);
    }
    if (name == "update_current_user") {
        return client.put("/api/users/me", args);
    }
    if (name == "list_reviewers") {
        return client.get("/api/users/reviewers");
    }
    if (name == "get_totp_status") {
        return client.get("/api/users/totp");
    }
    if (name == "setup_totp") {
        return client.post("/api/users/totp", json::object());
    }
    if (name == "disable_totp") {
        return client.del("/api/users/totp", {{"token", args["token"]}});
    }

    // =========================================================================
    // SETTINGS & TEMPLATE TOOLS
    // =========================================================================
    if (name == "list_templates") {
        return client.get("/api/templates");
    }
    if (name == "create_template") {
        json data = {
            {"name", args["name"]},
            {"ext", args["ext"]},
            {"file", args["file_content"]}
        };
        return client.post("/api/templates", data);
    }
    if (name == "update_template") {
        std::string template_id = args["template_id"].get<std::string>();
        json data = args;
        data.erase("template_id");
        if (data.contains("file_content")) {
            data["file"] = data["file_content"];
            data.erase("file_content");
        }
        return client.put("/api/templates/" + template_id, data);
    }
    if (name == "delete_template") {
        client.del("/api/templates/" + args["template_id"].get<std::string>());
        return {{"success", true}, {"message", "Template deleted"}};
    }
    if (name == "download_template") {
        return client.get("/api/templates/download/" + args["template_id"].get<std::string>());
    }
    if (name == "get_settings") {
        return client.get("/api/settings");
    }
    if (name == "get_public_settings") {
        return client.get("/api/settings/public");
    }
    if (name == "update_settings") {
        return client.put("/api/settings", args["settings"]);
    }
    if (name == "export_settings") {
        return client.get("/api/settings/export");
    }
    if (name == "import_settings") {
        return client.post("/api/settings/import", args["settings"]);
    }

    // =========================================================================
    // LANGUAGE TOOLS
    // =========================================================================
    if (name == "list_languages") {
        return client.get("/api/data/languages");
    }
    if (name == "create_language") {
        return client.post("/api/data/languages", args);
    }
    if (name == "update_language") {
        std::string language_id = args["language_id"].get<std::string>();
        json data = args;
        data.erase("language_id");
        return client.put("/api/data/languages/" + language_id, data);
    }
    if (name == "delete_language") {
        client.del("/api/data/languages/" + args["language_id"].get<std::string>());
        return {{"success", true}, {"message", "Language deleted"}};
    }

    // =========================================================================
    // AUDIT TYPE TOOLS
    // =========================================================================
    if (name == "list_audit_types") {
        return client.get("/api/data/audit-types");
    }
    if (name == "create_audit_type") {
        return client.post("/api/data/audit-types", args);
    }
    if (name == "update_audit_type") {
        std::string audit_type_id = args["audit_type_id"].get<std::string>();
        json data = args;
        data.erase("audit_type_id");
        return client.put("/api/data/audit-types/" + audit_type_id, data);
    }
    if (name == "delete_audit_type") {
        client.del("/api/data/audit-types/" + args["audit_type_id"].get<std::string>());
        return {{"success", true}, {"message", "Audit type deleted"}};
    }

    // =========================================================================
    // VULNERABILITY TYPE TOOLS
    // =========================================================================
    if (name == "list_vulnerability_types") {
        return client.get("/api/data/vulnerability-types");
    }
    if (name == "create_vulnerability_type") {
        return client.post("/api/data/vulnerability-types", args);
    }
    if (name == "update_vulnerability_type") {
        std::string vuln_type_id = args["vuln_type_id"].get<std::string>();
        json data = args;
        data.erase("vuln_type_id");
        return client.put("/api/data/vulnerability-types/" + vuln_type_id, data);
    }
    if (name == "delete_vulnerability_type") {
        client.del("/api/data/vulnerability-types/" + args["vuln_type_id"].get<std::string>());
        return {{"success", true}, {"message", "Vulnerability type deleted"}};
    }

    // =========================================================================
    // VULNERABILITY CATEGORY TOOLS
    // =========================================================================
    if (name == "list_vulnerability_categories") {
        return client.get("/api/data/vulnerability-categories");
    }
    if (name == "create_vulnerability_category") {
        return client.post("/api/data/vulnerability-categories", args);
    }
    if (name == "update_vulnerability_category") {
        std::string category_id = args["category_id"].get<std::string>();
        json data = args;
        data.erase("category_id");
        return client.put("/api/data/vulnerability-categories/" + category_id, data);
    }
    if (name == "delete_vulnerability_category") {
        client.del("/api/data/vulnerability-categories/" + args["category_id"].get<std::string>());
        return {{"success", true}, {"message", "Vulnerability category deleted"}};
    }

    // =========================================================================
    // SECTION TOOLS
    // =========================================================================
    if (name == "list_sections") {
        return client.get("/api/data/sections");
    }
    if (name == "create_section") {
        return client.post("/api/data/sections", args);
    }
    if (name == "update_section") {
        std::string section_id = args["section_id"].get<std::string>();
        json data = args;
        data.erase("section_id");
        return client.put("/api/data/sections/" + section_id, data);
    }
    if (name == "delete_section") {
        client.del("/api/data/sections/" + args["section_id"].get<std::string>());
        return {{"success", true}, {"message", "Section deleted"}};
    }

    // =========================================================================
    // CUSTOM FIELD TOOLS
    // =========================================================================
    if (name == "list_custom_fields") {
        return client.get("/api/data/custom-fields");
    }
    if (name == "create_custom_field") {
        return client.post("/api/data/custom-fields", args);
    }
    if (name == "update_custom_field") {
        std::string field_id = args["field_id"].get<std::string>();
        json data = args;
        data.erase("field_id");
        return client.put("/api/data/custom-fields/" + field_id, data);
    }
    if (name == "delete_custom_field") {
        client.del("/api/data/custom-fields/" + args["field_id"].get<std::string>());
        return {{"success", true}, {"message", "Custom field deleted"}};
    }

    // =========================================================================
    // ROLE TOOLS
    // =========================================================================
    if (name == "list_roles") {
        return client.get("/api/data/roles");
    }

    // =========================================================================
    // IMAGE TOOLS
    // =========================================================================
    if (name == "get_image") {
        return client.get("/api/images/" + args["image_id"].get<std::string>());
    }
    if (name == "download_image") {
        return client.get("/api/images/download/" + args["image_id"].get<std::string>());
    }
    if (name == "upload_image") {
        json data = {
            {"auditId", args["audit_id"]},
            {"name", args["name"]},
            {"value", args["value"]}
        };
        return client.post("/api/images", data);
    }
    if (name == "delete_image") {
        client.del("/api/images/" + args["image_id"].get<std::string>());
        return {{"success", true}, {"message", "Image deleted"}};
    }

    // =========================================================================
    // STATISTICS
    // =========================================================================
    if (name == "get_statistics") {
        // Note: This is implemented in Python as client-side aggregation
        // For now, return basic implementation
        return {{"error", "get_statistics not yet implemented in C++ - use Python version"}};
    }

    throw std::runtime_error("Unknown tool: " + name);
}
