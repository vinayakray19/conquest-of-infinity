# Authentication Setup Guide

This guide explains how to set up and use the authentication system for adding posts.

## Features

- **Login Page**: Secure login with username/password
- **Profile Page**: Dashboard to add new posts/memos
- **JWT Authentication**: Token-based authentication
- **Protected Endpoints**: POST, PUT, DELETE endpoints require authentication

## Default Credentials

**⚠️ IMPORTANT: Change these in production!**

- Username: `admin`
- Password: `admin`

## Setting Custom Credentials

### For Local Development

Set environment variables:
```bash
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_secure_password
```

### For Render Production

1. Go to Render Dashboard → Your Service → Environment
2. Add environment variables:
   - `ADMIN_USERNAME`: Your username
   - `ADMIN_PASSWORD`: Your secure password
   - `SECRET_KEY`: A secure random string (min 32 characters)

Generate a secure SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Usage

### 1. Login

1. Go to `login.html` or click "Login" in the navigation
2. Enter username and password
3. You'll be redirected to the profile page after successful login

### 2. Add New Post

1. After logging in, you'll see the Profile page
2. Fill in the form:
   - **Title**: Post title
   - **Date**: Select the date
   - **Content**: Write your memo content
3. Click "Create Post"
4. The post will be added to the database and appear in the diary listing

### 3. Logout

Click the "Logout" button in the profile page.

## Protected Endpoints

The following API endpoints require authentication:
- `POST /api/memos` - Create new memo
- `PUT /api/memos/{number}` - Update memo
- `DELETE /api/memos/{number}` - Delete memo

Public endpoints (no authentication required):
- `GET /api/memos` - List all memos
- `GET /api/memos/{number}` - Get specific memo
- `GET /api/memos/nav/{number}` - Get navigation
- `GET /api/stats` - Get statistics

## Security Notes

1. **Change Default Credentials**: Never use default credentials in production
2. **Secure SECRET_KEY**: Use a long, random string for JWT signing
3. **HTTPS**: Always use HTTPS in production
4. **Token Storage**: Tokens are stored in localStorage (client-side)
5. **Token Expiry**: Tokens expire after 30 days

## Troubleshooting

### Login Fails
- Check that credentials match environment variables
- Check browser console for errors
- Verify API is accessible

### Cannot Create Posts
- Make sure you're logged in
- Check that token is stored (localStorage in browser dev tools)
- Verify authentication headers are sent with requests

### Token Expired
- Log out and log in again
- Token will be refreshed

## API Endpoints

### Login
```bash
POST /api/login
Body: { "username": "admin", "password": "admin" }
Response: { "access_token": "...", "token_type": "bearer", "username": "admin" }
```

### Check Auth Status
```bash
GET /api/me
Headers: Authorization: Bearer <token>
Response: { "username": "admin", "authenticated": true }
```

### Logout
```bash
POST /api/logout
Headers: Authorization: Bearer <token>
Response: { "message": "Logged out successfully" }
```

