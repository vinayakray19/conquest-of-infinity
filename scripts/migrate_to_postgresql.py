#!/usr/bin/env python3
"""
Migrate memos from local SQLite to Render PostgreSQL.
This script reads from your local memos.db and transfers to PostgreSQL.

Usage:
    export DATABASE_URL="postgres://user:pass@host:port/dbname"
    python3 scripts/migrate_to_postgresql.py
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from backend.api.models import Memo, Base

def migrate_to_postgresql():
    """Migrate memos from local SQLite to PostgreSQL."""
    
    # Get PostgreSQL connection string
    pg_url = os.getenv('DATABASE_URL')
    if not pg_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("   Set it to your Render PostgreSQL connection string:")
        print("   export DATABASE_URL='postgres://user:pass@host:port/dbname'")
        print()
        print("   To get your DATABASE_URL from Render:")
        print("   1. Go to Render Dashboard → Your Database")
        print("   2. Click 'Connect' tab")
        print("   3. Copy 'Internal Database URL' (for same region)")
        print("   4. Or copy 'External Connection String' (if running locally)")
        return
    
    # Convert postgres:// to postgresql+psycopg:// for psycopg3 compatibility
    if pg_url.startswith('postgres://'):
        pg_url = pg_url.replace('postgres://', 'postgresql+psycopg://', 1)
    elif pg_url.startswith('postgresql://') and not pg_url.startswith('postgresql+'):
        # Convert postgresql:// to postgresql+psycopg://
        pg_url = pg_url.replace('postgresql://', 'postgresql+psycopg://', 1)
    
    # Connect to local SQLite
    local_db_path = Path(__file__).resolve().parent.parent / 'memos.db'
    if not local_db_path.exists():
        print(f"❌ Local database not found: {local_db_path}")
        print("   Make sure you have a local memos.db file")
        return
    
    sqlite_url = f'sqlite:///{local_db_path}'
    
    print("🔄 Starting migration from SQLite to PostgreSQL...")
    print(f"   Source: {local_db_path}")
    print(f"   Target: PostgreSQL (Render)")
    print()
    
    # Connect to databases
    try:
        sqlite_engine = create_engine(sqlite_url)
        pg_engine = create_engine(pg_url, pool_pre_ping=True)
        
        # Create tables in PostgreSQL if they don't exist
        print("1. Creating tables in PostgreSQL...")
        Base.metadata.create_all(bind=pg_engine)
        print("   ✅ Tables created/verified")
        
        # Create sessions
        SQLiteSession = sessionmaker(bind=sqlite_engine)
        PGSession = sessionmaker(bind=pg_engine)
        
        sqlite_db = SQLiteSession()
        pg_db = PGSession()
        
        # Read all memos from SQLite
        print("\n2. Reading memos from SQLite...")
        sqlite_memos = sqlite_db.query(Memo).all()
        print(f"   Found {len(sqlite_memos)} memos")
        
        if len(sqlite_memos) == 0:
            print("   ℹ️  No memos to migrate")
            return
        
        # Migrate each memo
        print("\n3. Migrating memos to PostgreSQL...")
        migrated = 0
        skipped = 0
        failed = 0
        
        for memo in sqlite_memos:
            try:
                # Check if memo already exists
                existing = pg_db.query(Memo).filter(Memo.memo_number == memo.memo_number).first()
                if existing:
                    print(f"   ⏭️  Memo #{memo.memo_number}: Already exists, skipping...")
                    skipped += 1
                    continue
                
                # Create new memo in PostgreSQL
                new_memo = Memo(
                    memo_number=memo.memo_number,
                    title=memo.title,
                    content=memo.content,
                    date=memo.date,
                    created_at=memo.created_at or datetime.utcnow(),
                    updated_at=memo.updated_at or datetime.utcnow()
                )
                
                pg_db.add(new_memo)
                pg_db.commit()
                
                print(f"   ✅ Memo #{memo.memo_number}: {memo.title[:50]}...")
                migrated += 1
                
            except Exception as e:
                print(f"   ❌ Memo #{memo.memo_number}: Error - {e}")
                pg_db.rollback()
                failed += 1
        
        # Summary
        print(f"\n📊 Migration Summary:")
        print(f"   ✅ Migrated: {migrated}")
        print(f"   ⏭️  Skipped: {skipped}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📦 Total: {len(sqlite_memos)}")
        print()
        print("✅ Migration complete! Your memos are now in PostgreSQL.")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    finally:
        sqlite_db.close()
        pg_db.close()

if __name__ == "__main__":
    migrate_to_postgresql()

