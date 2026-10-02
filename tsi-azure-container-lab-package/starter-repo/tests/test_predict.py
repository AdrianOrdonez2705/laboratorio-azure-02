from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings
from scripts.train_model import train_and_save


def test_predict_returns_class_confidence_and_version(tmp_path):
    model_path = train_and_save(tmp_path / "model.joblib")
    settings = Settings("test", "1.7", str(model_path), "INFO")
    with TestClient(create_app(settings)) as client:
        response = client.post(
            "/predict",
            json={"feature_1": 0.25, "feature_2": 0.75, "feature_3": -0.10},
        )
    body = response.json()
    assert response.status_code == 200
    assert body["prediction"] in {"low", "high"}
    assert 0.0 <= body["confidence"] <= 1.0
    assert body["model_version"] == "1.7"


def test_predict_rejects_malformed_payload(tmp_path):
    model_path = train_and_save(tmp_path / "model.joblib")
    settings = Settings("test", "1.0", str(model_path), "INFO")
    with TestClient(create_app(settings)) as client:
        response = client.post("/predict", json={"feature_1": "bad"})
    assert response.status_code == 422


def test_predict_rejects_out_of_range_features(tmp_path):
    model_path = train_and_save(tmp_path / "model.joblib")
    settings = Settings("test", "1.0", str(model_path), "INFO")
    with TestClient(create_app(settings)) as client:
        response = client.post(
            "/predict",
            json={"feature_1": 99, "feature_2": 0.0, "feature_3": 0.0},
        )
    assert response.status_code == 422


def test_predict_returns_503_when_model_missing(tmp_path):
    settings = Settings("test", "1.0", str(tmp_path / "missing.joblib"), "INFO")
    with TestClient(create_app(settings)) as client:
        response = client.post(
            "/predict",
            json={"feature_1": 0.25, "feature_2": 0.75, "feature_3": -0.10},
        )
    assert response.status_code == 503
    assert response.json()["detail"] == "Model is not ready"
