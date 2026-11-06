"""Starter de componentes de UX desacoplados de Streamlit."""

from model_ui.contracts import PredictionPayload, PredictionView, UiState
from model_ui.controller import PredictionController

__all__ = [
    "PredictionController",
    "PredictionPayload",
    "PredictionView",
    "UiState",
]
