#!/usr/bin/env python3
"""
Quick test script to verify the API is working.
"""
import requests
import sys

API_BASE_URL = "http://localhost:8001"

def test_api():
    print(f"Testing API at {API_BASE_URL}\n")
    
    try:
        # Test root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{API_BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        
        # Test getting all memos
        print("2. Testing GET /api/memos...")
        response = requests.get(f"{API_BASE_URL}/api/memos")
        print(f"   Status: {response.status_code}")
        memos = response.json()
        print(f"   Found {len(memos)} memos")
        if memos:
            print(f"   First memo: #{memos[0]['memo_number']} - {memos[0]['title']}\n")
        else:
            print("   No memos found in database!\n")
            return
        
        # Test getting a specific memo
        if memos:
            memo_num = memos[0]['memo_number']
            print(f"3. Testing GET /api/memos/{memo_num}...")
            response = requests.get(f"{API_BASE_URL}/api/memos/{memo_num}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                memo = response.json()
                print(f"   Title: {memo['title']}")
                print(f"   Date: {memo['date']}")
                print(f"   Content length: {len(memo.get('content', ''))} characters")
                print(f"   Content preview: {memo.get('content', '')[:100]}...\n")
            
            # Test navigation
            print(f"4. Testing GET /api/memos/nav/{memo_num}...")
            response = requests.get(f"{API_BASE_URL}/api/memos/nav/{memo_num}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                nav = response.json()
                print(f"   Current: #{nav['current']['memo_number']}")
                print(f"   Previous: #{nav['previous']['memo_number'] if nav['previous'] else 'None'}")
                print(f"   Next: #{nav['next']['memo_number'] if nav['next'] else 'None'}\n")
        
        print("✅ All tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error! Make sure the API server is running:")
        print(f"   python3 api.py")
        print(f"   or: uvicorn api:app --reload --port 8001")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_api()

