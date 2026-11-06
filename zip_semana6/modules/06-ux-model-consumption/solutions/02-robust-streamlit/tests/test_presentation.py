import pytest
from model_ui.contracts import PredictionPayload
from model_ui.errors import (
    ArtifactUnavailableError,
    InputContractError,
)
from model_ui.policies import classify_confidence, classify_latency
from model_ui.presentation import build_prediction_view, to_user_facing_error


def make_prediction(confidence: float = 0.42) -> PredictionPayload:
    """Devuelve una salida independiente de cualquier modelo real."""

    return PredictionPayload(
        quality_band="needs_review",
        confidence=confidence,
        model_version="wine-quality-rf-v1",
        preprocessing_version="wine-red-features-v1",
    )


def test_confidence_policy_has_explicit_boundary_values() -> None:
    assert classify_confidence(0.59) == "low"
    assert classify_confidence(0.60) == "medium"
    assert classify_confidence(0.85) == "high"

    with pytest.raises(ValueError, match="entre 0 y 1"):
        classify_confidence(1.1)


def test_latency_policy_marks_slow_responses_without_changing_result() -> None:
    assert classify_latency(300) == "within_target"
    assert classify_latency(300.1) == "above_target"

    view = build_prediction_view(make_prediction(), latency_ms=450)

    assert view.quality_band == "needs_review"
    assert view.confidence_level == "low"
    assert view.latency_status == "above_target"
    assert "requiere revisión" in view.confidence_message
    assert "no es una garantía" in view.confidence_message
    assert view.model_version == "wine-quality-rf-v1"


def test_error_translation_is_actionable_without_exception_detail() -> None:
    error = to_user_facing_error(
        InputContractError("ph fuera de rango: 99"), request_id="req-001"
    )

    assert error.code == "invalid_input"
    assert error.request_id == "req-001"
    assert "ph fuera de rango" not in error.message
    assert "Corrige" in error.recovery

    unavailable = to_user_facing_error(
        ArtifactUnavailableError("/secret/path/model.joblib"), request_id="req-002"
    )
    assert unavailable.code == "artifact_unavailable"
    assert "/secret/path" not in unavailable.message
