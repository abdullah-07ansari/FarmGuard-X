from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class RecommendationDetail(BaseModel):
    crop: str
    disease: str
    symptoms: List[str]
    cause: str
    severity: str
    organic_treatment: str
    chemical_treatment: str
    preventive_measures: List[str]
    recovery_time: str

class PredictionResponse(BaseModel):
    id: int
    crop: str
    disease: str
    confidence: float
    inference_time: float
    model_version: str
    image_path: str
    created_at: datetime
    recommendation: RecommendationDetail

class PredictionHistoryItem(BaseModel):
    id: int
    crop: str
    disease: str
    confidence: float
    inference_time: float
    image_path: str
    created_at: datetime
    recommendation: RecommendationDetail

    class Config:
        from_attributes = True

class PredictionHistoryResponse(BaseModel):
    total: int
    items: List[PredictionHistoryItem]
