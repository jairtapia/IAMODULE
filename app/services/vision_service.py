import google.generativeai as genai
from PIL import Image
import io
import logging
from app.core.config import settings

logger = logging.getLogger("ai_module")

class VisionService:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None
            # Log warning but don't crash, allowing app to start without key
            logger.warning("GOOGLE_API_KEY not set. Vision AI features will be unavailable.")

    async def extract_handwriting(self, image_content: bytes, mime_type: str = "image/jpeg") -> str:
        """
        Extract text from an image using Gemini Vision model.
        Ideal for handwriting or complex layouts.
        """
        if not self.model:
            raise ValueError("GOOGLE_API_KEY is not configured in .env. Cannot use Advanced Vision.")

        try:
            logger.info("Sending image to Gemini Vision...")
            
            # Create the image part
            image_part = {
                "mime_type": mime_type,
                "data": image_content
            }

            prompt = """
            Transcribe the text in this image exactly as written. 
            If it is handwriting, do your best to read it. 
            Output ONLY the transcribed text, no markdown code blocks or explanations.
            """

            response = self.model.generate_content([prompt, image_part])
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error in VisionService: {e}")
            raise ValueError(f"Failed to transcribe with Vision AI: {e}")

vision_service = VisionService()
