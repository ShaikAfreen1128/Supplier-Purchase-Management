from sqlalchemy.orm import Session
from models import supplier_models
from schemas import supplier_schemas as schemas
from datetime import datetime
from fastapi import HTTPException

#  SUPPLIER SERVICES
def create_supplier(db: Session, supplier: schemas.SupplierCreate):
    if not supplier.contact.isdigit() or len(supplier.contact) != 10:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid 10-digit contact number."
        )

    new_supplier = supplier_models.Supplier(
        name=supplier.name,
        contact=supplier.contact,
        address=supplier.address,
    )
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

def get_suppliers(db: Session):
    return db.query(supplier_models.Supplier).all()

#  PURCHASE ORDER SERVICES 
def create_purchase_order(db: Session, po_data: schemas.PurchaseOrderCreate):
    po = supplier_models.PurchaseOrder(supplier_id=po_data.supplier_id)
    db.add(po)
    db.commit()
    db.refresh(po)

    for item in po_data.items:
        po_item = supplier_models.PurchaseOrderItem(
            order_id=po.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_cost=item.unit_cost,
        )
        db.add(po_item)

    db.commit()
    db.refresh(po)
    return po
def mark_order_received(db: Session, order_id: int):
    po = db.query(supplier_models.PurchaseOrder).filter(
        supplier_models.PurchaseOrder.id == order_id
    ).first()
    if not po:
        return None

    po.status = "received"
    db.commit()
    for item in po.items:
        inv = (
            db.query(supplier_models.Inventory)
            .filter(supplier_models.Inventory.product_id == item.product_id)
            .first()
        )
        if inv:
            inv.quantity += item.quantity
        else:
            new_inv = supplier_models.Inventory(
                product_id=item.product_id,
                quantity=item.quantity,
                last_updated=datetime.now(),
            )
            db.add(new_inv)

    db.commit()
    db.refresh(po)
    return po

# INVENTORY SERVICES 
def get_inventory(db: Session):
    return db.query(supplier_models.Inventory).all()
