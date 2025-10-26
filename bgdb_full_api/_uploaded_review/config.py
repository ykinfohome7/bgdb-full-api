from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "BGDB Full API"
    ENV: str = "development"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    SECRET_KEY: str = Field("CHANGE_ME", min_length=16)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "bgdb"
    POSTGRES_USER: str = "bgdb"
    POSTGRES_PASSWORD: str = "bgdbpass"
    DATABASE_URL: str = "postgresql://bgdb:bgdbpass@localhost:5432/bgdb"

    RATE_LIMIT_CALLS: int = 100
    RATE_LIMIT_PERIOD: int = 60

    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "info@bgdb.eu"
    SMTP_PASSWORD: str = "CHANGE_ME"

    class Config:
        env_file = ".env"

settings = Settings()
