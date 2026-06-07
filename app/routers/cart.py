from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/cart", tags=["cart"])


class CartItemUpdate(BaseModel):
    quantity: int


@router.get("/", response_model=schemas.CartResponse)
def get_cart(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    cart_items = []
    total = 0.0
    for item in items:
        product = item.product
        cart_items.append(
            schemas.CartItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=product.name,
                product_price=product.price,
                quantity=item.quantity,
            )
        )
        total += product.price * item.quantity
    return schemas.CartResponse(items=cart_items, total=round(total, 2))


@router.post("/add", response_model=schemas.CartResponse)
def add_to_cart(
    item: schemas.CartItemAdd,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    existing = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.user_id == current_user.id,
            models.CartItem.product_id == item.product_id,
        )
        .first()
    )
    if existing:
        existing.quantity += item.quantity
    else:
        existing = models.CartItem(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.add(existing)
    db.commit()

    return get_cart(current_user=current_user, db=db)


@router.patch("/{item_id}", response_model=schemas.CartResponse)
def update_cart_item(
    item_id: int,
    update: CartItemUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    cart_item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.id == item_id,
            models.CartItem.user_id == current_user.id,
        )
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if update.quantity <= 0:
        db.delete(cart_item)
    else:
        product = cart_item.product
        if product.stock < update.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")
        cart_item.quantity = update.quantity

    db.commit()
    return get_cart(current_user=current_user, db=db)


@router.delete("/{item_id}", response_model=schemas.CartResponse)
def remove_from_cart(
    item_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    cart_item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.id == item_id,
            models.CartItem.user_id == current_user.id,
        )
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()
    return get_cart(current_user=current_user, db=db)
