
from pydantic import BaseModel
from typing import Optional
import os

class Settings(BaseModel):
    app_name: str = "BGDB Cloud API"
    env: str = os.getenv("BGDB_ENV", "dev")
    database_url: str = os.getenv("BGDB_DATABASE_URL", "sqlite:///./bgdb.sqlite3")

settings = Settings()
