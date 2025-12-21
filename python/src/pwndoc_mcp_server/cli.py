"""
PwnDoc MCP Server - Command Line Interface.

Provides a rich CLI for managing the MCP server, configuration,
and PwnDoc interactions.

Usage:
    pwndoc-mcp serve                   # Start MCP server (stdio)
    pwndoc-mcp serve --transport sse   # Start SSE server
    pwndoc-mcp config init             # Interactive configuration
    pwndoc-mcp config show             # Show current config
    pwndoc-mcp test                    # Test connection
    pwndoc-mcp version                 # Show version
"""

import json
import logging
import sys
from pathlib import Path
from typing import Optional, Union

try:
    import typer  # type: ignore[import-not-found]
    from rich.console import Console  # type: ignore[import-not-found]
    from rich.panel import Panel  # type: ignore[import-not-found]
    from rich.prompt import Prompt  # type: ignore[import-not-found]
    from rich.syntax import Syntax  # type: ignore[import-not-found]
    from rich.table import Table  # type: ignore[import-not-found]

    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    typer = None  # type: ignore[assignment]
    Prompt = None  # type: ignore[assignment,misc]

from pwndoc_mcp_server import __version__
from pwndoc_mcp_server.client import PwnDocClient, PwnDocError
from pwndoc_mcp_server.config import (
    DEFAULT_CONFIG_FILE,
    init_config_interactive,
    load_config,
    save_config,
)
from pwndoc_mcp_server.server import PwnDocMCPServer

# Create CLI app
if HAS_RICH:
    app = typer.Typer(
        name="pwndoc-mcp",
        help="PwnDoc MCP Server - Model Context Protocol for Pentest Documentation",
        add_completion=True,
    )
    console = Console()

    def version_callback(value: bool):
        """Callback for --version flag."""
        if value:
            console.print(f"pwndoc-mcp-server version {__version__}")
            raise typer.Exit()

    @app.callback()
    def cli_callback(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show version and exit",
            callback=version_callback,
            is_eager=True,
        )
    ):
        """PwnDoc MCP Server CLI."""
        pass

