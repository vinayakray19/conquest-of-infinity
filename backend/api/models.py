"""
Database models for the memo system.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Memo(Base):
    """Memo model representing a single diary entry."""
    __tablename__ = 'memos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    memo_number = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert memo to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'memo_number': self.memo_number,
            'title': self.title,
            'content': self.content,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Memo(memo_number={self.memo_number}, title='{self.title}', date={self.date})>"

