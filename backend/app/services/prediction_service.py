import os
import uuid
from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from app.core.config import settings
from app.db.models import Prediction
from app.ai.predictor import predictor
from app.services.recommendation_service import recommendation_service

class PredictionService:
    """Service handling image upload saving, AI inference, and database persistence."""

    @staticmethod
    async def process_and_save_prediction(
        db: Session,
        user_id: int,
        file: UploadFile
    ) -> Dict[str, Any]:
        """
        Process leaf image upload:
        1. Validate file extension / image type.
        2. Save raw file to uploads/ directory.
        3. Execute AI inference (OpenCV + MobileNetV3).
        4. Lookup recommendation dataset.
        5. Save record to SQLite database.
        """
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must be a valid image (JPEG, PNG, WEBP)."
            )

        file_bytes = await file.read()
        if len(file_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )

        # Generate unique filename and save locally
        file_ext = os.path.splitext(file.filename)[1] or ".jpg"
        unique_filename = f"scan_{uuid.uuid4().hex}{file_ext}"
        relative_path = f"uploads/{unique_filename}"
        full_file_path = settings.UPLOAD_DIR / unique_filename

        with open(full_file_path, "wb") as f:
            f.write(file_bytes)

        # Run AI Inference Engine
        try:
            ai_result = predictor.predict(file_bytes)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI model inference failed: {str(e)}"
            )

        # Lookup Disease Recommendation
        recommendation_data = recommendation_service.get_recommendation(ai_result["disease_key"])

        # Persist Record in SQLite Database
        db_prediction = Prediction(
            user_id=user_id,
            crop=ai_result["crop"],
            disease=ai_result["disease"],
            confidence=ai_result["confidence"],
            inference_time=ai_result["inference_time"],
            image_path=relative_path
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)

        return {
            "id": db_prediction.id,
            "crop": db_prediction.crop,
            "disease": db_prediction.disease,
            "confidence": db_prediction.confidence,
            "inference_time": db_prediction.inference_time,
            "model_version": ai_result["model_version"],
            "image_path": db_prediction.image_path,
            "created_at": db_prediction.created_at,
            "recommendation": recommendation_data
        }

prediction_service = PredictionService()
