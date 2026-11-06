# Clase 1 — Streamlit con una miniapp Churn

**Duración:** 120 minutos · **Formato:** 60 min de teoría guiada + 60 min de
Práctica 5.1

## Resultado de aprendizaje

Al terminar, cada pareja puede explicar y construir este recorrido:

```text
cuatro widgets → submit → predict(**values) → resultado o error
```

También puede explicar el rerun de Streamlit, justificar `st.form`, comprobar
el invariante cero/una llamada y separar el código de interfaz de una función
de inferencia ya probada.

## Caso y alcance

La clase usa un caso sintético de Churn, autocontenido y sin artefacto de
modelo. La regla es visible y determinista; su score no es una probabilidad
calibrada. Tanto la explicación como la práctica se realizan únicamente con
Streamlit.

No se usa el bundle Wine durante esta clase. Tampoco se implementan
`st.session_state`, caché, FSM ni telemetría: esas decisiones pertenecen a S6.

## Contenidos de los primeros 60 minutos

- propósito del caso Churn y contrato de `predict()`;
- cuatro entradas y tres salidas visibles;
- ejecución de arriba abajo y rerun de Streamlit;
- correspondencia entre widgets, tipos y argumentos;
- `st.form` y `st.form_submit_button`;
- cero llamadas al editar y una por envío;
- separación UI/inferencia;
- presentación del resultado y del error seguro.

## Práctica guiada de los últimos 60 minutos

La pareja recibe `model.py` completo y tres huecos en `app.py`:

1. construir el formulario;
2. conectar submit y llamada;
3. presentar la predicción o un error comprensible.

No se crea un tercer entregable ni se prepara un archivo para Wine.

## Materiales y orden

1. [Guion docente 60+60](../../guides/class-1-practices.md).
2. [Notebook guiado](notebooks/01-streamlit-basics-guiada.ipynb).
3. [Solución Churn para la explicación](../../solutions/01-churn-streamlit/README.md).
4. [Práctica 5.1 — starter Churn](../../exercises/01-churn-streamlit/README.md).

## Evidencia observable

- los perfiles `2, 95, 4, False` y `36, 35, 0, True` producen decisiones
  distintas y explicables;
- cambiar valores dentro del formulario no llama a `predict()`;
- cada submit válido produce exactamente una llamada;
- la pantalla muestra `label`, `risk_score` y `explanation`;
- un `ValueError` se transforma en un mensaje estable sin detalles internos;
- los trece tests de la solución están verdes.

## Puente a la clase 2

La clase 2 conserva formulario, submit, cero/una llamada y presentación segura.
Cambia a once variables Wine, `InferenceGateway`, `PredictionPayload` y el
bundle real de S4. No se copian datos ni código de Churn.
