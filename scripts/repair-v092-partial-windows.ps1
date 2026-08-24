[CmdletBinding()]
param(
    [string]$Workspace = (Join-Path $HOME '.openclaw\workspace'),
    [switch]$SyntaxOnly
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($env:OS -ne 'Windows_NT') {
    throw 'This repair helper is Windows-only.'
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Version = (Get-Content -LiteralPath (Join-Path $RepoRoot 'VERSION') -Raw).Trim()
if ($Version -ne '0.9.3') {
    throw "Expected CogentNexus-OpenClaw v0.9.3 candidate; found '$Version'."
}

$Downloads = Join-Path $HOME 'Downloads'
New-Item -ItemType Directory -Force -Path $Downloads | Out-Null
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$LogPath = Join-Path $Downloads "CNXCLAW_V092_PARTIAL_REPAIR_$Stamp.txt"
$BackupRoot = Join-Path $Downloads "CNXCLAW_V092_PARTIAL_REPAIR_BACKUP_$Stamp"
$InstalledSkill = Join-Path $Workspace 'skills\cogentnexus-openclaw'
$InstalledScripts = Join-Path $InstalledSkill 'scripts'
$Cnx = Join-Path $Workspace 'cnxclaw.cmd'
$Root = Join-Path $Workspace '.cogentnexus-openclaw'
$OwnershipScript = Join-Path $RepoRoot 'skills\cogentnexus-openclaw\scripts\namespace_ownership.py'
$Controller = Join-Path $Root 'host\controller.json'
$RouteState = Join-Path $Root 'host\openclaw-route-v092.json'
$WatchdogSnapshot = Join-Path $Root 'host\openclaw-watchdog-compat.json'
$OpenClawConfig = if ($env:OPENCLAW_CONFIG_PATH) {
    [IO.Path]::GetFullPath($env:OPENCLAW_CONFIG_PATH)
} else {
    Join-Path $HOME '.openclaw\openclaw.json'
}

$RepairFiles = @(
    'provider_event_liveness_v092.py',
    'checks_v092.py',
    'host_control_v092.py',
    'host_v092.py'
)

function Require-File([string]$Path, [string]$Label) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "$Label not found: $Path"
    }
}

function Invoke-Checked {
    param(
        [string]$Label,
        [scriptblock]$Action,
        [int[]]$AllowedExitCodes = @(0)
    )
    Write-Output ""
    Write-Output "============================================================"
    Write-Output $Label
    Write-Output "============================================================"
    & $Action
    $code = $LASTEXITCODE
    if ($null -eq $code) { $code = 0 }
    Write-Output "[exitCode=$code]"
    if ($AllowedExitCodes -notcontains [int]$code) {
        throw "$Label failed with exit code $code"
    }
}

function Get-CnxAdapterProcesses {
    return @(
        Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
            Where-Object {
                $null -ne $_.CommandLine -and
                $_.CommandLine -match 'provider_events_v092\.py' -and
                $_.CommandLine -match '\.cogentnexus-openclaw'
            } |
            Select-Object ProcessId, ParentProcessId, Name, CommandLine
    )
}

if ($SyntaxOnly) {
    Write-Host 'CogentNexus-OpenClaw v0.9.3 partial repair helper syntax/load: PASS'
    exit 0
}

