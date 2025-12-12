from functools import lru_cache
from fastapi import FastAPI

from backend.app.core.config import Settings

@lru_cache()
def get_settings():
    return Settings()

app = FastAPI()
