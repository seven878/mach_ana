# test_status_flow.py
from database import SessionLocal
import crud
from models import OrderStatus
from exceptions import InvalidStatusTransitionError, NotFoundError


def expect_ok(db, order_id, target):
    o = crud.update_order_status(db, order_id, target)
    print(f"✓ {target.value} 成功，当前状态 = {o.status.value}")


def expect_fail(db, order_id, target):
    try:
        crud.update_order_status(db, order_id, target)
        print(f"✗ 本应失败却成功了：{target.value}")
    except InvalidStatusTransitionError as e:
        print(f"✓ 正确拦截：{e.message}")


def main():
    db = SessionLocal()
    try:
        c = crud.create_customer(db, name="测试客户")
        o = crud.create_order(db, order_no="MO-T-001", customer_id=c.id)

        expect_ok(db, o.id, OrderStatus.TO_PRODUCTION)
        expect_ok(db, o.id, OrderStatus.IN_PRODUCTION)
        expect_ok(db, o.id, OrderStatus.TO_PRODUCTION)   # 退回
        expect_ok(db, o.id, OrderStatus.IN_PRODUCTION)
        expect_ok(db, o.id, OrderStatus.FINISHED)
        expect_ok(db, o.id, OrderStatus.SHIPPED)

        expect_fail(db, o.id, OrderStatus.IN_PRODUCTION)  # 终态

        # 取消流程
        o2 = crud.create_order(db, order_no="MO-T-002", customer_id=c.id)
        expect_ok(db, o2.id, OrderStatus.CANCELLED)
        expect_fail(db, o2.id, OrderStatus.TO_PRODUCTION)

        # 不存在的订单
        try:
            crud.update_order_status(db, 99999, OrderStatus.FINISHED)
        except NotFoundError as e:
            print(f"✓ 正确抛 NotFound：{e.message}")

    finally:
        db.close()


if __name__ == "__main__":
    main()