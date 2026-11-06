# Práctica 5.2 — Del bundle S4 al frontal Wine

Duración: **120 minutos**, por parejas. En esta práctica se transfiere a Wine
el patrón aprendido con Churn: formulario, envío explícito, una llamada a la
inferencia y actualización visible. No se reutilizan datos ni código de Churn.

## Prerrequisito obligatorio

Cada pareja parte de su bundle de S4. La ruta indicada debe ser un directorio
que contenga `manifest.json` y `model.joblib` compatibles con el contrato Wine
Quality. Una ejecución sin ese bundle no es una entrega válida.

El starter ya incluye el esquema completo de los once campos Wine en
`src/model_ui/ui_schema.py`. No hay que copiar ningún archivo de la práctica
5.1 ni reconstruir el entrenamiento, el preprocesado o la carga con `joblib`
desde `app.py`.

## Resultado esperado

Al terminar, `problem/starter/` debe incluir:

- un único `st.form` con once `number_input` generados desde `FIELD_SPECS`;
- cero llamadas a `gateway.predict(values)` al editar y una al enviar;
- una salida con `quality_band`, `confidence`, `model_version` y
  `preprocessing_version`;
- un error seguro y accionable cuando el bundle no está configurado o no se
  puede cargar;
- tests automáticos verdes y evidencia visual de los cuatro casos de QA.

Los dobles del gateway pertenecen exclusivamente a `tests/`. El código de
ejecución siempre carga el bundle indicado en `MODEL_UI_BUNDLE`.

## Cronograma de clase (120 min)

| Minutos | Trabajo |
|---:|---|
| 0–15 | Localizar y validar el bundle de S4. |
| 15–35 | Construir los once widgets desde `FIELD_SPECS`. |
| 35–55 | Completar el formulario y verificar la semántica del submit. |
| 55–75 | Revisar la conexión con `InferenceGateway` y el invariante 0/1. |
| 75–90 | Implementar `render_prediction()` con las cuatro salidas. |
| 90–105 | Comprobar la frontera segura ante bundle ausente o inválido. |
| 105–115 | Ejecutar tests y completar el QA visual. |
| 115–120 | Documentar la ejecución y los límites para S6. |

## Preparación y ejecución

Desde la raíz del repositorio, en PowerShell:

```powershell
cd semana5/modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/problem/starter
uv sync
$env:MODEL_UI_BUNDLE = 'RUTA_AL_BUNDLE_DE_S4'
uv run python -m pytest -q
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

La ruta debe apuntar al directorio del bundle, no directamente a
`model.joblib`. Antes de resolver el ejercicio, la suite falla solo en
`collect_values()` y `render_prediction()`.

## Orden de implementación

1. Abre `ui_schema.py` y confirma que contiene once especificaciones completas.
2. Implementa `collect_values()` sin llamar al gateway.
3. Comprueba que editar no infiere y que el submit llama una sola vez.
4. Implementa `render_prediction()` con los cuatro campos del payload.
5. Ejecuta los tests y completa la matriz de QA.

No añadas `session_state`, caché, FSM ni telemetría: son objetivos de S6.

## QA manual: cuatro casos

| Caso | Acción | Resultado esperado |
|---|---|---|
| Arranque con bundle | Configurar un bundle S4 válido y abrir la app. | Se muestran los once campos sin ejecutar inferencia. |
| Edición sin envío | Cambiar uno o varios valores. | El formulario cambia y hay cero llamadas al gateway. |
| Submit válido | Pulsar `Ejecutar inferencia`. | Hay una llamada y aparecen las cuatro salidas. |
| Bundle ausente | Quitar la variable o indicar un bundle inválido y relanzar. | Mensaje accionable con `MODEL_UI_BUNDLE`, sin ruta interna ni traceback. |

## Entrega y rúbrica (10 puntos)

| Criterio | Puntos |
|---|---:|
| Formulario Wine completo, generado desde las once especificaciones | 2 |
| Semántica correcta de submit: cero/una llamada | 2 |
| Integración con el bundle real de S4 sin duplicar inferencia | 2 |
| Presentación de los cuatro campos del payload | 2 |
| Error seguro, tests verdes y evidencia de los cuatro casos | 2 |

Entregad el starter completado, la salida de los tests y cuatro capturas o un
registro equivalente de la matriz de QA.
