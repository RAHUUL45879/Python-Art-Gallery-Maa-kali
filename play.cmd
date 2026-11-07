@echo off
rem Windows Command Prompt / PowerShell launcher (Python must be on PATH).
python "%~dp0play.py" %*
exit /b %ERRORLEVEL%
