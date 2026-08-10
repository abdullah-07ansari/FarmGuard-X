from typing import Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import Prediction
from app.services.recommendation_service import recommendation_service

class DashboardService:
    """Service generating analytics metrics and dashboard summaries."""

    @staticmethod
    def get_user_dashboard(db: Session, user_id: int) -> Dict[str, Any]:
        """
        Aggregate scan metrics for user:
        - Total scans
        - Healthy vs Diseased count & percentage
        - Crop distribution breakdown
        - Disease distribution breakdown
        - 5 most recent scans with recommendations
        """
        query = db.query(Prediction).filter(Prediction.user_id == user_id)
        total_scans = query.count()

        healthy_count = query.filter(Prediction.disease.ilike("%Healthy%")).count()
        diseased_count = total_scans - healthy_count

        healthy_percentage = (
            round((healthy_count / total_scans) * 100.0, 1) if total_scans > 0 else 0.0
        )

        # Crop Distribution Aggregation
        crop_counts = (
            db.query(Prediction.crop, func.count(Prediction.id))
            .filter(Prediction.user_id == user_id)
            .group_by(Prediction.crop)
            .all()
        )
        crop_distribution = [{"crop": c[0], "count": c[1]} for c in crop_counts]

        # Disease Distribution Aggregation
        disease_counts = (
            db.query(Prediction.disease, func.count(Prediction.id))
            .filter(Prediction.user_id == user_id)
            .group_by(Prediction.disease)
            .all()
        )
        disease_distribution = [{"disease": d[0], "count": d[1]} for d in disease_counts]

        # Recent Scans (Top 5)
        recent_records = (
            query.order_by(Prediction.created_at.desc())
            .limit(5)
            .all()
        )

        recent_scans = []
        for p in recent_records:
            disease_key = f"{p.crop}___{p.disease.replace(' ', '_')}"
            rec = recommendation_service.get_recommendation(disease_key)
            recent_scans.append({
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
            "total_scans": total_scans,
            "healthy_count": healthy_count,
            "diseased_count": diseased_count,
            "healthy_percentage": healthy_percentage,
            "crop_distribution": crop_distribution,
            "disease_distribution": disease_distribution,
            "recent_scans": recent_scans
        }

dashboard_service = DashboardService()
