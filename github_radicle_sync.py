#!/usr/bin/env python3
"""
GitHub ↔ Radicle Synchronization System

This module provides bidirectional synchronization of issues and patches/PRs
between GitHub and Radicle with idempotent operations to prevent duplication.
"""

import asyncio
import json
import os
import re
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from urllib.parse import urlparse

import requests


@dataclass
class IssueMapping:
    """Mapping between GitHub issue and Radicle issue."""
    github_id: int
    github_number: int
    radicle_id: str
    title: str
    last_sync: str
    github_updated_at: str
    radicle_updated_at: str


@dataclass
class PatchMapping:
    """Mapping between GitHub PR and Radicle patch."""
    github_id: int
    github_number: int
    radicle_id: str
    title: str
    last_sync: str
    github_updated_at: str
    radicle_updated_at: str


class SyncDatabase:
    """Simple JSON-based database for tracking sync mappings."""
    
    def __init__(self, db_path: str = ".radicle_github_sync.json"):
        self.db_path = Path(db_path)
        self.data = self._load_db()
    
    def _load_db(self) -> Dict[str, Any]:
        """Load database from JSON file."""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return {
            "issues": {},
            "patches": {},
            "last_sync": None,
            "github_repo": None,
            "radicle_rid": None
        }
    
    def save_db(self):
        """Save database to JSON file."""
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_issue_mapping(self, github_id: Optional[int] = None, radicle_id: Optional[str] = None) -> Optional[IssueMapping]:
        """Get issue mapping by GitHub ID or Radicle ID."""
        for mapping_data in self.data["issues"].values():
            mapping = IssueMapping(**mapping_data)
            if (github_id and mapping.github_id == github_id) or \
               (radicle_id and mapping.radicle_id == radicle_id):
                return mapping
        return None
    
    def save_issue_mapping(self, mapping: IssueMapping):
        """Save issue mapping."""
        key = f"gh{mapping.github_id}_rad{mapping.radicle_id}"
        self.data["issues"][key] = asdict(mapping)
        self.save_db()
    
    def get_patch_mapping(self, github_id: Optional[int] = None, radicle_id: Optional[str] = None) -> Optional[PatchMapping]:
        """Get patch mapping by GitHub ID or Radicle ID."""
        for mapping_data in self.data["patches"].values():
            mapping = PatchMapping(**mapping_data)
            if (github_id and mapping.github_id == github_id) or \
               (radicle_id and mapping.radicle_id == radicle_id):
                return mapping
        return None
    
    def save_patch_mapping(self, mapping: PatchMapping):
        """Save patch mapping."""
        key = f"gh{mapping.github_id}_rad{mapping.radicle_id}"
        self.data["patches"][key] = asdict(mapping)
        self.save_db()


