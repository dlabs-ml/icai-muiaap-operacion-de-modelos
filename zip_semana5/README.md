# Semana 5 — Interfaces rápidas para una función de inferencia

[Ver mi entrega, comprobaciones y evidencias](REPORT.md).

La semana 5 tiene **dos prácticas activas** conectadas por un mismo patrón,
pero no por sus datos ni por su código:

```text
formulario → submit → una inferencia → resultado o error comprensible
```

- En la **clase 1** se aprende el modelo mental de Streamlit con un caso
  sintético de Churn y se construye una miniapp funcional.
- En la **clase 2** se aplica ese patrón al proyecto Wine Quality usando
  obligatoriamente el bundle real generado en S4.

En S5 no se implementan estado de sesión, caché, máquinas de estados ni
telemetría. Esas extensiones se reservan para S6.

## Continuidad

| Semana | Se conserva | Se añade en S5 |
| --- | --- | --- |
| [S1](../semana1/README.md) | Riesgos y diferencia entre prototipo y servicio | Un resultado y un error comprensibles para una persona usuaria. |
| [S2](../semana2/README.md) | Proyecto reproducible, dependencias y tests | Dos miniapps ejecutables y verificables. |
| [S3](../semana3/README.md) | Contrato Wine de once variables y salida validada | Los nombres del contrato se convierten en claves del formulario. |
| [S4](../semana4/README.md) | Bundle con manifiesto, estimador y versiones | Un gateway conecta el bundle real con Streamlit. |
| S5 | Formulario, submit y frontera de inferencia | Base funcional que se reforzará en S6. |

## Clase 1 — 60 min de teoría + 60 min de práctica Churn

Durante los primeros 60 minutos se presenta el caso sintético, el contrato
`predict()`, el rerun de Streamlit, los widgets, `st.form`,
`st.form_submit_button` y la separación entre interfaz e inferencia.

Durante los 60 minutos siguientes cada pareja completa la Práctica 5.1. La
función `predict()` ya está implementada: el trabajo consiste en construir el
formulario, conectar el submit con exactamente una llamada y presentar
`label`, `risk_score`, `explanation` o un error seguro.

- [Sesión de clase 1](modules/05-streamlit-basic-model-ui/sessions/01-streamlit-basics/README.md)
- [Práctica 5.1 — miniapp Churn](modules/05-streamlit-basic-model-ui/exercises/01-churn-streamlit/README.md)

## Clase 2 — 120 min de práctica Wine

Cada pareja continúa su proyecto con el bundle real de S4. El starter ya
incluye los once `FIELD_SPECS` de Wine; no se copia ningún archivo desde la
Práctica 5.1. Se conservan el formulario, el submit, la semántica de cero/una
llamada y la presentación segura; cambian el contrato, el gateway y la salida.

- [Sesión de clase 2](modules/05-streamlit-basic-model-ui/sessions/02-first-model-ui/README.md)
- [Práctica 5.2 — frontal Wine sobre el bundle S4](modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/README.md)

## Las dos entregas

### Práctica 5.1 — miniapp Churn

- `app.py` completado;
- trece tests verdes;
- formulario único con cuatro entradas;
- cero llamadas al editar y una por submit;
- resultado y error seguro;
- checklist manual de cuatro casos.

### Práctica 5.2 — frontal Wine

- starter completado con once campos Wine;
- bundle real de S4 configurado mediante `MODEL_UI_BUNDLE`;
- llamada exclusiva a `gateway.predict(values)`;
- `quality_band`, `confidence`, `model_version` y
  `preprocessing_version` visibles;
- tests verdes y evidencia de los cuatro casos de QA.

Las referencias docentes están separadas de los puntos de partida:

- [Solución 5.1](modules/05-streamlit-basic-model-ui/solutions/01-churn-streamlit/README.md)
- [Solución 5.2](modules/05-streamlit-basic-model-ui/solutions/02-first-streamlit/README.md)

## Ejecución

Práctica 5.1, desde la raíz del repositorio:

```powershell
cd zip_semana5/modules/05-streamlit-basic-model-ui/exercises/01-churn-streamlit/problem/starter
uv sync
uv run python -m pytest -q
uv run streamlit run app.py
```

Práctica 5.2, con el bundle de cada pareja:

```powershell
cd zip_semana5/modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/problem/starter
uv sync
$env:MODEL_UI_BUNDLE = 'RUTA_AL_BUNDLE_DE_S4'
uv run python -m pytest -q
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

Una ejecución de la Práctica 5.2 sin un bundle S4 válido no constituye una
entrega.
