[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidateSet('fresh','legacy','upgrade')][string]$Mode,
    [switch]$PendingRollover,
    [switch]$PluginAlreadyExact,
    [switch]$SkipPlugin
)

if ($PendingRollover -and $PluginAlreadyExact) {
    throw 'pendingRollover and pluginAlreadyExact cannot both be true'
}
$installPlugin = $false
$rolloverPlugin = $false
if (-not $SkipPlugin) {
    if ($Mode -in @('fresh','legacy')) { $installPlugin = $true }
    elseif ($Mode -eq 'upgrade') {
        if ($PendingRollover) { $rolloverPlugin = $true }
        elseif (-not $PluginAlreadyExact) { $installPlugin = $true; $rolloverPlugin = $true }
    }
}
[ordered]@{
    mode=$Mode
    pendingRollover=[bool]$PendingRollover
    pluginAlreadyExact=[bool]$PluginAlreadyExact
    skipPlugin=[bool]$SkipPlugin
    installPlugin=$installPlugin
    rolloverPlugin=$rolloverPlugin
} | ConvertTo-Json -Compress
