# Homebrew Formula for PwnDoc MCP Server
# 
# To install:
#   brew tap walidfaour/pwndoc
#   brew install pwndoc-mcp-server
#
# Or directly:
#   brew install walidfaour/pwndoc/pwndoc-mcp-server

class PwndocMcpServer < Formula
  include Language::Python::Virtualenv

  desc "Model Context Protocol server for PwnDoc penetration testing documentation"
  homepage "https://github.com/walidfaour/pwndoc-mcp-server"
  url "https://github.com/walidfaour/pwndoc-mcp-server/archive/refs/tags/v1.0.7.tar.gz"
  sha256 "PLACEHOLDER_SHA256"  # Update with actual sha256 after release
  license "MIT"
  head "https://github.com/walidfaour/pwndoc-mcp-server.git", branch: "main"

  # Bottle configuration (pre-built binaries)
  # bottle do
  #   sha256 cellar: :any_skip_relocation, arm64_sonoma: "PLACEHOLDER"
  #   sha256 cellar: :any_skip_relocation, ventura: "PLACEHOLDER"
  #   sha256 cellar: :any_skip_relocation, monterey: "PLACEHOLDER"
  # end

  depends_on "python@3.11"

  resource "httpx" do
    url "https://files.pythonhosted.org/packages/source/h/httpx/httpx-0.27.0.tar.gz"
    sha256 "PLACEHOLDER_SHA256"
  end

  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/source/P/PyYAML/PyYAML-6.0.1.tar.gz"
    sha256 "PLACEHOLDER_SHA256"
  end

  resource "typer" do
    url "https://files.pythonhosted.org/packages/source/t/typer/typer-0.9.0.tar.gz"
    sha256 "PLACEHOLDER_SHA256"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.7.0.tar.gz"
    sha256 "PLACEHOLDER_SHA256"
  end

  def install
    virtualenv_install_with_resources

    # Generate shell completions
    generate_completions_from_executable(bin/"pwndoc-mcp", shells: [:bash, :zsh, :fish], shell_parameter_format: :click)
  end

  def caveats
    <<~EOS
      PwnDoc MCP Server has been installed!

      To configure, run:
        pwndoc-mcp config init

      Or set environment variables:
        export PWNDOC_URL="https://your-pwndoc-instance.com"
        export PWNDOC_USERNAME="your-username"
        export PWNDOC_PASSWORD="your-password"

      To integrate with Claude Desktop, add to your config:
        {
          "mcpServers": {
            "pwndoc": {
              "command": "#{opt_bin}/pwndoc-mcp",
              "args": ["serve"]
            }
          }
        }

      For more information:
        https://github.com/walidfaour/pwndoc-mcp-server
    EOS
  end

  test do
    # Test version output
    assert_match "pwndoc-mcp-server", shell_output("#{bin}/pwndoc-mcp --version")

    # Test help
    assert_match "PwnDoc MCP Server", shell_output("#{bin}/pwndoc-mcp --help")

    # Test tools listing
    assert_match "list_audits", shell_output("#{bin}/pwndoc-mcp tools")
  end
end
