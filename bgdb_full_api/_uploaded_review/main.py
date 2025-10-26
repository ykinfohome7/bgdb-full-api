from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.routers import auth, items, users

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=settings.APP_NAME, version="1.0.0", openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return exc.response

@app.on_event("startup")
def on_startup():
    logger.info("Starting BGDB API...")
    init_db()

@app.get("/health")
@limiter.limit("5/10seconds")
def health():
    return {"status": "ok", "env": settings.ENV}

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "docs": f"{settings.API_V1_STR}/docs"}

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(items.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
