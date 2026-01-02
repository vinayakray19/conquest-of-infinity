# GitHub Pages Setup Guide

This guide explains how to deploy the frontend to GitHub Pages.

## Overview

The frontend files are located in the root directory for easy GitHub Pages hosting:
- `index.html` - Home page
- `diary.html` - Diary listing page
- `memo.html` - Memo detail page
- `css/` - Stylesheets
- `js/` - JavaScript modules

## Setup Steps

### 1. Push to GitHub

Make sure your code is pushed to a GitHub repository:
```bash
git add .
git commit -m "Setup for GitHub Pages"
git push origin main
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - **Branch:** `main` (or your default branch)
   - **Folder:** `/ (root)`
4. Click **Save**

### 3. Configure API URL

Update the API URL in `js/config.js` for production:

```javascript
// In js/config.js, update this line:
API_BASE_URL = window.API_BASE_URL || 'https://your-api.onrender.com';
```

Replace `https://your-api.onrender.com` with your actual Render API URL.

**Alternative:** You can override the API URL using HTML meta tag or by setting it before the script loads:
```html
<script>
  window.API_BASE_URL = 'https://your-api.onrender.com';
</script>
<script src="js/config.js"></script>
```

### 4. Update CORS Settings

Make sure your backend API (on Render) allows requests from your GitHub Pages domain:

1. Go to Render Dashboard → Your Service → Environment
2. Set `CORS_ORIGINS` to include your GitHub Pages URL:
   ```
   https://yourusername.github.io,https://yourusername.github.io/repository-name
   ```

### 5. Access Your Site

After GitHub Pages is enabled, your site will be available at:
```
https://yourusername.github.io/repository-name/
```

Or if you're using a custom domain:
```
https://your-custom-domain.com
```

## File Structure

```
.
├── index.html          # Home page (GitHub Pages entry point)
├── diary.html          # Diary listing
├── memo.html           # Memo detail page
├── css/
│   └── styles.css      # Styles
└── js/
    ├── config.js       # Configuration (update API URL here)
    ├── api.js          # API client
    ├── utils.js        # Utilities
    ├── diary.js        # Diary page logic
    └── memo.js         # Memo page logic
```

## Custom Domain (Optional)

1. In your repository Settings → Pages
2. Under **Custom domain**, enter your domain
3. Follow GitHub's instructions to configure DNS
4. Update `CORS_ORIGINS` in your Render API to include your custom domain

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console:
- Make sure `CORS_ORIGINS` in Render includes your GitHub Pages URL
- Check that the API URL in `js/config.js` is correct
- Verify the API server is running

### Pages Not Loading

- Check that GitHub Pages is enabled and building
- Verify file paths are correct (relative paths, no `/frontend/` prefix)
- Check browser console for JavaScript errors

### API Not Connecting

- Verify the API URL in `js/config.js` is correct
- Make sure your Render API is running
- Check Render logs for connection errors
- Test API directly: `https://your-api.onrender.com/health`

## Testing Locally

Before pushing to GitHub, test locally:
```bash
# Serve the files locally
python3 -m http.server 8000

# Then open http://localhost:8000/diary.html
```

## CI/CD

GitHub Pages automatically rebuilds when you push to the main branch. No additional configuration needed!

