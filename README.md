# A Digital Diary - Vinayak Ray

A minimal, modern personal blog showcasing thoughts, reflections, and philosophical musings.

## Project Structure

```
my-blog/
├── index.html          # Home page
├── diary.html          # Diary listing page
├── add_memo.py         # Script to add new memos easily
├── css/
│   └── styles.css     # All stylesheets
├── memos/
│   ├── memo-1.html    # Oldest memo (June 1, 2020)
│   ├── memo-2.html
│   ├── ...
│   └── memo-24.html   # Newest memo (December 20, 2025)
└── README.md
```

## Features

- **Minimal Design**: Clean, modern interface with spring-inspired background
- **Individual Memo Pages**: Each story has its own dedicated page for better reading experience
- **Navigation**: Easy navigation between memos with Previous/Next buttons
- **Responsive**: Fully responsive design for mobile and desktop
- **Spring Theme**: Soothing spring background with green trees and falling leaves

## File Organization

### Root Directory
- `index.html` - Main home page with introduction
- `diary.html` - Diary listing page with all memo entries

### CSS Directory (`css/`)
- `styles.css` - All styling for the entire website

### Memos Directory (`memos/`)
- `memo-1.html` through `memo-24.html` - Individual memo pages
- Each memo page includes:
  - Full article content
  - Navigation to previous/next memo
  - Link back to diary listing

## Adding New Memos

### Using the Script (Recommended)

The easiest way to add a new memo is using the `add_memo.py` script:

**Interactive Mode:**
```bash
python3 add_memo.py
```
The script will prompt you for:
- Memo number (auto-detected as next number)
- Title
- Date (e.g., "January 1, 2026")
- Content (enter text, press Enter twice to finish)

**Command Line Mode:**
```bash
python3 add_memo.py --title "Your Title" --date "January 1, 2026" --content "Your content here"
```

**From File:**
```bash
python3 add_memo.py --title "Your Title" --date "January 1, 2026" --file content.txt
```

**From URL (WordPress Blog):**
```bash
python3 add_memo.py --url "https://example.com/post" --title "Your Title" --date "January 1, 2026"
```

The script can automatically extract content, title, and date from WordPress blog URLs!

The script automatically:
- Creates the memo HTML file with proper structure
- Adds entry to `diary.html` listing
- Updates navigation links in adjacent memos
- Handles numbering automatically

### Manual Method

If you prefer to add memos manually:

1. Create a new file `memos/memo-25.html` (or next number)
2. Use the existing memo files as a template
3. Update navigation links:
   - Previous memo: `memo-24.html`
   - Next memo: (will be memo-26 when created)
4. Add entry to `diary.html` in the diary entries section
5. Update the suggested read link if needed

## Navigation Structure

- **Home Page** (`index.html`) → Links to `diary.html`
- **Diary Page** (`diary.html`) → Links to all `memos/memo-X.html`
- **Memo Pages** (`memos/memo-X.html`) → Links to:
  - `../index.html` (Home)
  - `../diary.html` (Back to list)
  - `memo-(X-1).html` (Previous)
  - `memo-(X+1).html` (Next)

## Styling

All styles are centralized in `css/styles.css`:
- Spring background effects
- Typography (Inter, Playfair Display, Space Grotesk, Cormorant Garamond, Dancing Script)
- Responsive breakpoints
- Navigation styles
- Article content styles

## Browser Support

Modern browsers with support for:
- CSS Grid and Flexbox
- CSS animations
- HTML5 semantic elements

## Maintenance

- **Styles**: Edit `css/styles.css` for design changes
- **Content**: Edit individual memo files in `memos/` directory
- **Structure**: Main pages (`index.html`, `diary.html`) in root directory
