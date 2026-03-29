import httpx
import logging
import sys
from fastapi import FastAPI, Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from rate_limiter import AsyncTokenBucket
import time

# Configure Logging for High Throughput
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("api-gateway")

# Configuration
MAX_BODY_SIZE = 512 * 1024  # 512KB
API_KEY_HEADER = "X-API-Key"
VALID_API_KEYS = {"secret-token-123"}  # In production, use a database or cache
TARGET_URL = "https://api.github.com" # Updated to GitHub API

# Initialize Rate Limiter: 20 burst, 2/sec fill
rate_limiter = AsyncTokenBucket(capacity=20.0, fill_rate=2.0)

class GatewayMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, client: httpx.AsyncClient):
        super().__init__(app)
        self.client = client

    async def dispatch(self, request: Request, call_next):
        # Ignore favicon requests to keep logs professional
        if request.url.path == "/favicon.ico":
            return Response(status_code=204)

        start_time = time.perf_counter()
        
        # Log Incoming Request
        logger.info(f"REQUEST: {request.method} {request.url.path} from {request.client.host}")

        # 1. Check API Key
        api_key = request.headers.get(API_KEY_HEADER)
        if not api_key or api_key not in VALID_API_KEYS:
            logger.warning(f"RESPONSE: 401 Unauthorized (Invalid or missing API Key) for {request.client.host}")
            return Response(content="Unauthorized: Invalid or missing API Key", status_code=401)

        # 2. Check Body Size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_BODY_SIZE:
            logger.warning(f"RESPONSE: 413 Payload Too Large ({content_length} bytes) for {request.client.host}")
            return Response(content="Payload Too Large", status_code=413)

        # 3. Consume Token
        if not await rate_limiter.consume(1.0):
            logger.warning(f"RESPONSE: 429 Too Many Requests (Rate limit exceeded) for {request.client.host}")
            return Response(content="Too Many Requests", status_code=429)

        # 4. Proxy Request
        response = await self.proxy_request(request)
        
        duration = time.perf_counter() - start_time
        logger.info(f"RESPONSE: {response.status_code} Success ({duration:.4f}s)")
        return response

    async def proxy_request(self, request: Request) -> Response:
        # Stream the body to handle size limits and efficiency
        body = await request.body()
        if len(body) > MAX_BODY_SIZE:
            return Response(content="Payload Too Large", status_code=413)

        url = f"{TARGET_URL}{request.url.path}"
        if request.url.query:
            url += f"?{request.url.query}"

        # Filter out headers that GitHub API might reject or that should be replaced
        exclude_headers = {"host", "content-length", "x-api-key"}
        headers = {k: v for k, v in request.headers.items() if k.lower() not in exclude_headers}
        
        # Add required User-Agent for GitHub API
        if "user-agent" not in {k.lower() for k in headers.keys()}:
            headers["User-Agent"] = "Python-API-Gateway"

        try:
            response = await self.client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                follow_redirects=True,
                timeout=10.0
            )
            
            # Filter out headers that might cause Content-Length mismatches
            response_headers = {k: v for k, v in response.headers.items() if k.lower() not in {"content-length", "content-encoding", "transfer-encoding"}}
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=response_headers
            )
        except httpx.RequestError as exc:
            return Response(content=f"Gateway Error: {str(exc)}", status_code=502)

app = FastAPI()

# Shared client for high concurrency
client = httpx.AsyncClient()

@app.on_event("startup")
async def startup_event():
    global client
    client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()

app.add_middleware(GatewayMiddleware, client=client)

@app.get("/{path:path}")
@app.post("/{path:path}")
@app.put("/{path:path}")
@app.delete("/{path:path}")
async def gateway_entry():
    # This is handled by the middleware
    pass
