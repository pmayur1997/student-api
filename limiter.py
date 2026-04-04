from fastapi import HTTPException, Request
from collections import defaultdict
from datetime import datetime, timedelta
import threading

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock      = threading.Lock()

    def is_allowed(self, key: str, max_requests: int, window_seconds: int = 60) -> bool:
        now    = datetime.utcnow()
        window = now - timedelta(seconds=window_seconds)

        with self.lock:
            # Remove requests outside the window
            self.requests[key] = [
                t for t in self.requests[key] if t > window
            ]

            # Check if limit exceeded
            if len(self.requests[key]) >= max_requests:
                return False

            # Add current request timestamp
            self.requests[key].append(now)
            return True


# Single instance
rate_limiter = RateLimiter()


# ── Helper function to use in routes ────────────
def check_limit(request: Request, key: str, max_requests: int, window_seconds: int = 60):
    client_ip = request.client.host
    limit_key = f"{client_ip}:{key}"

    if not rate_limiter.is_allowed(limit_key, max_requests, window_seconds):
        raise HTTPException(
            status_code=429,
            detail={
                "error":   "Too many requests",
                "message": f"Max {max_requests} requests per {window_seconds} seconds. Try again later."
            }
        )