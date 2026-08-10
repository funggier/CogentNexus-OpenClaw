@echo off
setlocal
set "SKILL_ROOT=%~dp0..\.."
for %%I in ("%SKILL_ROOT%") do set "SKILL_ROOT=%%~fI"
set "PHASE3=%SKILL_ROOT%\scripts\phase3.py"
if defined COGENTNEXUS_ROOT (set "RUNTIME_ROOT=%COGENTNEXUS_ROOT%") else (set "RUNTIME_ROOT=%CD%\.cogent")
where python.exe >nul 2>&1 || (echo ERROR: python.exe was not found in PATH.& exit /b 9009)
python.exe "%PHASE3%" --root "%RUNTIME_ROOT%" lifecycle start --provider
exit /b %ERRORLEVEL%
