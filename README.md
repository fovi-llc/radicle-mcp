# Radicle + GitHub MCP Server

A Model Context Protocol (MCP) server setup that provides tools for interacting with both Radicle (peer-to-peer code collaboration) and GitHub through a unified interface.

## Features

This setup includes two MCP servers:

### 🌟 Radicle MCP Server (Python)
- **Repository Management**: Initialize, clone, and inspect Radicle repositories
- **Synchronization**: Sync repositories with the Radicle network
- **Patches & Issues**: List and manage patches and issues
- **Node Information**: Get node ID and remote information
- **Help System**: Access Radicle command documentation

### 🐙 GitHub MCP Server (Official)
- **Repository Operations**: Create, fork, clone GitHub repositories
- **Issue Management**: Create, update, and manage GitHub issues
- **Pull Requests**: Manage pull requests and reviews
- **File Operations**: Read, write, and manage repository files
- **Search**: Search repositories, issues, and code
- **User Management**: Manage user and organization information

- **Repository Management**: Initialize, clone, and inspect Radicle repositories
- **Synchronization**: Sync repositories with the Radicle network
- **Patches & Issues**: List and manage patches and issues
- **Node Information**: Get node ID and remote information
- **Help System**: Access Radicle command documentation

## Available Tools

### Repository Operations
- `rad_init`: Initialize a new Radicle repository
- `rad_clone`: Clone an existing repository by RID
- `rad_status`: Get repository status and information
- `rad_sync`: Sync repository with the network
- `rad_push`: Push changes to the network

### Collaboration Features
- `rad_patch_list`: List patches (pull requests) in a repository
- `rad_issue_list`: List issues in a repository
- `rad_remote_list`: List remotes/nodes for a repository

### Node & Identity
- `rad_id`: Get your Radicle node ID
- `rad_help`: Get help for Radicle commands

## Prerequisites

1. **Radicle CLI**: Ensure the `rad` command is installed and available in your PATH
   ```bash
   # Install Radicle (see https://radicle.xyz for installation instructions)
   curl -sSf https://install.radicle.xyz | sh
   ```

2. **Deno**: For running the GitHub MCP server
   ```bash
   # Install Deno
   curl -fsSL https://deno.land/install.sh | sh
   ```

3. **Python Environment**: Python 3.8+ with the MCP library
   ```bash
   pip install mcp
   ```

4. **GitHub Personal Access Token**: For GitHub integration
   - Go to https://github.com/settings/tokens
   - Create a new token with repo, issues, and pull request permissions
   - Set as environment variable: `GITHUB_PERSONAL_ACCESS_TOKEN`

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Install the official GitHub MCP server:
   ```bash
   deno install -g --name github-mcp npm:@modelcontextprotocol/server-github
   ```
4. Run the setup script:
   ```bash
   python setup_mcp.py
   ```

## Usage

### Quick Setup
```bash
# Set your GitHub token
export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here

# Run the setup script
python setup_mcp.py
```

### As Standalone Servers
```bash
# Radicle MCP Server
python -m radicle_mcp.server

# GitHub MCP Server  
github-mcp
```

### With Claude Desktop

The setup script automatically creates the configuration. Your `claude_desktop_config.json` will include:

```json
{
  "mcpServers": {
    "radicle-mcp": {
      "command": "/path/to/python",
      "args": ["-m", "radicle_mcp.server"]
    },
    "github-mcp": {
      "command": "/path/to/github-mcp",
      "args": [],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

### VS Code Integration

This project includes VS Code configuration for debugging the MCP server. Use the provided `mcp.json` file to connect compatible MCP clients.

## Example Commands

Once connected to an MCP client, you can use natural language to interact with both platforms:

### Radicle Operations
- "Initialize a new Radicle repository called 'my-project'"
- "Clone the repository with RID rad:z2..."
- "Show me the current patches in this repository"
- "Sync this repository with the network"
- "What's my Radicle node ID?"

### GitHub Operations  
- "Create a new GitHub repository called 'awesome-project'"
- "List my recent GitHub repositories"
- "Create an issue titled 'Bug fix needed'"
- "Show me open pull requests in my repository"
- "Search for repositories related to 'machine learning'"

### Cross-Platform Workflows
- "Publish this Radicle repository to GitHub"
- "Sync issues between Radicle and GitHub"
- "Compare this repository on both platforms"

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
black src/
flake8 src/
```

## Project Structure

```
radicle-mcp/
├── src/radicle_mcp/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── .vscode/
│   └── mcp.json          # VS Code MCP configuration
├── .github/
│   └── copilot-instructions.md
├── pyproject.toml        # Project configuration
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Related Links

- [Radicle Documentation](https://docs.radicle.xyz/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
