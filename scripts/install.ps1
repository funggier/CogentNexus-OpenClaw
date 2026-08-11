[CmdletBinding()]
param(
    [string]$Workspace = (Join-Path $HOME ".openclaw\workspace"),
    [switch]$SkipPlugin,
    [switch]$SkipGatewayRestart
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $repoRoot "skills\cogentnexus"
$targetSkill = Join-Path $Workspace "skills\cogentnexus"
$stagedSkill = Join-Path $Workspace ".cogent\install-staging\cogentnexus"
$backupRoot = Join-Path $Workspace ".cogent\install-backups"
$pluginDir = Join-Path $repoRoot "plugins\cogentnexus-rotation"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

Require-Command python
Require-Command openclaw
if (-not $SkipPlugin) { Require-Command npm }
python -c "import yaml" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "PyYAML is required. Run: python -m pip install -r requirements-dev.txt"
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetSkill) | Out-Null
if (Test-Path $targetSkill) {
    New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
    $backup = Join-Path $backupRoot "cogentnexus-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item -Recurse -Force -LiteralPath $targetSkill -Destination $backup
    Write-Host "Backed up existing skill to $backup"
}
if (Test-Path $stagedSkill) { Remove-Item -Recurse -Force -LiteralPath $stagedSkill }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $stagedSkill) | Out-Null
Copy-Item -Recurse -Force -LiteralPath $sourceSkill -Destination $stagedSkill
if (Test-Path $targetSkill) { Remove-Item -Recurse -Force -LiteralPath $targetSkill }
Move-Item -LiteralPath $stagedSkill -Destination $targetSkill
Write-Host "Installed CogentNexus skill to $targetSkill"

python (Join-Path $targetSkill "scripts\validate.py") --workspace-singleton
if ($LASTEXITCODE -ne 0) { throw "CogentNexus validation failed" }

if (-not $SkipPlugin) {
    Push-Location $pluginDir
    try {
        npm ci
        if ($LASTEXITCODE -ne 0) { throw "npm ci failed" }
        npm run plugin:validate
        if ($LASTEXITCODE -ne 0) { throw "plugin validation failed" }
        openclaw plugins install --link . --force
        if ($LASTEXITCODE -ne 0) { throw "plugin installation failed" }
    }
    finally { Pop-Location }
}

if (-not $SkipGatewayRestart) {
    openclaw gateway restart
    if ($LASTEXITCODE -ne 0) { throw "Gateway restart failed" }
}
openclaw gateway status
if ($LASTEXITCODE -ne 0) { throw "Gateway health check failed" }
python (Join-Path $targetSkill "scripts\phase3.py") supervisor doctor
if ($LASTEXITCODE -ne 0) { throw "CogentNexus supervisor check failed" }
Write-Host "CogentNexus installation completed successfully."
