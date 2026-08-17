@echo off
setlocal
python "%~dp0..\..\scripts\host_control_v091.py" --root "%~dp0..\..\..\..\.cogent" %*
exit /b %ERRORLEVEL%
