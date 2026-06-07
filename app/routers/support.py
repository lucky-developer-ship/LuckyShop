from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/support", tags=["support"])


class SupportRequest(BaseModel):
    name: str
    email: str
    subject: str = "general"
    message: str


class SupportResponse(BaseModel):
    success: bool
    message: str


@router.post("/", response_model=SupportResponse)
def submit_support(request: SupportRequest):
    name = request.name.strip()[:100]
    email = request.email.strip().lower()[:200]
    message = request.message.strip()[:5000]

    if not name or not email or not message:
        raise HTTPException(status_code=400, detail="Name, email, and message are required")

    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Invalid email address")

    logger.info(f"[SUPPORT] New message from {name} ({email}) - Subject: {request.subject}")

    return SupportResponse(
        success=True,
        message="Your support request has been received. We'll get back to you within 24 hours."
    )
