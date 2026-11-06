from __future__ import annotations

import sys
from collections.abc import Mapping

import app
import pytest
from bundle_fixture import SAMPLE, write_test_bundle
from fake_streamlit import FakeStreamlit
from model_ui.contracts import PredictionPayload
from model_ui.errors import ArtifactUnavailableError, InputContractError
from model_ui.gateway import FEATURE_NAMES, PackagedBundleGateway
from model_ui.ui_schema import FIELD_SPECS

PREDICTION = PredictionPayload(
    quality_band="acceptable",
    confidence=0.74,
    model_version="wine-model-v1",
    preprocessing_version="wine-preprocessing-v1",
)


class RecordingGateway:
    def __init__(self, prediction: PredictionPayload = PREDICTION) -> None:
        self.prediction = prediction
        self.calls: list[dict[str, object]] = []

    def predict(self, values: Mapping[str, object]) -> PredictionPayload:
        self.calls.append(dict(values))
        return self.prediction


class FailingGateway:
    def __init__(self, error: Exception) -> None:
        self.error = error
        self.calls = 0

    def predict(self, values: Mapping[str, object]) -> PredictionPayload:
        self.calls += 1
        raise self.error


def test_collect_values_renders_the_eleven_fields_inside_one_form() -> None:
    st = FakeStreamlit(submitted=False)

    submitted, values = app.collect_values(st)

    assert submitted is False
    assert tuple(values) == FEATURE_NAMES
    assert st.form_calls == ["wine_quality_form"]
    assert len(st.number_inputs) == 11
    assert {call.form_key for call in st.number_inputs} == {"wine_quality_form"}
    assert tuple(call.label for call in st.number_inputs) == tuple(
        field.label for field in FIELD_SPECS
    )
    assert len(st.submit_calls) == 1
    assert st.submit_calls[0].form_key == "wine_quality_form"
    assert st.submit_calls[0].label == "Ejecutar inferencia"
    assert tuple(call.kwargs["key"] for call in st.number_inputs) == tuple(
        f"input_{name}" for name in FEATURE_NAMES
    )
    assert tuple(call.kwargs["step"] for call in st.number_inputs) == tuple(
        field.step for field in FIELD_SPECS
    )
    assert tuple(
        (
            call.kwargs["min_value"],
            call.kwargs["max_value"],
            call.kwargs["value"],
        )
        for call in st.number_inputs
    ) == tuple(
        (field.min_value, field.max_value, field.default) for field in FIELD_SPECS
    )


def test_fake_rejects_widgets_and_submit_outside_a_form() -> None:
    st = FakeStreamlit()

    with pytest.raises(AssertionError, match="dentro de st.form"):
        st.number_input("Acidez", key="input_fixed_acidity", value=7.4)
    with pytest.raises(AssertionError, match="dentro de st.form"):
        st.form_submit_button("Ejecutar inferencia")


def test_no_submit_makes_zero_gateway_calls(monkeypatch) -> None:
    st = FakeStreamlit(submitted=False)
    gateway = RecordingGateway()
    monkeypatch.setattr(app, "collect_values", lambda _st: (False, SAMPLE))
    monkeypatch.setattr(
        app,
        "render_prediction",
        lambda _st, _prediction: (_ for _ in ()).throw(
            AssertionError("No debe renderizarse una predicción sin submit")
        ),
    )

    app.run_app(st, gateway)

    assert gateway.calls == []


def test_submit_makes_exactly_one_gateway_call(monkeypatch) -> None:
    st = FakeStreamlit(submitted=True)
    gateway = RecordingGateway()
    rendered: list[PredictionPayload] = []
    monkeypatch.setattr(app, "collect_values", lambda _st: (True, SAMPLE))
    monkeypatch.setattr(
        app, "render_prediction", lambda _st, item: rendered.append(item)
    )

    app.run_app(st, gateway)

    assert gateway.calls == [SAMPLE]
    assert rendered == [PREDICTION]


def test_render_prediction_shows_all_four_payload_fields() -> None:
    st = FakeStreamlit()

    app.render_prediction(st, PREDICTION)

    output = st.output_text()
    for field_name in (
        "quality_band",
        "confidence",
        "model_version",
        "preprocessing_version",
    ):
        assert field_name in output
    for value in (
        "acceptable",
        "0.74",
        "wine-model-v1",
        "wine-preprocessing-v1",
    ):
        assert value in output


