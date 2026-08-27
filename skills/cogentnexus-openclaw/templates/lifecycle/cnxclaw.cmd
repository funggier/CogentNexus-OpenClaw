@echo off
setlocal
python "%~dp0..\..\scripts\cnxclaw.py" --root "%~dp0..\..\..\..\.cogentnexus-openclaw" %*
exit /b %ERRORLEVEL%
