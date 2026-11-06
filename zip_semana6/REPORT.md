# Semana 6 · Estado, experiencia de usuario y telemetría

**Leyenda:** `->` objetivo · `~>` decisión y motivo · `>` acción · `>>` evidencia · `=>` resultado verificado.

`->` Parto del formulario de Wine Quality de S5 y hago explícito qué ocurre antes, durante y después de una inferencia.

| Práctica | Entrega | Comprobación |
| --- | --- | --- |
| Miércoles · Churn con historial | [Starter resuelto](entrega/miercoles/05_practica_starter.py) y [AppTest](entrega/miercoles/test_historial.py) | [Notebook docente y ejercicio A–C](entrega/evidencias/6-miercoles-churn.txt) |
| 6.1 · Contrato de UI | [Notebook ejecutado](modules/06-ux-model-consumption/exercises/01-ui-contract/problem/01-estado-streamlit-alumno.ipynb) y [playground](modules/06-ux-model-consumption/exercises/01-ui-contract/problem/ui_playground.py) | [Cinco escenarios de presentación](entrega/evidencias/6.1-playground.txt) |
| 6.2 · Streamlit robusto | [App y starter](modules/06-ux-model-consumption/exercises/02-robust-streamlit/problem/starter) | [Flujos de Streamlit](entrega/evidencias/6.2-streamlit.txt) y [8 tests](entrega/evidencias/6.2-pruebas.txt) |

`~>` Guardo el último estado, los valores del último envío y la telemetría en la sesión. Cacheo el gateway cargado porque es un recurso que puedo reutilizar; no contiene las features de una petición. El reintento recupera el último envío y **Limpiar último resultado** vuelve a `idle` conservando los agregados.

`~>` Distingo confianza baja (<60 %), intermedia (60–<85 %) y alta (≥85 %). Por encima de 300 ms muestro un aviso sin descartar el resultado. Dejo las versiones y el identificador en un desplegable. En el playground separé también el identificador del mensaje principal para que la acción de recuperación destaque.

`>` Desde `problem/starter` de 6.2:

```bash
uv sync --locked --extra app
uv run --locked --extra app python -m pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
MODEL_UI_BUNDLE=/ruta/al/wine_quality_bundle uv run --locked --extra app streamlit run app.py
```

`>` Abro el playground desde el mismo starter con `uv run --locked --extra app streamlit run ../../../01-ui-contract/problem/ui_playground.py`. Para el ejercicio del miércoles ejecuto `uv run --locked --extra app streamlit run RUTA_A_05_practica_starter.py` desde ese entorno.

`>>` Capturas de Streamlit: [carga](entrega/evidencias/6.2-carga.jpg) · [éxito sin demora añadida](entrega/evidencias/6.2-exito.jpg) · [error con trazabilidad](entrega/evidencias/6.2-error.jpg) · [resultado tras reintentar](entrega/evidencias/6.2-reintento.jpg). Para que el estado de carga fuese visible, añadí una espera controlada de 7 s solo durante la captura de carga y reintento. Ambas ejecuciones usan el [bundle real de S4](../semana4/REPORT.md). La latencia de esas capturas no mide el rendimiento del modelo.

`=>` Verifiqué el rerun, la recuperación tras restaurar el bundle y que limpiar conserva la telemetría, que registra latencias, contadores, códigos y versiones sin guardar features. Para S7 mantengo el formulario, el controlador, el estado de sesión, la presentación y la telemetría; el cambio queda en la configuración y el gateway.

`>>` En los PDF originales, las rutas que empiezan por `semana6/` corresponden aquí a `zip_semana6/`.
