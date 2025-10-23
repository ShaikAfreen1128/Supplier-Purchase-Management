from pydantic import BaseModel, validator
from datetime import datetime
import pytz
import re

IST = pytz.timezone("Asia/Kolkata")

class SupplierBase(BaseModel):
    name: str
    contact: str
    address: str

    @validator("contact")
    def validate_contact(cls, v):
        cleaned = re.sub(r"\D", "", v)  
        if len(cleaned) != 10:
            raise ValueError("Enter a valid 10-digit mobile number")
        return cleaned

class SupplierCreate(SupplierBase):
    pass

class SupplierOut(SupplierBase):
    id: int

    class Config:
        orm_mode = True

class PurchaseOrderItem(BaseModel):
    product_id: int
    quantity: int
    unit_cost: float

class PurchaseOrderBase(BaseModel):
    supplier_id: int
    items: list[PurchaseOrderItem]

class PurchaseOrderCreate(PurchaseOrderBase):
    pass

class PurchaseOrderOut(PurchaseOrderBase):
    id: int
    status: str
    created_at: str

    class Config:
        orm_mode = True

    @validator("created_at", pre=True, always=True)
    def format_created_at(cls, v):
        if v is None:
            return None
        if isinstance(v, datetime):
            v = v.astimezone(IST)
            return v.strftime("%I:%M %p, %d %b %Y")
        return v
