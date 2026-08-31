[CmdletBinding()]
param(
    [ValidateSet('ollama','lmstudio')]
    [string]$Provider = 'lmstudio',

    [ValidateRange(5,120)]
    [int]$TimeoutMinutes = 30,

    [switch]$RunDestructive
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($env:OS -ne 'Windows_NT') {
    throw 'This live acceptance runner is Windows-only.'
}

$Harness = Join-Path $PSScriptRoot 'accept-v092-windows-ps51.ps1'
if (-not (Test-Path -LiteralPath $Harness)) {
    throw "Acceptance harness not found: $Harness"
}

$Downloads = Join-Path $HOME 'Downloads'
New-Item -ItemType Directory -Force -Path $Downloads | Out-Null
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$RunnerOut = Join-Path $Downloads "CNXCLAW_V092_LIVE_RUNNER_$Stamp.out.txt"
$RunnerErr = Join-Path $Downloads "CNXCLAW_V092_LIVE_RUNNER_$Stamp.err.txt"
$StartedAt = Get-Date
$Deadline = $StartedAt.AddMinutes($TimeoutMinutes)

function Write-NewText {
    param(
        [string]$Path,
        [ref]$Offset,
        [switch]$ErrorStream
    )
    if (-not (Test-Path -LiteralPath $Path)) { return }
    try {
        $text = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop
    }
    catch { return }
    if ($null -eq $text) { $text = '' }
    $start = [int]$Offset.Value
    if ($text.Length -lt $start) { $start = 0 }
    if ($text.Length -gt $start) {
        $new = $text.Substring($start)
        if ($ErrorStream) { [Console]::Error.Write($new) } else { [Console]::Out.Write($new) }
        $Offset.Value = $text.Length
    }
}

function Show-ActiveTail {
    $files = @(
        Get-ChildItem -LiteralPath $env:TEMP -File -ErrorAction SilentlyContinue |
            Where-Object {
                $_.Name -like 'cnx-v092-*.out.txt' -or $_.Name -like 'cnx-v092-*.err.txt'
            } |
            Where-Object { $_.LastWriteTime -ge $StartedAt.AddSeconds(-5) } |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 4
    )
    foreach ($file in $files) {
        Write-Host "--- active temp: $($file.Name) [$($file.LastWriteTime.ToString('HH:mm:ss'))] ---" -ForegroundColor DarkGray
        Get-Content -LiteralPath $file.FullName -Tail 8 -ErrorAction SilentlyContinue |
            ForEach-Object { Write-Host $_ }
    }
}

function Show-RelevantProcesses {
    $rows = @(
        Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
            Where-Object {
                $null -ne $_.CommandLine -and
                $_.CommandLine -match '(?i)(accept-v092|install\.ps1|cnx\.py|host_control_v092|npm(?:\.cmd)?\s+(ci|run|pack)|openclaw(?:\.cmd)?\s+plugins)'
            } |
            Select-Object ProcessId, ParentProcessId, Name, CommandLine
    )
    if ($rows.Count -gt 0) {
        Write-Host '--- relevant processes ---' -ForegroundColor DarkGray
        $rows | Format-Table -AutoSize | Out-String -Width 240 | Write-Host
    }
}

$arguments = @(
    '-NoProfile',
    '-ExecutionPolicy','Bypass',
    '-File',$Harness,
    '-Provider',$Provider
)
if ($RunDestructive) { $arguments += '-RunDestructive' }

Write-Host "CogentNexus-OpenClaw v0.9.2 observable live acceptance runner"
Write-Host "Harness : $Harness"
Write-Host "Provider: $Provider"
Write-Host "Timeout : $TimeoutMinutes minute(s)"
Write-Host "Runner stdout: $RunnerOut"
Write-Host "Runner stderr: $RunnerErr"
Write-Host ''

$process = Start-Process -FilePath 'powershell.exe' -ArgumentList $arguments -PassThru `
    -WorkingDirectory $PSScriptRoot -RedirectStandardOutput $RunnerOut -RedirectStandardError $RunnerErr

$outOffset = 0
$errOffset = 0
$nextHeartbeat = (Get-Date).AddSeconds(30)
$timedOut = $false

try {
    while (-not $process.HasExited) {
        Start-Sleep -Seconds 2
        $process.Refresh()
        Write-NewText -Path $RunnerOut -Offset ([ref]$outOffset)
        Write-NewText -Path $RunnerErr -Offset ([ref]$errOffset) -ErrorStream

        $now = Get-Date
        if ($now -ge $nextHeartbeat) {
            $elapsed = [math]::Round(($now - $StartedAt).TotalMinutes, 1)
            Write-Host "[$($now.ToString('o'))] RUNNER HEARTBEAT elapsed=${elapsed}m pid=$($process.Id)" -ForegroundColor Cyan
            Show-ActiveTail
            Show-RelevantProcesses
            $nextHeartbeat = $now.AddSeconds(30)
        }

        if ($now -ge $Deadline) {
            $timedOut = $true
            Write-Host "LIVE ACCEPTANCE TIMEOUT after $TimeoutMinutes minute(s); terminating process tree PID $($process.Id)." -ForegroundColor Red
            & taskkill.exe /PID $process.Id /T /F 2>&1 | ForEach-Object { Write-Host $_ }
            break
        }
    }

    try { $process.WaitForExit() } catch {}
    Write-NewText -Path $RunnerOut -Offset ([ref]$outOffset)
    Write-NewText -Path $RunnerErr -Offset ([ref]$errOffset) -ErrorStream

    if ($timedOut) { exit 124 }
    $code = if ($null -ne $process.ExitCode) { [int]$process.ExitCode } else { 1 }
    Write-Host ''
    Write-Host "LiveAcceptanceExitCode: $code"
    exit $code
}
finally {
    if (-not $process.HasExited) {
        & taskkill.exe /PID $process.Id /T /F 2>$null | Out-Null
    }
}
