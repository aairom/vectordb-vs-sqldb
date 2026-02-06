#!/bin/bash

# Start script for Vector DB vs SQL DB Comparison Application
# This script launches both the backend API and opens the frontend in a browser

set -e

echo "=========================================="
echo "Vector DB vs SQL DB Comparison"
echo "Starting Application..."
echo "=========================================="

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create data directory if it doesn't exist
mkdir -p data

# Kill any existing Flask processes on port 8080
echo "Checking for existing processes on port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

echo ""
echo "============================================================"
echo "🚀 Vector DB vs SQL DB Comparison"
echo "============================================================"
echo "Starting application server..."

# Start the backend server in the background
cd backend
python3 app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Save PID to file for stop script
echo $BACKEND_PID > .backend.pid

# Wait for backend to start
echo "Waiting for server to start..."
sleep 5

# Check if backend is running
if ! curl -s http://localhost:8080/api/health > /dev/null; then
    echo "❌ Error: Server failed to start"
    echo "Check logs/backend.log for details:"
    cat logs/backend.log
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Server started successfully (PID: $BACKEND_PID)"
echo ""
echo "============================================================"
echo "🌐 APPLICATION URL:"
echo "   http://localhost:8080"
echo "============================================================"
echo ""
echo "📡 API Endpoints:"
echo "   • Health Check: http://localhost:8080/api/health"
echo "   • Initialize:   http://localhost:8080/api/initialize"
echo "   • Search:       http://localhost:8080/api/search/compare"
echo "   • Statistics:   http://localhost:8080/api/stats"
echo ""
echo "📝 Quick Start:"
echo "   1. Open http://localhost:8080 in your browser"
echo "   2. Click 'Initialize Databases' button"
echo "   3. Try example searches like 'comfortable seating'"
echo ""
echo "🛑 To stop: ./scripts/stop.sh"
echo "📋 Logs: logs/backend.log"
echo "============================================================"

# Open application in default browser
APP_URL="http://localhost:8080"
echo ""
echo "Opening http://localhost:8080 in your browser..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$APP_URL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$APP_URL" 2>/dev/null || sensible-browser "$APP_URL" 2>/dev/null
else
    echo "Please manually open $APP_URL in your browser"
fi

echo ""

# Made with Bob
