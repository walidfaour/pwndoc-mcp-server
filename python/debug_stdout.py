#!/usr/bin/env python3
"""
Debug script to capture exactly what's being written to stdout during MCP server startup.
This will help us identify the source of the Zod validation errors.
"""
import sys
import io
import json

# Capture stdout
original_stdout = sys.stdout
captured_output = io.StringIO()
sys.stdout = captured_output

try:
    # Import the MCP server (this is what Claude Desktop does)
    import pwndoc_mcp_server
    from pwndoc_mcp_server import create_server

    # Try to get tool definitions (this might trigger output)
    from pwndoc_mcp_server.server import get_tool_definitions
    tools = get_tool_definitions()

except Exception as e:
    # Restore stdout to print the error
    sys.stdout = original_stdout
    print(f"ERROR during import: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
finally:
    # Restore stdout
    sys.stdout = original_stdout

# Get what was captured
captured = captured_output.getvalue()

print("=== CAPTURED STDOUT OUTPUT ===", file=sys.stderr)
print(f"Length: {len(captured)} bytes", file=sys.stderr)
print(f"Content:\n{repr(captured)}", file=sys.stderr)
print("=== END CAPTURED OUTPUT ===", file=sys.stderr)

if captured:
    print("\n⚠️  STDOUT POLLUTION DETECTED!", file=sys.stderr)
    print("The following was written to stdout during import:", file=sys.stderr)
    print(captured, file=sys.stderr)

    # Try to identify the source
    if "warning" in captured.lower():
        print("\n💡 Looks like a warning message", file=sys.stderr)
    if "error" in captured.lower():
        print("\n💡 Looks like an error message", file=sys.stderr)
    if "info" in captured.lower() or "debug" in captured.lower():
        print("\n💡 Looks like a logging message", file=sys.stderr)
else:
    print("\n✅ No stdout pollution detected!", file=sys.stderr)
