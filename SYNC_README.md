# GitHub ↔ Radicle Synchronization

This project includes bidirectional synchronization between GitHub and Radicle repositories, allowing seamless collaboration across both platforms.

## Features

### ✅ Implemented
- **Issues Synchronization**: Bidirectional sync of issues between GitHub and Radicle
- **Idempotent Operations**: Safe to run multiple times without creating duplicates
- **Mapping Database**: JSON-based tracking of GitHub/Radicle ID relationships
- **Metadata Preservation**: Original author, creation date, and platform links preserved
- **MCP Integration**: Available as MCP tools for AI assistant access
- **CLI Interface**: Command-line tools for manual sync operations

### 🚧 Partial Implementation
- **Pull Request/Patch Sync**: Basic framework implemented but requires branch management
- **Update Detection**: Detects when items need updates but update logic not fully implemented

## Quick Start

### 1. Setup GitHub Access Token

```bash
# Create a GitHub Personal Access Token with 'repo' and 'issues' permissions
export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here
```

### 2. Test Connectivity

```bash
python demo_sync.py
```

### 3. Perform Sync

```bash
# Sync everything
python github_radicle_sync.py

# Or use the CLI wrapper
python sync_cli.py --repo fovi-llc/radicle-mcp --dry-run
python sync_cli.py --repo fovi-llc/radicle-mcp --issues-only
```

## MCP Tools

The sync functionality is available as MCP tools:

- `github_sync_test`: Test connectivity and show current state
- `github_sync_issues`: Sync issues only
- `github_sync_full`: Full bidirectional sync

## Sync Process

### Issues: GitHub → Radicle
1. Fetch all GitHub issues
2. Check existing mappings to avoid duplicates  
3. Create new Radicle issues for unmapped GitHub issues
4. Store mapping in local database
5. Format includes original GitHub metadata and links

### Issues: Radicle → GitHub  
1. Fetch all Radicle issues
2. Check existing mappings to avoid duplicates
3. Create new GitHub issues for unmapped Radicle issues
4. Tag with "from-radicle" label
5. Store mapping in local database

### Data Mapping

The sync maintains a JSON database (`.radicle_github_sync.json`) with:

```json
{
  "issues": {
    "gh123_rad456": {
      "github_id": 123,
      "github_number": 42, 
      "radicle_id": "456abc...",
      "title": "Example Issue",
      "last_sync": "2025-06-23T10:30:00",
      "github_updated_at": "2025-06-23T10:00:00",
      "radicle_updated_at": "2025-06-23T10:15:00"
    }
  },
  "patches": {},
  "last_sync": "2025-06-23T10:30:00",
  "github_repo": "owner/repo",
  "radicle_rid": "rad:abc123..."
}
```

## Configuration

### Environment Variables
- `GITHUB_PERSONAL_ACCESS_TOKEN`: Required for GitHub API access

### Repository Configuration
- Update `github_repo` variable in scripts to match your repository
- Radicle RID is auto-detected or can be specified

## Limitations

1. **Branch Management**: PR/patch sync requires Git branch synchronization not yet implemented
2. **Update Logic**: Changes to existing issues/PRs are detected but not yet synced
3. **Rate Limits**: No GitHub API rate limiting implemented
4. **Conflict Resolution**: No automated conflict resolution for divergent changes

## Architecture

- `github_radicle_sync.py`: Core sync engine
- `sync_cli.py`: Command-line interface
- `demo_sync.py`: Interactive demonstration
- `test_sync.py`: Connectivity testing
- `src/radicle_mcp/server.py`: MCP tool integration

## Future Enhancements

- [ ] Complete PR/patch synchronization with branch management
- [ ] Implement update synchronization for modified issues
- [ ] Add conflict resolution strategies
- [ ] Implement GitHub API rate limiting
- [ ] Add webhook support for real-time sync
- [ ] Support for labels, assignees, and milestones sync
- [ ] Multi-repository batch sync
