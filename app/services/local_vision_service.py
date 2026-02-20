import logging
import io
from typing import List

try:
    from PIL import Image
    from surya.foundation import FoundationPredictor
    from surya.detection import DetectionPredictor
    from surya.recognition import RecognitionPredictor
    from surya.common.surya.schema import TaskNames
    SURYA_AVAILABLE = True
except ImportError:
    Image = None
    FoundationPredictor = None
    DetectionPredictor = None
    RecognitionPredictor = None
    TaskNames = None
    SURYA_AVAILABLE = False

logger = logging.getLogger("ai_module")

class LocalVisionService:
    def __init__(self):
        self.foundation_predictor = None
        self.det_predictor = None
        self.rec_predictor = None
        self._initialized = False

    def _initialize_models(self):
        if self._initialized:
            return
            
        if not SURYA_AVAILABLE:
            logger.error("surya-ocr not installed or missing dependencies.")
            return

        try:
            logger.info("Loading Surya OCR models (this may take a while first time)...")
            # Initialize predictors
            self.foundation_predictor = FoundationPredictor()
            self.det_predictor = DetectionPredictor()
            self.rec_predictor = RecognitionPredictor(self.foundation_predictor)
            self._initialized = True
            logger.info("Surya OCR models loaded.")
        except Exception as e:
            logger.error(f"Failed to load Surya models: {e}")

    async def extract_text(self, image_content: bytes) -> str:
        """
        Extract text using Surya OCR (v0.17+ API).
        """
        if not SURYA_AVAILABLE:
            raise ImportError("surya-ocr is not installed.")

        # Lazy loading to avoid heavy startup if not used
        self._initialize_models()
        
        if not self._initialized:
            raise ValueError("Failed to initialize Local Vision models.")

        try:
            image = Image.open(io.BytesIO(image_content)).convert("RGB")
            
            # Prepare arguments for prediction
            task_name = TaskNames.ocr_with_boxes
            task_names = [task_name] # One task for one image
            
            # Run prediction
            # Note: highres_images=None by default, usually fine for standard usage in API
            predictions = self.rec_predictor(
                [image],
                task_names=task_names,
                det_predictor=self.det_predictor,
                math_mode=True # Defaulting to True as in CLI
            )
            
            # Flatten results
            full_text = ""
            for pred in predictions:
                for line in pred.text_lines:
                    full_text += line.text + "\n"
            
            return full_text.strip()
            
        except Exception as e:
            logger.error(f"Error in LocalVisionService: {e}")
            raise ValueError(f"Failed to extract text with Local Vision: {e}")

local_vision_service = LocalVisionService()
