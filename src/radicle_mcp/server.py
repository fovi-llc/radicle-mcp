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
from typing import Any, Dict, List, Optional
from pathlib import Path

from mcp.server.fastmcp import FastMCP

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


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
