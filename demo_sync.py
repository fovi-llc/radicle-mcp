#!/usr/bin/env python3
"""
Demo script showing GitHub ↔ Radicle synchronization functionality.
"""

import asyncio
import os
import sys
from datetime import datetime


async def demo_sync():
    """Demonstrate sync functionality."""
    print("🎯 GitHub ↔ Radicle Synchronization Demo")
    print("=" * 50)
    
    # Check environment
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not github_token:
        print("❌ Missing GITHUB_PERSONAL_ACCESS_TOKEN environment variable")
        print("📝 To set it up:")
        print("   1. Go to GitHub Settings > Developer settings > Personal access tokens")
        print("   2. Generate a new token with 'repo' and 'issues' permissions")
        print("   3. Export it: export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here")
        print("\n⚠️  Running in demo mode without actual sync...")
        
        # Show dry-run information
        print("\n🔍 What would be synced (dry-run):")
        print("  ✓ GitHub issues → Radicle issues")
        print("  ✓ Radicle issues → GitHub issues")  
        print("  ✓ GitHub PRs → Radicle patches (limited)")
        print("  ✓ Radicle patches → GitHub PRs (limited)")
        print("\n💡 Key features:")
        print("  • Idempotent operations (safe to run multiple times)")
        print("  • Mapping database tracks GitHub/Radicle ID relationships")
        print("  • Preserves original metadata and links")
        print("  • Respects existing mappings to avoid duplication")
        
        return
    
    # Test with actual sync
    try:
        from github_radicle_sync import GitHubRadicleSyncer
        
        github_repo = "fovi-llc/radicle-mcp"
        
        print(f"🚀 Testing sync with repository: {github_repo}")
        print(f"🔑 Token: {'*' * 8}...{github_token[-4:]}")
        
        syncer = GitHubRadicleSyncer(github_token, github_repo)
        
        print("\n🔍 Testing connectivity...")
        
        # Test GitHub connectivity
        github_issues = syncer.github.get_issues()
        print(f"✅ GitHub: Found {len(github_issues)} issues")
        
        github_prs = syncer.github.get_pull_requests()
        print(f"✅ GitHub: Found {len(github_prs)} pull requests")
        
        # Test Radicle connectivity
        radicle_issues = await syncer.radicle.get_issues()
        print(f"✅ Radicle: Found {len(radicle_issues)} issues")
        
        radicle_patches = await syncer.radicle.get_patches()
        print(f"✅ Radicle: Found {len(radicle_patches)} patches")
        
        # Show current mappings
        issue_mappings = len(syncer.db.data.get('issues', {}))
        patch_mappings = len(syncer.db.data.get('patches', {}))
        last_sync = syncer.db.data.get('last_sync', 'Never')
        
        print(f"\n📊 Current sync state:")
        print(f"  Issue mappings: {issue_mappings}")
        print(f"  Patch mappings: {patch_mappings}")
        print(f"  Last sync: {last_sync}")
        
        # Ask user if they want to perform actual sync
        print("\n🤔 Would you like to perform an actual sync? (y/N): ", end="")
        response = input().strip().lower()
        
        if response in ['y', 'yes']:
            print("\n🔄 Performing sync...")
            results = await syncer.sync_all()
            
            print("\n📊 Sync Results:")
            print(f"  Issues GitHub → Radicle: {results['issues_gh_to_rad']}")
            print(f"  Issues Radicle → GitHub: {results['issues_rad_to_gh']}")
            print(f"  Patches GitHub → Radicle: {results['patches_gh_to_rad']}")
            print(f"  Patches Radicle → GitHub: {results['patches_rad_to_gh']}")
            
            print(f"\n🎉 Sync completed at {datetime.now().isoformat()}")
        else:
            print("\n✅ Demo completed (no sync performed)")
        
    except ImportError:
        print("❌ github_radicle_sync module not available")
        print("Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(demo_sync())
