from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

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
    if not request.name or not request.email or not request.message:
        raise HTTPException(status_code=400, detail="Name, email, and message are required")

    print(f"[SUPPORT] New message from {request.name} ({request.email})")
    print(f"  Subject: {request.subject}")
    print(f"  Message: {request.message}")

    return SupportResponse(
        success=True,
        message="Your support request has been received. We'll get back to you within 24 hours."
    )