$Result = 0
try {
    & {
        & python $OwnershipScript verify --root $Root --workspace $Workspace | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'Ownership manifest mismatch; refusing repair mutation.' }
        Write-Output 'CogentNexus-OpenClaw v0.9.3 Partial MANAGED -> Native Repair'
        Write-Output "Generated : $((Get-Date).ToString('o'))"
        Write-Output "Repo      : $RepoRoot"
        Write-Output "Workspace : $Workspace"
        Write-Output "Backup    : $BackupRoot"
        Write-Output ''
        Write-Output 'Purpose:'
        Write-Output '- Repair only the v0.9.2 files implicated by live acceptance evidence.'
        Write-Output '- Return an interrupted partial MANAGED install to PASSTHROUGH/native.'
        Write-Output '- Do not reset, uninstall, or delete provider installations.'

        Require-File $Cnx 'Installed cnxclaw.cmd'
        Require-File $Controller 'CogentNexus-OpenClaw controller state'
        Require-File $RouteState 'v0.9.2 route baseline state'
        Require-File $WatchdogSnapshot 'v0.9.1 watchdog compatibility snapshot'
        Require-File $OpenClawConfig 'OpenClaw config'

        foreach ($name in $RepairFiles) {
            Require-File (Join-Path $RepoRoot "skills\cogentnexus-openclaw\scripts\$name") "Candidate repair source $name"
        }

        $watchdogBaseline = Get-Content -LiteralPath $WatchdogSnapshot -Raw | ConvertFrom-Json

        Write-Output ''
        Write-Output '============================================================'
        Write-Output 'PRE-REPAIR STATE'
        Write-Output '============================================================'
        Get-Content -LiteralPath $Controller -Raw
        Write-Output ''
        Write-Output '--- route baseline state ---'
        Get-Content -LiteralPath $RouteState -Raw
        Write-Output ''
        Write-Output '--- watchdog baseline state ---'
        Get-Content -LiteralPath $WatchdogSnapshot -Raw
        Write-Output ''
        Write-Output '--- provider adapter processes ---'
        $beforeProcesses = Get-CnxAdapterProcesses
        if ($beforeProcesses.Count -eq 0) {
            Write-Output 'none'
        } else {
            $beforeProcesses | Format-List | Out-String -Width 260 | Write-Output
        }

        New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
        foreach ($name in $RepairFiles) {
            $installed = Join-Path $InstalledScripts $name
            if (Test-Path -LiteralPath $installed) {
                Copy-Item -LiteralPath $installed -Destination (Join-Path $BackupRoot $name) -Force
            }
        }

        Write-Output ''
        Write-Output '============================================================'
        Write-Output 'STAGE VERIFIED v0.9.2 SAFETY FIXES'
        Write-Output '============================================================'
        foreach ($name in $RepairFiles) {
            $source = Join-Path $RepoRoot "skills\cogentnexus-openclaw\scripts\$name"
            $target = Join-Path $InstalledScripts $name
            Copy-Item -LiteralPath $source -Destination $target -Force
            $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
            $targetHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
            Write-Output "$name source=$sourceHash installed=$targetHash"
            if ($sourceHash -ne $targetHash) {
                throw "Installed repair file hash mismatch: $name"
            }
        }

        Invoke-Checked 'PYTHON COMPILE STAGED FILES' {
            & python -m py_compile @($RepairFiles | ForEach-Object { Join-Path $InstalledScripts $_ })
        }

        Invoke-Checked 'DISABLE CNXCLAW / RESTORE NATIVE BOUNDARY' {
            & $Cnx disable
        }

        Invoke-Checked 'OPENCLAW CONFIG VALIDATE' {
            & openclaw.cmd config validate
        }

        Invoke-Checked 'GATEWAY STATUS' {
            & openclaw.cmd gateway status
        }

        Invoke-Checked 'CNX STATUS AFTER DISABLE' {
            & $Cnx status
        }

        Invoke-Checked 'CNX RECOVERY CHECK AFTER FIX' {
            & $Cnx check recovery --json
        } @(0,1)

        Invoke-Checked 'OPENCLAW PLUGIN LIST' {
            & openclaw.cmd plugins list --json
        }

        Write-Output ''
        Write-Output '============================================================'
        Write-Output 'VERIFY PASSTHROUGH + ADAPTER RELEASE'
        Write-Output '============================================================'
        $state = Get-Content -LiteralPath $Controller -Raw | ConvertFrom-Json
        Write-Output "mode=$($state.mode)"
        Write-Output "desiredGateway=$($state.desiredGateway)"
        Write-Output "desiredProvider=$($state.desiredProvider)"
        Write-Output "selectedProvider=$($state.selectedProvider)"
        if ($state.mode -ne 'passthrough') {
            throw "Expected PASSTHROUGH after repair; got '$($state.mode)'"
        }

        $afterProcesses = Get-CnxAdapterProcesses
        if ($afterProcesses.Count -ne 0) {
            $afterProcesses | Format-List | Out-String -Width 260 | Write-Output
            throw "Provider event adapter process remains after disable: $($afterProcesses.Count)"
        }
        Write-Output 'providerEventAdapterProcesses=0'

        Write-Output ''
        Write-Output '============================================================'
        Write-Output 'VERIFY v0.9.1 WATCHDOG BASELINE RESTORED'
        Write-Output '============================================================'
        if (Test-Path -LiteralPath $WatchdogSnapshot) {
            throw 'Watchdog compatibility snapshot still exists after successful disable'
        }
        $openclaw = Get-Content -LiteralPath $OpenClawConfig -Raw | ConvertFrom-Json
        $diagnostics = $openclaw.diagnostics
        $watchdogPresent = $null -ne $diagnostics -and ($diagnostics.PSObject.Properties.Name -contains 'stuckSessionAbortMs')
        $watchdogValue = if ($watchdogPresent) { $diagnostics.stuckSessionAbortMs } else { $null }
        $expectedWatchdogPresent = [bool]$watchdogBaseline.originalPresent
        $expectedWatchdogValue = $watchdogBaseline.originalValue
        Write-Output "expectedPresent=$expectedWatchdogPresent actualPresent=$watchdogPresent"
        Write-Output "expectedValue=$expectedWatchdogValue actualValue=$watchdogValue"
        if ($watchdogPresent -ne $expectedWatchdogPresent) {
            throw 'OpenClaw native watchdog presence was not restored to the v0.9.1 pre-CNXCLAW snapshot'
        }
        if ($watchdogPresent) {
            $expectedJson = $expectedWatchdogValue | ConvertTo-Json -Compress -Depth 20
            $actualJson = $watchdogValue | ConvertTo-Json -Compress -Depth 20
            if ($expectedJson -ne $actualJson) {
                throw 'OpenClaw native watchdog value was not restored to the v0.9.1 pre-CNXCLAW snapshot'
            }
        }
        Write-Output 'watchdogBaselineRestored=true'

        Write-Output ''
        Write-Output '============================================================'
        Write-Output 'VERIFY CNXCLAW PLUGIN IS NOT ENABLED IN PASSTHROUGH'
        Write-Output '============================================================'
        $entries = if ($null -ne $openclaw.plugins) { $openclaw.plugins.entries } else { $null }
        $pluginEntry = if ($null -ne $entries) { $entries.'cogentnexus-openclaw' } else { $null }
        $pluginEnabled = $null -ne $pluginEntry -and $pluginEntry.enabled -eq $true
        Write-Output "pluginPresent=$($null -ne $pluginEntry)"
        Write-Output "pluginEnabled=$pluginEnabled"
        if ($pluginEnabled) {
            throw 'CogentNexus-OpenClaw plugin remains enabled after PASSTHROUGH repair boundary'
        }

        Write-Output ''
        Write-Output '============================================================'
        Write-Output 'VERIFY v0.9.2 ROUTE BASELINE RESTORED'
        Write-Output '============================================================'
        $verifyCode = @'
import copy
import json
import sys
from pathlib import Path

scripts = Path(sys.argv[1])
root = Path(sys.argv[2])
sys.path.insert(0, str(scripts))
import openclaw_route_v092 as route

config_path = route.openclaw_config_path()
config = route._load_json(config_path)
state = route._load_state(root)
expected = copy.deepcopy(config)
route._restore_managed_knobs(expected, state, restore_model=True)
match = expected == config
print(json.dumps({
    "configPath": str(config_path),
    "managedKnobsMatchBaseline": match,
    "currentModel": route._primary_model(config),
    "baseline": state.get("baseline"),
}, ensure_ascii=False, indent=2))
raise SystemExit(0 if match else 2)
'@
        $verifyCode | & python - $InstalledScripts $Root
        $routeRc = $LASTEXITCODE
        Write-Output "[exitCode=$routeRc]"
        if ($routeRc -ne 0) {
            throw 'v0.9.2-owned OpenClaw route/timeout/compat fields do not match the durable pre-CNXCLAW baseline'
        }

        Write-Output ''
        Write-Output '============================================================'
        Write-Output 'REPAIR RESULT: PASS'
        Write-Output '============================================================'
        Write-Output 'Machine is back at the CNXCLAW PASSTHROUGH/native boundary.'
        Write-Output 'No reset or uninstall was performed.'
        Write-Output "Finished: $((Get-Date).ToString('o'))"
    } *> $LogPath
}
catch {
    $Result = 1
    @(
        '',
        '============================================================',
        'REPAIR RESULT: FAIL',
        '============================================================',
        "Error: $($_.Exception.Message)",
        "At: $((Get-Date).ToString('o'))"
    ) | Add-Content -LiteralPath $LogPath -Encoding UTF8
}

Write-Host ''
Write-Host "RepairExitCode: $Result"
Write-Host 'Repair log:'
Write-Host $LogPath
if (Test-Path -LiteralPath $BackupRoot) {
    Write-Host 'Backup:'
    Write-Host $BackupRoot
}
exit $Result
