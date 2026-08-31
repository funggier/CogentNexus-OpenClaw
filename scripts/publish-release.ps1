[CmdletBinding()]
param(
    [string]$Version,
    [string]$Remote = "origin",
    [switch]$SkipLocalValidation
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$versionFile = Join-Path $repoRoot "VERSION"

function Run-Git([string[]]$Args) {
    $saved = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $output = & git -C $repoRoot @Args 2>&1 | Out-String
        $code = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $saved }
    if ($code -ne 0) { throw "git $($Args -join ' ') failed ($code):`n$output" }
    return $output.TrimEnd()
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git is required" }
if (-not (Test-Path -LiteralPath $versionFile)) { throw "VERSION file missing" }

$repoVersion = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if (-not $Version) { $Version = $repoVersion }
if ($Version -ne $repoVersion) { throw "Requested version $Version does not match VERSION $repoVersion" }

$tag = "v$Version"
$releaseBranch = "release/$tag"

$status = Run-Git @("status","--porcelain=v1","--untracked-files=no")
if ($status) { throw "Tracked worktree is not clean. Commit changes before release publication.`n$status" }

$head = (Run-Git @("rev-parse","HEAD")).Trim()
$remoteExisting = & git -C $repoRoot ls-remote --heads $Remote "refs/heads/$releaseBranch" 2>$null | Out-String
if ($LASTEXITCODE -ne 0) { throw "Could not inspect remote release branch" }
if ($remoteExisting.Trim()) { throw "Remote $releaseBranch already exists; refusing duplicate release trigger." }

if (-not $SkipLocalValidation) {
    Push-Location $repoRoot
    try {
        python scripts/check_namespace_isolation.py
        if ($LASTEXITCODE -ne 0) { throw "namespace isolation failed" }
        python scripts/check_baseline_consistency.py
        if ($LASTEXITCODE -ne 0) { throw "baseline consistency failed" }
        python skills/cogentnexus-openclaw/scripts/validate.py --workspace-singleton
        if ($LASTEXITCODE -ne 0) { throw "skill validation failed" }
        python -m unittest discover -s tests -v
        if ($LASTEXITCODE -ne 0) { throw "Python tests failed" }
        Push-Location (Join-Path $repoRoot "plugins\cogentnexus-openclaw")
        try {
            npm ci
            if ($LASTEXITCODE -ne 0) { throw "npm ci failed" }
            npm test
            if ($LASTEXITCODE -ne 0) { throw "plugin tests failed" }
            npm run evaluation
            if ($LASTEXITCODE -ne 0) { throw "evaluation failed" }
            npm run plugin:validate
            if ($LASTEXITCODE -ne 0) { throw "plugin validation failed" }
        }
        finally { Pop-Location }
    }
    finally { Pop-Location }
}

Write-Host "Publishing release trigger branch $releaseBranch from $head"
Run-Git @("push",$Remote,"HEAD:refs/heads/$releaseBranch") | Write-Host
Write-Host "Release workflow will validate/package and create GitHub Release $tag."
Write-Host "No tag is moved by this script; the workflow targets this release commit."
