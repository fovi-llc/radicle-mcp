#!/usr/bin/env python3
"""Extended test script to demonstrate Radicle MCP Server capabilities."""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from radicle_mcp.server import (
    rad_help, rad_id, rad_status, rad_patch_list, 
    rad_issue_list, rad_remote_list
)


async def demo_radicle_mcp():
    """Demonstrate what we can see with Radicle through our MCP server."""
    print("🚀 Radicle MCP Server Demo")
    print("=" * 50)
    
    # Test 1: Get Radicle ID
    print("\n1. 🆔 Getting Radicle Node ID:")
    id_result = await rad_id()
    print(id_result[:200] + "..." if len(id_result) > 200 else id_result)
    
    # Test 2: Repository Status
    print("\n2. 📊 Repository Status:")
    status_result = await rad_status()
    print(status_result[:200] + "..." if len(status_result) > 200 else status_result)
    
    # Test 3: List Patches
    print("\n3. 📋 Patches:")
    patch_result = await rad_patch_list()
    print(patch_result)
    
    # Test 4: List Issues
    print("\n4. 🐛 Issues:")
    issue_result = await rad_issue_list()
    print(issue_result)
    
    # Test 5: List Remotes
    print("\n5. 🌐 Remotes:")
    remote_result = await rad_remote_list()
    print(remote_result[:300] + "..." if len(remote_result) > 300 else remote_result)
    
    print("\n🎉 Demo complete! The MCP server can successfully wrap Radicle CLI commands.")


if __name__ == "__main__":
    asyncio.run(demo_radicle_mcp())
