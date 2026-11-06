from dataclasses import FrozenInstanceError
from typing import get_type_hints

import pytest

from model_ui.gateway import FEATURE_NAMES
from model_ui.ui_schema import FIELD_SPECS, FieldSpec

EXPECTED_RANGES = (
    ("fixed_acidity", 0.0, 20.0),
    ("volatile_acidity", 0.0, 2.0),
    ("citric_acid", 0.0, 2.0),
    ("residual_sugar", 0.0, 20.0),
    ("chlorides", 0.0, 1.0),
    ("free_sulfur_dioxide", 0.0, 100.0),
    ("total_sulfur_dioxide", 0.0, 300.0),
    ("density", 0.98, 1.01),
    ("ph", 2.5, 4.5),
    ("sulphates", 0.0, 3.0),
    ("alcohol", 5.0, 20.0),
)


def test_schema_uses_the_exact_gateway_keys_once_and_in_order() -> None:
    names = tuple(field.name for field in FIELD_SPECS)
    assert names == FEATURE_NAMES
    assert len(names) == len(set(names)) == 11
    assert (
        tuple((field.name, field.min_value, field.max_value) for field in FIELD_SPECS)
        == EXPECTED_RANGES
    )


def test_schema_is_ready_to_render_without_exercise_markers() -> None:
    for field in FIELD_SPECS:
        assert field.label.strip()
        assert "todo" not in field.label.casefold()
        assert field.default is not None
        assert field.min_value <= field.default <= field.max_value
        assert field.step is not None
        assert field.step > 0


def test_schema_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        FIELD_SPECS[0].label = "otro"  # type: ignore[misc]


def test_schema_field_types_are_complete_and_non_optional() -> None:
    assert get_type_hints(FieldSpec) == {
        "name": str,
        "label": str,
        "min_value": float,
        "max_value": float,
        "default": float,
        "step": float,
    }
