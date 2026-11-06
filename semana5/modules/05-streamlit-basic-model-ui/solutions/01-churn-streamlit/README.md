# Solución — Práctica 5.1 Churn con Streamlit

La referencia resuelve únicamente las tres responsabilidades del ejercicio:
recoge el perfil en un formulario, ejecuta una inferencia después del submit y
presenta el resultado o un error seguro. La regla permanece en
`src/churn_demo/model.py` sin duplicarse en la interfaz.

## Verificación

Desde la raíz del repositorio:

```powershell
cd semana5/modules/05-streamlit-basic-model-ui/solutions/01-churn-streamlit
uv sync
uv run python -m pytest -q
uv run ruff check app.py src tests
uv run ruff format --check app.py src tests
uv run streamlit run app.py
```

La referencia debe producir `13 passed`. Las pruebas validan el modelo, los
cuatro widgets dentro de `churn_form`, la semántica de cero/una llamada, los
tres campos visibles y la ocultación del detalle de un error.

## QA de referencia

1. La app arranca y presenta cuatro widgets.
2. Editar sin enviar no produce una predicción.
3. Un submit válido muestra etiqueta, score y explicación.
4. Un segundo perfil enviado reemplaza visualmente el resultado.

El score pertenece a una regla docente y no es una probabilidad calibrada. La
solución no añade estado de sesión ni caché: esos mecanismos cambian el ciclo
de vida de la app y se introducen en S6.
