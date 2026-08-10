from typing import Dict, Any
from sqlalchemy.orm import Session
from app.db.models import Prediction
from app.services.recommendation_service import recommendation_service

class HistoryService:
    """Service retrieving user prediction scan history."""

    @staticmethod
    def get_user_history(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Fetch paginated history items for user with recommendation details."""
        query = db.query(Prediction).filter(Prediction.user_id == user_id)
        total = query.count()

        predictions = (
            query.order_by(Prediction.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        items = []
        for p in predictions:
            disease_key = f"{p.crop}___{p.disease.replace(' ', '_')}"
            rec = recommendation_service.get_recommendation(disease_key)
            items.append({
                "id": p.id,
                "crop": p.crop,
                "disease": p.disease,
                "confidence": p.confidence,
                "inference_time": p.inference_time,
                "image_path": p.image_path,
                "created_at": p.created_at,
                "recommendation": rec
            })

        return {
            "total": total,
            "items": items
        }

history_service = HistoryService()
