[CmdletBinding()]
param(
    [ValidateSet('ollama','lmstudio')]
    [string]$Provider = 'lmstudio',

    [switch]$RunDestructive,

    [switch]$SerializerSelfTestOnly
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($env:OS -ne 'Windows_NT') {
    throw 'This acceptance harness wrapper is Windows-only.'
}

function New-EvidenceSerializer {
    Add-Type -AssemblyName System.Web.Extensions
    $serializer = New-Object System.Web.Script.Serialization.JavaScriptSerializer
    $serializer.MaxJsonLength = [int]::MaxValue
    $serializer.RecursionLimit = 100
    return $serializer
}

function ConvertTo-EvidencePlainValue {
    param($Value)

    if ($null -eq $Value) { return $null }
    if ($Value -is [string]) { return [string]$Value }
    if ($Value -is [bool]) { return [bool]$Value }
    if ($Value -is [datetime]) { return $Value.ToString('o') }

    $numericTypes = @(
        [byte],[sbyte],[int16],[uint16],[int32],[uint32],
        [int64],[uint64],[single],[double],[decimal]
    )
    foreach ($type in $numericTypes) {
        if ($Value -is $type) { return $Value }
    }

    if ($Value -is [System.Collections.IDictionary]) {
        $map = @{}
        foreach ($key in $Value.Keys) {
            $map[[string]$key] = ConvertTo-EvidencePlainValue $Value[$key]
        }
        return ,$map
    }

    if (($Value -is [System.Collections.IEnumerable]) -and -not ($Value -is [string])) {
        $items = New-Object System.Collections.ArrayList
        foreach ($item in $Value) {
            [void]$items.Add((ConvertTo-EvidencePlainValue $item))
        }
        return ,([object[]]$items.ToArray())
    }

    $properties = @(
        $Value.PSObject.Properties |
            Where-Object { $_.MemberType -in @('NoteProperty','Property','AliasProperty') }
    )
    if ($properties.Count -gt 0) {
        $map = @{}
        foreach ($property in $properties) {
            try {
                $propertyValue = $property.Value
            } catch {
                $propertyValue = '<unavailable>'
            }
            $map[[string]$property.Name] = ConvertTo-EvidencePlainValue $propertyValue
        }
        return ,$map
    }

    return [string]$Value
}

function Invoke-EvidenceSerializerSelfTest {
    $serializer = New-EvidenceSerializer
    $diagnostic = '{"name":"Provider event adapter","details":{"expected":true,"running":true,"pid":1234},"tags":["provider","event"]}' | ConvertFrom-Json
    $smoke = [pscustomobject][ordered]@{
        schemaVersion = 2
        candidateVersion = '0.9.2'
        startedAt = (Get-Date).ToString('o')
        provider = $Provider
        destructiveRequested = [bool]$RunDestructive
        repoRoot = 'smoke'
        openclawConfig = 'smoke'
        steps = (New-Object System.Collections.ArrayList)
        result = 'running'
        openclawBefore = [pscustomobject][ordered]@{
            primaryModel = 'ollama/qwen3.5:9b'
            agentTimeoutSeconds = $null
            stuckSessionAbortMs = $null
            lmstudioTimeoutSeconds = 600
            lmstudioCompat = $diagnostic.details
            cnxPluginPresent = $false
        }
        openclawAfter = $null
        finishedAt = $null
        error = $null
    }
    [void]$smoke.steps.Add([pscustomobject][ordered]@{
        name = 'openclaw-version'
        status = 'PASS'
        at = (Get-Date).ToString('o')
        data = [pscustomobject][ordered]@{
            command = @('openclaw.cmd','--version')
            exitCode = 0
            durationSeconds = 0.01
            stdout = "OpenClaw 2026.7.1-2 (0790d9f)`r`n"
            stderr = ''
            diagnostic = $diagnostic
        }
    })

    $plain = ConvertTo-EvidencePlainValue $smoke
    $json = $serializer.Serialize($plain)
    $doc = $json | ConvertFrom-Json
    if (@($doc.steps).Count -ne 1) {
        throw 'PowerShell 5.1 evidence serializer self-test lost the step array.'
    }
    if ($doc.steps[0].name -ne 'openclaw-version') {
        throw 'PowerShell 5.1 evidence serializer self-test changed the step name.'
    }
    if ($doc.steps[0].data.exitCode -ne 0) {
        throw 'PowerShell 5.1 evidence serializer self-test changed primitive step data.'
    }
    if ($doc.steps[0].data.diagnostic.details.running -ne $true) {
        throw 'PowerShell 5.1 evidence serializer self-test changed nested diagnostic data.'
    }

    Write-Host 'PowerShell 5.1 evidence serializer self-test: PASS'
}

Invoke-EvidenceSerializerSelfTest
if ($SerializerSelfTestOnly) {
    exit 0
}

$Source = Join-Path $PSScriptRoot 'accept-v092-windows.ps1'
if (-not (Test-Path $Source)) {
    throw "Acceptance harness not found: $Source"
}

# Patch the acceptance harness in a temporary sibling file. Keeping the
# temporary file beside the source preserves the original harness
# $PSScriptRoot -> repository-root resolution.
$Original = Get-Content $Source -Raw

$OldEvidence = @'
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
'@
$NewEvidence = @'
$Evidence = [pscustomobject][ordered]@{
    schemaVersion = 2
    candidateVersion = $Version
    startedAt = (Get-Date).ToString('o')
    provider = $Provider
    destructiveRequested = [bool]$RunDestructive
    repoRoot = $RepoRoot
    openclawConfig = $OpenClawConfig
    steps = (New-Object System.Collections.ArrayList)
    result = 'running'
    openclawBefore = $null
    openclawAfter = $null
    finishedAt = $null
    error = $null
}
'@

$OldSave = @'
function Save-Evidence {
    $Evidence | ConvertTo-Json -Depth 40 | Set-Content -Path $JsonPath -Encoding UTF8
}
'@
$NewSave = @'
function New-EvidenceSerializer {
    Add-Type -AssemblyName System.Web.Extensions
    $serializer = New-Object System.Web.Script.Serialization.JavaScriptSerializer
    $serializer.MaxJsonLength = [int]::MaxValue
    $serializer.RecursionLimit = 100
    return $serializer
}

function ConvertTo-EvidencePlainValue {
    param($Value)
    if ($null -eq $Value) { return $null }
    if ($Value -is [string]) { return [string]$Value }
    if ($Value -is [bool]) { return [bool]$Value }
    if ($Value -is [datetime]) { return $Value.ToString('o') }

    $numericTypes = @(
        [byte],[sbyte],[int16],[uint16],[int32],[uint32],
        [int64],[uint64],[single],[double],[decimal]
    )
    foreach ($type in $numericTypes) {
        if ($Value -is $type) { return $Value }
    }

    if ($Value -is [System.Collections.IDictionary]) {
        $map = @{}
        foreach ($key in $Value.Keys) {
            $map[[string]$key] = ConvertTo-EvidencePlainValue $Value[$key]
        }
        return ,$map
    }

    if (($Value -is [System.Collections.IEnumerable]) -and -not ($Value -is [string])) {
        $items = New-Object System.Collections.ArrayList
        foreach ($item in $Value) {
            [void]$items.Add((ConvertTo-EvidencePlainValue $item))
        }
        return ,([object[]]$items.ToArray())
    }

    $properties = @(
        $Value.PSObject.Properties |
            Where-Object { $_.MemberType -in @('NoteProperty','Property','AliasProperty') }
    )
    if ($properties.Count -gt 0) {
        $map = @{}
        foreach ($property in $properties) {
            try { $propertyValue = $property.Value } catch { $propertyValue = '<unavailable>' }
            $map[[string]$property.Name] = ConvertTo-EvidencePlainValue $propertyValue
        }
        return ,$map
    }

    return [string]$Value
}

$EvidenceJsonSerializer = New-EvidenceSerializer

function Save-Evidence {
    $plain = ConvertTo-EvidencePlainValue $Evidence
    $json = $EvidenceJsonSerializer.Serialize($plain)
    Set-Content -Path $JsonPath -Value $json -Encoding UTF8
}
'@

$OldStep = @'
    $Evidence.steps += [ordered]@{
        name = $Name
        status = $Status
        at = (Get-Date).ToString('o')
        data = $Data
    }
    Save-Evidence
'@
$NewStep = @'
    $step = [pscustomobject][ordered]@{
        name = $Name
        status = $Status
        at = (Get-Date).ToString('o')
        data = [pscustomobject]$Data
    }
    [void]$Evidence.steps.Add($step)
    Save-Evidence
'@

$OldComparable = @'
function ConvertTo-ComparableJson {
    param($Value)
    if ($null -eq $Value) { return '<null>' }
    return ($Value | ConvertTo-Json -Depth 30 -Compress)
}
'@
$NewComparable = @'
function ConvertTo-ComparableJson {
    param($Value)
    if ($null -eq $Value) { return '<null>' }
    return $EvidenceJsonSerializer.Serialize((ConvertTo-EvidencePlainValue $Value))
}
'@

foreach ($pair in @(
    @($OldEvidence, $NewEvidence),
    @($OldSave, $NewSave),
    @($OldStep, $NewStep),
    @($OldComparable, $NewComparable)
)) {
    if (-not $Original.Contains($pair[0])) {
        throw 'Expected PowerShell 5.1 serialization patch block was not found; refusing an unverified patch.'
    }
    $Original = $Original.Replace($pair[0], $pair[1])
}

$OldReturn = '    return [ordered]@{'
$NewReturn = '    return [pscustomobject][ordered]@{'
if (-not $Original.Contains($OldReturn)) {
    throw 'Expected Read-OpenClawFields return block was not found; refusing an unverified patch.'
}
$Patched = $Original.Replace($OldReturn, $NewReturn)

$Temp = Join-Path $PSScriptRoot (".accept-v092-ps51-{0}.tmp.ps1" -f ([guid]::NewGuid().ToString('N')))
try {
    Set-Content -Path $Temp -Value $Patched -Encoding UTF8

    $tokens = $null
    $errors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile(
        $Temp,
        [ref]$tokens,
        [ref]$errors
    )
    if ($errors.Count) {
        $errors | ForEach-Object { Write-Error "Patched acceptance harness :: $_" }
        throw 'Patched acceptance harness failed PowerShell syntax validation.'
    }

    $Arguments = @(
        '-NoProfile',
        '-ExecutionPolicy','Bypass',
        '-File',$Temp,
        '-Provider',$Provider
    )
    if ($RunDestructive) {
        $Arguments += '-RunDestructive'
    }

    & powershell.exe @Arguments
    $Code = $LASTEXITCODE
    if ($null -eq $Code) { $Code = 1 }
    exit [int]$Code
}
finally {
    Remove-Item $Temp -Force -ErrorAction SilentlyContinue
}
