# Project Structure

This project has been organized into a modular structure separating frontend and backend code for easier maintenance and upgrades.

## Directory Structure

```
conquest-of-infinity/
├── backend/                    # Backend API code
│   ├── api/                    # API package
│   │   ├── __init__.py
│   │   ├── models.py          # Database models
│   │   ├── database.py        # Database configuration
│   │   └── routes/            # API routes
│   │       ├── __init__.py
│   │       └── memos.py       # Memo-related endpoints
│   ├── config.py              # Backend configuration
│   ├── main.py                # FastAPI application entry point
│   └── requirements.txt       # Backend dependencies
│
├── css/                       # Frontend styles (GitHub Pages ready)
│   └── styles.css             # All styling
├── js/                        # JavaScript modules (GitHub Pages ready)
│   ├── config.js              # Frontend configuration
│   ├── api.js                 # API client
│   ├── utils.js               # Utility functions
│   ├── diary.js               # Diary listing page logic
│   └── memo.js                # Memo detail page logic
├── index.html                 # Home page (GitHub Pages entry point)
├── diary.html                 # Diary listing page
└── memo.html                  # Memo detail page
│
├── scripts/                    # Utility scripts
│   ├── migrate_memos.py       # Migrate HTML memos to database (if needed)
│   ├── add_memo_api.py        # Add new memo via API
│   ├── test_api.py            # Test API connectivity
│   └── requirements.txt       # Script dependencies
│
└── memos.db                    # SQLite database (all memos stored here)
│
└── Documentation files:
    ├── README.md               # Main documentation
    ├── BACKEND_SETUP.md        # Backend setup guide
    ├── TROUBLESHOOTING.md      # Troubleshooting guide
    └── PROJECT_STRUCTURE.md    # This file
```

## Key Design Decisions

### Backend Modularity

1. **Separated Models and Database**: 
   - `models.py` contains only data models
   - `database.py` handles database connection and sessions
   
2. **Route-based Organization**:
   - Each resource (memos) has its own route file
   - Easy to add new resources without cluttering

3. **Configuration Management**:
   - All configuration in `config.py`
   - Environment variable support for deployment

4. **Clear Entry Point**:
   - `main.py` is the single entry point
   - All routes registered here

### Frontend Modularity

1. **Separated JavaScript**:
   - Configuration, API client, and utilities in separate files
   - Page-specific logic in dedicated files
   - Easy to test and maintain

2. **Reusable Components**:
   - `api.js` can be used by any page
   - `utils.js` provides common functions
   - `config.js` centralizes configuration

3. **Clean HTML**:
   - HTML files only contain structure
   - All logic in JavaScript modules

4. **GitHub Pages Ready**:
   - Files in root directory for easy GitHub Pages hosting
   - No build step required
   - Static hosting compatible

### Benefits of This Structure

1. **Easy Upgrades**:
   - Backend and frontend can be upgraded independently
   - Clear separation of concerns

2. **Better Testing**:
   - Each module can be tested in isolation
   - Mock dependencies easily

3. **Scalability**:
   - Easy to add new features
   - New routes don't affect existing code
   - New pages can reuse existing modules

4. **Maintainability**:
   - Clear organization makes finding code easier
   - Reduced code duplication
   - Easier onboarding for new developers

## Migration from Old Structure

The old structure had everything in the root directory. The new structure:
- Preserves all existing functionality
- Maintains backward compatibility where possible
- Allows gradual migration

### Old Files (Deprecated but Preserved)

- `api.py` → Now `backend/main.py` + `backend/api/routes/memos.py`
- `models.py` → Now `backend/api/models.py`
- `diary.html` → Now `frontend/diary.html` (updated to use modules)
- `memo.html` → Now `frontend/memo.html` (updated to use modules)
- `add_memo.py` → Still exists for static HTML generation (if needed)
- `add_memo_api.py` → Moved to `scripts/add_memo_api.py`

## Upgrading the System

### Backend Upgrades

1. **Update Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt --upgrade
   ```

2. **Add New Routes**:
   - Create new file in `backend/api/routes/`
   - Import and register in `backend/main.py`

3. **Update Models**:
   - Edit `backend/api/models.py`
   - Run migrations if needed

### Frontend Upgrades

1. **Update JavaScript Modules**:
   - Edit files in `frontend/js/`
   - Changes automatically reflect in all pages using them

2. **Add New Pages**:
   - Create HTML file in `frontend/`
   - Include necessary JS modules

3. **Update Styles**:
   - Edit `frontend/css/styles.css`
   - Changes apply globally

## Development Workflow

1. **Backend Development**:
   ```bash
   cd backend
   python main.py  # or: uvicorn backend.main:app --reload
   ```

2. **Frontend Development**:
   - Edit files in `frontend/`
   - Use browser dev tools for debugging
   - API calls go to backend on port 8001

3. **Adding Features**:
   - Backend: Add routes in `backend/api/routes/`
   - Frontend: Update or create JS modules in `frontend/js/`
   - Update HTML files to use new functionality

