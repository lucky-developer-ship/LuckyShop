from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr


# --- User Schemas ---
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


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
