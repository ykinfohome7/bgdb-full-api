
from fastapi import FastAPI
from .routers import health, users, home
from .common.config import settings

app = FastAPI(title=f"{settings.app_name} - Public", version="1.0.0")
app.include_router(home.router)
app.include_router(health.router)
app.include_router(users.router)
