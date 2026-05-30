from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from services.rate_limiter import RateLimiter
from services.shortener_service import URLShortenerService

# Define request/response models
class URLRequest(BaseModel):
    url: str

class URLResponse(BaseModel):
    short_url: str
    short_id: str
    original_url: str

# Create rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=10)

# Create routers
shortener_router = APIRouter(prefix="/shorten-url", tags=["v1"], dependencies=[Depends(rate_limiter)])
get_og_url_router = APIRouter(tags=["v1"], dependencies=[Depends(rate_limiter)])
admin_router = APIRouter(prefix="/admin", tags=["admin"])

@shortener_router.post("/", response_model=URLResponse)
async def url_post(url_request: URLRequest, db: Session = Depends(get_db)):
    """Create a short URL for the given original URL"""
    result = URLShortenerService.create_short_url(db, url_request.url)
    return result

@get_og_url_router.get("/{short_url}")
async def url_get(short_url: str, db: Session = Depends(get_db)):
    """Redirect from short URL to original URL"""
    original_url = URLShortenerService.get_original_url(db, short_url)
    return RedirectResponse(url=original_url)

@admin_router.get("/all-mappings")
async def get_all_mappings(db: Session = Depends(get_db)):
    """Get all URL mappings (admin endpoint)"""
    mappings = URLShortenerService.get_all_mappings(db)
    return {"mappings": mappings, "total": len(mappings)}

@admin_router.delete("/{short_id}")
async def delete_mapping(short_id: str, db: Session = Depends(get_db)):
    """Delete a URL mapping"""
    URLShortenerService.delete_mapping(db, short_id)
    return {"message": f"URL mapping for {short_id} deleted successfully"}
