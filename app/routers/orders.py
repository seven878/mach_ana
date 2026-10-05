from app.database import get_db
from app import schemas, crud
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/orders", tags=["orders"])
# app/routers/orders.py
@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
def change_order_status(order_id: int,
                        payload: schemas.OrderStatusUpdate,
                        db: Session = Depends(get_db)):
    return crud.update_order_status(db, order_id, payload.status)
    # 订单不存在 → 自动 404
    # 非法流转   → 自动 400，还带详细信息
    # 成功       → 200 + 订单 JSON


from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import OrderStatus

router = APIRouter(prefix="/orders", tags=["orders"])


# ---------- 增（可级联写明细） ----------
@router.post("", response_model=schemas.OrderOut)
def create_order(payload: schemas.OrderCreate,
                 db: Session = Depends(get_db)):
    """
    接收 JSON：
    {
      "order_no": "MO-001",
      "customer_id": 1,
      "status": "to_production",
      "due_date": "2026-02-01T00:00:00",
      "remark": "急件",
      "items": [
        {"part_name": "传动轴", "quantity": 10, "unit_price": 85.5}
      ]
    }
    """
    return crud.create_order(
        db,
        order_no=payload.order_no,
        customer_id=payload.customer_id,
        status=payload.status,
        due_date=payload.due_date,
        remark=payload.remark,
        items=payload.items,          # list[OrderItemCreate]，crud 内部会处理
    )


# ---------- 查（列表，可按状态/客户过滤） ----------
@router.get("", response_model=List[schemas.OrderOut])
def list_orders(
    status: Optional[OrderStatus] = Query(None, description="按状态过滤"),
    customer_id: Optional[int] = Query(None, description="按客户过滤"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.list_orders(db, status=status,
                            customer_id=customer_id,
                            skip=skip, limit=limit)


# ---------- 查（详情） ----------
@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order(db, order_id)


# ---------- 改（基础字段，不含 status） ----------
@router.patch("/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: int,
                 payload: schemas.OrderUpdate,
                 db: Session = Depends(get_db)):
    return crud.update_order(
        db, order_id,
        **payload.model_dump(exclude_unset=True),
    )


# ---------- 改（状态流转，走校验） ----------
@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
def change_order_status(order_id: int,
                        payload: schemas.OrderStatusUpdate,
                        db: Session = Depends(get_db)):
    """
    合法流转：
      pending       -> to_production / cancelled
      to_production -> in_production
      in_production -> finished / to_production
      finished      -> shipped
    """
    return crud.update_order_status(db, order_id, payload.status)


# ---------- 删 ----------
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    crud.delete_order(db, order_id)
    return {"ok": True}