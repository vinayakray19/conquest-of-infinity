# Render Deployment Fix

## Issue
SQLAlchemy 2.0.23 is not compatible with Python 3.13, causing import errors.

## Solution

### Option 1: Use Python 3.12 (Recommended)

1. **Set Python version in Render:**
   - Go to Render Dashboard → Your Service → Settings
   - Set "Python Version" to `3.12.8` or `3.12`
   - Or add `runtime.txt` file in project root with: `python-3.12.8`

2. **Updated dependencies:**
   - SQLAlchemy updated to `>=2.0.36` (compatible with Python 3.13)
   - All other dependencies updated to latest compatible versions

### Option 2: Manual Configuration in Render

If using manual setup (not render.yaml):

1. **Environment Settings:**
   - Python Version: `3.12.8`

2. **Build Command:**
   ```bash
   pip install --upgrade pip && pip install -r backend/requirements.txt
   ```

3. **Start Command:**
   ```bash
   gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

## Updated Files

- `backend/requirements.txt` - Updated SQLAlchemy to >=2.0.36
- `runtime.txt` - Pins Python to 3.12.8
- `render.yaml` - Updated with Python 3.12 runtime

## Verification

After deployment, check:
1. Service starts without errors
2. Health check: `https://your-service.onrender.com/health`
3. API docs: `https://your-service.onrender.com/docs`

