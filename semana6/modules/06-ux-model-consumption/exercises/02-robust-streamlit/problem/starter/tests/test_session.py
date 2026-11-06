from model_ui.contracts import UiState
from model_ui.session import (
    LAST_STATE_KEY,
    LAST_VALUES_KEY,
    TELEMETRY_KEY,
    clear_last_state,
    initialize_session_state,
)
from model_ui.telemetry import Telemetry


def test_session_state_initialization_is_idempotent() -> None:
    session_state: dict[str, object] = {}
    initialize_session_state(session_state)
    telemetry = session_state[TELEMETRY_KEY]
    initialize_session_state(session_state)
    assert isinstance(telemetry, Telemetry)
    assert session_state[TELEMETRY_KEY] is telemetry
    assert session_state[LAST_STATE_KEY] == UiState(phase="idle")
    assert session_state[LAST_VALUES_KEY] == {}


def test_clear_last_state_keeps_telemetry() -> None:
    telemetry = Telemetry()
    session_state: dict[str, object] = {
        TELEMETRY_KEY: telemetry,
        LAST_STATE_KEY: UiState(phase="success"),
        LAST_VALUES_KEY: {"ph": 3.5},
    }
    clear_last_state(session_state)
    assert session_state[TELEMETRY_KEY] is telemetry
    assert session_state[LAST_STATE_KEY] == UiState(phase="idle")
    assert session_state[LAST_VALUES_KEY] == {}
