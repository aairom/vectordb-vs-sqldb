#!/bin/bash

# Simple run script for Vector DB vs SQL DB Comparison
# This script starts the application and displays the URL

echo ""
echo "======================================================================"
echo "🚀 Starting Vector DB vs SQL DB Comparison Application"
echo "======================================================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Create data directory
mkdir -p data logs

# Kill any existing process on port 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

echo "Starting server..."
echo ""

# Start the application
cd backend
python3 app.py

# Made with Bob
