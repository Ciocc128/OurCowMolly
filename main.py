from fastapi import FastAPI

from core.database import Base, engine
from products.routers import router as products_router

# Import models SQLAlchemy registers tables before create_all
from products import models as _products_model
from customers import models as _customers_model
from orders import models as _orders_model

app = FastAPI(title= "OurCowMolly API")

# dev-only mode, I need to create tables (later I will migrate them)
Base.metadata.create_all(bind=engine)

#Routers
app.include_router(products_router)

@app.get("/")
def index():
    return {"message": "OurCowMolly API is running!"}