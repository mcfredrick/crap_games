# Game Registry Update Workflow

This document explains how the game registry system works and how to use it from your game repositories.

## Overview

The `crap.games` registry system allows game repositories to automatically update their metadata in the central registry. This is accomplished through a **reusable GitHub Actions workflow** that other repositories can call.

### How It Works

1. **Game Repository** - Your game repository calls the reusable workflow from the `crap_games` registry repo
2. **Registry Workflow** - The `update-registry` workflow runs and updates the `games/registry.json` file
3. **Authentication** - The workflow uses a personal access token (`REGISTRY_UPDATE_TOKEN`) to authenticate and push changes
4. **Central Registry** - The updated registry file is committed back to the main `crap_games` repository
5. **Website Updates** - The main website automatically displays the updated game metadata via GitHub Pages

## For Game Developers

### Prerequisites

- Your game must be hosted in a GitHub repository
- You need a GitHub account that I (the repository owner) have authorized

### Usage

Add the following workflow to your game repository in `.github/workflows/register-game.yml`:

```yaml
name: Update Game Registry

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  update-registry:
    uses: mcfredrick/crap_games/.github/workflows/update-registry.yml@main
    with:
      game-name: "Your Game Name"
      subdomain: "your-game"
      description: "A short description of your game"
      category: "puzzle"
      tags: "html5, browser, casual"
      thumbnail-url: "https://your-game.crap.games/icon.png"
      author: "Your Name"
      repo-url: "https://github.com/your-username/your-game-repo"
      version: "1.0.0"
    secrets: inherit
```

### Input Parameters

#### Required Inputs

- **game-name** - The display name of your game (e.g., "Fuel Game")
- **subdomain** - The subdomain under crap.games (e.g., "fuel" → fuel.crap.games)
- **description** - A short description of what your game is about (2-3 sentences recommended)
- **category** - Game category. Choose from:
  - `puzzle` - Puzzle games
  - `action` - Action games
  - `strategy` - Strategy games
  - `simulation` - Simulation games
  - `arcade` - Arcade/retro games
  - `casual` - Casual games
  - `educational` - Educational games
  - `other` - Miscellaneous

#### Optional Inputs

- **tags** - Comma-separated tags for filtering (e.g., "html5, browser, 2d")
- **thumbnail-url** - URL to a thumbnail or icon image (recommended: 256x256 or larger)
- **author** - Game creator/author name
- **repo-url** - URL to the game's GitHub repository
- **version** - Version number (e.g., "1.0.0")

### Example Workflow

Here's a complete example for a game repository:

```yaml
name: Update Game Registry

on:
  push:
    branches: [ main, develop ]
  workflow_dispatch:

jobs:
  update-registry:
    uses: mcfredrick/crap_games/.github/workflows/update-registry.yml@main
    with:
      game-name: "Fuel"
      subdomain: "fuel"
      description: "A strategic resource management game where you optimize fuel production and consumption across multiple facilities."
      category: "simulation"
      tags: "strategy, resource-management, simulation, economic"
      thumbnail-url: "https://fuel.crap.games/assets/icon.png"
      author: "Matt"
      repo-url: "https://github.com/mcfredrick/fuel-game"
      version: "2.1.3"
    secrets: inherit
```

### Triggering Updates

The workflow will automatically run when:
- You push to the `main` branch
- You push to the `develop` branch (customize as needed)
- You manually trigger it via the "Run workflow" button

### Updating Game Information

Simply update the inputs in your workflow file and push to trigger an update. The workflow will:
- Add your game to the registry if it's new
- Update your game's metadata if it already exists
- Preserve the original registration date while updating the "last updated" timestamp

## For Repository Maintainer (You)

### Setup Requirements

1. **Personal Access Token**
   - Create a PAT (Personal Access Token) with `repo` and `workflow` scopes
   - Keep this token secure and never commit it
   - Store it as a repository secret named `REGISTRY_UPDATE_TOKEN`

2. **Repository Settings**
   - Only you (the main account) have push access to this repository
   - Game repos can only trigger the workflow through the reusable workflow mechanism
   - All changes must be pushed by the GitHub Action using the PAT

3. **Branch Protection**
   - Consider enabling branch protection on `main` to require reviews
   - However, GitHub Actions can bypass this if necessary

### Managing the Registry

#### Manual Updates

You can also manually update `games/registry.json` by:
1. Editing the file directly in GitHub or locally
2. Adding/updating game entries following the JSON schema
3. Pushing to `main`

#### Removing Games

To remove a game from the registry:
1. Edit `games/registry.json`
2. Remove the game object from the `games` array
3. Commit and push

#### Registry Entry Schema

```json
{
  "name": "Game Name",
  "subdomain": "game-subdomain",
  "url": "https://game-subdomain.crap.games",
  "description": "Short description",
  "category": "category-name",
  "tags": ["tag1", "tag2"],
  "author": "Author Name",
  "version": "1.0.0",
  "thumbnailUrl": "https://...",
  "repoUrl": "https://github.com/...",
  "registeredAt": "2024-12-21T12:00:00Z",
  "updatedAt": "2024-12-21T12:00:00Z",
  "registeredBy": "username",
  "lastCommit": "abc123..."
}
```

### Security Considerations

- **Token Access**: Only the `REGISTRY_UPDATE_TOKEN` secret can modify the registry
- **Workflow Limitations**: The reusable workflow can only update registry entries; it cannot modify other files
- **Audit Trail**: All registry updates are committed to Git with proper attribution
- **Restricted Push**: Only authenticated workflows with the proper token can push to this repo

## Troubleshooting

### Workflow Fails to Run

- Verify the workflow file path is correct: `.github/workflows/update-registry.yml`
- Check that `secrets: inherit` is included in your job definition
- Ensure you're using the correct branch reference (`@main`)

### Changes Not Appearing

- Check the Actions tab in your game repository for error logs
- Verify all required inputs are provided
- Check that the registry repo is accessible

### Token Issues

- If the `REGISTRY_UPDATE_TOKEN` is invalid or expired, regenerate it and update the secret
- Ensure the token has `repo` and `workflow` scopes

## Future Enhancements

Potential improvements to consider:
- Automatic validation of game metadata
- Webhook integration for real-time updates
- Automated screenshot/thumbnail generation
- Category and tag standardization validation
- Duplicate subdomain detection
