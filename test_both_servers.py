#!/usr/bin/env python3
"""
Test script to verify both Radicle and GitHub MCP servers are working.
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path

# Add the src directory to the path for Radicle MCP
sys.path.insert(0, str(Path(__file__).parent / "src"))

from radicle_mcp.server import rad_help, rad_id

async def test_radicle_mcp():
    """Test the Radicle MCP server."""
    print("🧪 Testing Radicle MCP Server...")
    try:
        # Test help command
        help_result = await rad_help()
        if "Radicle command line interface" in help_result:
            print("✅ Radicle MCP Server: WORKING")
            return True
        else:
            print("❌ Radicle MCP Server: Help command failed")
            return False
    except Exception as e:
        print(f"❌ Radicle MCP Server: Error - {e}")
        return False

def test_github_mcp():
    """Test the GitHub MCP server."""
    print("🧪 Testing GitHub MCP Server...")
    try:
        # Try to start the GitHub MCP server briefly
        result = subprocess.run(
            ["timeout", "2", "/home/vscode/.deno/bin/github-mcp"],
            capture_output=True,
            text=True,
            timeout=3
        )
        
        # The server should start and run (timeout is expected)
        if "GitHub MCP Server running on stdio" in result.stderr or result.returncode == 124:
            print("✅ GitHub MCP Server: WORKING")
            return True
        else:
            print(f"❌ GitHub MCP Server: Unexpected output - {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✅ GitHub MCP Server: WORKING (started successfully)")
        return True
    except FileNotFoundError:
        print("❌ GitHub MCP Server: Not found - please install with Deno")
        return False
    except Exception as e:
        print(f"❌ GitHub MCP Server: Error - {e}")
        return False

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking Prerequisites...")
    
    issues = []
    
    # Check if Deno is installed
    try:
        subprocess.run(["deno", "--version"], capture_output=True, check=True)
        print("✅ Deno: Installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        issues.append("❌ Deno: Not installed or not in PATH")
    
    # Check if rad is available
    try:
        subprocess.run(["rad", "--version"], capture_output=True, check=True)
        print("✅ Radicle CLI: Installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        issues.append("❌ Radicle CLI: Not installed or not in PATH")
    
    # Check if GitHub token is set (optional but recommended)
    if os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        print("✅ GitHub Token: Set")
    else:
        issues.append("⚠️  GitHub Token: Not set (GitHub MCP will have limited functionality)")
    
    return issues

async def main():
    """Main test function."""
    print("🚀 Testing Radicle + GitHub MCP Setup")
    print("=" * 50)
    
    # Check prerequisites
    issues = check_prerequisites()
    if issues:
        print("\n⚠️  Issues found:")
        for issue in issues:
            print(f"  {issue}")
        print()
    
    # Test both servers
    radicle_ok = await test_radicle_mcp()
    github_ok = test_github_mcp()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"Radicle MCP Server: {'✅ PASS' if radicle_ok else '❌ FAIL'}")
    print(f"GitHub MCP Server:  {'✅ PASS' if github_ok else '❌ FAIL'}")
    
    if radicle_ok and github_ok:
        print("\n🎉 SUCCESS! Both MCP servers are ready to use.")
        print("\n💡 Next steps:")
        print("   1. Set GITHUB_PERSONAL_ACCESS_TOKEN if not already set")
        print("   2. Connect to Claude Desktop or another MCP client")
        print("   3. Start using natural language commands!")
        return 0
    else:
        print("\n❌ Some servers failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    exit(asyncio.run(main()))
