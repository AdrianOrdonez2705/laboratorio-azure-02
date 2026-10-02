from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib


class ModelService:
    def __init__(self, model_path: str | Path):
        self.model_path = Path(model_path)
        self._estimator: Any | None = None
        self._labels: dict[int, str] = {0: "low", 1: "high"}

    def load(self) -> None:
        self._estimator = None
        if not self.model_path.exists():
            return
        bundle = joblib.load(self.model_path)
        self._estimator = bundle["estimator"]
        self._labels = bundle.get("labels", self._labels)

    def is_ready(self) -> bool:
        return self._estimator is not None

    def predict(self, features: list[float]) -> tuple[str, float]:
        if self._estimator is None:
            raise RuntimeError("Model is not loaded")
        probabilities = self._estimator.predict_proba([features])[0]
        class_index = int(probabilities.argmax())
        prediction = self._labels[class_index]
        confidence = float(probabilities[class_index])
        return prediction, confidence
