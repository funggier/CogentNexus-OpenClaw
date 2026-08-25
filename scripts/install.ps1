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
$sourceSkill = Join-Path $repoRoot "skills\cogentnexus-openclaw"
$targetSkill = Join-Path $Workspace "skills\cogentnexus-openclaw"
$stagedSkill = Join-Path $Workspace ".cogentnexus-openclaw\install-staging\cogentnexus-openclaw"
$backupRoot = Join-Path $Workspace ".cogentnexus-openclaw\install-backups"
$pluginDir = Join-Path $repoRoot "plugins\cogentnexus-openclaw"
$hostScript = Join-Path $targetSkill "scripts\host_v091.py"
$cliScript = Join-Path $targetSkill "scripts\cnxclaw_v093.py"
$cogentNexusOpenClawRoot = Join-Path $Workspace ".cogentnexus-openclaw"
$controllerPath = Join-Path $cogentNexusOpenClawRoot "host\controller.json"
$existingLauncher = Join-Path $Workspace "cnxclaw.cmd"
$ownershipScript = Join-Path $sourceSkill "scripts\namespace_ownership.py"
$legacyRoot = Join-Path $Workspace ".cogent"
$legacyControllerPath = Join-Path $legacyRoot "host\controller.json"
$legacyLauncher = Join-Path $Workspace "cnx.cmd"
$migrationSource = $null
$localAppData = [Environment]::GetFolderPath([Environment+SpecialFolder]::LocalApplicationData)
$applicationDataRoot = Join-Path $localAppData "CogentNexus-OpenClaw"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

function Get-ExistingCnxMode {
    $modeController = if ($migrationSource) { $legacyControllerPath } else { $controllerPath }
    if (-not (Test-Path -LiteralPath $modeController)) { return $null }
    try {
        $controller = Get-Content -LiteralPath $modeController -Raw | ConvertFrom-Json
    }
    catch {
        throw "Existing CogentNexus-OpenClaw controller is unreadable; refusing install mutation: $($_.Exception.Message)"
    }
    $mode = [string]$controller.mode
    if ([string]::IsNullOrWhiteSpace($mode)) {
        throw "Existing CogentNexus-OpenClaw controller has no mode; refusing install mutation."
    }
    return $mode
}

function Enter-NativeInstallBoundary {
    $mode = Get-ExistingCnxMode
    if ($null -eq $mode) { return }
    if ($mode -eq "passthrough") {
        Write-Host "Existing CogentNexus-OpenClaw already PASSTHROUGH; pre-install native handoff not required."
        return
    }
    if ($mode -notin @("managed", "maintenance")) {
        throw "Existing CogentNexus-OpenClaw mode '$mode' is not a recognized safe upgrade source; refusing install mutation."
    }
    $handoffLauncher = if ($migrationSource) { $legacyLauncher } else { $existingLauncher }
    if (-not (Test-Path -LiteralPath $handoffLauncher)) {
        throw "Existing CogentNexus-OpenClaw is $mode but launcher is missing: $handoffLauncher. Refusing install mutation before native handoff."
    }

    Write-Host "Existing CogentNexus-OpenClaw is $mode; entering PASSTHROUGH/native boundary before upgrade mutation."
    & $handoffLauncher disable
    if ($LASTEXITCODE -ne 0) {
        throw "Existing CogentNexus-OpenClaw disable failed; refusing install mutation."
    }
    $afterMode = Get-ExistingCnxMode
    if ($afterMode -ne "passthrough") {
        throw "Existing CogentNexus-OpenClaw did not reach PASSTHROUGH after disable (mode=$afterMode); refusing install mutation."
    }
    Write-Host "Pre-install native handoff: PASS"
}

Write-Host "Installing CogentNexus-OpenClaw v$version (Ollama-only)"
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

# CNX-20260825-067 D2: before classification, recover any incomplete
# fresh-install transaction left by a previously failed/crashed install.
# Fail-closed: without a valid incomplete marker, unowned residue is refused.
$recoveryJson = (& python $ownershipScript recovery-preflight --workspace $Workspace --app-data $applicationDataRoot | Out-String)
if ($LASTEXITCODE -eq 0) {
    $recovery = $recoveryJson | ConvertFrom-Json
    if ($recovery.status -eq "RECOVERED_FRESH") {
        Write-Host "Recovered incomplete fresh-install transaction; workspace returned to coherent fresh state."
    }
}

