# Solución — Práctica 5.2 Wine

Tiempo de referencia: **120 minutos**. Esta solución resuelve las dos
responsabilidades del alumno: genera los once widgets desde `FIELD_SPECS` y
presenta los cuatro campos de `PredictionPayload`. La aplicación exige el
bundle real de S4; los dobles del gateway aparecen únicamente en `tests/`.

## Verificación

Desde la raíz del repositorio, en PowerShell:

```powershell
cd semana5/modules/05-streamlit-basic-model-ui/solutions/02-first-streamlit
uv sync
$env:MODEL_UI_BUNDLE = 'RUTA_AL_BUNDLE_DE_S4'
uv run python -m pytest -q
uv run ruff check app.py src tests
uv run ruff format --check app.py src tests
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

`uv` encuentra el `pyproject.toml` de `semana5/` en un directorio padre. La
ruta configurada debe ser el directorio del bundle S4 que contiene
`manifest.json` y `model.joblib`.

## QA de referencia: cuatro casos

| Caso | Resultado esperado |
|---|---|
| Arranque con bundle | Once campos visibles y cero inferencias. |
| Edición sin envío | Cero llamadas al gateway. |
| Submit válido | Una llamada y `quality_band`, `confidence`, `model_version` y `preprocessing_version`. |
| Bundle ausente | Instrucción sobre `MODEL_UI_BUNDLE` sin excepción, ruta ni traceback. |

La solución debe completar las 27 pruebas. Una ejecución sin bundle nunca es
una entrega válida.

## Rúbrica de referencia (10 puntos)

| Criterio | Puntos |
|---|---:|
| Once widgets gobernados por el esquema Wine | 2 |
| Cero/una llamada según el submit | 2 |
| Bundle S4 real detrás de `InferenceGateway` | 2 |
| Cuatro salidas presentadas | 2 |
| Error seguro, tests y QA | 2 |

`session_state`, caché, FSM y telemetría se incorporarán en S6.
