#!/usr/bin/env python3
"""
Summary of the Radicle + GitHub MCP setup.
"""

import json
from pathlib import Path

def show_setup_summary():
    """Display a summary of the current MCP setup."""
    
    print("🌟 RADICLE + GITHUB MCP SETUP SUMMARY")
    print("=" * 60)
    
    print("\n📦 INSTALLED SERVERS:")
    print("1. ✅ Radicle MCP Server (Python)")
    print("   - Location: src/radicle_mcp/server.py")
    print("   - Command: python -m radicle_mcp.server")
    print("   - Tools: rad_init, rad_clone, rad_sync, rad_push, rad_patch_list, etc.")
    
    print("\n2. ✅ GitHub MCP Server (Official)")
    print("   - Location: /home/vscode/.deno/bin/github-mcp")
    print("   - Command: github-mcp")
    print("   - Tools: GitHub repo management, issues, PRs, file operations")
    
    print("\n🔧 CONFIGURATION FILES:")
    print("- .vscode/mcp.json (VS Code MCP config)")
    print("- ~/.config/claude/claude_desktop_config.json (Claude Desktop)")
    
    # Show VS Code MCP config
    try:
        with open('.vscode/mcp.json', 'r') as f:
            config = json.load(f)
        print("\n📋 VS Code MCP Configuration:")
        print(json.dumps(config, indent=2))
    except FileNotFoundError:
        print("\n❌ VS Code MCP config not found")
    
    print("\n🚀 GETTING STARTED:")
    print("1. Set GitHub token: export GITHUB_PERSONAL_ACCESS_TOKEN=your_token")
    print("2. Open Claude Desktop (it will automatically load both servers)")
    print("3. Look for the MCP tools icon in Claude")
    print("4. Try commands like:")
    print("   - 'Show me my Radicle repositories'")
    print("   - 'Create a new GitHub repository'")
    print("   - 'List issues in my project'")
    
    print("\n🔗 PUBLISHING TO GITHUB:")
    print("You can now use the GitHub MCP to:")
    print("- Create a new GitHub repository")
    print("- Push your Radicle project to GitHub")
    print("- Manage issues and pull requests")
    print("- Sync between both platforms")
    
    print("\n💡 EXAMPLE WORKFLOW:")
    print("1. 'Create a GitHub repository named radicle-mcp'")
    print("2. 'Add GitHub as a remote to this repository'")
    print("3. 'Push the current code to GitHub'")
    print("4. 'Create a README issue on GitHub'")
    
    print("\n🎉 Both Radicle and GitHub are now available through MCP!")

if __name__ == "__main__":
    show_setup_summary()
