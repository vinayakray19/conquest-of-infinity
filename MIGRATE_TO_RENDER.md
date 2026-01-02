# How to Add Memos to Render Server

Your Render server is currently empty. Here's how to populate it with memos.

## Option 1: Migrate from Backup Archive (Recommended)

If you have a backup archive with your memos:

```bash
# Migrate all memos from backup to Render API
python3 scripts/migrate_to_render.py
```

This script will:
- Find your backup archive (`memos_backup_*.tar.gz`)
- Extract all memo HTML files
- Parse and migrate them to the Render API
- Skip duplicates if they already exist

**Note:** The first request to Render may take time if the server is sleeping (free tier).

## Option 2: Add Memos One by One via API

Use the API script to add memos to Render:

```bash
# Set the API URL to Render
export API_BASE_URL=https://conquest-of-infinity.onrender.com

# Interactive mode
python3 scripts/add_memo_api.py

# Or from command line
python3 scripts/add_memo_api.py \
  --title "My Memo Title" \
  --date "January 2, 2026" \
  --content "Memo content here"

# Or from WordPress URL
python3 scripts/add_memo_api.py \
  --url "https://example.com/post" \
  --title "Title" \
  --date "January 2, 2026"
```

## Option 3: Check Status First

Check the current status of your Render server:

```bash
python3 scripts/check_render_status.py
```

This will show:
- Server health
- Number of memos in database
- Sample memo list

## Quick Check via Browser/curl

You can also check directly:

```bash
# Check stats
curl https://conquest-of-infinity.onrender.com/api/stats

# List all memos
curl https://conquest-of-infinity.onrender.com/api/memos

# Health check
curl https://conquest-of-infinity.onrender.com/health
```

## Troubleshooting

### Server is Sleeping
If you get timeout errors, the Render free tier service might be sleeping. 
- Just wait 30-60 seconds and try again
- The first request will wake it up

### Migration Fails
- Make sure you have the backup archive in the project root
- Check that the API is reachable: `python3 scripts/check_render_status.py`
- Verify your Render service is running in the dashboard

### Adding Memos Fails
- Make sure `API_BASE_URL` environment variable is set correctly
- Check Render logs for any errors
- Verify the API is healthy: `curl https://conquest-of-infinity.onrender.com/health`

## After Migration

Once memos are added:
1. Refresh your GitHub Pages site
2. The memos should now appear in the diary listing
3. You can verify via: `python3 scripts/check_render_status.py`

