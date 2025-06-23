#!/usr/bin/env python3
"""
Create a test issue to demonstrate sync functionality.
"""

import asyncio
import os
from github_radicle_sync import GitHubAPI


async def create_test_issue():
    """Create a test issue on GitHub."""
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not github_token:
        print("❌ GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
        return
    
    github_repo = "fovi-llc/radicle-mcp"
    
    github_api = GitHubAPI(github_token, github_repo)
    
    print(f"🔧 Creating test issue in {github_repo}...")
    
    try:
        test_issue = github_api.create_issue(
            title="Test Issue for GitHub ↔ Radicle Sync",
            body="""This is a test issue created to demonstrate the GitHub ↔ Radicle synchronization functionality.

**Features being tested:**
- Issue creation and sync
- Metadata preservation  
- Idempotent operations
- Mapping database

This issue should be automatically synced to Radicle when the sync process runs.

Created by: `create_test_issue.py`""",
            labels=["test", "sync", "demo"]
        )
        
        print(f"✅ Test issue created successfully!")
        print(f"   Issue #{test_issue['number']}: {test_issue['title']}")
        print(f"   URL: {test_issue['html_url']}")
        print(f"\n💡 Now run the sync to see it appear in Radicle:")
        print(f"   python github_radicle_sync.py")
        
    except Exception as e:
        print(f"❌ Failed to create test issue: {e}")


if __name__ == "__main__":
    asyncio.run(create_test_issue())
