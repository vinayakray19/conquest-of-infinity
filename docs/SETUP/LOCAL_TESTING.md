# Local Testing Guide for Mac

## Quick Start

### 1. Install Dependencies

```bash
# Install backend dependencies
cd backend
pip3 install -r requirements.txt
cd ..

# Install script dependencies (optional)
cd scripts
pip3 install -r requirements.txt
cd ..
```

### 2. Set Environment Variables (Optional - uses defaults if not set)

```bash
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=admin
export SECRET_KEY=your-secret-key-for-local-testing-min-32-chars
```

### 3. Start the Backend Server

**Important:** Run from the project root directory.

```bash
# Option 1: Using uvicorn (recommended)
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001

# Option 2: Using the test script
./test_local.sh

# Option 3: If uvicorn is installed globally
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

The API will be available at `http://localhost:8001`

### 4. Test the Frontend

Open in your browser:
- Home: `file:///path/to/conquest-of-infinity/index.html`
- Or use a local server:

```bash
# Option 1: Python HTTP server
python3 -m http.server 8000

# Then open: http://localhost:8000/index.html
```

```bash
# Option 2: PHP server (if installed)
php -S localhost:8000

# Then open: http://localhost:8000/index.html
```

## Testing Steps

### 1. Test API is Running

```bash
# Health check
curl http://localhost:8001/health

# Should return: {"status":"healthy"}
```

### 2. Test Login

```bash
# Login API
curl -X POST http://localhost:8001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Should return token and username
```

### 3. Test Frontend Login

1. Open `http://localhost:8000/login.html` (or `login.html` directly)
2. Enter:
   - Username: `admin`
   - Password: `admin`
3. Click "Login"
4. Should redirect to `profile.html`

### 4. Test Adding a Post

1. After logging in, fill in the form:
   - Title: "Test Post"
   - Date: Select today's date
   - Content: "This is a test post"
2. Click "Create Post"
3. Should see success message and the post appears in diary

### 5. Verify Post in Database

```bash
# Check all memos
curl http://localhost:8001/api/memos

# Check stats
curl http://localhost:8001/api/stats
```

## Troubleshooting

### Port Already in Use

If port 8001 is busy:
```bash
# Find process using port
lsof -ti:8001

# Kill it (replace PID)
kill -9 <PID>

# Or use different port
export API_PORT=8002
python3 backend/main.py
```

### Database Issues

```bash
# Check if database exists
ls -la memos.db

# If needed, initialize database
python3 backend/main.py
# Database will be created automatically
```

### CORS Errors

Make sure CORS is enabled in `backend/config.py`:
```python
CORS_ORIGINS = ['*']  # For local testing
```

### Frontend Can't Connect to API

Check `js/config.js` - it should automatically use `http://localhost:8001` for localhost.

## Complete Testing Command Sequence

```bash
# Terminal 1: Start backend
cd /path/to/conquest-of-infinity
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=admin
python3 backend/main.py

# Terminal 2: Start frontend server (optional)
cd /path/to/conquest-of-infinity
python3 -m http.server 8000

# Then open browser: http://localhost:8000/login.html
```

## Testing Checklist

- [ ] Backend starts without errors
- [ ] API health check returns healthy
- [ ] Login page loads
- [ ] Can login with credentials
- [ ] Redirects to profile page after login
- [ ] Profile page shows add post form
- [ ] Can create a new post
- [ ] Post appears in diary listing
- [ ] Can logout
- [ ] Protected endpoints require authentication

