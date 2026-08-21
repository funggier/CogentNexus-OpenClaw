[CmdletBinding()]
param(
    [ValidateSet('ollama','lmstudio')]
    [string]$Provider = 'lmstudio',

    [switch]$RunDestructive
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($env:OS -ne 'Windows_NT') {
    throw 'This acceptance harness wrapper is Windows-only.'
}

$Source = Join-Path $PSScriptRoot 'accept-v092-windows.ps1'
if (-not (Test-Path $Source)) {
    throw "Acceptance harness not found: $Source"
}

# Verify the object shape we are about to inject actually survives Windows
# PowerShell 5.1 ConvertTo-Json before touching the real acceptance harness.
$Smoke = [pscustomobject][ordered]@{
    schemaVersion = 2
    candidateVersion = '0.9.2'
    startedAt = (Get-Date).ToString('o')
    provider = $Provider
    destructiveRequested = [bool]$RunDestructive
    repoRoot = 'smoke'
    openclawConfig = 'smoke'
    steps = (New-Object System.Collections.ArrayList)
    result = 'running'
    openclawBefore = $null
    openclawAfter = $null
    finishedAt = $null
    error = $null
}
$SmokeStep = [pscustomobject][ordered]@{
    name = 'serialization-smoke'
    status = 'PASS'
    at = (Get-Date).ToString('o')
    data = [pscustomobject][ordered]@{
        command = @('openclaw.cmd','--version')
        exitCode = 0
        durationSeconds = 0.01
        stdout = 'OpenClaw smoke'
        stderr = ''
    }
}
[void]$Smoke.steps.Add($SmokeStep)
$SmokeJson = $Smoke | ConvertTo-Json -Depth 40
$SmokeRoundTrip = $SmokeJson | ConvertFrom-Json
if (@($SmokeRoundTrip.steps).Count -ne 1 -or $SmokeRoundTrip.steps[0].name -ne 'serialization-smoke') {
    throw 'PowerShell 5.1 evidence serialization smoke test failed.'
}
Write-Host 'PowerShell 5.1 evidence serialization smoke test: PASS'

# Patch the acceptance harness in a temporary sibling file. Keeping the
# temporary file beside the source preserves the original harness
# $PSScriptRoot -> repository-root resolution.
$Original = Get-Content $Source -Raw

$OldEvidence = @'
$Evidence = [ordered]@{
    schemaVersion = 2
    candidateVersion = $Version
    startedAt = (Get-Date).ToString('o')
    provider = $Provider
    destructiveRequested = [bool]$RunDestructive
    repoRoot = $RepoRoot
    openclawConfig = $OpenClawConfig
    steps = @()
    result = 'running'
}
'@
$NewEvidence = @'
$Evidence = [pscustomobject][ordered]@{
    schemaVersion = 2
    candidateVersion = $Version
    startedAt = (Get-Date).ToString('o')
    provider = $Provider
    destructiveRequested = [bool]$RunDestructive
    repoRoot = $RepoRoot
    openclawConfig = $OpenClawConfig
    steps = (New-Object System.Collections.ArrayList)
    result = 'running'
    openclawBefore = $null
    openclawAfter = $null
    finishedAt = $null
    error = $null
}
'@

$OldStep = @'
    $Evidence.steps += [ordered]@{
        name = $Name
        status = $Status
        at = (Get-Date).ToString('o')
        data = $Data
    }
    Save-Evidence
'@
$NewStep = @'
    $step = [pscustomobject][ordered]@{
        name = $Name
        status = $Status
        at = (Get-Date).ToString('o')
        data = [pscustomobject]$Data
    }
    [void]$Evidence.steps.Add($step)
    Save-Evidence
'@

foreach ($pair in @(
    @($OldEvidence, $NewEvidence),
    @($OldStep, $NewStep)
)) {
    if (-not $Original.Contains($pair[0])) {
        throw 'Expected PowerShell 5.1 serialization patch block was not found; refusing an unverified patch.'
    }
    $Original = $Original.Replace($pair[0], $pair[1])
}

$OldReturn = '    return [ordered]@{'
$NewReturn = '    return [pscustomobject][ordered]@{'
if (-not $Original.Contains($OldReturn)) {
    throw 'Expected Read-OpenClawFields return block was not found; refusing an unverified patch.'
}
$Patched = $Original.Replace($OldReturn, $NewReturn)

$Temp = Join-Path $PSScriptRoot (".accept-v092-ps51-{0}.tmp.ps1" -f ([guid]::NewGuid().ToString('N')))
try {
    Set-Content -Path $Temp -Value $Patched -Encoding UTF8

    $tokens = $null
    $errors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile(
        $Temp,
        [ref]$tokens,
        [ref]$errors
    )
    if ($errors.Count) {
        $errors | ForEach-Object { Write-Error "Patched acceptance harness :: $_" }
        throw 'Patched acceptance harness failed PowerShell syntax validation.'
    }

    $Arguments = @(
        '-NoProfile',
        '-ExecutionPolicy','Bypass',
        '-File',$Temp,
        '-Provider',$Provider
    )
    if ($RunDestructive) {
        $Arguments += '-RunDestructive'
    }

    & powershell.exe @Arguments
    $Code = $LASTEXITCODE
    if ($null -eq $Code) { $Code = 1 }
    exit [int]$Code
}
finally {
    Remove-Item $Temp -Force -ErrorAction SilentlyContinue
}
