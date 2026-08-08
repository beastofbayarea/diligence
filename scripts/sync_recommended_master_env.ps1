param(
    [string]$MasterEnvPath = 'C:\Users\Nagarro\Downloads\master_all_environment_variables.env',
    [string]$ConfigDirectory = 'C:\Users\Nagarro\Downloads\job-flow-ai-config'
)

$centConfig = Get-Content -LiteralPath (Join-Path $ConfigDirectory 'cent_capital_config.json') -Raw | ConvertFrom-Json
$geminiAccount = Get-Content -LiteralPath (Join-Path $ConfigDirectory 'cent-capital-472820-f55ada69e99b.json') -Raw | ConvertFrom-Json

$additions = [ordered]@{
    CENT_CAPITAL_BASE_URL = [string]$centConfig.application.base_url
    CENT_CAPITAL_PRODUCTION_API_URL = [string]$centConfig.application.production_api_url
    FINIPEDIA_DEFAULT_IMAGE_URL = [string]$centConfig.application.default_finipedia_image
    CENT_CAPITAL_GITHUB_REPOSITORY = 'https://github.com/Cent-Capital/cent-capital-fe'
    DILIGENCE_GITHUB_REPOSITORY = 'https://github.com/beastofbayarea/diligence'
    FINANCIAL_WELLNESS_LAB_GITHUB_REPOSITORY = 'https://github.com/beastofbayarea/financial-wellness-lab'
    JOB_FLOW_AI_GITHUB_REPOSITORY = 'https://github.com/beastofbayarea/job-flow-ai'
    GCP_PROJECT_NUMBER = [string]$centConfig.google.cloud_project_number
    GOOGLE_SEARCH_CONSOLE_CREDENTIALS = (Join-Path $ConfigDirectory 'cent-capital-472820-b18e17e354b9.json')
    GOOGLE_GEMINI_CREDENTIALS = (Join-Path $ConfigDirectory 'cent-capital-472820-f55ada69e99b.json')
    GOOGLE_VERTEX_CREDENTIALS = (Join-Path $ConfigDirectory 'vertex_service_account.json')
    GCP_GEMINI_SERVICE_ACCOUNT_EMAIL = [string]$geminiAccount.client_email
    GCP_GEMINI_SERVICE_ACCOUNT_CLIENT_ID = [string]$geminiAccount.client_id
    AWS_SES_IAM_USER = [string]$centConfig.aws.iam_user
}

foreach ($entry in $additions.GetEnumerator()) {
    if ([string]::IsNullOrWhiteSpace([string]$entry.Value)) {
        throw "Source value for $($entry.Key) is empty."
    }
}

$lines = [Collections.Generic.List[string]]::new()
$lines.AddRange([string[]][IO.File]::ReadAllLines($MasterEnvPath))
$existing = @{}
foreach ($line in $lines) {
    if ($line -match '^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=') {
        $existing[$matches[1]] = $true
    }
}

$duplicates = @($additions.Keys | Where-Object { $existing.ContainsKey($_) })
if ($duplicates.Count -gt 0) {
    throw "Refusing to overwrite existing keys: $($duplicates -join ', ')"
}

$backupPath = "$MasterEnvPath.before-recommendations.bak"
if (-not (Test-Path -LiteralPath $backupPath)) {
    [IO.File]::Copy($MasterEnvPath, $backupPath, $false)
}

if ($lines.Count -gt 0 -and $lines[$lines.Count - 1] -ne '') { $lines.Add('') }
$lines.Add('# ------------------------------------------------------------------------------')
$lines.Add('# 13. CENT CAPITAL RUNTIME & REPOSITORY REFERENCES')
$lines.Add('# ------------------------------------------------------------------------------')
foreach ($entry in $additions.GetEnumerator()) {
    $lines.Add("$($entry.Key)=$($entry.Value)")
}
$lines.Add('')

[IO.File]::WriteAllLines($MasterEnvPath, $lines, [Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Added = $additions.Count
    Backup = $backupPath
}
