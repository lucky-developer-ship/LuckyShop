from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from app.database import engine, Base
from app.routers import products, users, cart, orders, google_auth, support, upload, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Store API", version="1.0.0")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"status": "ok"}
