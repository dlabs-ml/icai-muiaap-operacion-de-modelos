"""S6: estado de sesión y presentación de inferencia."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from model_ui.contracts import UiState
from model_ui.controller import PredictionController
from model_ui.gateway import (
    FEATURE_NAMES,
    DemoGateway,
    InferenceGateway,
    PackagedBundleGateway,
    UnavailableGateway,
)
from model_ui.session import (
    LAST_STATE_KEY,
    LAST_VALUES_KEY,
    TELEMETRY_KEY,
    clear_last_state,
    initialize_session_state,
)

FEATURE_FIELDS = (
    ("fixed_acidity", "Fixed acidity", 0.0, 20.0, 7.4),
    ("volatile_acidity", "Volatile acidity", 0.0, 2.0, 0.7),
    ("citric_acid", "Citric acid", 0.0, 2.0, 0.0),
    ("residual_sugar", "Residual sugar", 0.0, 20.0, 1.9),
    ("chlorides", "Chlorides", 0.0, 1.0, 0.076),
    ("free_sulfur_dioxide", "Free sulfur dioxide", 0.0, 100.0, 11.0),
    ("total_sulfur_dioxide", "Total sulfur dioxide", 0.0, 300.0, 34.0),
    ("density", "Density", 0.98, 1.01, 0.9978),
    ("ph", "pH", 2.5, 4.5, 3.51),
    ("sulphates", "Sulphates", 0.0, 3.0, 0.56),
    ("alcohol", "Alcohol", 5.0, 20.0, 9.4),
)

assert tuple(field[0] for field in FEATURE_FIELDS) == FEATURE_NAMES


def build_gateway(bundle_value: str | None) -> InferenceGateway:
    """Selecciona el bundle configurado o conserva el gateway demo de S5."""

    if not bundle_value:
        return DemoGateway()
    return PackagedBundleGateway.from_bundle_path(Path(bundle_value))


def collect_values(st: Any) -> tuple[bool, dict[str, float]]:
    """Formulario heredado de S5; no es un TODO de esta semana."""

    values: dict[str, float] = {}
    with st.form("wine_quality_form"):
        st.caption("Formulario de S5: la inferencia se envía al pulsar el botón.")
        columns = st.columns(2)
        for index, (name, label, minimum, maximum, default) in enumerate(
            FEATURE_FIELDS
        ):
            with columns[index % 2]:
                values[name] = st.number_input(
                    label,
                    min_value=minimum,
                    max_value=maximum,
                    value=default,
                    key=f"input_{name}",
                )
        submitted = st.form_submit_button("Ejecutar inferencia")
    return submitted, values


def get_cached_gateway(st: Any, bundle_value: str | None) -> InferenceGateway:
    """Reutiliza el gateway para cada configuración del bundle."""
    try:
        return st.cache_resource(show_spinner=False)(build_gateway)(bundle_value)
    except Exception as error:  # noqa: BLE001 - frontera de carga del recurso
        return UnavailableGateway(str(error))


def render_state(st: Any, state: UiState, target: Any | None = None) -> None:
    """Muestra el estado actual y la recuperación disponible."""
    output = st if target is None else target
    if state.phase == "idle":
        output.info("Completa el formulario y pulsa «Ejecutar inferencia».")
    elif state.phase == "loading":
        output.info("Validando la muestra y ejecutando el modelo…")
    elif state.error is not None:
        output.error(state.error.title)
        output.write(state.error.message)
        output.info(state.error.recovery)
        with output.expander("Trazabilidad"):
            output.caption(f"Request ID: {state.error.request_id}")
    elif state.view is not None:
        view = state.view
        output.success(view.quality_label)
        category, confidence, latency = output.columns(3)
        category.metric("Categoría", view.quality_band)
        confidence.metric(view.confidence_label, f"{view.confidence:.0%}")
        latency.metric("Latencia", f"{view.latency_ms:.1f} ms")
        show_confidence = (
            output.warning if view.confidence_level == "low" else output.info
        )
        show_confidence(view.confidence_message)
        show_latency = (
            output.warning if view.latency_status == "above_target" else output.caption
        )
        show_latency(view.latency_message)
        with output.expander("Trazabilidad"):
            output.write(f"Modelo: {view.model_version}")
            output.write(f"Preprocesado: {view.preprocessing_version}")
            output.caption(f"Request ID: {state.request_id}")


def main() -> None:
    """Ejecuta la app de S5 con estado avanzado de S6."""

    try:
        import streamlit as st
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Instala Streamlit con `uv run --with streamlit streamlit run app.py`."
        ) from error

    st.set_page_config(page_title="Wine Quality · S6", page_icon="🍷")
    st.title("Inferencia de calidad de vino")
    st.caption("S6: la app de S5 ahora conserva estado y comunica la operación.")

    initialize_session_state(st.session_state)
    bundle_value = os.getenv("MODEL_UI_BUNDLE")
    gateway = get_cached_gateway(st, bundle_value)
    telemetry = st.session_state[TELEMETRY_KEY]
    controller = PredictionController(gateway, telemetry=telemetry)

    submitted, values = collect_values(st)
    state_slot = st.empty()
    if submitted:
        st.session_state[LAST_VALUES_KEY] = values
        with st.status("Ejecutando inferencia…", expanded=False) as status:
            state = controller.submit(
                values,
                emit=lambda event: (
                    render_state(st, event, state_slot)
                    if event.phase == "loading"
                    else None
                ),
            )
            st.session_state[LAST_STATE_KEY] = state
            state_slot.empty()
            status.update(
                label=(
                    "Inferencia completada"
                    if state.phase == "success"
                    else "La inferencia necesita atención"
                ),
                state="complete" if state.phase == "success" else "error",
            )

    if st.button("Limpiar último resultado"):
        clear_last_state(st.session_state)
        st.rerun()

    state = st.session_state[LAST_STATE_KEY]
    render_state(st, state)
    if state.phase == "error" and st.session_state[LAST_VALUES_KEY]:
        if st.button("Reintentar"):
            retry_state = controller.submit(st.session_state[LAST_VALUES_KEY])
            st.session_state[LAST_STATE_KEY] = retry_state
            st.rerun()

    st.divider()
    st.subheader("Telemetría de la sesión")
    st.json(telemetry.snapshot().__dict__)
    st.caption("Solo se muestran agregados; no se guardan las features en Telemetry.")


if __name__ == "__main__":
    main()
