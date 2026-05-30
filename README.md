# URL Shortener Service

A production-inspired URL Shortener built using FastAPI, SQLite, SQLAlchemy, and Redis.

This project demonstrates core backend engineering and system design concepts including URL shortening, caching, analytics tracking, rate limiting, and scalable architecture design.

## Features

* Create short URLs
* Redirect short URLs to original URLs
* Click analytics tracking
* Redis-based caching
* Redis-based rate limiting
* SQLite persistence
* Dockerized deployment
* Scalable architecture design

---

## Tech Stack

* FastAPI
* SQLite
* SQLAlchemy
* Redis
* Docker

---

## Project Structure

url_shortener/

├── main.py

├── database.py

├── cache.py

├── routes/

├── services/

├── models/

├── requirements.txt

├── Dockerfile

├── docker-compose.yml

└── README.md

---

## API Endpoints

### Create Short URL

POST /shorten

Request:

{
"url": "https://youtube.com"
}

Response:

{
"short_id": "abc123",
"short_url": "http://localhost:8000/abc123"
}

---

### Redirect

GET /{short_id}

Redirects to the original URL.

---

### Get All URLs

GET /urls

Returns all stored URL mappings.

---

## Architecture

Client
|
v
FastAPI
|
+--------+
| Redis |
+--------+
|
+--------+
| SQLite |
+--------+

### Redis Usage

* URL cache
* Analytics counters
* Rate limiting

### SQLite Usage

* Persistent URL mappings
* Analytics storage

---

## System Design Concepts Implemented

* Database Persistence
* Caching
* Analytics Aggregation
* Rate Limiting
* Scalability Planning
* Load Balancing Design
* API Design

---

## Run Locally

pip install -r requirements.txt

uvicorn main:app --reload

---

## Docker

docker-compose up --build

---

## Future Improvements

* PostgreSQL migration
* User authentication
* Custom aliases
* Expiration support
* Distributed deployment
* Kubernetes deployment
