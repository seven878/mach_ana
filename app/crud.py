"""
CRUD 层：所有数据库操作集中在这里，路由层只调用这些函数。
分三块：Customer / Order / OrderItem
"""

# app/crud.py
from decimal import Decimal
from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import app.models as models
from app.models import OrderStatus
from app.exceptions import (
    NotFoundError,
    InvalidStatusTransitionError,
    DuplicateError,
)


# =========================================================
# 客户 CRUD
# =========================================================


def get_customer_by_name(db: Session, name: str) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.name == name).first()


def list_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    return db.query(models.Customer).order_by(models.Customer.id.desc()).offset(skip).limit(limit).all()



def update_customer(db, customer_id, **fields):
    obj = db.get(models.Customer, customer_id)
    if not obj:
        raise NotFoundError("客户", customer_id)
    for k, v in fields.items():
        if v is not None and hasattr(obj, k):
            setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

# =========================================================
# 订单 CRUD
# =========================================================

def _calc_total(items) -> Decimal:
    """根据明细计算订单总额"""
    total = Decimal("0")
    for it in items:
        qty = it.get("quantity", 0) if isinstance(it, dict) else it.quantity
        price = it.get("unit_price", 0) if isinstance(it, dict) else it.unit_price
        total += Decimal(str(qty)) * Decimal(str(price))
    return total


def get_order_by_no(db: Session, order_no: str) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.order_no == order_no).first()


def list_orders(db: Session, *, status: OrderStatus = None,
                customer_id: int = None,
                skip: int = 0, limit: int = 100) -> List[models.Order]:
    q = db.query(models.Order)
    if status is not None:
        q = q.filter(models.Order.status == status)
    if customer_id is not None:
        q = q.filter(models.Order.customer_id == customer_id)
    return q.order_by(models.Order.id.desc()).offset(skip).limit(limit).all()


# =========================================================
# 订单状态流转校验
# =========================================================

ORDER_STATUS_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.TO_PRODUCTION, OrderStatus.CANCELLED},
    OrderStatus.TO_PRODUCTION: {OrderStatus.IN_PRODUCTION},
    OrderStatus.IN_PRODUCTION: {OrderStatus.FINISHED, OrderStatus.TO_PRODUCTION},
    OrderStatus.FINISHED: {OrderStatus.SHIPPED},
    OrderStatus.SHIPPED: set(),
    OrderStatus.CANCELLED: set(),
}


def is_transition_allowed(current: OrderStatus, target: OrderStatus) -> bool:
    if current == target:
        return False
    return target in ORDER_STATUS_TRANSITIONS.get(current, set())


def validate_transition(current: OrderStatus, target: OrderStatus) -> None:
    """非法流转抛 InvalidStatusTransitionError"""
    if current == target:
        raise InvalidStatusTransitionError(
            current, target, ORDER_STATUS_TRANSITIONS.get(current, set())
        )
    if not is_transition_allowed(current, target):
        raise InvalidStatusTransitionError(
            current, target, ORDER_STATUS_TRANSITIONS.get(current, set())
        )


def update_order_status(db: Session, order_id: int,
                        status: OrderStatus) -> models.Order:
    """
    状态更新。订单不存在抛 NotFoundError；
    非法流转抛 InvalidStatusTransitionError。
    成功返回更新后的 Order。
    """
    obj = db.get(models.Order, order_id)
    if not obj:
        raise NotFoundError("订单", order_id)

    validate_transition(obj.status, status)

    obj.status = status
    db.commit()
    db.refresh(obj)
    return obj


def recalc_order_total(db: Session, order_id: int) -> Optional[models.Order]:
    """重新汇总订单总额（明细增删改后调用）"""
    obj = db.get(models.Order, order_id)
    if not obj:
        return None
    obj.total_amount = _calc_total(obj.items)
    db.commit()
    db.refresh(obj)
    return obj


# =========================================================
# 加工件明细 CRUD
# =========================================================

def create_order_item(db: Session, *, order_id: int, part_name: str = None,
                      material: str = None, quantity: int = 1,
                      unit_price: Decimal = Decimal("0"),
                      process_req: str = None) -> models.OrderItem:
    item = models.OrderItem(
        order_id=order_id,
        part_name=part_name,
        material=material,
        quantity=quantity,
        unit_price=unit_price,
        process_req=process_req,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    # 同步订单总额
    recalc_order_total(db, order_id)
    return item


def list_order_items(db: Session, order_id: int) -> List[models.OrderItem]:
    return (
        db.query(models.OrderItem)
        .filter(models.OrderItem.order_id == order_id)
        .order_by(models.OrderItem.id.asc())
        .all()
    )


def update_order_item(db: Session, item_id: int, **fields) -> Optional[models.OrderItem]:
    obj = db.get(models.OrderItem, item_id)
    if not obj:
        return None
    for k, v in fields.items():
        if v is not None and hasattr(obj, k):
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    recalc_order_total(db, obj.order_id)
    return obj


# ---------- 客户 ----------

def create_customer(db: Session, *, name: str, contact: str = None,
                    phone: str = None) -> models.Customer:
    obj = models.Customer(name=name, contact=contact, phone=phone)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_customer(db: Session, customer_id: int) -> models.Customer:
    obj = db.get(models.Customer, customer_id)
    if not obj:
        raise NotFoundError("客户", customer_id)
    return obj


def delete_customer(db: Session, customer_id: int) -> None:
    obj = db.get(models.Customer, customer_id)
    if not obj:
        raise NotFoundError("客户", customer_id)
    db.delete(obj)
    db.commit()


# ---------- 订单 ----------

def create_order(db: Session, *, order_no: str, customer_id: int,
                 status: OrderStatus = OrderStatus.PENDING,
                 due_date=None, remark: str = None,
                 items: list = None) -> models.Order:
    items = items or []

    # 客户必须存在
    if not db.get(models.Customer, customer_id):
        raise NotFoundError("客户", customer_id)

    item_objs = []
    for it in items:
        data = it if isinstance(it, dict) else it.model_dump()
        item_objs.append(models.OrderItem(**data))

    total = _calc_total(item_objs)

    order = models.Order(
        order_no=order_no,
        customer_id=customer_id,
        status=status,
        due_date=due_date,
        total_amount=total,
        remark=remark,
        items=item_objs,
    )
    db.add(order)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateError("订单", "order_no", order_no)
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> models.Order:
    obj = db.get(models.Order, order_id)
    if not obj:
        raise NotFoundError("订单", order_id)
    return obj


def delete_order(db: Session, order_id: int) -> None:
    obj = db.get(models.Order, order_id)
    if not obj:
        raise NotFoundError("订单", order_id)
    db.delete(obj)
    db.commit()


def update_order(db: Session, order_id: int, **fields) -> models.Order:
    """更新基础字段（不含 status），status 必须走 update_order_status"""
    fields.pop("status", None)
    obj = db.get(models.Order, order_id)
    if not obj:
        raise NotFoundError("订单", order_id)
    for k, v in fields.items():
        if v is not None and hasattr(obj, k):
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


# ---------- 明细 ----------

def get_order_item(db: Session, item_id: int) -> models.OrderItem:
    obj = db.get(models.OrderItem, item_id)
    if not obj:
        raise NotFoundError("加工件明细", item_id)
    return obj


def delete_order_item(db: Session, item_id: int) -> None:
    obj = db.get(models.OrderItem, item_id)
    if not obj:
        raise NotFoundError("加工件明细", item_id)
    order_id = obj.order_id
    db.delete(obj)
    db.commit()
    recalc_order_total(db, order_id)
