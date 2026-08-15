[CmdletBinding()]
param(
    [string]$Workspace = (Join-Path $HOME ".openclaw\workspace"),
    [switch]$SkipPlugin,
    [switch]$SkipGatewayRestart,
    [switch]$SkipAgentsPolicy,
    [switch]$LinkPlugin
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $repoRoot "skills\cogentnexus"
$targetSkill = Join-Path $Workspace "skills\cogentnexus"
$stagedSkill = Join-Path $Workspace ".cogent\install-staging\cogentnexus"
$backupRoot = Join-Path $Workspace ".cogent\install-backups"
$pluginDir = Join-Path $repoRoot "plugins\cogentnexus-rotation"
$hostScript = Join-Path $targetSkill "scripts\host.py"

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

python (Join-Path $targetSkill "scripts\validate.py")
if ($LASTEXITCODE -ne 0) { throw "CogentNexus validation failed" }

if (-not $SkipAgentsPolicy) {
    python (Join-Path $repoRoot "scripts\manage_agents_policy.py") --workspace $Workspace --policy (Join-Path $targetSkill "templates\AGENTS.cogentnexus.md") --backup-root $backupRoot
    if ($LASTEXITCODE -ne 0) { throw "AGENTS.md policy integration failed" }
}

if (-not $SkipPlugin) {
    Push-Location $pluginDir
    try {
        npm ci
        if ($LASTEXITCODE -ne 0) { throw "npm ci failed" }
        npm run plugin:validate
        if ($LASTEXITCODE -ne 0) { throw "plugin validation failed" }
        if ($LinkPlugin) {
            openclaw plugins install --link . --force
        }
        else {
            $currentPaths = openclaw config get plugins.load.paths 2>$null
            if ($LASTEXITCODE -eq 0) {
                $filteredPaths = $currentPaths | python (Join-Path $repoRoot "scripts\filter_plugin_paths.py") --plugin-id cogentnexus-rotation
                if ($LASTEXITCODE -ne 0) { throw "failed to inspect existing plugin load paths" }
                openclaw config set plugins.load.paths $filteredPaths --strict-json --replace
                if ($LASTEXITCODE -ne 0) { throw "failed to remove an existing linked plugin path" }
            }
            openclaw plugins install . --force
        }
        if ($LASTEXITCODE -ne 0) { throw "plugin installation failed" }
    }
    finally { Pop-Location }
}

# Install a zero-dependency workspace launcher. It remains usable while OpenClaw is down.
$launcher = Join-Path $Workspace "cnx.cmd"
$hostEscaped = $hostScript.Replace('"','""')
$rootEscaped = (Join-Path $Workspace ".cogent").Replace('"','""')
$launcherText = "@echo off`r`npython `"$hostEscaped`" --root `"$rootEscaped`" %*`r`nexit /b %ERRORLEVEL%`r`n"
Set-Content -LiteralPath $launcher -Value $launcherText -Encoding ASCII -NoNewline
Write-Host "Installed Host Controller launcher to $launcher"

python $hostScript --root (Join-Path $Workspace ".cogent") init
if ($LASTEXITCODE -ne 0) { throw "CogentNexus Host initialization failed" }

if (-not $SkipGatewayRestart) {
    # Host enable configures Ticket-first mode, starts the native background supervisor,
    # verifies Gateway/provider readiness, and resumes recoverable committed work.
    python $hostScript --root (Join-Path $Workspace ".cogent") enable
    if ($LASTEXITCODE -ne 0) { throw "CogentNexus Host enable failed" }
}
else {
    Write-Host "Skipped Host enable because -SkipGatewayRestart was requested. Run .\cnx.cmd enable when ready."
}

openclaw gateway status
if ($LASTEXITCODE -ne 0 -and -not $SkipGatewayRestart) { throw "Gateway health check failed" }
python (Join-Path $targetSkill "scripts\runtime.py") supervisor doctor
if ($LASTEXITCODE -ne 0) { throw "CogentNexus supervisor check failed" }
Write-Host "CogentNexus installation completed successfully."
Write-Host "Control it with: $launcher status|start|stop|restart|disable|enable"
