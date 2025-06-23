# Radicle MCP Server

A Model Context Protocol (MCP) server that provides tools for interacting with Radicle, a peer-to-peer code collaboration network.

## Features

This MCP server wraps common Radicle CLI commands as MCP tools, allowing AI assistants to:

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

2. **Python Environment**: Python 3.8+ with the MCP library
   ```bash
   pip install mcp
   ```

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### As a Standalone Server
```bash
python -m radicle_mcp.server
```

### With Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "radicle-mcp": {
      "command": "/path/to/python",
      "args": ["-m", "radicle_mcp.server"]
    }
  }
}
```

### VS Code Integration

This project includes VS Code configuration for debugging the MCP server. Use the provided `mcp.json` file to connect compatible MCP clients.

## Example Commands

Once connected to an MCP client, you can use natural language to interact with Radicle:

- "Initialize a new Radicle repository called 'my-project'"
- "Clone the repository with RID rad:z2..."
- "Show me the current patches in this repository"
- "Sync this repository with the network"
- "What's my Radicle node ID?"

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
