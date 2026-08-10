from app.services.recommendation_service import RecommendationService

def test_recommendation_service_loading():
    service = RecommendationService()
    supported = service.list_supported_diseases()
    
    assert len(supported) == 8
    assert "Tomato___Late_blight" in supported
    assert "Potato___Early_blight" in supported
    assert "Pepper__bell___Bacterial_spot" in supported

def test_get_valid_recommendation():
    service = RecommendationService()
    rec = service.get_recommendation("Tomato___Late_blight")
    
    assert rec["crop"] == "Tomato"
    assert rec["disease"] == "Late Blight"
    assert rec["severity"] == "High"
    assert "Neem oil" in rec["organic_treatment"]
    assert "Copper Hydroxide" in rec["chemical_treatment"]

def test_get_unknown_recommendation_fallback():
    service = RecommendationService()
    rec = service.get_recommendation("Unknown_Crop_Disease")
    
    assert rec["disease"] == "Unknown_Crop_Disease"
    assert "Neem oil" in rec["organic_treatment"]
