Param(
    [string]$Message = "Update"
)

# Usage: .\scripts\push-all.ps1 -Message "Commit message"
# Safely add, commit, and push to origin/main.

$porcelain = git status --porcelain
if (-not $porcelain) {
    Write-Output "No changes to commit."
    exit 0
}

git add -A
$commit = git commit -m "$Message" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Output "git commit returned code $LASTEXITCODE: $commit"
    # If commit failed due to no changes, exit cleanly
    exit $LASTEXITCODE
}

git branch -M main
$push = git push -u origin main 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Output "git push failed: $push"
    exit $LASTEXITCODE
}

Write-Output "Pushed to origin/main"
