from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import supplier_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=list[dict])
def get_inventory(db: Session = Depends(get_db)):
    inventory = supplier_service.get_inventory(db)
    return [{"product_id": i.product_id, "quantity": i.quantity} for i in inventory]
