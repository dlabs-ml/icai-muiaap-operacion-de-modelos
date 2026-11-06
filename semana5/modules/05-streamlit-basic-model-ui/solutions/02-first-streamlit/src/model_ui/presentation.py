"""Presentación mínima de una predicción en S5."""

from model_ui.contracts import PredictionPayload

QUALITY_LABELS = {
    "needs_review": "Requiere revisión",
    "acceptable": "Resultado aceptable",
    "excellent": "Resultado excelente",
}


def quality_label(prediction: PredictionPayload) -> str:
    """Devuelve una etiqueta legible sin cambiar el payload."""

    return QUALITY_LABELS[prediction.quality_band]


def confidence_caption(prediction: PredictionPayload) -> str:
    """Construye el texto básico de confianza de la interfaz."""

    return f"Confianza reportada por el modelo: {prediction.confidence:.0%}."
