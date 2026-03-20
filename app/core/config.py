from typing import List, Union, Optional
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI_Module"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Optional path to Tesseract binary (if not in PATH)
    TESSERACT_CMD: Optional[str] = None
    
    # Google API Key for Advanced Vision
    GOOGLE_API_KEY: Optional[str] = None
    
    # Clave secreta para proteger los endpoints de la API
    API_SECRET_KEY: Optional[str] = None

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
