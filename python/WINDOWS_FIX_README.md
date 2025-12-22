# Windows MCP Zod Validation Error - Diagnostic & Fix

## Problem
You're seeing Zod validation errors in Claude Desktop on Windows:
```
invalid_union
invalid_type
Expected string, received null
```

## Step 1: Run Diagnostic

1. Open **Command Prompt** or **PowerShell** as Administrator
2. Navigate to where you saved `windows_diagnostic.py`
3. Run:
   ```cmd
   python windows_diagnostic.py > diagnostic_output.txt 2>&1
   ```
4. Open `diagnostic_output.txt` and read the results

## Step 2: Likely Fixes

### Fix A: Nuclear Fix Not Installed (Most Likely)

If diagnostic shows "Nuclear fix NOT found":

```cmd
pip uninstall pwndoc-mcp-server -y
pip install pwndoc-mcp-server --force-reinstall --no-cache-dir
```

Then **completely restart Claude Desktop** (not just close - fully quit from system tray).

### Fix B: Wrong Python Environment

If diagnostic shows the fix IS present but you still get errors, Claude Desktop might be using a different Python:

1. Find which Python Claude Desktop is configured to use:
   - Open: `%APPDATA%\Claude\claude_desktop_config.json`
   - Look for the `command` in the `pwndoc` MCP server config
   - Note the full path to Python

2. Install to that specific Python:
   ```cmd
   "C:\path\to\that\python.exe" -m pip install pwndoc-mcp-server --force-reinstall --no-cache-dir
   ```

### Fix C: Editable Install (Development)

If you're developing and have cloned the repo:

```cmd
cd C:\path\to\pwndoc-mcp-server\python
pip uninstall pwndoc-mcp-server -y
pip install -e .
```

## Step 3: Verify Fix

1. **Completely quit Claude Desktop** (right-click system tray icon → Exit)
2. Wait 10 seconds
3. Open Claude Desktop
4. Try using PwnDoc MCP server
5. Check if Zod errors are gone

## Still Having Issues?

Run the diagnostic again and share the `diagnostic_output.txt` file for further help.
