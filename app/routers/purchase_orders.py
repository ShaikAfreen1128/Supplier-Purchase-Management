from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import supplier_schemas as schemas
from services import supplier_service
from models import supplier_models

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])

@router.post("/", response_model=schemas.PurchaseOrderOut)
def create_po(po: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    return supplier_service.create_purchase_order(db, po)

@router.put(
    "/{order_id}/tracking",
    summary="Purchase Tracking",
    description="Track and update received quantities for a purchase order."
)
def purchase_tracking(order_id: int, data: schemas.ReceiveOrder, db: Session = Depends(get_db)):
    if not data.received_items:
        raise HTTPException(status_code=400, detail="No items provided to mark as received.")
    return supplier_service.mark_order_received(db, order_id, data.received_items)

@router.get("/{order_id}/items")
def get_items_by_status(
    order_id: int,
    status: str = Query(..., enum=["pending", "partial", "received"]),
    db: Session = Depends(get_db),
):
    po = (
        db.query(supplier_models.PurchaseOrder)
        .filter(supplier_models.PurchaseOrder.id == order_id)
        .first()
    )

    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    filtered_items = []
    for item in po.items:
        if item.received_quantity == item.quantity:
            item_status = "received"
        elif item.received_quantity > 0:
            item_status = "partial"
        else:
            item_status = "pending"

        if item_status == status:
            filtered_items.append({
                "product_id": item.product_id,
                "ordered_quantity": item.quantity,
                "received_quantity": item.received_quantity,
                "unit_cost": item.unit_cost,
                "status": item_status,
            })

    if not filtered_items:
        return {
            "order_id": order_id,
            "selected_status": status,
            "total_items": 0,
            "message": f"No items found for status '{status}'."
        }

    return {
        "order_id": order_id,
        "selected_status": status,
        "total_items": len(filtered_items),
        "items": filtered_items,
    }
