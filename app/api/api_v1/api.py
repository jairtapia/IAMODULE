from fastapi import APIRouter
from app.api.api_v1.endpoints import ai, extraction

api_router = APIRouter()
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(extraction.router, prefix="/extraction", tags=["extraction"])
