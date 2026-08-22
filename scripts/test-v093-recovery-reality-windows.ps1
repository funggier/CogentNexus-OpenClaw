[CmdletBinding()]
param(
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
    Write-Host 'CogentNexus v0.9.3 Ollama-only Recovery Reality harness syntax/load: PASS'
    exit 0
}
if ($env:OS -ne 'Windows_NT') { throw 'This harness is Windows-only.' }
if ($RecoveryFuseSeconds -lt 30 -or $RecoveryFuseSeconds -gt 1800) { throw 'RecoveryFuseSeconds must be between 30 and 1800.' }
if ($IntentionalStopObservationSeconds -lt 5 -or $IntentionalStopObservationSeconds -gt 120) { throw 'IntentionalStopObservationSeconds must be between 5 and 120.' }

$Downloads = Join-Path $HOME 'Downloads'
$Workspace = Join-Path $HOME '.openclaw\workspace'
$Cnx = Join-Path $Workspace 'cnx.cmd'
$OpenClawConfig = if ($env:OPENCLAW_CONFIG_PATH) {
    [IO.Path]::GetFullPath((Join-Path (Get-Location) $env:OPENCLAW_CONFIG_PATH))
} else {
    Join-Path $HOME '.openclaw\openclaw.json'
}
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$LogPath = Join-Path $Downloads "CNX_V093_OLLAMA_RECOVERY_$Stamp.txt"
$JsonPath = Join-Path $Downloads "CNX_V093_OLLAMA_RECOVERY_$Stamp.json"
$RunRoot = Join-Path $Downloads "CNX_V093_OLLAMA_RECOVERY_$Stamp"
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
    throw "Disruptive scenarios requested without -RunDisruptive: $($DisruptiveScenarios -join ', ')"
}

function Get-ProcessRecord {
    param([int]$Id)
    $row = Get-CimInstance Win32_Process -Filter "ProcessId=$Id" -ErrorAction SilentlyContinue
    if ($null -eq $row) { return $null }
    return [ordered]@{
        pid = [int]$row.ProcessId
        parentPid = [int]$row.ParentProcessId
        name = [string]$row.Name
        executablePath = [string]$row.ExecutablePath
        commandLine = [string]$row.CommandLine
    }
}

function Get-AncestorPids {
    param([int]$StartPid)
    $seen = New-Object System.Collections.Generic.HashSet[int]
    $result = New-Object System.Collections.Generic.List[int]
    $current = $StartPid
    for ($i = 0; $i -lt 32; $i++) {
        $row = Get-ProcessRecord -Id $current
        if ($null -eq $row) { break }
        $parent = [int]$row.parentPid
        if ($parent -le 0 -or $seen.Contains($parent)) { break }
        [void]$seen.Add($parent)
        [void]$result.Add($parent)
        $current = $parent
    }
    return @($result)
}

$Evidence = [ordered]@{
    schemaVersion = 2
    suite = 'v0.9.3-ollama-recovery-reality-windows'
    startedAt = (Get-Date).ToString('o')
    provider = 'ollama'
    scenarios = @($ExpandedScenarios)
    installRelease = [bool]$InstallRelease
    releaseTag = $ReleaseTag
    expectedReleaseCommit = $ExpectedReleaseCommit
    recoveryFuseSeconds = $RecoveryFuseSeconds
    intentionalStopObservationSeconds = $IntentionalStopObservationSeconds
    runRoot = $RunRoot
    openclawConfig = $OpenClawConfig
    harness = [ordered]@{
        pid = [int]$PID
        process = Get-ProcessRecord -Id ([int]$PID)
        ancestorPids = @(Get-AncestorPids -StartPid ([int]$PID))
    }
    activeOperation = $null
    steps = @()
    result = 'running'
    error = $null
}

function Save-Evidence { $Evidence | ConvertTo-Json -Depth 60 | Set-Content -Path $JsonPath -Encoding UTF8 }
function Write-Evidence {
    param([string]$Message)
    $line = "[$((Get-Date).ToString('o'))] $Message"
    Write-Host $line
    Add-Content -Path $LogPath -Value $line -Encoding UTF8
}
function Add-Step {
    param([string]$Name,[string]$Status,$Data)
    $Evidence.steps += [ordered]@{ name=$Name; status=$Status; at=(Get-Date).ToString('o'); data=$Data }
    Save-Evidence
}
function Set-ActiveOperation {
    param([string]$Name,$Data)
    $Evidence.activeOperation = [ordered]@{ name=$Name; at=(Get-Date).ToString('o'); data=$Data }
    Save-Evidence
}
function Clear-ActiveOperation { $Evidence.activeOperation = $null; Save-Evidence }

