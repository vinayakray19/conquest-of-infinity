# Quick Start Guide

## The Problem

If you see "501 Unsupported method" or directory listing on port 8000, you have a **simple HTTP server** running instead of the **FastAPI server**.

## Solution

### Step 1: Stop any server on port 8000

```bash
# Find and stop any process on port 8000
kill $(lsof -ti:8000) 2>/dev/null
```

### Step 2: Start FastAPI Server

**Option A: Use the startup script (Recommended)**
```bash
# With default credentials (admin/admin)
./start_backend.sh

# Or with custom credentials
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_password
./start_backend.sh
```

**Option B: Manual start**
```bash
# Set credentials (optional - defaults to admin/admin)
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_password
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Start server
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify Server is Running

```bash
# Should return: {"status":"healthy"}
curl http://127.0.0.1:8000/health

# Should return API info
curl http://127.0.0.1:8000/
```

### Step 4: Test Login

```bash
# Test script
./test_login.sh

# Or manually
curl -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

## Common Issues

### Issue: "501 Unsupported method"
**Cause:** Simple HTTP server running instead of FastAPI  
**Fix:** Stop the HTTP server and start FastAPI server

### Issue: "Connection refused"
**Cause:** FastAPI server not running  
**Fix:** Start the server with `./start_backend.sh` or uvicorn command

### Issue: "Incorrect username or password"
**Cause:** Credentials don't match what server expects  
**Fix:** Use the credentials you set, or use defaults (admin/admin)

## Two Different Servers

1. **FastAPI Server** (for backend API):
   ```bash
   python3 -m uvicorn backend.main:app --reload --port 8000
   ```
   - Handles `/api/login`, `/api/memos`, etc.
   - Returns JSON responses

2. **Simple HTTP Server** (for serving frontend files):
   ```bash
   python3 -m http.server 8000
   ```
   - Serves static HTML/CSS/JS files
   - Returns directory listings
   - Does NOT handle POST requests

**Use FastAPI server for the backend!**

