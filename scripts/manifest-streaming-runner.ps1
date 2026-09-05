[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$LaunchManifest,
  [Parameter(Mandatory=$true)][string]$EvidenceRoot
)
$ErrorActionPreference='Stop'
$started=Get-Date
New-Item -ItemType Directory -Force -Path $EvidenceRoot | Out-Null
$startedPath=Join-Path $EvidenceRoot 'runner-started.json'
$childStartedPath=Join-Path $EvidenceRoot 'child-started.json'
$resultPath=Join-Path $EvidenceRoot 'runner-result.json'
$stdoutPath=Join-Path $EvidenceRoot 'child-stdout.txt'
$stderrPath=Join-Path $EvidenceRoot 'child-stderr.txt'
$transcriptPath=Join-Path $EvidenceRoot 'runner-transcript.txt'
$fallbackPath=Join-Path $EvidenceRoot 'runner-fallback.log'
$exitCode=1; $outcome='runner_exception'; $childStarted=$false; $transcriptOk=$false; $fallbackOk=$false
$Utf8NoBom=New-Object System.Text.UTF8Encoding($false)
function Append-Line([string]$path,[string]$line){[IO.File]::AppendAllText($path,$line+[Environment]::NewLine,[Text.Encoding]::UTF8)}
function Quote-WindowsArg([string]$value){
  if($value -notmatch '[\s"]'){ return $value }
  $sb=New-Object Text.StringBuilder; [void]$sb.Append('"'); $slashes=0
  foreach($ch in $value.ToCharArray()){
    if($ch -eq '\'){ $slashes++; continue }
    if($ch -eq '"'){ [void]$sb.Append(('\' * ($slashes*2 + 1))); [void]$sb.Append('"'); $slashes=0; continue }
    if($slashes){ [void]$sb.Append(('\' * $slashes)); $slashes=0 }; [void]$sb.Append($ch)
  }
  if($slashes){ [void]$sb.Append(('\' * ($slashes*2))) }; [void]$sb.Append('"'); $sb.ToString()
}
try {
  [IO.File]::WriteAllBytes($stdoutPath,[byte[]]@()); [IO.File]::WriteAllBytes($stderrPath,[byte[]]@())
  $manifestBytes=[IO.File]::ReadAllBytes($LaunchManifest);$manifestSha=([Security.Cryptography.SHA256]::Create().ComputeHash($manifestBytes)|ForEach-Object ToString x2)-join ''
  $runnerBytes=[IO.File]::ReadAllBytes($PSCommandPath);$runnerSha=([Security.Cryptography.SHA256]::Create().ComputeHash($runnerBytes)|ForEach-Object ToString x2)-join ''
  $m=Get-Content -Raw -LiteralPath $LaunchManifest|ConvertFrom-Json
  $child=[string]$m.childExecutable;$args=@($m.childArguments);$wd=[string]$m.workingDirectory
  $startRecord=[ordered]@{schema='cnx254.runner-started.v2';runnerPath=$PSCommandPath;launchManifest=$LaunchManifest;manifestSha256=$manifestSha;runnerSha256=$runnerSha;childExecutable=$child;childArguments=$args;workingDirectory=$wd;identity=[Security.Principal.WindowsIdentity]::GetCurrent().Name;pid=$PID;startedUtc=$started.ToUniversalTime().ToString('o');stdoutPath=$stdoutPath;stderrPath=$stderrPath;resultPath=$resultPath;transport='dotnet-process-direct'}
  [IO.File]::WriteAllText($startedPath,($startRecord|ConvertTo-Json -Depth 8),$Utf8NoBom)
  $psi=New-Object System.Diagnostics.ProcessStartInfo;$psi.FileName=$child;$psi.Arguments=(($args|ForEach-Object{Quote-WindowsArg ([string]$_)}) -join ' ');$psi.UseShellExecute=$false;$psi.CreateNoWindow=$true;$psi.WorkingDirectory=$wd;$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
  $proc=New-Object System.Diagnostics.Process;$proc.StartInfo=$psi
  if(-not ('CnxStreamingSink' -as [type])){
    Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Text;
using System.Diagnostics;
public static class CnxStreamingSink {
  public static void Attach(Process p, string output, string error) {
    p.OutputDataReceived += (s,e) => { if(e.Data != null) File.AppendAllText(output, e.Data + Environment.NewLine, new UTF8Encoding(false)); };
    p.ErrorDataReceived += (s,e) => { if(e.Data != null) File.AppendAllText(error, e.Data + Environment.NewLine, new UTF8Encoding(false)); };
  }
}
'@
  }
  [CnxStreamingSink]::Attach($proc,$stdoutPath,$stderrPath)
  if(-not $proc.Start()){throw 'Process.Start returned false'}
  $childStarted=$true; $proc.BeginOutputReadLine(); $proc.BeginErrorReadLine()
  $childRecord=[ordered]@{schema='cnx254.child-started.v2';startedUtc=(Get-Date).ToUniversalTime().ToString('o');pid=$proc.Id;executable=$child;manifestSha256=$manifestSha;runnerSha256=$runnerSha;transport='dotnet-process-direct'}
  [IO.File]::WriteAllText($childStartedPath,($childRecord|ConvertTo-Json -Depth 8),$Utf8NoBom)
  while(-not $proc.HasExited){Start-Sleep -Milliseconds 100}
  $proc.WaitForExit();Start-Sleep -Milliseconds 200;$proc.Refresh();$exitCode=$proc.ExitCode;$outcome='child_nonzero_exit';if($exitCode -eq 0){$outcome='child_success'}
  $transcript="stdout:`n$([IO.File]::ReadAllText($stdoutPath))`nstderr:`n$([IO.File]::ReadAllText($stderrPath))`nexitCode=$exitCode`n";[IO.File]::WriteAllText($transcriptPath,$transcript,[Text.Encoding]::UTF8);$transcriptOk=$true
} catch {
  $exceptionType=$_.Exception.GetType().FullName;$exceptionMessage=$_.Exception.Message
  if($childStarted){$outcome='child_execution_exception'}else{$outcome='child_launch_exception'}
  try{Append-Line $fallbackPath ("outcome=$outcome`nexceptionType=$exceptionType`nexceptionMessage=$exceptionMessage");$fallbackOk=$true}catch{}
} finally {
  try {$reportedExitCode=$null;if($childStarted){$reportedExitCode=[int]$exitCode};$r=[ordered]@{schema='cnx254.runner-result.v2';startedUtc=$started.ToUniversalTime().ToString('o');endedUtc=(Get-Date).ToUniversalTime().ToString('o');outcome=$outcome;childStarted=$childStarted;childExitCode=$reportedExitCode;exceptionType=$exceptionType;exceptionMessage=$exceptionMessage;runnerStartedPath=$startedPath;childStartedPath=$childStartedPath;stdoutPath=$stdoutPath;stderrPath=$stderrPath;transcriptPath=$transcriptPath;fallbackPath=$fallbackPath;manifestSha256=$manifestSha;runnerSha256=$runnerSha;transcriptWriteSucceeded=$transcriptOk;fallbackWriteSucceeded=$fallbackOk};[IO.File]::WriteAllText($resultPath,($r|ConvertTo-Json -Depth 8),$Utf8NoBom)} catch {try{Append-Line $fallbackPath ("finally-write-exception=$($_.Exception.Message)")}catch{}}
}
exit([int]$exitCode)
