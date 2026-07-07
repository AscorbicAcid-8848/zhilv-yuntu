from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.export import router as export_router
from app.api.routes.trip import router as trip_router
from app.api.routes.weather import router as weather_router
from app.config import CORS_ALLOWED_ORIGINS
from app.services.storage_service import init_db
from app.shared.http_client import close_http_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_http_client()


app = FastAPI(
    title="Trip Planner Demo Backend",
    description="MVP backend for the intelligent travel assistant.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    """根路径接口，用于确认后端服务已启动。"""
    return {"message": "Trip Planner Demo backend is running."}


@app.get("/health")
def health_check() -> dict[str, str]:
    """健康检查接口。"""
    return {"status": "ok"}


app.include_router(trip_router)
app.include_router(export_router)
app.include_router(weather_router)
