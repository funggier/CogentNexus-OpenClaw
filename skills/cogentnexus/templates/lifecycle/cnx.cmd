@echo off
setlocal
python "%~dp0..\..\scripts\host.py" --root "%~dp0..\..\..\..\.cogent" %*
exit /b %ERRORLEVEL%
