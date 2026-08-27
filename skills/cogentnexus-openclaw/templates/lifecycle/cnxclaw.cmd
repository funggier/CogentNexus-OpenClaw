@echo off
setlocal
python "%~dp0..\..\scripts\cnxclaw_v093.py" --root "%~dp0..\..\..\..\.cogentnexus-openclaw" %*
exit /b %ERRORLEVEL%
