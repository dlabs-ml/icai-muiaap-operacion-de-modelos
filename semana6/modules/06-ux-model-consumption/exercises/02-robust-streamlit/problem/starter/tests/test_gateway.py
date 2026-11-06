import pytest

from model_ui.errors import InputContractError
from model_ui.gateway import FEATURE_NAMES, DemoGateway


def test_demo_gateway_rejects_unknown_and_missing_features() -> None:
    gateway = DemoGateway()
    sample = {name: 1.0 for name in FEATURE_NAMES}
    with pytest.raises(InputContractError, match="no permitidos"):
        gateway.predict({**sample, "unexpected": 1.0})
    missing = dict(sample)
    missing.pop("alcohol")
    with pytest.raises(InputContractError, match="faltan"):
        gateway.predict(missing)
