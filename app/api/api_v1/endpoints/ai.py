from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ai import AIInput, AIOutput
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/process", response_model=AIOutput)
async def process_ai_request(input_data: AIInput):
    """
    Process an AI request.
    """
    try:
        result = ai_service.process_request(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
