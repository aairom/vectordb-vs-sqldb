#!/bin/bash

# Stop script for Vector DB vs SQL DB Comparison Application
# This script stops the backend server

set -e

echo "=========================================="
echo "Vector DB vs SQL DB Comparison"
echo "Stopping Application..."
echo "=========================================="

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Check if PID file exists
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    
    # Check if process is running
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        
        # Wait for process to stop
        sleep 2
        
        # Force kill if still running
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            echo "Force stopping backend server..."
            kill -9 $BACKEND_PID
        fi
        
        echo "Backend server stopped"
    else
        echo "Backend server is not running (PID: $BACKEND_PID)"
    fi
    
    # Remove PID file
    rm .backend.pid
else
    echo "No PID file found"
fi

# Kill any remaining processes on port 8080
echo "Checking for any remaining processes on port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Deactivate virtual environment if active
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate 2>/dev/null || true
fi

echo ""
echo "=========================================="
echo "Application stopped successfully!"
echo "=========================================="

# Made with Bob
