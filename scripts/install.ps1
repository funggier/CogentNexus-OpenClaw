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
$versionFile = Join-Path $repoRoot "VERSION"
$version = if (Test-Path $versionFile) { (Get-Content -LiteralPath $versionFile -Raw).Trim() } else { "unknown" }
$sourceSkill = Join-Path $repoRoot "skills\cogentnexus"
$targetSkill = Join-Path $Workspace "skills\cogentnexus"
$stagedSkill = Join-Path $Workspace ".cogent\install-staging\cogentnexus"
$backupRoot = Join-Path $Workspace ".cogent\install-backups"
$pluginDir = Join-Path $repoRoot "plugins\cogentnexus-rotation"
$hostScript = Join-Path $targetSkill "scripts\host_v091.py"
$hostControlScript = Join-Path $targetSkill "scripts\host_control_v091.py"
$cogentRoot = Join-Path $Workspace ".cogent"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

Write-Host "Installing CogentNexus v$version"
Write-Host "Workspace: $Workspace"

if (($SkipPlugin -or $SkipAgentsPolicy) -and -not $SkipGatewayRestart) {
    throw "-SkipPlugin and -SkipAgentsPolicy are staging-only options in v0.9.1. Use them with -SkipGatewayRestart; transactional MANAGED enable requires the bridge and managed policy."
}

Require-Command python
Require-Command openclaw
if (-not $SkipPlugin) {
    Require-Command node
    Require-Command npm
}

python -c "import yaml" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "PyYAML is required. Run: python -m pip install 'PyYAML>=6.0,<7'"
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

# v0.9.1 fresh initialization is PASSTHROUGH. MANAGED is committed only after
# the transactional Host enable sequence verifies every activation stage.
python $hostScript --root $cogentRoot init
if ($LASTEXITCODE -ne 0) { throw "CogentNexus Host initialization failed" }

if ($SkipGatewayRestart) {
    $controllerPath = Join-Path $cogentRoot "host\controller.json"
    $mode = if (Test-Path $controllerPath) { (Get-Content -LiteralPath $controllerPath -Raw | ConvertFrom-Json).mode } else { $null }
    if ($mode -ne "passthrough") {
        throw "-SkipGatewayRestart safe staging requires CogentNexus PASSTHROUGH mode. Run '.\cnx.cmd disable' before staging an upgrade."
    }
}

# Transactional enable reapplies the registered policy before committing
# MANAGED; in PASSTHROUGH this command is intentionally a no-op.
if (-not $SkipAgentsPolicy) {
    python $hostScript --root $cogentRoot policy apply
    if ($LASTEXITCODE -ne 0) { throw "managed AGENTS.md policy integration failed" }
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
            $currentPaths = $null
            $pathExit = 1
            $savedErrorActionPreference = $ErrorActionPreference
            try {
                $ErrorActionPreference = "Continue"
                $currentPaths = openclaw config get plugins.load.paths 2>$null
                $pathExit = $LASTEXITCODE
            }
            finally { $ErrorActionPreference = $savedErrorActionPreference }
            if ($pathExit -eq 0) {
                $filteredPaths = $currentPaths | python (Join-Path $repoRoot "scripts\filter_plugin_paths.py") --plugin-id cogentnexus-rotation
                if ($LASTEXITCODE -ne 0) { throw "failed to inspect existing plugin load paths" }
                openclaw config set plugins.load.paths $filteredPaths --strict-json --replace
                if ($LASTEXITCODE -ne 0) { throw "failed to remove an existing linked plugin path" }
            }
            openclaw plugins install . --force
        }
        if ($LASTEXITCODE -ne 0) { throw "plugin installation failed" }

        # Installation may restart Gateway through OpenClaw's native plugin
        # lifecycle. Keep CNX inactive until transactional enable stages valid
        # config and commits MANAGED.
        openclaw plugins disable cogentnexus-rotation
        if ($LASTEXITCODE -ne 0) { throw "failed to leave CogentNexus plugin disabled after installation" }
    }
    finally { Pop-Location }
}

$launcher = Join-Path $Workspace "cnx.cmd"
$hostControlEscaped = $hostControlScript.Replace('"','""')
$rootEscaped = $cogentRoot.Replace('"','""')
$launcherText = "@echo off`r`npython `"$hostControlEscaped`" --root `"$rootEscaped`" %*`r`nexit /b %ERRORLEVEL%`r`n"
Set-Content -LiteralPath $launcher -Value $launcherText -Encoding ASCII -NoNewline
Write-Host "Installed Host Controller launcher to $launcher"

if (-not $SkipGatewayRestart) {
    python $hostControlScript --root $cogentRoot enable
    if ($LASTEXITCODE -ne 0) { throw "CogentNexus Host enable failed" }
}
else {
    Write-Host "Skipped Host enable because -SkipGatewayRestart was requested."
    Write-Host "Note: OpenClaw plugin installation itself may have restarted Gateway as part of its native plugin lifecycle."
    Write-Host "CogentNexus remains PASSTHROUGH with its plugin disabled. Run .\cnx.cmd enable from the workspace when ready."
}

openclaw gateway status
if ($LASTEXITCODE -ne 0 -and -not $SkipGatewayRestart) { throw "Gateway health check failed" }

python (Join-Path $targetSkill "scripts\runtime.py") supervisor doctor
if ($LASTEXITCODE -ne 0) { throw "CogentNexus supervisor check failed" }

python $hostScript --root $cogentRoot status
if ($LASTEXITCODE -ne 0) { throw "CogentNexus Host status check failed" }

Write-Host "CogentNexus v$version installation completed successfully."
Write-Host "Control it with: $launcher status|start|stop|restart|gateway|ticket|session|policy|disable|enable"
