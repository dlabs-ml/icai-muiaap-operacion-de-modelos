"""Controlador de estados independiente de Streamlit."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from time import perf_counter
from uuid import uuid4

from model_ui.contracts import PredictionPayload, UiState
from model_ui.gateway import InferenceGateway
from model_ui.presentation import build_prediction_view, to_user_facing_error
from model_ui.telemetry import Telemetry

StateEmitter = Callable[[UiState], None]
Clock = Callable[[], float]
RequestIdFactory = Callable[[], str]


class PredictionController:
    """Orquesta loading, gateway, errores y telemetría."""

    def __init__(
        self,
        gateway: InferenceGateway,
        *,
        telemetry: Telemetry | None = None,
        clock: Clock = perf_counter,
        request_id_factory: RequestIdFactory | None = None,
    ) -> None:
        self.gateway = gateway
        self.telemetry = telemetry or Telemetry()
        self._clock = clock
        self._request_id_factory = request_id_factory or (lambda: uuid4().hex[:10])

    def submit(
        self,
        values: Mapping[str, object],
        *,
        emit: StateEmitter | None = None,
    ) -> UiState:
        """Ejecuta una inferencia y registra el estado final."""
        request_id = self._request_id_factory()
        if emit is not None:
            emit(UiState(phase="loading", request_id=request_id))
        started = self._clock()
        try:
            prediction = PredictionPayload.model_validate(self.gateway.predict(values))
        except Exception as exc:  # noqa: BLE001 - frontera de errores de la UI
            elapsed_ms = round((self._clock() - started) * 1000, 3)
            error = to_user_facing_error(exc, request_id)
            self.telemetry.record_error(error.code, elapsed_ms)
            state = UiState(phase="error", request_id=request_id, error=error)
        else:
            elapsed_ms = round((self._clock() - started) * 1000, 3)
            view = build_prediction_view(prediction, elapsed_ms)
            self.telemetry.record_success(
                elapsed_ms,
                model_version=view.model_version,
                preprocessing_version=view.preprocessing_version,
            )
            state = UiState(phase="success", request_id=request_id, view=view)
        if emit is not None:
            emit(state)
        return state
