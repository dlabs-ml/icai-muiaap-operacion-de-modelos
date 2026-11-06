# Clase 2 — Taller: evolucionar la app de S5

**Duración:** 2 horas de práctica

La pareja trabaja sobre un snapshot del proyecto de S5. El formulario básico ya
está presente; el trabajo consiste en convertir su ejecución implícita en una
experiencia con estado explícito y recursos reutilizables.

## Qué viene de S5

- `FEATURE_FIELDS` y los once nombres del contrato;
- `st.form` y los widgets de entrada;
- selección de `DemoGateway` o bundle de S4;
- presentación básica de categoría, confianza y versiones.

## Qué se implementa en S6

- inicialización idempotente de `st.session_state`;
- carga cacheada del gateway mediante `st.cache_resource`;
- controlador independiente de Streamlit;
- transiciones `loading → success/error`;
- reintento y limpieza del último resultado;
- copy de confianza y latencia;
- errores accionables con `request_id`;
- telemetría agregada.

## Secuencia

| Minutos | Hito | Pista | Comprobación |
| ---: | --- | --- | --- |
| 0–10 | Comparar S5 y starter S6 | “El formulario ya está hecho.” | Localizan solo las nuevas fronteras. |
| 10–25 | Estado de sesión | “Inicializa sin sobrescribir.” | La predicción sobrevive a un rerun. |
| 25–40 | Caché | “El recurso se carga, los datos no se confunden.” | El gateway no se reconstruye innecesariamente. |
| 40–65 | Políticas y presentación | “Confianza y latencia son señales distintas.” | Límites y copy pasan los tests. |
| 65–90 | Controlador | “Emite `loading` antes del gateway.” | Se observan transiciones y request ID. |
| 90–110 | Renderizado avanzado | “Usa un placeholder o `st.status`.” | La app comunica carga, éxito y error. |
| 110–120 | Reintento y debrief | “No borres telemetría al limpiar.” | Aceptación de sesión completa. |

## Criterios de aceptación

Después de completar los `TODO` del starter:

```bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
```

Además, la demo debe mostrar:

- un resultado que permanece tras un rerun;
- gateway cargado mediante caché de recurso;
- estado de carga visible;
- error de entrada y error de bundle con recuperación;
- confianza baja sin lenguaje de garantía;
- latencia alta como `success` lento, no como error de contrato;
- botón de reintento y botón de limpiar;
- telemetría sin valores del formulario.
