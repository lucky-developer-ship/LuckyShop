import base64
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/api/upload", tags=["upload"])

import os
import tempfile
from pathlib import Path
from fastapi.responses import FileResponse

def get_upload_dir():
    if os.getenv("VERCEL"):
        tmp = Path(tempfile.gettempdir()) / "uploads"
    else:
        tmp = Path(__file__).parent.parent / "static" / "uploads"
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    allowed = {"image/jpeg", "image/png", "image/gif", "image/webp"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, GIF, WebP allowed")

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    ext = file.filename.split(".")[-1] if "." in file.filename else "png"
    filename = f"{uuid.uuid4()}.{ext}"
    upload_dir = get_upload_dir()
    filepath = upload_dir / filename
    
    with open(filepath, "wb") as f:
        f.write(content)
        
    if os.getenv("VERCEL"):
        return {"url": f"/api/upload/serve/{filename}"}
    return {"url": f"/static/uploads/{filename}"}

@router.get("/serve/{filename}")
async def serve_upload(filename: str):
    upload_dir = get_upload_dir()
    filepath = upload_dir / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath)
