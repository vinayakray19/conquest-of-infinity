"""
Routes for memo management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List

from backend.api.models import Memo
from backend.api.database import get_db

router = APIRouter(prefix="/api/memos", tags=["memos"])

@router.get("", response_model=List[dict])
async def get_memos(
    skip: int = 0,
    limit: int = 100,
    order: str = "desc",  # "asc" for oldest first, "desc" for newest first
    db: Session = Depends(get_db)
):
    """Get all memos, optionally paginated."""
    order_by = desc(Memo.date) if order == "desc" else Memo.date
    memos = db.query(Memo).order_by(order_by).offset(skip).limit(limit).all()
    return [memo.to_dict() for memo in memos]

@router.get("/{memo_number}", response_model=dict)
async def get_memo_by_number(memo_number: int, db: Session = Depends(get_db)):
    """Get a specific memo by its memo number."""
    memo = db.query(Memo).filter(Memo.memo_number == memo_number).first()
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memo #{memo_number} not found"
        )
    return memo.to_dict()

@router.get("/id/{memo_id}", response_model=dict)
async def get_memo_by_id(memo_id: int, db: Session = Depends(get_db)):
    """Get a specific memo by its database ID."""
    memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memo with ID {memo_id} not found"
        )
    return memo.to_dict()

@router.get("/nav/{memo_number}", response_model=dict)
async def get_memo_navigation(memo_number: int, db: Session = Depends(get_db)):
    """Get navigation information (previous and next memo) for a given memo."""
    current_memo = db.query(Memo).filter(Memo.memo_number == memo_number).first()
    if not current_memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memo #{memo_number} not found"
        )
    
    # Get previous memo (lower memo number, chronologically earlier)
    prev_memo = db.query(Memo).filter(
        Memo.memo_number < memo_number
    ).order_by(desc(Memo.memo_number)).first()
    
    # Get next memo (higher memo number, chronologically later)
    next_memo = db.query(Memo).filter(
        Memo.memo_number > memo_number
    ).order_by(Memo.memo_number).first()
    
    return {
        "current": current_memo.to_dict(),
        "previous": prev_memo.to_dict() if prev_memo else None,
        "next": next_memo.to_dict() if next_memo else None
    }

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_memo(
    memo_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new memo."""
    # Validate required fields
    required_fields = ['title', 'content', 'date']
    for field in required_fields:
        if field not in memo_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {field}"
            )
    
    # Parse date if it's a string
    date = memo_data['date']
    if isinstance(date, str):
        try:
            # Try parsing various date formats
            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        except:
            try:
                # Try format: "December 30, 2025"
                date = datetime.strptime(date, "%B %d, %Y")
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date format. Use ISO format or 'Month Day, Year'"
                )
    
    # Auto-assign memo_number if not provided
    if 'memo_number' not in memo_data:
        last_memo = db.query(Memo).order_by(desc(Memo.memo_number)).first()
        memo_data['memo_number'] = (last_memo.memo_number + 1) if last_memo else 1
    
    # Check if memo_number already exists
    existing = db.query(Memo).filter(Memo.memo_number == memo_data['memo_number']).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Memo #{memo_data['memo_number']} already exists"
        )
    
    memo = Memo(
        memo_number=memo_data['memo_number'],
        title=memo_data['title'],
        content=memo_data['content'],
        date=date
    )
    
    db.add(memo)
    db.commit()
    db.refresh(memo)
    
    return memo.to_dict()

@router.put("/{memo_number}", response_model=dict)
async def update_memo(
    memo_number: int,
    memo_data: dict,
    db: Session = Depends(get_db)
):
    """Update an existing memo."""
    memo = db.query(Memo).filter(Memo.memo_number == memo_number).first()
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memo #{memo_number} not found"
        )
    
    # Update fields
    if 'title' in memo_data:
        memo.title = memo_data['title']
    if 'content' in memo_data:
        memo.content = memo_data['content']
    if 'date' in memo_data:
        date = memo_data['date']
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except:
                try:
                    date = datetime.strptime(date, "%B %d, %Y")
                except:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid date format"
                    )
        memo.date = date
    
    memo.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(memo)
    
    return memo.to_dict()

@router.delete("/{memo_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memo(memo_number: int, db: Session = Depends(get_db)):
    """Delete a memo."""
    memo = db.query(Memo).filter(Memo.memo_number == memo_number).first()
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memo #{memo_number} not found"
        )
    
    db.delete(memo)
    db.commit()
    
    return None


