"""Estado de sesión de Streamlit aislado para poder probarlo sin Streamlit."""

from __future__ import annotations

from collections.abc import MutableMapping

from model_ui.contracts import UiState
from model_ui.telemetry import Telemetry

LAST_STATE_KEY = "last_state"
TELEMETRY_KEY = "telemetry"
LAST_VALUES_KEY = "last_values"


def initialize_session_state(
    session_state: MutableMapping[str, object],
) -> None:
    """Crea solo las claves que faltan."""
    if TELEMETRY_KEY not in session_state:
        session_state[TELEMETRY_KEY] = Telemetry()
    session_state.setdefault(LAST_STATE_KEY, UiState(phase="idle"))
    session_state.setdefault(LAST_VALUES_KEY, {})


def clear_last_state(session_state: MutableMapping[str, object]) -> None:
    """Limpia la última petición y conserva los contadores."""
    session_state[LAST_STATE_KEY] = UiState(phase="idle")
    session_state[LAST_VALUES_KEY] = {}
