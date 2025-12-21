"""
Utility to bump all version references for a new release.

Usage:
    python scripts/bump_version.py --version v1.0.3

Pass the version with or without a leading "v". The script updates:
- python/pyproject.toml
- python/src/pwndoc_mcp_server/version.py (fallback version)
- python/src/pwndoc_mcp_server/server.py (SERVER_VERSION)
- mcp-registry.json
- packaging/homebrew/pwndoc-mcp-server.rb
- packaging/scoop/pwndoc-mcp-server.json
- docs references that embed the release version

The goal is to keep CLI output, metadata, docs, and packaging manifests in sync
with the release tag (e.g., v1.0.3).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Callable


def normalize_version(raw: str) -> tuple[str, str]:
    """Return (version, tag) where tag always includes the leading 'v'."""
    cleaned = raw.strip()
    version = cleaned[1:] if cleaned.startswith("v") else cleaned
    tag = f"v{version}"
    return version, tag


def update_file(path: Path, pattern: str, repl: Callable[[re.Match[str]], str]) -> None:
    text = path.read_text(encoding="utf-8")
    new_text, count = re.subn(pattern, repl, text, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"Pattern not found in {path}: {pattern}")
    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump version across the repository.")
    parser.add_argument("--version", required=True, help="Release version (e.g., v1.0.3 or 1.0.3)")
    args = parser.parse_args()

    version, tag = normalize_version(args.version)

    root = Path(__file__).resolve().parents[2]  # repo root

    # Core metadata
    update_file(
        root / "python" / "pyproject.toml",
        r'^version = "[^"]+"',
        lambda _: f'version = "{version}"',
    )
    update_file(
        root / "python" / "src" / "pwndoc_mcp_server" / "version.py",
        r'_FALLBACK_VERSION = "[^"]+"',
        lambda _: f'_FALLBACK_VERSION = "{version}"',
    )
    update_file(
        root / "mcp-registry.json",
        r'"version": "[^"]+"',
        lambda _: f'"version": "{version}"',
    )

    # Packaging manifests
    update_file(
        root / "packaging" / "homebrew" / "pwndoc-mcp-server.rb",
        r"v[0-9]+\.[0-9]+\.[0-9]+\.tar\.gz",
        lambda _: f"{tag}.tar.gz",
    )
    update_file(
        root / "packaging" / "scoop" / "pwndoc-mcp-server.json",
        r'"version": "[^"]+"',
        lambda _: f'"version": "{version}"',
    )
    update_file(
        root / "packaging" / "scoop" / "pwndoc-mcp-server.json",
        r"releases/download/v[0-9]+\.[0-9]+\.[0-9]+/pwndoc-mcp-server-windows-x64\.exe",
        lambda _: f"releases/download/{tag}/pwndoc-mcp-server-windows-x64.exe",
    )

    # Documentation references (keep these scoped to release numbers)
    docs_patterns = [
        (root / "docs" / "user-guide" / "cli.md", r"pwndoc-mcp-server [0-9]+\.[0-9]+\.[0-9]+"),
        (root / "docs" / "user-guide" / "docker.md", r'"version": "[0-9]+\.[0-9]+\.[0-9]+"'),
        (root / "docs" / "user-guide" / "docker.md", r"`[0-9]+\.[0-9]+\.[0-9]+`"),
        (root / "docs" / "development" / "building.md", r"pwndoc_mcp_server-[0-9]+\.[0-9]+\.[0-9]+"),
        (root / "docs" / "development" / "building.md", r"pwndoc-mcp-server:[0-9]+\.[0-9]+\.[0-9]+"),
        (root / "docs" / "development" / "building.md", r"pwndoc-mcp-server_[0-9]+\.[0-9]+\.[0-9]+"),
        (root / "docs" / "getting-started" / "installation.md", r"pwndoc-mcp-server_[0-9]+\.[0-9]+\.[0-9]+_amd64\.deb"),
        (root / "docs" / "getting-started" / "installation.md", r"pwndoc-mcp-server-[0-9]+\.[0-9]+\.[0-9]+-1\.x86_64\.rpm"),
    ]

    def replace_version_literal(match: re.Match[str]) -> str:
        return re.sub(r"[0-9]+\.[0-9]+\.[0-9]+", version, match.group(0))

    for path, pattern in docs_patterns:
        update_file(path, pattern, replace_version_literal)

    print(f"Updated repository version to {version} (tag {tag})")


if __name__ == "__main__":
    main()
