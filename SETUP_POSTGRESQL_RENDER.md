# Quick Setup: PostgreSQL on Render (Free Tier)

## ⚠️ IMPORTANT: Stop Data Loss!

Your data is being lost because you're using SQLite on Render. SQLite files are **ephemeral** - they disappear when:
- Service sleeps (free tier)
- Service redeploys
- Service restarts

**Solution: Use PostgreSQL** ✅

## Quick Setup (5 minutes)

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name:** `digital-diary-db`
   - **Plan:** **Free**
   - **Region:** Same as your web service
4. Click **"Create Database"**

### Step 2: Link to Your Web Service

**Option A: Automatic (if using Blueprint)**
- Your `render.yaml` already configures this
- Just redeploy or update the service
- PostgreSQL will be automatically linked

**Option B: Manual**
1. Go to your **Web Service** → **"Environment"** tab
2. Click **"Link Resource"**
3. Select `digital-diary-db`
4. Click **"Link"**
5. `DATABASE_URL` will be automatically added

### Step 3: Verify Setup

1. Go to your Web Service → **"Environment"** tab
2. Look for `DATABASE_URL` variable
3. Should look like: `postgres://user:password@host:port/dbname`
4. ✅ If present, you're good!

### Step 4: Redeploy Service

1. Go to your Web Service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Wait for deployment to complete
4. Check logs - should see successful database connection

### Step 5: Verify Data Persists

1. Go to your Profile page
2. Add a test memo
3. Wait 15 minutes (or manually suspend service)
4. Wake up service
5. Check - memo should still be there! ✅

## Migration (If You Have Existing Data)

If you have memos in your local SQLite or previous deployment:

```bash
# Get DATABASE_URL from Render Dashboard
export DATABASE_URL="postgres://user:pass@host:port/dbname"

# Run migration script
python3 scripts/migrate_to_postgresql.py
```

## Troubleshooting

### "DATABASE_URL not found"
- Make sure database is linked to your service
- Check Environment variables in Render Dashboard
- Try unlinking and re-linking the database

### "Connection refused"
- Verify database is running (not paused)
- Check database and service are in same region
- Verify DATABASE_URL is correct

### Data still lost?
- Check logs for database connection errors
- Verify DATABASE_URL starts with `postgres://` (not `sqlite://`)
- Make sure you're using the **Internal Database URL** (not Public URL)

## That's It! 🎉

Your data will now persist across:
- ✅ Service sleeps
- ✅ Deployments
- ✅ Restarts
- ✅ All operations

No more data loss! 🚀

---

**Need more details?** See [POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md) for comprehensive guide.

