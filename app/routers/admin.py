from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/admin", tags=["admin"])


def get_admin_user(current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/users", response_model=list[schemas.UserResponse])
def list_users(
    admin: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    users = db.query(models.User).all()
    return [
        schemas.UserResponse(
            id=u.id, username=u.username, email=u.email,
            is_active=u.is_active, created_at=u.created_at
        ) for u in users
    ]


@router.get("/orders", response_model=list[schemas.OrderResponse])
def list_all_orders(
    admin: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).all()
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


@router.patch("/orders/{order_id}")
def update_order_status(
    order_id: int,
    status: schemas.OrderStatusUpdate,
    admin: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status.status
    db.commit()
    return {"message": "Order updated"}


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    admin: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


@router.get("/stats")
def admin_stats(
    admin: models.User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    from sqlalchemy import func
    products = db.query(func.count(models.Product.id)).scalar()
    users = db.query(func.count(models.User.id)).scalar()
    orders = db.query(func.count(models.Order.id)).scalar()
    revenue = db.query(func.coalesce(func.sum(models.Order.total_price), 0)).scalar()
    return {
        "products": products,
        "users": users,
        "orders": orders,
        "revenue": round(float(revenue), 2),
    }
