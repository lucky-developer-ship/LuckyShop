from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    product_count = db.query(func.count(models.Product.id)).scalar()
    user_count = db.query(func.count(models.User.id)).scalar()
    return {"products": product_count, "users": user_count}


@router.get("/", response_model=list[schemas.ProductResponse])
def list_products(
    category: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
