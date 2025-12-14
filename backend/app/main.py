from functools import lru_cache
from fastapi import FastAPI

from backend.app.core.config import Settings
from backend.app.api.ai import router as ai_router

@lru_cache()
def get_settings():
	return Settings()

app = FastAPI()

app.include_router(ai_router, prefix="/api/ai", tags=["AI"])

@app.get("/")
async def health_check():
	return {"status": "ok"}