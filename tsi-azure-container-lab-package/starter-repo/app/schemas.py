from __future__ import annotations

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    feature_1: float = Field(ge=-10.0, le=10.0)
    feature_2: float = Field(ge=-10.0, le=10.0)
    feature_3: float = Field(ge=-10.0, le=10.0)


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float = Field(ge=0.0, le=1.0)
    model_version: str


class ReadyResponse(BaseModel):
    status: str
    model_loaded: bool
