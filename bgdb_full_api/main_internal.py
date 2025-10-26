
from fastapi import FastAPI
from .routers import health, users
from .common.config import settings

app = FastAPI(title=f"{settings.app_name} - Internal", version="1.0.0")

# Re-mount under /internal for clear separation
from fastapi import APIRouter
internal = APIRouter(prefix="/internal")
internal.include_router(health.router)
internal.include_router(users.router)
app.include_router(internal)
