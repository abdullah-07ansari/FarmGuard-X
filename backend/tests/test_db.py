from app.db.models import User, Prediction

def test_create_user_and_prediction(db_session):
    # 1. Create a User
    user = User(
        email="farmer@farmguard.ai",
        hashed_password="hashed_secret_password",
        full_name="Farmer John"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "farmer@farmguard.ai"

    # 2. Create a Prediction record linked to User
    prediction = Prediction(
        user_id=user.id,
        crop="Tomato",
        disease="Tomato Late Blight",
        confidence=0.974,
        inference_time=0.042,
        image_path="uploads/test_tomato.jpg"
    )
    db_session.add(prediction)
    db_session.commit()
    db_session.refresh(prediction)

    assert prediction.id is not None
    assert prediction.user_id == user.id
    assert prediction.crop == "Tomato"
    assert prediction.confidence == 0.974
    assert len(user.predictions) == 1
    assert user.predictions[0].disease == "Tomato Late Blight"
