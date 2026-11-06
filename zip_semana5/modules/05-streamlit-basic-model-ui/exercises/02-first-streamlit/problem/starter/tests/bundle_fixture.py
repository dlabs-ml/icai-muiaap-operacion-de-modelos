from __future__ import annotations

import json
from pathlib import Path

import joblib

from model_ui.gateway import FEATURE_NAMES

SAMPLE = {
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "ph": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4,
}


class FixedEstimator:
    """Estimador importable y determinista para el bundle temporal de S4."""

    def predict(self, features: list[list[float]]) -> list[str]:
        return ["acceptable" for _ in features]

    def predict_proba(self, features: list[list[float]]) -> list[list[float]]:
        return [[0.1, 0.8, 0.1] for _ in features]


def write_test_bundle(bundle_path: Path) -> None:
    """Escribe el formato real de S4 sin reutilizar un gateway de ejecución."""

    bundle_path.mkdir()
    manifest = {
        "schema_version": "wine-quality-bundle-v1",
        "model_version": "wine-test-v1",
        "preprocessing_version": "wine-red-features-v1",
        "feature_names": list(FEATURE_NAMES),
        "output_labels": ["needs_review", "acceptable", "excellent"],
        "estimator_type": "FixedEstimator",
    }
    (bundle_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    joblib.dump({"estimator": FixedEstimator()}, bundle_path / "model.joblib")
