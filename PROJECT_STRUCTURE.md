# Project Structure

This project follows a clean, modular architecture separating frontend and backend for easy maintenance and upgrades.

## Directory Structure

```
conquest-of-infinity/
├── backend/                    # Backend API (FastAPI)
│   ├── api/
│   │   ├── models.py          # Database models
│   │   ├── database.py        # Database configuration
│   │   ├── auth.py            # Authentication utilities
│   │   └── routes/            # API endpoints
│   │       ├── memos.py       # Memo endpoints
│   │       ├── auth.py        # Authentication endpoints
│   │       └── stats.py       # Statistics endpoints
│   ├── config.py              # Backend configuration
│   ├── main.py                # FastAPI application entry point
│   └── requirements.txt       # Backend dependencies
│
├── css/                       # Frontend styles
│   └── styles.css             # All styling (global)
│
├── js/                        # JavaScript modules
│   ├── config.js              # Frontend configuration
│   ├── api.js                 # API client
│   ├── auth.js                # Authentication handling
│   ├── nav.js                 # Navigation logic
│   ├── utils.js               # Utility functions
│   ├── diary.js               # Diary listing page
│   ├── memo.js                # Memo detail page
│   └── profile.js             # Profile page
│
├── docs/                      # Documentation
│   ├── SETUP/                 # Setup guides
│   │   ├── BACKEND_SETUP.md
│   │   ├── LOCAL_TESTING.md
│   │   ├── GITHUB_PAGES_SETUP.md
│   │   ├── RENDER_DEPLOYMENT.md
│   │   ├── RENDER_FIXES.md
│   │   └── RENDER_PYTHON_FIX.md
│   ├── DATABASE/              # Database guides
│   │   ├── POSTGRESQL_SETUP.md
│   │   ├── SETUP_POSTGRESQL_RENDER.md
│   │   ├── MIGRATE_TO_POSTGRES.md
│   │   ├── MIGRATE_TO_RENDER.md
│   │   └── MIGRATION_GUIDE.md
│   ├── AUTH/                  # Authentication guides
│   │   ├── AUTHENTICATION_SETUP.md
│   │   ├── CHANGE_CREDENTIALS.md
│   │   └── DEBUG_LOGIN.md
│   ├── TROUBLESHOOTING.md
│   └── README.md
│
├── scripts/                   # Utility scripts
│   ├── setup/                 # Setup scripts
│   │   ├── start_backend.sh
│   │   ├── test_local.sh
│   │   ├── test_login.sh
│   │   └── migrate_now.sh
│   ├── migrations/            # Migration scripts
│   │   ├── migrate_memos.py
│   │   ├── migrate_to_postgresql.py
│   │   └── migrate_to_render.py
│   ├── utils/                 # Utility scripts
│   │   ├── test_api.py
│   │   └── check_render_status.py
│   ├── add_memo_api.py        # Add memo via API
│   └── requirements.txt       # Script dependencies
│
├── index.html                 # Home page
├── diary.html                 # Diary listing page
├── memo.html                  # Memo detail page
├── login.html                 # Login page
├── profile.html               # Profile/Admin page
│
├── render.yaml                # Render deployment config
├── runtime.txt                # Python version
├── README.md                  # Main documentation
├── QUICK_START.md             # Quick start guide
├── PROJECT_STRUCTURE.md       # This file
└── ADD_MEMO_EXAMPLE.md        # Example usage
```

## Key Design Principles

### 1. Separation of Concerns
- **Backend**: FastAPI application with modular routes
- **Frontend**: Static HTML + JavaScript modules
- **Documentation**: Organized by topic in `docs/`
- **Scripts**: Organized by purpose

### 2. Modular Architecture

#### Backend
- `config.py` - Centralized configuration
- `api/models.py` - Database models
- `api/database.py` - Database connection
- `api/routes/` - API endpoints (one file per resource)
- `main.py` - Application entry point

#### Frontend
- `js/config.js` - Configuration
- `js/api.js` - API client (reusable)
- `js/auth.js` - Authentication (reusable)
- `js/utils.js` - Utilities (reusable)
- Page-specific modules: `diary.js`, `memo.js`, `profile.js`

### 3. File Organization

- **Root level**: Only essential files (HTML, config, main docs)
- **Documentation**: Organized in `docs/` by category
- **Scripts**: Organized by purpose (`setup/`, `migrations/`, `utils/`)
- **No redundancy**: Single source of truth for each file

## Development Workflow

### Backend Development
```bash
# Start backend server
cd scripts/setup
./start_backend.sh

# Or manually
python3 -m uvicorn backend.main:app --reload --port 8001
```

### Frontend Development
- Edit HTML files in root
- Edit JavaScript in `js/`
- Edit CSS in `css/styles.css`
- No build step required

### Adding Features

**Backend:**
1. Add routes in `backend/api/routes/`
2. Update models in `backend/api/models.py` if needed
3. Register routes in `backend/main.py`

**Frontend:**
1. Add JavaScript module in `js/` if reusable
2. Update page-specific JS if needed
3. Update HTML to use new functionality

### Running Scripts

```bash
# Migration scripts
python3 scripts/migrations/migrate_to_postgresql.py

# Utility scripts
python3 scripts/utils/test_api.py

# Add memo
python3 scripts/add_memo_api.py
```

## File Naming Conventions

- **HTML**: lowercase with hyphens (`diary.html`, `login.html`)
- **JavaScript**: camelCase (`diary.js`, `profile.js`)
- **Python**: snake_case (`migrate_memos.py`, `add_memo_api.py`)
- **Documentation**: UPPERCASE with underscores (`BACKEND_SETUP.md`)

## Deployment Structure

- **Frontend**: Files in root directory (GitHub Pages compatible)
- **Backend**: `backend/` directory (deployed to Render)
- **Config**: `render.yaml` for Render deployment

## Benefits of This Structure

✅ **Clear Organization** - Easy to find files  
✅ **No Redundancy** - Single source of truth  
✅ **Modular** - Easy to upgrade components  
✅ **Scalable** - Easy to add new features  
✅ **Maintainable** - Clear separation of concerns  
✅ **Documented** - Organized documentation  
