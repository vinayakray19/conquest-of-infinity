# A Digital Diary - Vinayak Ray

A minimal, modern personal blog showcasing thoughts, reflections, and philosophical musings. Built with a modular architecture separating frontend and backend for easy maintenance and upgrades.

## Project Structure

```
conquest-of-infinity/
├── backend/                    # Backend API (FastAPI)
│   ├── api/
│   │   ├── models.py          # Database models
│   │   ├── database.py        # Database configuration
│   │   └── routes/            # API endpoints
│   ├── config.py              # Configuration
│   ├── main.py                # Application entry point
│   └── requirements.txt       # Backend dependencies
│
├── css/                       # Frontend styles
│   └── styles.css             # All styling
├── js/                        # JavaScript modules
│   ├── config.js              # Configuration
│   ├── api.js                 # API client
│   ├── utils.js               # Utilities
│   ├── diary.js               # Diary page logic
│   └── memo.js                # Memo page logic
├── index.html                 # Home page (GitHub Pages entry)
├── diary.html                 # Diary listing
└── memo.html                  # Memo detail page
│
├── scripts/                    # Utility scripts
│   ├── migrate_memos.py       # Migrate HTML to database
│   ├── add_memo_api.py        # Add memo via API
│   └── test_api.py            # Test API
│
└── memos.db                    # SQLite database
```

## Quick Start

### 1. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Scripts (optional, for migration and utilities):**
```bash
cd scripts
pip install -r requirements.txt
```

### 2. Initialize Database

The database will be automatically created when you start the backend. If you have existing HTML memo files to migrate, use:
```bash
python3 scripts/migrate_memos.py
```

### 3. Start the Backend Server

```bash
# From project root
python3 backend/main.py

# Or with uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

The API will be available at `http://localhost:8001`
- API Docs: `http://localhost:8001/docs`
- Health Check: `http://localhost:8001/health`

### 4. View the Frontend

Open `diary.html` in your browser (or serve via a web server).

**For GitHub Pages:**
- Push your code to GitHub
- Enable GitHub Pages in repository settings
- The frontend files are in the root directory for easy GitHub Pages hosting

## Features

- **Modular Architecture**: Clean separation of frontend and backend
- **RESTful API**: FastAPI backend with auto-generated documentation
- **Database-Driven**: SQLite database for fast queries and scalability
- **Dynamic Frontend**: JavaScript modules for maintainable code
- **Responsive Design**: Modern, minimal UI with spring theme
- **Easy Content Management**: Scripts to add memos from URLs or files

## API Endpoints

- `GET /api/memos` - Get all memos (supports pagination and sorting)
- `GET /api/memos/{number}` - Get a specific memo
- `GET /api/memos/nav/{number}` - Get navigation (prev/next) for a memo
- `POST /api/memos` - Create a new memo
- `PUT /api/memos/{number}` - Update a memo
- `DELETE /api/memos/{number}` - Delete a memo
- `GET /api/stats` - Get statistics

## Adding New Memos

### Using the Script (Recommended)

```bash
# Interactive mode
python3 scripts/add_memo_api.py

# Command line
python3 scripts/add_memo_api.py --title "Title" --date "December 31, 2025" --content "Content"

# From URL (WordPress)
python3 scripts/add_memo_api.py --url "https://example.com/post" --title "Title" --date "Date"
```

### Using the API Directly

```bash
curl -X POST http://localhost:8001/api/memos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Memo",
    "content": "Memo content here",
    "date": "2025-12-31T00:00:00"
  }'
```

## Configuration

### Backend Configuration

Edit `backend/config.py` or set environment variables:
- `DATABASE_URL` - Database connection string
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8001)
- `CORS_ORIGINS` - Allowed CORS origins

### Frontend Configuration

Edit `frontend/js/config.js` to change API URL or update `API_BASE_URL` detection logic.

## Development

### Project Structure Benefits

1. **Modular Backend**: Easy to add new routes and features
2. **Reusable Frontend**: JavaScript modules can be shared across pages
3. **Independent Upgrades**: Frontend and backend can be upgraded separately
4. **Better Testing**: Each module can be tested in isolation
5. **Scalability**: Easy to add new features without cluttering

### Adding New Features

**Backend:**
1. Create new route file in `backend/api/routes/`
2. Import and register in `backend/main.py`

**Frontend:**
1. Add JavaScript module in `frontend/js/`
2. Include in HTML files that need it

See `PROJECT_STRUCTURE.md` for detailed architecture documentation.

## Documentation

- `PROJECT_STRUCTURE.md` - Detailed project architecture
- `BACKEND_SETUP.md` - Backend setup and configuration
- `MIGRATION_GUIDE.md` - Guide for migrating from old structure
- `TROUBLESHOOTING.md` - Common issues and solutions

## Browser Support

Modern browsers with support for:
- ES6+ JavaScript (fetch, async/await, arrow functions)
- CSS Grid and Flexbox
- CSS animations

## License

Personal project - All rights reserved.
