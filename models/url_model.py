from sqlalchemy import Column, String, DateTime,Integer
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from datetime import datetime

class URLMapping(Base):
    """SQLAlchemy model for storing short URL to original URL mappings"""
    __tablename__ = "url_mappings"
    
    short_id = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_url = Column(String, unique=True, index=True)
    clicked= Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return f"<URLMapping(short_id={self.short_id}, original_url={self.original_url})>"