function Quote-CmdArg {
    param([string]$Value)
    if ($Value -notmatch '[\s&()\[\]{}^=;!''+,`~"]') { return $Value }
    return '"' + ($Value -replace '"','\"') + '"'
}

function Invoke-DirectProbe {
    param([string]$Name,[scriptblock]$Command,[int[]]$AllowedExitCodes=@(0))
    Write-Evidence "START $Name"
    Set-ActiveOperation $Name ([ordered]@{ mode='direct-probe'; harnessPid=[int]$PID })
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $text = & $Command 2>&1 | Out-String
    $rc = $LASTEXITCODE
    $sw.Stop()
    if ($text) { Add-Content -Path $LogPath -Value $text -Encoding UTF8 }
    $ok = $AllowedExitCodes -contains $rc
    Add-Step $Name $(if ($ok) { 'PASS' } else { 'FAIL' }) ([ordered]@{ exitCode=$rc; durationSeconds=[math]::Round($sw.Elapsed.TotalSeconds,3); output=$text })
    Clear-ActiveOperation
    if (-not $ok) { throw "$Name failed with exit code $rc." }
    Write-Evidence "PASS $Name"
    return [pscustomobject]@{ ExitCode=$rc; Output=$text }
}

function Invoke-CapturedProcess {
    param([string]$Name,[string]$FilePath,[string[]]$Arguments=@(),[int[]]$AllowedExitCodes=@(0),[int]$TimeoutSeconds=900)
    Write-Evidence "START $Name :: $FilePath $($Arguments -join ' ')"
    $stdout = Join-Path $env:TEMP "cnx-v093-$Stamp-$([guid]::NewGuid().ToString('N')).out.txt"
    $stderr = Join-Path $env:TEMP "cnx-v093-$Stamp-$([guid]::NewGuid().ToString('N')).err.txt"
    $launchFile = $FilePath
    $launchArgs = @($Arguments)
    $ext = [IO.Path]::GetExtension($FilePath)
    if ($ext -ieq '.cmd' -or $ext -ieq '.bat') {
        $cmdline = (Quote-CmdArg $FilePath)
        foreach ($arg in $Arguments) { $cmdline += ' ' + (Quote-CmdArg ([string]$arg)) }
        $launchFile = 'cmd.exe'
        $launchArgs = @('/d','/s','/c',$cmdline)
    }
    $sw = [Diagnostics.Stopwatch]::StartNew()
    try {
        $proc = Start-Process -FilePath $launchFile -ArgumentList $launchArgs -PassThru -NoNewWindow -RedirectStandardOutput $stdout -RedirectStandardError $stderr
        $null = $proc.Handle
        Set-ActiveOperation $Name ([ordered]@{
            mode='captured-process'; requestedFile=$FilePath; requestedArguments=@($Arguments)
            launchFile=$launchFile; launchArguments=@($launchArgs); childPid=[int]$proc.Id
            child=Get-ProcessRecord -Id ([int]$proc.Id); timeoutSeconds=$TimeoutSeconds
        })
        if (-not $proc.WaitForExit($TimeoutSeconds * 1000)) {
            Write-Evidence "TIMEOUT $Name :: stopping exact root pid=$($proc.Id); process trees are never killed"
            Stop-Process -Id ([int]$proc.Id) -Force -ErrorAction SilentlyContinue
            throw "$Name exceeded bounded timeout ${TimeoutSeconds}s."
        }
        $proc.WaitForExit(); $proc.Refresh(); $rc = [int]$proc.ExitCode; $sw.Stop()
        $outText = if (Test-Path $stdout) { Get-Content $stdout -Raw } else { '' }
        $errText = if (Test-Path $stderr) { Get-Content $stderr -Raw } else { '' }
        if ($outText) { Add-Content -Path $LogPath -Value $outText -Encoding UTF8 }
        if ($errText) { Add-Content -Path $LogPath -Value $errText -Encoding UTF8 }
        $ok = $AllowedExitCodes -contains $rc
        Add-Step $Name $(if ($ok) { 'PASS' } else { 'FAIL' }) ([ordered]@{ exitCode=$rc; durationSeconds=[math]::Round($sw.Elapsed.TotalSeconds,3); stdout=$outText; stderr=$errText; launchFile=$launchFile; launchArguments=@($launchArgs) })
        Clear-ActiveOperation
        if (-not $ok) { throw "$Name failed with exit code $rc." }
        Write-Evidence "PASS $Name"
        return [pscustomobject]@{ ExitCode=$rc; Stdout=$outText; Stderr=$errText }
    }
    finally { Remove-Item $stdout,$stderr -Force -ErrorAction SilentlyContinue }
}

