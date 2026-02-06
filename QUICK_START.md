# Quick Start Guide

## ⭐ Recommended Method

```bash
cd /Users/alainairom/Devs/vectordb-vs-sqldb
./scripts/run.sh
```

The console will display:
```
🌐 OPEN THIS URL IN YOUR BROWSER:
   ┌─────────────────────────────────────┐
   │  http://localhost:8080              │
   └─────────────────────────────────────┘
```

Then open: **http://localhost:8080**

## Stop the Application

Press `Ctrl+C` in the terminal

## Usage

1. Click "Initialize Databases" button
2. Wait for data to load (first time may take 1-2 minutes to download ML model)
3. Try searching with example queries:
   - "comfortable seating"
   - "exercise equipment"
   - "kitchen appliances"
   - "work from home"

## To Stop

Press `Ctrl+C` in the terminal where the app is running

## Troubleshooting

### If port 8080 is in use:
```bash
lsof -ti:8080 | xargs kill -9
```

### If dependencies are missing:
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