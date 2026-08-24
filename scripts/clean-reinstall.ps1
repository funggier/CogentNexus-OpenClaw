[CmdletBinding(SupportsShouldProcess=$true, ConfirmImpact="High")]
param(
    [string]$Workspace = (Join-Path $HOME ".openclaw\workspace"),
    [string]$BackupRoot = (Join-Path $env:LOCALAPPDATA "CogentNexus-OpenClaw\clean-reinstall-backups"),
    [switch]$NoBackup,
    [switch]$LinkPlugin
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$installer = Join-Path $PSScriptRoot "install.ps1"
$stateRoot = Split-Path -Parent $Workspace
$cnxRoot = Join-Path $Workspace ".cogentnexus-openclaw"
$skill = Join-Path $Workspace "skills\cogentnexus-openclaw"
$launcher = Join-Path $Workspace "cnxclaw.cmd"
$extension = Join-Path $stateRoot "extensions\cogentnexus-openclaw"
$agents = Join-Path $Workspace "AGENTS.md"
$openclawConfig = Join-Path $stateRoot "openclaw.json"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = Join-Path $BackupRoot $stamp
$ownershipScript = Join-Path $repoRoot "skills\cogentnexus-openclaw\scripts\namespace_ownership.py"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { throw "Required command not found: $Name" }
}

function Invoke-NativeCapture {
    param([Parameter(Mandatory=$true)][scriptblock]$Command)
    $saved = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $output = & $Command 2>&1 | Out-String
        $code = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $saved }
    return [pscustomobject]@{ Code = $code; Output = $output.TrimEnd() }
}

function Copy-Backup([string]$Path, [string]$Name) {
    if (-not (Test-Path -LiteralPath $Path)) { return }
    $dest = Join-Path $backup $Name
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
    Copy-Item -LiteralPath $Path -Destination $dest -Recurse -Force
}

function Remove-OwnedPath([string]$Path) {
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
        Write-Host "Removed: $Path"
    }
}

if (-not (Test-Path -LiteralPath $installer)) { throw "Installer not found beside this script: $installer" }
Require-Command python
Require-Command openclaw
Require-Command node
Require-Command npm

Write-Host "CogentNexus-OpenClaw clean reinstall"
Write-Host "Workspace : $Workspace"
Write-Host "Repo/root : $repoRoot"

if (Test-Path -LiteralPath $cnxRoot) {
    & python $ownershipScript verify --root $cnxRoot --workspace $Workspace | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Ownership manifest mismatch; refusing clean-reinstall mutation." }
}

if (-not $NoBackup) {
    New-Item -ItemType Directory -Force -Path $backup | Out-Null
    Copy-Backup $cnxRoot ".cogentnexus-openclaw"
    Copy-Backup $skill "skills\cogentnexus-openclaw"
    Copy-Backup $launcher "cnxclaw.cmd"
    Copy-Backup $extension "extension\cogentnexus-openclaw"
    Copy-Backup $agents "AGENTS.md"
    Copy-Backup $openclawConfig "openclaw.json"
    Write-Host "Backup created: $backup"
}
else {
    Write-Warning "-NoBackup selected: existing CogentNexus-OpenClaw durable state will be permanently purged."
}

# Never destructively purge a managed installation before native OpenClaw is restored.
if (Test-Path -LiteralPath $launcher) {
    Write-Host "Disabling existing CogentNexus-OpenClaw to restore PASSTHROUGH..."
    $disable = Invoke-NativeCapture { & $launcher disable }
    if ($disable.Output) { Write-Host $disable.Output }
    if ($disable.Code -ne 0) { throw "cnxclaw disable failed. Refusing destructive cleanup while ownership may still be MANAGED." }
}

$list = Invoke-NativeCapture { openclaw plugins list --json }
if ($list.Code -ne 0) { throw "Could not inspect OpenClaw plugins before cleanup:`n$($list.Output)" }
$hasPlugin = $list.Output -match 'cogentnexus-openclaw'

if ($hasPlugin) {
    Write-Host "Uninstalling CogentNexus-OpenClaw OpenClaw plugin non-interactively..."
    $uninstall = Invoke-NativeCapture { openclaw plugins uninstall cogentnexus-openclaw --force }
    if ($uninstall.Output) { Write-Host $uninstall.Output }
    if ($uninstall.Code -ne 0) { throw "OpenClaw plugin uninstall failed; refusing to delete remaining state." }
}

# Linked/manual plugin installations can leave filesystem residue after registry cleanup.
Remove-OwnedPath $extension
Remove-OwnedPath $skill
Remove-OwnedPath $cnxRoot
if (Test-Path -LiteralPath $launcher) {
    Remove-Item -LiteralPath $launcher -Force
    Write-Host "Removed: $launcher"
}

$listAfter = Invoke-NativeCapture { openclaw plugins list --json }
if ($listAfter.Code -ne 0) { throw "Could not inspect OpenClaw plugins after cleanup:`n$($listAfter.Output)" }
if ($listAfter.Output -match 'cogentnexus-openclaw') {
    throw "CogentNexus-OpenClaw plugin is still registered after uninstall/cleanup. Refusing reinstall."
}

Write-Host "Installing fresh CogentNexus-OpenClaw from: $repoRoot"
if ($LinkPlugin) { & $installer -Workspace $Workspace -LinkPlugin }
else { & $installer -Workspace $Workspace }
if ($LASTEXITCODE -ne 0) { throw "Fresh CogentNexus-OpenClaw installation failed" }

if (-not (Test-Path -LiteralPath $launcher)) { throw "Fresh install did not create cnxclaw.cmd" }
& $launcher status
if ($LASTEXITCODE -ne 0) { throw "CogentNexus-OpenClaw post-install status failed" }
openclaw gateway status
if ($LASTEXITCODE -ne 0) { throw "Gateway post-install health check failed" }
openclaw plugins list
if ($LASTEXITCODE -ne 0) { throw "Plugin post-install inventory failed" }

Write-Host ""
Write-Host "CLEAN REINSTALL: PASS"
if (-not $NoBackup) { Write-Host "Backup: $backup" }
