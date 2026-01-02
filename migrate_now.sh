#!/bin/bash
# Quick migration script to PostgreSQL on Render

echo "🚀 PostgreSQL Migration Helper"
echo "================================"
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not set!"
    echo ""
    echo "📋 To get your DATABASE_URL:"
    echo "   1. Go to Render Dashboard → Your PostgreSQL Database"
    echo "   2. Click 'Connect' tab"
    echo "   3. Copy 'External Connection String' (for local migration)"
    echo ""
    echo "   Then run:"
    echo "   export DATABASE_URL='postgres://user:pass@host:port/dbname'"
    echo "   ./migrate_now.sh"
    exit 1
fi

echo "✅ DATABASE_URL is set"
echo ""

# Check if local database exists
if [ ! -f "memos.db" ]; then
    echo "❌ Local memos.db not found!"
    echo "   Make sure you're in the project root directory"
    exit 1
fi

echo "✅ Found local memos.db"
echo ""

# Check if Python dependencies are installed
echo "📦 Checking dependencies..."
python3 -c "import sqlalchemy, psycopg" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required packages..."
    pip install sqlalchemy psycopg[binary] --quiet
fi

echo ""
echo "🔄 Starting migration..."
echo ""

# Run migration
python3 scripts/migrate_to_postgresql.py

echo ""
echo "✅ Migration script completed!"
echo ""
echo "📋 Next steps:"
echo "   1. Check the migration summary above"
echo "   2. Verify data in Render Dashboard or via API"
echo "   3. Test your application"

