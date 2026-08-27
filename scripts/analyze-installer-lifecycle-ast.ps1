[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$Installer)

$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($Installer, [ref]$tokens, [ref]$errors)
if ($errors.Count -gt 0) { throw "PowerShell parse failed: $($errors[0].Message)" }

function Get-IfAncestors($node) {
    $result = @()
    while ($null -ne $node) {
        if ($node -is [System.Management.Automation.Language.IfStatementAst]) {
            $result += $node.Extent.Text
        }
        $node = $node.Parent
    }
    return @($result)
}

$commands = $ast.FindAll({ param($node)
    if ($node -isnot [System.Management.Automation.Language.CommandAst]) { return $false }
    $text = $node.Extent.Text
    return ($text -match 'rollover-plan|rollover-apply|resolve-plugin|npm pack|plugins install|plugins disable')
}, $true)

$rows = foreach ($command in $commands) {
    [ordered]@{
        command = $command.Extent.Text
        start = [int]$command.Extent.StartOffset
        ancestors = @(Get-IfAncestors $command)
    }
}
$rows | ConvertTo-Json -Depth 8 -Compress
