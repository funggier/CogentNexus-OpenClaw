[CmdletBinding()]
param(
    [string]$Workspace = (Join-Path $HOME ".openclaw\workspace"),
    [ValidateSet("ollama")]
    [string]$Provider = "ollama",
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
$cliScript = Join-Path $targetSkill "scripts\cnx_v093.py"
$cogentRoot = Join-Path $Workspace ".cogent"
$controllerPath = Join-Path $cogentRoot "host\controller.json"
$existingLauncher = Join-Path $Workspace "cnx.cmd"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

function Get-ExistingCnxMode {
    if (-not (Test-Path -LiteralPath $controllerPath)) { return $null }
    try {
        $controller = Get-Content -LiteralPath $controllerPath -Raw | ConvertFrom-Json
    }
    catch {
        throw "Existing CogentNexus controller is unreadable; refusing install mutation: $($_.Exception.Message)"
    }
    $mode = [string]$controller.mode
    if ([string]::IsNullOrWhiteSpace($mode)) {
        throw "Existing CogentNexus controller has no mode; refusing install mutation."
    }
    return $mode
}

function Enter-NativeInstallBoundary {
    $mode = Get-ExistingCnxMode
    if ($null -eq $mode) { return }
    if ($mode -eq "passthrough") {
        Write-Host "Existing CogentNexus already PASSTHROUGH; pre-install native handoff not required."
        return
    }
    if ($mode -notin @("managed", "maintenance")) {
        throw "Existing CogentNexus mode '$mode' is not a recognized safe upgrade source; refusing install mutation."
    }
    if (-not (Test-Path -LiteralPath $existingLauncher)) {
        throw "Existing CogentNexus is $mode but launcher is missing: $existingLauncher. Refusing install mutation before native handoff."
    }

    Write-Host "Existing CogentNexus is $mode; entering PASSTHROUGH/native boundary before upgrade mutation."
    & $existingLauncher disable
    if ($LASTEXITCODE -ne 0) {
        throw "Existing CogentNexus disable failed; refusing install mutation."
    }
    $afterMode = Get-ExistingCnxMode
    if ($afterMode -ne "passthrough") {
        throw "Existing CogentNexus did not reach PASSTHROUGH after disable (mode=$afterMode); refusing install mutation."
    }
    Write-Host "Pre-install native handoff: PASS"
}

Write-Host "Installing CogentNexus v$version (Ollama-only)"
Write-Host "Workspace: $Workspace"
Write-Host "Provider: ollama"

if (($SkipPlugin -or $SkipAgentsPolicy) -and -not $SkipGatewayRestart) {
    throw "-SkipPlugin and -SkipAgentsPolicy are staging-only options. Use them with -SkipGatewayRestart; transactional MANAGED enable requires the bridge and managed policy."
}

Require-Command python
Require-Command openclaw
Require-Command ollama
if (-not $SkipPlugin) {
    Require-Command node
    Require-Command npm
}

python -c "import yaml" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "PyYAML is required. Run: python -m pip install 'PyYAML>=6.0,<7'"
}

# A v0.9.2 deployment may still be MANAGED by LM Studio.  Always use the old
# launcher first so it restores native OpenClaw before v0.9.3 replaces files.
# The new installation then enters MANAGED with Ollama only.
Enter-NativeInstallBoundary

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

python $hostScript --root $cogentRoot init
if ($LASTEXITCODE -ne 0) { throw "CogentNexus Host initialization failed" }

if ($SkipGatewayRestart) {
    $mode = if (Test-Path $controllerPath) { (Get-Content -LiteralPath $controllerPath -Raw | ConvertFrom-Json).mode } else { $null }
    if ($mode -ne "passthrough") {
        throw "-SkipGatewayRestart safe staging requires CogentNexus PASSTHROUGH mode. Run '.\cnx.cmd disable' before staging an upgrade."
    }
}

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

        node .\scripts\bootstrap-ticket-db.mjs --workspace $Workspace
        if ($LASTEXITCODE -ne 0) { throw "Ticket database bootstrap failed" }

        if ($LinkPlugin) {
            openclaw plugins install --link . --force
            if ($LASTEXITCODE -ne 0) { throw "linked plugin installation failed" }
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

            $packOutput = (& npm pack --json | Out-String)
            if ($LASTEXITCODE -ne 0) { throw "npm pack failed" }
            try { $packed = $packOutput | ConvertFrom-Json }
            catch { throw "npm pack returned invalid JSON: $($_.Exception.Message)" }
            $packedItems = @($packed)
            if ($packedItems.Count -ne 1 -or -not $packedItems[0].filename) {
                throw "npm pack did not return exactly one package artifact"
            }
            $packagePath = Join-Path $pluginDir ([string]$packedItems[0].filename)
            if (-not (Test-Path -LiteralPath $packagePath)) { throw "npm pack artifact not found: $packagePath" }
            try {
                openclaw plugins install ("npm-pack:" + $packagePath) --force
                if ($LASTEXITCODE -ne 0) { throw "plugin installation from npm-pack artifact failed" }
            }
            finally { Remove-Item -LiteralPath $packagePath -Force -ErrorAction SilentlyContinue }
        }

        openclaw plugins disable cogentnexus-rotation
        if ($LASTEXITCODE -ne 0) { throw "failed to leave CogentNexus plugin disabled after installation" }
    }
    finally { Pop-Location }
}

$launcher = Join-Path $Workspace "cnx.cmd"
$cliEscaped = $cliScript.Replace('"','""')
$rootEscaped = $cogentRoot.Replace('"','""')
$launcherText = "@echo off`r`npython `"$cliEscaped`" --root `"$rootEscaped`" %*`r`nexit /b %ERRORLEVEL%`r`n"
Set-Content -LiteralPath $launcher -Value $launcherText -Encoding ASCII -NoNewline
Write-Host "Installed CogentNexus launcher to $launcher"

if (-not $SkipGatewayRestart) {
    & python $cliScript --root $cogentRoot enable --provider ollama
    if ($LASTEXITCODE -ne 0) { throw "CogentNexus Host enable failed for Ollama" }
}
else {
    Write-Host "Skipped Host enable because -SkipGatewayRestart was requested."
    Write-Host "CogentNexus remains PASSTHROUGH with its plugin disabled."
    Write-Host "Run .\cnx.cmd enable when ready; v0.9.3 will use Ollama."
}

openclaw gateway status
if ($LASTEXITCODE -ne 0 -and -not $SkipGatewayRestart) { throw "Gateway health check failed" }

python (Join-Path $targetSkill "scripts\runtime.py") supervisor doctor
if ($LASTEXITCODE -ne 0) { throw "CogentNexus supervisor check failed" }

& python $cliScript --root $cogentRoot status
if ($LASTEXITCODE -ne 0) { throw "CogentNexus status check failed" }

Write-Host "CogentNexus v$version installation completed successfully (Ollama-only)."
Write-Host "Control it with: $launcher status|check|provider|start|stop|restart|gateway|ticket|session|policy|disable|enable|reset|uninstall"
