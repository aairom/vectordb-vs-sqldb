#!/bin/bash

# Unified Launch Script for Vector DB vs SQL DB Comparison
# This script handles all setup and launches the application

set -e

echo ""
echo "======================================================================"
echo "🚀 Vector DB vs SQL DB Comparison - Unified Launcher"
echo "======================================================================"
echo ""

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs
echo "✅ Directories ready"
echo ""

# Kill any existing processes on port 8080
echo "🔍 Checking for existing processes on port 8080..."
if lsof -ti:8080 > /dev/null 2>&1; then
    echo "⚠️  Stopping existing process on port 8080..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    sleep 2
fi
echo "✅ Port 8080 is available"
echo ""

echo "======================================================================"
echo "🌐 Starting Application Server"
echo "======================================================================"
echo ""

# Start the backend server
cd backend
python3 app.py

# Note: The script will stay in foreground and show all output
# Press Ctrl+C to stop the server

# Made with Bob
