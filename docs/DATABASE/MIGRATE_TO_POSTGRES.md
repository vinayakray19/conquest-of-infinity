# Migrate to PostgreSQL on Render

This guide walks you through migrating your memos from local SQLite to PostgreSQL on Render.

## Step 1: Get Your PostgreSQL Connection String

1. **Go to Render Dashboard** → Your PostgreSQL Database
2. **Click the "Connect" tab**
3. **Copy the connection string:**
   - **For local migration:** Use "External Connection String" or "Connection Pooling"
   - **For Render Shell:** Use "Internal Database URL"

The connection string looks like:
```
postgres://user:password@host:port/dbname
```

## Step 2: Set Environment Variable

### On macOS/Linux:

```bash
export DATABASE_URL="postgres://user:password@host:port/dbname"
```

### On Windows (PowerShell):

```powershell
$env:DATABASE_URL="postgres://user:password@host:port/dbname"
```

### On Windows (CMD):

```cmd
set DATABASE_URL=postgres://user:password@host:port/dbname
```

## Step 3: Install Dependencies (if needed)

Make sure you have the required packages:

```bash
# Install backend dependencies (includes psycopg)
pip install -r backend/requirements.txt

# Or install just what's needed for migration
pip install sqlalchemy psycopg[binary]
```

## Step 4: Run Migration

```bash
python3 scripts/migrate_to_postgresql.py
```

The script will:
1. ✅ Connect to local SQLite database
2. ✅ Connect to Render PostgreSQL database
3. ✅ Create tables if they don't exist
4. ✅ Read all memos from SQLite
5. ✅ Transfer each memo to PostgreSQL (skipping duplicates)
6. ✅ Show migration summary

## Step 5: Verify Migration

After migration completes, verify your data:

### Option A: Via Render Dashboard

1. Go to your Web Service → Logs
2. Check for successful startup (no database errors)
3. Test the API: `https://your-service.onrender.com/api/stats`
4. Should show the correct number of memos

### Option B: Via API

```bash
# Check stats
curl https://your-service.onrender.com/api/stats

# List memos
curl https://your-service.onrender.com/api/memos?limit=10
```

### Option C: Via Profile Page

1. Go to your Profile page
2. Check "Existing Memos" section
3. Should see all your migrated memos

## Troubleshooting

### Issue: "DATABASE_URL not set"
**Fix:** Make sure you've set the environment variable:
```bash
echo $DATABASE_URL  # Should show your connection string
```

### Issue: "Connection refused" or "timeout"
**Fix:** 
- Use **External Connection String** from Render (if migrating from local machine)
- Check if your IP needs to be whitelisted in Render
- Verify database is running (not paused)

### Issue: "No module named 'psycopg'"
**Fix:** Install the package:
```bash
pip install psycopg[binary]
```

### Issue: "ModuleNotFoundError: No module named 'backend'"
**Fix:** Run from project root directory:
```bash
cd /path/to/conquest-of-infinity
python3 scripts/migrate_to_postgresql.py
```

### Issue: "memos.db not found"
**Fix:** 
- Make sure `memos.db` is in the project root
- Or you can migrate directly via API (see Alternative Method below)

## Alternative: Migrate via API (If you don't have local SQLite)

If you don't have a local `memos.db` file but have memos somewhere else:

1. **Export memos from current location** (if possible)
2. **Use the Profile page** to manually add memos via the web interface
3. **Or use the API directly:**

```bash
# Get your auth token first
curl -X POST https://your-service.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'

# Use the token to create memos
curl -X POST https://your-service.onrender.com/api/memos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Your Memo Title",
    "content": "Your memo content here",
    "date": "2025-01-15T00:00:00"
  }'
```

## After Migration

✅ **Data is now persistent!**
- Your memos survive service sleeps
- Data persists across redeploys
- No more data loss!

## Next Steps

1. **Verify all memos are present** in PostgreSQL
2. **Test the application** - everything should work the same
3. **Optional: Backup your local SQLite** file before deleting it
4. **Local development** will still use SQLite (configured automatically)

## Notes

- The migration script **skips duplicate memos** (by memo_number)
- If migration fails partway, you can run it again (it's safe to retry)
- The script preserves all memo data: title, content, date, timestamps
- Local SQLite file is not modified (read-only operation)

## Quick Reference

```bash
# 1. Get connection string from Render Dashboard
# 2. Set environment variable
export DATABASE_URL="postgres://user:pass@host:port/dbname"

# 3. Run migration
python3 scripts/migrate_to_postgresql.py

# 4. Verify
curl https://your-service.onrender.com/api/stats
```

That's it! Your data is now in PostgreSQL and will persist! 🎉

