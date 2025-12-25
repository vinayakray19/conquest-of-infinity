#!/usr/bin/env python3
"""
Script to add a new memo to the blog.

Usage:
    python3 add_memo.py --title "Title" --date "Month Day, Year" --content "Content here"
    python3 add_memo.py --url "https://example.com/post" --title "Title" --date "Date"
    
Or run interactively:
    python3 add_memo.py
"""

import os
import re
import argparse
from datetime import datetime
from urllib.request import urlopen, Request
from html import unescape

MEMOS_DIR = "memos"
CSS_PATH = "../css/styles.css"
DIARY_FILE = "diary.html"

def get_next_memo_number():
    """Find the highest memo number and return the next one."""
    max_num = 0
    if os.path.exists(MEMOS_DIR):
        for filename in os.listdir(MEMOS_DIR):
            match = re.match(r'memo-(\d+)\.html', filename)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)
    return max_num + 1

def create_memo_template(memo_num, title, date, content):
    """Create the HTML template for a memo page."""
    # Determine previous and next memo numbers
    prev_num = memo_num - 1 if memo_num > 1 else None
    next_num = memo_num + 1 if os.path.exists(f"{MEMOS_DIR}/memo-{memo_num + 1}.html") else None
    
    # Build navigation links
    nav_links = []
    if prev_num:
        nav_links.append(f'                    <a href="memo-{prev_num}.html" class="nav-button prev">← Previous Memo</a>')
    else:
        nav_links.append('                    <span></span>')
    
    if next_num:
        nav_links.append(f'                    <a href="memo-{next_num}.html" class="nav-button next">Next Memo →</a>')
    
    nav_html = '\n'.join(nav_links)
    
    # Escape HTML in title for the page title
    title_escaped = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memo #{memo_num}: {title_escaped} - A Digital Diary</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{CSS_PATH}">
</head>
<body>
    <div class="spring-background">
        <div class="spring-trees"></div>
        <div class="spring-leaves"></div>
    </div>
    <nav>
        <div class="nav-container">
            <a href="../index.html" class="nav-link">Home</a>
            <a href="../diary.html" class="nav-link active">Diary</a>
        </div>
    </nav>

    <main class="container">
        <div class="content">
            <div class="memo-header">
                <a href="../diary.html" class="back-to-list-link">← Back to Diary List</a>
                <h1>Memo #{memo_num}</h1>
            </div>

            <article class="diary-article">
                <h2>{title}</h2>
                <p class="article-date">{date}</p>
                <div class="article-content">
{content}
                </div>
                <div class="article-navigation">
{nav_html}
                </div>
            </article>
        </div>
    </main>
</body>
</html>'''
    
    return template

def update_adjacent_memos(memo_num):
    """Update navigation links in adjacent memo files."""
    # Update previous memo's "Next" link
    prev_num = memo_num - 1
    if prev_num >= 1:
        prev_file = f"{MEMOS_DIR}/memo-{prev_num}.html"
        if os.path.exists(prev_file):
            with open(prev_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if next link already exists and update it, or add it
            if f'href="memo-{memo_num}.html"' in content:
                # Already correct
                pass
            else:
                # Find and replace existing next link, or add new one
                # Pattern to find the navigation section
                nav_pattern = r'(<div class="article-navigation">\s*\n)(.*?)(\s*</div>)'
                match = re.search(nav_pattern, content, re.DOTALL)
                
                if match:
                    nav_start = match.group(1)
                    nav_content = match.group(2)
                    nav_end = match.group(3)
                    
                    # Remove old next link if exists
                    nav_content = re.sub(r'\s*<a href="memo-\d+\.html" class="nav-button next">Next Memo →</a>\s*\n?', '', nav_content)
                    
                    # Add new next link
                    nav_content = nav_content.rstrip() + f'\n                    <a href="memo-{memo_num}.html" class="nav-button next">Next Memo →</a>'
                    
                    # Reconstruct navigation
                    new_nav = nav_start + nav_content + nav_end
                    content = content[:match.start()] + new_nav + content[match.end():]
            
            with open(prev_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated memo-{prev_num}.html navigation")
    
    # Update next memo's "Previous" link
    next_num = memo_num + 1
    next_file = f"{MEMOS_DIR}/memo-{next_num}.html"
    if os.path.exists(next_file):
        with open(next_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace previous link - find the exact pattern
        content = re.sub(
            r'href="memo-\d+\.html" class="nav-button prev"',
            f'href="memo-{memo_num}.html" class="nav-button prev"',
            content
        )
        
        with open(next_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated memo-{next_num}.html navigation")

def add_to_diary_listing(memo_num, title, date):
    """Add the new memo entry to diary.html."""
    with open(DIARY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create the new entry HTML
    new_entry = f'''                <div class="entry">
                    <a href="memos/memo-{memo_num}.html" class="entry-link">
                        <span class="entry-number">Memo #{memo_num}.</span>
                        <span class="entry-title">{title}.</span>
                        <span class="entry-date">{date}</span>
                    </a>
                </div>
