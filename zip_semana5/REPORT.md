# Semana 5 · Streamlit e inferencia local

**Leyenda:** `->` objetivo · `~>` decisión y motivo · `>` acción · `>>` evidencia · `=>` resultado verificado.

`->` Conecto un modelo a un formulario y traslado el mismo flujo al contrato Wine Quality de la semana 4.

| Práctica | Entrega | Comprobación |
| --- | --- | --- |
| 5.1 · Churn | [App](modules/05-streamlit-basic-model-ui/exercises/01-churn-streamlit/problem/starter/app.py) | [Prueba en Chrome](entrega/evidencias/5.1-navegador.txt) y [13 tests](entrega/evidencias/5.1-pruebas.txt) |
| Contrato Wine de las diapositivas | [Notebook ejecutado](entrega/01-ui-form-alumno.ipynb) y [esquema](modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/problem/starter/src/model_ui/ui_schema.py) | 11 claves, rangos, valores por defecto y pasos; payload validado con la muestra `red-001` de S3 |
| 5.2 · Wine Quality | [App](modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/problem/starter/app.py) | [QA con el bundle real](entrega/evidencias/5.2-streamlit.txt) y [27 tests](entrega/evidencias/5.2-pruebas.txt) |

`~>` Uso un único `st.form` para separar la edición del envío. En Wine importo `FIELD_SPECS` tanto en el notebook como en la app para que el contrato tenga una única fuente. Los ejemplos de Churn sirven para entender los reruns; el repositorio asigna Churn a 5.1 y el consumo de Wine a 5.2, y las diapositivas piden además el diseño del formulario Wine.

`>` Desde cada directorio `problem/starter`:

```bash
uv sync --locked
uv run --locked python -m pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

`>` Para abrir Churn: `uv run --locked streamlit run app.py`. Para abrir Wine:

```bash
MODEL_UI_BUNDLE=/ruta/al/wine_quality_bundle uv run --locked --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

`>>` Probé dos perfiles Churn con scores 0,95 y 0,05. Es una regla docente: el score no es una probabilidad calibrada. En Wine comprobé el arranque, la edición sin predicción, un envío, un valor en el límite y el mensaje cuando falta el bundle. Los resultados muestran categoría, confianza y las versiones de modelo y preprocesado.

`=>` Las dos apps pasan 40 pruebas en total y Ruff. Wine se ejecutó con `wine-quality-rf-v1` y `wine-red-features-v1`; el artefacto se reconstruye siguiendo [S4](../semana4/REPORT.md).

`>>` En los PDF originales, las rutas que empiezan por `semana5/` corresponden aquí a `zip_semana5/`.