# Inventory every legacy/new filesystem surface before the first mutation.
$classificationJson = (& python $ownershipScript classify-install --workspace $Workspace --app-data $applicationDataRoot | Out-String)
if ($LASTEXITCODE -ne 0) { throw "Installation ownership is partial, mixed, ambiguous, or unproven; refusing mutation." }
$classification = $classificationJson | ConvertFrom-Json
if ($classification.mode -eq "legacy") { $migrationSource = "legacy-cogentnexus-pre-v0.9.3" }
if ($LinkPlugin) {
    throw "-LinkPlugin is incompatible with ownership-safe managed installation; linked and npm-managed roots must not be mixed."
}
if ($SkipPlugin) {
    & python $ownershipScript preflight-skip-plugin --mode ([string]$classification.mode) | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "-SkipPlugin requires a coherent upgrade with an existing exact v0.9.3 plugin; refusing before mutation." }
}
if ($classification.mode -eq "fresh") {
    $newPluginInventory = openclaw plugins list --json 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) { throw "Could not prove current plugin registration inventory before installation." }
    $newTask = Get-ScheduledTask -TaskName "CogentNexus-OpenClaw-Supervisor" -ErrorAction SilentlyContinue
    if ($newPluginInventory -match 'cogentnexus-openclaw' -or $newTask) {
        throw "Current plugin/task registration exists without coherent ownership; refusing partial-state adoption."
    }
}

# CNX-20260826-068: production fresh-install transaction.
# Begin ONLY for fresh mode, after classification, before the first
# residue-capable mutation. The marker itself is the authorized first
# fresh mutation (it may create the CNX state root).
$isFreshTransaction = $false
function Invoke-FreshTransactionRollback {
    param(
        [string]$WorkspacePath,
        [object]$OriginalError
    )
    $rollbackOutput = & python $ownershipScript transaction-rollback --workspace $WorkspacePath 2>&1 | Out-String
    $rollbackExit = $LASTEXITCODE
    if ($rollbackExit -ne 0) {
        throw "Install failed AND bounded rollback failed. Install error: $OriginalError || Rollback error/state: $rollbackOutput"
    }
    Write-Host "Bounded fresh-install rollback completed; original install error follows."
    throw $OriginalError
}

if ($classification.mode -eq "fresh") {
    & python $ownershipScript transaction-begin --workspace $Workspace --app-data $applicationDataRoot | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Failed to begin the fresh-install transaction; refusing mutation." }
    $isFreshTransaction = $true
    Write-Host "Fresh-install transaction started; created owned paths will be recorded for bounded recovery."
}

# A v0.9.2 deployment may still be MANAGED by LM Studio.  Always use the old
# launcher first so it restores native OpenClaw before v0.9.3 replaces files.
# The new installation then enters MANAGED with Ollama only.
Enter-NativeInstallBoundary

if ($migrationSource) {
    $migrationBackupRoot = Join-Path $localAppData "CogentNexus-OpenClaw\migration-backups\v$version-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    New-Item -ItemType Directory -Force -Path $migrationBackupRoot | Out-Null
    foreach ($legacyPath in @($legacyRoot, (Join-Path $Workspace "skills\cogentnexus"), $legacyLauncher)) {
        if (Test-Path -LiteralPath $legacyPath) { Copy-Item -Recurse -Force -LiteralPath $legacyPath -Destination $migrationBackupRoot }
    }
    Write-Host "Backed up proven legacy installation to $migrationBackupRoot"
    trap {
        $failure = $_.Exception.Message
        $partialLauncher = Join-Path $Workspace "cnxclaw.cmd"
        if (Test-Path -LiteralPath $partialLauncher) {
            try { & $partialLauncher disable | Out-Null } catch { }
        }
        $recoveryReport = [ordered]@{
            status = "INTERRUPTED"
            productId = "cogentnexus-openclaw"
            safetyState = "PASSTHROUGH_REQUESTED"
            error = $failure
            backup = $migrationBackupRoot
            legacyRoot = $legacyRoot
            newRoot = $cogentNexusOpenClawRoot
            humanDecisionRequired = $true
        }
        $recoveryReport | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $migrationBackupRoot "migration-report.json") -Encoding UTF8
        Write-Host "CogentNexus-OpenClaw migration interrupted; recoverable report: $(Join-Path $migrationBackupRoot 'migration-report.json')" -ForegroundColor Red
        break
    }
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetSkill) | Out-Null
if (Test-Path $targetSkill) {
    New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
  $backup = Join-Path $backupRoot "cogentnexus-openclaw-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item -Recurse -Force -LiteralPath $targetSkill -Destination $backup
    Write-Host "Backed up existing skill to $backup"
}

