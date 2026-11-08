@echo off
rem Starts the agent team's page and opens it in your browser. Keep this window open; close it to stop the page.
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (python page.py) else (py page.py)
pause
