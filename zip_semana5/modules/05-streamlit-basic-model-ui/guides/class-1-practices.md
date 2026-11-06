# Guion docente — Clase 1: teoría y práctica Churn con Streamlit

**Duración:** 120 minutos · **Estructura:** 60 min de teoría guiada + 60 min de
Práctica 5.1

**Resultado:** cada pareja comprende el rerun, construye una miniapp Streamlit
funcional y demuestra que la inferencia ocurre cero veces al editar y una vez
al enviar.

## Preparación

- Abrir el [notebook guiado](../sessions/01-streamlit-basics/notebooks/01-streamlit-basics-guiada.ipynb).
- Preparar la [solución Churn](../solutions/01-churn-streamlit/README.md) para
  recorrerla durante la explicación.
- Compartir al comenzar el tramo práctico el
  [starter 5.1](../exercises/01-churn-streamlit/problem/starter/README.md).
- Tener visibles los trece tests: seis fijan el contrato de `predict()` y siete
  especifican la interfaz.
- No introducir estado de sesión, caché, FSM ni telemetría; pertenecen a S6.

## Mensaje conductor

> Una interfaz fina recoge valores, llama a una función ya probada y presenta
> su salida. La regla de inferencia no se copia dentro de la pantalla.

El caso Churn es sintético y determinista. Su `risk_score` es un score docente,
no una probabilidad calibrada ni una predicción sobre clientes reales.

## Secuencia de 120 minutos

| Minutos | Desarrollo | Evidencia |
| ---: | --- | --- |
| 0–10 | Propósito y caso Churn | La clase distingue el caso sintético del proyecto Wine. |
| 10–20 | Contrato `predict()` y salida | Se identifican cuatro entradas y `label`, `risk_score`, `explanation`. |
| 20–35 | Rerun, widgets y formulario | Se explica por qué `st.form` agrupa cambios y el submit dispara la acción. |
| 35–50 | Demostración guiada Streamlit | Se sigue el recorrido widget → argumento → llamada → pantalla. |
| 50–60 | Preparación del starter | Se localizan los tres huecos y se confirma el estado inicial de los tests. |
| 60–70 | Contrato y predicciones del alumno | Cada pareja anticipa dos perfiles antes de ejecutar. |
| 70–85 | Formulario | Se implementan cuatro widgets dentro de un único formulario. |
| 85–95 | Submit y llamada | Se comprueban cero llamadas al editar y una por envío. |
| 95–105 | Resultado y error | Se muestran los tres campos y un mensaje de error comprensible, sin detalle crudo. |
| 105–115 | Tests | Se corrigen únicamente los contratos incumplidos hasta obtener trece tests verdes. |
| 115–120 | QA y puente Churn → Wine | Se revisan cuatro casos y se verbaliza qué se conserva y qué cambia. |

Los breves ejercicios de predicción de las secciones siguientes son pausas
dentro de esta secuencia; no constituyen una tercera práctica ni una entrega
adicional.

## Pausa 1 — Predecir el rerun

Antes de ejecutar, la pareja dibuja el recorrido al:

1. abrir la aplicación;
2. modificar un widget dentro del formulario;
3. pulsar **Calcular riesgo**.

La respuesta esperada es que Streamlit recorre el script de arriba abajo. El
formulario agrupa las ediciones y `submitted` decide si se llama a la función:

```text
rerun → dibujar formulario → ¿submitted?
                              ├─ no: 0 llamadas y una instrucción
                              └─ sí: 1 llamada → resultado o error
```

## Pausa 2 — Traducir contrato a widgets

La pareja propone label, unidad, componente y valor inicial para:

| Argumento | Tipo | Componente de referencia |
| --- | --- | --- |
| `tenure_months` | entero | `st.slider` |
| `monthly_spend_eur` | real | `st.number_input` |
| `support_calls` | entero | `st.slider` |
| `has_annual_contract` | booleano | `st.checkbox` |

Preguntas de debrief:

- ¿Qué información pertenece al label, pero no al argumento de `predict()`?
- ¿Por qué los límites del widget no sustituyen la validación de la función?
- ¿Qué ocurriría si el checkbox enviase la cadena `"sí"` en lugar de `True`?

## Pausa 3 — Separar interfaz e inferencia

Localizar en la solución:

1. dónde vive la regla sintética;
2. dónde se llama a `predictor(**values)`;
3. dónde se traduce un `ValueError` a un mensaje estable.

La evidencia que interesa es una explicación de treinta segundos:

> `model.py` valida y calcula; `app.py` recoge, llama y presenta.

Duplicar la regla en la interfaz permitiría que ambas versiones divergieran y
obligaría a repetir las pruebas de inferencia.

## Perfiles para anticipar

| Perfil | Valores | Resultado esperado |
| --- | --- | --- |
| Riesgo alto | `2, 95, 4, False` | Score alto y baja probable. |
| Riesgo bajo | `36, 35, 0, True` | Score bajo y permanencia probable. |

Pedir que expliquen los factores antes de ejecutar y recordar que el score está
acotado por la regla docente.

## Comprobación docente

PowerShell, desde la raíz del repositorio:

```powershell
Set-Location .\semana5\modules\05-streamlit-basic-model-ui\solutions\01-churn-streamlit
uv sync
uv run python -m pytest -q
uv run ruff check app.py src tests
uv run ruff format --check app.py src tests
uv run streamlit run app.py
```

La solución debe producir trece tests verdes. Para el starter, el estado
inicial esperado es `5 failed, 8 passed`, todos ligados a los tres huecos del
alumno.

## QA manual

| Caso | Acción | Evidencia |
| --- | --- | --- |
| Arranque | Abrir la app. | Formulario con cuatro widgets e instrucción inicial. |
| Edición sin envío | Cambiar varios valores. | No aparece una predicción. |
| Submit válido | Pulsar **Calcular riesgo**. | Una llamada y los tres campos de salida. |
| Resultado actualizado | Cambiar el perfil y volver a enviar. | La salida corresponde al nuevo perfil. |

## Puente a la clase 2

| Se conserva | Cambia |
| --- | --- |
| un formulario y un submit | cuatro campos Churn → once campos Wine |
| cero llamadas al editar y una al enviar | `predict()` → `InferenceGateway.predict()` |
| separación entre UI e inferencia | regla sintética → bundle real de S4 |
| resultado o error comprensible | salida Churn → `PredictionPayload` |

No se entrega ni se copia ningún archivo Churn a la Práctica 5.2. El puente es
exclusivamente conceptual.

## Exit ticket

Cada pareja completa una frase:

1. «El rerun de Streamlit significa que…»
2. «`st.form` evita que la inferencia…»
3. «De Churn a Wine conservamos…, pero cambiamos…»

Estas respuestas forman parte del cierre de 5.1, no de una entrega separada.
