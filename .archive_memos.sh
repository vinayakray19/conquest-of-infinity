#!/bin/bash
# Optional script to archive the memos directory before removal
# This creates a backup before deleting the directory

ARCHIVE_NAME="memos_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

if [ -d "memos" ]; then
    echo "Creating backup archive: $ARCHIVE_NAME"
    tar -czf "$ARCHIVE_NAME" memos/
    echo "✓ Backup created: $ARCHIVE_NAME"
    echo ""
    echo "To remove the memos directory, run:"
    echo "  rm -rf memos/"
    echo ""
    echo "Or if you want to remove both the directory and backup:"
    echo "  rm -rf memos/ && rm $ARCHIVE_NAME"
else
    echo "memos/ directory not found. Nothing to archive."
fi

