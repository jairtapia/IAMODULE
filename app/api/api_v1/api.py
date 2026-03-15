from fastapi import APIRouter
from app.api.api_v1.endpoints import ai, extraction, clasificacion

api_router = APIRouter()
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(extraction.router, prefix="/extraction", tags=["extraction"])
api_router.include_router(clasificacion.router, prefix="/clasificacion", tags=["clasificacion"])
