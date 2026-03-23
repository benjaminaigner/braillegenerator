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
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Checking dependencies...
echo.

REM Check if Flask is installed, if not install it
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Error: Failed to install requirements
        echo Try running: pip install Flask Flask-CORS
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
) else (
    echo Dependencies found.
)

echo.
echo Starting Braille Generator server...
echo.
echo =====================================
echo Server will be available at:
echo   http://localhost:5000
echo =====================================
echo.
echo Press CTRL+C to stop the server
echo.

python server.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start server
    echo Check that:
    echo   - index.html exists in this folder
    echo   - braille.jscad exists in this folder
    echo   - Port 5000 is not already in use
    pause
)
