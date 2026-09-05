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
$artifactResolver = Join-Path $repoRoot "scripts\resolve-npm-pack-artifact.ps1"
$actionResolver = Join-Path $repoRoot "scripts\resolve-plugin-lifecycle-actions.ps1"
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

function Start-InstallerDiagnosticStage {
    param([Parameter(Mandatory = $true)][string]$Stage)

    $startedAt = [DateTimeOffset]::UtcNow
    $stopwatch = [Diagnostics.Stopwatch]::StartNew()
    Write-Host ("CNXCLAW_INSTALL_STAGE_START stage={0} utc={1}" -f $Stage, $startedAt.ToString("o"))
    return [pscustomobject]@{
        Stage = $Stage
        Stopwatch = $stopwatch
    }
}

function Complete-InstallerDiagnosticStage {
    param(
        [Parameter(Mandatory = $true)][object]$Context,
        [Parameter(Mandatory = $true)][int]$ExitCode
    )

    $Context.Stopwatch.Stop()
    $completedAt = [DateTimeOffset]::UtcNow
    Write-Host ("CNXCLAW_INSTALL_STAGE_COMPLETE stage={0} utc={1} elapsed_ms={2} exit_code={3}" -f $Context.Stage, $completedAt.ToString("o"), $Context.Stopwatch.ElapsedMilliseconds, $ExitCode)
}

