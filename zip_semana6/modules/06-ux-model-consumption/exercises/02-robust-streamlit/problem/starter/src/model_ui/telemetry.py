"""Telemetría agregada entregada como soporte del taller."""

from dataclasses import dataclass, field
from math import ceil
from statistics import mean


@dataclass(frozen=True)
class TelemetrySnapshot:
    """Snapshot sin valores del formulario."""

    requests_total: int
    requests_success: int
    requests_error: int
    errors_by_code: dict[str, int]
    latency_mean_ms: float | None
    latency_p95_ms: float | None
    model_versions: tuple[str, ...]
    preprocessing_versions: tuple[str, ...]


@dataclass
class Telemetry:
    """Cuenta peticiones y versiones sin guardar el payload."""

    requests_total: int = 0
    requests_success: int = 0
    requests_error: int = 0
    _latencies_ms: list[float] = field(default_factory=list, repr=False)
    _errors_by_code: dict[str, int] = field(default_factory=dict, repr=False)
    _model_versions: set[str] = field(default_factory=set, repr=False)
    _preprocessing_versions: set[str] = field(default_factory=set, repr=False)

    def record_success(
        self,
        latency_ms: float,
        *,
        model_version: str,
        preprocessing_version: str,
    ) -> None:
        """Registra éxito y versiones."""

        self.requests_total += 1
        self.requests_success += 1
        self._latencies_ms.append(round(float(latency_ms), 3))
        self._model_versions.add(model_version)
        self._preprocessing_versions.add(preprocessing_version)

    def record_error(self, code: str, latency_ms: float) -> None:
        """Registra un error por código."""

        self.requests_total += 1
        self.requests_error += 1
        self._latencies_ms.append(round(float(latency_ms), 3))
        self._errors_by_code[code] = self._errors_by_code.get(code, 0) + 1

    def snapshot(self) -> TelemetrySnapshot:
        """Calcula agregados de latencia."""

        if self._latencies_ms:
            ordered = sorted(self._latencies_ms)
            p95_index = max(0, ceil(len(ordered) * 0.95) - 1)
            mean_latency = round(mean(ordered), 3)
            p95_latency = ordered[p95_index]
        else:
            mean_latency = None
            p95_latency = None
        return TelemetrySnapshot(
            requests_total=self.requests_total,
            requests_success=self.requests_success,
            requests_error=self.requests_error,
            errors_by_code=dict(sorted(self._errors_by_code.items())),
            latency_mean_ms=mean_latency,
            latency_p95_ms=p95_latency,
            model_versions=tuple(sorted(self._model_versions)),
            preprocessing_versions=tuple(sorted(self._preprocessing_versions)),
        )
