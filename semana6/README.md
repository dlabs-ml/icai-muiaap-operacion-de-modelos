# Semana 6 — Streamlit avanzado para servir un modelo de IA

[Ver mi entrega, comprobaciones y evidencias](zip_semana6/REPORT.md).

S6 es la continuación directa de la interfaz que el alumnado construye en S5.
No vuelve a enseñar widgets ni a crear una app desde cero. Parte de una primera
app funcional y la convierte en una aplicación más robusta mediante estado de
sesión, caché de recursos, máquina de estados, errores accionables, latencia,
confianza y telemetría agregada.

## Hilo conductor

```text
S3: módulo local
      ↓
S4: bundle validado
      ↓
S5: formulario Streamlit + primera predicción
      ↓
S6: reruns controlados + estado + UX robusta
      ↓
S7: gateway HTTP
```

La app de S5 es el punto de partida. El código de S6 conserva el formulario y
la frontera `InferenceGateway`, pero extrae las decisiones que se vuelven
importantes cuando Streamlit reejecuta el script.

## Continuidad entre semanas

| Semana | Entrada que llega a S6 | Evolución |
| --- | --- | --- |
| [S1](../semana1/README.md) | Riesgos, trazabilidad y límites de interpretación | La confianza, la latencia y los errores se comunican como señales operativas, no como garantías. |
| S2 | Proyecto modular y dependencias reproducibles | El refactor conserva la separación entre app, gateway, contratos y tests. |
| [S3](../semana3/README.md) | `WineQualityRequest`, once features y `WineQualityPrediction` | S6 conserva el esquema de salida al adaptarlo a la vista de la UI. |
| [S4](../semana4/README.md) | `manifest.json`, `model.joblib`, versiones e inferencia empaquetada | S6 conserva el gateway como única frontera con el bundle. |
| [S5](../semana5/README.md) | App Streamlit básica con formulario, botón y resultado | S6 añade `st.session_state`, `st.cache_resource`, estados y reintentos. |

## Qué debe saber el alumnado antes de S6

- crear una app Streamlit y ejecutarla;
- usar `st.form`, `st.number_input`, columnas y mensajes básicos;
- recoger los once campos del contrato;
- llamar a un gateway y mostrar un payload;
- explicar que cada interacción puede provocar un rerun.

## Clases

### Clase 1 — Del rerun implícito al estado explícito

Se inspecciona la app de S5, se observa qué se pierde en cada rerun y se diseña
una máquina de estados para una petición de inferencia. Se introducen
`st.session_state`, `st.cache_resource`, placeholders, estados de carga,
reintentos y UX de errores. La teoría se aterriza sobre la aplicación existente.

[Material de la clase 1](modules/06-ux-model-consumption/sessions/01-ux-estados-confianza/README.md)

### Clase 2 — Taller: evolucionar la app de S5

La pareja recibe un snapshot de la app básica de S5. Mantiene el formulario,
pero implementa el estado de sesión, el gateway cacheado, el controlador de
transiciones y la presentación avanzada de errores, confianza y latencia.

[Material de la clase 2](modules/06-ux-model-consumption/sessions/02-interfaz-robusta/README.md)

## Prácticas y entregables

- [Práctica 01 — analizar y diseñar el estado de la app de S5](modules/06-ux-model-consumption/exercises/01-ui-contract/problem/README.md).
- [Práctica 02 — refactorizar S5 como interfaz avanzada](modules/06-ux-model-consumption/exercises/02-robust-streamlit/README.md).
- [Solución docente](modules/06-ux-model-consumption/solutions/02-robust-streamlit/README.md).

La entrega es una evolución de la app de S5, no una aplicación paralela:

- el formulario de S5 sigue funcionando;
- el gateway se carga una sola vez mediante `st.cache_resource`;
- la última respuesta y la telemetría sobreviven a los reruns;
- se observan `idle`, `loading`, `success` y `error`;
- hay reintento y limpieza del resultado;
- confianza y latencia se comunican sin sobreafirmar;
- los errores muestran una acción y `request_id`, no un traceback;
- la telemetría no contiene los valores de las features.

## Ejecución

Desde `semana6/`:

```bash
uv sync
uv run pytest
uv run ruff check modules/06-ux-model-consumption/solutions
uv run ruff format --check modules/06-ux-model-consumption/solutions
uv sync --extra app
uv run streamlit run modules/06-ux-model-consumption/solutions/02-robust-streamlit/app.py
```

Para trabajar con el starter:

```bash
cd modules/06-ux-model-consumption/exercises/02-robust-streamlit/problem/starter
uv sync
uv run pytest
uv run ruff check src tests
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

El starter conserva `TODO` en los puntos de extensión del taller; sus tests
empiezan en rojo y deben quedar verdes cuando se complete la implementación.
