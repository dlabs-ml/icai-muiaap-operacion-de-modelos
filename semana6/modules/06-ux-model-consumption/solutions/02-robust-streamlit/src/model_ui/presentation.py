"""Traducción de resultados y errores a mensajes de UX."""

from __future__ import annotations

from pydantic import ValidationError

from model_ui.contracts import (
    PredictionPayload,
    PredictionView,
    UserFacingError,
)
from model_ui.errors import (
    ArtifactUnavailableError,
    BackendInferenceError,
    InferenceTimeoutError,
    InputContractError,
)
from model_ui.policies import (
    DEFAULT_CONFIDENCE_POLICY,
    DEFAULT_LATENCY_POLICY,
    ConfidencePolicy,
    LatencyPolicy,
    classify_confidence,
    classify_latency,
)

QUALITY_LABELS = {
    "needs_review": "Requiere revisión",
    "acceptable": "Resultado aceptable",
    "excellent": "Resultado excelente",
}

CONFIDENCE_COPY = {
    "low": (
        "Confianza baja",
        "El resultado es orientativo y requiere revisión; "
        "la confianza no es una garantía.",
    ),
    "medium": (
        "Confianza intermedia",
        "Usa el resultado como señal orientativa y revisa su contexto antes de actuar.",
    ),
    "high": (
        "Confianza alta",
        "La confianza es alta para este modelo, pero no garantiza "
        "que la decisión sea correcta.",
    ),
}

LATENCY_COPY = {
    "within_target": (
        "Dentro del objetivo",
        "La respuesta quedó dentro del objetivo de la demo.",
    ),
    "above_target": (
        "Por encima del objetivo",
        "La respuesta llegó, pero la latencia supera el objetivo técnico de la demo.",
    ),
}


def build_prediction_view(
    prediction: PredictionPayload,
    latency_ms: float,
    *,
    confidence_policy: ConfidencePolicy = DEFAULT_CONFIDENCE_POLICY,
    latency_policy: LatencyPolicy = DEFAULT_LATENCY_POLICY,
) -> PredictionView:
    """Construye copy seguro y estable a partir de la salida validada."""

    level = classify_confidence(prediction.confidence, confidence_policy)
    latency_status = classify_latency(latency_ms, latency_policy)
    confidence_label, confidence_message = CONFIDENCE_COPY[level]
    latency_label, latency_message = LATENCY_COPY[latency_status]
    return PredictionView(
        quality_band=prediction.quality_band,
        quality_label=QUALITY_LABELS[prediction.quality_band],
        confidence=prediction.confidence,
        confidence_level=level,
        confidence_label=confidence_label,
        confidence_message=confidence_message,
        latency_ms=round(latency_ms, 3),
        latency_status=latency_status,
        latency_label=latency_label,
        latency_message=latency_message,
        model_version=prediction.model_version,
        preprocessing_version=prediction.preprocessing_version,
    )


def to_user_facing_error(error: Exception, request_id: str) -> UserFacingError:
    """Convierte una excepción en un error accionable y sin detalles internos."""

    if isinstance(error, (InputContractError, ValidationError)):
        return UserFacingError(
            code="invalid_input",
            title="Revisa los datos",
            message="La muestra no cumple el contrato de entrada.",
            recovery="Corrige los campos indicados y vuelve a enviar la petición.",
            request_id=request_id,
        )
    if isinstance(error, ArtifactUnavailableError):
        return UserFacingError(
            code="artifact_unavailable",
            title="Modelo no disponible",
            message="No se pudo preparar el artefacto de inferencia.",
            recovery="Comprueba el bundle configurado o avisa al responsable técnico.",
            request_id=request_id,
        )
    if isinstance(error, InferenceTimeoutError):
        return UserFacingError(
            code="timeout",
            title="La respuesta está tardando",
            message="La inferencia no terminó dentro del tiempo esperado.",
            recovery=(
                "Espera unos segundos y reintenta; si persiste, avisa al responsable."
            ),
            request_id=request_id,
        )
    if isinstance(error, BackendInferenceError):
        return UserFacingError(
            code="prediction_error",
            title="No se pudo obtener una predicción",
            message="El backend no devolvió una salida compatible.",
            recovery="Revisa la versión del bundle o avisa al responsable técnico.",
            request_id=request_id,
        )
    return UserFacingError(
        code="prediction_error",
        title="No se pudo completar la petición",
        message="Se produjo un fallo controlado durante la inferencia.",
        recovery=(
            "Reintenta y comparte el identificador de petición si el problema continúa."
        ),
        request_id=request_id,
    )
