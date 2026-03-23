@echo off
REM Braille Plate Generator - Start Server
REM This script starts the Flask development server

echo.
echo =====================================
echo   Braille Plate Generator Server
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install requirements
        pause
        exit /b 1
    )
)

echo Starting Braille Generator server...
echo.
echo Server will be available at: http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo.

python server.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start server
    pause
)
