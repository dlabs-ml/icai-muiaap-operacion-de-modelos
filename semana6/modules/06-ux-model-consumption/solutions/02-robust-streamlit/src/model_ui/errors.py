"""Errores de frontera que la UI puede traducir a acciones."""


class InputContractError(ValueError):
    """La petición no cumple el contrato de entrada del modelo."""


class ArtifactUnavailableError(FileNotFoundError):
    """El bundle o el backend necesario no está disponible."""


class InferenceTimeoutError(TimeoutError):
    """La inferencia superó el tiempo permitido por el consumidor."""


class BackendInferenceError(RuntimeError):
    """El backend no pudo producir una salida compatible."""
