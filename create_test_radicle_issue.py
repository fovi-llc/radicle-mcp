#!/usr/bin/env python3
"""
Create a test issue in Radicle to demonstrate reverse sync functionality.
"""

import asyncio
import subprocess


async def create_test_radicle_issue():
    """Create a test issue in Radicle."""
    print("🔧 Creating test issue in Radicle...")
    
    try:
        # Create a test issue using rad CLI
        process = await asyncio.create_subprocess_exec(
            "rad", "issue", "open",
            "--title", "Test Radicle Issue for GitHub Sync",
            "--description", """This is a test issue created in Radicle to demonstrate the Radicle → GitHub synchronization functionality.

**Features being tested:**
- Issue creation from Radicle
- Reverse sync to GitHub
- Metadata preservation  
- Idempotent operations

This issue should be automatically synced to GitHub when the sync process runs.

Created by: `create_test_radicle_issue.py`""",
            "--label", "test",
            "--label", "radicle-sync", 
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print(f"✅ Test issue created successfully in Radicle!")
            print(f"   Output: {stdout.decode().strip()}")
            print(f"\n💡 Now run the sync to see it appear in GitHub:")
            print(f"   python github_radicle_sync.py")
            print(f"\n🔍 You can also list Radicle issues with:")
            print(f"   rad issue list")
        else:
            print(f"❌ Failed to create Radicle issue")
            print(f"   Error: {stderr.decode().strip()}")
            
    except Exception as e:
        print(f"❌ Error creating Radicle issue: {e}")


if __name__ == "__main__":
    asyncio.run(create_test_radicle_issue())
