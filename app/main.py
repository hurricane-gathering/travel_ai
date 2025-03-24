from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger import logger
from contextlib import asynccontextmanager
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    logger.info("Starting up application...")
    yield
    # 关闭时执行
    logger.info("Shutting down application...")

app = FastAPI( 
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"请求: {request.method} {request.url.path} "
        f"状态码: {response.status_code} "
        f"处理时间: {process_time:.2f}ms"
    )
    return response

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 导入路由
from app.api.api_v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR) 