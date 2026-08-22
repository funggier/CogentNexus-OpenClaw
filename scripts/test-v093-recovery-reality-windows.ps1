[CmdletBinding()]
param(
    [ValidateSet('ollama','lmstudio')]
    [string]$Provider = 'lmstudio',

    [ValidateSet('baseline','gateway-crash','provider-crash','operator-stop','all')]
    [string[]]$Scenario = @('all'),

    [switch]$InstallRelease,
    [string]$ReleaseTag = 'v0.9.2',
    [string]$ExpectedReleaseCommit = '986f3c7be8389866f3ffe4f9b372ff1264ddbe8e',
    [switch]$RunDisruptive,
    [int]$RecoveryFuseSeconds = 420,
    [int]$IntentionalStopObservationSeconds = 10,
    [switch]$SyntaxOnly
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($SyntaxOnly) {
    Write-Host 'CogentNexus v0.9.3 Recovery Reality harness syntax/load: PASS'
    exit 0
}

if ($env:OS -ne 'Windows_NT') {
    throw 'This recovery-reality harness is Windows-only.'
}
if ($RecoveryFuseSeconds -lt 30 -or $RecoveryFuseSeconds -gt 1800) {
    throw 'RecoveryFuseSeconds must be between 30 and 1800 seconds.'
}
if ($IntentionalStopObservationSeconds -lt 5 -or $IntentionalStopObservationSeconds -gt 120) {
    throw 'IntentionalStopObservationSeconds must be between 5 and 120 seconds.'
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Downloads = Join-Path $HOME 'Downloads'
$Workspace = Join-Path $HOME '.openclaw\workspace'
$Cnx = Join-Path $Workspace 'cnx.cmd'
$OpenClawConfig = if ($env:OPENCLAW_CONFIG_PATH) {
    [IO.Path]::GetFullPath((Join-Path (Get-Location) $env:OPENCLAW_CONFIG_PATH))
} else {
    Join-Path $HOME '.openclaw\openclaw.json'
}

New-Item -ItemType Directory -Force -Path $Downloads | Out-Null
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$LogPath = Join-Path $Downloads "CNX_V093_RECOVERY_REALITY_$Stamp.txt"
$JsonPath = Join-Path $Downloads "CNX_V093_RECOVERY_REALITY_$Stamp.json"
$RunRoot = Join-Path $Downloads "CNX_V093_RECOVERY_REALITY_$Stamp"
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null

$ExpandedScenarios = New-Object System.Collections.Generic.List[string]
foreach ($item in $Scenario) {
    if ($item -eq 'all') {
        foreach ($name in @('baseline','gateway-crash','provider-crash','operator-stop')) {
            if (-not $ExpandedScenarios.Contains($name)) { [void]$ExpandedScenarios.Add($name) }
        }
    } elseif (-not $ExpandedScenarios.Contains($item)) {
        [void]$ExpandedScenarios.Add($item)
    }
}

$DisruptiveScenarios = @($ExpandedScenarios | Where-Object { $_ -ne 'baseline' })
if ($DisruptiveScenarios.Count -gt 0 -and -not $RunDisruptive) {
    throw "Scenarios $($DisruptiveScenarios -join ', ') intentionally kill/restart runtime processes. Re-run with -RunDisruptive after reviewing the suite."
}

$Evidence = [ordered]@{
    schemaVersion = 1
    suite = 'v0.9.3-recovery-reality-windows'
    startedAt = (Get-Date).ToString('o')
    provider = $Provider
    scenarios = @($ExpandedScenarios)
    installRelease = [bool]$InstallRelease
    releaseTag = $ReleaseTag
    expectedReleaseCommit = $ExpectedReleaseCommit
    recoveryFuseSeconds = $RecoveryFuseSeconds
    intentionalStopObservationSeconds = $IntentionalStopObservationSeconds
    repoRoot = $RepoRoot
    runRoot = $RunRoot
    openclawConfig = $OpenClawConfig
    steps = @()
    result = 'running'
    error = $null
}

function Save-Evidence {
    $Evidence | ConvertTo-Json -Depth 50 | Set-Content -Path $JsonPath -Encoding UTF8
}

function Write-Evidence {
    param([string]$Message)
    $line = "[$((Get-Date).ToString('o'))] $Message"
    Write-Host $line
    Add-Content -Path $LogPath -Value $line -Encoding UTF8
}

function Add-Step {
    param(
        [string]$Name,
        [string]$Status,
        $Data
    )
    $Evidence.steps += [ordered]@{
        name = $Name
        status = $Status
        at = (Get-Date).ToString('o')
        data = $Data
    }
    Save-Evidence
}

function Quote-CmdArgument {
    param([string]$Value)
    if ($Value -notmatch '[\s"]') { return $Value }
    return '"' + ($Value -replace '"','\"') + '"'
}

function Invoke-RootProcess {
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$Arguments = @(),
        [int[]]$AllowedExitCodes = @(0),
        [int]$TimeoutSeconds = 900,
        [switch]$NoStep
    )

    Write-Evidence "START $Name :: $FilePath $($Arguments -join ' ')"
    $stdout = Join-Path $env:TEMP "cnx-v093-$Stamp-$([guid]::NewGuid().ToString('N')).out.txt"
    $stderr = Join-Path $env:TEMP "cnx-v093-$Stamp-$([guid]::NewGuid().ToString('N')).err.txt"
    $sw = [Diagnostics.Stopwatch]::StartNew()
    try {
        $proc = Start-Process -FilePath $FilePath -ArgumentList $Arguments -PassThru -NoNewWindow `
            -RedirectStandardOutput $stdout -RedirectStandardError $stderr

        # Windows PowerShell 5.1 can expose a null ExitCode for a quickly-exiting
        # Start-Process -PassThru child unless the native process handle is cached.
        $null = $proc.Handle

        if (-not $proc.WaitForExit($TimeoutSeconds * 1000)) {
            Write-Evidence "TIMEOUT $Name :: killing root process tree pid=$($proc.Id)"
            & taskkill.exe /PID $proc.Id /T /F 2>&1 | Add-Content -Path $LogPath -Encoding UTF8
            throw "$Name exceeded bounded observation timeout ${TimeoutSeconds}s."
        }
        $proc.WaitForExit()
        $proc.Refresh()
        if (-not $proc.HasExited) { throw "$Name root process did not reach exited state." }
        $exitCode = [int]$proc.ExitCode
        $sw.Stop()

        $outText = if (Test-Path $stdout) { Get-Content $stdout -Raw } else { '' }
        $errText = if (Test-Path $stderr) { Get-Content $stderr -Raw } else { '' }
        if ($outText) { Add-Content -Path $LogPath -Value $outText -Encoding UTF8 }
        if ($errText) { Add-Content -Path $LogPath -Value $errText -Encoding UTF8 }

        $ok = $AllowedExitCodes -contains $exitCode
        if (-not $NoStep) {
            Add-Step $Name $(if ($ok) { 'PASS' } else { 'FAIL' }) ([ordered]@{
                command = @($FilePath) + $Arguments
                exitCode = $exitCode
                durationSeconds = [math]::Round($sw.Elapsed.TotalSeconds, 3)
                stdout = $outText
                stderr = $errText
            })
        }
        if (-not $ok) { throw "$Name failed with exit code $exitCode." }
        Write-Evidence "PASS $Name"
        return [pscustomobject]@{
            ExitCode = $exitCode
            Stdout = $outText
            Stderr = $errText
            DurationSeconds = [math]::Round($sw.Elapsed.TotalSeconds, 3)
        }
    }
    finally {
        Remove-Item $stdout,$stderr -Force -ErrorAction SilentlyContinue
    }
}

function Read-OpenClawConfig {
    if (-not (Test-Path $OpenClawConfig)) { throw "OpenClaw config not found: $OpenClawConfig" }
    return Get-Content $OpenClawConfig -Raw | ConvertFrom-Json
}

function Get-GatewayPort {
    $cfg = Read-OpenClawConfig
    if ($null -ne $cfg.gateway -and $null -ne $cfg.gateway.port) {
        return [int]$cfg.gateway.port
    }
    return 18789
}

function Get-ProviderPort {
    if ($Provider -eq 'lmstudio') { return 1234 }
    return 11434
}

function Get-ListenerSnapshot {
    param([int]$Port)
    $rows = @()
    try {
        $rows = @(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction Stop)
    }
    catch {
        $rows = @()
    }
    if ($rows.Count -eq 0) {
        return [ordered]@{ port = $Port; listening = $false; pid = $null; processName = $null }
    }
    $pidValue = [int]$rows[0].OwningProcess
    $processName = $null
    try { $processName = (Get-Process -Id $pidValue -ErrorAction Stop).ProcessName } catch {}
    return [ordered]@{
        port = $Port
        listening = $true
        pid = $pidValue
        processName = $processName
    }
}

function Wait-ListenerState {
    param(
        [string]$Label,
        [int]$Port,
        [bool]$Listening,
        [Nullable[int]]$DifferentFromPid = $null,
        [int]$FuseSeconds = $RecoveryFuseSeconds
    )

    $deadline = (Get-Date).AddSeconds($FuseSeconds)
    $last = $null
    while ((Get-Date) -lt $deadline) {
        $last = Get-ListenerSnapshot -Port $Port
        $stateMatches = [bool]$last.listening -eq $Listening
        $pidMatches = $true
        if ($Listening -and $DifferentFromPid.HasValue -and $null -ne $last.pid) {
            $pidMatches = ([int]$last.pid -ne $DifferentFromPid.Value)
        }
        if ($stateMatches -and $pidMatches) {
            Add-Step $Label 'PASS' ([ordered]@{
                observationOnly = $true
                fuseSeconds = $FuseSeconds
                expectedListening = $Listening
                differentFromPid = if ($DifferentFromPid.HasValue) { $DifferentFromPid.Value } else { $null }
                observed = $last
            })
            Write-Evidence "PASS $Label :: port=$Port listening=$Listening pid=$($last.pid)"
            return $last
        }
        Start-Sleep -Seconds 1
    }

    Add-Step $Label 'FAIL' ([ordered]@{
        observationOnly = $true
        fuseSeconds = $FuseSeconds
        expectedListening = $Listening
        differentFromPid = if ($DifferentFromPid.HasValue) { $DifferentFromPid.Value } else { $null }
        lastObserved = $last
    })
    throw "$Label did not reach the expected listener state inside the bounded observation fuse."
}

function Get-CnxStatusDocument {
    param([string]$StepName = 'cnx-status')
    if (-not (Test-Path $Cnx)) { throw "cnx.cmd not found: $Cnx" }
    $result = Invoke-RootProcess $StepName $Cnx @('status') @(0)
    try { return $result.Stdout | ConvertFrom-Json } catch { throw "$StepName did not return valid JSON." }
}

function Get-ProviderStatusDocument {
    param([string]$StepName = 'provider-status')
    $result = Invoke-RootProcess $StepName $Cnx @('provider','status','--json') @(0)
    try { return $result.Stdout | ConvertFrom-Json } catch { throw "$StepName did not return valid JSON." }
}

function Get-RecoveryDocument {
    param([string]$StepName = 'check-recovery')
    $result = Invoke-RootProcess $StepName $Cnx @('check','recovery','--json') @(0,1)
    try { return $result.Stdout | ConvertFrom-Json } catch { throw "$StepName did not return valid JSON." }
}

function Assert-ManagedBaseline {
    param([string]$Label)
    $status = Get-CnxStatusDocument "status-$Label"
    $providerDoc = Get-ProviderStatusDocument "provider-status-$Label"
    $recovery = Get-RecoveryDocument "recovery-$Label"

    $mode = [string]$status.state.mode
    $selected = [string]$providerDoc.selectedProvider
    $adapterRows = @($recovery.checks | Where-Object { $_.name -eq 'Provider event adapter' })
    $adapterOkay = $adapterRows.Count -eq 1
    if ($Provider -eq 'lmstudio' -and $adapterOkay) {
        $adapterOkay = [bool]$adapterRows[0].details.expected -and [bool]$adapterRows[0].details.running
    }
    if ($Provider -eq 'ollama' -and $adapterOkay) {
        $adapterOkay = -not [bool]$adapterRows[0].details.expected
    }

    $gateway = Get-ListenerSnapshot -Port (Get-GatewayPort)
    $providerListener = Get-ListenerSnapshot -Port (Get-ProviderPort)
    $ok = ($mode -eq 'managed') -and ($selected -eq $Provider) -and $adapterOkay -and [bool]$gateway.listening -and [bool]$providerListener.listening

    Add-Step "assert-managed-$Label" $(if ($ok) { 'PASS' } else { 'FAIL' }) ([ordered]@{
        mode = $mode
        selectedProvider = $selected
        providerEventAdapter = if ($adapterRows.Count -eq 1) { $adapterRows[0] } else { $null }
        gateway = $gateway
        providerListener = $providerListener
    })
    if (-not $ok) { throw "Managed baseline assertion failed at '$Label'." }
    Write-Evidence "PASS assert-managed-$Label"
}

function Confirm-DisruptiveSuite {
    if ($DisruptiveScenarios.Count -eq 0) { return }
    Write-Host ''
    Write-Host 'DISRUPTIVE RECOVERY REALITY TESTS REQUESTED.'
    Write-Host "Scenarios: $($DisruptiveScenarios -join ', ')"
    Write-Host 'The harness will force-kill the OpenClaw Gateway and/or selected provider process.'
    Write-Host 'It will not reset or uninstall CogentNexus.'
    $answer = Read-Host 'Type y to continue'
    if ($answer -cne 'y') {
        throw 'Disruptive suite cancelled; exact lowercase y was not supplied.'
    }
    Add-Step 'explicit-disruptive-confirmation' 'PASS' ([ordered]@{ confirmation = 'y'; scenarios = $DisruptiveScenarios })
}

function Install-ReleasedCogentNexus {
    if (Test-Path $Cnx) {
        throw "-InstallRelease requires a clean consumer path with no existing cnx.cmd. Found: $Cnx"
    }

    $api = "https://api.github.com/repos/funggier/cogentnexus/releases/tags/$ReleaseTag"
    $headers = @{ 'User-Agent'='CogentNexus-Recovery-Reality'; 'Accept'='application/vnd.github+json' }
    Write-Evidence "Fetching release metadata: $ReleaseTag"
    $release = Invoke-RestMethod -Uri $api -Headers $headers -UseBasicParsing
    if ($release.tag_name -ne $ReleaseTag -or [bool]$release.draft -or [bool]$release.prerelease) {
        throw "Release $ReleaseTag is not a published stable release."
    }
    if ($ExpectedReleaseCommit -and [string]$release.target_commitish -ne $ExpectedReleaseCommit) {
        throw "Release target mismatch: expected $ExpectedReleaseCommit; got $($release.target_commitish)."
    }

    $name = "cogentnexus-$ReleaseTag"
    $zipName = "$name.zip"
    $requiredNames = @($zipName,'SHA256SUMS.txt')
    $assets = @($release.assets)
    foreach ($required in $requiredNames) {
        if (@($assets | Where-Object { $_.name -eq $required }).Count -ne 1) {
            throw "Release asset missing or duplicated: $required"
        }
    }

    $releaseRoot = Join-Path $RunRoot 'release'
    New-Item -ItemType Directory -Force -Path $releaseRoot | Out-Null
    foreach ($required in $requiredNames) {
        $asset = $assets | Where-Object { $_.name -eq $required } | Select-Object -First 1
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile (Join-Path $releaseRoot $required) -UseBasicParsing
    }

    $hashes = @{}
    Get-Content (Join-Path $releaseRoot 'SHA256SUMS.txt') | ForEach-Object {
        if ($_ -match '^([0-9a-fA-F]{64})\s+\*?(.+)$') {
            $hashes[$Matches[2].Trim()] = $Matches[1].ToLowerInvariant()
        }
    }
    if (-not $hashes.ContainsKey($zipName)) { throw "SHA256SUMS.txt has no entry for $zipName" }
    $actualHash = (Get-FileHash -Algorithm SHA256 -Path (Join-Path $releaseRoot $zipName)).Hash.ToLowerInvariant()
    if ($actualHash -ne $hashes[$zipName]) { throw "Release ZIP SHA256 mismatch." }

    $extractRoot = Join-Path $releaseRoot 'extracted'
    Expand-Archive -Path (Join-Path $releaseRoot $zipName) -DestinationPath $extractRoot -Force
    $sourceRoot = Join-Path $extractRoot $name
    if (-not (Test-Path (Join-Path $sourceRoot 'scripts\install.ps1'))) {
        throw "Release archive does not contain expected installer root: $sourceRoot"
    }
    $version = (Get-Content (Join-Path $sourceRoot 'VERSION') -Raw).Trim()
    if ("v$version" -ne $ReleaseTag) { throw "Release archive VERSION '$version' does not match tag $ReleaseTag." }

    Add-Step 'release-consumer-download' 'PASS' ([ordered]@{
        release = $ReleaseTag
        targetCommit = [string]$release.target_commitish
        zip = $zipName
        sha256 = $actualHash
        extractedRoot = $sourceRoot
    })

    Invoke-RootProcess 'release-consumer-install' 'powershell.exe' @(
        '-NoProfile','-ExecutionPolicy','Bypass','-File',(Join-Path $sourceRoot 'scripts\install.ps1'),'-Provider',$Provider
    ) @(0) 1200 | Out-Null

    if (-not (Test-Path $Cnx)) { throw 'Release consumer install did not create cnx.cmd.' }
    Assert-ManagedBaseline 'after-release-install'
}

function Invoke-GatewayCrashScenario {
    Write-Evidence 'SCENARIO gateway-crash :: begin'
    Assert-ManagedBaseline 'gateway-crash-before'
    $port = Get-GatewayPort
    $before = Get-ListenerSnapshot -Port $port
    if (-not $before.listening -or $null -eq $before.pid) { throw 'Gateway listener was not present before failure injection.' }

    Stop-Process -Id ([int]$before.pid) -Force -ErrorAction Stop
    Add-Step 'inject-gateway-hard-crash' 'PASS' ([ordered]@{
        method = 'Stop-Process -Force'
        port = $port
        killedPid = [int]$before.pid
        processName = $before.processName
    })
    Write-Evidence "Injected Gateway hard crash pid=$($before.pid)"

    $after = Wait-ListenerState 'observe-gateway-recovered' $port $true ([Nullable[int]]([int]$before.pid))
    Assert-ManagedBaseline 'gateway-crash-after'
    Add-Step 'scenario-gateway-crash' 'PASS' ([ordered]@{ before = $before; after = $after })
    Write-Evidence 'SCENARIO gateway-crash :: PASS'
}

function Invoke-ProviderCrashScenario {
    Write-Evidence "SCENARIO provider-crash :: begin provider=$Provider"
    Assert-ManagedBaseline 'provider-crash-before'
    $port = Get-ProviderPort
    $before = Get-ListenerSnapshot -Port $port
    if (-not $before.listening -or $null -eq $before.pid) { throw 'Selected provider listener was not present before failure injection.' }

    Stop-Process -Id ([int]$before.pid) -Force -ErrorAction Stop
    Add-Step 'inject-provider-hard-crash' 'PASS' ([ordered]@{
        method = 'Stop-Process -Force'
        provider = $Provider
        port = $port
        killedPid = [int]$before.pid
        processName = $before.processName
    })
    Write-Evidence "Injected $Provider hard crash pid=$($before.pid)"

    $after = Wait-ListenerState 'observe-provider-recovered' $port $true ([Nullable[int]]([int]$before.pid))
    $providerDoc = Get-ProviderStatusDocument 'provider-status-after-hard-crash'
    if ([string]$providerDoc.selectedProvider -ne $Provider) {
        throw "Provider recovery changed durable selectedProvider to '$($providerDoc.selectedProvider)'."
    }
    $recovery = Get-RecoveryDocument 'recovery-after-provider-hard-crash'
    $incidentRows = @($recovery.checks | Where-Object { $_.name -eq 'Provider recovery incident' })
    if ($incidentRows.Count -ne 1) { throw 'Provider recovery incident diagnostic row is missing after provider crash.' }
    if ([bool]$incidentRows[0].details.circuitOpen) { throw 'Provider recovery circuit is open after a single injected provider crash.' }
    Assert-ManagedBaseline 'provider-crash-after'
    Add-Step 'scenario-provider-crash' 'PASS' ([ordered]@{
        before = $before
        after = $after
        recoveryIncident = $incidentRows[0]
    })
    Write-Evidence 'SCENARIO provider-crash :: PASS'
}

function Invoke-OperatorStopScenario {
    Write-Evidence 'SCENARIO operator-stop :: begin'
    Assert-ManagedBaseline 'operator-stop-before'

    Invoke-RootProcess 'intentional-cnx-stop' $Cnx @('stop') @(0) 600 | Out-Null
    $status = Get-CnxStatusDocument 'status-after-intentional-stop'
    $state = $status.state
    $maintenanceOkay = ([string]$state.mode -eq 'maintenance') -and ([string]$state.desiredGateway -eq 'stopped') -and ([string]$state.desiredProvider -eq 'stopped')
    if (-not $maintenanceOkay) {
        throw 'Intentional stop did not persist maintenance/stopped desired state.'
    }

    $gatewayPort = Get-GatewayPort
    [void](Wait-ListenerState 'observe-gateway-stopped-intentionally' $gatewayPort $false $null 60)
    Start-Sleep -Seconds $IntentionalStopObservationSeconds
    $afterObservation = Get-ListenerSnapshot -Port $gatewayPort
    if ($afterObservation.listening) {
        throw 'Gateway auto-recovered during an intentional operator-stop observation window.'
    }
    Add-Step 'intentional-stop-no-auto-recovery' 'PASS' ([ordered]@{
        observationOnly = $true
        observationSeconds = $IntentionalStopObservationSeconds
        state = $state
        gatewayAfterObservation = $afterObservation
    })

    Invoke-RootProcess 'start-after-intentional-stop' $Cnx @('start') @(0) 900 | Out-Null
    [void](Wait-ListenerState 'observe-gateway-started-after-operator-start' $gatewayPort $true $null)
    [void](Wait-ListenerState 'observe-provider-started-after-operator-start' (Get-ProviderPort) $true $null)
    Assert-ManagedBaseline 'operator-stop-after-start'
    Add-Step 'scenario-operator-stop' 'PASS' ([ordered]@{ noAutoRecoveryObserved = $true })
    Write-Evidence 'SCENARIO operator-stop :: PASS'
}

function Invoke-BestEffortReconcile {
    if (-not (Test-Path $Cnx)) { return }
    try {
        Write-Evidence 'CLEANUP :: best-effort cnx start --provider selected provider'
        Invoke-RootProcess 'cleanup-reconcile-start' $Cnx @('start','--provider',$Provider) @(0) 900 | Out-Null
        Assert-ManagedBaseline 'cleanup'
        Add-Step 'cleanup-reconcile' 'PASS' ([ordered]@{ provider = $Provider })
    }
    catch {
        Add-Step 'cleanup-reconcile' 'FAIL' ([ordered]@{ provider = $Provider; error = $_.Exception.Message })
        Write-Evidence "CLEANUP FAILED :: $($_.Exception.Message)"
    }
}

Set-Content -Path $LogPath -Value "CogentNexus v0.9.3 Recovery Reality Windows Harness`r`n" -Encoding UTF8
Save-Evidence

try {
    Invoke-RootProcess 'openclaw-version' 'openclaw.cmd' @('--version') @(0) 60 | Out-Null
    Invoke-RootProcess 'openclaw-config-validate' 'openclaw.cmd' @('config','validate') @(0) 120 | Out-Null

    if ($InstallRelease) {
        Install-ReleasedCogentNexus
    } elseif (-not (Test-Path $Cnx)) {
        throw "cnx.cmd is not installed. Use -InstallRelease for a clean consumer-path installation of $ReleaseTag, or install CogentNexus first."
    }

    Confirm-DisruptiveSuite

    foreach ($name in $ExpandedScenarios) {
        switch ($name) {
            'baseline' {
                Assert-ManagedBaseline 'baseline'
                Add-Step 'scenario-baseline' 'PASS' ([ordered]@{ provider = $Provider })
            }
            'gateway-crash' { Invoke-GatewayCrashScenario }
            'provider-crash' { Invoke-ProviderCrashScenario }
            'operator-stop' { Invoke-OperatorStopScenario }
            default { throw "Unknown scenario: $name" }
        }
    }

    $Evidence.result = 'PASS'
    $Evidence.completedAt = (Get-Date).ToString('o')
    Save-Evidence
    Write-Evidence 'COGENTNEXUS v0.9.3 RECOVERY REALITY SUITE: PASS'
    Write-Host "Evidence: $LogPath"
    Write-Host "Evidence JSON: $JsonPath"
    exit 0
}
catch {
    $Evidence.result = 'FAIL'
    $Evidence.error = $_.Exception.Message
    $Evidence.failedAt = (Get-Date).ToString('o')
    Save-Evidence
    Write-Evidence "FAIL :: $($_.Exception.Message)"
    if ($RunDisruptive) { Invoke-BestEffortReconcile }
    Save-Evidence
    Write-Host "Evidence: $LogPath"
    Write-Host "Evidence JSON: $JsonPath"
    exit 1
}
