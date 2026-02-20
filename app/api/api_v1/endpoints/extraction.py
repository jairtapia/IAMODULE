from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from app.services.extraction_service import extraction_service
from app.services.vision_service import vision_service
from app.services.local_vision_service import local_vision_service
from pydantic import BaseModel

router = APIRouter()

class ExtractionResponse(BaseModel):
    filename: str
    content_type: str
    text: str
    page_count: Optional[int] = None # Not always available
    method: str = "standard"

@router.post("/text", response_model=ExtractionResponse)
async def extract_text_from_file(
    file: UploadFile = File(...),
    mode: str = Form("standard", description="Extraction mode: 'standard', 'gemini', 'local_vision'")
):
    """
    Upload a file and get text content. Mode options:
    - **standard**: Fast, local (EasyOCR/Pdf). Default.
    - **gemini**: Cloud Vision (Best accuracy). Requires API Key.
    - **local_vision**: Advanced local OCR (Surya). Better than standard, heavier.
    """
    try:
        content = await file.read()
        used_method = mode
        text = ""

        if mode == "gemini":
            if not file.content_type.startswith("image/"):
                 raise HTTPException(400, "Gemini mode only supports images for now.")
            text = await vision_service.extract_handwriting(content, file.content_type)
            
        elif mode == "local_vision":
            if not file.content_type.startswith("image/"):
                 raise HTTPException(400, "Local Vision mode only supports images for now.")
            text = await local_vision_service.extract_text(content)
            
        else:
            # Standard Fallback
            text = await extraction_service.extract_text(
                file_content=content,
                filename=file.filename,
                content_type=file.content_type
            )
            used_method = "standard"
        
        return ExtractionResponse(
            filename=file.filename,
            content_type=file.content_type,
            text=text,
            method=used_method
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ImportError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
