# Vector Database vs Traditional SQL Database Comparison

An educational demonstration application showcasing the differences between traditional SQL databases and Vector Databases.

## 🚀 Quick Start (1 Command!)

### Run the Application

```bash
cd /Users/alainairom/Devs/vectordb-vs-sqldb
./scripts/launch.sh
```

**That's it!** The unified launcher automatically:
- ✅ Checks Python installation
- ✅ Creates virtual environment (if needed)
- ✅ Installs all dependencies
- ✅ Creates necessary directories
- ✅ Clears port 8080 if occupied
- ✅ Starts the server

### Open in Browser

The console will display:
```
🌐 OPEN THIS URL IN YOUR BROWSER:
   ┌─────────────────────────────────────┐
   │  http://localhost:8080              │
   └─────────────────────────────────────┘
```

**Open**: http://localhost:8080

### Stop the Application

Press `Ctrl+C` in the terminal where the application is running

---

## 🎯 Overview

This application provides a side-by-side comparison of:
- **Traditional SQL Database**: Exact text matching with SQL LIKE queries
- **Vector Database**: Semantic search with embeddings for context-aware results

## ✨ Features

- 🔍 **Dual Search Comparison**: Search simultaneously in both database types
- 📊 **Performance Metrics**: Real-time execution time comparison
- 🎨 **Interactive GUI**: Modern web-based interface
- 📈 **Statistics Dashboard**: View database statistics and insights
- 🚀 **Easy Setup**: Simple run script
- 📝 **Sample Data**: Pre-loaded with 25 diverse products

## 🏗️ Architecture

```
vectordb-vs-sqldb/
├── backend/              # Python Flask API
│   ├── app.py           # Main API server
│   ├── traditional_db.py # Traditional SQLite implementation
│   ├── vector_db.py     # Vector database implementation
│   └── sample_data.py   # Sample product data
├── frontend/            # Web-based GUI
│   ├── index.html       # Main HTML page
│   ├── styles.css       # Styling
│   └── app.js          # Frontend logic
├── scripts/             # Automation scripts
│   ├── start.sh        # Launch application
│   ├── stop.sh         # Stop application
│   └── push_to_github.sh # Git automation
├── docs/               # Documentation
├── data/               # Database files (auto-generated)
└── logs/               # Application logs
```

## 📂 Available Scripts

All scripts are in the `scripts/` folder:

| Script | Purpose | Usage |
|--------|---------|-------|
| **launch.sh** | ⭐ **RECOMMENDED** - Unified launcher (auto-setup) | `./scripts/launch.sh` |
| stop.sh | Stop the application | `./scripts/stop.sh` |
| push_to_github.sh | Push to GitHub | `./scripts/push_to_github.sh <repo-url>` |

**Recommended**: Use `./scripts/launch.sh` - it handles everything automatically!

## 📖 Usage Guide

### Search Examples

Try these queries to see the difference between exact matching and semantic search:

| Query | Traditional SQL | Vector Database |
|-------|----------------|-----------------|
| "comfortable seating" | May find nothing | Finds chairs, ottomans |
| "exercise equipment" | Limited results | Finds yoga mats, dumbbells, resistance bands |
| "kitchen appliances" | Exact matches only | Finds blenders, coffee makers, air fryers |
| "work from home" | May miss items | Finds desks, chairs, laptops stands |

### Key Differences Demonstrated

**Traditional SQL Database:**
- ✓ Fast for exact keyword matches
- ✓ Simple and predictable
- ✗ Misses semantic relationships
- ✗ Requires exact words in query

**Vector Database:**
- ✓ Understands context and meaning
- ✓ Finds semantically related items
- ✓ Works with synonyms and related concepts
- ✗ Slightly slower due to embedding computation

## 🛠️ Technical Details

### Backend Stack

- **Framework**: Flask 3.0.0
- **Database**: SQLite 3
- **Vector Extension**: sqlite-vec 0.1.1
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Dimensions**: 384

### API Endpoints

- `GET /api/health` - Health check
- `POST /api/initialize` - Initialize databases with sample data
- `POST /api/search/traditional` - Search traditional database
- `POST /api/search/vector` - Search vector database
- `POST /api/search/compare` - Compare both databases
- `GET /api/stats` - Get database statistics
- `POST /api/clear` - Clear all data

### Frontend Stack

- Pure HTML5, CSS3, JavaScript (ES6+)
- No framework dependencies
- Responsive design
- Modern UI with gradient backgrounds

## 📊 Performance Comparison

Typical performance metrics (on sample dataset):

| Operation | Traditional SQL | Vector Database |
|-----------|----------------|-----------------|
| Exact match | ~1-5ms | ~50-100ms |
| Semantic search | N/A | ~50-100ms |
| Initialization | ~10ms | ~2-3s (embedding generation) |

## 🔧 Development

### Project Structure

```
backend/
├── traditional_db.py    # SQL LIKE-based search
├── vector_db.py        # Embedding-based semantic search
├── sample_data.py      # 25 sample products
└── app.py             # Flask API with CORS

frontend/
├── index.html         # Main interface
├── styles.css         # Modern gradient design
└── app.js            # API integration
```

### Adding More Data

Edit `backend/sample_data.py` to add more products:

```python
SAMPLE_PRODUCTS = [
    {
        "name": "Product Name",
        "description": "Detailed description",
        "category": "Category",
        "price": 99.99
    },
    # Add more products...
]
```

## 📝 Scripts

### Start Application
```bash
./scripts/start.sh
```
- Creates virtual environment
- Installs dependencies
- Starts backend server
- Opens frontend in browser

### Stop Application
```bash
./scripts/stop.sh
```
- Stops backend server
- Cleans up processes

### Push to GitHub
```bash
./scripts/push_to_github.sh
```
- Interactive git commit and push
- Automatic commit message generation
- Status confirmation

## 🐛 Troubleshooting

### Backend won't start
- Check if port 5000 is available: `lsof -i :5000`
- View logs: `cat logs/backend.log`
- Ensure Python 3.8+ is installed: `python3 --version`

### Dependencies installation fails
- Upgrade pip: `pip install --upgrade pip`
- Install manually: `pip install -r requirements.txt`

### Frontend can't connect to backend
- Ensure backend is running: `curl http://localhost:5000/api/health`
- Check browser console for CORS errors
- Verify firewall settings

## 📚 Educational Value

This application demonstrates:

1. **Database Paradigms**: Traditional relational vs. vector-based storage
2. **Search Techniques**: Exact matching vs. semantic similarity
3. **Embeddings**: How text is converted to numerical vectors
4. **Performance Trade-offs**: Speed vs. semantic understanding
5. **Use Cases**: When to use each database type

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🔗 References

- [SQLite Official](https://github.com/sqlite/sqlite)
- [sqlite-vec Extension](https://github.com/sqliteai/sqlite-vector)
- [Sentence Transformers](https://www.sbert.net/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 👨‍💻 Author

Created as an educational demonstration of database technologies.

## 🙏 Acknowledgments

- SQLite team for the robust database engine
- sqlite-vec developers for the vector extension
- Sentence Transformers team for the embedding models