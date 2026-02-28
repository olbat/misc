# Gerrit Git Hooks

## About
Git hooks for [Gerrit](https://www.gerritcodereview.com/) code review integration.

| File | Description |
|:-----|:------------|
| [prepare-commit-msg](prepare-commit-msg) | Generates Gerrit Change-IDs for commits |
| [bugzilla/change-merged](bugzilla/change-merged) | Notifies Bugzilla when a change is merged |
| [bugzilla/patchset-created](bugzilla/patchset-created) | Notifies Bugzilla when a patchset is created |

## Usage
Copy the hooks into your repository's `.git/hooks/` directory.
