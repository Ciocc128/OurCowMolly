from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, index=True)
    # unit = add later (try to understand in which type of unit you sell your product)
    price = Column(Numeric(10,2), nullable=False)
    in_stock = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # ORM relationships
    order_items = relationship("OrderItem", back_populates="product")