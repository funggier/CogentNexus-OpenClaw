[CmdletBinding()]
param(
    [ValidateSet('ollama','lmstudio')]
    [string]$Provider = 'lmstudio',

    [switch]$RunDestructive
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if ($env:OS -ne 'Windows_NT') {
    throw 'This acceptance harness wrapper is Windows-only.'
}

$Source = Join-Path $PSScriptRoot 'accept-v092-windows.ps1'
if (-not (Test-Path $Source)) {
    throw "Acceptance harness not found: $Source"
}

# Windows PowerShell 5.1 enumerates OrderedDictionary on += in this context.
# Patch the acceptance harness in a temporary sibling file so each evidence
# step is appended as one PSCustomObject and ConvertTo-Json receives a stable
# object graph. Keeping the temporary file beside the source also preserves
# the original harness $PSScriptRoot -> repository-root resolution.
$Original = Get-Content $Source -Raw
$Old = @'
    $Evidence.steps += [ordered]@{
        name = $Name
        status = $Status
        at = (Get-Date).ToString('o')
        data = $Data
    }
    Save-Evidence
'@
$New = @'
    $step = [pscustomobject][ordered]@{
        name = $Name
        status = $Status
        at = (Get-Date).ToString('o')
        data = $Data
    }
    $Evidence.steps = @($Evidence.steps) + @($step)
    Save-Evidence
'@

if (-not $Original.Contains($Old)) {
    throw 'Expected Add-Step serialization block was not found; refusing an unverified patch.'
}

$Patched = $Original.Replace($Old, $New)
if ($Patched -eq $Original) {
    throw 'Acceptance harness patch produced no change.'
}

$Temp = Join-Path $PSScriptRoot (".accept-v092-ps51-{0}.tmp.ps1" -f ([guid]::NewGuid().ToString('N')))
try {
    Set-Content -Path $Temp -Value $Patched -Encoding UTF8

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
