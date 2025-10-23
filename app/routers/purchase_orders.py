from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import supplier_schemas as schemas
from services import supplier_service

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])

@router.post("/", response_model=schemas.PurchaseOrderOut)
def create_po(po: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    return supplier_service.create_purchase_order(db, po)

@router.put("/{order_id}/receive", response_model=schemas.PurchaseOrderOut)
def receive_po(order_id: int, db: Session = Depends(get_db)):
    po = supplier_service.mark_order_received(db, order_id)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return po