else:
    app = None  # type: ignore[assignment]
    console = None  # type: ignore[assignment]
    version_callback = None  # type: ignore[assignment]


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Configure logging."""
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


# =============================================================================
# VERSION COMMAND
# =============================================================================

if HAS_RICH:

    @app.command()
    def version():
        """Show version information."""
        console.print(
            Panel(
                f"[bold green]PwnDoc MCP Server[/bold green]\n"
                f"Version: [cyan]{__version__}[/cyan]\n"
                f"Python: [cyan]{sys.version.split()[0]}[/cyan]",
                title="Version Info",
            )
        )


# =============================================================================
# SERVE COMMAND
# =============================================================================

if HAS_RICH:

    @app.command()
    def serve(
        transport: str = typer.Option("stdio", help="Transport type (stdio, sse)"),
        host: str = typer.Option("127.0.0.1", help="Host for SSE/WebSocket"),
        port: int = typer.Option(8080, help="Port for SSE/WebSocket"),
        log_level: str = typer.Option("INFO", help="Log level"),
        log_file: Optional[str] = typer.Option(None, help="Log file path"),
        config_file: Optional[Path] = typer.Option(None, "--config", "-c", help="Config file path"),
    ):
        """Start the MCP server."""
        setup_logging(log_level, log_file)

        try:
            config = load_config(
                config_file=config_file,
                mcp_transport=transport,
                mcp_host=host,
                mcp_port=port,
                log_level=log_level,
                log_file=log_file,
            )

            if not config.is_configured:
                console.print(
                    "[red]Error:[/red] Server not configured. Run 'pwndoc-mcp config init' first."
                )
                raise typer.Exit(1)

            if transport != "stdio":
                console.print("[green]Starting PwnDoc MCP Server[/green]")
                console.print(f"  Transport: [cyan]{transport}[/cyan]")
                console.print(f"  URL: [cyan]{config.url}[/cyan]")
                if transport == "sse":
                    console.print(f"  Endpoint: [cyan]http://{host}:{port}/mcp[/cyan]")

            server = PwnDocMCPServer(config)
            server.run(transport)

        except KeyboardInterrupt:
            console.print("\n[yellow]Server stopped[/yellow]")
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)


# =============================================================================
# CONFIG COMMANDS
# =============================================================================

if HAS_RICH:
    config_app = typer.Typer(help="Configuration management")
    app.add_typer(config_app, name="config")

    @config_app.command("init")
    def config_init():
        """Interactive configuration wizard."""
        try:
            init_config_interactive()
            console.print("[green]✓ Configuration complete![/green]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Configuration cancelled[/yellow]")

    @config_app.command("show")
    def config_show(
        reveal_secrets: bool = typer.Option(False, "--reveal", help="Show sensitive values"),
    ):
        """Show current configuration."""
        config = load_config()

        table = Table(title="Current Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("URL", config.url or "[dim]not set[/dim]")
        table.add_row("Username", config.username or "[dim]not set[/dim]")
        table.add_row(
            "Password",
            (
                ("*" * 8 if config.password else "[dim]not set[/dim]")
                if not reveal_secrets
                else config.password
            ),
        )
        table.add_row(
            "Token",
            (
                ("*" * 20 if config.token else "[dim]not set[/dim]")
                if not reveal_secrets
                else (config.token or "")
            ),
        )
        table.add_row("Verify SSL", str(config.verify_ssl))
        table.add_row("Timeout", str(config.timeout))
        table.add_row("Log Level", config.log_level)
        table.add_row("MCP Transport", config.mcp_transport)
        table.add_row("Auth Method", config.auth_method)
        table.add_row(
            "Configured",
            "[green]Yes[/green]" if config.is_configured else "[red]No[/red]",
        )

        console.print(table)
        console.print(f"\nConfig file: [dim]{DEFAULT_CONFIG_FILE}[/dim]")

    @config_app.command("set")
    def config_set(
        key: str = typer.Argument(..., help="Configuration key"),
        value: str = typer.Argument(..., help="Configuration value"),
    ):
        """Set a configuration value."""
        config = load_config()

        if hasattr(config, key):
            # Convert value to appropriate type
            current = getattr(config, key)
            converted_value: Union[bool, int, str]
            if isinstance(current, bool):
                converted_value = value.lower() in ("true", "1", "yes")
            elif isinstance(current, int):
                converted_value = int(value)
            else:
                converted_value = value

            setattr(config, key, converted_value)
            save_config(config)
            console.print(f"[green]✓[/green] Set {key} = {value}")
        else:
            console.print(f"[red]Error:[/red] Unknown configuration key: {key}")
            raise typer.Exit(1)

    @config_app.command("path")
    def config_path():
        """Show configuration file path."""
        console.print(f"[cyan]{DEFAULT_CONFIG_FILE}[/cyan]")
        if DEFAULT_CONFIG_FILE.exists():
            console.print("[green]  (exists)[/green]")
        else:
            console.print("[yellow]  (not created)[/yellow]")


# =============================================================================
# TEST COMMAND
# =============================================================================

if HAS_RICH:

    @app.command()
    def test(
        config_file: Optional[Path] = typer.Option(None, "--config", "-c", help="Config file path"),
    ):
        """Test connection to PwnDoc server."""
        config = load_config(config_file=config_file)

        if not config.is_configured:
            console.print(
                "[red]Error:[/red] Server not configured. Run 'pwndoc-mcp config init' first."
            )
            raise typer.Exit(1)

        console.print(f"Testing connection to [cyan]{config.url}[/cyan]...")

        try:
            with PwnDocClient(config) as client:
                client.authenticate()
                console.print("[green]✓ Authentication successful[/green]")

                user = client.get_current_user()
                console.print(f"[green]✓ Logged in as:[/green] {user.get('username', 'unknown')}")

                audits = client.list_audits()
                console.print(f"[green]✓ Found {len(audits)} audits[/green]")

                console.print("\n[bold green]All tests passed![/bold green]")

        except PwnDocError as e:
            console.print(f"[red]✗ Connection failed:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(1)


# =============================================================================
# QUERY COMMAND (for quick queries)
# =============================================================================

if HAS_RICH:

    @app.command()
    def query(
        tool: str = typer.Argument(..., help="Tool name to call"),
        params: Optional[str] = typer.Option(None, "--params", "-p", help="JSON parameters"),
        config_file: Optional[Path] = typer.Option(None, "--config", "-c", help="Config file path"),
    ):
        """Execute a tool query directly."""
        config = load_config(config_file=config_file)

        if not config.is_configured:
            console.print("[red]Error:[/red] Server not configured.")
            raise typer.Exit(1)

        server = PwnDocMCPServer(config)

        if tool not in server._tools:
            console.print(f"[red]Error:[/red] Unknown tool: {tool}")
            console.print("\nAvailable tools:")
            for t in sorted(server._tools.keys()):
                console.print(f"  • {t}")
            raise typer.Exit(1)

        try:
            arguments = json.loads(params) if params else {}
            result = server._tools[tool].handler(**arguments)

            # Pretty print result
            syntax = Syntax(json.dumps(result, indent=2, default=str), "json", theme="monokai")
            console.print(syntax)

        except json.JSONDecodeError as e:
            console.print(f"[red]Error:[/red] Invalid JSON parameters: {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)


# =============================================================================
# TOOLS COMMAND
# =============================================================================

if HAS_RICH:

    @app.command()
    def tools():
        """List all available MCP tools."""
        config = load_config()
        server = PwnDocMCPServer(config)

        table = Table(title="Available Tools")
        table.add_column("Tool", style="cyan")
        table.add_column("Description", style="white")

        for name, tool in sorted(server._tools.items()):
            table.add_row(
                name,
                tool.description[:60] + "..." if len(tool.description) > 60 else tool.description,
            )

        console.print(table)
        console.print(f"\nTotal: [cyan]{len(server._tools)}[/cyan] tools")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


def main():
    """Main entry point for CLI."""
    if not HAS_RICH:
        # Fallback to simple argparse if rich/typer not available
        import argparse

        parser = argparse.ArgumentParser(
            description="PwnDoc MCP Server",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
    pwndoc-mcp serve                    Start MCP server (stdio)
    pwndoc-mcp serve --transport sse    Start SSE server

For rich CLI experience, install: pip install typer[all] rich
            """,
        )

        subparsers = parser.add_subparsers(dest="command", help="Commands")

        # Serve command
        serve_parser = subparsers.add_parser("serve", help="Start MCP server")
        serve_parser.add_argument("--transport", default="stdio", choices=["stdio", "sse"])
        serve_parser.add_argument("--host", default="127.0.0.1")
        serve_parser.add_argument("--port", type=int, default=8080)
        serve_parser.add_argument("--log-level", default="INFO")
        serve_parser.add_argument("--config", "-c", type=Path)

        # Version command
        subparsers.add_parser("version", help="Show version")

        # Test command
        test_parser = subparsers.add_parser("test", help="Test connection")
        test_parser.add_argument("--config", "-c", type=Path)

        args = parser.parse_args()

        if args.command == "version":
            print(f"PwnDoc MCP Server v{__version__}")
        elif args.command == "serve":
            setup_logging(args.log_level)
            config = load_config(
                config_file=args.config,
                mcp_transport=args.transport,
                mcp_host=args.host,
                mcp_port=args.port,
            )
            server = PwnDocMCPServer(config)
            server.run()
        elif args.command == "test":
            config = load_config(config_file=args.config)
            try:
                with PwnDocClient(config) as client:
                    client.authenticate()
                    print("✓ Connection successful!")
            except Exception as e:
                print(f"✗ Connection failed: {e}")
                sys.exit(1)
        else:
            parser.print_help()
    else:
        app()


if __name__ == "__main__":
    main()
