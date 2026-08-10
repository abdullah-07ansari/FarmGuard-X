from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.prediction import PredictionHistoryResponse
from app.services.history_service import history_service

router = APIRouter()

@router.get("/history", response_model=PredictionHistoryResponse)
def get_prediction_history(
    skip: int = Query(0, ge=0, description="Pagination skip offset"),
    limit: int = Query(20, ge=1, le=100, description="Max items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve paginated prediction history for current authenticated user."""
    return history_service.get_user_history(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
