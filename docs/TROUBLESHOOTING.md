# Troubleshooting Guide

This guide helps resolve common issues when running the Vector DB vs SQL DB Comparison application.

## Quick Fix: Dependency Issues

If you see "Failed to fetch" or import errors, run:

```bash
./scripts/fix_dependencies.sh
```

This will:
1. Stop any running instances
2. Remove the old virtual environment
3. Create a fresh virtual environment
4. Install all dependencies with correct versions

Then restart the application:
```bash
./scripts/start.sh
```

## Common Issues

### 1. "Failed to fetch" Error

**Symptom:** Frontend shows "Failed to initialize databases: Failed to fetch"

**Cause:** Backend server failed to start due to dependency issues

**Solution:**
```bash
# Check backend logs
cat logs/backend.log

# Fix dependencies
./scripts/fix_dependencies.sh

# Restart
./scripts/start.sh
```

### 2. Import Error: sentence_transformers

**Error Message:**
```
ImportError: cannot import name 'cached_download' from 'huggingface_hub'
```

**Cause:** Version incompatibility between sentence-transformers and huggingface-hub

**Solution:**
```bash
./scripts/fix_dependencies.sh
```

### 3. Port 5000 Already in Use

**Error Message:**
```
Address already in use
```

**Solution:**
```bash
# Stop existing processes
./scripts/stop.sh

# Or manually kill the process
lsof -ti:5000 | xargs kill -9

# Restart
./scripts/start.sh
```

### 4. Backend Won't Start

**Symptoms:**
- Browser opens but shows connection error
- No response from http://localhost:5000

**Diagnosis:**
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Check logs
cat logs/backend.log

# Check if port is in use
lsof -i :5000
```

**Solution:**
```bash
# Stop everything
./scripts/stop.sh

# Fix dependencies
./scripts/fix_dependencies.sh

# Start fresh
./scripts/start.sh
```

### 5. Python Version Issues

**Error Message:**
```
Python 3.8 or higher required
```

**Solution:**
```bash
# Check Python version
python3 --version

# If < 3.8, install newer Python
# macOS:
brew install python@3.11

# Linux:
sudo apt update
sudo apt install python3.11
```

### 6. Virtual Environment Issues

**Symptoms:**
- Packages not found
- Wrong Python version in venv

**Solution:**
```bash
# Remove old venv
rm -rf venv

# Create new venv with specific Python
python3.11 -m venv venv

# Activate and install
source venv/bin/activate
pip install -r requirements.txt
```

### 7. CORS Errors in Browser

**Error Message:**
```
Access to fetch at 'http://localhost:5000' has been blocked by CORS policy
```

**Cause:** Opening HTML file directly instead of through the start script

**Solution:**
- Always use `./scripts/start.sh` to launch the application
- Don't open `frontend/index.html` directly in browser

### 8. Database Locked Error

**Error Message:**
```
database is locked
```

**Solution:**
```bash
# Stop all instances
./scripts/stop.sh

# Remove lock files
rm data/*.db-shm data/*.db-wal

# Restart
./scripts/start.sh
```

### 9. Model Download Issues

**Symptoms:**
- Long initialization time
- Timeout errors
- Network errors

**Cause:** First-time download of sentence-transformers model (~80MB)

**Solution:**
- Ensure stable internet connection
- Wait for download to complete (may take 1-5 minutes)
- Model is cached after first download

**Manual download:**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

### 10. Memory Issues

**Symptoms:**
- Application crashes
- Slow performance
- System freezes

**Cause:** Insufficient RAM for ML model

**Solution:**
- Ensure at least 2GB free RAM
- Close other applications
- Use lighter model (edit `backend/vector_db.py`):
```python
self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Smaller model
```

## Verification Steps

After fixing issues, verify everything works:

### 1. Check Backend Health
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "healthy", "message": "API is running"}
```

### 2. Test Frontend Connection
1. Open browser to the frontend
2. Open browser console (F12)
3. Should see no errors
4. Click "Initialize Databases"
5. Should see success notification

### 3. Test Search
1. Click "Initialize Databases"
2. Enter query: "comfortable seating"
3. Click "Compare Search"
4. Should see results in both panels

## Getting Help

If issues persist:

1. **Check Logs:**
   ```bash
   cat logs/backend.log
   ```

2. **Check System Requirements:**
   - Python 3.8+
   - 2GB+ free RAM
   - Internet connection (first run)
   - Port 5000 available

3. **Clean Install:**
   ```bash
   # Complete clean install
   ./scripts/stop.sh
   rm -rf venv data/*.db logs/*.log
   ./scripts/fix_dependencies.sh
   ./scripts/start.sh
   ```

4. **Report Issue:**
   - Include error message
   - Include logs/backend.log
   - Include Python version
   - Include OS version

## Prevention Tips

1. **Always use scripts:**
   - Use `./scripts/start.sh` to start
   - Use `./scripts/stop.sh` to stop
   - Don't run `python app.py` directly

2. **Keep dependencies updated:**
   ```bash
   source venv/bin/activate
   pip install --upgrade -r requirements.txt
   ```

3. **Regular cleanup:**
   ```bash
   # Clean old logs
   rm logs/*.log
   
   # Clean database files
   rm data/*.db
   ```

4. **Monitor resources:**
   - Check available RAM
   - Check disk space
   - Check network connection

## Advanced Troubleshooting

### Debug Mode

Enable debug logging in `backend/app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

**Test Traditional DB:**
```python
from backend.traditional_db import TraditionalDB
db = TraditionalDB(":memory:")
db.insert_product("Test", "Description", "Category", 99.99)
results, time = db.search_exact("test")
print(results)
```

**Test Vector DB:**
```python
from backend.vector_db import VectorDB
db = VectorDB(":memory:")
db.insert_product("Test", "Description", "Category", 99.99)
results, time = db.search_semantic("test")
print(results)
```

### Network Debugging

```bash
# Check if backend is listening
netstat -an | grep 5000

# Test API directly
curl -X POST http://localhost:5000/api/initialize

# Check CORS headers
curl -I http://localhost:5000/api/health
```

## Still Having Issues?

1. Review the [Deployment Guide](DEPLOYMENT.md)
2. Check the [Architecture Documentation](ARCHITECTURE.md)
3. Read the [README](../README.md)
4. Create a GitHub issue with:
   - Error message
   - Steps to reproduce
   - System information
   - Log files

---

**Most Common Solution:** Run `./scripts/fix_dependencies.sh` and restart!