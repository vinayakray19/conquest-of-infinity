#!/bin/bash
# Test login with current credentials

echo "🔐 Testing Login..."
echo ""

# First check if server is running (try both ports)
echo "1. Checking if FastAPI server is running..."
# Try port 8001 first (most common), then 8000
health_check=$(curl -s http://127.0.0.1:8001/health 2>&1)
PORT=8001
if ! echo "$health_check" | grep -q "healthy"; then
    health_check=$(curl -s http://127.0.0.1:8000/health 2>&1)
    PORT=8000
fi
if echo "$health_check" | grep -q "healthy"; then
    echo "   ✅ FastAPI server is running"
else
    echo "   ❌ FastAPI server is NOT running or wrong port!"
    echo "   Response: $health_check"
    echo ""
    echo "   💡 Start the server with:"
    echo "      export ADMIN_USERNAME=your_username"
    echo "      export ADMIN_PASSWORD=your_password"
    echo "      python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
    exit 1
fi
echo ""

echo "2. If you set ADMIN_USERNAME and ADMIN_PASSWORD, use those."
echo "   Otherwise, default is: admin / admin"
echo ""

read -p "Enter username: " username
read -sp "Enter password: " password
echo ""
echo ""

# Test login
echo "3. Attempting login on port $PORT..."
response=$(curl -s -X POST http://127.0.0.1:$PORT/api/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$username\",\"password\":\"$password\"}" 2>&1)

if echo "$response" | grep -q "access_token"; then
    echo "✅ Login successful!"
    echo ""
    echo "Token received:"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo "❌ Login failed!"
    echo ""
    echo "Response:"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    echo ""
    echo "💡 Troubleshooting:"
    echo "   1. Check if server is running: curl http://127.0.0.1:$PORT/health"
    echo "   2. Verify credentials match what you set in environment"
    echo "   3. Try default: admin / admin (if no env vars set)"
    echo "   4. Check server logs for errors"
fi

