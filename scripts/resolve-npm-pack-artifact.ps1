[CmdletBinding()]
param()

function Resolve-NpmPackArtifact {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$PackJson,
        [Parameter(Mandatory = $true)][string]$PluginDir
    )

    try {
        $packed = $PackJson | ConvertFrom-Json
    }
    catch {
        throw "npm pack returned invalid JSON: $($_.Exception.Message)"
    }

    if ($null -eq $packed) {
        throw "npm pack returned an empty JSON value"
    }

    if ($packed -is [array]) {
        $items = @($packed)
        $shape = "array"
    }
    elseif ($packed -is [pscustomobject]) {
        $properties = @($packed.PSObject.Properties)
        if ($properties.Count -ne 1) {
            throw "npm pack returned $($properties.Count) keyed package entries; expected exactly one"
        }
        $items = @($properties[0].Value)
        $shape = "keyed-object"
    }
    else {
        throw "npm pack returned unsupported JSON shape: $($packed.GetType().Name)"
    }

    if ($items.Count -ne 1) {
        throw "npm pack returned $($items.Count) package artifacts from $shape; expected exactly one"
    }

    $filename = $items[0].filename
    if ($filename -isnot [string] -or [string]::IsNullOrWhiteSpace($filename)) {
        throw "npm pack artifact has no non-empty filename"
    }
    $filename = $filename.Trim()
    if ([IO.Path]::IsPathRooted($filename) -or $filename -match '[\\/]' -or $filename -match '(^|\.\.)\.\.' -or $filename -notmatch '^[^:*?"<>|]+\.tgz$') {
        throw "npm pack artifact filename is unsafe: $filename"
    }

    $root = [IO.Path]::GetFullPath($PluginDir).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $candidate = [IO.Path]::GetFullPath((Join-Path $root $filename))
    $prefix = $root + [IO.Path]::DirectorySeparatorChar
    if (-not $candidate.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "npm pack artifact escapes plugin directory: $filename"
    }
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        throw "npm pack artifact does not exist: $candidate"
    }

    [pscustomobject]@{ filename = $filename; path = $candidate }
}