def test_inference_bundle_error_is_actionable_and_hides_details(monkeypatch) -> None:
    secret_detail = r"Traceback: File C:\secret\models\wine.joblib"
    st = FakeStreamlit(submitted=True)
    gateway = FailingGateway(ArtifactUnavailableError(secret_detail))
    monkeypatch.setattr(app, "collect_values", lambda _st: (True, SAMPLE))

    app.run_app(st, gateway)

    output = st.output_text()
    assert gateway.calls == 1
    assert "MODEL_UI_BUNDLE" in output
    assert secret_detail not in output
    assert "Traceback" not in output
    assert "wine.joblib" not in output


@pytest.mark.parametrize("error_type", [InputContractError, ValueError])
def test_invalid_inference_error_is_actionable_and_hides_details(
    monkeypatch, error_type: type[ValueError]
) -> None:
    secret_detail = r"Traceback: File C:\secret\models\wine.joblib"
    st = FakeStreamlit(submitted=True)
    gateway = FailingGateway(error_type(secret_detail))
    monkeypatch.setattr(app, "collect_values", lambda _st: (True, SAMPLE))

    app.run_app(st, gateway)

    output = st.output_text()
    assert gateway.calls == 1
    assert "No se pudo ejecutar la inferencia." in output
    assert "Revisa los datos y la compatibilidad del bundle de S4." in output
    assert "MODEL_UI_BUNDLE" not in output
    assert secret_detail not in output
    assert "Traceback" not in output
    assert "wine.joblib" not in output


def test_build_gateway_without_configuration_raises(monkeypatch) -> None:
    monkeypatch.delenv("MODEL_UI_BUNDLE", raising=False)

    with pytest.raises(ArtifactUnavailableError, match="MODEL_UI_BUNDLE"):
        app.build_gateway()


def test_build_gateway_loads_the_configured_s4_bundle(monkeypatch, tmp_path) -> None:
    bundle_path = tmp_path / "wine-bundle"
    write_test_bundle(bundle_path)
    monkeypatch.setenv("MODEL_UI_BUNDLE", str(bundle_path))

    gateway = app.build_gateway()
    prediction = gateway.predict(SAMPLE)

    assert isinstance(gateway, PackagedBundleGateway)
    assert prediction.quality_band == "acceptable"
    assert prediction.model_version == "wine-test-v1"


def test_build_gateway_wraps_an_invalid_path_without_leaking_it(
    monkeypatch, tmp_path
) -> None:
    missing_path = tmp_path / "secret" / "wine.joblib"
    monkeypatch.setenv("MODEL_UI_BUNDLE", str(missing_path))

    with pytest.raises(ArtifactUnavailableError) as captured:
        app.build_gateway()

    assert str(captured.value) == "No se pudo cargar el bundle de S4."
    assert str(missing_path) not in str(captured.value)
    assert captured.value.__cause__ is not None


def test_configured_app_hides_bundle_error_details() -> None:
    st = FakeStreamlit()

    def failing_factory() -> RecordingGateway:
        raise ArtifactUnavailableError(r"Traceback C:\secret\wine.joblib")

    app.run_configured_app(st, failing_factory)

    output = st.output_text()
    assert "MODEL_UI_BUNDLE" in output
    assert "Traceback" not in output
    assert "wine.joblib" not in output


def test_configured_app_passes_the_loaded_gateway_to_run_app(monkeypatch) -> None:
    st = FakeStreamlit()
    gateway = RecordingGateway()
    calls: list[tuple[FakeStreamlit, RecordingGateway]] = []
    monkeypatch.setattr(app, "run_app", lambda ui, item: calls.append((ui, item)))

    app.run_configured_app(st, lambda: gateway)

    assert calls == [(st, gateway)]


def test_main_configures_the_page_and_delegates_to_configured_app(monkeypatch) -> None:
    st = FakeStreamlit()
    calls: list[FakeStreamlit] = []
    monkeypatch.setitem(sys.modules, "streamlit", st)
    monkeypatch.setattr(app, "run_configured_app", lambda ui: calls.append(ui))

    app.main()

    assert calls == [st]
    assert [event[0] for event in st.events[:3]] == [
        "set_page_config",
        "title",
        "caption",
    ]
