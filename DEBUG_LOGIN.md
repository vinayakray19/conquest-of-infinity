# Debugging Login Issues

## Issue: Cannot Login with Credentials

### Problem 1: Port Mismatch
- **Server running on:** Port 8000
- **Frontend configured for:** Port 8001

**Fix:** Updated `js/config.js` to use port 8000 for localhost. If your server is on a different port, update it.

### Problem 2: Environment Variables Not Set
When you run:
```bash
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_password
python3 -m uvicorn backend.main:app --reload
```

The environment variables must be in the **same terminal session** where you start the server.

### Solution: Set Credentials and Start in One Command

```bash
cd /Users/vinayakray/Codebase/vscode/Explain/conquest-of-infinity
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_password
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Verify Credentials Are Loaded

**Option 1: Test API directly**
```bash
curl -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

**Option 2: Use test script**
```bash
./test_login.sh
```

### Check What Credentials Server Is Using

If you're not sure what credentials are active, check:

1. **Default credentials (if no env vars set):**
   - Username: `admin`
   - Password: `admin`

2. **Environment variables override defaults:**
   ```bash
   # Check if set in current shell
   echo $ADMIN_USERNAME
   echo $ADMIN_PASSWORD
   ```

### Common Issues

1. **Server restart needed:** After setting env vars, restart the server
2. **Wrong terminal:** Env vars only exist in the terminal where they're set
3. **Port mismatch:** Make sure frontend and backend use same port
4. **Browser cache:** Clear browser cache or use incognito mode

### Quick Fix: Use Default Credentials

If you just want to test, use the defaults:
- Username: `admin`
- Password: `admin`

The server will accept these if no environment variables are set.

### Set Up Properly

1. Create `.env` file:
```bash
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
```

2. Load and start:
```bash
export $(cat .env | xargs)
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

3. Test login:
```bash
./test_login.sh
```

