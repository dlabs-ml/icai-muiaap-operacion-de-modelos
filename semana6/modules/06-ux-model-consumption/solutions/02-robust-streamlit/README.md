# Solución — App de S5 evolucionada con Streamlit avanzado

La solución conserva el formulario de S5 y añade:

- `session.py`: inicialización idempotente y limpieza;
- `policies.py`: confianza y latencia como políticas explícitas;
- `controller.py`: estados, medición y errores;
- `telemetry.py`: agregados sin payload;
- `app.py`: `st.cache_resource`, `st.session_state`, `st.empty`/estado de carga,
  retry y clear;
- `gateway.py`: el mismo adaptador del bundle de S4.

## Ejecución

Desde `semana6/`:

```bash
uv run pytest
uv run ruff check modules/06-ux-model-consumption/solutions/02-robust-streamlit
uv run ruff format --check modules/06-ux-model-consumption/solutions/02-robust-streamlit
uv sync --extra app
uv run streamlit run modules/06-ux-model-consumption/solutions/02-robust-streamlit/app.py
```

La demo usa `DemoGateway` por defecto. Para un bundle real, define
`MODEL_UI_BUNDLE`. La app sigue sin conocer `joblib.load` ni el preprocesado.
