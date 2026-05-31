import random
from datetime import datetime
from sqlalchemy.orm import Session
from models.url_model import URLMapping
from fastapi import HTTPException
from cache import redis_client
# Temporary cache to store click counts and access times before flushing to DB
# Structure: {short_id: {"clicked": int, "last_accessed": datetime}}
dbCache = {}
BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

class URLShortenerService:
    """Service class to handle URL shortening operations"""

    @staticmethod
    def _base62_encode(number: int) -> str:
        if number == 0:
            return BASE62_ALPHABET[0]
        encoded_chars = []
        while number > 0:
            number, rem = divmod(number, 62)
            encoded_chars.append(BASE62_ALPHABET[rem])
        return "".join(reversed(encoded_chars))

    @staticmethod
    def _generate_unique_short_id(db: Session, length: int = 6) -> str:
        max_value = 62 ** length
        while True:
            raw_id = random.randrange(max_value)
            short_id = URLShortenerService._base62_encode(raw_id).rjust(length, "0")
            existing = db.query(URLMapping).filter(URLMapping.short_id == short_id).first()
            if not existing:
                return short_id

    @staticmethod
    def create_short_url(db: Session, original_url: str) -> dict:
        """
        Create a short URL mapping and store it in database
        
        Args:
            db: Database session
            original_url: The original URL to shorten
            
        Returns:
            Dictionary with short_url and short_id
        """
        # Generate unique short ID using Base62 encoding
        short_id = URLShortenerService._generate_unique_short_id(db)
        short_url = f"http://localhost:8000/{short_id}"
        
        # Create URL mapping record
        url_mapping = URLMapping(
            short_id=short_id,
            original_url=original_url,
            short_url=short_url
        )
        
        try:
            db.add(url_mapping)
            db.commit()
            db.refresh(url_mapping)
            return {
                "short_url": short_url,
                "short_id": short_id,
                "original_url": original_url
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating short URL: {str(e)}")
    
    @staticmethod
    def get_original_url(db: Session, short_id: str) -> str:
        """
        Retrieve original URL by short ID
        
        Args:
            db: Database session
            short_id: The short ID
            
        Returns:
            Original URL
            
        Raises:
            HTTPException: If URL not found
        """
        # 1. Find URL in Database
        url_mapping = db.query(URLMapping).filter(
            URLMapping.short_id == short_id
        ).first()
        
        if not url_mapping:
            raise HTTPException(status_code=404, detail="URL not found")
        
        # 2. Initialize  redis cache
        cache_key=f"url:{short_id}"

        #Increment click count in Redis
        redis_client.hincrby(cache_key, "clicked", 1)

        #update last accessed time
        redis_client.hset(
            cache_key,
            "last_accessed",
            datetime.utcnow().isoformat()
        )


        # 4. Periodic Flush: If clicks in cache exceed threshold, sync to DB
        clicked=int(redis_client.hget(cache_key, "clicked")or 0)
        if clicked%10==0:# Sync every 10 clicks
            url_mapping.clicked=clicked
            last_accessed=redis_client.hget(
                cache_key,
                "last_accessed"
            )
            if last_accessed:
                url_mapping.last_accessed=datetime.fromisoformat(last_accessed)
                
            db.commit()
            db.refresh(url_mapping)

        # 5. Redirect (Return original URL)
        return url_mapping.original_url
    
    @staticmethod
    def get_all_mappings(db: Session) -> list:
        """
        Retrieve all URL mappings
        
        Args:
            db: Database session
            
        Returns:
            List of all URL mappings
        """
        mappings = db.query(URLMapping).all()
        return [
            {
                "short_id": m.short_id,
                "short_url": m.short_url,
                "original_url": m.original_url,
                "created_at": m.created_at.isoformat() if m.created_at else None
            }
            for m in mappings
        ]
    
    @staticmethod
    def delete_mapping(db: Session, short_id: str) -> bool:
        """
        Delete a URL mapping
        
        Args:
            db: Database session
            short_id: The short ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        url_mapping = db.query(URLMapping).filter(
            URLMapping.short_id == short_id
        ).first()
        
        if not url_mapping:
            raise HTTPException(status_code=404, detail="URL not found")
        
        try:
            db.delete(url_mapping)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting URL: {str(e)}")
