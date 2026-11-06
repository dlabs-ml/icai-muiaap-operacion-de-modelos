"""Doble mínimo de Streamlit para probar la app sin levantar un servidor."""

from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NumberInputCall:
    """Llamada registrada a ``number_input``."""

    label: str
    kwargs: dict[str, Any]
    form_key: str


@dataclass(frozen=True)
class SubmitCall:
    """Submit registrado junto al formulario que lo contiene."""

    label: str
    form_key: str


class _Context(AbstractContextManager["_Context"]):
    def __enter__(self) -> _Context:
        return self

    def __exit__(self, *exc_info: object) -> None:
        return None


class _FormContext(_Context):
    def __init__(self, owner: FakeStreamlit, key: str) -> None:
        self._owner = owner
        self._key = key

    def __enter__(self) -> _FormContext:
        if self._owner.active_form is not None:
            raise AssertionError("La práctica solo admite un formulario activo")
        self._owner.active_form = self._key
        return self

    def __exit__(self, *exc_info: object) -> None:
        self._owner.active_form = None
        return None


class _Column(_Context):
    def __init__(self, owner: FakeStreamlit) -> None:
        self._owner = owner

    def metric(self, label: str, value: object) -> None:
        self._owner.events.append(("metric", label, value))


class FakeStreamlit(_Context):
    """API mínima usada por ``app.py`` y registro observable de eventos."""

    def __init__(
        self,
        *,
        submitted: bool = False,
        input_values: dict[str, float] | None = None,
    ) -> None:
        self.submitted = submitted
        self.input_values = input_values or {}
        self.form_calls: list[str] = []
        self.submit_calls: list[SubmitCall] = []
        self.number_inputs: list[NumberInputCall] = []
        self.events: list[tuple[object, ...]] = []
        self.active_form: str | None = None

    def form(self, key: str) -> _FormContext:
        self.form_calls.append(key)
        self.events.append(("form", key))
        return _FormContext(self, key)

    def columns(self, count: int) -> list[_Column]:
        self.events.append(("columns", count))
        return [_Column(self) for _ in range(count)]

    def number_input(self, label: str, **kwargs: Any) -> float | None:
        form_key = self._require_form("number_input")
        self.number_inputs.append(
            NumberInputCall(label=label, kwargs=kwargs, form_key=form_key)
        )
        key = str(kwargs["key"])
        return self.input_values.get(key, kwargs.get("value"))

    def form_submit_button(self, label: str) -> bool:
        form_key = self._require_form("form_submit_button")
        self.submit_calls.append(SubmitCall(label=label, form_key=form_key))
        self.events.append(("form_submit_button", label))
        return self.submitted

    def _require_form(self, component: str) -> str:
        if self.active_form is None:
            raise AssertionError(f"{component} debe ejecutarse dentro de st.form")
        return self.active_form

    def expander(self, label: str) -> _Context:
        self.events.append(("expander", label))
        return _Context()

    def set_page_config(self, **kwargs: Any) -> None:
        self.events.append(("set_page_config", kwargs))

    def title(self, value: object) -> None:
        self.events.append(("title", value))

    def caption(self, value: object) -> None:
        self.events.append(("caption", value))

    def success(self, value: object) -> None:
        self.events.append(("success", value))

    def info(self, value: object) -> None:
        self.events.append(("info", value))

    def error(self, value: object) -> None:
        self.events.append(("error", value))

    def write(self, value: object) -> None:
        self.events.append(("write", value))

    def output_text(self) -> str:
        """Devuelve toda la salida como texto para aserciones de seguridad."""

        return repr(self.events)
