from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/", response_model=schemas.OrderResponse)
def place_order(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0.0
    order_items = []
    for cart_item in cart_items:
        product = cart_item.product
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}",
            )
        product.stock -= cart_item.quantity
        total_price += product.price * cart_item.quantity
        order_items.append(
            {
                "product_id": product.id,
                "quantity": cart_item.quantity,
                "price_at_purchase": product.price,
            }
        )

    order = models.Order(
        user_id=current_user.id, total_price=round(total_price, 2)
    )
    db.add(order)
    db.flush()

    for oi in order_items:
        db.add(models.OrderItem(order_id=order.id, **oi))

    for cart_item in cart_items:
        db.delete(cart_item)

    db.commit()
    db.refresh(order)

    response_items = [
        schemas.CartItemResponse(
            id=oi.id,
            product_id=oi.product_id,
            product_name=oi.product.name,
            product_price=oi.price_at_purchase,
            quantity=oi.quantity,
        )
        for oi in order.items
    ]
    return schemas.OrderResponse(
        id=order.id,
        total_price=order.total_price,
        status=order.status,
        created_at=order.created_at,
        items=response_items,
    )


@router.get("/", response_model=list[schemas.OrderResponse])
def get_orders(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.id)
        .order_by(models.Order.created_at.desc())
        .all()
    )
    result = []
    for order in orders:
        items = [
            schemas.CartItemResponse(
                id=oi.id,
                product_id=oi.product_id,
                product_name=oi.product.name,
                product_price=oi.price_at_purchase,
                quantity=oi.quantity,
            )
            for oi in order.items
        ]
        result.append(
            schemas.OrderResponse(
                id=order.id,
                total_price=order.total_price,
                status=order.status,
                created_at=order.created_at,
                items=items,
            )
        )
    return result
