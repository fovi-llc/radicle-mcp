#!/usr/bin/env python3
"""
Setup script for Radicle + GitHub MCP servers.

This script helps you configure both MCP servers for use with Claude Desktop
or other MCP clients.
"""

import json
import os
from pathlib import Path

def create_claude_config():
    """Create a Claude Desktop configuration file."""
    
    # Determine the Claude config path based on OS
    home = Path.home()
    if os.name == 'nt':  # Windows
        config_path = home / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    elif os.uname().sysname == 'Darwin':  # macOS
        config_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        config_path = home / ".config" / "claude" / "claude_desktop_config.json"
    
    # Current project paths
    current_dir = Path(__file__).parent
    python_path = current_dir / ".venv" / "bin" / "python"
    github_mcp_path = Path("/home/vscode/.deno/bin/github-mcp")
    
    # Create the configuration
    config = {
        "mcpServers": {
            "radicle-mcp": {
                "command": str(python_path),
                "args": ["-m", "radicle_mcp.server"]
            },
            "github-mcp": {
                "command": str(github_mcp_path),
                "args": [],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
                }
            }
        }
    }
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created Claude Desktop config at: {config_path}")
    return config_path

def print_setup_instructions():
    """Print setup instructions for the user."""
    print("\n" + "="*60)
    print("🚀 RADICLE + GITHUB MCP SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 NEXT STEPS:")
    print("\n1. 🔑 Set up GitHub Personal Access Token:")
    print("   - Go to https://github.com/settings/tokens")
    print("   - Create a new token with repo, issues, and pull request permissions")
    print("   - Set the environment variable:")
    print("     export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here")
    
    print("\n2. 🖥️  For Claude Desktop:")
    print("   - Restart Claude Desktop")
    print("   - Look for the MCP tools icon in the interface")
    print("   - You should see tools from both Radicle and GitHub servers")
    
    print("\n3. 🧪 Test the servers:")
    print("   - Radicle: 'Show me my Radicle repositories'")
    print("   - GitHub: 'List my GitHub repositories'")
    
    print("\n4. 🌐 Available Tools:")
    print("   Radicle MCP:")
    print("   - rad_init, rad_clone, rad_sync, rad_push")
    print("   - rad_patch_list, rad_issue_list, rad_status")
    print("   - rad_id, rad_remote_list, rad_help")
    print("\n   GitHub MCP:")
    print("   - Repository management, issues, pull requests")
    print("   - File operations, search, user management")
    
    print("\n🎉 You can now use AI assistants to work with both Radicle and GitHub!")

def main():
    """Main setup function."""
    print("🔧 Setting up Radicle + GitHub MCP servers...")
    
    try:
        config_path = create_claude_config()
        print_setup_instructions()
        
        print(f"\n📄 Configuration written to: {config_path}")
        print("\n💡 Tip: You can manually edit this file to customize the setup.")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
