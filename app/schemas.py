from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, field_validator


def sanitize_str(v: str) -> str:
    return v.strip()[:500] if v else v


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        v = v.strip()
        if len(v) < 3 or len(v) > 30:
            raise ValueError("Username must be 3-30 characters")
        if not v.isalnum() and "_" not in v:
            raise ValueError("Username can only contain letters, numbers, underscore")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email address")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a number")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


# --- Product Schemas ---
class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    stock: int = 0
    image_url: str = ""
    category: str = ""

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        return sanitize_str(v)

    @field_validator("description")
    @classmethod
    def validate_desc(cls, v):
        return v.strip()[:2000] if v else ""

    @field_validator("image_url")
    @classmethod
    def validate_url(cls, v):
        if v and not v.startswith(("http://", "https://", "/")):
            raise ValueError("Invalid image URL")
        return v[:500] if v else ""

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        if v > 999999:
            raise ValueError("Price too high")
        return round(v, 2)

    @field_validator("stock")
    @classmethod
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError("Stock cannot be negative")
        return v


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    image_url: str
    category: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Cart Schemas ---
class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int

    model_config = {"from_attributes": True}


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: float


# --- Order Schemas ---
class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    created_at: datetime
    items: list[CartItemResponse]

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: str
