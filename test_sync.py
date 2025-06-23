#!/usr/bin/env python3
"""
Test script for GitHub ↔ Radicle synchronization with dry-run mode.
"""

import asyncio
import os
from github_radicle_sync import GitHubRadicleSyncer


async def test_sync_dry_run():
    """Test sync functionality in dry-run mode."""
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not github_token:
        print("❌ GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
        print("Please set it with: export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here")
        return 1
    
    github_repo = "fovi-llc/radicle-mcp"
    
    print("🧪 Testing GitHub ↔ Radicle synchronization (dry-run mode)")
    print(f"GitHub repo: {github_repo}")
    
    try:
        syncer = GitHubRadicleSyncer(github_token, github_repo)
        
        # Test GitHub API connectivity
        print("\n🔍 Testing GitHub API connection...")
        github_issues = syncer.github.get_issues()
        print(f"✅ Found {len(github_issues)} issues on GitHub")
        
        # Test Radicle CLI connectivity
        print("\n🔍 Testing Radicle CLI connection...")
        radicle_issues = await syncer.radicle.get_issues()
        print(f"✅ Found {len(radicle_issues)} issues in Radicle")
        
        radicle_patches = await syncer.radicle.get_patches()
        print(f"✅ Found {len(radicle_patches)} patches in Radicle")
        
        github_prs = syncer.github.get_pull_requests()
        print(f"✅ Found {len(github_prs)} pull requests on GitHub")
        
        # Display sync database status
        print(f"\n📊 Sync database status:")
        print(f"  Issue mappings: {len(syncer.db.data.get('issues', {}))}")
        print(f"  Patch mappings: {len(syncer.db.data.get('patches', {}))}")
        print(f"  Last sync: {syncer.db.data.get('last_sync', 'Never')}")
        
        print("\n✅ All connectivity tests passed!")
        print("💡 To run actual sync, use: python github_radicle_sync.py")
        
        return 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1


if __name__ == "__main__":
    exit(asyncio.run(test_sync_dry_run()))
