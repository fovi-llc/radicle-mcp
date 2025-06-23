#!/usr/bin/env python3
"""
Radicle MCP Server

A Model Context Protocol server that provides tools for interacting with Radicle,
a peer-to-peer code collaboration network.
"""

import asyncio
import subprocess
import json
import logging
import sys
import os
from typing import Any, Dict, List, Optional
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Import our sync functionality
try:
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from github_radicle_sync import GitHubRadicleSyncer
    SYNC_AVAILABLE = True
except ImportError:
    SYNC_AVAILABLE = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("radicle-mcp")

# Initialize the MCP server
mcp = FastMCP("Radicle MCP Server")


async def run_rad_command(command: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
    """
    Run a rad command and return the result.
    
    Args:
        command: List of command arguments starting with 'rad'
        cwd: Working directory to run the command in
        
    Returns:
        Dictionary with stdout, stderr, and return_code
    """
    try:
        # Ensure command starts with 'rad'
        if not command or command[0] != "rad":
            command = ["rad"] + command
            
        logger.info(f"Running command: {' '.join(command)}")
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        
        stdout, stderr = await process.communicate()
        
        return {
            "stdout": stdout.decode("utf-8").strip(),
            "stderr": stderr.decode("utf-8").strip(),
            "return_code": process.returncode,
            "success": process.returncode == 0
        }
        
    except FileNotFoundError:
        return {
            "stdout": "",
            "stderr": "rad command not found. Please ensure Radicle is installed.",
            "return_code": 127,
            "success": False
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error running command: {str(e)}",
            "return_code": 1,
            "success": False
        }


@mcp.tool()
async def rad_init(name: str, description: str = "", public: bool = True) -> str:
    """
    Initialize a new Radicle repository.
    
    Args:
        name: Name of the repository
        description: Description of the repository
        public: Whether the repository should be public (default: True)
    """
    command = ["rad", "init", "--name", name]
    
    if description:
        command.extend(["--description", description])
    
    if public:
        command.append("--public")
    else:
        command.append("--private")
    
    result = await run_rad_command(command)
    
    if result["success"]:
        return f"✅ Successfully initialized Radicle repository '{name}'\n{result['stdout']}"
    else:
        return f"❌ Failed to initialize repository: {result['stderr']}"


@mcp.tool()
async def rad_clone(rid: str, path: Optional[str] = None) -> str:
    """
    Clone a Radicle repository.
    
    Args:
        rid: Repository ID (RID) to clone
        path: Optional path where to clone the repository
    """
    command = ["rad", "clone", rid]
    
    if path:
        command.append(path)
    
    result = await run_rad_command(command)
    
    if result["success"]:
        return f"✅ Successfully cloned repository {rid}\n{result['stdout']}"
    else:
        return f"❌ Failed to clone repository: {result['stderr']}"


@mcp.tool()
async def rad_sync(repository_path: str = ".") -> str:
    """
    Sync a Radicle repository with the network.
    
    Args:
        repository_path: Path to the repository (default: current directory)
    """
    result = await run_rad_command(["rad", "sync"], cwd=repository_path)
    
    if result["success"]:
        return f"✅ Successfully synced repository\n{result['stdout']}"
    else:
        return f"❌ Failed to sync repository: {result['stderr']}"


@mcp.tool()
async def rad_push(repository_path: str = ".") -> str:
    """
    Push changes to the Radicle network.
    
    Args:
        repository_path: Path to the repository (default: current directory)
    """
    result = await run_rad_command(["rad", "push"], cwd=repository_path)
    
    if result["success"]:
        return f"✅ Successfully pushed changes\n{result['stdout']}"
    else:
        return f"❌ Failed to push changes: {result['stderr']}"


@mcp.tool()
async def rad_patch_list(repository_path: str = ".") -> str:
    """
    List patches in a Radicle repository.
    
    Args:
        repository_path: Path to the repository (default: current directory)
    """
    result = await run_rad_command(["rad", "patch", "list"], cwd=repository_path)
    
    if result["success"]:
        if result["stdout"]:
            return f"📋 Patches in repository:\n{result['stdout']}"
        else:
            return "📋 No patches found in repository"
    else:
        return f"❌ Failed to list patches: {result['stderr']}"


@mcp.tool()
async def rad_issue_list(repository_path: str = ".") -> str:
    """
    List issues in a Radicle repository.
    
    Args:
        repository_path: Path to the repository (default: current directory)
    """
    result = await run_rad_command(["rad", "issue", "list"], cwd=repository_path)
    
    if result["success"]:
        if result["stdout"]:
            return f"🐛 Issues in repository:\n{result['stdout']}"
        else:
            return "🐛 No issues found in repository"
    else:
        return f"❌ Failed to list issues: {result['stderr']}"


@mcp.tool()
async def rad_id() -> str:
    """
    Get the current node's Radicle ID.
    """
    result = await run_rad_command(["rad", "self"])
    
    if result["success"]:
        return f"🆔 Your Radicle ID:\n{result['stdout']}"
    else:
        return f"❌ Failed to get Radicle ID: {result['stderr']}"


@mcp.tool()
async def rad_status(repository_path: str = ".") -> str:
    """
    Get the status of a Radicle repository.
    
    Args:
        repository_path: Path to the repository (default: current directory)
    """
    result = await run_rad_command(["rad", "inspect"], cwd=repository_path)
    
    if result["success"]:
        return f"📊 Repository status:\n{result['stdout']}"
    else:
        return f"❌ Failed to get repository status: {result['stderr']}"


@mcp.tool()
async def rad_remote_list(repository_path: str = ".") -> str:
    """
    List remotes in a Radicle repository.
    
    Args:
        repository_path: Path to the repository (default: current directory)
    """
    result = await run_rad_command(["rad", "remote"], cwd=repository_path)
    
    if result["success"]:
        if result["stdout"]:
            return f"🌐 Remotes in repository:\n{result['stdout']}"
        else:
            return "🌐 No remotes found in repository"
    else:
        return f"❌ Failed to list remotes: {result['stderr']}"


@mcp.tool()
async def rad_help(command: Optional[str] = None) -> str:
    """
    Get help for Radicle commands.
    
    Args:
        command: Specific command to get help for (optional)
    """
    if command:
        result = await run_rad_command(["rad", command, "--help"])
    else:
        result = await run_rad_command(["rad", "--help"])
    
    if result["success"]:
        return f"📖 Radicle Help:\n{result['stdout']}"
    else:
        return f"❌ Failed to get help: {result['stderr']}"


# GitHub Sync Tools (if available)
if SYNC_AVAILABLE:
    @mcp.tool()
    async def github_sync_test(github_repo: str, github_token: Optional[str] = None) -> str:
        """
        Test GitHub ↔ Radicle sync connectivity.
        
        Args:
            github_repo: GitHub repository in format 'owner/repo'
            github_token: GitHub personal access token (or set GITHUB_PERSONAL_ACCESS_TOKEN env var)
        """
        try:
            token = github_token or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
            if not token:
                return "❌ GitHub token required. Set GITHUB_PERSONAL_ACCESS_TOKEN or provide github_token parameter"
            
            syncer = GitHubRadicleSyncer(token, github_repo)
            
            # Test connectivity
            github_issues = syncer.github.get_issues()
            radicle_issues = await syncer.radicle.get_issues()
            github_prs = syncer.github.get_pull_requests()
            radicle_patches = await syncer.radicle.get_patches()
            
            result = f"✅ GitHub ↔ Radicle sync connectivity test successful!\n\n"
            result += f"📊 Current state:\n"
            result += f"  GitHub issues: {len(github_issues)}\n"
            result += f"  Radicle issues: {len(radicle_issues)}\n"
            result += f"  GitHub PRs: {len(github_prs)}\n"
            result += f"  Radicle patches: {len(radicle_patches)}\n"
            result += f"  Existing mappings: {len(syncer.db.data.get('issues', {}))} issues, {len(syncer.db.data.get('patches', {}))} patches\n"
            result += f"  Last sync: {syncer.db.data.get('last_sync', 'Never')}"
            
            return result
            
        except Exception as e:
            return f"❌ Sync test failed: {str(e)}"

    @mcp.tool()
    async def github_sync_issues(github_repo: str, github_token: Optional[str] = None, direction: str = "both") -> str:
        """
        Synchronize issues between GitHub and Radicle.
        
        Args:
            github_repo: GitHub repository in format 'owner/repo'
            github_token: GitHub personal access token (or set GITHUB_PERSONAL_ACCESS_TOKEN env var)
            direction: Sync direction - 'both', 'github-to-radicle', or 'radicle-to-github'
        """
        try:
            token = github_token or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
            if not token:
                return "❌ GitHub token required. Set GITHUB_PERSONAL_ACCESS_TOKEN or provide github_token parameter"
            
            syncer = GitHubRadicleSyncer(token, github_repo)
            
            results = {}
            
            if direction in ["both", "github-to-radicle"]:
                results["github_to_radicle"] = await syncer.sync_issues_github_to_radicle()
            
            if direction in ["both", "radicle-to-github"]:
                results["radicle_to_github"] = await syncer.sync_issues_radicle_to_github()
            
            syncer.db.data["last_sync"] = syncer.db.data.get("last_sync", "")
            syncer.db.save_db()
            
            result = f"✅ Issue synchronization complete!\n\n"
            result += f"📊 Results:\n"
            for key, value in results.items():
                result += f"  {key}: {value}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Issue sync failed: {str(e)}"

    @mcp.tool()
    async def github_sync_full(github_repo: str, github_token: Optional[str] = None) -> str:
        """
        Perform full bidirectional sync between GitHub and Radicle (issues and patches).
        
        Args:
            github_repo: GitHub repository in format 'owner/repo'
            github_token: GitHub personal access token (or set GITHUB_PERSONAL_ACCESS_TOKEN env var)
        """
        try:
            token = github_token or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
            if not token:
                return "❌ GitHub token required. Set GITHUB_PERSONAL_ACCESS_TOKEN or provide github_token parameter"
            
            syncer = GitHubRadicleSyncer(token, github_repo)
            results = await syncer.sync_all()
            
            result = f"✅ Full synchronization complete!\n\n"
            result += f"📊 Results:\n"
            result += f"  Issues GitHub → Radicle: {results['issues_gh_to_rad']}\n"
            result += f"  Issues Radicle → GitHub: {results['issues_rad_to_gh']}\n"
            result += f"  Patches GitHub → Radicle: {results['patches_gh_to_rad']}\n"
            result += f"  Patches Radicle → GitHub: {results['patches_rad_to_gh']}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Full sync failed: {str(e)}"

else:
    @mcp.tool()
    async def github_sync_unavailable() -> str:
        """
        GitHub sync functionality is not available.
        """
        return "❌ GitHub sync functionality not available. Please ensure the github_radicle_sync module is properly installed."


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
