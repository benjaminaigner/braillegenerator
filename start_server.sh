#!/bin/bash

# Braille Plate Generator - Start Server
# This script starts the Flask development server

echo ""
echo "====================================="
echo "  Braille Plate Generator Server"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org"
    exit 1
fi

# Check if requirements are installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install requirements"
        exit 1
    fi
fi

echo "Starting Braille Generator server..."
echo ""
echo "Server will be available at: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python3 server.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Failed to start server"
    exit 1
fi
