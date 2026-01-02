# Scripts Directory

This directory contains utility scripts organized by purpose.

## Directory Structure

```
scripts/
├── setup/              # Setup and development scripts
│   ├── start_backend.sh       # Start backend server
│   ├── test_local.sh          # Test local setup
│   ├── test_login.sh          # Test authentication
│   └── migrate_now.sh         # Quick PostgreSQL migration helper
│
├── migrations/         # Database migration scripts
│   ├── migrate_memos.py              # Migrate HTML memos to database
│   ├── migrate_to_postgresql.py      # Migrate from SQLite to PostgreSQL
│   └── migrate_to_render.py          # Migrate to Render deployment
│
├── utils/              # Utility scripts
│   ├── test_api.py            # Test API connectivity
│   └── check_render_status.py # Check Render deployment status
│
├── add_memo_api.py     # Add new memo via API
└── requirements.txt    # Python dependencies for scripts
```

## Usage

### Setup Scripts

```bash
# Start backend server
./scripts/setup/start_backend.sh

# Test local setup
./scripts/setup/test_local.sh

# Test login
./scripts/setup/test_login.sh

# Quick migration to PostgreSQL
export DATABASE_URL="postgres://..."
./scripts/setup/migrate_now.sh
```

### Migration Scripts

```bash
# Migrate HTML memos to database
python3 scripts/migrations/migrate_memos.py

# Migrate from SQLite to PostgreSQL
export DATABASE_URL="postgres://..."
python3 scripts/migrations/migrate_to_postgresql.py

# Migrate to Render
export DATABASE_URL="postgres://..."
python3 scripts/migrations/migrate_to_render.py
```

### Utility Scripts

```bash
# Test API
python3 scripts/utils/test_api.py

# Check Render status
python3 scripts/utils/check_render_status.py
```

### Add Memo

```bash
# Interactive mode
python3 scripts/add_memo_api.py

# Command line
python3 scripts/add_memo_api.py --title "Title" --date "2025-01-15" --content "Content"
```

## Requirements

Install script dependencies:
```bash
pip install -r scripts/requirements.txt
```

