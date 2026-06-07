from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time
import logging
from pathlib import Path
import os
from app.database import engine, Base
from app.routers import products, users, cart, orders, google_auth, support, upload, admin
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    if engine is not None:
        Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.warning(f"Could not create tables: {e}")

app = FastAPI(title="E-commerce Store API", version="1.0.0")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Not found"},
    )

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limit_store = defaultdict(list)
RATE_LIMIT = 60
RATE_WINDOW = 60


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        rate_limit_store[client_ip] = [
            t for t in rate_limit_store[client_ip] if now - t < RATE_WINDOW
        ]
        if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please slow down."},
            )
        rate_limit_store[client_ip].append(now)

        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' https://cdnjs.cloudflare.com https://fonts.googleapis.com 'unsafe-inline'; style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; img-src 'self' data: https://images.unsplash.com https://via.placeholder.com; font-src 'self' https://fonts.gstatic.com; connect-src 'self'"

        path = request.url.path
        if path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=86400"
        elif path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response.headers["Pragma"] = "no-cache"

        return response


app.add_middleware(SecurityMiddleware)

app.include_router(products.router)
app.include_router(users.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(google_auth.router)
app.include_router(support.router)
app.include_router(upload.router)
app.include_router(admin.router)

static_dir = Path(__file__).parent / "static"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

HTML_CONTENT = None
html_file = static_dir / "index.html"
if html_file.exists():
    HTML_CONTENT = html_file.read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
def root():
    if HTML_CONTENT:
        return HTMLResponse(content=HTML_CONTENT)
    return HTMLResponse(content="<h1>LuckyShop API</h1><p>Frontend not available in this environment.</p>")


@app.get("/health")
def health():
    db_ok = False
    if engine is not None:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                db_ok = True
        except Exception:
            pass
    return {"status": "ok", "database": "connected" if db_ok else "disconnected"}
