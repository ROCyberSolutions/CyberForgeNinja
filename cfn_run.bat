@echo off
:: Enhanced CyberForge Ninja Launcher with error checking

setlocal
set VENV_PATH=Your path to venv 
set PYTHON_PATH=%VENV_PATH%\Scripts\python.exe
set SCRIPT_PATH=Your path to CyberForge\cfn.py

:: Check if files exist
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found in virtual environment
    echo Expected at: %PYTHON_PATH%
    pause
    exit /b 1
)

if not exist "%SCRIPT_PATH%" (
    echo Error: CyberForge script not found
    echo Expected at: %SCRIPT_PATH%
    pause
    exit /b 1
)

:: Run with virtual environment
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

echo Launching CyberForge Ninja...
"%PYTHON_PATH%" "%SCRIPT_PATH%"

pause
