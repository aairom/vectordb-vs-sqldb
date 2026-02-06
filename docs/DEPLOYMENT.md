# Deployment Guide

This document provides comprehensive deployment instructions for the Vector DB vs SQL DB Comparison application.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Production Deployment](#production-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)

## System Requirements

### Minimum Requirements

- **Operating System**: macOS, Linux, or Windows (with WSL)
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB for application and dependencies
- **Network**: Port 5000 must be available

### Software Dependencies

- Python 3.8+
- pip (Python package manager)
- Git (for version control)
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd vectordb-vs-sqldb
```

### 2. Verify Python Installation

```bash
python3 --version
# Should output: Python 3.8.x or higher
```

If Python is not installed:

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows (WSL):**
```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0 (Web framework)
- Flask-CORS 4.0.0 (Cross-Origin Resource Sharing)
- numpy 1.26.2 (Numerical computing)
- sqlite-vec 0.1.1 (Vector database extension)
- sentence-transformers 2.2.2 (Text embeddings)

### 6. Create Required Directories

```bash
mkdir -p data logs
```

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Database Configuration
TRADITIONAL_DB_PATH=data/traditional.db
VECTOR_DB_PATH=data/vector.db

# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Port Configuration

If port 5000 is already in use, modify `backend/app.py`:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Change port here
```

Also update `frontend/app.js`:

```javascript
const API_BASE_URL = 'http://localhost:5001/api';  // Update port
```

## Running the Application

### Development Mode

#### Using Start Script (Recommended)

```bash
./scripts/start.sh
```

This automated script:
1. Creates/activates virtual environment
2. Installs/updates dependencies
3. Creates necessary directories
4. Starts the backend server
5. Opens the frontend in your browser

#### Manual Start

```bash
# Activate virtual environment
source venv/bin/activate

# Start backend
cd backend
python3 app.py &

# Open frontend
open ../frontend/index.html  # macOS
# or
xdg-open ../frontend/index.html  # Linux
```

### Stopping the Application

#### Using Stop Script (Recommended)

```bash
./scripts/stop.sh
```

#### Manual Stop

```bash
# Find the process
lsof -i :5000

# Kill the process
kill <PID>
```

## Production Deployment

### Using Gunicorn (Recommended)

1. **Install Gunicorn**

```bash
pip install gunicorn
```

2. **Create Gunicorn Configuration**

Create `gunicorn_config.py`:

```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
errorlog = "logs/gunicorn_error.log"
accesslog = "logs/gunicorn_access.log"
loglevel = "info"
```

3. **Run with Gunicorn**

```bash
cd backend
gunicorn -c ../gunicorn_config.py app:app
```

### Using Nginx as Reverse Proxy

1. **Install Nginx**

```bash
# macOS
brew install nginx

# Linux
sudo apt install nginx
```

2. **Configure Nginx**

Create `/etc/nginx/sites-available/vectordb-comparison`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/vectordb-vs-sqldb/frontend;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **Enable Site**

```bash
sudo ln -s /etc/nginx/sites-available/vectordb-comparison /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Using Systemd Service

Create `/etc/systemd/system/vectordb-backend.service`:

```ini
[Unit]
Description=Vector DB Comparison Backend
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/vectordb-vs-sqldb/backend
Environment="PATH=/path/to/vectordb-vs-sqldb/venv/bin"
ExecStart=/path/to/vectordb-vs-sqldb/venv/bin/gunicorn -c ../gunicorn_config.py app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable vectordb-backend
sudo systemctl start vectordb-backend
sudo systemctl status vectordb-backend
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY data/ ./data/

EXPOSE 5000

CMD ["python", "backend/app.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

Build and run:

```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port (see Configuration section)
```

#### 2. Module Not Found

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Permission Denied

**Error**: `Permission denied: './scripts/start.sh'`

**Solution**:
```bash
chmod +x scripts/*.sh
```

#### 4. Database Locked

**Error**: `database is locked`

**Solution**:
```bash
# Stop all instances
./scripts/stop.sh

# Remove lock files
rm data/*.db-shm data/*.db-wal

# Restart
./scripts/start.sh
```

#### 5. CORS Errors

**Error**: `Access to fetch at 'http://localhost:5000' has been blocked by CORS policy`

**Solution**:
- Ensure Flask-CORS is installed
- Check that CORS is enabled in `backend/app.py`
- Open frontend via the start script (not directly opening HTML file)

### Log Files

Check logs for detailed error information:

```bash
# Backend logs
cat logs/backend.log

# Gunicorn logs (if using)
cat logs/gunicorn_error.log
cat logs/gunicorn_access.log
```

## Maintenance

### Updating Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade flask
```

### Database Maintenance

```bash
# Backup databases
cp data/traditional.db data/traditional.db.backup
cp data/vector.db data/vector.db.backup

# Clear databases (via API)
curl -X POST http://localhost:5000/api/clear

# Or delete database files
rm data/*.db
```

### Monitoring

#### Check Application Health

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### Monitor Resource Usage

```bash
# CPU and Memory
top -p $(pgrep -f "python.*app.py")

# Disk usage
du -sh data/
```

### Backup Strategy

1. **Database Backups**
```bash
# Create backup script
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp data/*.db "$BACKUP_DIR/"
echo "Backup created: $BACKUP_DIR"
EOF

chmod +x scripts/backup.sh
```

2. **Automated Backups** (using cron)
```bash
# Add to crontab
crontab -e

# Add line (daily backup at 2 AM)
0 2 * * * /path/to/vectordb-vs-sqldb/scripts/backup.sh
```

### Performance Tuning

1. **Increase Gunicorn Workers**
```python
# gunicorn_config.py
workers = multiprocessing.cpu_count() * 2 + 1
```

2. **Enable Database WAL Mode**
```python
# In traditional_db.py and vector_db.py
cursor.execute("PRAGMA journal_mode=WAL")
```

3. **Optimize Embeddings Cache**
```python
# In vector_db.py
self.model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./cache')
```

## Security Considerations

### Production Checklist

- [ ] Disable Flask debug mode
- [ ] Use environment variables for sensitive data
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Use HTTPS (SSL/TLS)
- [ ] Regular security updates
- [ ] Restrict CORS origins
- [ ] Implement input validation
- [ ] Set up firewall rules
- [ ] Regular backups

### Example Production Configuration

```python
# backend/app.py
import os

app = Flask(__name__)

# Production settings
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Restrict CORS to specific origins
CORS(app, origins=['https://your-domain.com'])

# Run with production server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
```

## Support

For issues and questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review logs in `logs/` directory
3. Consult the [README.md](../README.md)
4. Open an issue on GitHub

## Version History

- **v1.0.0** - Initial release
  - Traditional SQL database implementation
  - Vector database with semantic search
  - Web-based GUI
  - Automated deployment scripts