#!/usr/bin/env python3
"""
Windows diagnostic script for MCP server issues.
Run this on your Windows machine to identify the problem.
"""
import sys
import os
import subprocess
import json

print("=== PwnDoc MCP Server Diagnostic Tool ===\n")

# 1. Check Python version
print(f"1. Python Version: {sys.version}")
print(f"   Python Executable: {sys.executable}\n")

# 2. Check pwndoc-mcp-server installation
print("2. Checking pwndoc-mcp-server installation...")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "pwndoc-mcp-server"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
except Exception as e:
    print(f"   ERROR: {e}\n")

# 3. Check actual module location
print("3. Checking actual module location...")
try:
    import pwndoc_mcp_server
    import inspect
    module_file = inspect.getfile(pwndoc_mcp_server)
    print(f"   Module loaded from: {module_file}")
    print(f"   Module version: {pwndoc_mcp_server.__version__}\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

# 4. Check for nuclear fix
print("4. Checking for nuclear fix...")
try:
    import pwndoc_mcp_server
    has_fix = hasattr(pwndoc_mcp_server, '_devnull')
    print(f"   Nuclear fix present: {has_fix}")
    if not has_fix:
        print("   ⚠️  WARNING: Nuclear fix NOT found in installed version!")
        print("   This is the likely cause of your Zod validation errors.\n")
    else:
        print("   ✅ Nuclear fix is present.\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

# 5. Check Claude Desktop config
print("5. Checking Claude Desktop configuration...")
config_paths = [
    os.path.join(os.environ.get('APPDATA', ''), 'Claude', 'claude_desktop_config.json'),
    os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Roaming', 'Claude', 'claude_desktop_config.json'),
]

config_found = False
for config_path in config_paths:
    if os.path.exists(config_path):
        print(f"   Config found at: {config_path}")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                if 'mcpServers' in config and 'pwndoc' in config['mcpServers']:
                    print(f"   PwnDoc MCP Server config:")
                    print(f"   {json.dumps(config['mcpServers']['pwndoc'], indent=4)}\n")
                    config_found = True
        except Exception as e:
            print(f"   ERROR reading config: {e}\n")

if not config_found:
    print("   ⚠️  WARNING: Could not find Claude Desktop config or pwndoc server config.\n")

# 6. Test stdout pollution
print("6. Testing for stdout pollution...")
import io
original_stdout = sys.stdout
captured = io.StringIO()
sys.stdout = captured

try:
    # Force reimport
    if 'pwndoc_mcp_server' in sys.modules:
        del sys.modules['pwndoc_mcp_server']

    import pwndoc_mcp_server
    from pwndoc_mcp_server.server import get_tool_definitions
    tools = get_tool_definitions()
except Exception as e:
    sys.stdout = original_stdout
    print(f"   ERROR during import: {e}")
finally:
    sys.stdout = original_stdout

captured_output = captured.getvalue()
if captured_output:
    print(f"   ⚠️  STDOUT POLLUTION DETECTED! ({len(captured_output)} bytes)")
    print(f"   Content: {repr(captured_output[:200])}")
    if len(captured_output) > 200:
        print(f"   ... (truncated, {len(captured_output) - 200} more bytes)")
    print()
else:
    print("   ✅ No stdout pollution detected.\n")

# 7. Summary
print("=== SUMMARY ===")
print("If you see 'Nuclear fix NOT found' above, you need to reinstall:")
print("  pip uninstall pwndoc-mcp-server -y")
print("  pip install pwndoc-mcp-server --force-reinstall --no-cache-dir")
print("\nIf you see 'STDOUT POLLUTION DETECTED', please share the output with Claude.")
print("\nAfter any fixes, restart Claude Desktop completely.")
