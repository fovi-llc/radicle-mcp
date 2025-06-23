#!/usr/bin/env python3
"""Test script for Radicle MCP Server."""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from radicle_mcp.server import rad_help


async def test_server():
    """Simple test to verify the server tools work."""
    print("🧪 Testing Radicle MCP Server...")
    
    # Test the help function
    try:
        help_result = await rad_help()
        print("✅ Help command test passed")
        print(f"📖 Result preview: {help_result[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Help command test failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_server())
    if success:
        print("🎉 Radicle MCP Server is ready!")
    else:
        print("⚠️  Server tests failed - check Radicle installation")
        sys.exit(1)
