from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
import httpx
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/auth/google", tags=["google-auth"])

GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
GOOGLE_REDIRECT_URI = "http://127.0.0.1:8000/api/auth/google/callback"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@router.get("/login")
def google_login():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return RedirectResponse(f"{GOOGLE_AUTH_URL}?{query}")


@router.get("/callback")
async def google_callback(code: str = "", db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="No authorization code")

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(GOOGLE_TOKEN_URL, data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        })
        if token_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get token")

        access_token = token_resp.json().get("access_token")
        user_resp = await client.get(GOOGLE_USERINFO_URL, headers={
            "Authorization": f"Bearer {access_token}"
        })
        if user_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info")

        user_info = user_resp.json()

    email = user_info.get("email")
    name = user_info.get("name", email.split("@")[0])

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        username = name.replace(" ", "").lower()
        base_username = username
        counter = 1
        while db.query(models.User).filter(models.User.username == username).first():
            username = f"{base_username}{counter}"
            counter += 1

        user = models.User(
            username=username,
            email=email,
            hashed_password=auth.get_password_hash("google_oauth_no_password"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = auth.create_access_token(data={"sub": user.username})

    html = f"""
    <html><body><script>
        window.opener.postMessage({{token: "{jwt_token}", username: "{user.username}"}}, "*");
        window.close();
    </script></body></html>
    """
    return HTMLResponse(content=html)


from pydantic import BaseModel

class TokenRequest(BaseModel):
    id_token: str

@router.post("/token")
async def google_token(req: TokenRequest, db: Session = Depends(get_db)):
    id_token = req.id_token
    async with httpx.AsyncClient() as client:
        user_resp = await client.get(GOOGLE_USERINFO_URL, headers={
            "Authorization": f"Bearer {id_token}"
        })
        if user_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid token")
        user_info = user_resp.json()

    email = user_info.get("email")
    name = user_info.get("name", email.split("@")[0])

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        username = name.replace(" ", "").lower()
        base_username = username
        counter = 1
        while db.query(models.User).filter(models.User.username == username).first():
            username = f"{base_username}{counter}"
            counter += 1

        user = models.User(
            username=username,
            email=email,
            hashed_password=auth.get_password_hash("google_oauth_no_password"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": jwt_token, "token_type": "bearer", "username": user.username}
