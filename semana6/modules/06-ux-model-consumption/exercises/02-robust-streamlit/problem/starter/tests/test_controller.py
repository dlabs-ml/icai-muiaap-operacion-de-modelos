from collections.abc import Mapping

from model_ui.contracts import PredictionPayload, UiState
from model_ui.controller import PredictionController
from model_ui.errors import InputContractError
from model_ui.gateway import FEATURE_NAMES, DemoGateway
from model_ui.telemetry import Telemetry

SAMPLE = {name: 1.0 for name in FEATURE_NAMES}


class FixedClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)

    def __call__(self) -> float:
        return next(self._values)


class FailingGateway:
    def predict(self, values: Mapping[str, object]) -> PredictionPayload:
        raise InputContractError("entrada inválida")


def test_controller_emits_loading_then_success_and_records_versions() -> None:
    events: list[UiState] = []
    telemetry = Telemetry()
    controller = PredictionController(
        DemoGateway(confidence=0.93),
        telemetry=telemetry,
        clock=FixedClock(10.0, 10.123),
        request_id_factory=lambda: "req-success",
    )
    state = controller.submit(SAMPLE, emit=events.append)
    assert [event.phase for event in events] == ["loading", "success"]
    assert state.view is not None
    assert state.view.confidence_level == "high"
    assert state.view.latency_ms == 123.0
    snapshot = telemetry.snapshot()
    assert snapshot.requests_total == 1
    assert snapshot.model_versions == ("demo-ui-v1",)


def test_controller_emits_loading_then_error_without_payload_telemetry() -> None:
    events: list[UiState] = []
    telemetry = Telemetry()
    controller = PredictionController(
        FailingGateway(),
        telemetry=telemetry,
        clock=FixedClock(20.0, 20.025),
        request_id_factory=lambda: "req-error",
    )
    state = controller.submit(SAMPLE, emit=events.append)
    assert [event.phase for event in events] == ["loading", "error"]
    assert state.error is not None
    assert state.error.code == "invalid_input"
    snapshot = telemetry.snapshot()
    assert snapshot.errors_by_code == {"invalid_input": 1}
    assert "fixed_acidity" not in repr(snapshot)
    assert "1.0" not in repr(snapshot)
