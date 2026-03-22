from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.api.deps import get_api_key

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://cuceishare-front.onrender.com",
    "https://cuceishare-back.onrender.com",
]

# Add origins from settings if configured
if settings.CORS_ORIGINS:
    for origin in settings.CORS_ORIGINS:
        origin_str = str(origin)
        if origin_str not in origins:
            origins.append(origin_str)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.onrender\.com", # Permite cualquier subdominio en onrender.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Protegemos todos los endpoints de api_router
app.include_router(
    api_router, 
    prefix=settings.API_V1_STR, 
    dependencies=[Depends(get_api_key)]
)

@app.get("/")
def root():
    return {"message": "AI Module API is running"}
