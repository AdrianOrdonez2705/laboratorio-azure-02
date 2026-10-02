from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status

from app.model_service import ModelService
from app.schemas import PredictionRequest, PredictionResponse, ReadyResponse
from app.settings import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    runtime_settings = settings or get_settings()
    model_service = ModelService(runtime_settings.model_path)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        model_service.load()
        app.state.model_service = model_service
        app.state.settings = runtime_settings
        yield

    app = FastAPI(
        title="TSI Intelligent API",
        version=runtime_settings.app_version,
        description="API minima para el laboratorio de Docker y Azure Container Apps.",
        lifespan=lifespan,
    )

    @app.get("/")
    def root() -> dict[str, str]:
        return {
            "service": "tsi-intelligent-api",
            "version": runtime_settings.app_version,
            "environment": runtime_settings.app_env,
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready", response_model=ReadyResponse)
    def ready(request: Request) -> ReadyResponse:
        loaded = request.app.state.model_service.is_ready()
        if not loaded:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={"status": "not_ready", "model_loaded": False},
            )
        return ReadyResponse(status="ready", model_loaded=True)

    @app.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictionRequest, request: Request) -> PredictionResponse:
        service: ModelService = request.app.state.model_service
        if not service.is_ready():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model is not ready",
            )
        prediction, confidence = service.predict(
            [payload.feature_1, payload.feature_2, payload.feature_3]
        )
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            model_version=runtime_settings.app_version,
        )

    return app


app = create_app()
