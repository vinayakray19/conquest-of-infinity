#!/usr/bin/env python3
"""
Check the status of the Render API server and database.
"""
import requests
import sys

API_BASE_URL = "https://conquest-of-infinity.onrender.com"

def check_status():
    print(f"Checking Render API: {API_BASE_URL}\n")
    
    try:
        # Check health
        print("1. Health Check...")
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Server is healthy: {response.json()}\n")
        else:
            print(f"   ❌ Health check failed: {response.status_code}\n")
            return
        
        # Check stats
        print("2. Database Stats...")
        response = requests.get(f"{API_BASE_URL}/api/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total memos: {stats.get('total_memos', 0)}")
            print(f"   Oldest date: {stats.get('oldest_date', 'N/A')}")
            print(f"   Newest date: {stats.get('newest_date', 'N/A')}")
            print(f"   First memo: #{stats.get('first_memo_number', 'N/A')}")
            print(f"   Last memo: #{stats.get('last_memo_number', 'N/A')}\n")
        else:
            print(f"   ❌ Failed to get stats: {response.status_code}\n")
        
        # Check memos
        print("3. Checking memos...")
        response = requests.get(f"{API_BASE_URL}/api/memos", timeout=10)
        if response.status_code == 200:
            memos = response.json()
            print(f"   Found {len(memos)} memos")
            if memos:
                print(f"\n   Sample memos:")
                for memo in memos[:5]:  # Show first 5
                    print(f"   - Memo #{memo['memo_number']}: {memo['title']}")
                if len(memos) > 5:
                    print(f"   ... and {len(memos) - 5} more")
            else:
                print("   ⚠️  No memos found in database!")
                print("\n   To add memos:")
                print("   1. Use: python3 scripts/add_memo_api.py")
                print("   2. Or migrate from backup: python3 scripts/migrate_to_render.py")
            print()
        else:
            print(f"   ❌ Failed to get memos: {response.status_code}\n")
        
    except requests.exceptions.Timeout:
        print("❌ Connection timeout! The server might be sleeping.")
        print("   Render free tier services sleep after inactivity.")
        print("   Try again in a few moments - the first request may take time to wake it up.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Connection error! Check if the server is running.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_status()

