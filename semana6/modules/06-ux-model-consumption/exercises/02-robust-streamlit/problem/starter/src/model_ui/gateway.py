"""Gateways proporcionados para separar UI de inferencia."""

from __future__ import annotations

import sys
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Protocol

from pydantic import ValidationError

from model_ui.contracts import PredictionPayload
from model_ui.errors import (
    ArtifactUnavailableError,
    BackendInferenceError,
    InferenceTimeoutError,
    InputContractError,
)

FEATURE_NAMES = (
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
)


class InferenceGateway(Protocol):
    """Frontera sustituible por un cliente HTTP en S7."""

    def predict(self, values: Mapping[str, object]) -> PredictionPayload:
        """Devuelve una salida validada."""


def _validate_feature_names(values: Mapping[str, object]) -> None:
    """Rechaza campos ausentes o desconocidos antes de inferir."""

    missing = [name for name in FEATURE_NAMES if name not in values]
    unknown = [name for name in values if name not in FEATURE_NAMES]
    if missing or unknown:
        details = []
        if missing:
            details.append(f"faltan: {', '.join(missing)}")
        if unknown:
            details.append(f"no permitidos: {', '.join(unknown)}")
        raise InputContractError(
            "La muestra no cumple el contrato: " + "; ".join(details)
        )


class DemoGateway:
    """Backend determinista para ejecutar la práctica sin un `.joblib`."""

    def __init__(
        self,
        *,
        quality_band: str = "acceptable",
        confidence: float = 0.74,
        delay_seconds: float = 0.0,
        model_version: str = "demo-ui-v1",
        preprocessing_version: str = "wine-red-features-v1",
    ) -> None:
        self._prediction = PredictionPayload(
            quality_band=quality_band,
            confidence=confidence,
            model_version=model_version,
            preprocessing_version=preprocessing_version,
        )
        self._delay_seconds = delay_seconds

    def predict(self, values: Mapping[str, object]) -> PredictionPayload:
        """Valida claves y devuelve la salida determinista."""

        _validate_feature_names(values)
        if self._delay_seconds > 0:
            time.sleep(self._delay_seconds)
        return self._prediction


class UnavailableGateway:
    """Permite mostrar el estado de bundle no disponible."""

    def __init__(self, reason: str = "El bundle no está disponible.") -> None:
        self._reason = reason

    def predict(self, values: Mapping[str, object]) -> PredictionPayload:
        """Falla de forma traducible por el controlador."""

        raise ArtifactUnavailableError(self._reason)


class PackagedBundleGateway:
    """Adaptador del bundle de S4, sin duplicar su inferencia."""

    def __init__(
        self,
        bundle: Any,
        request_model: Any,
        infer_function: Callable[[Any, Any], Any],
    ) -> None:
        self._bundle = bundle
        self._request_model = request_model
        self._infer_function = infer_function

    @classmethod
    def from_bundle_path(cls, bundle_path: Path) -> PackagedBundleGateway:
        """Localiza el código de S4 y carga el bundle validado."""

        try:
            from model_packaging.artifact import infer_wine_quality, load_model_bundle
            from model_packaging.contracts import WineQualityRequest
        except ModuleNotFoundError:
            repository_root = _find_repository_root(Path(__file__))
            source = repository_root / (
                "semana4/modules/04-model-packaging/solutions/"
                "01.02-serializable-inference-module/src"
            )
            if str(source) not in sys.path:
                sys.path.insert(0, str(source))
            from model_packaging.artifact import infer_wine_quality, load_model_bundle
            from model_packaging.contracts import WineQualityRequest
        bundle = load_model_bundle(bundle_path)
        return cls(bundle, WineQualityRequest, infer_wine_quality)

    def predict(self, values: Mapping[str, object]) -> PredictionPayload:
        """Construye el request de S4 y valida la respuesta."""

        _validate_feature_names(values)
        try:
            request = self._request_model.model_validate(dict(values))
        except ValidationError as error:
            raise InputContractError(
                "La muestra no cumple el contrato de entrada."
            ) from error
        try:
            prediction = self._infer_function(self._bundle, request)
            return PredictionPayload.model_validate(prediction.model_dump())
        except FileNotFoundError as error:
            raise ArtifactUnavailableError(
                "No se encontró el bundle configurado."
            ) from error
        except TimeoutError as error:
            raise InferenceTimeoutError(
                "La inferencia superó el tiempo permitido."
            ) from error
        except ValidationError as error:
            raise BackendInferenceError(
                "La salida del modelo no cumple el contrato."
            ) from error
        except (TypeError, ValueError) as error:
            raise BackendInferenceError(
                "El bundle no pudo producir una salida válida."
            ) from error


def _find_repository_root(start: Path) -> Path:
    """Encuentra el checkout para localizar el código docente de S4."""

    for parent in (start, *start.parents):
        if (parent / "semana4/modules/04-model-packaging").is_dir():
            return parent
    raise ArtifactUnavailableError("No se encontró el repositorio de la asignatura.")
