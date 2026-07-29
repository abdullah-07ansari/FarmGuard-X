from typing import List, Dict, Any
from pydantic import BaseModel
from app.schemas.prediction import PredictionHistoryItem

class CropDistribution(BaseModel):
    crop: str
    count: int

class DiseaseDistribution(BaseModel):
    disease: str
    count: int

class DashboardResponse(BaseModel):
    total_scans: int
    healthy_count: int
    diseased_count: int
    healthy_percentage: float
    crop_distribution: List[CropDistribution]
    disease_distribution: List[DiseaseDistribution]
    recent_scans: List[PredictionHistoryItem]
