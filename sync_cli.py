#!/usr/bin/env python3
"""
Simple CLI wrapper for GitHub ↔ Radicle synchronization.
This can be invoked by MCP clients or used directly.
"""

import argparse
import asyncio
import os
import sys
from github_radicle_sync import GitHubRadicleSyncer


async def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Synchronize GitHub and Radicle repositories"
    )
    parser.add_argument(
        "--repo", 
        required=True,
        help="GitHub repository in format 'owner/repo'"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (or set GITHUB_PERSONAL_ACCESS_TOKEN)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without making changes"
    )
    parser.add_argument(
        "--issues-only",
        action="store_true",
        help="Sync only issues, not patches/PRs"
    )
    parser.add_argument(
        "--patches-only",
        action="store_true",
        help="Sync only patches/PRs, not issues"
    )
    
    args = parser.parse_args()
    
    # Get token from args or environment
    github_token = args.token or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not github_token:
        print("❌ GitHub token required. Set GITHUB_PERSONAL_ACCESS_TOKEN or use --token")
        return 1
    
    try:
        syncer = GitHubRadicleSyncer(github_token, args.repo)
        
        if args.dry_run:
            print("🧪 DRY RUN MODE - No changes will be made")
            # Test connectivity and show current state
            github_issues = syncer.github.get_issues()
            radicle_issues = await syncer.radicle.get_issues()
            github_prs = syncer.github.get_pull_requests()
            radicle_patches = await syncer.radicle.get_patches()
            
            print(f"\n📊 Current state:")
            print(f"  GitHub issues: {len(github_issues)}")
            print(f"  Radicle issues: {len(radicle_issues)}")
            print(f"  GitHub PRs: {len(github_prs)}")
            print(f"  Radicle patches: {len(radicle_patches)}")
            print(f"  Existing mappings: {len(syncer.db.data.get('issues', {}))} issues, {len(syncer.db.data.get('patches', {}))} patches")
            
        else:
            print(f"🚀 Starting sync for {args.repo}")
            
            results = {}
            
            if not args.patches_only:
                print("\n🔄 Syncing issues...")
                results["issues_gh_to_rad"] = await syncer.sync_issues_github_to_radicle()
                results["issues_rad_to_gh"] = await syncer.sync_issues_radicle_to_github()
            
            if not args.issues_only:
                print("\n🔄 Syncing patches/PRs...")
                results["patches_gh_to_rad"] = await syncer.sync_patches_github_to_radicle()
                results["patches_rad_to_gh"] = await syncer.sync_patches_radicle_to_github()
            
            # Update last sync time
            syncer.db.data["last_sync"] = syncer.db.data.get("last_sync", "")
            syncer.db.save_db()
            
            print("\n📊 Sync Results:")
            for key, value in results.items():
                print(f"  {key}: {value}")
            
            print("\n🎉 Synchronization complete!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
