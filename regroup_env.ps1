param([Parameter(Mandatory)][string]$Path)

$lines = [IO.File]::ReadAllLines($Path)
$assignments = [System.Collections.Generic.List[object]]::new()
foreach ($line in $lines) {
    if ($line -match '^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=') {
        $assignments.Add([pscustomobject]@{ Key = $matches[1]; Line = $line })
    }
}

$groups = [ordered]@{
    '1. ORGANIZATION, LEGAL, CONTACT & PUBLICATION' = '^(COMPANY_|DELAWARE_|DUNS_|EVERIFY_|NAICS_|SIC_|UK_|EMAIL_|GOOGLE_IARC_|MICROSOFT_IARC_|APPLE_APP_|GOOGLE_PLAY_|BOOK_)'
    '2. INFRASTRUCTURE, HOSTING & LOCAL RUNTIME' = '^(VPS_|HOSTINGER_|VERCEL_|CLOUDFLARE_|JAVA_HOME$|CLAUDE_CODE_GIT_BASH_PATH$|USER_AGENT$|AGENT_PLATFORM_)'
    '3. APPLICATION, BACKEND, DATABASE & AUTH' = '^(SUPABASE_|POSTGRES_|JWT_|NEXT_PUBLIC_API_URL$|SERVER_PORT$|SPRING_PROFILES_ACTIVE$|GENERATE_SOURCEMAP$|JOB_APP_DASHBOARD_|CENT_CAPITAL_(?:BASE_URL|PRODUCTION_API_URL)$|FINIPEDIA_DEFAULT_IMAGE_URL$)'
    '4. GOOGLE CLOUD, VERTEX AI & GOOGLE OAUTH' = '^(GCP_|GOOGLE_CLOUD_|GOOGLE_APPLICATION_|GOOGLE_GENAI_|GOOGLE_WORKSPACE_|GOOGLE_OAUTH_|GOOGLE_INSTALLED_|GOOGLE_SA_|GOOGLE_SEARCH_CONSOLE_CREDENTIALS$|GOOGLE_GEMINI_CREDENTIALS$|GOOGLE_VERTEX_CREDENTIALS$|VERTEX_|GEMINI_|SAMSUNG_GALAXY_|NEXT_PUBLIC_GOOGLE_|OAUTH_|WEB_)'
    '5. AI PROVIDERS' = '^(XAI_|GROK_|OPENROUTER_|OPEN_ROUTER_|MISTRAL_|VIBE_)'
    '6. PAYMENTS, BANKING & FINANCIAL ACCOUNTS' = '^(STRIPE_|PLAID_|BANK_)'
    '7. EMAIL, MESSAGING & AUTOMATION' = '^(AWS_|APP_EMAIL_|SENDER_NET_|IFTTT_|AZURE_|LINKEDIN_|SLACK_|AMAZON_DEVELOPER_)'
    '8. SOURCE CONTROL, CMS, MEDIA & META' = '^(GITHUB_|GH_TOKEN$|.*_GITHUB_REPOSITORY$|PUBLIC_CONTENTFUL_|CONTENTFUL_|PEXELS_|META_)'
    '9. SEARCH INDEXING, SEO & ANALYTICS' = '^(GSC_|GOOGLE_SITE_VERIFICATION$|MICROSOFT_CLARITY_|GTM_|MICROSOFT_UET_|DOMAIN_|INDEXNOW_|BING_SUBMISSION_|GOOGLE_SEARCH_CONSOLE_)'
    '10. FINANCIAL, MARKET & ECONOMIC DATA APIS' = '^(EXCHANGE_RATE_|CURRENCY_API_|COINGECKO_|FRED_|ST_LOUIS_|MARKET_DATA_|FINANCIAL_MARKET_|FMP_|FINANCIAL_MODELING_|ALPHA_VANTAGE_)'
    '11. JOB APPLICATION AUTOMATION & CANDIDATE PROFILE' = '^(CANDIDATE_|APPLICATION_ENGINE_|SEARCH_)'
    '12. WEATHER, NEWS, GEOCODING & GOVERNMENT DATA' = '^(OPENWEATHER_|NEWSAPI_|OPENCAGE_|DATA_GOV_)'
}

$bucketed = [ordered]@{}
foreach ($name in $groups.Keys) { $bucketed[$name] = [System.Collections.Generic.List[object]]::new() }
$unmatched = [System.Collections.Generic.List[object]]::new()
foreach ($assignment in $assignments) {
    $matched = $false
    foreach ($name in $groups.Keys) {
        if ($assignment.Key -match $groups[$name]) {
            $bucketed[$name].Add($assignment)
            $matched = $true
            break
        }
    }
    if (-not $matched) { $unmatched.Add($assignment) }
}
if ($unmatched.Count -gt 0) {
    throw "Unmatched environment keys: $($unmatched.Key -join ', ')"
}

$output = [System.Collections.Generic.List[string]]::new()
$output.Add('# ==============================================================================')
$output.Add('# MASTER ENVIRONMENT CONFIGURATION (FULL PLATFORM, APIS & SERVICES SYNC)')
$output.Add('# Grouped by operational domain; assignment values preserved verbatim.')
$output.Add('# ==============================================================================')
foreach ($name in $groups.Keys) {
    $output.Add('')
    $output.Add('# ------------------------------------------------------------------------------')
    $output.Add("# $name")
    $output.Add('# ------------------------------------------------------------------------------')
    foreach ($assignment in $bucketed[$name]) { $output.Add($assignment.Line) }
}
$output.Add('')

$beforeKeys = @($assignments.Key | Sort-Object)
$afterKeys = @($bucketed.Values | ForEach-Object { $_.Key } | Sort-Object)
if (($beforeKeys -join "`n") -ne ($afterKeys -join "`n")) { throw 'Key preservation check failed.' }

$backup = "$Path.before-regrouping.bak"
if (-not (Test-Path -LiteralPath $backup)) { [IO.File]::Copy($Path, $backup, $false) }
$encoding = [Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllLines($Path, $output, $encoding)

[pscustomobject]@{
    Assignments = $assignments.Count
    Groups = $groups.Count
    Backup = $backup
}
