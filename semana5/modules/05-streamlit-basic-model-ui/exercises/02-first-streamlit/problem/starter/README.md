# Starter — Práctica 5.2 Wine

Tiempo previsto: **120 minutos**. Este proyecto ya contiene el contrato de los
once campos Wine y toda la integración con el bundle de S4. El trabajo del
alumno está limitado a dos funciones de `app.py`:

1. `collect_values()`: construir un único formulario a partir de
   `FIELD_SPECS`;
2. `render_prediction()`: mostrar los cuatro campos de `PredictionPayload`.

`run_app()` ya garantiza cero llamadas antes del submit y una después.
`run_configured_app()` contiene de forma segura los fallos de configuración o
carga. Los dobles de gateway se usan solo en `tests/`.

## Preparación

Desde la raíz del repositorio, en PowerShell:

```powershell
cd semana5/modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/problem/starter
uv sync
$env:MODEL_UI_BUNDLE = 'RUTA_AL_BUNDLE_DE_S4'
uv run python -m pytest -q
uv run ruff check app.py src tests
uv run ruff format --check app.py src tests
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

`RUTA_AL_BUNDLE_DE_S4` debe contener `manifest.json` y `model.joblib`. Sin ese
bundle la app muestra cómo configurar `MODEL_UI_BUNDLE`, pero la ejecución no
cuenta como entrega válida.

Antes de implementar los dos huecos, deben aprobarse 25 pruebas y fallar solo
las pruebas de `collect_values()` y `render_prediction()`. Al terminar, las 27
pruebas deben estar verdes.

## Checklist visual obligatorio

- [ ] Arranque con un bundle S4 válido: aparecen once campos y no hay inferencia.
- [ ] Edición sin envío: cero llamadas al gateway.
- [ ] Submit válido: una llamada y cuatro campos de salida.
- [ ] Bundle ausente o inválido: mensaje accionable sin ruta ni traceback.

No añadas `session_state`, caché, FSM ni telemetría; pertenecen a S6.
