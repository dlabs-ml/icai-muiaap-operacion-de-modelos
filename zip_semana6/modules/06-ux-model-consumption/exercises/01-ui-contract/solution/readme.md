# Solución orientativa — Estado de una app Streamlit de inferencia

Una solución válida conserva solo agregados y view models:

| Clave | Tipo | Razón |
| --- | --- | --- |
| `last_state` | `UiState` | Permite volver a pintar el último resultado tras un rerun. |
| `telemetry` | `Telemetry` | Acumula contadores, errores, latencias y versiones. |
| gateway cacheado | recurso | Evita cargar el bundle en cada ejecución. |
| valores completos del formulario | no se registran | Pueden contener datos que no deben entrar en telemetría. |

Las transiciones mínimas son:

```text
idle --submit--> loading --valid payload--> success
                         └--exception----> error
```

La app de S5 conserva el formulario. S6 añade `session_state`, un gateway
cacheado, un `PredictionController` y un renderizado que traduce errores a
mensajes accionables. Limpiar vuelve a `idle` sin borrar `Telemetry`.

Una salida válida con latencia alta sigue siendo `success` y lleva
`latency_status=above_target`. No se mezcla con un error de contrato.
