[CmdletBinding()]
param(
    [switch]$RunDisruptive,
    [int]$RecoveryFuseSeconds = 420,
    [switch]$SyntaxOnly
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($SyntaxOnly) {
    Write-Host 'CogentNexus v0.9.3 Gateway Convergence diagnostic syntax/load: PASS'
    exit 0
}
if ($env:OS -ne 'Windows_NT') { throw 'This diagnostic is Windows-only.' }
if (-not $RunDisruptive) { throw 'Gateway convergence diagnostic requires -RunDisruptive.' }
if ($RecoveryFuseSeconds -lt 30 -or $RecoveryFuseSeconds -gt 1800) { throw 'RecoveryFuseSeconds must be between 30 and 1800.' }

$Downloads = Join-Path $HOME 'Downloads'
$Workspace = Join-Path $HOME '.openclaw\workspace'
$Cnx = Join-Path $Workspace 'cnx.cmd'
$OpenClawConfig = if ($env:OPENCLAW_CONFIG_PATH) { [IO.Path]::GetFullPath((Join-Path (Get-Location) $env:OPENCLAW_CONFIG_PATH)) } else { Join-Path $HOME '.openclaw\openclaw.json' }
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$LogPath = Join-Path $Downloads "CNX_V093_GATEWAY_CONVERGENCE_$Stamp.txt"
$JsonPath = Join-Path $Downloads "CNX_V093_GATEWAY_CONVERGENCE_$Stamp.json"

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
    schemaVersion=1
    suite='v0.9.3-gateway-durable-recovery-convergence'
    startedAt=(Get-Date).ToString('o')
    recoveryFuseSeconds=$RecoveryFuseSeconds
    harness=[ordered]@{pid=[int]$PID;process=Get-ProcessRecord -ProcessId ([int]$PID);ancestorPids=@(Get-AncestorPids -StartPid ([int]$PID))}
    steps=@()
    result='running'
    error=$null
}
function Save-Evidence { $Evidence | ConvertTo-Json -Depth 50 | Set-Content -Path $JsonPath -Encoding UTF8 }
function Log { param([string]$Text) $line="[$((Get-Date).ToString('o'))] $Text"; Write-Host $line; Add-Content -Path $LogPath -Value $line -Encoding UTF8 }
function Step { param([string]$Name,[string]$Status,$Data) $Evidence.steps += [ordered]@{name=$Name;status=$Status;at=(Get-Date).ToString('o');data=$Data}; Save-Evidence }

