"""Errores que la capa de UX debe convertir en acciones."""


class InputContractError(ValueError):
    """La petición no cumple el contrato de entrada."""


class ArtifactUnavailableError(FileNotFoundError):
    """El bundle o backend no está disponible."""


class InferenceTimeoutError(TimeoutError):
    """La inferencia tardó más de lo permitido."""


class BackendInferenceError(RuntimeError):
    """El backend no produjo una salida compatible."""
