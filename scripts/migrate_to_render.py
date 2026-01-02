#!/usr/bin/env python3
"""
Migrate memos from local backup archive to Render API.
This script reads from the backup archive and adds memos via the Render API.
"""
import os
import sys
import tarfile
import tempfile
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import requests

API_BASE_URL = os.getenv('API_BASE_URL', 'https://conquest-of-infinity.onrender.com')

# Find backup archive
BACKUP_PATTERN = "memos_backup_*.tar.gz"
BACKUP_DIR = Path(__file__).resolve().parent.parent

def find_backup():
    """Find the memo backup archive."""
    backups = list(BACKUP_DIR.glob(BACKUP_PATTERN))
    if not backups:
        print(f"❌ No backup archive found matching {BACKUP_PATTERN}")
        print(f"   Searched in: {BACKUP_DIR}")
        return None
    
    # Get the most recent backup
    backup = max(backups, key=lambda p: p.stat().st_mtime)
    print(f"📦 Found backup: {backup.name}")
    return backup

def extract_content_from_html(html_content):
    """Extract title, date, and content from HTML memo file."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title_elem = soup.find('h2')
    title = title_elem.get_text().strip() if title_elem else "Untitled"
    
    # Extract date
    date_elem = soup.find('p', class_='article-date')
    date_str = date_elem.get_text().strip() if date_elem else None
    
    if date_str:
        try:
            # Parse date: "December 30, 2025"
            date = datetime.strptime(date_str, "%B %d, %Y")
        except ValueError:
            print(f"   ⚠️  Could not parse date '{date_str}', using current date")
            date = datetime.now()
    else:
        print(f"   ⚠️  No date found, using current date")
        date = datetime.now()
    
    # Extract content
    content_div = soup.find('div', class_='article-content')
    if content_div:
        content_parts = []
        for p in content_div.find_all('p'):
            inner_html = p.decode_contents()
            if inner_html.strip():
                content_parts.append(inner_html)
        content = '\n\n'.join(content_parts)
        
        if not content.strip():
            content = content_div.get_text(separator='\n', strip=True)
        
        import re
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = content.strip()
    else:
        content = ""
    
    return title, date, content

def add_memo_to_api(memo_num, title, date, content):
    """Add a memo to the Render API."""
    url = f"{API_BASE_URL}/api/memos"
    payload = {
        "memo_number": memo_num,
        "title": title,
        "content": content,
        "date": date.isoformat()
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code in (200, 201):  # 200 OK or 201 Created
            return True, None
        elif response.status_code == 409 or "already exists" in response.text.lower() or "duplicate" in response.text.lower():
            return False, "already exists"
        else:
            return False, f"Status {response.status_code}: {response.text[:100]}"
    except requests.exceptions.Timeout:
        return False, "timeout - server might be sleeping"
    except Exception as e:
        return False, str(e)

def migrate_from_backup():
    """Migrate memos from backup archive to Render API."""
    print(f"🚀 Starting migration to Render API: {API_BASE_URL}\n")
    
    # Find backup
    backup = find_backup()
    if not backup:
        return
    
    # Check API connection (with retry for sleeping services)
    print("\n1. Checking API connection...")
    print("   (First request may take 30-60s if server is sleeping...)")
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=60)
            if response.status_code == 200:
                print(f"   ✅ API is reachable")
                break
            else:
                print(f"   ⚠️  Health check returned {response.status_code}, retrying...")
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10
                print(f"   ⏳ Server might be sleeping, waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                import time
                time.sleep(wait_time)
            else:
                print(f"   ❌ Connection timeout after {max_retries} attempts")
                print(f"   The Render service might be sleeping. Please try again in a moment.")
                return
        except Exception as e:
            print(f"   ❌ Cannot connect to API: {e}")
            print(f"   Make sure the Render service is running")
            return
    else:
        print(f"   ❌ Failed to connect after {max_retries} attempts")
        return
    
    # Check existing memos
    print("\n2. Checking existing memos...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            existing_count = stats.get('total_memos', 0)
            print(f"   Found {existing_count} existing memos in database")
    except Exception as e:
        print(f"   ⚠️  Could not check existing memos: {e}")
    
    # Extract and process backup
    print("\n3. Processing backup archive...")
    with tempfile.TemporaryDirectory() as temp_dir:
        with tarfile.open(backup, 'r:gz') as tar:
            tar.extractall(temp_dir)
        
        memos_dir = Path(temp_dir) / "memos"
        if not memos_dir.exists():
            print(f"   ❌ memos/ directory not found in archive")
            return
        
        # Find all memo files
        memo_files = []
        for filename in sorted(memos_dir.glob("memo-*.html")):
            import re
            match = re.match(r'memo-(\d+)\.html', filename.name)
            if match:
                memo_num = int(match.group(1))
                memo_files.append((memo_num, filename))
        
        memo_files.sort(key=lambda x: x[0])
        print(f"   Found {len(memo_files)} memo files\n")
        
        if not memo_files:
            print("   ⚠️  No memo files found in archive")
            return
        
        # Migrate each memo
        migrated = 0
        skipped = 0
        failed = 0
        
        print("4. Migrating memos...\n")
        for memo_num, filepath in memo_files:
            try:
                # Read and parse HTML
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                title, date, content = extract_content_from_html(html_content)
                
                # Add to API
                success, error = add_memo_to_api(memo_num, title, date, content)
                
                if success:
                    print(f"   ✅ Memo #{memo_num}: {title[:50]}...")
                    migrated += 1
                elif "already exists" in str(error).lower() or "duplicate" in str(error).lower():
                    print(f"   ⏭️  Memo #{memo_num}: Already exists, skipping...")
                    skipped += 1
                else:
                    print(f"   ❌ Memo #{memo_num}: Failed - {error}")
                    failed += 1
                    
            except Exception as e:
                print(f"   ❌ Memo #{memo_num}: Error - {e}")
                failed += 1
        
        # Summary
        print(f"\n📊 Migration Summary:")
        print(f"   ✅ Migrated: {migrated}")
        print(f"   ⏭️  Skipped: {skipped}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📦 Total: {len(memo_files)}")

if __name__ == "__main__":
    migrate_from_backup()

