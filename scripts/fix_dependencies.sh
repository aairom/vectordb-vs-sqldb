#!/bin/bash

# Fix Dependencies Script
# This script resolves common dependency issues

set -e

echo "=========================================="
echo "Fixing Dependencies"
echo "=========================================="

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Stop any running instances
echo "Stopping any running instances..."
./scripts/stop.sh 2>/dev/null || true

# Remove existing virtual environment
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create fresh virtual environment
echo "Creating fresh virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Dependencies fixed successfully!"
echo "=========================================="
echo ""
echo "Now run: ./scripts/start.sh"

# Made with Bob
