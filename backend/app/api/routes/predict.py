from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.prediction import PredictionResponse
from app.services.prediction_service import prediction_service

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def predict_crop_disease(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload crop leaf image for AI pathology analysis.
    Returns predicted crop disease, confidence score, inference time, and treatment recommendations.
    """
    return await prediction_service.process_and_save_prediction(
        db=db,
        user_id=current_user.id,
        file=file
    )
