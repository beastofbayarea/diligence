Helper script: push-all.ps1

Usage:
- From repo root run: .\scripts\push-all.ps1 -Message "Your commit message"

Behavior:
- If no changes, exits with message "No changes to commit." and does nothing.
- Otherwise, stages all changes, commits with provided message, ensures branch is main, and pushes to origin/main.

Note: This is a convenience script. For automated CI or hooks, prefer safer workflows and avoid embedding credentials.