function Invoke-CnxJson {
    param([string]$Name,[string[]]$CommandArgs,[int[]]$AllowedExitCodes=@(0),[switch]$Quiet)
    $copy=@($CommandArgs)
    if (-not $Quiet) { Log "START $Name :: cnx.cmd $($copy -join ' ')" }
    $sw=[Diagnostics.Stopwatch]::StartNew(); $text=& $Cnx @copy 2>&1 | Out-String; $rc=$LASTEXITCODE; $sw.Stop()
    if (-not ($AllowedExitCodes -contains $rc)) { throw "$Name failed with exit code $rc." }
    try { $doc=$text | ConvertFrom-Json } catch { throw "$Name did not return valid JSON." }
    if (-not $Quiet) { Step $Name 'PASS' ([ordered]@{exitCode=$rc;durationSeconds=[math]::Round($sw.Elapsed.TotalSeconds,3);requestedArguments=$copy;output=$text}) }
    [pscustomobject]@{Document=$doc;ExitCode=$rc;DurationSeconds=$sw.Elapsed.TotalSeconds}
}
function Read-Config { Get-Content $OpenClawConfig -Raw | ConvertFrom-Json }
function Get-GatewayPort { $cfg=Read-Config; if($null -ne $cfg.gateway -and $null -ne $cfg.gateway.port){[int]$cfg.gateway.port}else{18789} }
function Get-Listener {
    param([int]$Port)
    $rows=@(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue)
    if($rows.Count -eq 0){return [ordered]@{port=$Port;listening=$false;pid=$null;process=$null}}
    $p=[int]$rows[0].OwningProcess
    [ordered]@{port=$Port;listening=$true;pid=$p;process=Get-ProcessRecord -ProcessId $p}
}
function Get-RecoverySummary {
    param($Document)
    $maintenance=@($Document.checks|Where-Object{$_.name -eq 'Maintenance/recovery fence'})
    $incident=@($Document.checks|Where-Object{$_.name -eq 'Provider recovery incident'})
    [ordered]@{
        verdict=[string]$Document.verdict
        exitCode=[int]$Document.exitCode
        maintenance=$(if($maintenance.Count -eq 1){$maintenance[0]}else{$null})
        providerIncident=$(if($incident.Count -eq 1){$incident[0]}else{$null})
    }
}
function Assert-InitialBaseline {
    $status=(Invoke-CnxJson -Name 'status-before' -CommandArgs @('status')).Document
    $provider=(Invoke-CnxJson -Name 'provider-before' -CommandArgs @('provider','status','--json')).Document
    $recovery=(Invoke-CnxJson -Name 'recovery-before' -CommandArgs @('check','recovery','--json') -AllowedExitCodes @(0,1)).Document
    $gateway=Get-Listener -Port (Get-GatewayPort); $ollama=Get-Listener -Port 11434
    $state=$status.host.state
    $ok=([string]$state.mode -eq 'managed') -and ([string]$state.selectedProvider -eq 'ollama') -and ([string]$provider.selectedProvider -eq 'ollama') -and ([string]$recovery.verdict -eq 'READY') -and [bool]$gateway.listening -and [bool]$ollama.listening
    Step 'assert-initial-baseline' $(if($ok){'PASS'}else{'FAIL'}) ([ordered]@{mode=[string]$state.mode;hostProvider=[string]$state.selectedProvider;provider=[string]$provider.selectedProvider;recovery=Get-RecoverySummary $recovery;gateway=$gateway;ollama=$ollama})
    if(-not $ok){throw 'Initial managed Ollama baseline is not READY.'}
    return $gateway
}
function Assert-SafeGatewayTarget {
    param($Snapshot)
    if(-not [bool]$Snapshot.listening -or $null -eq $Snapshot.process){throw 'Gateway listener is not present.'}
    $target=$Snapshot.process; $name=([string]$target.name).ToLowerInvariant(); $cmd=([string]$target.commandLine).ToLowerInvariant(); $targetPid=[int]$target.pid
    $banned=@('powershell.exe','pwsh.exe','cmd.exe','conhost.exe','firefox.exe','explorer.exe','windowsterminal.exe','openconsole.exe')
    if($banned -contains $name){throw "Refusing unsafe target $name."}
    if($targetPid -eq [int]$PID){throw 'Refusing to kill harness.'}
    $anc=@(Get-AncestorPids -StartPid ([int]$PID)); if($anc -contains $targetPid){throw 'Refusing to kill harness ancestor.'}
    if($name -ne 'node.exe' -or $cmd -notmatch 'openclaw' -or $cmd -notmatch 'gateway'){throw "Refusing unverified Gateway target pid=$targetPid."}
    Step 'safe-kill-target-gateway' 'PASS' ([ordered]@{target=$target;harnessPid=[int]$PID;harnessAncestors=$anc})
    return $target
}
function Wait-NewGateway {
    param([int]$Port,[int]$OldPid)
    $deadline=(Get-Date).AddSeconds($RecoveryFuseSeconds); $last=$null
    while((Get-Date)-lt $deadline){
        $last=Get-Listener -Port $Port
        if([bool]$last.listening -and $null -ne $last.pid -and [int]$last.pid -ne $OldPid){Step 'observe-gateway-listener-recovered' 'PASS' ([ordered]@{oldPid=$OldPid;observed=$last;observationFuseSeconds=$RecoveryFuseSeconds});return $last}
        Start-Sleep -Seconds 1
    }
    Step 'observe-gateway-listener-recovered' 'FAIL' ([ordered]@{oldPid=$OldPid;lastObserved=$last;observationFuseSeconds=$RecoveryFuseSeconds})
    throw 'Gateway listener did not recover inside observation fuse.'
}
function Wait-RecoveryReady {
    $deadline=(Get-Date).AddSeconds($RecoveryFuseSeconds); $attempt=0; $first=$null; $last=$null; $sw=[Diagnostics.Stopwatch]::StartNew()
    while((Get-Date)-lt $deadline){
        $attempt++
        $r=Invoke-CnxJson -Name "recovery-convergence-$attempt" -CommandArgs @('check','recovery','--json') -AllowedExitCodes @(0,1) -Quiet
        $last=Get-RecoverySummary $r.Document
        if($null -eq $first){$first=$last}
        if([string]$r.Document.verdict -eq 'READY'){
            $sw.Stop(); Step 'observe-durable-recovery-converged' 'PASS' ([ordered]@{observationOnly=$true;attempts=$attempt;elapsedSeconds=[math]::Round($sw.Elapsed.TotalSeconds,3);firstObserved=$first;finalObserved=$last})
            return $r.Document
        }
        Start-Sleep -Seconds 2
    }
    $sw.Stop(); Step 'observe-durable-recovery-converged' 'FAIL' ([ordered]@{observationOnly=$true;attempts=$attempt;elapsedSeconds=[math]::Round($sw.Elapsed.TotalSeconds,3);firstObserved=$first;lastObserved=$last;observationFuseSeconds=$RecoveryFuseSeconds})
    throw 'Durable recovery state did not converge to READY inside observation fuse.'
}
function Best-Effort-Cleanup {
    try {
        $text=& $Cnx start 2>&1 | Out-String; $rc=$LASTEXITCODE
        Step 'cleanup-start' $(if($rc -eq 0){'PASS'}else{'FAIL'}) ([ordered]@{exitCode=$rc;output=$text})
    } catch { Step 'cleanup-start' 'FAIL' ([ordered]@{error=$_.Exception.Message}) }
}

