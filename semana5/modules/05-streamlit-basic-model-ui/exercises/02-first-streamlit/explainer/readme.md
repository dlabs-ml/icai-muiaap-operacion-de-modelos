# Explicación — La app Wine como adaptador fino

Durante los **120 minutos** de la práctica, la interfaz de S5 traduce una
interacción humana a una llamada al contrato de inferencia de S4 y traduce la
respuesta validada a una pantalla:

```text
11 widgets -> st.form -> gateway.predict(values) -> PredictionPayload -> pantalla
                              |
                              +-> bundle real de S4
```

`ui_schema.py` ya contiene las once especificaciones Wine completas. Es la
única fuente para nombres, etiquetas, rangos, valores iniciales y pasos; por
eso `app.py` no mantiene una segunda lista de campos.

El formulario agrupa las ediciones. Mientras no se pulse el botón, el gateway
recibe cero llamadas. Tras un submit válido recibe exactamente una. Esta es la
misma regla conceptual practicada con Churn, pero no se copian sus campos ni su
función `predict()`.

## Frontera del bundle

`build_gateway()` exige `MODEL_UI_BUNDLE` y construye el adaptador del bundle
S4. Si falta la variable o falla la carga, `run_configured_app()` detiene el
flujo antes de dibujar el formulario y muestra una instrucción segura. La UI
no imprime la excepción original, la ruta interna ni un traceback.

Los dobles usados para comprobar llamadas existen solo bajo `tests/`. En una
ejecución de la aplicación no hay predicciones sustitutas: el bundle S4 es un
prerrequisito.

PowerShell, desde la raíz del repositorio:

```powershell
cd semana5/modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/problem/starter
uv sync
$env:MODEL_UI_BUNDLE = 'RUTA_AL_BUNDLE_DE_S4'
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

La comprobación manual cubre exactamente cuatro casos: arranque con bundle,
edición sin envío, submit válido y bundle ausente. Los criterios y los diez
puntos de la rúbrica están detallados en el [enunciado principal](../README.md).

Persistencia con `session_state`, caché, FSM y telemetría quedan para S6.
