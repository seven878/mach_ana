# run.py（放在项目根目录，和 app/ 同级）
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",       # 模块路径:实例名
        host="127.0.0.1",
        port=8000,
        reload=True,          # 开发时热重载
    )