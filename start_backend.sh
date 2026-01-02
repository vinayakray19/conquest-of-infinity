#!/bin/bash
# Start backend server from project root

cd "$(dirname "$0")"

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing backend dependencies..."
    pip3 install -r backend/requirements.txt
fi

# Set default credentials for testing (can be overridden)
export ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
export ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin}
export SECRET_KEY=${SECRET_KEY:-local-testing-secret-key-change-in-production-32chars}

# Use port from environment or default to 8000
PORT=${API_PORT:-8000}

echo "🚀 Starting backend server..."
echo "   API: http://localhost:$PORT"
echo "   Docs: http://localhost:$PORT/docs"
echo "   Username: $ADMIN_USERNAME"
echo "   Press Ctrl+C to stop"
echo ""

# Start with uvicorn (handles Python path correctly)
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port $PORT
