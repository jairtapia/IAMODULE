import io
import logging
from typing import Optional

# Import libraries with error handling to avoid crashing if one is missing (though they should be installed)
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None

try:
    import easyocr
    from PIL import Image
    import numpy as np
except ImportError:
    easyocr = None
    Image = None
    np = None

logger = logging.getLogger("ai_module")

class ExtractionService:
    def __init__(self):
        self.reader = None
        if easyocr:
            logger.info("Initializing EasyOCR Reader...")
            # Initialize for English and Spanish. GPU=False for compatibility, set True if available.
            self.reader = easyocr.Reader(['en', 'es'], gpu=False)

    async def extract_text(self, file_content: bytes, filename: str, content_type: str) -> str:
        """
        Extract text from a file based on its content type or extension.
        """
        logger.info(f"Extracting text from {filename} ({content_type})")
        
        extracted_text = ""
        
        if "pdf" in content_type or filename.endswith(".pdf"):
            extracted_text = self._extract_from_pdf(file_content)
        elif "word" in content_type or "officedocument" in content_type or filename.endswith(".docx"):
            extracted_text = self._extract_from_docx(file_content)
        elif "image" in content_type or filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp")):
            extracted_text = self._extract_from_image(file_content)
        else:
            # Fallback for plain text
            try:
                extracted_text = file_content.decode("utf-8")
            except Exception:
                raise ValueError(f"Unsupported file type: {content_type}")
                
        return extracted_text.strip()

    def _extract_from_pdf(self, content: bytes) -> str:
        if not pypdf:
            raise ImportError("pypdf is not installed")
        
        text = ""
        try:
            pdf_file = io.BytesIO(content)
            reader = pypdf.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")
        return text

    def _extract_from_docx(self, content: bytes) -> str:
        if not docx:
            raise ImportError("python-docx is not installed")
        
        text = ""
        try:
            doc_file = io.BytesIO(content)
            doc = docx.Document(doc_file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            logger.error(f"Error extracting Docx: {e}")
            raise ValueError(f"Failed to extract text from Word document: {e}")
        return text

    def _extract_from_image(self, content: bytes) -> str:
        if not self.reader or not Image:
            raise ImportError("easyocr or Pillow is not installed")
            
        try:
            # EasyOCR reads from bytes directly or numpy array
            result = self.reader.readtext(content, detail=0)
            return " ".join(result)
        except Exception as e:
            logger.error(f"Error extracting Image with EasyOCR: {e}")
            raise ValueError(f"Failed to extract text from Image: {e}")

extraction_service = ExtractionService()

