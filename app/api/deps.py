from fastapi import Header, HTTPException, status
from app.core.config import settings

def get_api_key(x_api_key: str = Header(None, alias="X-API-Key")) -> str:
    """
    Dependency para verificar el token en las peticiones.
    Busca el header 'X-API-Key'.
    """
    # Si por alguna razón no tienes API_SECRET_KEY en el .env, no bloqueamos.
    if not settings.API_SECRET_KEY:
        return ""

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el token de autorización (Header X-API-Key requerido).",
        )

    if x_api_key != settings.API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de API inválido.",
        )

    return x_api_key
