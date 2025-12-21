#include "tools.hpp"
#include <stdexcept>

using json = nlohmann::json;

json get_tool_definitions() {
    return json::array({
        // ========== Audits (15 tools) ==========
        {{"name", "list_audits"}, {"description", "List all audits"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "get_audit"}, {"description", "Get audit details by ID"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        {{"name", "create_audit"}, {"description", "Create a new audit"}, {"inputSchema", {{"type", "object"}, {"properties", {{"name", {{"type", "string"}}}, {"language", {{"type", "string"}}}, {"type", {{"type", "string"}}}}}, {"required", {"name"}}}}},
        {{"name", "update_audit"}, {"description", "Update an existing audit"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"audit_id", "data"}}}}},
        {{"name", "delete_audit"}, {"description", "Delete an audit"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        {{"name", "get_audit_types"}, {"description", "Get available audit types"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "create_audit_type"}, {"description", "Create a new audit type"}, {"inputSchema", {{"type", "object"}, {"properties", {{"name", {{"type", "string"}}}}}, {"required", {"name"}}}}},
        {{"name", "update_audit_type"}, {"description", "Update an audit type"}, {"inputSchema", {{"type", "object"}, {"properties", {{"type_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"type_id", "data"}}}}},
        {{"name", "delete_audit_type"}, {"description", "Delete an audit type"}, {"inputSchema", {{"type", "object"}, {"properties", {{"type_id", {{"type", "string"}}}}}, {"required", {"type_id"}}}}},
        {{"name", "generate_audit_report"}, {"description", "Generate report for an audit"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        {{"name", "get_audit_network"}, {"description", "Get audit network information"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        {{"name", "update_audit_network"}, {"description", "Update audit network info"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"network", {{"type", "object"}}}}}, {"required", {"audit_id", "network"}}}}},
        {{"name", "sort_audit_findings"}, {"description", "Sort findings in an audit"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"sort_by", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        {{"name", "update_audit_sorting"}, {"description", "Update audit sorting preferences"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"sorting", {{"type", "object"}}}}}, {"required", {"audit_id", "sorting"}}}}},
        {{"name", "move_audit_finding"}, {"description", "Move finding position in audit"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}, {"position", {{"type", "integer"}}}}}, {"required", {"audit_id", "finding_id", "position"}}}}},
        
        // ========== Findings (12 tools) ==========
        {{"name", "list_findings"}, {"description", "List findings for an audit"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        {{"name", "get_finding"}, {"description", "Get finding details"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}}}, {"required", {"audit_id", "finding_id"}}}}},
        {{"name", "create_finding"}, {"description", "Create a new finding"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"title", {{"type", "string"}}}}}, {"required", {"audit_id", "title"}}}}},
        {{"name", "update_finding"}, {"description", "Update an existing finding"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"audit_id", "finding_id", "data"}}}}},
        {{"name", "delete_finding"}, {"description", "Delete a finding"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}}}, {"required", {"audit_id", "finding_id"}}}}},
        {{"name", "search_findings"}, {"description", "Search findings across all audits"}, {"inputSchema", {{"type", "object"}, {"properties", {{"title", {{"type", "string"}}}, {"vulnType", {{"type", "string"}}}, {"severity", {{"type", "string"}}}}}}}},
        {{"name", "get_finding_categories"}, {"description", "Get finding categories"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "create_finding_category"}, {"description", "Create finding category"}, {"inputSchema", {{"type", "object"}, {"properties", {{"name", {{"type", "string"}}}}}, {"required", {"name"}}}}},
        {{"name", "update_finding_category"}, {"description", "Update finding category"}, {"inputSchema", {{"type", "object"}, {"properties", {{"category_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"category_id", "data"}}}}},
        {{"name", "delete_finding_category"}, {"description", "Delete finding category"}, {"inputSchema", {{"type", "object"}, {"properties", {{"category_id", {{"type", "string"}}}}}, {"required", {"category_id"}}}}},
        {{"name", "import_findings"}, {"description", "Import findings from file"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"data", {{"type", "array"}}}}}, {"required", {"audit_id", "data"}}}}},
        {{"name", "export_findings"}, {"description", "Export findings from audit"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        
        // ========== Vulnerabilities (8 tools) ==========
        {{"name", "list_vulnerabilities"}, {"description", "List all vulnerabilities"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "get_vulnerability"}, {"description", "Get vulnerability details"}, {"inputSchema", {{"type", "object"}, {"properties", {{"vuln_id", {{"type", "string"}}}}}, {"required", {"vuln_id"}}}}},
        {{"name", "create_vulnerability"}, {"description", "Create new vulnerability"}, {"inputSchema", {{"type", "object"}, {"properties", {{"title", {{"type", "string"}}}}}, {"required", {"title"}}}}},
        {{"name", "update_vulnerability"}, {"description", "Update vulnerability"}, {"inputSchema", {{"type", "object"}, {"properties", {{"vuln_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"vuln_id", "data"}}}}},
        {{"name", "delete_vulnerability"}, {"description", "Delete vulnerability"}, {"inputSchema", {{"type", "object"}, {"properties", {{"vuln_id", {{"type", "string"}}}}}, {"required", {"vuln_id"}}}}},
        {{"name", "merge_vulnerability"}, {"description", "Merge vulnerabilities"}, {"inputSchema", {{"type", "object"}, {"properties", {{"source_id", {{"type", "string"}}}, {"target_id", {{"type", "string"}}}}}, {"required", {"source_id", "target_id"}}}}},
        {{"name", "get_vulnerability_updates"}, {"description", "Get vulnerability updates"}, {"inputSchema", {{"type", "object"}, {"properties", {{"vuln_id", {{"type", "string"}}}}}, {"required", {"vuln_id"}}}}},
        {{"name", "import_vulnerabilities"}, {"description", "Import vulnerabilities"}, {"inputSchema", {{"type", "object"}, {"properties", {{"data", {{"type", "array"}}}}}, {"required", {"data"}}}}},
        
        // ========== Clients (6 tools) ==========
        {{"name", "list_clients"}, {"description", "List all clients"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "get_client"}, {"description", "Get client details"}, {"inputSchema", {{"type", "object"}, {"properties", {{"client_id", {{"type", "string"}}}}}, {"required", {"client_id"}}}}},
        {{"name", "create_client"}, {"description", "Create new client"}, {"inputSchema", {{"type", "object"}, {"properties", {{"company", {{"type", "string"}}}}}, {"required", {"company"}}}}},
        {{"name", "update_client"}, {"description", "Update client"}, {"inputSchema", {{"type", "object"}, {"properties", {{"client_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"client_id", "data"}}}}},
        {{"name", "delete_client"}, {"description", "Delete client"}, {"inputSchema", {{"type", "object"}, {"properties", {{"client_id", {{"type", "string"}}}}}, {"required", {"client_id"}}}}},
        {{"name", "get_client_audits"}, {"description", "Get audits for a client"}, {"inputSchema", {{"type", "object"}, {"properties", {{"client_id", {{"type", "string"}}}}}, {"required", {"client_id"}}}}},
        
        // ========== Companies (6 tools) ==========
        {{"name", "list_companies"}, {"description", "List all companies"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "get_company"}, {"description", "Get company details"}, {"inputSchema", {{"type", "object"}, {"properties", {{"company_id", {{"type", "string"}}}}}, {"required", {"company_id"}}}}},
        {{"name", "create_company"}, {"description", "Create new company"}, {"inputSchema", {{"type", "object"}, {"properties", {{"name", {{"type", "string"}}}}}, {"required", {"name"}}}}},
        {{"name", "update_company"}, {"description", "Update company"}, {"inputSchema", {{"type", "object"}, {"properties", {{"company_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"company_id", "data"}}}}},
        {{"name", "delete_company"}, {"description", "Delete company"}, {"inputSchema", {{"type", "object"}, {"properties", {{"company_id", {{"type", "string"}}}}}, {"required", {"company_id"}}}}},
        {{"name", "get_company_stats"}, {"description", "Get company statistics"}, {"inputSchema", {{"type", "object"}, {"properties", {{"company_id", {{"type", "string"}}}}}, {"required", {"company_id"}}}}},
        
        // ========== Users (8 tools) ==========
        {{"name", "list_users"}, {"description", "List all users"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "get_user"}, {"description", "Get user details"}, {"inputSchema", {{"type", "object"}, {"properties", {{"user_id", {{"type", "string"}}}}}, {"required", {"user_id"}}}}},
        {{"name", "create_user"}, {"description", "Create new user"}, {"inputSchema", {{"type", "object"}, {"properties", {{"username", {{"type", "string"}}}, {"password", {{"type", "string"}}}}}, {"required", {"username", "password"}}}}},
        {{"name", "update_user"}, {"description", "Update user"}, {"inputSchema", {{"type", "object"}, {"properties", {{"user_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"user_id", "data"}}}}},
        {{"name", "delete_user"}, {"description", "Delete user"}, {"inputSchema", {{"type", "object"}, {"properties", {{"user_id", {{"type", "string"}}}}}, {"required", {"user_id"}}}}},
        {{"name", "get_current_user"}, {"description", "Get current logged in user"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "update_current_user"}, {"description", "Update current user profile"}, {"inputSchema", {{"type", "object"}, {"properties", {{"data", {{"type", "object"}}}}}, {"required", {"data"}}}}},
        {{"name", "change_password"}, {"description", "Change user password"}, {"inputSchema", {{"type", "object"}, {"properties", {{"current_password", {{"type", "string"}}}, {"new_password", {{"type", "string"}}}}}, {"required", {"current_password", "new_password"}}}}},
        
        // ========== Templates (10 tools) ==========
        {{"name", "list_templates"}, {"description", "List all templates"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "get_template"}, {"description", "Get template details"}, {"inputSchema", {{"type", "object"}, {"properties", {{"template_id", {{"type", "string"}}}}}, {"required", {"template_id"}}}}},
        {{"name", "create_template"}, {"description", "Create new template"}, {"inputSchema", {{"type", "object"}, {"properties", {{"name", {{"type", "string"}}}}}, {"required", {"name"}}}}},
        {{"name", "update_template"}, {"description", "Update template"}, {"inputSchema", {{"type", "object"}, {"properties", {{"template_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"template_id", "data"}}}}},
        {{"name", "delete_template"}, {"description", "Delete template"}, {"inputSchema", {{"type", "object"}, {"properties", {{"template_id", {{"type", "string"}}}}}, {"required", {"template_id"}}}}},
        {{"name", "list_sections"}, {"description", "List template sections"}, {"inputSchema", {{"type", "object"}, {"properties", {{"template_id", {{"type", "string"}}}}}, {"required", {"template_id"}}}}},
        {{"name", "create_section"}, {"description", "Create template section"}, {"inputSchema", {{"type", "object"}, {"properties", {{"template_id", {{"type", "string"}}}, {"name", {{"type", "string"}}}}}, {"required", {"template_id", "name"}}}}},
        {{"name", "update_section"}, {"description", "Update template section"}, {"inputSchema", {{"type", "object"}, {"properties", {{"template_id", {{"type", "string"}}}, {"section_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"template_id", "section_id", "data"}}}}},
        {{"name", "delete_section"}, {"description", "Delete template section"}, {"inputSchema", {{"type", "object"}, {"properties", {{"template_id", {{"type", "string"}}}, {"section_id", {{"type", "string"}}}}}, {"required", {"template_id", "section_id"}}}}},
        {{"name", "get_custom_fields"}, {"description", "Get custom fields configuration"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        
        // ========== Languages (4 tools) ==========
        {{"name", "list_languages"}, {"description", "List all languages"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "create_language"}, {"description", "Create new language"}, {"inputSchema", {{"type", "object"}, {"properties", {{"language", {{"type", "string"}}}, {"locale", {{"type", "string"}}}}}, {"required", {"language", "locale"}}}}},
        {{"name", "update_language"}, {"description", "Update language"}, {"inputSchema", {{"type", "object"}, {"properties", {{"lang_id", {{"type", "string"}}}, {"data", {{"type", "object"}}}}}, {"required", {"lang_id", "data"}}}}},
        {{"name", "delete_language"}, {"description", "Delete language"}, {"inputSchema", {{"type", "object"}, {"properties", {{"lang_id", {{"type", "string"}}}}}, {"required", {"lang_id"}}}}},
        
        // ========== Settings (4 tools) ==========
        {{"name", "get_settings"}, {"description", "Get system settings"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "update_settings"}, {"description", "Update system settings"}, {"inputSchema", {{"type", "object"}, {"properties", {{"data", {{"type", "object"}}}}}, {"required", {"data"}}}}},
        {{"name", "get_reviews"}, {"description", "Get review configuration"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "export_reviews"}, {"description", "Export reviews"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        
        // ========== Images (4 tools) ==========
        {{"name", "upload_image"}, {"description", "Upload an image"}, {"inputSchema", {{"type", "object"}, {"properties", {{"image_base64", {{"type", "string"}}}, {"filename", {{"type", "string"}}}}}, {"required", {"image_base64", "filename"}}}}},
        {{"name", "get_image"}, {"description", "Get image metadata"}, {"inputSchema", {{"type", "object"}, {"properties", {{"image_id", {{"type", "string"}}}}}, {"required", {"image_id"}}}}},
        {{"name", "download_image"}, {"description", "Download image data"}, {"inputSchema", {{"type", "object"}, {"properties", {{"image_id", {{"type", "string"}}}}}, {"required", {"image_id"}}}}},
        {{"name", "delete_image"}, {"description", "Delete an image"}, {"inputSchema", {{"type", "object"}, {"properties", {{"image_id", {{"type", "string"}}}}}, {"required", {"image_id"}}}}},
        
        // ========== Data (6 tools) ==========
        {{"name", "get_statistics"}, {"description", "Get system statistics"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "get_cvss_scores"}, {"description", "Get CVSS score distribution"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "backup_data"}, {"description", "Create system backup"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "restore_data"}, {"description", "Restore from backup"}, {"inputSchema", {{"type", "object"}, {"properties", {{"backup_data", {{"type", "object"}}}}}, {"required", {"backup_data"}}}}},
        {{"name", "export_data"}, {"description", "Export all data"}, {"inputSchema", {{"type", "object"}, {"properties", json::object()}}}},
        {{"name", "import_data"}, {"description", "Import data"}, {"inputSchema", {{"type", "object"}, {"properties", {{"data", {{"type", "object"}}}}}, {"required", {"data"}}}}},
        
        // ========== Collaboration (6 tools) ==========
        {{"name", "list_comments"}, {"description", "List comments on finding"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}}}, {"required", {"audit_id", "finding_id"}}}}},
        {{"name", "create_comment"}, {"description", "Add comment to finding"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}, {"text", {{"type", "string"}}}}}, {"required", {"audit_id", "finding_id", "text"}}}}},
        {{"name", "update_comment"}, {"description", "Update comment"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}, {"comment_id", {{"type", "string"}}}, {"text", {{"type", "string"}}}}}, {"required", {"audit_id", "finding_id", "comment_id", "text"}}}}},
        {{"name", "delete_comment"}, {"description", "Delete comment"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}, {"comment_id", {{"type", "string"}}}}}, {"required", {"audit_id", "finding_id", "comment_id"}}}}},
        {{"name", "get_audit_history"}, {"description", "Get audit change history"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}}}, {"required", {"audit_id"}}}}},
        {{"name", "get_finding_history"}, {"description", "Get finding change history"}, {"inputSchema", {{"type", "object"}, {"properties", {{"audit_id", {{"type", "string"}}}, {"finding_id", {{"type", "string"}}}}}, {"required", {"audit_id", "finding_id"}}}}}
    });
}

json execute_tool(PwnDocClient& client, const std::string& name, const json& args) {
    // ========== Audits ==========
    if (name == "list_audits") return client.get("/audits");
    if (name == "get_audit") return client.get("/audits/" + args["audit_id"].get<std::string>());
    if (name == "create_audit") return client.post("/audits", args);
    if (name == "update_audit") return client.put("/audits/" + args["audit_id"].get<std::string>(), args["data"]);
    if (name == "delete_audit") return client.del("/audits/" + args["audit_id"].get<std::string>());
    if (name == "get_audit_types") return client.get("/data/audit-types");
    if (name == "create_audit_type") return client.post("/data/audit-types", args);
    if (name == "update_audit_type") return client.put("/data/audit-types/" + args["type_id"].get<std::string>(), args["data"]);
    if (name == "delete_audit_type") return client.del("/data/audit-types/" + args["type_id"].get<std::string>());
    if (name == "generate_audit_report") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/generate");
    if (name == "get_audit_network") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/network");
    if (name == "update_audit_network") return client.put("/audits/" + args["audit_id"].get<std::string>() + "/network", args["network"]);
    if (name == "sort_audit_findings") return client.put("/audits/" + args["audit_id"].get<std::string>() + "/sortfindings", {{"sortBy", args.value("sort_by", "cvss")}});
    if (name == "update_audit_sorting") return client.put("/audits/" + args["audit_id"].get<std::string>() + "/sorting", args["sorting"]);
    if (name == "move_audit_finding") return client.put("/audits/" + args["audit_id"].get<std::string>() + "/movefinding", {{"findingId", args["finding_id"]}, {"position", args["position"]}});
    
    // ========== Findings ==========
    if (name == "list_findings") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/findings");
    if (name == "get_finding") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>());
    if (name == "create_finding") {
        json data = args;
        std::string audit_id = data["audit_id"].get<std::string>();
        data.erase("audit_id");
        return client.post("/audits/" + audit_id + "/findings", data);
    }
    if (name == "update_finding") return client.put("/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>(), args["data"]);
    if (name == "delete_finding") return client.del("/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>());
    if (name == "search_findings") return client.get("/findings");
    if (name == "get_finding_categories") return client.get("/data/vulnerability-categories");
    if (name == "create_finding_category") return client.post("/data/vulnerability-categories", args);
    if (name == "update_finding_category") return client.put("/data/vulnerability-categories/" + args["category_id"].get<std::string>(), args["data"]);
    if (name == "delete_finding_category") return client.del("/data/vulnerability-categories/" + args["category_id"].get<std::string>());
    if (name == "import_findings") return client.post("/audits/" + args["audit_id"].get<std::string>() + "/findings/import", args["data"]);
    if (name == "export_findings") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/findings/export");
    
    // ========== Vulnerabilities ==========
    if (name == "list_vulnerabilities") return client.get("/vulnerabilities");
    if (name == "get_vulnerability") return client.get("/vulnerabilities/" + args["vuln_id"].get<std::string>());
    if (name == "create_vulnerability") return client.post("/vulnerabilities", args);
    if (name == "update_vulnerability") return client.put("/vulnerabilities/" + args["vuln_id"].get<std::string>(), args["data"]);
    if (name == "delete_vulnerability") return client.del("/vulnerabilities/" + args["vuln_id"].get<std::string>());
    if (name == "merge_vulnerability") return client.post("/vulnerabilities/" + args["source_id"].get<std::string>() + "/merge/" + args["target_id"].get<std::string>());
    if (name == "get_vulnerability_updates") return client.get("/vulnerabilities/" + args["vuln_id"].get<std::string>() + "/updates");
    if (name == "import_vulnerabilities") return client.post("/vulnerabilities/import", args["data"]);
    
    // ========== Clients ==========
    if (name == "list_clients") return client.get("/clients");
    if (name == "get_client") return client.get("/clients/" + args["client_id"].get<std::string>());
    if (name == "create_client") return client.post("/clients", args);
    if (name == "update_client") return client.put("/clients/" + args["client_id"].get<std::string>(), args["data"]);
    if (name == "delete_client") return client.del("/clients/" + args["client_id"].get<std::string>());
    if (name == "get_client_audits") return client.get("/clients/" + args["client_id"].get<std::string>() + "/audits");
    
    // ========== Companies ==========
    if (name == "list_companies") return client.get("/companies");
    if (name == "get_company") return client.get("/companies/" + args["company_id"].get<std::string>());
    if (name == "create_company") return client.post("/companies", args);
    if (name == "update_company") return client.put("/companies/" + args["company_id"].get<std::string>(), args["data"]);
    if (name == "delete_company") return client.del("/companies/" + args["company_id"].get<std::string>());
    if (name == "get_company_stats") return client.get("/companies/" + args["company_id"].get<std::string>() + "/statistics");
    
    // ========== Users ==========
    if (name == "list_users") return client.get("/users");
    if (name == "get_user") return client.get("/users/" + args["user_id"].get<std::string>());
    if (name == "create_user") return client.post("/users", args);
    if (name == "update_user") return client.put("/users/" + args["user_id"].get<std::string>(), args["data"]);
    if (name == "delete_user") return client.del("/users/" + args["user_id"].get<std::string>());
    if (name == "get_current_user") return client.get("/users/me");
    if (name == "update_current_user") return client.put("/users/me", args["data"]);
    if (name == "change_password") return client.put("/users/me/password", {{"currentPassword", args["current_password"]}, {"newPassword", args["new_password"]}});
    
    // ========== Templates ==========
    if (name == "list_templates") return client.get("/templates");
    if (name == "get_template") return client.get("/templates/" + args["template_id"].get<std::string>());
    if (name == "create_template") return client.post("/templates", args);
    if (name == "update_template") return client.put("/templates/" + args["template_id"].get<std::string>(), args["data"]);
    if (name == "delete_template") return client.del("/templates/" + args["template_id"].get<std::string>());
    if (name == "list_sections") return client.get("/templates/" + args["template_id"].get<std::string>() + "/sections");
    if (name == "create_section") return client.post("/templates/" + args["template_id"].get<std::string>() + "/sections", args);
    if (name == "update_section") return client.put("/templates/" + args["template_id"].get<std::string>() + "/sections/" + args["section_id"].get<std::string>(), args["data"]);
    if (name == "delete_section") return client.del("/templates/" + args["template_id"].get<std::string>() + "/sections/" + args["section_id"].get<std::string>());
    if (name == "get_custom_fields") return client.get("/data/custom-fields");
    
    // ========== Languages ==========
    if (name == "list_languages") return client.get("/data/languages");
    if (name == "create_language") return client.post("/data/languages", args);
    if (name == "update_language") return client.put("/data/languages/" + args["lang_id"].get<std::string>(), args["data"]);
    if (name == "delete_language") return client.del("/data/languages/" + args["lang_id"].get<std::string>());
    
    // ========== Settings ==========
    if (name == "get_settings") return client.get("/settings");
    if (name == "update_settings") return client.put("/settings", args["data"]);
    if (name == "get_reviews") return client.get("/data/reviews");
    if (name == "export_reviews") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/reviews/export");
    
    // ========== Images ==========
    if (name == "upload_image") return {{"error", "Image upload not implemented in native version"}};
    if (name == "get_image") return client.get("/images/" + args["image_id"].get<std::string>());
    if (name == "download_image") return {{"error", "Image download not implemented in native version"}};
    if (name == "delete_image") return client.del("/images/" + args["image_id"].get<std::string>());
    
    // ========== Data ==========
    if (name == "get_statistics") return client.get("/data/statistics");
    if (name == "get_cvss_scores") return client.get("/data/cvss-scores");
    if (name == "backup_data") return client.get("/data/backup");
    if (name == "restore_data") return client.post("/data/restore", args["backup_data"]);
    if (name == "export_data") return client.get("/data/export");
    if (name == "import_data") return client.post("/data/import", args["data"]);
    
    // ========== Collaboration ==========
    if (name == "list_comments") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>() + "/comments");
    if (name == "create_comment") return client.post("/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>() + "/comments", {{"text", args["text"]}});
    if (name == "update_comment") return client.put("/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>() + "/comments/" + args["comment_id"].get<std::string>(), {{"text", args["text"]}});
    if (name == "delete_comment") return client.del("/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>() + "/comments/" + args["comment_id"].get<std::string>());
    if (name == "get_audit_history") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/history");
    if (name == "get_finding_history") return client.get("/audits/" + args["audit_id"].get<std::string>() + "/findings/" + args["finding_id"].get<std::string>() + "/history");
    
    throw std::runtime_error("Unknown tool: " + name);
}