if (Test-Path $stagedSkill) { Remove-Item -Recurse -Force -LiteralPath $stagedSkill }
if ($isFreshTransaction) {
    # Record owned paths BEFORE/at creation so a crash cannot leave an
    # unrecorded fresh artifact. Recording is bounded to exact CNX roots.
    & python $ownershipScript transaction-record --workspace $Workspace --path $targetSkill | Out-Null
    & python $ownershipScript transaction-record --workspace $Workspace --path $cogentNexusOpenClawRoot | Out-Null
    if (-not (Test-Path $applicationDataRoot)) {
        & python $ownershipScript transaction-record --workspace $Workspace --path $applicationDataRoot | Out-Null
    }
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $stagedSkill) | Out-Null
Copy-Item -Recurse -Force -LiteralPath $sourceSkill -Destination $stagedSkill
if (Test-Path $targetSkill) { Remove-Item -Recurse -Force -LiteralPath $targetSkill }
Move-Item -LiteralPath $stagedSkill -Destination $targetSkill
Write-Host "Installed CogentNexus-OpenClaw skill to $targetSkill"

python (Join-Path $targetSkill "scripts\validate.py")
if ($LASTEXITCODE -ne 0) { throw "CogentNexus-OpenClaw validation failed" }

python $hostScript --root $cogentNexusOpenClawRoot init
if ($LASTEXITCODE -ne 0) { throw "CogentNexus-OpenClaw Host initialization failed" }

if ($SkipGatewayRestart) {
    $mode = if (Test-Path $controllerPath) { (Get-Content -LiteralPath $controllerPath -Raw | ConvertFrom-Json).mode } else { $null }
    if ($mode -ne "passthrough") {
        throw "-SkipGatewayRestart safe staging requires CogentNexus-OpenClaw PASSTHROUGH mode. Run '.\cnxclaw.cmd disable' before staging an upgrade."
    }
}

if (-not $SkipAgentsPolicy) {
    python $hostScript --root $cogentNexusOpenClawRoot policy apply
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
            $filteredPaths = $currentPaths | python (Join-Path $repoRoot "scripts\filter_plugin_paths.py") --plugin-id cogentnexus-openclaw
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

        openclaw plugins disable cogentnexus-openclaw
        if ($LASTEXITCODE -ne 0) { throw "failed to leave CogentNexus-OpenClaw plugin disabled after installation" }
    }
    finally { Pop-Location }

    if ($classification.mode -eq "upgrade") {
        $rolloverStaging = Join-Path $cogentNexusOpenClawRoot "install-staging"
        New-Item -ItemType Directory -Force -Path $rolloverStaging | Out-Null
        $rolloverId = [guid]::NewGuid().ToString("N")
        $rolloverInventoryPath = Join-Path $rolloverStaging "plugin-inventory-$rolloverId.json"
        $rolloverApplyInventoryPath = Join-Path $rolloverStaging "plugin-inventory-apply-$rolloverId.json"
        $rolloverPlanPath = Join-Path $rolloverStaging "plugin-rollover-plan-$rolloverId.json"
        try {
            $rolloverInventory = (& openclaw plugins list --json | Out-String)
            if ($LASTEXITCODE -ne 0) { throw "could not prove active canonical plugin registration after replacement" }
            [System.IO.File]::WriteAllText(
                $rolloverInventoryPath,
                $rolloverInventory,
                (New-Object System.Text.UTF8Encoding($false))
            )
            $rolloverPlanOutput = (& python (Join-Path $targetSkill "scripts\namespace_ownership.py") "rollover-plan" "--root" $cogentNexusOpenClawRoot "--workspace" $Workspace "--app-data" $applicationDataRoot "--inventory-json" $rolloverInventoryPath "--plan" $rolloverPlanPath | Out-String)
            if ($LASTEXITCODE -ne 0) { throw "ownership-safe plugin generation rollover plan was rejected" }
            $rolloverPlanSha256 = [string](($rolloverPlanOutput | ConvertFrom-Json).planSha256)
            if ([string]::IsNullOrWhiteSpace($rolloverPlanSha256)) { throw "plugin generation rollover plan hash was not observed" }
            $rolloverApplyInventory = (& openclaw plugins list --json | Out-String)
            if ($LASTEXITCODE -ne 0) { throw "could not re-prove active canonical plugin registration immediately before rollover apply" }
            [System.IO.File]::WriteAllText(
                $rolloverApplyInventoryPath,
                $rolloverApplyInventory,
                (New-Object System.Text.UTF8Encoding($false))
            )
            & python (Join-Path $targetSkill "scripts\namespace_ownership.py") "rollover-apply" "--plan" $rolloverPlanPath "--plan-sha256" $rolloverPlanSha256 "--inventory-json" $rolloverApplyInventoryPath | Out-Null
            if ($LASTEXITCODE -ne 0) { throw "ownership-safe plugin generation rollover apply failed" }
            Write-Host "Retired the exact prior plugin generation into the CogentNexus-OpenClaw backup boundary."
        }
        finally {
            Remove-Item -LiteralPath $rolloverInventoryPath,$rolloverApplyInventoryPath,$rolloverPlanPath -Force -ErrorAction SilentlyContinue
        }
    }
}

