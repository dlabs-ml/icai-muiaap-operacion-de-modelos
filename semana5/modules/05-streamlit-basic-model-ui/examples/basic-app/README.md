# Mapa de la app Wine Quality de clase 2

Este esquema pertenece al proyecto incremental Wine Quality. La
[Práctica 5.1](../../exercises/01-churn-streamlit/README.md) utiliza Churn para
aprender el patrón, pero no aporta datos ni archivos a esta aplicación.

La solución de S5 conserva una interfaz fina:

```text
11 FIELD_SPECS
      ↓
st.form → collect_values → InferenceGateway.predict → render_prediction
                              ↓
                      bundle real de S4
```

La capa visual no carga `joblib`, no reconstruye el vector de variables y no
duplica el preprocesado. La ubicación del bundle se configura mediante
`MODEL_UI_BUNDLE`.

En S6 se conservarán el formulario y el contrato, y se añadirán estado de
sesión, caché, una máquina de estados y telemetría.
