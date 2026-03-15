from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, Dict
from app.core.security import verify_api_key

router = APIRouter()


# ─── Schemas ────────────────────────────────────────────────────────────────

class ClasificarRequest(BaseModel):
    texto: str = Field(
        ...,
        min_length=1,
        description="Texto / apunte que se desea clasificar.",
        examples=["El ciclo de Krebs ocurre en la mitocondria y produce ATP."],
    )


class ClasificarResponse(BaseModel):
    resultado: str = Field(description="Categoría predicha por el modelo.")
    confianza: float = Field(description="Probabilidad de la clase predicha (0 a 1).")
    advertencia: Optional[str] = Field(
        default=None,
        description="Presente cuando la confianza es menor al 40 %.",
    )
    todas_las_probabilidades: Dict[str, float] = Field(
        description="Probabilidad asignada a cada clase disponible."
    )


class AnalizarArchivoResponse(BaseModel):
    filename: str = Field(description="Nombre del archivo procesado.")
    content_type: str = Field(description="Tipo MIME del archivo.")
    texto_extraido: str = Field(description="Texto extraído del archivo (sin IA).")
    resultado: str = Field(description="Categoría predicha por el modelo.")
    confianza: float = Field(description="Probabilidad de la clase predicha (0 a 1).")
    advertencia: Optional[str] = Field(
        default=None,
        description="Presente cuando la confianza es menor al 40 %.",
    )
    todas_las_probabilidades: Dict[str, float] = Field(
        description="Probabilidad asignada a cada clase disponible."
    )


# ─── Endpoints ───────────────────────────────────────────────────────────────

@router.post(
    "/clasificar",
    response_model=ClasificarResponse,
    summary="Clasificar un apunte",
    description=(
        "Recibe un texto (apunte) y devuelve su categoría predicha "
        "junto con el nivel de confianza, usando el modelo local `modelo_apuntes.pkl`."
    ),
    dependencies=[Depends(verify_api_key)],
)
def clasificar_apunte(body: ClasificarRequest):
    """
    Clasifica el texto recibido con el modelo de apuntes entrenado localmente.
    """
    try:
        from lib.models.clasificador import clasificar_texto
        resultado = clasificar_texto(body.texto)
        return resultado
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al clasificar: {exc}")


@router.post(
    "/analizar-archivo",
    response_model=AnalizarArchivoResponse,
    summary="Extraer texto de archivo y clasificarlo",
    description=(
        "Sube un archivo (imagen, PDF, Word, etc.), extrae su texto usando OCR/parsers locales "
        "**sin IA externa** (modo standard: EasyOCR + PyPDF) y lo clasifica automáticamente "
        "con el modelo local `modelo_apuntes.pkl`. Todo en un solo paso."
    ),
    dependencies=[Depends(verify_api_key)],
)
async def analizar_archivo(file: UploadFile = File(...)):
    """
    Pipeline completo local:
    1. Lee el archivo subido.
    2. Extrae el texto con EasyOCR / PyPDF (sin llamadas a APIs externas).
    3. Clasifica el texto con el modelo pkl entrenado localmente.
    """
    try:
        from app.services.extraction_service import extraction_service
        from lib.models.clasificador import clasificar_texto

        # 1. Leer bytes del archivo
        content = await file.read()

        if not content:
            raise HTTPException(status_code=400, detail="El archivo está vacío.")

        # 2. Extraer texto (modo standard: sin IA)
        texto = await extraction_service.extract_text(
            file_content=content,
            filename=file.filename,
            content_type=file.content_type,
        )

        if not texto or not texto.strip():
            raise HTTPException(
                status_code=422,
                detail="No se pudo extraer texto del archivo. "
                       "Verifica que el archivo tenga contenido legible.",
            )

        # 3. Clasificar el texto extraído
        clasificacion = clasificar_texto(texto.strip())

        return AnalizarArchivoResponse(
            filename=file.filename,
            content_type=file.content_type,
            texto_extraido=texto.strip(),
            resultado=clasificacion["resultado"],
            confianza=clasificacion["confianza"],
            advertencia=clasificacion["advertencia"],
            todas_las_probabilidades=clasificacion["todas_las_probabilidades"],
        )

    except HTTPException:
        raise
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {exc}")
