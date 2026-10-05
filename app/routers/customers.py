from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
import app.schemas as schemas
import app.crud as crud


router = APIRouter(prefix="/customers", tags=["customers"])


# ---------- 增 ----------
@router.post("", response_model=schemas.CustomerOut)
def create_customer(payload: schemas.CustomerCreate,
                    db: Session = Depends(get_db)):
    """
    接收 JSON：
    { "name": "苏州精密", "contact": "张工", "phone": "138..." }
    """
    return crud.create_customer(
        db,
        name=payload.name,
        contact=payload.contact,
        phone=payload.phone,
    )


# ---------- 查（列表） ----------
@router.get("", response_model=List[schemas.CustomerOut])
def list_customers(skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db)):
    return crud.list_customers(db, skip=skip, limit=limit)


# ---------- 查（详情） ----------
@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_customer(db, customer_id)


# ---------- 改 ----------
@router.patch("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int,
                    payload: schemas.CustomerUpdate,
                    db: Session = Depends(get_db)):
    # exclude_unset=True：只更新客户端真正传了的字段
    return crud.update_customer(
        db, customer_id,
        **payload.model_dump(exclude_unset=True),
    )


# ---------- 删 ----------
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    crud.delete_customer(db, customer_id)
    return {"ok": True}