'''
    
    # Find the diary entries section and insert at the beginning (newest first)
    # Look for the opening div tag followed by the first entry
    pattern = r'(<div id="diary-entries" class="diary-entries">\s*\n)'
    replacement = f'\\1{new_entry}'
    content = re.sub(pattern, replacement, content)
    
    with open(DIARY_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Added entry to {DIARY_FILE}")

def fetch_content_from_url(url):
    """Fetch and extract content from a WordPress blog URL."""
    try:
        # Create a request with a user agent to avoid blocking
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        with urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        # Extract content from WordPress post
        # Look for the main content area (entry-content, post-content, etc.)
        content_patterns = [
            r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*post-content[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*wp-block-post-content[^"]*"[^>]*>(.*?)</div>',
            r'<article[^>]*class="[^"]*post[^"]*"[^>]*>(.*?)</article>',
            r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
        ]
        
        extracted_content = None
        for pattern in content_patterns:
            match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if match:
                extracted_content = match.group(1)
                break
        
        if not extracted_content:
            # Fallback: try to find main content between common WordPress tags
            # Look for content after h1 title and before navigation/footer
            main_match = re.search(r'<h1[^>]*>.*?</h1>(.*?)(?:<nav|</nav>|<footer|</footer>|</article|</main|<!--\s*Post navigation)', html_content, re.DOTALL | re.IGNORECASE)
            if main_match:
                extracted_content = main_match.group(1)
        
        if not extracted_content:
            raise ValueError("Could not extract content from URL. The page structure may not be recognized.")
        
        # Clean up the extracted content
        # Remove script and style tags
        extracted_content = re.sub(r'<script[^>]*>.*?</script>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<style[^>]*>.*?</style>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove WordPress-specific elements and widgets
        extracted_content = re.sub(r'<div[^>]*class="[^"]*wp-block[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<div[^>]*class="[^"]*widget[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<!--.*?-->', '', extracted_content, flags=re.DOTALL)
        
        # Remove social sharing buttons and related content
        extracted_content = re.sub(r'<div[^>]*class="[^"]*share[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<div[^>]*class="[^"]*post-navigation[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<div[^>]*class="[^"]*comments[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up extra whitespace
        extracted_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', extracted_content)
        extracted_content = extracted_content.strip()
        
        # Try to extract title if not provided
        title = None
        # Try h1 with entry-title class first
        title_match = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', html_content, re.DOTALL | re.IGNORECASE)
        if not title_match:
            # Try any h1 in the main content
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL | re.IGNORECASE)
        if not title_match:
            # Fallback to page title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.DOTALL | re.IGNORECASE)
        
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            title = unescape(title)  # Decode HTML entities
            # Clean up WordPress title format (remove site name and separators)
            title = re.sub(r'\s*[-|–—]\s*.*$', '', title).strip()
            title = re.sub(r'\s*\|.*$', '', title).strip()
        
        # Try to extract date if not provided
        date_match = re.search(r'<time[^>]*datetime="([^"]*)"', html_content, re.IGNORECASE)
        if not date_match:
            date_match = re.search(r'class="[^"]*published[^"]*"[^>]*>([^<]*)', html_content, re.IGNORECASE)
        
        date = None
        if date_match:
            date_str = date_match.group(1).strip()
            # Try to parse and format the date
            try:
                # Handle ISO format dates
                if 'T' in date_str:
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    date = dt.strftime('%B %d, %Y')
                else:
                    date = date_str
            except:
                date = date_str
        
        return extracted_content.strip(), title, date
        
    except Exception as e:
        raise ValueError(f"Error fetching content from URL: {str(e)}")

def format_content(content):
    """Format content by wrapping paragraphs in <p> tags if needed."""
    # If content already has HTML tags, return as is (but ensure proper indentation)
    if '<p>' in content or '<div>' in content or '<h' in content:
        # Ensure proper indentation
        lines = content.split('\n')
        formatted_lines = []
        for line in lines:
            line = line.strip()
            if line:
                # If it's already a tag, add proper indentation
                if line.startswith('<'):
                    formatted_lines.append(f"                    {line}")
                else:
                    formatted_lines.append(f"                    {line}")
        return '\n'.join(formatted_lines)
    
    # Otherwise, split by double newlines and wrap each paragraph
    paragraphs = content.strip().split('\n\n')
    formatted = []
    for para in paragraphs:
        para = para.strip()
        if para:
            # Replace single newlines with spaces, then wrap in <p>
            para = ' '.join(para.split('\n'))
            # Escape HTML entities
            para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            formatted.append(f"                    <p>{para}</p>")
    
    return '\n'.join(formatted) if formatted else f"                    <p>{content}</p>"

def main():
    parser = argparse.ArgumentParser(description='Add a new memo to the blog')
    parser.add_argument('--title', help='Title of the memo')
    parser.add_argument('--date', help='Date of the memo (e.g., "January 1, 2026")')
    parser.add_argument('--content', help='Content of the memo')
    parser.add_argument('--number', type=int, help='Memo number (auto-detected if not provided)')
    parser.add_argument('--file', help='Read content from a file')
    parser.add_argument('--url', help='Fetch content from a URL (WordPress blog, etc.)')
    
    args = parser.parse_args()
    
    # Handle URL fetching first (if provided)
    url_title = None
    url_date = None
    if args.url:
        print(f"Fetching content from URL: {args.url}")
        try:
            url_content, url_title, url_date = fetch_content_from_url(args.url)
            print(f"✓ Successfully fetched content from URL")
            if url_title:
                print(f"  Found title: {url_title}")
            if url_date:
                print(f"  Found date: {url_date}")
        except Exception as e:
            print(f"Error: {str(e)}")
            return
        
        # Use URL content, title, and date as defaults
        content = url_content
        if url_title and not args.title:
            args.title = url_title
        if url_date and not args.date:
            args.date = url_date
    
    # Interactive mode if no arguments provided
    if not args.title and not args.date and not args.content and not args.file and not args.url:
        print("=== Add New Memo ===\n")
        
        # Get memo number
        next_num = get_next_memo_number()
        memo_num = input(f"Memo number (default: {next_num}): ").strip()
        memo_num = int(memo_num) if memo_num else next_num
        
        # Ask for URL first
        url_input = input("URL to fetch content from (or press Enter to skip): ").strip()
        if url_input:
            print(f"Fetching content from URL...")
            try:
                url_content, url_title, url_date = fetch_content_from_url(url_input)
                print(f"✓ Successfully fetched content")
                content = url_content
                if url_title:
                    print(f"  Found title: {url_title}")
                    use_title = input(f"Use this title? (Y/n): ").strip().lower()
                    title = url_title if use_title != 'n' else input("Title: ").strip()
                else:
                    title = input("Title: ").strip()
                
                if url_date:
                    print(f"  Found date: {url_date}")
                    use_date = input(f"Use this date? (Y/n): ").strip().lower()
                    date = url_date if use_date != 'n' else input("Date (e.g., 'January 1, 2026'): ").strip()
                else:
                    date = input("Date (e.g., 'January 1, 2026'): ").strip()
            except Exception as e:
                print(f"Error fetching from URL: {str(e)}")
                return
        else:
            # Get title
            title = input("Title: ").strip()
            if not title:
                print("Error: Title is required")
                return
            
            # Get date
            date = input("Date (e.g., 'January 1, 2026'): ").strip()
            if not date:
                print("Error: Date is required")
                return
            
            # Get content
            print("\nEnter content (press Enter twice to finish):")
            content_lines = []
            while True:
                try:
                    line = input()
                    if line == '' and content_lines and content_lines[-1] == '':
                        break
                    content_lines.append(line)
                except EOFError:
                    break
            
            content = '\n'.join(content_lines).strip()
            
            # Check if content should be read from file
            if not content:
                file_path = input("\nContent file path (or press Enter to skip): ").strip()
                if file_path and os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
    else:
        # Command line mode
        memo_num = args.number or get_next_memo_number()
        
        # Title and date handling
        title = args.title
        date = args.date
        
        # If URL was provided, content is already set above
        if not args.url:
            if args.file:
                if os.path.exists(args.file):
                    with open(args.file, 'r', encoding='utf-8') as f:
                        content = f.read()
                else:
                    print(f"Error: File {args.file} not found")
                    return
            elif args.content:
                content = args.content
            else:
                print("Error: Either --content, --file, or --url is required")
                return
        
        # Validate title and date
        if not title:
            print("Error: --title is required (or provide --url to auto-detect)")
            return
        
        if not date:
            print("Error: --date is required (or provide --url to auto-detect)")
            return
    
    # Format content
    content = format_content(content)
    
    # Create memo file
    memo_file = f"{MEMOS_DIR}/memo-{memo_num}.html"
    template = create_memo_template(memo_num, title, date, content)
    
    # Ensure memos directory exists
    os.makedirs(MEMOS_DIR, exist_ok=True)
    
    with open(memo_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✓ Created {memo_file}")
    
    # Update adjacent memos
    update_adjacent_memos(memo_num)
    
    # Add to diary listing
    add_to_diary_listing(memo_num, title, date)
    
    print(f"\n✅ Successfully added Memo #{memo_num}: {title}")
    print(f"   File: {memo_file}")
    print(f"   Date: {date}")

if __name__ == "__main__":
    main()

