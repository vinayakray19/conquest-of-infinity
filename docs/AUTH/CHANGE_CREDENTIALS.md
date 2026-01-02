# How Authentication Works & Changing Credentials

## How It Works

The authentication system uses environment variables with defaults:

**Location:** `backend/config.py`
```python
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')  # Default: 'admin'
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')  # Default: 'admin'
```

**Authentication Check:** `backend/api/routes/auth.py`
- When you login, it compares your input with `ADMIN_USERNAME` and `ADMIN_PASSWORD`
- If they match, you get a JWT token
- If not, login fails

## How to Change Credentials

### Option 1: Environment Variables (Recommended)

#### For Local Development (Mac/Linux)

**Temporary (current terminal session):**
```bash
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_secure_password
export SECRET_KEY=your-secret-key-min-32-characters-long
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

**Permanent (add to your shell profile):**
```bash
# Edit your ~/.zshrc file (or ~/.bash_profile for bash)
nano ~/.zshrc

# Add these lines:
export ADMIN_USERNAME=your_username
export ADMIN_PASSWORD=your_secure_password
export SECRET_KEY=your-secret-key-min-32-characters-long

# Reload shell
source ~/.zshrc
```

#### Using a `.env` File (Easier)

1. Create `.env` file in project root:
```bash
cd /Users/vinayakray/Codebase/vscode/Explain/conquest-of-infinity
cat > .env << EOF
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
EOF
```

2. Load it before starting server:
```bash
export $(cat .env | xargs)
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

#### For Render Production

1. Go to **Render Dashboard** → **Your Service** → **Environment**
2. Click **"Add Environment Variable"**
3. Add these variables:
   - `ADMIN_USERNAME`: Your username
   - `ADMIN_PASSWORD`: Your secure password
   - `SECRET_KEY`: Generate with: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

4. **Redeploy** your service for changes to take effect

### Option 2: Direct Code Edit (Not Recommended)

**⚠️ Warning:** Never commit credentials to git!

Edit `backend/config.py`:
```python
ADMIN_USERNAME = 'your_username'
ADMIN_PASSWORD = 'your_secure_password'
```

**Better:** Use environment variables so credentials aren't in code!

## Generate Secure SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

This generates a secure random key like:
```
xK9pL2mN8qR4tV6wY0zA1bC3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5z
```

## Quick Setup Script

Create `set_credentials.sh`:
```bash
#!/bin/bash
read -p "Enter username: " username
read -sp "Enter password: " password
echo ""
read -p "Generate SECRET_KEY? (y/n): " gen_key

if [ "$gen_key" = "y" ]; then
    secret_key=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo "SECRET_KEY=$secret_key" >> .env
fi

echo "ADMIN_USERNAME=$username" >> .env
echo "ADMIN_PASSWORD=$password" >> .env

echo "✅ Credentials saved to .env"
echo "📝 Start server with: export \$(cat .env | xargs) && python3 -m uvicorn backend.main:app --reload"
```

Make it executable:
```bash
chmod +x set_credentials.sh
./set_credentials.sh
```

## Verify Credentials

After setting, verify they're loaded:
```python
python3 -c "import os; print('Username:', os.getenv('ADMIN_USERNAME', 'admin')); print('Password set:', 'Yes' if os.getenv('ADMIN_PASSWORD') else 'No')"
```

## Security Best Practices

1. ✅ **Use environment variables** - Never hardcode credentials
2. ✅ **Use strong passwords** - At least 12 characters, mix of letters/numbers/symbols
3. ✅ **Generate secure SECRET_KEY** - Use the secrets module
4. ✅ **Don't commit .env** - Add `.env` to `.gitignore`
5. ✅ **Change defaults** - Always change from admin/admin in production

## Current Defaults

- **Username:** `admin`
- **Password:** `admin`
- **SECRET_KEY:** `your-secret-key-change-in-production-min-32-chars`

**⚠️ Change these before deploying to production!**

