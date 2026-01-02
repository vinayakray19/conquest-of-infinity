#!/bin/bash
# Quick test script for local development on Mac

echo "🚀 Starting Local Testing Setup"
echo ""

# Check if backend dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing backend dependencies..."
    pip3 install -r backend/requirements.txt
    echo ""
fi

# Set default credentials for testing
export ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
export ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin}
export SECRET_KEY=${SECRET_KEY:-local-testing-secret-key-change-in-production}

echo "✅ Configuration:"
echo "   Username: $ADMIN_USERNAME"
echo "   API will run on: http://localhost:8001"
echo ""

# Start backend server (from project root)
echo "🔧 Starting backend server..."
echo "   Press Ctrl+C to stop"
echo ""
cd "$(dirname "$0")"
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001