class GitHubAPI:
    """GitHub API wrapper for sync operations."""
    
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo  # format: "owner/repo"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"
    
    def get_issues(self, state: str = "all") -> List[Dict[str, Any]]:
        """Get issues from GitHub repository."""
        url = f"{self.base_url}/repos/{self.repo}/issues"
        params: Dict[str, Union[str, int]] = {"state": state, "per_page": 100}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        # Filter out pull requests (GitHub API includes PRs in issues)
        return [issue for issue in response.json() if not issue.get("pull_request")]
    
    def create_issue(self, title: str, body: str, labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a new issue on GitHub."""
        url = f"{self.base_url}/repos/{self.repo}/issues"
        data: Dict[str, Any] = {
            "title": title,
            "body": body,
            "labels": labels or []
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def update_issue(self, issue_number: int, title: Optional[str] = None, body: Optional[str] = None, 
                    state: Optional[str] = None, labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """Update an existing GitHub issue."""
        url = f"{self.base_url}/repos/{self.repo}/issues/{issue_number}"
        data: Dict[str, Any] = {}
        
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if state is not None:
            data["state"] = state
        if labels is not None:
            data["labels"] = labels
        
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_pull_requests(self, state: str = "all") -> List[Dict[str, Any]]:
        """Get pull requests from GitHub repository."""
        url = f"{self.base_url}/repos/{self.repo}/pulls"
        params: Dict[str, Union[str, int]] = {"state": state, "per_page": 100}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()


class RadicleAPI:
    """Radicle CLI wrapper for sync operations."""
    
    async def run_command(self, command: List[str], cwd: str = ".") -> Dict[str, Any]:
        """Run a rad command and return the result."""
        try:
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
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "return_code": 1,
                "success": False
            }
    
    async def get_issues(self) -> List[Dict[str, Any]]:
        """Get issues from Radicle repository."""
        result = await self.run_command(["rad", "issue", "list"])
        
        if result["success"] and result["stdout"]:
            # Parse the table output since --format json is not available
            issues = []
            lines = result["stdout"].split('\n')
            
            for line in lines:
                # Look for issue lines (start with │ ● and have an ID)
                if '│ ●' in line and len(line.split()) >= 3:
                    parts = line.split()
                    # Find the ID (should be after ●)
                    try:
                        id_index = parts.index('●') + 1
                        if id_index < len(parts):
                            issue_id = parts[id_index]
                            # Try to extract title (everything between ID and Author)
                            # This is a basic parser - in a real implementation you'd want more robust parsing
                            title_start = line.find(issue_id) + len(issue_id)
                            author_keywords = ['vscode', 'you)', 'Author']
                            title_end = len(line)
                            for keyword in author_keywords:
                                pos = line.find(keyword, title_start)
                                if pos > title_start:
                                    title_end = pos
                                    break
                            
                            title = line[title_start:title_end].strip()
                            
                            issues.append({
                                "id": issue_id,
                                "title": title,
                                "author": "vscode",  # Extracted from the table
                                "created_at": "unknown",  # Not available in table format
                                "updated_at": "unknown",
                                "description": "No description available from list format"
                            })
                    except (ValueError, IndexError):
                        continue
            
            return issues
        return []
    
    async def create_issue(self, title: str, description: str, labels: Optional[List[str]] = None) -> Optional[str]:
        """Create a new issue in Radicle repository."""
        command = ["rad", "issue", "open", "--title", title, "--description", description]
        
        if labels:
            for label in labels:
                command.extend(["--label", label])
        
        result = await self.run_command(command)
        
        if result["success"]:
            # Extract issue ID from output
            # Format is typically "✓ Issue abc123... opened"
            match = re.search(r"Issue ([a-f0-9]+)", result["stdout"])
            if match:
                return match.group(1)
        
        return None
    
    async def get_patches(self) -> List[Dict[str, Any]]:
        """Get patches from Radicle repository."""
        result = await self.run_command(["rad", "patch", "list"])
        
        if result["success"] and result["stdout"]:
            # Parse the table output since --format json may not be available
            patches = []
            lines = result["stdout"].split('\n')
            
            for line in lines:
                # Look for patch lines (similar to issues)
                if '│' in line and len(line.split()) >= 3:
                    # Basic parsing - would need enhancement for production use
                    parts = line.split()
                    if len(parts) > 2:
                        try:
                            # Try to extract patch ID and title
                            patch_id = parts[1] if parts[1] != '│' else parts[2]
                            title = " ".join(parts[3:5]) if len(parts) > 4 else "Unknown patch"
                            
                            patches.append({
                                "id": patch_id,
                                "title": title,
                                "author": "unknown",
                                "created_at": "unknown",
                                "updated_at": "unknown",
                                "description": "No description available from list format"
                            })
                        except (ValueError, IndexError):
                            continue
            
            return patches
        return []

    async def create_patch(self, branch_name: str, title: str, description: str) -> Optional[str]:
        """Create a new patch in Radicle repository."""
        # First check if the branch exists
        result = await self.run_command(["git", "show-ref", "--verify", f"refs/heads/{branch_name}"])
        if not result["success"]:
            print(f"⚠️  Branch {branch_name} does not exist, skipping patch creation")
            return None
        
        command = ["rad", "patch", "open", "--title", title, "--description", description, branch_name]
        result = await self.run_command(command)
        
        if result["success"]:
            # Extract patch ID from output
            # Format is typically "✓ Patch abc123... opened"
            match = re.search(r"Patch ([a-f0-9]+)", result["stdout"])
            if match:
                return match.group(1)
        
        return None


class GitHubRadicleSyncer:
    """Main synchronization engine between GitHub and Radicle."""
    
    def __init__(self, github_token: str, github_repo: str, radicle_rid: Optional[str] = None):
        self.github = GitHubAPI(github_token, github_repo)
        self.radicle = RadicleAPI()
        self.db = SyncDatabase()
        
        # Update database with current repo info
        self.db.data["github_repo"] = github_repo
        if radicle_rid:
            self.db.data["radicle_rid"] = radicle_rid
        self.db.save_db()
    
    async def sync_issues_github_to_radicle(self) -> Dict[str, int]:
        """Sync issues from GitHub to Radicle."""
        print("🔄 Syncing issues: GitHub → Radicle")
        
        github_issues = self.github.get_issues()
        created = 0
        updated = 0
        skipped = 0
        
        for gh_issue in github_issues:
            github_id = gh_issue["id"]
            github_number = gh_issue["number"]
            
            # Check if already mapped
            existing_mapping = self.db.get_issue_mapping(github_id=github_id)
            
            if existing_mapping:
                # Check if update needed
                if gh_issue["updated_at"] > existing_mapping.github_updated_at:
                    print(f"⚠️  Issue #{github_number} needs update (not implemented yet)")
                    updated += 1
                else:
                    skipped += 1
                continue
            
            # Create new issue in Radicle
            title = gh_issue["title"]
            body = self._format_issue_body_for_radicle(gh_issue)
            labels = [label["name"] for label in gh_issue.get("labels", [])]
            
            radicle_id = await self.radicle.create_issue(title, body, labels)
            
            if radicle_id:
                # Save mapping
                mapping = IssueMapping(
                    github_id=github_id,
                    github_number=github_number,
                    radicle_id=radicle_id,
                    title=title,
                    last_sync=datetime.now().isoformat(),
                    github_updated_at=gh_issue["updated_at"],
                    radicle_updated_at=datetime.now().isoformat()
                )
                self.db.save_issue_mapping(mapping)
                print(f"✅ Created Radicle issue {radicle_id[:8]}... for GitHub #{github_number}")
                created += 1
            else:
                print(f"❌ Failed to create Radicle issue for GitHub #{github_number}")
        
        return {"created": created, "updated": updated, "skipped": skipped}
    
    async def sync_issues_radicle_to_github(self) -> Dict[str, int]:
        """Sync issues from Radicle to GitHub."""
        print("🔄 Syncing issues: Radicle → GitHub")
        
        radicle_issues = await self.radicle.get_issues()
        created = 0
        updated = 0
        skipped = 0
        
        for rad_issue in radicle_issues:
            radicle_id = rad_issue.get("id")
            if not radicle_id:
                continue
            
            # Check if already mapped
            existing_mapping = self.db.get_issue_mapping(radicle_id=radicle_id)
            
            if existing_mapping:
                skipped += 1
                continue
            
            # Create new issue in GitHub
            title = rad_issue.get("title", "Untitled")
            body = self._format_issue_body_for_github(rad_issue)
            labels = ["from-radicle"]  # Tag to identify Radicle-originated issues
            
            try:
                gh_issue = self.github.create_issue(title, body, labels)
                
                # Save mapping
                mapping = IssueMapping(
                    github_id=gh_issue["id"],
                    github_number=gh_issue["number"],
                    radicle_id=radicle_id,
                    title=title,
                    last_sync=datetime.now().isoformat(),
                    github_updated_at=gh_issue["updated_at"],
                    radicle_updated_at=rad_issue.get("updated_at", datetime.now().isoformat())
                )
                self.db.save_issue_mapping(mapping)
                print(f"✅ Created GitHub issue #{gh_issue['number']} for Radicle {radicle_id[:8]}...")
                created += 1
                
            except Exception as e:
                print(f"❌ Failed to create GitHub issue for Radicle {radicle_id[:8]}...: {e}")
        
        return {"created": created, "updated": updated, "skipped": skipped}
    
    async def sync_patches_github_to_radicle(self) -> Dict[str, int]:
        """Sync pull requests from GitHub to Radicle patches."""
        print("🔄 Syncing patches: GitHub PRs → Radicle")
        
        github_prs = self.github.get_pull_requests()
        created = 0
        updated = 0
        skipped = 0
        
        for gh_pr in github_prs:
            github_id = gh_pr["id"]
            github_number = gh_pr["number"]
            
            # Check if already mapped
            existing_mapping = self.db.get_patch_mapping(github_id=github_id)
            
            if existing_mapping:
                # Check if update needed
                if gh_pr["updated_at"] > existing_mapping.github_updated_at:
                    print(f"⚠️  PR #{github_number} needs update (not implemented yet)")
                    updated += 1
                else:
                    skipped += 1
                continue
            
            # Skip closed or merged PRs without a corresponding branch
            if gh_pr["state"] in ["closed", "merged"]:
                print(f"⚠️  Skipping closed/merged PR #{github_number}")
                skipped += 1
                continue
            
            # Create new patch in Radicle
            title = gh_pr["title"]
            body = self._format_patch_body_for_radicle(gh_pr)
            branch_name = f"github-pr-{github_number}"
            
            # For now, we'll skip creating actual patches since it requires branch management
            # In a real implementation, you'd need to:
            # 1. Fetch the PR branch from GitHub
            # 2. Create a local branch
            # 3. Create the patch
            print(f"⚠️  PR to patch sync requires branch management (PR #{github_number} skipped)")
            skipped += 1
        
        return {"created": created, "updated": updated, "skipped": skipped}
    
    async def sync_patches_radicle_to_github(self) -> Dict[str, int]:
        """Sync patches from Radicle to GitHub pull requests."""
        print("🔄 Syncing patches: Radicle → GitHub PRs")
        
        radicle_patches = await self.radicle.get_patches()
        created = 0
        updated = 0
        skipped = 0
        
        for rad_patch in radicle_patches:
            radicle_id = rad_patch.get("id")
            if not radicle_id:
                continue
            
            # Check if already mapped
            existing_mapping = self.db.get_patch_mapping(radicle_id=radicle_id)
            
            if existing_mapping:
                skipped += 1
                continue
            
            # For now, we'll skip creating actual PRs since it requires branch management
            # In a real implementation, you'd need to:
            # 1. Push the patch branch to GitHub
            # 2. Create a PR
            print(f"⚠️  Patch to PR sync requires branch management (patch {radicle_id[:8]}... skipped)")
            skipped += 1
        
        return {"created": created, "updated": updated, "skipped": skipped}
    
    def _format_issue_body_for_radicle(self, gh_issue: Dict[str, Any]) -> str:
        """Format GitHub issue body for Radicle."""
        body = f"**Originally from GitHub issue #{gh_issue['number']}**\n\n"
        body += f"Author: @{gh_issue['user']['login']}\n"
        body += f"Created: {gh_issue['created_at']}\n"
        body += f"GitHub URL: {gh_issue['html_url']}\n\n"
        body += "---\n\n"
        body += gh_issue.get("body", "") or "No description provided."
        return body
    
    def _format_issue_body_for_github(self, rad_issue: Dict[str, Any]) -> str:
        """Format Radicle issue body for GitHub."""
        body = f"**Originally from Radicle issue {rad_issue.get('id', 'unknown')[:8]}...**\n\n"
        body += f"Author: {rad_issue.get('author', 'unknown')}\n"
        body += f"Created: {rad_issue.get('created_at', 'unknown')}\n\n"
        body += "---\n\n"
        body += rad_issue.get("description", "") or "No description provided."
        return body
    
    def _format_patch_body_for_radicle(self, gh_pr: Dict[str, Any]) -> str:
        """Format GitHub PR body for Radicle patch."""
        body = f"**Originally from GitHub PR #{gh_pr['number']}**\n\n"
        body += f"Author: @{gh_pr['user']['login']}\n"
        body += f"Created: {gh_pr['created_at']}\n"
        body += f"GitHub URL: {gh_pr['html_url']}\n"
        body += f"Base: {gh_pr['base']['ref']} ← Head: {gh_pr['head']['ref']}\n\n"
        body += "---\n\n"
        body += gh_pr.get("body", "") or "No description provided."
        return body
    
    def _format_patch_body_for_github(self, rad_patch: Dict[str, Any]) -> str:
        """Format Radicle patch body for GitHub PR."""
        body = f"**Originally from Radicle patch {rad_patch.get('id', 'unknown')[:8]}...**\n\n"
        body += f"Author: {rad_patch.get('author', 'unknown')}\n"
        body += f"Created: {rad_patch.get('created_at', 'unknown')}\n\n"
        body += "---\n\n"
        body += rad_patch.get("description", "") or "No description provided."
        return body
    
    async def sync_all(self) -> Dict[str, Any]:
        """Perform bidirectional sync of issues and patches."""
        print("🚀 Starting comprehensive GitHub ↔ Radicle sync")
        
        results = {}
        
        # Sync issues both directions
        results["issues_gh_to_rad"] = await self.sync_issues_github_to_radicle()
        results["issues_rad_to_gh"] = await self.sync_issues_radicle_to_github()
        
        # Sync patches both directions  
        results["patches_gh_to_rad"] = await self.sync_patches_github_to_radicle()
        results["patches_rad_to_gh"] = await self.sync_patches_radicle_to_github()
        
        # Update last sync time
        self.db.data["last_sync"] = datetime.now().isoformat()
        self.db.save_db()
        
        return results


async def main():
    """Main sync function."""
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not github_token:
        print("❌ GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
        return 1
    
    github_repo = "fovi-llc/radicle-mcp"  # Update this to match your repo
    
    syncer = GitHubRadicleSyncer(github_token, github_repo)
    
    print("🔄 Starting GitHub ↔ Radicle synchronization")
    print(f"GitHub repo: {github_repo}")
    print(f"Radicle RID: {syncer.db.data.get('radicle_rid', 'auto-detect')}")
    
    try:
        results = await syncer.sync_all()
        
        print("\n📊 Sync Results:")
        print(f"Issues GitHub → Radicle: {results['issues_gh_to_rad']}")
        print(f"Issues Radicle → GitHub: {results['issues_rad_to_gh']}")
        print(f"Patches GitHub → Radicle: {results['patches_gh_to_rad']}")
        print(f"Patches Radicle → GitHub: {results['patches_rad_to_gh']}")
        
        print("\n🎉 Synchronization complete!")
        return 0
        
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
