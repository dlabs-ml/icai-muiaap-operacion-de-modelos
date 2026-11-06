"""Cliente HTTP para la API docente de bombas."""

from __future__ import annotations

from typing import Any

import requests


class PredictionClientError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


def request_prediction(
    payload: dict[str, Any],
    *,
    base_url: str = "http://127.0.0.1:8000",
    timeout: float = 5.0,
    session: Any | None = None,
) -> dict[str, Any]:
    """Envía una predicción y devuelve un objeto JSON de respuesta."""
    client = requests if session is None else session
    try:
        response = client.post(
            f"{base_url.rstrip('/')}/v1/predictions",
            json=payload,
            headers={"Accept": "application/json"},
            timeout=timeout,
            # Una redirección 307/308 podría volver a enviar el POST con los datos.
            allow_redirects=False,
        )
        response.raise_for_status()
    except requests.Timeout as error:
        raise PredictionClientError("Se agotó el tiempo de espera.") from error
    except requests.ConnectionError as error:
        raise PredictionClientError("No se pudo conectar con la API.") from error
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else None
        raise PredictionClientError(
            "La API rechazó la petición.", status_code=status
        ) from error
    except requests.RequestException as error:
        raise PredictionClientError("No se pudo completar la petición.") from error
    if not 200 <= response.status_code < 300:
        raise PredictionClientError(
            "La API no devolvió un estado de éxito.", status_code=response.status_code
        )
    try:
        body = response.json()
    except ValueError as error:
        raise PredictionClientError("La API no devolvió JSON válido.") from error
    if not isinstance(body, dict):
        raise PredictionClientError("La respuesta debe ser un objeto JSON.")
    return body
