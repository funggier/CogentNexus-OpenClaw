[CmdletBinding(DefaultParameterSetName = "Run")]
param(
    [Parameter(ParameterSetName = "SelfTest", Mandatory = $true)]
    [switch]$SelfTest,

    [Parameter(ParameterSetName = "Run", Mandatory = $true)]
    [string]$FilePath,

    [Parameter(ParameterSetName = "Run")]
    [string[]]$ArgumentList = @(),

    [Parameter(ParameterSetName = "Run", Mandatory = $true)]
    [string]$StdoutPath,

    [Parameter(ParameterSetName = "Run", Mandatory = $true)]
    [string]$StderrPath,

    [Parameter(ParameterSetName = "Run", Mandatory = $true)]
    [string]$PoststatePath
)

$ErrorActionPreference = "Stop"

function ConvertTo-WindowsQuotedArgument {
    param([AllowEmptyString()][string]$Value)

    if ($null -eq $Value) {
        throw "Process argument must be an observed string; null is not allowed."
    }
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') {
        return $Value
    }

    $builder = New-Object System.Text.StringBuilder
    [void]$builder.Append('"')
    $backslashCount = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') {
            $backslashCount += 1
            continue
        }
        if ($character -eq '"') {
            if ($backslashCount -gt 0) {
                [void]$builder.Append(('\' * (2 * $backslashCount)))
            }
            [void]$builder.Append('\"')
            $backslashCount = 0
            continue
        }
        if ($backslashCount -gt 0) {
            [void]$builder.Append(('\' * $backslashCount))
            $backslashCount = 0
        }
        [void]$builder.Append($character)
    }
    if ($backslashCount -gt 0) {
        [void]$builder.Append(('\' * (2 * $backslashCount)))
    }
    [void]$builder.Append('"')
    return $builder.ToString()
}

function ConvertTo-WindowsCommandLine {
    param([AllowEmptyCollection()][AllowEmptyString()][string[]]$Values = @())

    return (($Values | ForEach-Object { ConvertTo-WindowsQuotedArgument -Value $_ }) -join ' ')
}

function ConvertTo-ObservedExitCode {
    param([AllowNull()]$Value)

    if ($null -eq $Value) {
        throw "Root process exit code was unobserved; refusing to coerce null to zero."
    }
    return [int]$Value
}

function Invoke-ExactRootProcess {
    param(
        [Parameter(Mandatory = $true)][string]$ProcessFilePath,
        [string[]]$ProcessArgumentList = @(),
        [Parameter(Mandatory = $true)][string]$ProcessStdoutPath,
        [Parameter(Mandatory = $true)][string]$ProcessStderrPath
    )

    $startedAt = [DateTimeOffset]::UtcNow
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $commandLine = ConvertTo-WindowsCommandLine -Values $ProcessArgumentList
    $startParameters = @{
        FilePath = $ProcessFilePath
        PassThru = $true
        NoNewWindow = $true
        RedirectStandardOutput = $ProcessStdoutPath
        RedirectStandardError = $ProcessStderrPath
    }
    if ($ProcessArgumentList.Count -gt 0) {
        # Start-Process joins string-array elements in Windows PowerShell 5.1.
        # Supplying one deliberately quoted command-line string preserves exact argv.
        $startParameters["ArgumentList"] = $commandLine
    }
    $process = Start-Process @startParameters

    # Windows PowerShell 5.1 can lose the numeric ExitCode for a quickly
    # exiting redirected child unless its native handle is cached while alive.
    $null = $process.Handle
    $process.WaitForExit()
    $process.Refresh()
    if (-not $process.HasExited) {
        throw "Root process did not reach an observed exited state."
    }
    $rawExitCode = $process.ExitCode
    $exitCode = ConvertTo-ObservedExitCode -Value $rawExitCode
    $stopwatch.Stop()

    return [pscustomobject][ordered]@{
        pid = [int]$process.Id
        startedAtUtc = $startedAt.ToString("o")
        endedAtUtc = [DateTimeOffset]::UtcNow.ToString("o")
        durationSeconds = [Math]::Round($stopwatch.Elapsed.TotalSeconds, 6)
        observedExitCode = $exitCode
    }
}

if ($SelfTest) {
    $observed = @()
    foreach ($expected in @(0, 7)) {
        $stdout = Join-Path $env:TEMP ("cnxclaw-root-exit-{0}.stdout" -f ([guid]::NewGuid().ToString("N")))
        $stderr = Join-Path $env:TEMP ("cnxclaw-root-exit-{0}.stderr" -f ([guid]::NewGuid().ToString("N")))
        try {
            $result = Invoke-ExactRootProcess -ProcessFilePath "cmd.exe" `
                -ProcessArgumentList @("/d", "/c", "exit /b $expected") `
                -ProcessStdoutPath $stdout -ProcessStderrPath $stderr
            if ($null -eq $result.observedExitCode -or [int]$result.observedExitCode -ne $expected) {
                throw "Expected numeric exit code $expected; observed $($result.observedExitCode)."
            }
            $observed += [int]$result.observedExitCode
        }
        finally {
            Remove-Item -LiteralPath $stdout,$stderr -Force -ErrorAction SilentlyContinue
        }
    }
    if ($observed.Count -ne 2 -or $observed[0] -ne 0 -or $observed[1] -ne 7) {
        throw "Root-process numeric exit-code self-test did not preserve both cases."
    }
    Write-Host "CogentNexus-OpenClaw numeric exit-code self-test: PASS (0,7)"

    $nullRejected = $false
    try {
        $nullResult = ConvertTo-ObservedExitCode -Value $null
    }
    catch {
        if ($_.Exception.Message -match "unobserved") { $nullRejected = $true }
        else { throw }
    }
    if (-not $nullRejected) {
        throw "Root-process null exit-code self-test accepted an unobserved value: $nullResult"
    }
    Write-Host "CogentNexus-OpenClaw unobserved null exit-code self-test: PASS"

    $argumentTestRoot = Join-Path $env:TEMP ("cnxclaw root args {0}" -f ([guid]::NewGuid().ToString("N")))
    $argumentProbe = Join-Path $argumentTestRoot "echo arguments.ps1"
    $argumentStdout = Join-Path $argumentTestRoot "arguments.stdout"
    $argumentStderr = Join-Path $argumentTestRoot "arguments.stderr"
    $expectedArguments = @("plain", "space value", 'quote"value', "", 'trailing\')
    try {
        New-Item -ItemType Directory -Force -Path $argumentTestRoot | Out-Null
        [System.IO.File]::WriteAllText(
            $argumentProbe,
            '[Console]::Out.Write((@($args) | ConvertTo-Json -Compress))',
            (New-Object System.Text.UTF8Encoding($false))
        )
        $probeResult = Invoke-ExactRootProcess -ProcessFilePath "powershell.exe" `
            -ProcessArgumentList (@("-NoProfile", "-File", $argumentProbe) + $expectedArguments) `
            -ProcessStdoutPath $argumentStdout -ProcessStderrPath $argumentStderr
        if ($probeResult.observedExitCode -ne 0) {
            throw "Argument probe exited $($probeResult.observedExitCode): $(Get-Content -LiteralPath $argumentStderr -Raw)"
        }
        $actualArguments = @((Get-Content -LiteralPath $argumentStdout -Raw | ConvertFrom-Json))
        if ($actualArguments.Count -ne $expectedArguments.Count) {
            throw "Argument round-trip count mismatch: expected $($expectedArguments.Count), actual $($actualArguments.Count)."
        }
        for ($index = 0; $index -lt $expectedArguments.Count; $index += 1) {
            if ([string]$actualArguments[$index] -cne [string]$expectedArguments[$index]) {
                throw "Argument round-trip mismatch at index $index."
            }
        }
    }
    finally {
        Remove-Item -LiteralPath $argumentTestRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
    Write-Host "CogentNexus-OpenClaw argument round-trip self-test: PASS"
    exit 0
}

foreach ($path in @($StdoutPath, $StderrPath, $PoststatePath)) {
    $parent = Split-Path -Parent $path
    if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
}
$result = Invoke-ExactRootProcess -ProcessFilePath $FilePath -ProcessArgumentList $ArgumentList `
    -ProcessStdoutPath $StdoutPath -ProcessStderrPath $StderrPath
$poststate = [ordered]@{
    schemaVersion = 1
    productId = "cogentnexus-openclaw"
    pid = $result.pid
    startedAtUtc = $result.startedAtUtc
    endedAtUtc = $result.endedAtUtc
    durationSeconds = $result.durationSeconds
    observedExitCode = $result.observedExitCode
    stdoutBytes = (Get-Item -LiteralPath $StdoutPath).Length
    stderrBytes = (Get-Item -LiteralPath $StderrPath).Length
    stdoutSha256 = (Get-FileHash -LiteralPath $StdoutPath -Algorithm SHA256).Hash
    stderrSha256 = (Get-FileHash -LiteralPath $StderrPath -Algorithm SHA256).Hash
}
$temporaryPoststate = "$PoststatePath.tmp"
[System.IO.File]::WriteAllText(
    $temporaryPoststate,
    (($poststate | ConvertTo-Json -Depth 4) + "`n"),
    (New-Object System.Text.UTF8Encoding($false))
)
Move-Item -LiteralPath $temporaryPoststate -Destination $PoststatePath -Force
exit ([int]$result.observedExitCode)
