# Guion docente — Clase 2: frontal Wine sobre el bundle S4

**Duración:** 120 minutos de práctica guiada

**Resultado:** cada pareja completa una app Streamlit que consume su bundle
real de S4, conserva el contrato Wine de once variables y presenta una
predicción trazable.

## Antes de empezar

- Pedir a cada pareja el directorio de su bundle S4 con `manifest.json` y
  `model.joblib`.
- Distribuir
  [`exercises/02-first-streamlit/problem/starter/`](../exercises/02-first-streamlit/problem/starter/).
- Confirmar que `src/model_ui/ui_schema.py` ya contiene los once
  `FIELD_SPECS`; no se copia ningún archivo de 5.1.
- Explicar que los dobles del gateway pertenecen solo a los tests. La
  aplicación exige `MODEL_UI_BUNDLE`.
- Mantener cerrada la solución hasta el debrief.

## Puente conceptual desde 5.1

La Práctica 5.1 no entrega código reutilizable para Wine. Transfiere un patrón:

| Se conserva | Wine añade o sustituye |
| --- | --- |
| `st.form` y submit explícito | once campos canónicos |
| cero llamadas al editar y una al enviar | `InferenceGateway.predict(values)` |
| frontera entre UI e inferencia | bundle real de S4 |
| presentación y error seguro | cuatro campos de `PredictionPayload` |

No se reutilizan los datos, los labels ni la regla de Churn.

## Secuencia de 120 minutos

| Minutos | Hito | Comprobación |
| ---: | --- | --- |
| 0–15 | Localizar y validar el bundle de S4 | La variable apunta al directorio correcto. |
| 15–35 | Construir los once widgets | Cada widget usa el nombre canónico y su `FieldSpec`. |
| 35–55 | Formulario y semántica del submit | Hay un formulario, cero llamadas al editar y una al enviar. |
| 55–75 | Conexión con el gateway | La UI llama solo a `gateway.predict(values)`. |
| 75–90 | Presentación del resultado | Se ven categoría, confianza y dos versiones. |
| 90–105 | Tratamiento del bundle ausente | Mensaje accionable sin ruta, excepción ni traceback. |
| 105–115 | Tests y QA visual | Tests verdes y matriz de cuatro casos completada. |
| 115–120 | Documentación y límites de S6 | Se registra cómo arrancar y qué se aplaza. |

## Preparación y ejecución

PowerShell, desde la raíz del repositorio:

```powershell
Set-Location .\semana5\modules\05-streamlit-basic-model-ui\exercises\02-first-streamlit\problem\starter
uv sync
$env:MODEL_UI_BUNDLE = 'RUTA_AL_BUNDLE_DE_S4'
uv run python -m pytest -q
uv run ruff check app.py src tests
uv run ruff format --check app.py src tests
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

Antes de implementar, los fallos deben corresponder únicamente a
`collect_values()` y `render_prediction()`. Después, toda la suite y las
comprobaciones de estilo deben quedar verdes.

## Criterios de aceptación

- El bundle S4 es un prerrequisito efectivo de ejecución.
- Los once campos proceden del esquema completo entregado en el starter.
- Editar genera cero llamadas; cada submit genera una.
- `app.py` usa la frontera del gateway y no carga `joblib`, el estimador ni el
  preprocesador.
- La pantalla muestra `quality_band`, `confidence`, `model_version` y
  `preprocessing_version`.
- Un bundle ausente o inválido produce un mensaje seguro con la siguiente
  acción.
- No existe un recorrido de ejecución con predicciones simuladas.

## QA manual

| Caso | Acción | Resultado esperado |
| --- | --- | --- |
| Arranque con bundle | Configurar un bundle válido y abrir la app. | Once campos visibles y cero inferencias. |
| Edición sin envío | Modificar una o varias medidas. | El gateway no recibe llamadas. |
| Submit válido | Pulsar **Ejecutar inferencia**. | Una llamada y cuatro campos de salida. |
| Bundle ausente | Quitar la variable o usar un directorio inválido. | Mensaje accionable sin detalle interno. |

Para probar el último caso en PowerShell:

```powershell
Remove-Item Env:MODEL_UI_BUNDLE -ErrorAction SilentlyContinue
```

Una ejecución sin bundle real no es una evidencia válida de entrega.

## Cierre hacia S6

La pareja anota dos límites observables —por ejemplo, resultado no persistente
y recurso no reutilizado— sin resolverlos todavía. Estado de sesión, caché,
FSM, latencia y telemetría pertenecen a S6.
