@echo off
setlocal
python "%~dp0..\..\scripts\cnx.py" --root "%~dp0..\..\..\..\.cogent" %*
exit /b %ERRORLEVEL%