function Read-OpenClawConfig {
    if (-not (Test-Path $OpenClawConfig)) { throw "OpenClaw config not found: $OpenClawConfig" }
    return Get-Content $OpenClawConfig -Raw | ConvertFrom-Json
}
function Get-GatewayPort {
    $cfg = Read-OpenClawConfig
    if ($null -ne $cfg.gateway -and $null -ne $cfg.gateway.port) { return [int]$cfg.gateway.port }
    return 18789
}
function Get-ListenerSnapshot {
    param([int]$Port)
    $rows = @(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue)
    if ($rows.Count -eq 0) { return [ordered]@{ port=$Port; listening=$false; pid=$null; process=$null } }
    $pidValue = [int]$rows[0].OwningProcess
    return [ordered]@{ port=$Port; listening=$true; pid=$pidValue; process=Get-ProcessRecord -Id $pidValue }
}
function Wait-ListenerState {
    param([string]$Label,[int]$Port,[bool]$Listening,[Nullable[int]]$DifferentFromPid=$null,[int]$FuseSeconds=$RecoveryFuseSeconds)
    $deadline = (Get-Date).AddSeconds($FuseSeconds)
    $last = $null
    while ((Get-Date) -lt $deadline) {
        $last = Get-ListenerSnapshot -Port $Port
        $stateOkay = ([bool]$last.listening -eq $Listening)
        $pidOkay = $true
        if ($Listening -and $DifferentFromPid.HasValue -and $null -ne $last.pid) { $pidOkay = ([int]$last.pid -ne $DifferentFromPid.Value) }
        if ($stateOkay -and $pidOkay) {
            Add-Step $Label 'PASS' ([ordered]@{ observationOnly=$true; fuseSeconds=$FuseSeconds; observed=$last; differentFromPid=$(if ($DifferentFromPid.HasValue) { $DifferentFromPid.Value } else { $null }) })
            return $last
        }
        Start-Sleep -Seconds 1
    }
    Add-Step $Label 'FAIL' ([ordered]@{ observationOnly=$true; fuseSeconds=$FuseSeconds; lastObserved=$last })
    throw "$Label did not reach expected listener state inside observation fuse."
}

function Assert-SafeKillTarget {
    param([ValidateSet('gateway','provider')][string]$Role,$Snapshot)
    if (-not [bool]$Snapshot.listening -or $null -eq $Snapshot.pid -or $null -eq $Snapshot.process) { throw "$Role target is not a live listener process." }
    $target = $Snapshot.process
    $targetPid = [int]$target.pid
    $name = ([string]$target.name).ToLowerInvariant()
    $cmd = ([string]$target.commandLine).ToLowerInvariant()
    $banned = @('powershell.exe','pwsh.exe','cmd.exe','conhost.exe','firefox.exe','explorer.exe','windowsterminal.exe','openconsole.exe')
    if ($banned -contains $name) { throw "Refusing to kill unsafe process '$name' for role $Role." }
    if ($targetPid -eq [int]$PID) { throw "Refusing to kill harness PID $targetPid." }
    $ancestors = @(Get-AncestorPids -StartPid ([int]$PID))
    if ($ancestors -contains $targetPid) { throw "Refusing to kill harness ancestor PID $targetPid." }
    $identityOkay = if ($Role -eq 'gateway') {
        ($name -eq 'node.exe' -and $cmd -match 'openclaw')
    } else {
        ($name -match 'ollama' -or $cmd -match 'ollama')
    }
    if (-not $identityOkay) { throw "Refusing unverified $Role target pid=$targetPid name='$name' commandLine='$($target.commandLine)'." }
    Add-Step "safe-kill-target-$Role" 'PASS' ([ordered]@{ target=$target; harnessPid=[int]$PID; harnessAncestors=$ancestors })
    return $target
}
function Invoke-ExactHardKill {
    param([ValidateSet('gateway','provider')][string]$Role,$Snapshot)
    $target = Assert-SafeKillTarget -Role $Role -Snapshot $Snapshot
    Set-ActiveOperation "inject-$Role-hard-crash" ([ordered]@{ target=$target; method='Stop-Process exact PID only' })
    Stop-Process -Id ([int]$target.pid) -Force -ErrorAction Stop
    Add-Step "inject-$Role-hard-crash" 'PASS' ([ordered]@{ target=$target; method='Stop-Process exact PID only' })
    Clear-ActiveOperation
}

