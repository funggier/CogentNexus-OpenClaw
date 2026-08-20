[CmdletBinding(SupportsShouldProcess=$true, ConfirmImpact="High")]
param(
    [string]$Workspace = (Join-Path $HOME ".openclaw\workspace"),
    [string]$BackupRoot = (Join-Path $env:LOCALAPPDATA "CogentNexus\clean-reinstall-backups"),
    [switch]$NoBackup,
    [switch]$LinkPlugin
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$installer = Join-Path $PSScriptRoot "install.ps1"
$stateRoot = Split-Path -Parent $Workspace
$cnxRoot = Join-Path $Workspace ".cogent"
$skill = Join-Path $Workspace "skills\cogentnexus"
$launcher = Join-Path $Workspace "cnx.cmd"
$extension = Join-Path $stateRoot "extensions\cogentnexus-rotation"
$agents = Join-Path $Workspace "AGENTS.md"
$openclawConfig = Join-Path $stateRoot "openclaw.json"
$pluginIndex = Join-Path $stateRoot "plugins\installs.json"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = Join-Path $BackupRoot $stamp

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
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
    $parent = Split-Path -Parent $dest
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    Copy-Item -LiteralPath $Path -Destination $dest -Recurse -Force
}

function Remove-OwnedPath([string]$Path) {
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
        Write-Host "Removed: $Path"
    }
}

if (-not (Test-Path -LiteralPath $installer)) {
    throw "Installer not found beside this script: $installer"
}

Require-Command python
Require-Command openclaw
Require-Command node
Require-Command npm

Write-Host "CogentNexus clean reinstall"
Write-Host "Workspace : $Workspace"
Write-Host "Repo/root : $repoRoot"

if (-not $NoBackup) {
    New-Item -ItemType Directory -Force -Path $backup | Out-Null
    Copy-Backup $cnxRoot ".cogent"
    Copy-Backup $skill "skills\cogentnexus"
    Copy-Backup $launcher "cnx.cmd"
    Copy-Backup $extension "extension\cogentnexus-rotation"
    Copy-Backup $agents "AGENTS.md"
    Copy-Backup $openclawConfig "openclaw.json"
    Copy-Backup $pluginIndex "plugins\installs.json"
    Write-Host "Backup created: $backup"
}
else {
    Write-Warning "-NoBackup selected: existing CogentNexus durable state will be permanently purged."
}

# Return a managed installation to native OpenClaw before destructive cleanup.
if (Test-Path -LiteralPath $launcher) {
    Write-Host "Disabling existing CogentNexus to restore PASSTHROUGH..."
    $disable = Invoke-NativeCapture { & $launcher disable }
    if ($disable.Output) { Write-Host $disable.Output }
    if ($disable.Code -ne 0) {
        throw "cnx disable failed. Refusing destructive cleanup while ownership may still be MANAGED."
    }
}

# Inventory must succeed before we decide whether uninstall is required.
$list = Invoke-NativeCapture { openclaw plugins list --json }
if ($list.Code -ne 0) {
    throw "Could not inspect OpenClaw plugins before cleanup:`n$($list.Output)"
}
$hasPlugin = $list.Output -match 'cogentnexus-rotation'

if ($hasPlugin) {
    Write-Host "Uninstalling CogentNexus OpenClaw plugin..."
    $uninstall = Invoke-NativeCapture { openclaw plugins uninstall cogentnexus-rotation }
    if ($uninstall.Output) { Write-Host $uninstall.Output }
    if ($uninstall.Code -ne 0) {
        throw "OpenClaw plugin uninstall failed; refusing to delete remaining state."
    }
}

# Linked/manual plugin installations can leave files even after registry cleanup.
Remove-OwnedPath $extension
Remove-OwnedPath $skill
Remove-OwnedPath $cnxRoot
if (Test-Path -LiteralPath $launcher) {
    Remove-Item -LiteralPath $launcher -Force
    Write-Host "Removed: $launcher"
}

# Verify the plugin registry no longer exposes the old installation before reinstall.
$listAfter = Invoke-NativeCapture { openclaw plugins list --json }
if ($listAfter.Code -ne 0) {
    throw "Could not inspect OpenClaw plugins after cleanup:`n$($listAfter.Output)"
}
if ($listAfter.Output -match 'cogentnexus-rotation') {
    throw "CogentNexus plugin is still registered after uninstall/cleanup. Refusing reinstall."
}

Write-Host "Installing fresh CogentNexus from: $repoRoot"
if ($LinkPlugin) {
    & $installer -Workspace $Workspace -LinkPlugin
}
else {
    & $installer -Workspace $Workspace
}
if ($LASTEXITCODE -ne 0) { throw "Fresh CogentNexus installation failed" }

if (-not (Test-Path -LiteralPath $launcher)) {
    throw "Fresh install did not create cnx.cmd"
}

& $launcher status
if ($LASTEXITCODE -ne 0) { throw "CogentNexus post-install status failed" }
openclaw gateway status
if ($LASTEXITCODE -ne 0) { throw "Gateway post-install health check failed" }
openclaw plugins list
if ($LASTEXITCODE -ne 0) { throw "Plugin post-install inventory failed" }

Write-Host ""
Write-Host "CLEAN REINSTALL: PASS"
if (-not $NoBackup) { Write-Host "Backup: $backup" }
