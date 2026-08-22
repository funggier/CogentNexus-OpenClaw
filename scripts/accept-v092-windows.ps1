[CmdletBinding()]
param(
    [ValidateSet('ollama','lmstudio')]
    [string]$Provider = 'lmstudio',

    [switch]$RunDestructive
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($env:OS -ne 'Windows_NT') {
    throw 'This acceptance harness is Windows-only.'
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Version = (Get-Content (Join-Path $RepoRoot 'VERSION') -Raw).Trim()
if ($Version -ne '0.9.2') {
    throw "Expected CogentNexus Core 0.9.2 candidate; found '$Version'."
}

$Downloads = Join-Path $HOME 'Downloads'
New-Item -ItemType Directory -Force -Path $Downloads | Out-Null
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$LogPath = Join-Path $Downloads "CNX_V092_WINDOWS_ACCEPT_$Stamp.txt"
$JsonPath = Join-Path $Downloads "CNX_V092_WINDOWS_ACCEPT_$Stamp.json"
$OpenClawConfig = if ($env:OPENCLAW_CONFIG_PATH) {
    [IO.Path]::GetFullPath((Join-Path (Get-Location) $env:OPENCLAW_CONFIG_PATH))
} else {
    Join-Path $HOME '.openclaw\openclaw.json'
}

$Evidence = [ordered]@{
    schemaVersion = 2
    candidateVersion = $Version
    startedAt = (Get-Date).ToString('o')
    provider = $Provider
    destructiveRequested = [bool]$RunDestructive
    repoRoot = $RepoRoot
    openclawConfig = $OpenClawConfig
    steps = @()
    result = 'running'
}

function Write-Evidence {
    param([string]$Message)
    $line = "[$((Get-Date).ToString('o'))] $Message"
    Write-Host $line
    Add-Content -Path $LogPath -Value $line -Encoding UTF8
}

function Save-Evidence {
    $Evidence | ConvertTo-Json -Depth 40 | Set-Content -Path $JsonPath -Encoding UTF8
}

function Add-Step {
    param(
        [string]$Name,
        [string]$Status,
        [hashtable]$Data
    )
    $Evidence.steps += [ordered]@{
        name = $Name
        status = $Status
        at = (Get-Date).ToString('o')
        data = $Data
    }
    Save-Evidence
}

function ConvertTo-ComparableJson {
    param($Value)
    if ($null -eq $Value) { return '<null>' }
    return ($Value | ConvertTo-Json -Depth 30 -Compress)
}

function Test-EquivalentValue {
    param($Left, $Right)
    return (ConvertTo-ComparableJson $Left) -eq (ConvertTo-ComparableJson $Right)
}

function Invoke-Captured {
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$Arguments,
        [int[]]$AllowedExitCodes = @(0)
    )

    Write-Evidence "START $Name :: $FilePath $($Arguments -join ' ')"
    $stdout = Join-Path $env:TEMP "cnx-v092-$Stamp-$([guid]::NewGuid().ToString('N')).out.txt"
    $stderr = Join-Path $env:TEMP "cnx-v092-$Stamp-$([guid]::NewGuid().ToString('N')).err.txt"
    try {
        $sw = [Diagnostics.Stopwatch]::StartNew()
        $proc = Start-Process -FilePath $FilePath -ArgumentList $Arguments -Wait -PassThru -NoNewWindow `
            -RedirectStandardOutput $stdout -RedirectStandardError $stderr
        $sw.Stop()
        $outText = if (Test-Path $stdout) { Get-Content $stdout -Raw } else { '' }
        $errText = if (Test-Path $stderr) { Get-Content $stderr -Raw } else { '' }
        Add-Content -Path $LogPath -Value $outText -Encoding UTF8
        Add-Content -Path $LogPath -Value $errText -Encoding UTF8
        $ok = $AllowedExitCodes -contains $proc.ExitCode
        $stepStatus = if ($ok) { 'PASS' } else { 'FAIL' }
        Add-Step $Name $stepStatus @{
            command = @($FilePath) + $Arguments
            exitCode = $proc.ExitCode
            durationSeconds = [math]::Round($sw.Elapsed.TotalSeconds, 2)
            stdout = $outText
            stderr = $errText
        }
        if (-not $ok) {
            throw "$Name failed with exit code $($proc.ExitCode)."
        }
        Write-Evidence "PASS $Name"
        return [pscustomobject]@{ ExitCode = $proc.ExitCode; Stdout = $outText; Stderr = $errText }
    }
    finally {
        Remove-Item $stdout,$stderr -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-CnxConfirmed {
    param(
        [string]$Name,
        [string[]]$Arguments
    )
    $cnx = Join-Path $HOME '.openclaw\workspace\cnx.cmd'
    if (-not (Test-Path $cnx)) {
        throw "cnx.cmd not found: $cnx"
    }
    $stdin = Join-Path $env:TEMP "cnx-v092-$Stamp-$([guid]::NewGuid().ToString('N')).in.txt"
    $stdout = Join-Path $env:TEMP "cnx-v092-$Stamp-$([guid]::NewGuid().ToString('N')).out.txt"
    $stderr = Join-Path $env:TEMP "cnx-v092-$Stamp-$([guid]::NewGuid().ToString('N')).err.txt"
    try {
        "y`r`n" | Set-Content -Path $stdin -Encoding ASCII -NoNewline
        $quoted = '"' + $cnx + '" ' + (($Arguments | ForEach-Object {
            if ($_ -match '[\s"]') { '"' + ($_ -replace '"','\"') + '"' } else { $_ }
        }) -join ' ')
        Write-Evidence "START $Name :: cnx.cmd $($Arguments -join ' ') [explicit y supplied after harness confirmation]"
        $sw = [Diagnostics.Stopwatch]::StartNew()
        $proc = Start-Process -FilePath 'cmd.exe' -ArgumentList @('/d','/c',$quoted) -Wait -PassThru -NoNewWindow `
            -RedirectStandardInput $stdin -RedirectStandardOutput $stdout -RedirectStandardError $stderr
        $sw.Stop()
        $outText = if (Test-Path $stdout) { Get-Content $stdout -Raw } else { '' }
        $errText = if (Test-Path $stderr) { Get-Content $stderr -Raw } else { '' }
        Add-Content -Path $LogPath -Value $outText -Encoding UTF8
        Add-Content -Path $LogPath -Value $errText -Encoding UTF8
        $ok = $proc.ExitCode -eq 0
        $stepStatus = if ($ok) { 'PASS' } else { 'FAIL' }
        Add-Step $Name $stepStatus @{
            command = @('cnx.cmd') + $Arguments
            explicitConfirmation = 'y'
            exitCode = $proc.ExitCode
            durationSeconds = [math]::Round($sw.Elapsed.TotalSeconds, 2)
            stdout = $outText
            stderr = $errText
        }
        if (-not $ok) { throw "$Name failed with exit code $($proc.ExitCode)." }
        Write-Evidence "PASS $Name"
    }
    finally {
        Remove-Item $stdin,$stdout,$stderr -Force -ErrorAction SilentlyContinue
    }
}

function Read-OpenClawFields {
    if (-not (Test-Path $OpenClawConfig)) { return $null }
    $cfg = Get-Content $OpenClawConfig -Raw | ConvertFrom-Json
    $primary = $null
    if ($cfg.agents.defaults.model -is [string]) {
        $primary = $cfg.agents.defaults.model
    } elseif ($null -ne $cfg.agents.defaults.model.primary) {
        $primary = [string]$cfg.agents.defaults.model.primary
    }
    $lm = $cfg.models.providers.lmstudio_local
    $lmModel = if ($null -ne $lm.models -and $lm.models.Count -gt 0) { $lm.models[0] } else { $null }
    return [ordered]@{
        primaryModel = $primary
        agentTimeoutSeconds = $cfg.agents.defaults.timeoutSeconds
        stuckSessionAbortMs = $cfg.diagnostics.stuckSessionAbortMs
        lmstudioTimeoutSeconds = if ($null -ne $lm) { $lm.timeoutSeconds } else { $null }
        lmstudioCompat = if ($null -ne $lmModel) { $lmModel.compat } else { $null }
        cnxPluginPresent = $null -ne $cfg.plugins.entries.'cogentnexus-rotation'
    }
}

function Assert-SelectedProvider {
    param([string]$Expected)
    $cnx = Join-Path $HOME '.openclaw\workspace\cnx.cmd'
    $result = Invoke-Captured "provider-status-$Expected" $cnx @('provider','status','--json')
    $doc = $result.Stdout | ConvertFrom-Json
    if ($doc.selectedProvider -ne $Expected) {
        throw "Expected selectedProvider=$Expected; got '$($doc.selectedProvider)'."
    }
}

function Assert-ProviderEventAdapter {
    param(
        [string]$Label,
        [bool]$Expected,
        [bool]$Running
    )
    $cnx = Join-Path $HOME '.openclaw\workspace\cnx.cmd'
    $result = Invoke-Captured "check-recovery-$Label" $cnx @('check','recovery','--json') @(0,1)
    $doc = $result.Stdout | ConvertFrom-Json
    $rows = @($doc.checks | Where-Object { $_.name -eq 'Provider event adapter' })
    if ($rows.Count -ne 1) {
        throw "Expected exactly one Provider event adapter diagnostic row at '$Label'; found $($rows.Count)."
    }
    $actualExpected = [bool]$rows[0].details.expected
    $actualRunning = [bool]$rows[0].details.running
    $matches = ($actualExpected -eq $Expected) -and ($actualRunning -eq $Running)
    $status = if ($matches) { 'PASS' } else { 'FAIL' }
    Add-Step "provider-event-adapter-$Label" $status @{
        expected = $Expected
        running = $Running
        actualExpected = $actualExpected
        actualRunning = $actualRunning
        diagnostic = $rows[0]
    }
    if (-not $matches) {
        throw "Provider event adapter mismatch at '$Label': expected expected=$Expected running=$Running; actual expected=$actualExpected running=$actualRunning."
    }
}

function Get-CnxProviderAdapterProcesses {
    return @(
        Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
            Where-Object {
                $null -ne $_.CommandLine -and
                $_.CommandLine -match 'provider_events_v092\.py' -and
                $_.CommandLine -match '\.cogent'
            } |
            Select-Object ProcessId, CommandLine
    )
}

try {
    Set-Content -Path $LogPath -Value "CogentNexus v0.9.2 Windows Live Acceptance`r`n" -Encoding UTF8
    Save-Evidence

    $beforeFields = Read-OpenClawFields
    $Evidence.openclawBefore = $beforeFields
    Save-Evidence

    Invoke-Captured 'openclaw-version' 'openclaw.cmd' @('--version') | Out-Null
    Invoke-Captured 'openclaw-config-before' 'openclaw.cmd' @('config','validate') | Out-Null

    $install = Join-Path $RepoRoot 'scripts\install.ps1'
    Invoke-Captured 'install-candidate' 'powershell.exe' @(
        '-NoProfile','-ExecutionPolicy','Bypass','-File',$install,'-Provider',$Provider
    ) | Out-Null

    $cnx = Join-Path $HOME '.openclaw\workspace\cnx.cmd'
    if (-not (Test-Path $cnx)) { throw 'Candidate install did not create cnx.cmd.' }

    Invoke-Captured 'check-system-managed' $cnx @('check','system','--json') @(0,1) | Out-Null
    Assert-SelectedProvider $Provider
    $managedAdapter = $Provider -eq 'lmstudio'
    Assert-ProviderEventAdapter 'managed-after-install' $managedAdapter $managedAdapter

    Invoke-Captured 'disable-native' $cnx @('disable') | Out-Null
    Assert-ProviderEventAdapter 'after-disable' $false $false
    Invoke-Captured 'gateway-after-disable' 'openclaw.cmd' @('gateway','status') | Out-Null
    $disabledFields = Read-OpenClawFields
    Add-Step 'native-fields-after-disable' 'PASS' @{ fields = $disabledFields }

    Invoke-Captured 'enable-managed' $cnx @('enable','--provider',$Provider) | Out-Null
    Assert-SelectedProvider $Provider
    Assert-ProviderEventAdapter 'after-enable' $managedAdapter $managedAdapter

    Invoke-Captured 'stop-managed' $cnx @('stop') | Out-Null
    Assert-ProviderEventAdapter 'after-stop' $false $false
    Invoke-Captured 'start-after-stop' $cnx @('start') | Out-Null
    Assert-SelectedProvider $Provider
    Assert-ProviderEventAdapter 'after-start' $managedAdapter $managedAdapter

    $other = if ($Provider -eq 'lmstudio') { 'ollama' } else { 'lmstudio' }
    $prospective = Invoke-Captured "prospective-$other" $cnx @('check','system','--provider',$other,'--json') @(0,1,2)
    try {
        $prospectiveDoc = $prospective.Stdout | ConvertFrom-Json
        $routeCheck = @($prospectiveDoc.checks | Where-Object { $_.name -eq 'OpenClaw prospective model route' })
        $routeStatus = if ($routeCheck.Count -eq 1) { 'PASS' } else { 'FAIL' }
        Add-Step "prospective-route-semantics-$other" $routeStatus @{
            verdict = $prospectiveDoc.verdict
            routeCheck = $routeCheck
        }
        if ($routeCheck.Count -ne 1) { throw 'Prospective provider check did not emit the prospective route item.' }
    } catch {
        throw "Prospective provider check JSON verification failed: $($_.Exception.Message)"
    }

    # Switch only when the prospective check says the alternate route is not NOT_READY/INDETERMINATE.
    if ($prospectiveDoc.verdict -in @('READY','READY_WITH_WARNINGS')) {
        Invoke-Captured "switch-to-$other" $cnx @('start','--provider',$other) | Out-Null
        Assert-SelectedProvider $other
        $otherAdapter = $other -eq 'lmstudio'
        Assert-ProviderEventAdapter "after-switch-to-$other" $otherAdapter $otherAdapter

        Invoke-Captured "switch-back-$Provider" $cnx @('start','--provider',$Provider) | Out-Null
        Assert-SelectedProvider $Provider
        Assert-ProviderEventAdapter "after-switch-back-$Provider" $managedAdapter $managedAdapter
    } else {
        Add-Step "switch-to-$other" 'SKIP' @{ reason = "prospective verdict: $($prospectiveDoc.verdict)" }
    }

    if (-not $RunDestructive) {
        $Evidence.result = 'PASS_NON_DESTRUCTIVE'
        $Evidence.finishedAt = (Get-Date).ToString('o')
        Save-Evidence
        Write-Evidence 'PASS non-destructive acceptance. Full release gate still requires -RunDestructive for reset + uninstall.'
        Write-Host "Evidence: $LogPath"
        Write-Host "Evidence JSON: $JsonPath"
        exit 0
    }

    Write-Host ''
    Write-Host 'DESTRUCTIVE ACCEPTANCE REQUESTED.' -ForegroundColor Yellow
    Write-Host 'This will reset CogentNexus and then uninstall it after verification.' -ForegroundColor Yellow
    $answer = (Read-Host 'Type y to continue with reset + uninstall').Trim().ToLowerInvariant()
    if ($answer -ne 'y') {
        throw 'Destructive acceptance was not explicitly confirmed with y.'
    }

    Invoke-CnxConfirmed 'reset-fresh-managed' @('reset','--provider',$Provider)
    $cnx = Join-Path $HOME '.openclaw\workspace\cnx.cmd'
    Assert-SelectedProvider $Provider
    Invoke-Captured 'check-system-after-reset' $cnx @('check','system','--json') @(0,1) | Out-Null
    Assert-ProviderEventAdapter 'after-reset' $managedAdapter $managedAdapter

    Invoke-CnxConfirmed 'uninstall-cogentnexus' @('uninstall')
    Start-Sleep -Seconds 4

    Invoke-Captured 'gateway-after-uninstall' 'openclaw.cmd' @('gateway','status') | Out-Null
    Invoke-Captured 'openclaw-config-after-uninstall' 'openclaw.cmd' @('config','validate') | Out-Null

    $afterFields = Read-OpenClawFields
    $Evidence.openclawAfter = $afterFields
    $launcherStillExists = Test-Path (Join-Path $HOME '.openclaw\workspace\cnx.cmd')
    $pluginList = Invoke-Captured 'plugins-after-uninstall' 'openclaw.cmd' @('plugins','list','--json')
    $pluginStillRegistered = $pluginList.Stdout -match 'cogentnexus-rotation'
    $adapterProcesses = Get-CnxProviderAdapterProcesses

    $nativeFieldPass = (
        $afterFields.primaryModel -eq $beforeFields.primaryModel -and
        $afterFields.agentTimeoutSeconds -eq $beforeFields.agentTimeoutSeconds -and
        $afterFields.stuckSessionAbortMs -eq $beforeFields.stuckSessionAbortMs -and
        $afterFields.lmstudioTimeoutSeconds -eq $beforeFields.lmstudioTimeoutSeconds -and
        (Test-EquivalentValue $afterFields.lmstudioCompat $beforeFields.lmstudioCompat)
    )
    $finalPass = (
        $nativeFieldPass -and
        -not $pluginStillRegistered -and
        -not $launcherStillExists -and
        -not $afterFields.cnxPluginPresent -and
        $adapterProcesses.Count -eq 0
    )
    $finalStatus = if ($finalPass) { 'PASS' } else { 'FAIL' }
    Add-Step 'final-native-ownership' $finalStatus @{
        before = $beforeFields
        after = $afterFields
        pluginStillRegistered = $pluginStillRegistered
        launcherStillExists = $launcherStillExists
        providerAdapterProcesses = $adapterProcesses
    }
    if (-not $nativeFieldPass) { throw 'Pre-CNX model/request-timeout/watchdog/schema-compat fields were not restored after uninstall.' }
    if ($pluginStillRegistered -or $afterFields.cnxPluginPresent) { throw 'CogentNexus plugin remains registered/configured after uninstall.' }
    if ($launcherStillExists) { throw 'cnx.cmd still exists after uninstall cleanup window.' }
    if ($adapterProcesses.Count -ne 0) { throw 'CogentNexus provider event adapter process remains after uninstall.' }

    $Evidence.result = 'PASS_FULL'
    $Evidence.finishedAt = (Get-Date).ToString('o')
    Save-Evidence
    Write-Evidence 'FULL WINDOWS v0.9.2 ACCEPTANCE: PASS'
    Write-Host "Evidence: $LogPath"
    Write-Host "Evidence JSON: $JsonPath"
}
catch {
    $Evidence.result = 'FAIL'
    $Evidence.error = $_.Exception.Message
    $Evidence.finishedAt = (Get-Date).ToString('o')
    Save-Evidence
    Write-Evidence "FAIL: $($_.Exception.Message)"
    Write-Host "Evidence: $LogPath"
    Write-Host "Evidence JSON: $JsonPath"
    exit 1
}
