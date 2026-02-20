from pydantic import BaseModel
from typing import Optional, Any

class AIInput(BaseModel):
    prompt: str
    model: Optional[str] = "default-model"
    parameters: Optional[dict[str, Any]] = None

class AIOutput(BaseModel):
    result: str
    confidence: float
    metadata: Optional[dict[str, Any]] = None
