from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


# ============ 枚举：订单状态 ============
class OrderStatus(str, enum.Enum):
    """订单状态枚举，值存入数据库为字符串"""
    PENDING = "pending"                # 待定
    TO_PRODUCTION = "to_production"    # 待生产
    IN_PRODUCTION = "in_production"    # 生产中
    FINISHED = "finished"              # 生产完成
    SHIPPED = "shipped"                # 已发货
    CANCELLED = "cancelled"            # 已取消


# ============ 客户表 ============
class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {"comment": "客户"}

    id = Column(Integer, primary_key=True, comment="主键ID")
    name = Column(String(255), nullable=False, comment="客户公司名")
    contact = Column(String(255), comment="联系方式")
    phone = Column(String(255), comment="手机号")
    created_at = Column(DateTime, server_default=func.now(), comment="建立日期")

    # 关系
    orders = relationship("Order", back_populates="customer")


# ============ 订单表 ============
class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"comment": "订单"}

    id = Column(Integer, primary_key=True, comment="主键ID")
    order_no = Column(String(255), nullable=False, unique=True, comment="订单编号")
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False, comment="客户ID")
    status = Column(
        SAEnum(OrderStatus, name="order_status", native_enum=False, length=255),
        default=OrderStatus.PENDING,
        comment="状态：pending待定/to_production待生产/in_production生产中/finished生产完成/shipped已发货/cancelled已取消",
    )
    due_date = Column(DateTime, comment="交期")
    total_amount = Column(Numeric(12, 2), default=0, comment="总数")
    remark = Column(String(255), comment="备注")
    created_at = Column(DateTime, server_default=func.now(), comment="建立日期")
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="最后修改日期",
    )

    # 关系
    customer = relationship("Customer", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )


# ============ 加工件明细表 ============
class OrderItem(Base):
    __tablename__ = "order_item"
    __table_args__ = {"comment": "加工件明细"}

    id = Column(Integer, primary_key=True, comment="主键ID")
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"),
                      nullable=False, comment="订单ID")
    part_name = Column(String(255), comment="零件名")
    material = Column(String(255), comment="材料")
    quantity = Column(Integer, default=1, comment="数量")
    unit_price = Column(Numeric(10, 2), default=0, comment="单价")
    process_req = Column(String(255), comment="工艺要求")
    created_at = Column(DateTime, server_default=func.now(), comment="建立日期")

    # 关系
    order = relationship("Order", back_populates="items")