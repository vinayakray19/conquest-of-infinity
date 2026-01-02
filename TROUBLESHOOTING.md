# Troubleshooting Guide

## Memo Not Loading

If memos are not loading, follow these steps to diagnose the issue:

### 1. Check if API Server is Running

**Test the API:**
```bash
python3 test_api.py
```

This will verify:
- API server is running
- Database has memos
- API endpoints are responding correctly

**If the API is not running:**
```bash
# Start the API server
python3 api.py

# Or with uvicorn
uvicorn api:app --reload --host 0.0.0.0 --port 8001
```

### 2. Check Browser Console

Open your browser's developer console (F12) and look for errors:

- **CORS errors**: The API should have CORS enabled. Check `api.py` line 22-28.
- **Network errors**: Check if the API URL is correct (should be `http://localhost:8001`)
- **404 errors**: The memo number might not exist in the database

### 3. Verify Database Has Data

**Check if memos exist:**
```bash
python3 -c "
from models import SessionLocal, Memo
db = SessionLocal()
count = db.query(Memo).count()
print(f'Total memos in database: {count}')
if count > 0:
    first = db.query(Memo).order_by(Memo.memo_number).first()
    print(f'First memo: #{first.memo_number} - {first.title}')
db.close()
"
```

**If database is empty, migrate existing memos:**
```bash
python3 migrate_memos.py
```

### 4. Check API Response Directly

Test the API endpoint directly in your browser:
- `http://localhost:8001/api/memos` - Should return JSON array of all memos
- `http://localhost:8001/api/memos/1` - Should return memo #1
- `http://localhost:8001/docs` - Interactive API documentation

### 5. Common Issues

#### Issue: "Failed to connect to API"
**Solution:** Make sure the API server is running on port 8001

#### Issue: "Memo #X not found"
**Solution:** 
- Check if the memo exists: `http://localhost:8001/api/memos/X`
- Verify the memo number in the URL parameter

#### Issue: Content is blank or not displaying
**Solution:**
- Check browser console for JavaScript errors
- Verify the content exists in the database
- Check if content has HTML that needs to be preserved

#### Issue: CORS errors in browser
**Solution:** 
- The API has CORS enabled for all origins
- If still seeing errors, verify `CORSMiddleware` is properly configured in `api.py`

### 6. Debug Mode

To see detailed logs, check:
1. Browser console (F12) - JavaScript errors and API calls
2. API server terminal - Python errors and request logs
3. Network tab in browser DevTools - See actual API responses

### 7. Quick Test

Run this to verify everything works:

```bash
# 1. Start API
python3 api.py

# 2. In another terminal, test API
python3 test_api.py

# 3. Open diary.html in browser
# Should see list of memos

# 4. Click on a memo
# Should load memo content
```

## Still Having Issues?

1. Check the error message in browser console
2. Verify API is responding: `curl http://localhost:8001/api/memos`
3. Check database: `sqlite3 memos.db "SELECT COUNT(*) FROM memos;"`
4. Review the API logs for errors

