@echo off
:: System Cleaner Launcher - Requests Admin privileges
:: This batch file will run the Python cleaner script as Administrator

cd /d "%~dp0"

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Run the Python cleaner script
echo Running System Cleaner...
python "%~dp0system_cleaner.py"

pause
