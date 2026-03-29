import asyncio
import time
from typing import Optional

class AsyncTokenBucket:
    def __init__(self, capacity: float, fill_rate: float):
        """
        :param capacity: Maximum number of tokens (burst capacity).
        :param fill_rate: Tokens added per second.
        """
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = float(capacity)
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def consume(self, tokens: float = 1.0) -> bool:
        """
        Consumes tokens from the bucket if available.
        Calculates tokens based on elapsed time since last update.
        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            
            # Refill bucket based on elapsed time
            new_tokens = elapsed * self.fill_rate
            if new_tokens > 0:
                self.tokens = min(self.capacity, self.tokens + new_tokens)
                self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            return False
