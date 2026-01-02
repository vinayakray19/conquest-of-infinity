#!/usr/bin/env python3
"""
Migration script to import existing HTML memo files into the database.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime
from bs4 import BeautifulSoup
from backend.api.models import Memo
from backend.api.database import SessionLocal, init_db

MEMOS_DIR = Path(__file__).resolve().parent.parent / "memos"

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
            print(f"Warning: Could not parse date '{date_str}', using current date")
            date = datetime.now()
    else:
        print(f"Warning: No date found, using current date")
        date = datetime.now()
    
    # Extract content
    content_div = soup.find('div', class_='article-content')
    if content_div:
        # Get all paragraph content, preserving HTML structure
        content_parts = []
        for p in content_div.find_all('p'):
            # Get the HTML content of the paragraph (preserves <br> tags, etc.)
            inner_html = p.decode_contents()
            if inner_html.strip():
                content_parts.append(inner_html)
        
        # Join paragraphs with double newlines
        content = '\n\n'.join(content_parts)
        
        # If no content found, try getting all text
        if not content.strip():
            content = content_div.get_text(separator='\n', strip=True)
        
        # Clean up extra whitespace
        import re
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = content.strip()
    else:
        content = ""
    
    return title, date, content

def migrate_memos():
    """Migrate all HTML memo files to the database."""
    print("Starting migration of HTML memos to database...\n")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Get all memo files
        memo_files = []
        if MEMOS_DIR.exists():
            for filename in sorted(MEMOS_DIR.iterdir()):
                if filename.name.startswith("memo-") and filename.name.endswith(".html"):
                    import re
                    match = re.match(r'memo-(\d+)\.html', filename.name)
                    if match:
                        memo_num = int(match.group(1))
                        memo_files.append((memo_num, filename))
        
        memo_files.sort(key=lambda x: x[0])
        
        print(f"Found {len(memo_files)} memo files to migrate\n")
        
        migrated = 0
        skipped = 0
        
        for memo_num, filepath in memo_files:
            # Check if memo already exists
            existing = db.query(Memo).filter(Memo.memo_number == memo_num).first()
            if existing:
                print(f"  ⚠️  Memo #{memo_num} already exists in database, skipping...")
                skipped += 1
                continue
            
            # Read and parse HTML file
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                title, date, content = extract_content_from_html(html_content)
                
                # Create memo in database
                memo = Memo(
                    memo_number=memo_num,
                    title=title,
                    content=content,
                    date=date
                )
                
                db.add(memo)
                db.commit()
                
                print(f"  ✓ Migrated Memo #{memo_num}: {title[:50]}...")
                migrated += 1
                
            except Exception as e:
                print(f"  ✗ Error migrating memo-{memo_num}.html: {e}")
                db.rollback()
                continue
        
        print(f"\n✅ Migration complete!")
        print(f"   Migrated: {migrated}")
        print(f"   Skipped: {skipped}")
        print(f"   Total: {len(memo_files)}")
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate_memos()
