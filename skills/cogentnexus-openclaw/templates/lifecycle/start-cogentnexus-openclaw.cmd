@echo off
setlocal
set "SKILL_ROOT=%~dp0..\.."
for %%I in ("%SKILL_ROOT%") do set "SKILL_ROOT=%%~fI"
set "RUNTIME=%SKILL_ROOT%\scripts\runtime.py"
if defined COGENTNEXUS_OPENCLAW_ROOT (set "RUNTIME_ROOT=%COGENTNEXUS_OPENCLAW_ROOT%") else (set "RUNTIME_ROOT=%CD%\.cogentnexus-openclaw")
where python.exe >nul 2>&1 || (echo ERROR: python.exe was not found in PATH.& exit /b 9009)
python.exe "%RUNTIME%" --root "%RUNTIME_ROOT%" lifecycle start --provider
exit /b %ERRORLEVEL%
