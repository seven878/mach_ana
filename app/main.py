# app/main.py
from fastapi import FastAPI, Request

from app.exceptions import (
    NotFoundError,
    InvalidStatusTransitionError,
    DuplicateError,
    BusinessError,
)

app = FastAPI(title="Machining Order System")


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(InvalidStatusTransitionError)
async def invalid_transition_handler(request: Request,
                                     exc: InvalidStatusTransitionError):
    return JSONResponse(status_code=400, content={
        "detail": exc.message,
        "current": exc.current.value,
        "target": exc.target.value,
        "allowed": [s.value for s in exc.allowed],
    })


@app.exception_handler(DuplicateError)
async def duplicate_handler(request: Request, exc: DuplicateError):
    return JSONResponse(status_code=409, content={"detail": exc.message})


@app.exception_handler(BusinessError)
async def business_handler(request: Request, exc: BusinessError):
    # 兜底：其他业务异常统一 400
    return JSONResponse(status_code=400, content={"detail": exc.message})



from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routers import customers, orders, order_items
from app.exceptions import (
    NotFoundError,
    InvalidStatusTransitionError,
    DuplicateError,
    BusinessError,
)

app = FastAPI(title="Machining Order System")

Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(order_items.router)


# ---------- 业务异常 → HTTP 响应 ----------
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(InvalidStatusTransitionError)
async def invalid_transition_handler(request: Request,
                                     exc: InvalidStatusTransitionError):
    return JSONResponse(status_code=400, content={
        "detail": exc.message,
        "current": exc.current.value,
        "target": exc.target.value,
        "allowed": [s.value for s in exc.allowed],
    })


@app.exception_handler(DuplicateError)
async def duplicate_handler(request: Request, exc: DuplicateError):
    return JSONResponse(status_code=409, content={"detail": exc.message})


@app.exception_handler(BusinessError)
async def business_handler(request: Request, exc: BusinessError):
    return JSONResponse(status_code=400, content={"detail": exc.message})


@app.get("/health")
def health():
    return {"status": "ok"}



from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ... 其他代码 ...

# 挂载静态目录
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")