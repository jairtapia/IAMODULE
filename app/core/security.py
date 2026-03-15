"""
app/core/security.py
Dependencia reutilizable para validar el API Key en los endpoints protegidos.

Uso en un endpoint:
    from app.core.security import verify_api_key
    @router.post("/mi-endpoint", dependencies=[Depends(verify_api_key)])
    def mi_endpoint(): ...

Si API_SECRET_KEY no está definida en .env, la validación se omite
(útil para desarrollo local sin configurar el secreto).
"""

from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str | None = Security(API_KEY_HEADER)) -> None:
    """
    Valida el header X-API-Key contra settings.API_SECRET_KEY.
    - Si API_SECRET_KEY no está configurada → permite todo (modo dev).
    - Si está configurada y el header no coincide → 403.
    """
    secret = settings.API_SECRET_KEY
    if not secret:
        # Sin secreto configurado: modo desarrollo, todo pasa
        return

    if not api_key or api_key != secret:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida o ausente. Incluye el header X-API-Key.",
        )
