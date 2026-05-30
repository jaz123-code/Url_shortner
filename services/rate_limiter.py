import time
from fastapi import HTTPException, Request
from cache import redis_client

class RateLimiter:
    """
    Token Bucket Rate Limiter using Redis.
    Flow: Client -> Rate Limiter -> API Server -> Database
    """
    def __init__(self, requests_per_minute: int = 10):
        self.rate = requests_per_minute
        self.interval = 60  # 1 minute

    async def __call__(self, request: Request):
        # Identify client by IP
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        now = time.time()
        
        # Use Redis pipeline for atomic operations
        pipe = redis_client.pipeline()
        pipe.get(f"{key}:tokens")
        pipe.get(f"{key}:last_refill")
        results = pipe.execute()

        tokens = float(results[0]) if results[0] else self.rate
        last_refill = float(results[1]) if results[1] else now

        # Refill tokens based on time passed
        passed = now - last_refill
        tokens = min(self.rate, tokens + passed * (self.rate / self.interval))

        if tokens < 1:
            raise HTTPException(status_code=429, detail="Too Many Requests - Rate Limit Exceeded")

        # Consume 1 token and update Redis
        redis_client.setex(f"{key}:tokens", self.interval, tokens - 1)
        redis_client.setex(f"{key}:last_refill", self.interval, now)