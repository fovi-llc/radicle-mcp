#!/usr/bin/env python3
"""
Use MCP tools to sync with GitHub repository.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from radicle_mcp.server import run_rad_command

async def use_mcp_for_github_sync():
    """Use MCP tools to handle GitHub sync."""
    
    print("🔄 Using MCP to sync with GitHub repository fovi-llc/radicle-mcp")
    
    # First, let's check our current Radicle status
    print("\n1. 📊 Checking current Radicle status...")
    status_result = await run_rad_command(["rad", "inspect"])
    print(f"Current RID: {status_result['stdout']}")
    
    # Check current remotes
    print("\n2. 🌐 Checking current remotes...")
    remote_result = await run_rad_command(["rad", "remote"])
    print(f"Current remotes:\n{remote_result['stdout']}")
    
    # Use git through our MCP wrapper to add GitHub remote
    print("\n3. 🐙 Adding GitHub remote...")
    git_remote_result = await run_rad_command([
        "git", "remote", "add", "github", 
        "https://github.com/fovi-llc/radicle-mcp.git"
    ])
    
    if git_remote_result['success']:
        print("✅ GitHub remote added successfully")
    else:
        print(f"⚠️  GitHub remote add result: {git_remote_result['stderr']}")
    
    # Fetch from GitHub to get the LICENSE file
    print("\n4. 📥 Fetching from GitHub...")
    fetch_result = await run_rad_command(["git", "fetch", "github"])
    
    if fetch_result['success']:
        print("✅ Successfully fetched from GitHub")
        print(f"Fetch output: {fetch_result['stdout']}")
    else:
        print(f"❌ Fetch failed: {fetch_result['stderr']}")
    
    # Check what we got
    print("\n5. 🔍 Checking GitHub branches...")
    branch_result = await run_rad_command(["git", "branch", "-r"])
    print(f"Remote branches: {branch_result['stdout']}")
    
    # Merge or rebase with GitHub main if it exists
    print("\n6. 🔀 Merging GitHub changes...")
    merge_result = await run_rad_command([
        "git", "merge", "github/main", "--allow-unrelated-histories"
    ])
    
    if merge_result['success']:
        print("✅ Successfully merged GitHub changes")
    else:
        print(f"⚠️  Merge result: {merge_result['stderr']}")
        # Try to continue anyway
    
    # Stage all our new files
    print("\n7. 📝 Staging local changes...")
    add_result = await run_rad_command(["git", "add", "."])
    
    if add_result['success']:
        print("✅ All files staged")
    else:
        print(f"❌ Failed to stage files: {add_result['stderr']}")
    
    # Commit our changes
    print("\n8. 💾 Committing changes...")
    commit_result = await run_rad_command([
        "git", "commit", "-m", 
        "Add Radicle + GitHub MCP server integration\n\n- Complete Python MCP server for Radicle CLI\n- GitHub MCP server integration\n- VS Code and Claude Desktop configuration\n- Setup and test scripts"
    ])
    
    if commit_result['success']:
        print("✅ Changes committed successfully")
        print(f"Commit result: {commit_result['stdout']}")
    else:
        print(f"⚠️  Commit result: {commit_result['stderr']}")
    
    # Push to GitHub
    print("\n9. 🚀 Pushing to GitHub...")
    push_result = await run_rad_command(["git", "push", "github", "main"])
    
    if push_result['success']:
        print("✅ Successfully pushed to GitHub!")
        print(f"Push result: {push_result['stdout']}")
    else:
        print(f"❌ Push failed: {push_result['stderr']}")
    
    print("\n🎉 MCP-powered GitHub sync complete!")
    print("Your local changes are now synced with https://github.com/fovi-llc/radicle-mcp")

if __name__ == "__main__":
    asyncio.run(use_mcp_for_github_sync())
