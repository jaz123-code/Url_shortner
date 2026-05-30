from fastapi import FastAPI
import uvicorn
from database import engine, Base
from routes.url_routes import shortener_router, get_og_url_router, admin_router
from models.url_model import URLMapping

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

app.include_router(shortener_router)
app.include_router(get_og_url_router)
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)