# app/schemas.py

from decimal import Decimal
from typing import List
from app.models import OrderStatus
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import  Optional

# ============ 客户 ============
class CustomerBase(BaseModel):
    name: str
    contact: Optional[str] = None
    phone: Optional[str] = None





# ============ 加工件明细 ============
class OrderItemBase(BaseModel):
    part_name: Optional[str] = None
    material: Optional[str] = None
    quantity: int = 1
    unit_price: Decimal = Decimal("0")
    process_req: Optional[str] = None

class OrderItemCreate(BaseModel):
    part_name: Optional[str] = None
    material: Optional[str] = None
    quantity: int = 1
    unit_price: Decimal = Decimal("0")
    process_req: Optional[str] = None

class OrderItemUpdate(BaseModel):
    part_name: Optional[str] = None
    material: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    process_req: Optional[str] = None

class OrderItemOut(BaseModel):
    id: int
    order_id: int
    part_name: Optional[str] = None
    material: Optional[str] = None
    quantity: int
    unit_price: Decimal
    process_req: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# ============ 订单 ============
class OrderBase(BaseModel):
    order_no: str
    customer_id: int
    status: OrderStatus = OrderStatus.PENDING
    due_date: Optional[datetime] = None
    remark: Optional[str] = None

class OrderCreate(BaseModel):
    order_no: str
    customer_id: int
    status: OrderStatus = OrderStatus.PENDING
    due_date: Optional[datetime] = None
    remark: Optional[str] = None
    items: List[OrderItemCreate] = []

class OrderUpdate(BaseModel):
    due_date: Optional[datetime] = None
    remark: Optional[str] = None
    # 注意：不包含 status，状态走专门的接口

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderOut(BaseModel):
    id: int
    order_no: str
    customer_id: int
    status: OrderStatus
    due_date: Optional[datetime] = None
    total_amount: Decimal
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []
    model_config = ConfigDict(from_attributes=True)

# ============ 客户 ============
class CustomerCreate(BaseModel):
    name: str
    contact: Optional[str] = None
    phone: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    phone: Optional[str] = None

class CustomerOut(BaseModel):
    id: int
    name: str
    contact: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)