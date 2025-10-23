from fastapi import FastAPI
from database import Base, engine
from models import supplier_models 
from app.routers import suppliers, purchase_orders, inventory


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(suppliers.router)
app.include_router(purchase_orders.router)
app.include_router(inventory.router)
