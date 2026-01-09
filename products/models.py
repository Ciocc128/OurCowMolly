from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean
from sqlalchemy.sql import func

from core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    # unit = add later (try to understand in which type of unit you sell your product)
    price = Column(DECIMAL, nullable=False)
    in_stock = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

