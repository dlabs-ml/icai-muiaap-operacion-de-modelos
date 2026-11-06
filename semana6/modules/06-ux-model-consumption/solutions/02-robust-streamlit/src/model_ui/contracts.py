"""Contratos públicos de la experiencia de consumo."""

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat

QualityBand = Literal["needs_review", "acceptable", "excellent"]
UiPhase = Literal["idle", "loading", "success", "error"]
ConfidenceLevel = Literal["low", "medium", "high"]
LatencyStatus = Literal["within_target", "above_target"]
ErrorCode = Literal[
    "invalid_input",
    "artifact_unavailable",
    "timeout",
    "prediction_error",
]


class PredictionPayload(BaseModel):
    """Salida que la UI recibe del gateway de S3/S4."""

    model_config = ConfigDict(extra="forbid")

    quality_band: QualityBand
    confidence: FiniteFloat = Field(ge=0, le=1)
    model_version: str = Field(min_length=1)
    preprocessing_version: str = Field(min_length=1)


@dataclass(frozen=True)
class PredictionView:
    """Texto y señales listas para presentar sin exponer detalles internos."""

    quality_band: QualityBand
    quality_label: str
    confidence: float
    confidence_level: ConfidenceLevel
    confidence_label: str
    confidence_message: str
    latency_ms: float
    latency_status: LatencyStatus
    latency_label: str
    latency_message: str
    model_version: str
    preprocessing_version: str


class UserFacingError(BaseModel):
    """Error estable para pantalla y telemetría, sin traceback ni payload."""

    model_config = ConfigDict(extra="forbid")

    code: ErrorCode
    title: str
    message: str
    recovery: str
    request_id: str = Field(min_length=1)


@dataclass(frozen=True)
class UiState:
    """Estado observable de una petición de inferencia."""

    phase: UiPhase
    request_id: str | None = None
    view: PredictionView | None = None
    error: UserFacingError | None = None
