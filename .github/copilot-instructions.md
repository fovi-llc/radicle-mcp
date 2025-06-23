# Copilot Instructions for Radicle MCP Server

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a Model Context Protocol (MCP) server project for Radicle, a peer-to-peer code collaboration network.

## Project Context
- This MCP server provides tools for interacting with Radicle repositories
- It wraps Radicle CLI commands as MCP tools for use by AI assistants
- The server uses Python's `mcp` library with FastMCP for easy tool definition
- All Radicle operations are performed through subprocess calls to the `rad` CLI

## Key Guidelines
1. **Tool Functions**: Each MCP tool should be async and use the `@mcp.tool()` decorator
2. **Error Handling**: Always handle subprocess errors gracefully and provide meaningful error messages
3. **Command Safety**: Validate all user inputs before passing to CLI commands
4. **Documentation**: Include clear docstrings with parameter descriptions for all tools
5. **Radicle CLI**: Use the official `rad` command-line interface for all operations

## Radicle Concepts
- **RID**: Repository ID - unique identifier for Radicle repositories
- **Patches**: Similar to pull requests in Git-based systems
- **Issues**: Bug reports and feature requests
- **Remotes**: Other nodes hosting copies of the repository
- **Sync**: Synchronizing with the Radicle network

## Reference Links
- You can find more info and examples at https://modelcontextprotocol.io/llms-full.txt
- MCP Python SDK: https://github.com/modelcontextprotocol/create-python-server
- Radicle Documentation: https://docs.radicle.xyz/
