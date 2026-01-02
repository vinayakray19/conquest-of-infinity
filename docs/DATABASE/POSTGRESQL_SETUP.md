# PostgreSQL Setup on Render - Free Tier

This guide explains how to set up PostgreSQL on Render's free tier to persist your data.

## Why PostgreSQL?

**SQLite on Render = Data Loss** ❌
- SQLite files are stored in ephemeral filesystem
- Data is lost when service sleeps or redeploys
- Not suitable for production

**PostgreSQL on Render = Persistent Data** ✅
- Data persists across sleeps and redeploys
- Free tier available (90 days, then need to restart)
- Production-ready database

## Setup Steps

### Option 1: Using render.yaml (Automatic - Recommended)

Your `render.yaml` already includes PostgreSQL configuration. Just deploy:

1. **Push your code to GitHub**

2. **In Render Dashboard:**
   - Go to Dashboard
   - Click "New" → "Blueprint"
   - Connect your repository
   - Render will automatically:
     - Create PostgreSQL database
     - Link it to your web service
     - Set `DATABASE_URL` environment variable

3. **Verify Setup:**
   - Check your service's Environment variables
   - `DATABASE_URL` should be set automatically
   - It should look like: `postgres://user:pass@host:port/dbname`

### Option 2: Manual Setup

1. **Create PostgreSQL Database:**
   - Render Dashboard → "New" → "PostgreSQL"
   - Name: `digital-diary-db`
   - Plan: **Free**
   - Region: Choose closest to your web service
   - Click "Create Database"

2. **Link to Web Service:**
   - Go to your web service → "Environment"
   - Click "Link Resource"
   - Select your PostgreSQL database
   - Render will automatically set `DATABASE_URL`

3. **Verify Connection:**
   - Check Environment variables
   - `DATABASE_URL` should be present
   - Format: `postgres://user:password@host:port/dbname`

## Migration from SQLite to PostgreSQL

After setting up PostgreSQL, you need to migrate your existing memos:

### Method 1: Using Migration Script

```bash
# On your local machine, set DATABASE_URL to Render's PostgreSQL
export DATABASE_URL="postgres://user:pass@host:port/dbname"

# Run migration
python3 scripts/migrate_to_render.py
```

### Method 2: Manual Migration via API

1. Export memos from local SQLite (if you have them)
2. Use the migration script pointing to Render's PostgreSQL
3. Or add memos via the Profile page after setup

### Method 3: Fresh Start

If you don't have important data, just start fresh:
- PostgreSQL will be empty
- Add memos via the Profile page
- Data will persist now!

## Verify PostgreSQL is Working

1. **Check Logs:**
   - Render Dashboard → Your Service → Logs
   - Should see successful database connection

2. **Test API:**
   ```bash
   curl https://your-service.onrender.com/api/stats
   ```
   Should return database stats

3. **Check Tables:**
   - Render Dashboard → Your Database → "Connect" tab
   - Use psql or any PostgreSQL client
   - Run: `\dt` to list tables
   - Should see `memos` table

## Important Notes

### Free Tier Limitations

- **90 Days:** Free tier databases pause after 90 days of inactivity
- **Restart Required:** You may need to manually restart the database
- **Size Limit:** 1GB storage limit on free tier
- **Connection Limits:** Limited concurrent connections

### Data Persistence

✅ **Persistent:**
- Database survives service sleep
- Data persists across redeploys
- Database survives service restarts

❌ **Not Persistent (SQLite):**
- Data lost on sleep
- Data lost on redeploy
- Data lost on restart

## Troubleshooting

### Issue: "DATABASE_URL not set"
**Fix:** 
1. Create PostgreSQL database in Render
2. Link it to your web service
3. Check Environment variables

### Issue: "Connection refused"
**Fix:**
1. Verify database is running (not paused)
2. Check DATABASE_URL is correct
3. Ensure database and service are in same region

### Issue: "Database locked" or connection errors
**Fix:**
1. Check connection pool settings
2. Verify database isn't at connection limit
3. Restart the database if needed

### Issue: Data not persisting
**Fix:**
1. Verify you're using PostgreSQL (check DATABASE_URL)
2. Not using SQLite (check logs)
3. Database is linked correctly

## Connection String Format

Render provides PostgreSQL connection strings in this format:
```
postgres://user:password@host:port/dbname
```

Our code automatically converts `postgres://` to `postgresql://` (required by SQLAlchemy).

## Cost

**Free Tier:**
- 90 days free
- 1GB storage
- Suitable for personal projects

**After 90 days:**
- Database pauses automatically
- You can restart it manually (free)
- Or upgrade to paid plan for always-on

## Migration Checklist

- [ ] PostgreSQL database created in Render
- [ ] Database linked to web service
- [ ] DATABASE_URL environment variable set
- [ ] Service redeployed
- [ ] Database tables created (automatic on first start)
- [ ] Memos migrated (if needed)
- [ ] Verified data persists after sleep

## Next Steps

1. **Set up PostgreSQL** following steps above
2. **Verify connection** works
3. **Migrate existing data** (if any)
4. **Test persistence** by letting service sleep and wake it up
5. **Monitor** database usage in Render Dashboard

Your data will now persist across all deployments and sleeps! 🎉