function Get-JsonCommand {
    param([string]$Name,[string[]]$Args,[int[]]$Allowed=@(0))
    $result = Invoke-CapturedProcess $Name $Cnx $Args $Allowed 900
    try { return $result.Stdout | ConvertFrom-Json } catch { throw "$Name did not return valid JSON." }
}
function Assert-ManagedBaseline {
    param([string]$Label)
    $status = Get-JsonCommand "status-$Label" @('status') @(0)
    $providerDoc = Get-JsonCommand "provider-status-$Label" @('provider','status','--json') @(0)
    $recovery = Get-JsonCommand "recovery-$Label" @('check','recovery','--json') @(0,1)
    $adapterRows = @($recovery.checks | Where-Object { $_.name -eq 'Provider event adapter' })
    $adapterOkay = ($adapterRows.Count -eq 1 -and -not [bool]$adapterRows[0].details.expected)
    $gateway = Get-ListenerSnapshot -Port (Get-GatewayPort)
    $ollama = Get-ListenerSnapshot -Port 11434
    $ok = ([string]$status.state.mode -eq 'managed') -and ([string]$providerDoc.selectedProvider -eq 'ollama') -and $adapterOkay -and [bool]$gateway.listening -and [bool]$ollama.listening
    Add-Step "assert-managed-$Label" $(if ($ok) { 'PASS' } else { 'FAIL' }) ([ordered]@{ mode=[string]$status.state.mode; selectedProvider=[string]$providerDoc.selectedProvider; providerEventAdapter=$(if ($adapterRows.Count -eq 1) { $adapterRows[0] } else { $null }); gateway=$gateway; ollama=$ollama })
    if (-not $ok) { throw "Managed Ollama baseline failed at $Label." }
}

function Install-ReleasedCogentNexus {
    if (Test-Path $Cnx) { throw "-InstallRelease requires a clean consumer path with no existing cnx.cmd: $Cnx" }
    $api = "https://api.github.com/repos/funggier/cogentnexus/releases/tags/$ReleaseTag"
    $headers = @{ 'User-Agent'='CogentNexus-Ollama-Recovery-Reality'; 'Accept'='application/vnd.github+json' }
    Set-ActiveOperation 'release-metadata' ([ordered]@{ uri=$api })
    $release = Invoke-RestMethod -Uri $api -Headers $headers -UseBasicParsing
    Clear-ActiveOperation
    if ($release.tag_name -ne $ReleaseTag -or [bool]$release.draft -or [bool]$release.prerelease) { throw "Release $ReleaseTag is not a published stable release." }
    if ([string]$release.target_commitish -ne $ExpectedReleaseCommit) { throw "Release target mismatch." }
    $name = "cogentnexus-$ReleaseTag"; $zipName = "$name.zip"; $assets = @($release.assets)
    $zipAsset = @($assets | Where-Object { $_.name -eq $zipName }); $sumAsset = @($assets | Where-Object { $_.name -eq 'SHA256SUMS.txt' })
    if ($zipAsset.Count -ne 1 -or $sumAsset.Count -ne 1) { throw 'Required release assets missing or duplicated.' }
    $releaseRoot = Join-Path $RunRoot 'release'; New-Item -ItemType Directory -Force -Path $releaseRoot | Out-Null
    $zipPath = Join-Path $releaseRoot $zipName; $sumPath = Join-Path $releaseRoot 'SHA256SUMS.txt'
    Invoke-WebRequest -Uri $zipAsset[0].browser_download_url -OutFile $zipPath -UseBasicParsing
    Invoke-WebRequest -Uri $sumAsset[0].browser_download_url -OutFile $sumPath -UseBasicParsing
    $expectedHash = $null
    foreach ($line in Get-Content $sumPath) { if ($line -match '^([0-9a-fA-F]{64})\s+\*?(.+)$' -and $Matches[2].Trim() -eq $zipName) { $expectedHash=$Matches[1].ToLowerInvariant() } }
    if (-not $expectedHash) { throw 'ZIP hash missing from SHA256SUMS.txt.' }
    $actualHash = (Get-FileHash -Algorithm SHA256 -Path $zipPath).Hash.ToLowerInvariant()
    if ($actualHash -ne $expectedHash) { throw 'Release ZIP SHA256 mismatch.' }
    $extractRoot = Join-Path $releaseRoot 'extracted'; Expand-Archive -Path $zipPath -DestinationPath $extractRoot -Force
    $sourceRoot = Join-Path $extractRoot $name; $installer = Join-Path $sourceRoot 'scripts\install.ps1'
    if (-not (Test-Path $installer)) { throw 'Released installer missing after extraction.' }
    Add-Step 'release-consumer-download' 'PASS' ([ordered]@{ tag=$ReleaseTag; targetCommit=[string]$release.target_commitish; sha256=$actualHash; sourceRoot=$sourceRoot })
    Invoke-CapturedProcess 'release-consumer-install' 'powershell.exe' @('-NoProfile','-ExecutionPolicy','Bypass','-File',$installer,'-Provider','ollama') @(0) 1200 | Out-Null
    if (-not (Test-Path $Cnx)) { throw 'Release install did not create cnx.cmd.' }
    Assert-ManagedBaseline 'after-release-install'
}

