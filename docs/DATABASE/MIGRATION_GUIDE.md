# Migration Guide: Old to New Structure

This guide helps you migrate from the old flat structure to the new modular structure.

## Quick Start

The new structure is ready to use. Follow these steps:

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Script Dependencies

```bash
cd scripts
pip install -r requirements.txt
cd ..
```

### 3. Start the Backend

```bash
# From project root
python backend/main.py

# Or using uvicorn directly
uvicorn backend.main:app --reload --port 8001
```

### 4. Use the Frontend

Open `root diary.html` in your browser (or serve via a web server).

## File Mapping

### Backend Files

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `api.py` | `backend/main.py` + `backend/api/routes/memos.py` | Split into main app and routes |
| `models.py` | `backend/api/models.py` | Moved to api package |
| N/A | `backend/config.py` | New: Configuration management |
| N/A | `backend/api/database.py` | New: Database setup |

### Frontend Files

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `diary.html` | `root diary.html` | Updated to use JS modules |
| `memo.html` | `root memo.html` | Updated to use JS modules |
| `index.html` | `root index.html` | Unchanged |
| `css/styles.css` | `css/styles.css` | Same location |
| N/A | `js/*.js` | New: Extracted JavaScript modules |

### Scripts

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `migrate_memos.py` | `scripts/migrate_memos.py` | Updated imports |
| `add_memo_api.py` | `scripts/add_memo_api.py` | Same functionality |
| `test_api.py` | `scripts/test_api.py` | Same functionality |

## Breaking Changes

1. **Import Paths**: Scripts now import from `backend.api.*` instead of root-level modules
2. **Running Backend**: Use `python backend/main.py` instead of `python api.py`
3. **Frontend Paths**: Use `root diary.html` instead of `diary.html`

## Backward Compatibility

The old files are still in the root directory but are **deprecated**. They still work but should not be used for new development.

- Old `api.py` still works but won't have latest features
- Old HTML files still work but use inline JavaScript (harder to maintain)

## Next Steps

1. Update any scripts or documentation that reference old file paths
2. Gradually migrate to using `root ` directory
3. Remove old files once fully migrated (optional)

