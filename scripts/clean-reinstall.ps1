[CmdletBinding(SupportsShouldProcess=$true, ConfirmImpact="High")]
param(
    [string]$Workspace = (Join-Path $HOME ".openclaw\workspace"),
    [string]$BackupRoot = (Join-Path $env:LOCALAPPDATA "CogentNexus-OpenClaw-Clean-Reinstall-Backups"),
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
$handoffScript = Join-Path $repoRoot "scripts\clean_reinstall_handoff.py"
$applicationDataRoot = Join-Path $env:LOCALAPPDATA "CogentNexus-OpenClaw"

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

if (-not $NoBackup) {
    & python $handoffScript validate-boundary --app-data $applicationDataRoot --backup-root $BackupRoot | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Backup boundary is unsafe; refusing clean reinstall before mutation." }
}

$classificationJson = (& python $ownershipScript classify-install --workspace $Workspace --app-data $applicationDataRoot | Out-String)
if ($LASTEXITCODE -ne 0) { throw "Ownership is missing, partial, mixed, or invalid; refusing clean-reinstall before backup or deletion." }
$classification = $classificationJson | ConvertFrom-Json
if ($classification.mode -eq "legacy") { throw "Clean reinstall does not adopt a legacy namespace; run the v0.9.3 installer migration." }
if ($classification.mode -eq "upgrade") {
    $ownershipJson = (& python $ownershipScript verify --root $cnxRoot --workspace $Workspace | Out-String)
    if ($LASTEXITCODE -ne 0) { throw "Ownership manifest mismatch; refusing clean-reinstall mutation." }
    $ownership = $ownershipJson | ConvertFrom-Json
    $skill = [string]$ownership.skillPath
    $launcher = [string]$ownership.launcherPath
    $extension = [string]$ownership.pluginPath
}

$pluginInventoryBefore = Invoke-NativeCapture { openclaw plugins list --json }
if ($pluginInventoryBefore.Code -ne 0) { throw "Could not inspect OpenClaw plugins before ownership decision:`n$($pluginInventoryBefore.Output)" }
$taskBefore = Get-ScheduledTask -TaskName "CogentNexus-OpenClaw-Supervisor" -ErrorAction SilentlyContinue
if ($classification.mode -eq "fresh" -and ($pluginInventoryBefore.Output -match 'cogentnexus-openclaw' -or $taskBefore)) {
    throw "Registered plugin/task exists without a coherent ownership manifest; refusing clean-reinstall before backup or deletion."
}

if (-not $NoBackup) {
    New-Item -ItemType Directory -Force -Path $backup | Out-Null
    Copy-Backup $cnxRoot ".cogentnexus-openclaw"
    Copy-Backup $skill "skills\cogentnexus-openclaw"
    Copy-Backup $launcher "cnxclaw.cmd"
    Copy-Backup $extension "extension\cogentnexus-openclaw"
    Copy-Backup $applicationDataRoot "application-data\CogentNexus-OpenClaw"
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
Remove-OwnedPath $applicationDataRoot
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
try {
    if ($LinkPlugin) { & $installer -Workspace $Workspace -LinkPlugin }
    else { & $installer -Workspace $Workspace }
    if ($LASTEXITCODE -ne 0) { throw "Fresh CogentNexus-OpenClaw installation failed with exit code $LASTEXITCODE" }
}
catch {
    if (-not $NoBackup -and (Test-Path -LiteralPath $backup)) {
        & python $handoffScript write-recovery --backup $backup --workspace $Workspace --error $_.Exception.Message | Out-Null
        Write-Warning "Fresh install failed; backup and recovery record were preserved at $backup"
    }
    throw
}

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
