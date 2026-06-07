from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import os
from app.database import engine, Base
from app.routers import products, users, cart, orders, google_auth, support

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


@app.get("/")
def root():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
