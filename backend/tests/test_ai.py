import cv2
import numpy as np
import pytest
from app.ai.preprocess import preprocess_image
from app.ai.model_loader import model_loader
from app.ai.predictor import predictor

def create_synthetic_jpeg_bytes() -> bytes:
    """Generate a synthetic green leaf image encoded as JPEG bytes."""
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :, 1] = 180  # Green channel
    img[100:200, 100:200, 0] = 120  # Brown spot
    img[100:200, 100:200, 2] = 40
    _, buffer = cv2.imencode('.jpg', img)
    return buffer.tobytes()

def test_preprocess_image():
    image_bytes = create_synthetic_jpeg_bytes()
    nchw_tensor, resized_img = preprocess_image(image_bytes, target_size=(224, 224))
    
    assert nchw_tensor.shape == (1, 3, 224, 224)
    assert resized_img.shape == (224, 224, 3)

def test_model_loader_class_info():
    info = model_loader.get_class_info(2)
    assert info["crop"] == "Tomato"
    assert info["disease"] == "Late Blight"
    assert info["key"] == "Tomato___Late_blight"

def test_disease_predictor():
    image_bytes = create_synthetic_jpeg_bytes()
    res = predictor.predict(image_bytes)

    assert "crop" in res
    assert "disease" in res
    assert "disease_key" in res
    assert "confidence" in res
    assert "inference_time" in res
    assert "model_version" in res

    assert res["crop"] in ["Tomato", "Potato", "Bell Pepper"]
    assert res["confidence"] > 0.5
    assert res["inference_time"] > 0.0