$launcher = Join-Path $Workspace "cnxclaw.cmd"
$cliEscaped = $cliScript.Replace('"','""')
$rootEscaped = $cogentNexusOpenClawRoot.Replace('"','""')
# One explicit runtime-authority script resolution (Task CNX-20260825-065 B5).
$runtimeAuthorityScript = Join-Path $targetSkill "scripts\runtime_authority.py"
if (-not (Test-Path -LiteralPath $runtimeAuthorityScript)) {
    throw "Runtime authority script not found: $runtimeAuthorityScript"
}
# Unconditional ensure/validate on every install/install-over (B6): a stale
# runtime with a missing manifest or broken interpreter must be repaired or
# fail closed BEFORE any durable launcher/task definition is written.
$runtimeManifestJson = (& python $runtimeAuthorityScript ensure-runtime --application-data-root "$applicationDataRoot" | Out-String)
if ($LASTEXITCODE -ne 0) { throw "CogentNexus-owned runtime provisioning failed; refusing to install." }
$runtimeManifest = $runtimeManifestJson | ConvertFrom-Json
$ownedPython = [string]$runtimeManifest.foregroundInterpreter
$ownedPythonw = [string]$runtimeManifest.backgroundInterpreter
if (-not (Test-Path -LiteralPath $ownedPython)) { throw "Owned foreground interpreter not found after provisioning: $ownedPython" }
if (-not (Test-Path -LiteralPath $ownedPythonw)) { throw "Owned background interpreter not found after provisioning: $ownedPythonw" }
Write-Host "Owned runtime interpreter: $ownedPython"
$launcherText = "@echo off`r`n`"$ownedPython`" `"$cliEscaped`" --root `"$rootEscaped`" %*`r`nexit /b %ERRORLEVEL%`r`n"
if ($isFreshTransaction) {
    & python $ownershipScript transaction-record --workspace $Workspace --path $launcher | Out-Null
}
Set-Content -LiteralPath $launcher -Value $launcherText -Encoding ASCII -NoNewline
Write-Host "Installed CogentNexus-OpenClaw launcher to $launcher"

$pluginResolutionJson = (& $ownedPython (Join-Path $targetSkill "scripts\namespace_ownership.py") resolve-plugin --openclaw-state (Split-Path -Parent $Workspace) --version $version | Out-String)
if ($LASTEXITCODE -ne 0) { throw "Installed plugin identity/path is missing, conflicting, or ambiguous; refusing ownership." }
$installedPluginPath = [string](($pluginResolutionJson | ConvertFrom-Json).root)
$ownershipArguments = @((Join-Path $targetSkill "scripts\namespace_ownership.py"), "create", "--root", $cogentNexusOpenClawRoot, "--workspace", $Workspace, "--skill", $targetSkill, "--plugin-path", $installedPluginPath, "--launcher", $launcher, "--version", $version)
if ($migrationSource) { $ownershipArguments += @("--migration-source", $migrationSource) }
& $ownedPython @ownershipArguments | Out-Null
if ($LASTEXITCODE -ne 0) {
    if ($isFreshTransaction) { Invoke-FreshTransactionRollback -WorkspacePath $Workspace -OriginalError "Ownership manifest creation failed; refusing MANAGED authority." }
    throw "Ownership manifest creation failed; refusing MANAGED authority."
}
& $ownedPython (Join-Path $targetSkill "scripts\namespace_ownership.py") verify --root $cogentNexusOpenClawRoot --workspace $Workspace | Out-Null
if ($LASTEXITCODE -ne 0) {
    if ($isFreshTransaction) { Invoke-FreshTransactionRollback -WorkspacePath $Workspace -OriginalError "New ownership manifest/artifacts failed exact verification; remaining PASSTHROUGH." }
    throw "New ownership manifest/artifacts failed exact verification; remaining PASSTHROUGH."
}
if ($isFreshTransaction) {
    # CNX-20260826-068: commit only AFTER ownership create + exact verify.
    & python $ownershipScript transaction-commit --workspace $Workspace | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Fresh-install transaction commit failed after ownership verification." }
    Write-Host "Fresh-install transaction committed; recovery marker retired."
}

