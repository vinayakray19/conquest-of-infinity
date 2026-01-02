# Render Deployment Guide

This guide explains how to deploy the Digital Diary backend to Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Your code pushed to a GitHub repository

## Quick Deploy

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**

2. **Connect to Render:**
   - Go to Render Dashboard
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Configure:**
   - Render will create the web service and database
   - Update `CORS_ORIGINS` in render.yaml to your frontend domain

4. **Deploy:**
   - Render will automatically deploy on every push to main branch

### Option 2: Manual Setup

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Choose a name (e.g., `digital-diary-db`)
   - Note the connection string

2. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** `digital-diary-api`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r backend/requirements.txt`
     - **Start Command:** `gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
     - **Root Directory:** (leave empty, or set to root if needed)

3. **Environment Variables:**
   - `DATABASE_URL` - From your PostgreSQL database (Internal Database URL)
   - `ENVIRONMENT` - `production`
   - `CORS_ORIGINS` - Your frontend domain (e.g., `https://your-frontend.vercel.app`)
   - `PORT` - Automatically set by Render (don't override)

## Database Setup

### Using PostgreSQL (Recommended for Production)

Render provides PostgreSQL databases. The app will automatically use the DATABASE_URL.

1. **Create Database on Render:**
   - New → PostgreSQL
   - Note the Internal Database URL

2. **Set Environment Variable:**
   - Add `DATABASE_URL` in your web service settings
   - Use the Internal Database URL from Render

3. **Run Migrations:**
   After first deployment, you can run migrations:
   ```bash
   # Via Render Shell or locally with DATABASE_URL set
   python3 scripts/migrate_memos.py
   ```

### Using SQLite (Development Only)

⚠️ **NOT RECOMMENDED FOR PRODUCTION** - SQLite files on Render are ephemeral and will be lost on redeploy.

**Important:** The `render.yaml` is configured to use PostgreSQL. If you see database errors, ensure:
1. The PostgreSQL database is created in Render
2. The `DATABASE_URL` environment variable is set correctly
3. The database connection string uses the **Internal Database URL** (not Public URL)

If you must use SQLite for testing (not recommended):
- The app will try to use `/tmp/memos.db` automatically
- Data will be lost on each deployment
- You may encounter permission errors

## Environment Variables

Set these in Render Dashboard → Your Service → Environment:

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://...` | PostgreSQL connection string (from Render database) |
| `ENVIRONMENT` | `production` | Environment name |
| `CORS_ORIGINS` | `https://your-frontend.com` | Allowed CORS origins (comma-separated) |
| `PORT` | (auto) | Automatically set by Render |

## Start Command

For Render deployment, use:
```bash
gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

## Build Command

```bash
pip install -r backend/requirements.txt
```

## Health Check

The service provides a health check endpoint:
- URL: `/health`
- Configure in Render: Health Check Path = `/health`

## Frontend Configuration

After deploying the backend, update your frontend:

1. **Update API URL in `frontend/js/config.js`:**
   ```javascript
   const API_BASE_URL = 'https://your-api.onrender.com';
   ```

2. **Or set via environment variable** and use build-time configuration

## Troubleshooting

### Service won't start
- Check logs in Render Dashboard
- Verify `DATABASE_URL` is set correctly
- Ensure `PORT` environment variable is available (set by Render automatically)

### Database connection errors
- Verify `DATABASE_URL` uses Internal Database URL (not Public URL)
- Check database is running
- Ensure network access is configured

### CORS errors
- Update `CORS_ORIGINS` in Render environment variables
- Include both `https://` and `http://` if testing locally
- For development, you can temporarily set to `*`

### Build failures
- Check `backend/requirements.txt` has all dependencies
- Verify Python version compatibility
- Check build logs for specific errors

## Monitoring

- **Logs:** Available in Render Dashboard → Your Service → Logs
- **Metrics:** Available in Render Dashboard
- **Health:** Check `/health` endpoint

## Custom Domain

1. Go to Render Dashboard → Your Service → Settings
2. Add Custom Domain
3. Update `CORS_ORIGINS` to include your custom domain

## CI/CD

Render automatically deploys on every push to your main branch. For manual deployments:
- Use "Manual Deploy" in Render Dashboard
- Or deploy specific branches/commits

## Cost

- **Free Tier:** Includes 750 hours/month of runtime
- **PostgreSQL:** Free tier available (limited)
- **Custom Domain:** Free SSL included

## Next Steps

1. Set up automatic backups for your database
2. Configure monitoring and alerts
3. Set up staging environment
4. Configure custom domain

