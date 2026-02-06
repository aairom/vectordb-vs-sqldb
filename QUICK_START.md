# Quick Start Guide

Get up and running with a single command!

## Prerequisites

- Python 3.8 or higher (the script will check for you)
- Modern web browser

## Step 1: Navigate to Project Directory

```bash
cd /Users/alainairom/Devs/vectordb-vs-sqldb
```

## Step 2: Run the Unified Launcher

```bash
./scripts/launch.sh
```

**That's it!** The unified launcher automatically handles:
- ✅ Python version check
- ✅ Virtual environment creation (if needed)
- ✅ Dependency installation
- ✅ Directory creation (data/, logs/)
- ✅ Port conflict resolution (kills processes on port 8080)
- ✅ Server startup

The console will display:
```
🌐 OPEN THIS URL IN YOUR BROWSER:
   ┌─────────────────────────────────────┐
   │  http://localhost:8080              │
   └─────────────────────────────────────┘
```

Then open: **http://localhost:8080**

## Stop the Application

Press `Ctrl+C` in the terminal where the app is running

Or use the stop script:
```bash
./scripts/stop.sh
```

## Usage

1. Click "Initialize Databases" button
2. Wait for data to load (first time may take 1-2 minutes to download ML model)
3. Try searching with example queries:
   - "comfortable seating"
   - "exercise equipment"
   - "kitchen appliances"
   - "work from home"

## Troubleshooting

### If port 8080 is in use:
The launcher automatically clears port 8080, but if needed:
```bash
lsof -ti:8080 | xargs kill -9
```

### If you need to reinstall dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### First Run Takes Longer
The first time you run the app, it downloads the ML model (~80MB).
This only happens once and is cached for future runs.

## What You'll See

- **Traditional SQL**: Exact keyword matching, fast but limited
- **Vector Database**: Semantic search, understands context and meaning
- **Side-by-side comparison**: See the differences in real-time
- **Performance metrics**: Execution times for each search method

Enjoy exploring the differences between traditional SQL and vector databases!