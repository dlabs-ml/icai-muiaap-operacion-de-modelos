"""Políticas explícitas para comunicar confianza y latencia."""

from dataclasses import dataclass

from model_ui.contracts import ConfidenceLevel, LatencyStatus


@dataclass(frozen=True)
class ConfidencePolicy:
    """Umbrales de copy UX; no son umbrales clínicos ni de aprobación."""

    low_below: float = 0.60
    high_from: float = 0.85


@dataclass(frozen=True)
class LatencyPolicy:
    """Objetivo visible de latencia para la demo local."""

    target_ms: float = 300.0


DEFAULT_CONFIDENCE_POLICY = ConfidencePolicy()
DEFAULT_LATENCY_POLICY = LatencyPolicy()


def classify_confidence(
    confidence: float, policy: ConfidencePolicy = DEFAULT_CONFIDENCE_POLICY
) -> ConfidenceLevel:
    """Clasifica una confianza válida con una política estable."""

    if not 0 <= confidence <= 1:
        raise ValueError("confidence debe estar entre 0 y 1")
    if confidence < policy.low_below:
        return "low"
    if confidence < policy.high_from:
        return "medium"
    return "high"


def classify_latency(
    latency_ms: float, policy: LatencyPolicy = DEFAULT_LATENCY_POLICY
) -> LatencyStatus:
    """Indica si una respuesta quedó dentro del objetivo de experiencia."""

    if latency_ms < 0:
        raise ValueError("latency_ms no puede ser negativa")
    return "within_target" if latency_ms <= policy.target_ms else "above_target"