function Confirm-DisruptiveSuite {
    if ($DisruptiveScenarios.Count -eq 0) { return }
    Write-Host ''; Write-Host 'DISRUPTIVE OLLAMA RECOVERY REALITY TESTS REQUESTED.'
    Write-Host "Scenarios: $($DisruptiveScenarios -join ', ')"
    Write-Host 'Only exact validated Gateway/Ollama listener PIDs may be force-killed; process trees are never killed.'
    $answer = Read-Host 'Type y to continue'
    if ($answer -cne 'y') { throw 'Disruptive suite cancelled.' }
    Add-Step 'explicit-disruptive-confirmation' 'PASS' ([ordered]@{ confirmation='y'; scenarios=$DisruptiveScenarios })
}
function Invoke-GatewayCrashScenario {
    Assert-ManagedBaseline 'gateway-crash-before'; $port = Get-GatewayPort; $before = Get-ListenerSnapshot -Port $port
    Invoke-ExactHardKill -Role 'gateway' -Snapshot $before
    $after = Wait-ListenerState 'observe-gateway-recovered' $port $true ([Nullable[int]]([int]$before.pid))
    Assert-ManagedBaseline 'gateway-crash-after'; Add-Step 'scenario-gateway-crash' 'PASS' ([ordered]@{ before=$before; after=$after }); Write-Evidence 'SCENARIO gateway-crash :: PASS'
}
function Invoke-ProviderCrashScenario {
    Assert-ManagedBaseline 'provider-crash-before'; $before = Get-ListenerSnapshot -Port 11434
    Invoke-ExactHardKill -Role 'provider' -Snapshot $before
    $after = Wait-ListenerState 'observe-ollama-recovered' 11434 $true ([Nullable[int]]([int]$before.pid))
    $recovery = Get-JsonCommand 'recovery-after-ollama-hard-crash' @('check','recovery','--json') @(0,1)
    $incidentRows = @($recovery.checks | Where-Object { $_.name -eq 'Provider recovery incident' })
    if ($incidentRows.Count -ne 1) { throw 'Provider recovery incident diagnostic row missing.' }
    if ([bool]$incidentRows[0].details.circuitOpen) { throw 'Ollama recovery circuit open after one injected crash.' }
    Assert-ManagedBaseline 'provider-crash-after'; Add-Step 'scenario-provider-crash' 'PASS' ([ordered]@{ before=$before; after=$after; recoveryIncident=$incidentRows[0] }); Write-Evidence 'SCENARIO provider-crash :: PASS'
}
function Invoke-OperatorStopScenario {
    Assert-ManagedBaseline 'operator-stop-before'; Invoke-CapturedProcess 'intentional-cnx-stop' $Cnx @('stop') @(0) 600 | Out-Null
    $status = Get-JsonCommand 'status-after-intentional-stop' @('status') @(0)
    if ([string]$status.state.mode -ne 'maintenance' -or [string]$status.state.desiredGateway -ne 'stopped' -or [string]$status.state.desiredProvider -ne 'stopped') { throw 'Intentional stop state mismatch.' }
    $gatewayPort = Get-GatewayPort; [void](Wait-ListenerState 'observe-gateway-stopped-intentionally' $gatewayPort $false $null 60)
    Start-Sleep -Seconds $IntentionalStopObservationSeconds
    $afterObservation = Get-ListenerSnapshot -Port $gatewayPort
    if ([bool]$afterObservation.listening) { throw 'Gateway auto-recovered during intentional stop observation.' }
    Add-Step 'intentional-stop-no-auto-recovery' 'PASS' ([ordered]@{ observationSeconds=$IntentionalStopObservationSeconds; gateway=$afterObservation })
    Invoke-CapturedProcess 'start-after-intentional-stop' $Cnx @('start') @(0) 900 | Out-Null
    [void](Wait-ListenerState 'observe-gateway-started-after-operator-start' $gatewayPort $true $null); [void](Wait-ListenerState 'observe-ollama-started-after-operator-start' 11434 $true $null)
    Assert-ManagedBaseline 'operator-stop-after-start'; Add-Step 'scenario-operator-stop' 'PASS' ([ordered]@{ noAutoRecoveryObserved=$true }); Write-Evidence 'SCENARIO operator-stop :: PASS'
}
function Invoke-BestEffortReconcile {
    if (-not (Test-Path $Cnx)) { return }
    try { Invoke-CapturedProcess 'cleanup-reconcile-start' $Cnx @('start') @(0) 900 | Out-Null; Assert-ManagedBaseline 'cleanup'; Add-Step 'cleanup-reconcile' 'PASS' ([ordered]@{ provider='ollama' }) }
    catch { Add-Step 'cleanup-reconcile' 'FAIL' ([ordered]@{ error=$_.Exception.Message }) }
}