function Invoke-NativeInstallerDiagnostic {
    param(
        [Parameter(Mandatory = $true)][string]$Executable,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    $savedErrorActionPreference = $ErrorActionPreference
    try {
        # Windows PowerShell 5.1 promotes native stderr to a terminating
        # NativeCommandError under Stop, truncating the child diagnostic.
        $ErrorActionPreference = "Continue"
        $output = (& $Executable @Arguments 2>&1 | Out-String)
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $savedErrorActionPreference
    }
    return [pscustomobject]@{ Output = $output; ExitCode = $exitCode }
}

function Get-BoundedInstallerDiagnostic {
    param([AllowNull()][string]$Output)

    $maximumCharacters = 4096
    $placeholder = "[no child diagnostic output captured]"
    $trimmed = if ($null -eq $Output) { "" } else { $Output.Trim() }
    if ([string]::IsNullOrWhiteSpace($trimmed)) { return $placeholder }
    if ($trimmed.Length -le $maximumCharacters) { return $trimmed }

    $truncationMarker = "`n...[child diagnostic truncated]...`n"
    $headCharacters = [Math]::Floor(($maximumCharacters - $truncationMarker.Length) / 2)
    $tailCharacters = $maximumCharacters - $truncationMarker.Length - $headCharacters
    return $trimmed.Substring(0, $headCharacters) + $truncationMarker + $trimmed.Substring($trimmed.Length - $tailCharacters)
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

Write-Host "Installing CogentNexus-OpenClaw v$version"
Write-Host "Workspace: $Workspace"

if (($SkipPlugin -or $SkipAgentsPolicy) -and -not $SkipGatewayRestart) {
    throw "-SkipPlugin and -SkipAgentsPolicy are staging-only options. Use them with -SkipGatewayRestart; transactional MANAGED enable requires the bridge and managed policy."
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

# CNX-20260825-067 D2 / CNX-20260826-073 R5: before classification, recover
# any incomplete fresh-install transaction left by a previously failed/crashed
# install. Fail-closed: a nonzero preflight stops the installer BEFORE
# classify-install; an unrecognized successful status also fails closed.
# Accepted successful statuses: CLEAN_FRESH, RECOVERED_FRESH, OWNERSHIP_PRESENT.
$recoveryJson = (& python $ownershipScript recovery-preflight --workspace $Workspace --app-data $applicationDataRoot 2>&1 | Out-String)
$recoveryExit = $LASTEXITCODE
if ($recoveryExit -ne 0) {
    throw "Recovery preflight failed (exit $recoveryExit); refusing to proceed to classification: $recoveryJson"
}
$recovery = $recoveryJson | ConvertFrom-Json
if ($recovery.status -notin @("CLEAN_FRESH", "RECOVERED_FRESH", "OWNERSHIP_PRESENT")) {
    throw "Recovery preflight returned unrecognized successful status '$($recovery.status)'; failing closed."
}
if ($recovery.status -eq "RECOVERED_FRESH") {
    Write-Host "Recovered incomplete fresh-install transaction; workspace returned to coherent fresh state."
}

# Inventory every legacy/new filesystem surface before the first mutation.
# classify-install --workspace is intentionally read-only and precedes mutation.
$expectedPluginFingerprint = $null
$pluginPrepared = $false
$classificationInventoryPath = Join-Path ([IO.Path]::GetTempPath()) ("cnx-plugin-inventory-" + [guid]::NewGuid().ToString("N") + ".json")
if (-not $SkipPlugin) {
    Push-Location $pluginDir
    try {
        npm ci
        if ($LASTEXITCODE -ne 0) { throw "candidate npm ci failed before classification" }
        npm run plugin:validate
        if ($LASTEXITCODE -ne 0) { throw "candidate plugin validation failed before classification" }
        $pluginPrepared = $true
    }
    finally { Pop-Location }
    $fingerprintJson = (& python $ownershipScript plugin-fingerprint --plugin-root $pluginDir --version $version | Out-String)
    if ($LASTEXITCODE -ne 0) { throw "Candidate source plugin fingerprint could not be proven; refusing mutation: $fingerprintJson" }
    $expectedPluginFingerprint = [string](($fingerprintJson | ConvertFrom-Json).fingerprint)
    if ($expectedPluginFingerprint -notmatch '^[0-9a-fA-F]{64}$') { throw "Candidate source plugin fingerprint is invalid; refusing mutation." }
}
$preInstallInventoryJson = (& openclaw plugins list --json | Out-String)
if ($LASTEXITCODE -ne 0) { throw "Could not prove current plugin registration inventory before installation." }
[IO.File]::WriteAllText($classificationInventoryPath, $preInstallInventoryJson, (New-Object Text.UTF8Encoding($false)))
$classificationArgs = @("classify-install", "--workspace", $Workspace, "--app-data", $applicationDataRoot)
if ($expectedPluginFingerprint) {
    $classificationArgs += @("--plugin-inventory-json", $classificationInventoryPath, "--expected-replacement-fingerprint", $expectedPluginFingerprint)
}
$classificationJson = (& python $ownershipScript @classificationArgs | Out-String)
$classificationExit = $LASTEXITCODE
Remove-Item -LiteralPath $classificationInventoryPath -Force -ErrorAction SilentlyContinue
if ($classificationExit -ne 0) { throw "Installation ownership is partial, mixed, ambiguous, or unproven; refusing mutation." }
$classification = $classificationJson | ConvertFrom-Json
$pendingRollover = [bool]$classification.pendingRollover
$pluginAlreadyExact = [bool]$classification.pluginAlreadyExact

$actionArgs = @{
    Mode = [string]$classification.mode
}
if ($pendingRollover) { $actionArgs.PendingRollover = $true }
if ($pluginAlreadyExact) { $actionArgs.PluginAlreadyExact = $true }
if ($SkipPlugin) { $actionArgs.SkipPlugin = $true }
$actionsJson = (& $actionResolver @actionArgs | Out-String)
$actions = $actionsJson | ConvertFrom-Json

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
$script:FreshPluginInstalled = $false
# CNX-20260826-069 B1/B3: one production fresh-transaction failure boundary.
# Every caught failure after successful transaction-begin and before successful
# transaction-commit routes through this helper, which performs all safe bounded
# recovery for effects created by THIS fresh attempt before rethrowing the
# original error. Supported OpenClaw surfaces are used for external effects:
# the plugin inverse applies only because fresh preflight proved no plugin was
# registered before this attempt ($script:FreshPluginInstalled is set only
# after a successful plugins install in this same attempt).
function Invoke-FreshTransactionRollback {
    param(
        [string]$WorkspacePath,
        [object]$OriginalError
    )
    if ($script:FreshPluginInstalled) {
        $savedPreference = $ErrorActionPreference
        try {
            $ErrorActionPreference = "Continue"
            $pluginUninstallOutput = openclaw plugins uninstall cogentnexus-openclaw --force 2>&1 | Out-String
            $pluginUninstallExit = $LASTEXITCODE
        }
        finally { $ErrorActionPreference = $savedPreference }
        if ($pluginUninstallExit -ne 0) {
            throw "Install failed AND the supported fresh-attempt plugin inverse failed. Install error: $OriginalError || Plugin uninstall error/state: $pluginUninstallOutput"
        }
    }
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

# CNX-20260826-069 B1 / CNX-20260826-070: single production caught-failure
# boundary. The try body is SHARED by fresh/upgrade/legacy modes; only the
# catch branches on $isFreshTransaction. Non-fresh failures propagate through
# the normal error path without any fresh rollback.
try {

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
    # moved below transaction-commit (CNX-20260826-069 B3): a failed
    # pre-commit installation can no longer leave a managed AGENTS block.
}

if (-not $SkipPlugin) {
    $ticketDbDiagnostic = Start-InstallerDiagnosticStage -Stage "ticket-db-bootstrap"
    node (Join-Path $pluginDir "scripts\bootstrap-ticket-db.mjs") --workspace $Workspace
    $ticketDbExit = $LASTEXITCODE
    Complete-InstallerDiagnosticStage -Context $ticketDbDiagnostic -ExitCode $ticketDbExit
    if ($ticketDbExit -ne 0) { throw "Ticket database bootstrap failed" }
}

if ($actions.installPlugin) {
    Push-Location $pluginDir
    try {
        if (-not $pluginPrepared) {
            npm ci
            if ($LASTEXITCODE -ne 0) { throw "npm ci failed" }
            npm run plugin:validate
            if ($LASTEXITCODE -ne 0) { throw "plugin validation failed" }
        }

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

        $rolloverTransactionPath = $null
        $packDiagnostic = Start-InstallerDiagnosticStage -Stage "plugin-npm-pack"
        $packOutput = (& npm pack --json | Out-String)
        $packExit = $LASTEXITCODE
        Complete-InstallerDiagnosticStage -Context $packDiagnostic -ExitCode $packExit
        if ($packExit -ne 0) { throw "npm pack failed" }
        $packagePath = $null
        try {
            . $artifactResolver
            $packedArtifact = Resolve-NpmPackArtifact -PackJson $packOutput -PluginDir $pluginDir
            $packagePath = [string]$packedArtifact.path
            if ($classification.mode -eq "upgrade" -and $actions.rolloverPlugin) {
                $rolloverStaging = Join-Path $cogentNexusOpenClawRoot "install-staging"
                New-Item -ItemType Directory -Force -Path $rolloverStaging | Out-Null
                $rolloverId = [guid]::NewGuid().ToString("N")
                $rolloverTransactionPath = Join-Path $rolloverStaging "plugin-rollover-transaction-$rolloverId.json"
                $rolloverPrepareDiagnostic = Start-InstallerDiagnosticStage -Stage "plugin-rollover-prepare"
                $prepareCapture = Invoke-NativeInstallerDiagnostic -Executable "python" -Arguments @(
                    (Join-Path $targetSkill "scripts\namespace_ownership.py"), "rollover-prepare",
                    "--root", $cogentNexusOpenClawRoot, "--workspace", $Workspace,
                    "--app-data", $applicationDataRoot,
                    "--expected-replacement-fingerprint", $expectedPluginFingerprint,
                    "--backup-token", $rolloverId, "--transaction", $rolloverTransactionPath
                )
                $prepareOutput = [string]$prepareCapture.Output
                $rolloverPrepareExit = [int]$prepareCapture.ExitCode
                Complete-InstallerDiagnosticStage -Context $rolloverPrepareDiagnostic -ExitCode $rolloverPrepareExit
                if ($rolloverPrepareExit -ne 0) {
                    $boundedPrepareDiagnostic = Get-BoundedInstallerDiagnostic -Output $prepareOutput
                    throw "ownership-safe plugin generation rollover pre-install proof failed; child diagnostic: $boundedPrepareDiagnostic"
                }
                if (-not (Test-Path -LiteralPath $rolloverTransactionPath)) { throw "rollover transaction proof was not persisted" }
            }
            $pluginInstallDiagnostic = Start-InstallerDiagnosticStage -Stage "plugin-install-local-package"
            openclaw plugins install $packagePath --force
            $pluginInstallExit = $LASTEXITCODE
            Complete-InstallerDiagnosticStage -Context $pluginInstallDiagnostic -ExitCode $pluginInstallExit
            if ($pluginInstallExit -ne 0) { throw "plugin installation from local package archive failed" }
            if ($isFreshTransaction) { $script:FreshPluginInstalled = $true }
        }
        finally {
            if ($packagePath -and (Test-Path -LiteralPath $packagePath)) {
                Remove-Item -LiteralPath $packagePath -Force -ErrorAction SilentlyContinue
            }
        }

        $pluginDisableDiagnostic = Start-InstallerDiagnosticStage -Stage "plugin-disable-post-install"
        openclaw plugins disable cogentnexus-openclaw
        $pluginDisableExit = $LASTEXITCODE
        Complete-InstallerDiagnosticStage -Context $pluginDisableDiagnostic -ExitCode $pluginDisableExit
        if ($pluginDisableExit -ne 0) { throw "failed to leave CogentNexus-OpenClaw plugin disabled after installation" }
        if ($rolloverTransactionPath) {
            $rolloverInventoryPath = Join-Path $rolloverStaging "plugin-inventory-$rolloverId.json"
            $rolloverInventory = (& openclaw plugins list --json | Out-String)
            if ($LASTEXITCODE -ne 0) { throw "could not prove active canonical plugin registration after replacement" }
            [System.IO.File]::WriteAllText($rolloverInventoryPath, $rolloverInventory, (New-Object System.Text.UTF8Encoding($false)))
            $rolloverFinalizeDiagnostic = Start-InstallerDiagnosticStage -Stage "plugin-rollover-finalize"
            & python (Join-Path $targetSkill "scripts\namespace_ownership.py") "rollover-finalize" "--transaction" $rolloverTransactionPath "--inventory-json" $rolloverInventoryPath | Out-Null
            $rolloverFinalizeExit = $LASTEXITCODE
            Complete-InstallerDiagnosticStage -Context $rolloverFinalizeDiagnostic -ExitCode $rolloverFinalizeExit
            if ($rolloverFinalizeExit -ne 0) { throw "ownership-safe plugin generation rollover finalization failed" }
        }
    }
    finally { Pop-Location }
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
$runtimeEnsureDiagnostic = Start-InstallerDiagnosticStage -Stage "owned-runtime-ensure"
$runtimeManifestJson = (& python $runtimeAuthorityScript ensure-runtime --application-data-root "$applicationDataRoot" | Out-String)
$runtimeEnsureExit = $LASTEXITCODE
Complete-InstallerDiagnosticStage -Context $runtimeEnsureDiagnostic -ExitCode $runtimeEnsureExit
if ($runtimeEnsureExit -ne 0) { throw "CogentNexus-OpenClaw-owned runtime provisioning failed; refusing to install." }
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
$installedPlugin = $pluginResolutionJson | ConvertFrom-Json
$installedPluginPath = [string]$installedPlugin.root
$installedPluginFingerprint = [string]$installedPlugin.fingerprint
if ($installedPluginFingerprint -notmatch '^[0-9a-fA-F]{64}$' -or $installedPluginFingerprint.ToLowerInvariant() -ne $expectedPluginFingerprint.ToLowerInvariant()) {
    throw "Installed plugin fingerprint does not match the expected candidate fingerprint; refusing managed activation."
}
$ownershipArguments = @((Join-Path $targetSkill "scripts\namespace_ownership.py"), "create", "--root", $cogentNexusOpenClawRoot, "--workspace", $Workspace, "--skill", $targetSkill, "--plugin-path", $installedPluginPath, "--launcher", $launcher, "--version", $version)
if ($migrationSource) { $ownershipArguments += @("--migration-source", $migrationSource) }
& $ownedPython @ownershipArguments | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Ownership manifest creation failed; refusing MANAGED authority." }
& $ownedPython (Join-Path $targetSkill "scripts\namespace_ownership.py") verify --root $cogentNexusOpenClawRoot --workspace $Workspace | Out-Null
if ($LASTEXITCODE -ne 0) { throw "New ownership manifest/artifacts failed exact verification; remaining PASSTHROUGH." }
if ($isFreshTransaction) {
    # CNX-20260826-068: commit only AFTER ownership create + exact verify.
    & python $ownershipScript transaction-commit --workspace $Workspace | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Fresh-install transaction commit failed after ownership verification." }
    Write-Host "Fresh-install transaction committed; recovery marker retired."
}
} catch {
    # CNX-20260826-069 B1 / CNX-20260826-070: only a fresh transaction rolls
    # back. Upgrade/legacy failures propagate through the normal error path
    # with no fresh rollback and no plugin inverse.
    if ($isFreshTransaction) {
        Invoke-FreshTransactionRollback -WorkspacePath $Workspace -OriginalError $_.Exception.Message
    }
    throw
}

if (-not $SkipAgentsPolicy) {
    python $hostScript --root $cogentNexusOpenClawRoot policy apply
    if ($LASTEXITCODE -ne 0) { throw "managed AGENTS.md policy integration failed" }
}

if (-not $SkipGatewayRestart) {
    & $ownedPython $cliScript --root $cogentNexusOpenClawRoot enable
    if ($LASTEXITCODE -ne 0) { throw "CogentNexus-OpenClaw Host enable failed" }
}
else {
    Write-Host "Skipped Host enable because -SkipGatewayRestart was requested."
    Write-Host "CogentNexus-OpenClaw remains PASSTHROUGH with its plugin disabled."
    Write-Host "Run .\cnxclaw.cmd enable when ready."
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

Write-Host "CogentNexus-OpenClaw v$version installation completed successfully."
Write-Host "Control it with: $launcher status|check|provider|start|stop|restart|gateway|ticket|session|policy|disable|enable|reset|uninstall"