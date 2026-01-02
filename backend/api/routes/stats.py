"""
Routes for statistics and health checks.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.api.models import Memo
from backend.api.database import get_db

router = APIRouter(prefix="/api", tags=["stats"])

@router.get("/stats", response_model=dict)
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about the memos."""
    total_memos = db.query(Memo).count()
    if total_memos == 0:
        return {
            "total_memos": 0,
            "oldest_date": None,
            "newest_date": None
        }
    
    oldest = db.query(Memo).order_by(Memo.date).first()
    newest = db.query(Memo).order_by(desc(Memo.date)).first()
    
    return {
        "total_memos": total_memos,
        "oldest_date": oldest.date.isoformat() if oldest else None,
        "newest_date": newest.date.isoformat() if newest else None,
        "first_memo_number": oldest.memo_number if oldest else None,
        "last_memo_number": newest.memo_number if newest else None
    }

