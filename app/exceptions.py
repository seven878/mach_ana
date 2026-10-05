"""
业务异常：CRUD 层抛出，Router 层捕获转成 HTTP 响应。
不依赖任何 Web 框架，纯业务语义。
"""


class BusinessError(Exception):
    """所有业务异常的基类"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(BusinessError):
    """资源不存在"""
    def __init__(self, resource: str, key):
        super().__init__(f"{resource} 不存在：{key}")
        self.resource = resource
        self.key = key


class InvalidStatusTransitionError(BusinessError):
    """非法的订单状态流转"""
    def __init__(self, current, target, allowed):
        self.current = current
        self.target = target
        self.allowed = allowed
        allowed_str = "、".join(s.value for s in allowed) or "无（终态）"
        super().__init__(
            f"不允许的状态流转：{current.value} -> {target.value}；"
            f"当前状态 {current.value} 只能流转到：{allowed_str}"
        )


class DuplicateError(BusinessError):
    """唯一约束冲突，比如订单号重复"""
    def __init__(self, resource: str, field: str, value):
        super().__init__(f"{resource} 的 {field} 已存在：{value}")
        self.resource = resource
        self.field = field
        self.value = value