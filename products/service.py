from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import Product
from .schemas import ProductCreate

def create_product(db: Session, payload: ProductCreate) -> Product:
   product = Product(
       name = payload.name,
       price = payload.price,
       in_stock = payload.in_stock
   )
   db.add(product)
   db.commit()
   db.refresh(product)
   return product


def list_products(db: Session) -> list[Product]:
    result = db.execute(select(Product).order_by(Product.id))
    products = result.scalars().all()
    return products