# Repository Access Configuration

This document explains how to configure the `crap_games` repository to restrict write access and set up the personal access token for the reusable workflow.

## Overview

To ensure only you can modify the game registry, while still allowing game repositories to trigger updates through the reusable workflow, you need to:

1. Restrict repository write permissions
2. Create and store a personal access token
3. Configure branch protection (recommended)

## Step 1: Create a Personal Access Token

The reusable workflow needs a token to authenticate and push changes to the registry repository.

### How to Create the Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name: `crap_games_registry_updates`
4. Set expiration to 90 days (or longer based on your preference)
5. Select the following scopes:
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (update GitHub Action workflows)
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again)

### Store the Token as a Repository Secret

1. Go to your repository: https://github.com/mcfredrick/crap_games
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click "New repository secret"
4. Name: `REGISTRY_UPDATE_TOKEN`
5. Value: Paste the token you generated
6. Click "Add secret"

## Step 2: Configure Repository Access

### Make Repository Private or Restrict Pushes

Choose one of the following approaches:

#### Option A: Keep as Public but Restrict Push Access (Recommended)

This allows people to view and clone the code but only you (and authorized workflows) can push changes.

1. Go to **Settings** → **Collaborators and teams**
2. Ensure only your account has write/admin access
3. Remove any other collaborators or set them to read-only
4. Verify that external accounts cannot push

#### Option B: Make Repository Private

For maximum security:

1. Go to **Settings** → **General**
2. Scroll to "Danger Zone"
3. Click "Change repository visibility"
4. Select "Private"
5. Confirm

**Note**: If private, game developers cannot clone the repo, but they can still call the reusable workflow from their own repositories.

## Step 3: Configure Branch Protection (Optional but Recommended)

Add branch protection to prevent accidental direct pushes and maintain audit trail:

1. Go to **Settings** → **Branches**
2. Click "Add rule" under "Branch protection rules"
3. Apply to branch: `main`
4. Enable:
   - ✅ "Require a pull request before merging"
   - ✅ "Require status checks to pass before merging"
   - ✅ "Include administrators" (if you want to enforce even for yourself)
   - ✅ "Require branches to be up to date before merging"

5. Dismiss stale pull request approvals: Yes
6. Create

**Note**: The GitHub Action will be able to bypass branch protection rules if configured to do so, but this adds an extra layer of safety.

## Step 4: Verify Permissions

After configuration, verify that:

- ✅ Only your account has write access to the main branch
- ✅ The `REGISTRY_UPDATE_TOKEN` secret is set in repository settings
- ✅ Game developers can call the reusable workflow from their repos
- ✅ Commits from the workflow are attributed correctly

## Testing the Setup

To test that everything is working:

1. Create a test game repository
2. Add the `.github/workflows/update-registry.yml` workflow (see `REGISTRY_WORKFLOW.md`)
3. Push to trigger the workflow
4. Check the Actions tab to verify it runs successfully
5. Verify that `games/registry.json` was updated in the main `crap_games` repo

## Troubleshooting

### "Permission denied" error in workflow

- Verify the `REGISTRY_UPDATE_TOKEN` secret exists
- Ensure the token has `repo` and `workflow` scopes
- Check that the token hasn't expired
- Regenerate if needed and update the secret

### Workflow can't checkout the registry repo

- Verify the token has access to the `crap_games` repository
- If the repo is private, ensure the token has been generated with full `repo` access
- Check the workflow logs for the exact error message

### Can't push from workflow

- Verify the git config is correct (user.email, user.name)
- Check that the token has not expired
- Ensure the branch exists in the remote

### Unintended commits to main

- Enable branch protection rules to require PR reviews
- Consider enabling "Require status checks to pass"
- Add administrator enforcement to prevent accidental pushes

## Token Rotation

For security best practices:

1. Rotate the token every 90-180 days
2. Create a new token following the steps above
3. Update the `REGISTRY_UPDATE_TOKEN` secret
4. Optionally delete the old token from https://github.com/settings/tokens

## Security Considerations

- **Never** commit the token to the repository
- **Never** share the token in public channels
- The token is only accessible to workflows in this repository
- GitHub automatically masks the token in workflow logs
- Each game repository calling the workflow will inherit the token via `secrets: inherit`

## Next Steps

After completing this configuration:

1. Share the `REGISTRY_WORKFLOW.md` documentation with game developers
2. Have them set up the `.github/workflows/update-registry.yml` in their repositories
3. Test with your own game repositories first
4. Monitor the Actions logs for any issues
5. Create issues or PRs for any improvements needed
