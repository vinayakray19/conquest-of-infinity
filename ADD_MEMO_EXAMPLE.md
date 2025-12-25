# How to Add a New Memo

## Quick Start

### Interactive Mode (Easiest)

Simply run:
```bash
python3 add_memo.py
```

The script will guide you through:
1. Memo number (auto-detected, just press Enter)
2. Title
3. Date (e.g., "January 15, 2026")
4. Content (type your text, press Enter twice when done)

### Command Line Mode

```bash
python3 add_memo.py --title "My New Memo" --date "January 15, 2026" --content "This is the content of my memo."
```

### From a File

If you have your content in a file:
```bash
python3 add_memo.py --title "My New Memo" --date "January 15, 2026" --file my_content.txt
```

### From a URL (WordPress Blog)

Fetch content directly from a WordPress blog URL:
```bash
python3 add_memo.py --url "https://insearchofexistece.wordpress.com/2020/12/31/saransh-2020/" --title "Saransh 2020" --date "December 31, 2020"
```

The script will automatically:
- Extract the article content from the page
- Try to detect title and date (you can override with --title and --date)
- Format the content properly

## What the Script Does Automatically

✅ Creates the memo HTML file with proper structure  
✅ Adds entry to `diary.html` (at the top, newest first)  
✅ Updates navigation links in adjacent memos  
✅ Handles numbering automatically  
✅ Formats content properly  

## Example

```bash
$ python3 add_memo.py
=== Add New Memo ===

Memo number (default: 25): 
Title: Reflections on Life
Date (e.g., 'January 1, 2026'): January 15, 2026

Enter content (press Enter twice to finish):
Life is a journey filled with moments of reflection.
Each day brings new opportunities to learn and grow.

We must embrace the challenges and celebrate the victories.

✓ Created memos/memo-25.html
✓ Updated memo-24.html navigation
✓ Added entry to diary.html

✅ Successfully added Memo #25: Reflections on Life
   File: memos/memo-25.html
   Date: January 15, 2026
```

## Tips

- **Content Formatting**: The script automatically wraps paragraphs in `<p>` tags
- **HTML Content**: If your content already has HTML tags, they'll be preserved
- **Numbering**: The script auto-detects the next memo number, but you can override it with `--number`
- **File Input**: Use `--file` to read content from a text file (useful for longer content)
- **URL Input**: Use `--url` to fetch content from WordPress blogs. The script will try to auto-detect title and date, but you can override with `--title` and `--date`
- **WordPress Support**: The script is optimized for WordPress.com blogs and will extract the main article content automatically

