from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas, crud

# 注意 prefix 里带 order_id，路径更清晰
router = APIRouter(prefix="/orders/{order_id}/items", tags=["order-items"])


# ---------- 增 ----------
@router.post("", response_model=schemas.OrderItemOut)
def create_item(order_id: int,
                payload: schemas.OrderItemCreate,
                db: Session = Depends(get_db)):
    return crud.create_order_item(
        db,
        order_id=order_id,
        part_name=payload.part_name,
        material=payload.material,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
        process_req=payload.process_req,
    )


# ---------- 查（某订单的全部明细） ----------
@router.get("", response_model=List[schemas.OrderItemOut])
def list_items(order_id: int, db: Session = Depends(get_db)):
    return crud.list_order_items(db, order_id)


# ---------- 查（单条明细） ----------
@router.get("/{item_id}", response_model=schemas.OrderItemOut)
def get_item(order_id: int, item_id: int, db: Session = Depends(get_db)):
    return crud.get_order_item(db, item_id)


# ---------- 改 ----------
@router.patch("/{item_id}", response_model=schemas.OrderItemOut)
def update_item(order_id: int, item_id: int,
                payload: schemas.OrderItemUpdate,
                db: Session = Depends(get_db)):
    return crud.update_order_item(
        db, item_id,
        **payload.model_dump(exclude_unset=True),
    )


# ---------- 删 ----------
@router.delete("/{item_id}")
def delete_item(order_id: int, item_id: int, db: Session = Depends(get_db)):
    crud.delete_order_item(db, item_id)
    return {"ok": True}