import pytest
from bundle_fixture import SAMPLE, write_test_bundle

import model_ui.gateway as gateway_module
from model_ui.contracts import PredictionPayload
from model_ui.errors import InputContractError
from model_ui.gateway import InferenceGateway, PackagedBundleGateway


@pytest.fixture
def packaged_gateway(tmp_path) -> PackagedBundleGateway:
    bundle_path = tmp_path / "wine-bundle"
    write_test_bundle(bundle_path)
    return PackagedBundleGateway.from_bundle_path(bundle_path)


def test_packaged_bundle_gateway_runs_the_real_s4_format(
    packaged_gateway: PackagedBundleGateway,
) -> None:
    prediction = packaged_gateway.predict(SAMPLE)

    assert isinstance(prediction, PredictionPayload)
    assert prediction.quality_band == "acceptable"
    assert prediction.confidence == 0.8
    assert prediction.model_version == "wine-test-v1"
    assert prediction.preprocessing_version == "wine-red-features-v1"


@pytest.mark.parametrize("missing", ["fixed_acidity", "alcohol"])
def test_packaged_gateway_rejects_a_missing_feature(
    packaged_gateway: PackagedBundleGateway, missing: str
) -> None:
    values = {name: value for name, value in SAMPLE.items() if name != missing}

    with pytest.raises(InputContractError, match="faltan"):
        packaged_gateway.predict(values)


def test_packaged_gateway_rejects_an_unknown_feature(
    packaged_gateway: PackagedBundleGateway,
) -> None:
    values = {**SAMPLE, "unexpected": 1.0}

    with pytest.raises(InputContractError, match="no permitidos"):
        packaged_gateway.predict(values)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("fixed_acidity", "no-es-un-numero"),
        ("density", 1.02),
        ("alcohol", 4.9),
    ],
)
def test_packaged_gateway_rejects_invalid_contract_values(
    packaged_gateway: PackagedBundleGateway, field: str, bad_value: object
) -> None:
    values = {**SAMPLE, field: bad_value}

    with pytest.raises(InputContractError, match="contrato de entrada"):
        packaged_gateway.predict(values)


def test_runtime_gateway_exposes_only_the_supported_gateway_types() -> None:
    runtime_types = {
        name
        for name, value in vars(gateway_module).items()
        if isinstance(value, type) and value.__module__ == gateway_module.__name__
    }

    assert runtime_types == {InferenceGateway.__name__, PackagedBundleGateway.__name__}
