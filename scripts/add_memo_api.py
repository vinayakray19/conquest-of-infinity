#!/usr/bin/env python3
"""
Script to add a new memo via the API.
This is the updated version that works with the backend API.

Usage:
    python3 add_memo_api.py --title "Title" --date "Month Day, Year" --content "Content here"
    python3 add_memo_api.py --url "https://example.com/post" --title "Title" --date "Date"
    
Or run interactively:
    python3 add_memo_api.py
"""
import os
import re
import argparse
import sys
from datetime import datetime
from urllib.request import urlopen, Request
from html import unescape
import requests

# API base URL - can be overridden via environment variable
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8001')

def fetch_content_from_url(url):
    """Fetch and extract content from a WordPress blog URL."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        with urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        # Extract content from WordPress post
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
            main_match = re.search(r'<h1[^>]*>.*?</h1>(.*?)(?:<nav|</nav>|<footer|</footer>|</article|</main|<!--\s*Post navigation)', html_content, re.DOTALL | re.IGNORECASE)
            if main_match:
                extracted_content = main_match.group(1)
        
        if not extracted_content:
            raise ValueError("Could not extract content from URL. The page structure may not be recognized.")
        
        # Clean up the extracted content
        extracted_content = re.sub(r'<script[^>]*>.*?</script>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<style[^>]*>.*?</style>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<div[^>]*class="[^"]*wp-block[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<div[^>]*class="[^"]*widget[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<!--.*?-->', '', extracted_content, flags=re.DOTALL)
        extracted_content = re.sub(r'<div[^>]*class="[^"]*share[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<div[^>]*class="[^"]*post-navigation[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'<div[^>]*class="[^"]*comments[^"]*"[^>]*>.*?</div>', '', extracted_content, flags=re.DOTALL | re.IGNORECASE)
        extracted_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', extracted_content)
        extracted_content = extracted_content.strip()
        
        # Try to extract title
        title = None
        title_match = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', html_content, re.DOTALL | re.IGNORECASE)
        if not title_match:
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL | re.IGNORECASE)
        if not title_match:
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.DOTALL | re.IGNORECASE)
        
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            title = unescape(title)
            title = re.sub(r'\s*[-|–—]\s*.*$', '', title).strip()
            title = re.sub(r'\s*\|.*$', '', title).strip()
        
        # Try to extract date
        date_match = re.search(r'<time[^>]*datetime="([^"]*)"', html_content, re.IGNORECASE)
        if not date_match:
            date_match = re.search(r'class="[^"]*published[^"]*"[^>]*>([^<]*)', html_content, re.IGNORECASE)
        
        date = None
        if date_match:
            date_str = date_match.group(1).strip()
            try:
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

def create_memo(title, date, content, api_url):
    """Create a memo via the API."""
    try:
        # Parse date
        if isinstance(date, str):
            date_obj = datetime.strptime(date, "%B %d, %Y")
        else:
            date_obj = date
        
        payload = {
            "title": title,
            "content": content,
            "date": date_obj.isoformat()
        }
        
        response = requests.post(f"{api_url}/api/memos", json=payload)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to create memo via API: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Add a new memo via API')
    parser.add_argument('--title', help='Title of the memo')
    parser.add_argument('--date', help='Date of the memo (e.g., "January 1, 2026")')
    parser.add_argument('--content', help='Content of the memo')
    parser.add_argument('--file', help='Read content from a file')
    parser.add_argument('--url', help='Fetch content from a URL (WordPress blog, etc.)')
    parser.add_argument('--api-url', help=f'API base URL (default: {API_BASE_URL})', default=API_BASE_URL)
    
    args = parser.parse_args()
    
    # Handle URL fetching first
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
        
        content = url_content
        if url_title and not args.title:
            args.title = url_title
        if url_date and not args.date:
            args.date = url_date
    
    # Interactive mode if no arguments provided
    if not args.title and not args.date and not args.content and not args.file and not args.url:
        print("=== Add New Memo (via API) ===\n")
        
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
            title = input("Title: ").strip()
            if not title:
                print("Error: Title is required")
                return
            
            date = input("Date (e.g., 'January 1, 2026'): ").strip()
            if not date:
                print("Error: Date is required")
                return
            
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
            
            if not content:
                file_path = input("\nContent file path (or press Enter to skip): ").strip()
                if file_path and os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
    else:
        # Command line mode
        title = args.title
        date = args.date
        
        if args.url:
            # Content already set above
            pass
        elif args.file:
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
        
        if not title:
            print("Error: --title is required (or provide --url to auto-detect)")
            return
        
        if not date:
            print("Error: --date is required (or provide --url to auto-detect)")
            return
    
    # Create memo via API
    print(f"\nCreating memo via API...")
    result = create_memo(title, date, content, args.api_url)
    
    print(f"\n✅ Successfully created memo via API!")
    print(f"   Memo #: {result['memo_number']}")
    print(f"   Title: {result['title']}")
    print(f"   Date: {result['date']}")

if __name__ == "__main__":
    main()

