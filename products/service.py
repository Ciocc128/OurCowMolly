from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import Product
from .schemas import ProductCreate, ProductUpdate

def create_product(db: Session, payload: ProductCreate) -> Product:
   print(f"[DEBUG] Creating product with name={payload.name}, price={payload.price}, in_stock={payload.in_stock}")  # Debug: stampa i dati prima del commit
   product = Product(
       name = payload.name,
       price = payload.price,
       in_stock = payload.in_stock
   )
   db.add(product)
   db.commit()
   db.refresh(product)
   print(f"[DEBUG] Created product: {product}")  # Debug: stampa il prodotto creato
   return product

def list_products(db: Session) -> list[Product]:
    result = db.execute(select(Product).order_by(Product.id))
    products = result.scalars().all()
    return products

def get_product_by_id(db: Session, product_id: int) -> Product | None:
    result = db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    return product

def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product | None:
    product = get_product_by_id(db=db, product_id=product_id)

    if product is None:
        return None
    
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> dict | None:
    result = db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if product is None:
        return None
    
    db.delete(product)
    db.commit()
    return {"message": f"Product with ID={product_id} successfully deleted!"}
    