if (-not $SkipGatewayRestart) {
    & $ownedPython $cliScript --root $cogentNexusOpenClawRoot enable --provider ollama
    if ($LASTEXITCODE -ne 0) { throw "CogentNexus-OpenClaw Host enable failed for Ollama" }
}
else {
    Write-Host "Skipped Host enable because -SkipGatewayRestart was requested."
    Write-Host "CogentNexus-OpenClaw remains PASSTHROUGH with its plugin disabled."
    Write-Host "Run .\cnxclaw.cmd enable when ready; v0.9.3 will use Ollama."
}

openclaw gateway status
if ($LASTEXITCODE -ne 0 -and -not $SkipGatewayRestart) { throw "Gateway health check failed" }

& $ownedPython (Join-Path $targetSkill "scripts\runtime.py") supervisor doctor
if ($LASTEXITCODE -ne 0) { throw "CogentNexus-OpenClaw supervisor check failed" }

& $ownedPython $cliScript --root $cogentNexusOpenClawRoot status
if ($LASTEXITCODE -ne 0) { throw "CogentNexus-OpenClaw status check failed" }

if ($migrationSource) {
    $savedPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $legacyUninstallOutput = openclaw plugins uninstall cogentnexus-rotation --force 2>&1 | Out-String
        $legacyUninstallExit = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $savedPreference }
    if ($legacyUninstallExit -ne 0) { throw "Legacy plugin uninstall failed ($legacyUninstallExit): $legacyUninstallOutput" }

    $legacyPluginInventory = openclaw plugins list --json 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0 -or $legacyPluginInventory -match 'cogentnexus-rotation') {
        throw "Legacy plugin registration remains after uninstall; refusing migration success."
    }
    $legacyLoadPaths = openclaw config get plugins.load.paths 2>$null | Out-String
    $legacyLoadPathExit = $LASTEXITCODE
    if ($legacyLoadPathExit -eq 0 -and $legacyLoadPaths -match 'cogentnexus-rotation') {
        throw "Legacy plugin load path remains after uninstall; refusing migration success."
    }
    $legacyConfigEntry = openclaw config get plugins.entries.cogentnexus-rotation 2>$null | Out-String
    if ($LASTEXITCODE -eq 0 -and $legacyConfigEntry.Trim() -notin @('', 'null')) {
        throw "Legacy plugin config entry remains after uninstall; refusing migration success."
    }
    foreach ($legacyPath in @($legacyRoot, (Join-Path $Workspace "skills\cogentnexus"), $legacyLauncher)) {
        if (Test-Path -LiteralPath $legacyPath) { Remove-Item -Recurse -Force -LiteralPath $legacyPath }
    }
    $oldTask = Get-ScheduledTask -TaskName "CogentNexus Supervisor" -ErrorAction SilentlyContinue
    if ($oldTask) { Unregister-ScheduledTask -TaskName "CogentNexus Supervisor" -Confirm:$false }
    $remainingLegacy = @($legacyRoot, (Join-Path $Workspace "skills\cogentnexus"), $legacyLauncher) | Where-Object { Test-Path -LiteralPath $_ }
    if ($remainingLegacy.Count -ne 0 -or (Get-ScheduledTask -TaskName "CogentNexus Supervisor" -ErrorAction SilentlyContinue)) {
        throw "Legacy operational artifacts remain after cleanup; refusing migration success: $remainingLegacy"
    }
    Write-Host "Removed legacy aliases after the new namespace passed validation."
}

Write-Host "CogentNexus-OpenClaw v$version installation completed successfully (Ollama-only)."
Write-Host "Control it with: $launcher status|check|provider|start|stop|restart|gateway|ticket|session|policy|disable|enable|reset|uninstall"
