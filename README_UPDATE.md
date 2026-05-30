# URL Shortener with SQLite Persistent Storage

## Overview
This is an updated URL shortener application that now uses **SQLAlchemy with SQLite** for persistent storage instead of in-memory dictionaries. All shortened URLs are now permanently stored in the database and survive application restarts.

## Changes Made

### 1. **Database Configuration** (`database.py`)
- Configured SQLite database with SQLAlchemy ORM
- Database file: `urls.db` (created automatically on first run)
- Session management with dependency injection for FastAPI

### 2. **Data Model** (`models/url_model.py`)
- `URLMapping` SQLAlchemy model with the following fields:
  - `short_id`: Primary key (short URL identifier)
  - `original_url`: The original long URL
  - `short_url`: Full short URL
  - `created_at`: Timestamp of creation

### 3. **Service Layer** (`services/shortener_service.py`)
- `URLShortenerService` class with methods for:
  - `create_short_url()`: Generate and store short URL
  - `get_original_url()`: Retrieve original URL by short ID
  - `get_all_mappings()`: List all URL mappings
  - `delete_mapping()`: Delete a URL mapping

### 4. **API Routes** (`routes/url_routes.py`)
- **POST** `/shorten-url/` - Create short URL (Request body: `{"url": "https://example.com"}`)
- **GET** `/{short_id}` - Redirect to original URL
- **GET** `/admin/all-mappings` - View all stored mappings
- **DELETE** `/admin/{short_id}` - Delete a URL mapping

### 5. **Main Application** (`main.py`)
- Database tables are created automatically on startup
- All three routers included

## Installation & Setup

### 1. Install Dependencies
```bash
cd /Users/mymacbook/Desktop/scheduler.pr/URLS
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Usage

### Create a Short URL
```bash
curl -X POST "http://localhost:8000/shorten-url/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'
```

Response:
```json
{
  "short_url": "http://localhost:8000/abc123",
  "short_id": "abc123",
  "original_url": "https://www.example.com/very/long/url"
}
```

### Redirect to Original URL
```bash
# Simply visit in browser or curl
curl -L "http://localhost:8000/abc123"
```

### View All Mappings (Admin)
```bash
curl "http://localhost:8000/admin/all-mappings"
```

### Delete a Mapping
```bash
curl -X DELETE "http://localhost:8000/admin/abc123"
```

## Database File
- **Location**: `urls.db` (in the URLS project directory)
- **Type**: SQLite database
- **Persistence**: All data persists even after application restart

## Key Features
✅ **Persistent Storage**: URLs survive application restarts
✅ **SQLAlchemy ORM**: Type-safe database operations
✅ **FastAPI Integration**: Async request handling
✅ **Admin Endpoints**: View and manage all URL mappings
✅ **Error Handling**: Proper HTTP error responses
✅ **Timestamps**: Track when each URL was created

## Troubleshooting

**Issue**: Import errors when running
- Solution: Ensure you're in the correct directory and all dependencies are installed

**Issue**: Database locked error
- Solution: Make sure only one instance of the app is running

**Issue**: Short ID not found when redirecting
- Solution: Make sure the short ID was created and stored correctly using the `/shorten-url/` endpoint
