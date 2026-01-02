# Backend Setup Guide

This guide will help you set up the backend system for your digital diary.

## Overview

The system uses a modular architecture with a database-driven backend:
- **FastAPI**: Modern, fast Python web framework
- **SQLite**: Lightweight database (easy to migrate to PostgreSQL later)
- **RESTful API**: Clean API endpoints for all operations
- **Modular Structure**: Separated frontend and backend for easy maintenance

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

2. **Install script dependencies (optional, for utilities):**
   ```bash
   cd scripts
   pip install -r requirements.txt
   cd ..
   ```

3. **Migrate existing HTML memos to database (if you have HTML files to migrate):**
   ```bash
   python3 scripts/migrate_memos.py
   ```
   **Note:** This step is only needed if you have HTML memo files. The database will be created automatically when the backend starts.

4. **Start the API server:**
   ```bash
   # From project root
   python3 backend/main.py
   
   # Or with uvicorn directly
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
   ```
   
   The API will be available at `http://localhost:8001`

5. **Test the API:**
   Open your browser and visit:
   - `http://localhost:8001/docs` - Interactive API documentation (Swagger UI)
   - `http://localhost:8001/redoc` - Alternative API documentation
   - `http://localhost:8001/api/memos` - Get all memos (JSON)
   - `http://localhost:8001/health` - Health check endpoint

## Usage

### Adding New Memos

Use the API script:
```bash
python3 scripts/add_memo_api.py --title "My Title" --date "December 31, 2025" --content "My content"
```

Or with URL:
```bash
python3 scripts/add_memo_api.py --url "https://example.com/post" --title "Title" --date "Date"
```

Or interactively:
```bash
python3 scripts/add_memo_api.py
```

### Frontend

The frontend is located in the `frontend/` directory:
- `frontend/index.html` - Home page
- `frontend/diary.html` - Diary listing page (loads memos from API)
- `frontend/memo.html` - Memo detail page (loads from API)

Open `frontend/diary.html` in your browser (or serve via a web server) and it will automatically load memos from the API.

**Important:** Make sure the API server is running when viewing the frontend pages.

### API Endpoints

- `GET /api/memos` - Get all memos (supports `?order=desc&limit=100`)
- `GET /api/memos/{memo_number}` - Get a specific memo by number
- `GET /api/memos/nav/{memo_number}` - Get navigation (prev/next) for a memo
- `POST /api/memos` - Create a new memo
- `PUT /api/memos/{memo_number}` - Update a memo
- `DELETE /api/memos/{memo_number}` - Delete a memo
- `GET /api/stats` - Get statistics

## Configuration

### Backend Configuration

Edit `backend/config.py` or set environment variables:
- `DATABASE_URL` - Database connection string (default: `sqlite:///memos.db`)
- `API_HOST` - API host (default: `0.0.0.0`)
- `API_PORT` - API port (default: `8001`)
- `CORS_ORIGINS` - Allowed CORS origins (default: `*`)
- `ENVIRONMENT` - Environment name (default: `development`)

### Frontend Configuration

The frontend automatically detects the API URL. Edit `frontend/js/config.js` if you need to customize:
- Automatically uses `http://localhost:8001` on localhost
- Uses relative URLs in production (if API and frontend on same domain)

### Database

By default, the database is stored in `memos.db` (SQLite) in the project root. To use PostgreSQL:

1. Install PostgreSQL adapter: `pip install psycopg2-binary`
2. Set environment variable: `export DATABASE_URL=postgresql://user:password@localhost/dbname`
3. Restart the API server

The database is automatically created when the backend starts if it doesn't exist.

## File Structure

```
.
├── backend/                    # Backend API code
│   ├── api/
│   │   ├── models.py          # Database models
│   │   ├── database.py        # Database configuration
│   │   └── routes/            # API routes
│   │       ├── memos.py       # Memo endpoints
│   │       └── stats.py       # Statistics endpoints
│   ├── config.py              # Configuration
│   ├── main.py                # Application entry point
│   └── requirements.txt       # Backend dependencies
│
├── frontend/                   # Frontend code
│   ├── css/
│   │   └── styles.css         # Styles
│   ├── js/                    # JavaScript modules
│   │   ├── config.js          # Configuration
│   │   ├── api.js             # API client
│   │   ├── utils.js           # Utilities
│   │   ├── diary.js           # Diary page logic
│   │   └── memo.js            # Memo page logic
│   ├── index.html             # Home page
│   ├── diary.html             # Diary listing
│   └── memo.html              # Memo detail
│
├── scripts/                    # Utility scripts
│   ├── migrate_memos.py       # Migrate HTML to database
│   ├── add_memo_api.py        # Add memo via API
│   ├── test_api.py            # Test API
│   └── requirements.txt       # Script dependencies
│
└── memos.db                    # SQLite database (all memos stored here)
```

## Benefits

1. **Performance**: Database queries are much faster than reading multiple HTML files
2. **Scalability**: Easy to add pagination, search, filtering
3. **Maintainability**: Single source of truth for memo data
4. **API Access**: Can build mobile apps, integrations, etc.
5. **No File Management**: No need to manage hundreds of HTML files
6. **Modular Architecture**: Easy to upgrade and maintain

## Migration Notes

- All memos are stored in the database (`memos.db`)
- HTML memo files can be migrated using `scripts/migrate_memos.py` if needed
- The frontend uses JavaScript to fetch data dynamically from the API
- The system is fully database-driven - no HTML file management needed

## Troubleshooting

**Issue: CORS errors in browser**
- The API includes CORS middleware configured in `backend/main.py`
- Check the `allow_origins` setting in `backend/config.py`

**Issue: Memos not loading**
- Make sure the API server is running: `python3 backend/main.py`
- Check browser console for errors (F12)
- Verify API is accessible: `curl http://localhost:8001/api/memos`
- Check `frontend/js/config.js` for API URL configuration

**Issue: Migration fails**
- Make sure script dependencies are installed: `pip install -r scripts/requirements.txt`
- Check that HTML memo files exist (if migrating from old system)
- Verify database permissions

**Issue: Module not found errors**
- Make sure you're running from the project root
- Install backend dependencies: `pip install -r backend/requirements.txt`
- Check Python path is set correctly

**Issue: Database not found**
- The database is automatically created on first startup
- Check file permissions in the project directory
- Verify `DATABASE_URL` in `backend/config.py` is correct

## Testing

Test the API:
```bash
python3 scripts/test_api.py
```

This will verify:
- API server connectivity
- Database access
- Endpoint functionality

## Next Steps

- Add authentication if needed
- Implement search functionality
- Add tags/categories
- Set up production deployment
- Migrate to PostgreSQL for better performance at scale
- Add caching for better performance
- Implement pagination for large datasets
