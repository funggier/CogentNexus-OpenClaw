[CmdletBinding()]
param(
    [ValidateSet('baseline','gateway-crash','provider-crash','operator-stop','all')]
    [string[]]$Scenario = @('all'),
    [switch]$RunDisruptive,
    [int]$RecoveryFuseSeconds = 420,
    [int]$IntentionalStopObservationSeconds = 10,
    [switch]$SyntaxOnly
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($SyntaxOnly) {
    Write-Host 'CogentNexus v0.9.3 Ollama Recovery Reality harness v3 syntax/load: PASS'
    exit 0
}
if ($env:OS -ne 'Windows_NT') { throw 'This harness is Windows-only.' }
if ($RecoveryFuseSeconds -lt 30 -or $RecoveryFuseSeconds -gt 1800) { throw 'RecoveryFuseSeconds must be between 30 and 1800.' }
if ($IntentionalStopObservationSeconds -lt 5 -or $IntentionalStopObservationSeconds -gt 120) { throw 'IntentionalStopObservationSeconds must be between 5 and 120.' }

$Downloads = Join-Path $HOME 'Downloads'
$Workspace = Join-Path $HOME '.openclaw\workspace'
$Cnx = Join-Path $Workspace 'cnx.cmd'
$OpenClawConfig = if ($env:OPENCLAW_CONFIG_PATH) { [IO.Path]::GetFullPath((Join-Path (Get-Location) $env:OPENCLAW_CONFIG_PATH)) } else { Join-Path $HOME '.openclaw\openclaw.json' }
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$LogPath = Join-Path $Downloads "CNX_V093_OLLAMA_RECOVERY_V3_$Stamp.txt"
$JsonPath = Join-Path $Downloads "CNX_V093_OLLAMA_RECOVERY_V3_$Stamp.json"

$Expanded = New-Object System.Collections.Generic.List[string]
foreach ($item in $Scenario) {
    if ($item -eq 'all') {
        foreach ($name in @('baseline','gateway-crash','provider-crash','operator-stop')) { if (-not $Expanded.Contains($name)) { [void]$Expanded.Add($name) } }
    } elseif (-not $Expanded.Contains($item)) { [void]$Expanded.Add($item) }
}
$Disruptive = @($Expanded | Where-Object { $_ -ne 'baseline' })
if ($Disruptive.Count -gt 0 -and -not $RunDisruptive) { throw "Disruptive scenarios requested without -RunDisruptive: $($Disruptive -join ', ')" }

function Get-ProcessRecord {
    param([int]$ProcessId)
    $row = Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" -ErrorAction SilentlyContinue
    if ($null -eq $row) { return $null }
    [ordered]@{ pid=[int]$row.ProcessId; parentPid=[int]$row.ParentProcessId; name=[string]$row.Name; executablePath=[string]$row.ExecutablePath; commandLine=[string]$row.CommandLine }
}
function Get-AncestorPids {
    param([int]$StartPid)
    $seen = New-Object System.Collections.Generic.HashSet[int]
    $out = New-Object System.Collections.Generic.List[int]
    $current = $StartPid
    for ($i=0; $i -lt 32; $i++) {
        $row = Get-ProcessRecord -ProcessId $current
        if ($null -eq $row) { break }
        $parent = [int]$row.parentPid
        if ($parent -le 0 -or $seen.Contains($parent)) { break }
        [void]$seen.Add($parent); [void]$out.Add($parent); $current=$parent
    }
    @($out)
}

$Evidence = [ordered]@{
    schemaVersion=4; suite='v0.9.3-ollama-recovery-reality-windows-v3'; startedAt=(Get-Date).ToString('o'); provider='ollama'; scenarios=@($Expanded)
    recoveryFuseSeconds=$RecoveryFuseSeconds; intentionalStopObservationSeconds=$IntentionalStopObservationSeconds; openclawConfig=$OpenClawConfig
    harness=[ordered]@{ pid=[int]$PID; process=Get-ProcessRecord -ProcessId ([int]$PID); ancestorPids=@(Get-AncestorPids -StartPid ([int]$PID)) }
    activeOperation=$null; steps=@(); result='running'; error=$null
}
function Save-Evidence { $Evidence | ConvertTo-Json -Depth 60 | Set-Content -Path $JsonPath -Encoding UTF8 }
function Log { param([string]$Text) $line="[$((Get-Date).ToString('o'))] $Text"; Write-Host $line; Add-Content -Path $LogPath -Value $line -Encoding UTF8 }
function Step { param([string]$Name,[string]$Status,$Data) $Evidence.steps += [ordered]@{name=$Name;status=$Status;at=(Get-Date).ToString('o');data=$Data}; Save-Evidence }
function Active { param([string]$Name,$Data) $Evidence.activeOperation=[ordered]@{name=$Name;at=(Get-Date).ToString('o');data=$Data}; Save-Evidence }
function Clear-Active { $Evidence.activeOperation=$null; Save-Evidence }

function Invoke-CnxText {
    param([string]$Name,[string[]]$CommandArgs,[int[]]$AllowedExitCodes=@(0))
    if (-not (Test-Path $Cnx)) { throw "cnx.cmd not found: $Cnx" }
    $argsCopy=@($CommandArgs)
    Log "START $Name :: cnx.cmd $($argsCopy -join ' ')"
    Active $Name ([ordered]@{requestedFile=$Cnx;requestedArguments=$argsCopy;mode='direct-command'})
    $sw=[Diagnostics.Stopwatch]::StartNew()
    $text = & $Cnx @argsCopy 2>&1 | Out-String
    $rc=$LASTEXITCODE; $sw.Stop()
    if ($text) { Add-Content -Path $LogPath -Value $text -Encoding UTF8 }
    $ok=$AllowedExitCodes -contains $rc
    Step $Name $(if($ok){'PASS'}else{'FAIL'}) ([ordered]@{exitCode=$rc;durationSeconds=[math]::Round($sw.Elapsed.TotalSeconds,3);requestedArguments=$argsCopy;output=$text})
    Clear-Active
    if (-not $ok) { throw "$Name failed with exit code $rc." }
    [pscustomobject]@{ExitCode=$rc;Output=$text}
}
function Invoke-CnxJson {
    param([string]$Name,[string[]]$CommandArgs,[int[]]$AllowedExitCodes=@(0))
    $r=Invoke-CnxText -Name $Name -CommandArgs $CommandArgs -AllowedExitCodes $AllowedExitCodes
    try { $r.Output | ConvertFrom-Json } catch { throw "$Name did not return valid JSON." }
}
function Invoke-Probe {
    param([string]$Name,[scriptblock]$Command,[int[]]$AllowedExitCodes=@(0))
    Log "START $Name"; Active $Name ([ordered]@{mode='direct-probe';harnessPid=[int]$PID})
    $sw=[Diagnostics.Stopwatch]::StartNew(); $text=& $Command 2>&1 | Out-String; $rc=$LASTEXITCODE; $sw.Stop()
    if($text){Add-Content -Path $LogPath -Value $text -Encoding UTF8}; $ok=$AllowedExitCodes -contains $rc
    Step $Name $(if($ok){'PASS'}else{'FAIL'}) ([ordered]@{exitCode=$rc;durationSeconds=[math]::Round($sw.Elapsed.TotalSeconds,3);output=$text}); Clear-Active
    if(-not $ok){throw "$Name failed with exit code $rc."}; Log "PASS $Name"
}

function Read-Config { Get-Content $OpenClawConfig -Raw | ConvertFrom-Json }
function Get-GatewayPort { $cfg=Read-Config; if($null -ne $cfg.gateway -and $null -ne $cfg.gateway.port){[int]$cfg.gateway.port}else{18789} }
function Get-Listener {
    param([int]$Port)
    $rows=@(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue)
    if($rows.Count -eq 0){return [ordered]@{port=$Port;listening=$false;pid=$null;process=$null}}
    $p=[int]$rows[0].OwningProcess; [ordered]@{port=$Port;listening=$true;pid=$p;process=Get-ProcessRecord -ProcessId $p}
}
function Wait-Listener {
    param([string]$Name,[int]$Port,[bool]$Listening,[Nullable[int]]$DifferentFromPid=$null,[int]$FuseSeconds=$RecoveryFuseSeconds)
    $deadline=(Get-Date).AddSeconds($FuseSeconds); $last=$null
    while((Get-Date)-lt $deadline){
        $last=Get-Listener -Port $Port; $state=([bool]$last.listening -eq $Listening); $pidOkay=$true
        if($Listening -and $DifferentFromPid.HasValue -and $null -ne $last.pid){$pidOkay=([int]$last.pid -ne $DifferentFromPid.Value)}
        if($state -and $pidOkay){Step $Name 'PASS' ([ordered]@{observationOnly=$true;fuseSeconds=$FuseSeconds;observed=$last;differentFromPid=$(if($DifferentFromPid.HasValue){$DifferentFromPid.Value}else{$null})});return $last}
        Start-Sleep -Seconds 1
    }
    Step $Name 'FAIL' ([ordered]@{observationOnly=$true;fuseSeconds=$FuseSeconds;lastObserved=$last}); throw "$Name did not reach expected listener state inside observation fuse."
}
function Assert-SafeKill {
    param([ValidateSet('gateway','provider')][string]$Role,$Snapshot)
    if(-not [bool]$Snapshot.listening -or $null -eq $Snapshot.pid -or $null -eq $Snapshot.process){throw "$Role target is not a live listener process."}
    $target=$Snapshot.process; $targetPid=[int]$target.pid; $name=([string]$target.name).ToLowerInvariant(); $cmd=([string]$target.commandLine).ToLowerInvariant()
    $banned=@('powershell.exe','pwsh.exe','cmd.exe','conhost.exe','firefox.exe','explorer.exe','windowsterminal.exe','openconsole.exe')
    if($banned -contains $name){throw "Refusing unsafe kill target '$name'."}
    if($targetPid -eq [int]$PID){throw 'Refusing to kill harness.'}
    $anc=@(Get-AncestorPids -StartPid ([int]$PID)); if($anc -contains $targetPid){throw "Refusing to kill harness ancestor PID $targetPid."}
    $identity=if($Role -eq 'gateway'){($name -eq 'node.exe' -and $cmd -match 'openclaw')}else{($name -match 'ollama' -or $cmd -match 'ollama')}
    if(-not $identity){throw "Refusing unverified $Role target pid=$targetPid name='$name' commandLine='$($target.commandLine)'."}
    Step "safe-kill-target-$Role" 'PASS' ([ordered]@{target=$target;harnessPid=[int]$PID;harnessAncestors=$anc}); $target
}
function Hard-Kill {
    param([ValidateSet('gateway','provider')][string]$Role,$Snapshot)
    $target=Assert-SafeKill -Role $Role -Snapshot $Snapshot
    Active "inject-$Role-hard-crash" ([ordered]@{target=$target;method='Stop-Process exact PID only'})
    Stop-Process -Id ([int]$target.pid) -Force -ErrorAction Stop
    Step "inject-$Role-hard-crash" 'PASS' ([ordered]@{target=$target;method='Stop-Process exact PID only'}); Clear-Active
}

function Get-HostState {
    param($StatusDocument)
    if ($null -eq $StatusDocument.host -or $null -eq $StatusDocument.host.state) { throw 'cnx status JSON is missing host.state.' }
    return $StatusDocument.host.state
}
function Assert-Baseline {
    param([string]$Label)
    $status=Invoke-CnxJson -Name "status-$Label" -CommandArgs @('status')
    $hostState=Get-HostState -StatusDocument $status
    $provider=Invoke-CnxJson -Name "provider-$Label" -CommandArgs @('provider','status','--json')
    $recovery=Invoke-CnxJson -Name "recovery-$Label" -CommandArgs @('check','recovery','--json') -AllowedExitCodes @(0,1)
    $adapter=@($recovery.checks|Where-Object{$_.name -eq 'Provider event adapter'}); $adapterOkay=($adapter.Count -eq 1 -and -not [bool]$adapter[0].details.expected)
    $gateway=Get-Listener -Port (Get-GatewayPort); $ollama=Get-Listener -Port 11434
    $ok=([string]$hostState.mode -eq 'managed') -and ([string]$hostState.selectedProvider -eq 'ollama') -and ([string]$provider.selectedProvider -eq 'ollama') -and ([string]$recovery.verdict -eq 'READY') -and $adapterOkay -and [bool]$gateway.listening -and [bool]$ollama.listening
    Step "assert-managed-$Label" $(if($ok){'PASS'}else{'FAIL'}) ([ordered]@{mode=[string]$hostState.mode;hostSelectedProvider=[string]$hostState.selectedProvider;selectedProvider=[string]$provider.selectedProvider;recoveryVerdict=[string]$recovery.verdict;providerEventAdapter=$(if($adapter.Count -eq 1){$adapter[0]}else{$null});gateway=$gateway;ollama=$ollama})
    if(-not $ok){throw "Managed Ollama baseline failed at $Label."}
}
function Wait-DurableConvergence {
    param([string]$Name,[bool]$RequireProviderIncident=$false)
    $started=Get-Date; $deadline=$started.AddSeconds($RecoveryFuseSeconds); $observations=@(); $first=$null; $last=$null
    while((Get-Date)-lt $deadline){
        $status=Invoke-CnxJson -Name "$Name-status" -CommandArgs @('status')
        $provider=Invoke-CnxJson -Name "$Name-provider" -CommandArgs @('provider','status','--json')
        $recovery=Invoke-CnxJson -Name "$Name-recovery" -CommandArgs @('check','recovery','--json') -AllowedExitCodes @(0,1)
        $adapter=@($recovery.checks|Where-Object{$_.name -eq 'Provider event adapter'})
        $incident=@($recovery.checks|Where-Object{$_.name -eq 'Provider recovery incident'})
        $gateway=Get-Listener -Port (Get-GatewayPort); $ollama=Get-Listener -Port 11434
        $hostState=Get-HostState -StatusDocument $status
        $observation=[ordered]@{
            at=(Get-Date).ToString('o'); mode=[string]$hostState.mode; hostSelectedProvider=[string]$hostState.selectedProvider
            selectedProvider=[string]$provider.selectedProvider; recoveryVerdict=[string]$recovery.verdict
            gateway=$gateway; ollama=$ollama; providerEventAdapter=$(if($adapter.Count -eq 1){$adapter[0]}else{$null})
            providerRecoveryIncident=$(if($incident.Count -eq 1){$incident[0]}else{$null})
        }
        if($null -eq $first){$first=$observation}; $last=$observation; $observations += $observation
        $incidentOkay=(-not $RequireProviderIncident) -or ($incident.Count -eq 1 -and -not [bool]$incident[0].details.circuitOpen)
        $ok=($observation.mode -eq 'managed' -and $observation.hostSelectedProvider -eq 'ollama' -and $observation.selectedProvider -eq 'ollama' -and $observation.recoveryVerdict -eq 'READY' -and $adapter.Count -eq 1 -and -not [bool]$adapter[0].details.expected -and [bool]$gateway.listening -and [bool]$ollama.listening -and $incidentOkay)
        if($ok){
            $data=[ordered]@{observationOnly=$true;firstVerdict=$first.recoveryVerdict;finalVerdict=$observation.recoveryVerdict;attempts=$observations.Count;elapsedSeconds=[math]::Round(((Get-Date)-$started).TotalSeconds,3);lastObservation=$observation;observations=$observations}
            Step $Name 'PASS' $data; return $data
        }
        Start-Sleep -Seconds 1
    }
    $data=[ordered]@{observationOnly=$true;firstVerdict=$(if($null -ne $first){$first.recoveryVerdict}else{$null});finalVerdict=$(if($null -ne $last){$last.recoveryVerdict}else{$null});attempts=$observations.Count;elapsedSeconds=[math]::Round(((Get-Date)-$started).TotalSeconds,3);lastObservation=$last;observations=$observations}
    Step $Name 'FAIL' $data; throw "$Name did not observe durable READY convergence inside RecoveryFuseSeconds."
}
function Confirm-Disruptive {
    if($Disruptive.Count -eq 0){return}
    Write-Host ''; Write-Host 'DISRUPTIVE OLLAMA RECOVERY REALITY TESTS REQUESTED.'; Write-Host "Scenarios: $($Disruptive -join ', ')"; Write-Host 'Only exact validated Gateway/Ollama listener PIDs may be force-killed; process trees are never killed.'
    $answer=Read-Host 'Type y to continue'; if($answer -cne 'y'){throw 'Disruptive suite cancelled.'}; Step 'explicit-disruptive-confirmation' 'PASS' ([ordered]@{confirmation='y';scenarios=$Disruptive})
}
function Scenario-Gateway {
    Assert-Baseline 'gateway-before'; $port=Get-GatewayPort; $before=Get-Listener -Port $port; Hard-Kill -Role gateway -Snapshot $before
    $after=Wait-Listener -Name 'observe-gateway-recovered' -Port $port -Listening $true -DifferentFromPid ([Nullable[int]]([int]$before.pid)); $convergence=Wait-DurableConvergence 'converge-gateway-after'; Step 'scenario-gateway-crash' 'PASS' ([ordered]@{before=$before;after=$after;convergence=$convergence}); Log 'SCENARIO gateway-crash :: PASS'
}
function Scenario-Provider {
    Assert-Baseline 'provider-before'; $before=Get-Listener -Port 11434; Hard-Kill -Role provider -Snapshot $before
    $after=Wait-Listener -Name 'observe-ollama-recovered' -Port 11434 -Listening $true -DifferentFromPid ([Nullable[int]]([int]$before.pid))
    $recovery=Invoke-CnxJson -Name 'recovery-after-ollama-hard-crash' -CommandArgs @('check','recovery','--json') -AllowedExitCodes @(0,1); $incident=@($recovery.checks|Where-Object{$_.name -eq 'Provider recovery incident'})
    if($incident.Count -ne 1){throw 'Provider recovery incident diagnostic row missing.'}; if([bool]$incident[0].details.circuitOpen){throw 'Ollama recovery circuit open after one injected crash.'}
    $convergence=Wait-DurableConvergence 'converge-provider-after' $true; Step 'scenario-provider-crash' 'PASS' ([ordered]@{before=$before;after=$after;recoveryIncident=$incident[0];convergence=$convergence}); Log 'SCENARIO provider-crash :: PASS'
}
function Scenario-OperatorStop {
    Assert-Baseline 'operator-before'; Invoke-CnxText -Name 'intentional-cnx-stop' -CommandArgs @('stop') | Out-Null
    $status=Invoke-CnxJson -Name 'status-after-intentional-stop' -CommandArgs @('status'); $hostState=Get-HostState -StatusDocument $status
    if([string]$hostState.mode -ne 'maintenance' -or [string]$hostState.desiredGateway -ne 'stopped' -or [string]$hostState.desiredProvider -ne 'stopped'){throw 'Intentional stop state mismatch.'}
    $port=Get-GatewayPort; [void](Wait-Listener -Name 'observe-gateway-stopped-intentionally' -Port $port -Listening $false -FuseSeconds 60); Start-Sleep -Seconds $IntentionalStopObservationSeconds
    $obs=Get-Listener -Port $port; if([bool]$obs.listening){throw 'Gateway auto-recovered during intentional stop observation.'}; Step 'intentional-stop-no-auto-recovery' 'PASS' ([ordered]@{observationSeconds=$IntentionalStopObservationSeconds;gateway=$obs})
    Invoke-CnxText -Name 'start-after-intentional-stop' -CommandArgs @('start') | Out-Null; [void](Wait-Listener -Name 'observe-gateway-started-after-operator-start' -Port $port -Listening $true); [void](Wait-Listener -Name 'observe-ollama-started-after-operator-start' -Port 11434 -Listening $true)
    $convergence=Wait-DurableConvergence 'converge-after-operator-start'; Step 'scenario-operator-stop' 'PASS' ([ordered]@{noAutoRecoveryObserved=$true;convergence=$convergence}); Log 'SCENARIO operator-stop :: PASS'
}
function Best-Effort-Reconcile {
    if(-not(Test-Path $Cnx)){return}
    try{Invoke-CnxText -Name 'cleanup-start' -CommandArgs @('start')|Out-Null;Assert-Baseline 'cleanup';Step 'cleanup-reconcile' 'PASS' ([ordered]@{provider='ollama'})}catch{Step 'cleanup-reconcile' 'FAIL' ([ordered]@{error=$_.Exception.Message})}
}

Set-Content -Path $LogPath -Value "CogentNexus v0.9.3 Ollama-only Recovery Reality Windows Harness v3`r`n" -Encoding UTF8; Save-Evidence
try {
    Invoke-Probe -Name 'openclaw-version' -Command { & openclaw.cmd --version }
    Invoke-Probe -Name 'openclaw-config-validate' -Command { & openclaw.cmd config validate }
    Invoke-Probe -Name 'ollama-version' -Command { & ollama.exe --version }
    if(-not(Test-Path $Cnx)){throw 'cnx.cmd is not installed.'}; Confirm-Disruptive
    foreach($name in $Expanded){switch($name){'baseline'{Assert-Baseline 'baseline';Step 'scenario-baseline' 'PASS' ([ordered]@{provider='ollama'});Log 'SCENARIO baseline :: PASS'}'gateway-crash'{Scenario-Gateway}'provider-crash'{Scenario-Provider}'operator-stop'{Scenario-OperatorStop}}}
    $Evidence.result='PASS';$Evidence.completedAt=(Get-Date).ToString('o');Clear-Active;Save-Evidence;Log 'COGENTNEXUS v0.9.3 OLLAMA RECOVERY REALITY SUITE V3: PASS';Write-Host "Evidence: $LogPath";Write-Host "Evidence JSON: $JsonPath";exit 0
} catch {
    $Evidence.result='FAIL';$Evidence.error=$_.Exception.Message;$Evidence.failedAt=(Get-Date).ToString('o');Save-Evidence;Log "FAIL :: $($_.Exception.Message)";if($RunDisruptive){Best-Effort-Reconcile};Save-Evidence;Write-Host "Evidence: $LogPath";Write-Host "Evidence JSON: $JsonPath";exit 1
}
