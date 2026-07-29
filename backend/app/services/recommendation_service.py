import json
import os
from typing import Dict, Any, Optional
from app.core.config import settings

class RecommendationService:
    def __init__(self, json_path: Optional[str] = None):
        self.json_path = json_path or str(settings.RECOMMENDATIONS_FILE)
        self.recommendations: Dict[str, Any] = {}
        self._load_recommendations()

    def _load_recommendations(self) -> None:
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"Recommendations JSON file not found at: {self.json_path}")
        
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.recommendations = json.load(f)

    def get_recommendation(self, disease_key: str) -> Dict[str, Any]:
        """
        Lookup recommendations for a given disease class key.
        e.g., 'Tomato___Late_blight' or 'Tomato Late Blight'
        """
        # Exact lookup
        if disease_key in self.recommendations:
            return self.recommendations[disease_key]
        
        # Normalized key lookup (e.g. replacing spaces with underscores)
        normalized_key = disease_key.replace(" ", "_")
        if normalized_key in self.recommendations:
            return self.recommendations[normalized_key]

        # Case insensitive key search fallback
        for key, value in self.recommendations.items():
            if key.lower() == disease_key.lower() or key.lower() == normalized_key.lower():
                return value

        # Default fallback if disease is not in dataset
        return {
            "crop": "General Crop",
            "disease": disease_key,
            "symptoms": ["General leaf spot or damage observed"],
            "cause": "Unclassified pathogen or environmental factor",
            "severity": "Medium",
            "organic_treatment": "Apply broad-spectrum Neem oil spray (15ml / 3L water).",
            "chemical_treatment": "Consult local agricultural officer before applying chemical spray.",
            "preventive_measures": ["Isolate affected plants", "Maintain drip irrigation"],
            "recovery_time": "7–14 days"
        }

    def list_supported_diseases(self) -> list[str]:
        return list(self.recommendations.keys())

# Singleton instance
recommendation_service = RecommendationService()
