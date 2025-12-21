# crap.games

A static website that lists all games hosted on subdomains of crap.games.

## Features

- **Dynamic game registry** - Games register themselves via GitHub Actions
- **Rich metadata** - Each game can include descriptions, tags, thumbnails, and more
- **Category filtering** - Browse games by type (puzzle, action, strategy, etc.)
- **Responsive design** - Works great on mobile and desktop
- **Auto-updating** - Registry updates automatically when games are deployed

## Architecture

This system consists of:

1. **Main website** (`index.html`) - Displays the game registry
2. **Game registry** (`games/registry.json`) - Stores game metadata
3. **Registry update workflow** (`.github/workflows/update-registry.yml`) - Reusable workflow for updating registry
4. **Deployment workflow** (`.github/workflows/deploy.yml`) - Deploys to GitHub Pages

## For Game Developers

### Register Your Game

Your game repository can automatically update its metadata in the registry using a reusable workflow. Add this to your game repository as `.github/workflows/update-registry.yml`:

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

**Important**: You must have authorization from the repository owner to use this workflow.

See [REGISTRY_WORKFLOW.md](REGISTRY_WORKFLOW.md) for complete setup instructions and all available options.

## Registry Schema

Each game entry contains:

```json
{
  "name": "Game Name",
  "subdomain": "game-subdomain", 
  "url": "https://game-subdomain.crap.games",
  "description": "Game description",
  "category": "puzzle",
  "tags": ["html5", "browser", "casual"],
  "thumbnailUrl": "https://example.com/thumbnail.png",
  "author": "Developer Name",
  "version": "1.0.0",
  "repoUrl": "https://github.com/user/repo",
  "registeredAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z",
  "registeredBy": "username/repo-name",
  "lastCommit": "commit-sha"
}
```

## Development

### Local Development

1. Clone this repository
2. Run a local server:
   ```bash
   python3 -m http.server 8000
   ```
3. Open `http://localhost:8000` in your browser

### Adding Test Games

To test the registry locally, you can add games directly to `games/registry.json`:

```bash
cp games/registry.json games/registry.json.backup
# Edit games/registry.json to add test games
```

## Deployment

This site is automatically deployed to GitHub Pages when pushed to the `main` branch.

The deployment workflow:
1. Builds the static site
2. Deploys to GitHub Pages
3. Updates the live site within a few minutes

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Areas for Contribution

- UI/UX improvements
- New features (search, sorting, etc.)
- Better error handling
- Performance optimizations
- Documentation improvements

## License

MIT License - see LICENSE file for details.

## Documentation

- [REGISTRY_WORKFLOW.md](REGISTRY_WORKFLOW.md) - Complete guide to the registry update workflow system
  - For game developers: How to register your game
  - For maintainers: Setup, security, and management details

## Support

- Create an issue for bugs or feature requests
- Check [REGISTRY_WORKFLOW.md](REGISTRY_WORKFLOW.md) for game registration and troubleshooting
- Review existing issues before creating new ones
