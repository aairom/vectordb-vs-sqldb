#!/bin/bash

# GitHub Push Automation Script
# Usage: ./scripts/push_to_github.sh [repository-url]
# Example: ./scripts/push_to_github.sh https://github.com/username/vectordb-vs-sqldb.git

set -e

echo ""
echo "======================================================================"
echo "🚀 GitHub Push Automation"
echo "======================================================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed"
    echo "Please install git first: https://git-scm.com/downloads"
    exit 1
fi

# Check if this is a git repository
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .gitignore
    git commit -m "Initial commit: Add .gitignore"
    echo "✅ Git repository initialized"
    echo ""
fi

# Check if remote is configured
if ! git remote get-url origin &> /dev/null; then
    # Check if URL was provided as argument
    if [ -n "$1" ]; then
        REPO_URL="$1"
    else
        echo "======================================================================"
        echo "📝 GitHub Repository Setup"
        echo "======================================================================"
        echo ""
        echo "Usage: ./scripts/push_to_github.sh <repository-url>"
        echo ""
        echo "Examples:"
        echo "  ./scripts/push_to_github.sh https://github.com/username/vectordb-vs-sqldb.git"
        echo "  ./scripts/push_to_github.sh git@github.com:username/vectordb-vs-sqldb.git"
        echo ""
        read -p "Enter repository URL: " REPO_URL
    fi
    
    # Validate URL is not empty
    if [ -z "$REPO_URL" ]; then
        echo "❌ Error: Repository URL cannot be empty"
        exit 1
    fi
    
    # Add remote
    echo ""
    echo "🔗 Adding remote repository..."
    git remote add origin "$REPO_URL"
    echo "✅ Remote repository configured: $REPO_URL"
    echo ""
fi

# Show current status
echo "Current git status:"
git status --short
echo ""

# Check if there are changes to commit
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit"
    exit 0
fi

# Get commit message from user
echo "Enter commit message (or press Enter for default message):"
read -r COMMIT_MESSAGE

if [ -z "$COMMIT_MESSAGE" ]; then
    COMMIT_MESSAGE="Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Add all changes
echo "Adding all changes..."
git add .

# Show what will be committed
echo ""
echo "Files to be committed:"
git --no-pager diff --cached --name-status
echo ""

# Confirm before committing
read -p "Proceed with commit and push? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted"
    exit 0
fi

# Commit changes
echo "Committing changes..."
git commit -m "$COMMIT_MESSAGE"

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Push to remote
echo "Pushing to origin/$CURRENT_BRANCH..."
git push origin "$CURRENT_BRANCH"

echo ""
echo "=========================================="
echo "Successfully pushed to GitHub!"
echo "Branch: $CURRENT_BRANCH"
echo "Commit: $COMMIT_MESSAGE"
echo "=========================================="

# Made with Bob
