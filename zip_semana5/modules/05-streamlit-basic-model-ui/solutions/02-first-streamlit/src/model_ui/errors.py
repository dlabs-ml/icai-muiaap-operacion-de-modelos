"""Errores mínimos de la primera interfaz."""


class InputContractError(ValueError):
    """La petición no cumple la forma del contrato."""


class ArtifactUnavailableError(FileNotFoundError):
    """El bundle configurado no está disponible."""
