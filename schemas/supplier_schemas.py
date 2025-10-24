from pydantic import BaseModel, field_serializer, field_validator
from pydantic_core import PydanticCustomError
from typing import List, Optional
from datetime import datetime
import pytz
import re

IST = pytz.timezone("Asia/Kolkata")

class SupplierBase(BaseModel):
    name: str
    contact: str
    address: str

    @field_validator("address")
    def validate_address(cls, v):
        if not v or not v.strip():
            raise ValueError("Supplier address is required. Please enter the address.")
        v = v.strip()
        if v.lower() == "string":
            raise ValueError("Enter a valid address, not a placeholder like 'string'.")
        return v.strip()
    @field_validator("contact")
    def validate_contact(cls, v):
        if not v or not v.strip():
            raise ValueError("Supplier contact number is required.")
        v = v.strip()
        if not re.match(r"^[6-9]\d{9}$", v):
            raise ValueError("Enter a valid 10-digit mobile number starting with 6, 7, 8, or 9.")
        return v


class SupplierCreate(SupplierBase):
 
    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip() if v else ""
        if not v:
            raise PydanticCustomError(
                "value_error.name_required",
                "Supplier name is required. Please enter the supplier name.",
            )
        if v.lower() == "string":
            raise PydanticCustomError(
                "value_error.invalid_name",
                "Enter a valid supplier name, not a placeholder like 'string'.",
            )
        return v




class SupplierOut(BaseModel):
    id: int
    name: str
    contact: str
    address: str

    class Config:
        orm_mode = True


class PurchaseOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_cost: float


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass


class PurchaseOrderItemOut(PurchaseOrderItemBase):
    id: int
    received_quantity: int = 0

    class Config:
        orm_mode = True


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    items: List[PurchaseOrderItemCreate]


class PurchaseOrderOut(BaseModel):
    id: int
    supplier_id: int
    status: str
    created_at: Optional[datetime] = None
    items: List[PurchaseOrderItemOut] = []

    class Config:
        orm_mode = True

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: Optional[datetime], _info):
        if not created_at:
            return None
        ist_time = created_at.astimezone(IST)
        return ist_time.strftime("%d-%b-%Y %I:%M:%S %p IST")


class ReceivedItem(BaseModel):
    product_id: int
    received_quantity: int


class ReceiveOrder(BaseModel):
    received_items: List[ReceivedItem]


class InventoryOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True

    @field_serializer("last_updated")
    def serialize_last_updated(self, last_updated: Optional[datetime], _info):
        if not last_updated:
            return None
        ist_time = last_updated.astimezone(IST)
        return ist_time.strftime("%d-%b-%Y %I:%M:%S %p IST")