Set-Content -Path $LogPath -Value "CogentNexus v0.9.3 Gateway Durable Recovery Convergence Diagnostic`r`n" -Encoding UTF8
Save-Evidence
try {
    if(-not(Test-Path $Cnx)){throw "cnx.cmd not found: $Cnx"}
    $answer=Read-Host 'This will hard-kill the exact validated OpenClaw Gateway PID once. Type y to continue'
    if($answer -cne 'y'){throw 'Diagnostic cancelled.'}
    Step 'explicit-disruptive-confirmation' 'PASS' ([ordered]@{confirmation='y'})
    $before=Assert-InitialBaseline
    $target=Assert-SafeGatewayTarget -Snapshot $before
    Stop-Process -Id ([int]$target.pid) -Force -ErrorAction Stop
    Step 'inject-gateway-hard-crash' 'PASS' ([ordered]@{target=$target;method='Stop-Process exact PID only'})
    $after=Wait-NewGateway -Port (Get-GatewayPort) -OldPid ([int]$target.pid)
    $ready=Wait-RecoveryReady
    $status=(Invoke-CnxJson -Name 'status-after-convergence' -CommandArgs @('status')).Document
    $provider=(Invoke-CnxJson -Name 'provider-after-convergence' -CommandArgs @('provider','status','--json')).Document
    $gateway=Get-Listener -Port (Get-GatewayPort); $ollama=Get-Listener -Port 11434
    $state=$status.host.state
    $ok=([string]$state.mode -eq 'managed') -and ([string]$state.selectedProvider -eq 'ollama') -and ([string]$provider.selectedProvider -eq 'ollama') -and [bool]$gateway.listening -and [bool]$ollama.listening
    Step 'assert-final-managed-baseline' $(if($ok){'PASS'}else{'FAIL'}) ([ordered]@{mode=[string]$state.mode;hostProvider=[string]$state.selectedProvider;provider=[string]$provider.selectedProvider;gateway=$gateway;ollama=$ollama;recovery=Get-RecoverySummary $ready})
    if(-not $ok){throw 'Final managed baseline failed after durable recovery convergence.'}
    $Evidence.result='PASS';$Evidence.completedAt=(Get-Date).ToString('o');Save-Evidence;Log 'COGENTNEXUS v0.9.3 GATEWAY DURABLE RECOVERY CONVERGENCE: PASS';Write-Host "Evidence: $LogPath";Write-Host "Evidence JSON: $JsonPath";exit 0
} catch {
    $Evidence.result='FAIL';$Evidence.error=$_.Exception.Message;$Evidence.failedAt=(Get-Date).ToString('o');Save-Evidence;Log "FAIL :: $($_.Exception.Message)";Best-Effort-Cleanup;Save-Evidence;Write-Host "Evidence: $LogPath";Write-Host "Evidence JSON: $JsonPath";exit 1
}
