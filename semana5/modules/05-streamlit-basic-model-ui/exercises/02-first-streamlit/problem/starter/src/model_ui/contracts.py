"""Contrato de salida que consume la interfaz de S5."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat

QualityBand = Literal["needs_review", "acceptable", "excellent"]


class PredictionPayload(BaseModel):
    """Respuesta validada que llega desde el gateway."""

    model_config = ConfigDict(extra="forbid")

    quality_band: QualityBand
    confidence: FiniteFloat = Field(ge=0, le=1)
    model_version: str = Field(min_length=1)
    preprocessing_version: str = Field(min_length=1)