Set-Content -Path $LogPath -Value "CogentNexus v0.9.3 Ollama-only Recovery Reality Windows Harness`r`n" -Encoding UTF8
Save-Evidence
try {
    Invoke-DirectProbe 'openclaw-version' { & openclaw.cmd --version } @(0) | Out-Null
    Invoke-DirectProbe 'openclaw-config-validate' { & openclaw.cmd config validate } @(0) | Out-Null
    Invoke-DirectProbe 'ollama-version' { & ollama.exe --version } @(0) | Out-Null
    if ($InstallRelease) { Install-ReleasedCogentNexus } elseif (-not (Test-Path $Cnx)) { throw 'cnx.cmd is not installed; use -InstallRelease on a clean consumer path.' }
    Confirm-DisruptiveSuite
    foreach ($name in $ExpandedScenarios) {
        switch ($name) {
            'baseline' { Assert-ManagedBaseline 'baseline'; Add-Step 'scenario-baseline' 'PASS' ([ordered]@{ provider='ollama' }) }
            'gateway-crash' { Invoke-GatewayCrashScenario }
            'provider-crash' { Invoke-ProviderCrashScenario }
            'operator-stop' { Invoke-OperatorStopScenario }
        }
    }
    $Evidence.result='PASS'; $Evidence.completedAt=(Get-Date).ToString('o'); Clear-ActiveOperation; Save-Evidence
    Write-Evidence 'COGENTNEXUS v0.9.3 OLLAMA RECOVERY REALITY SUITE: PASS'
    Write-Host "Evidence: $LogPath"; Write-Host "Evidence JSON: $JsonPath"; exit 0
}
catch {
    $Evidence.result='FAIL'; $Evidence.error=$_.Exception.Message; $Evidence.failedAt=(Get-Date).ToString('o'); Save-Evidence
    Write-Evidence "FAIL :: $($_.Exception.Message)"
    if ($RunDisruptive) { Invoke-BestEffortReconcile }
    Save-Evidence; Write-Host "Evidence: $LogPath"; Write-Host "Evidence JSON: $JsonPath"; exit 1
}
