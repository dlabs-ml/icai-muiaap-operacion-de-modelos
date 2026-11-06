# Módulo — Streamlit básico: de Churn a Wine

El módulo contiene exactamente dos prácticas. Comparten un patrón de
interacción, no un conjunto de datos ni un archivo que deba copiarse:

```text
Clase 1
60 min teoría guiada Churn
60 min Práctica 5.1 Churn
             ↓
puente conceptual: formulario → submit → una inferencia → resultado/error
             ↓
Clase 2
120 min Práctica 5.2 Wine con el bundle real de S4
```

## Responsabilidades

| Capa | Práctica 5.1 · Churn | Práctica 5.2 · Wine |
| --- | --- | --- |
| Entrada | Cuatro campos sintéticos | Once campos canónicos de S3/S4 |
| Interfaz | Un `st.form` y un submit | Un `st.form` generado desde `FIELD_SPECS` |
| Inferencia | `predict(**values)` ya proporcionado | `InferenceGateway.predict(values)` |
| Artefacto | No hay modelo entrenado | Bundle real de S4 obligatorio |
| Salida | Etiqueta, score y explicación | Categoría, confianza y dos versiones |
| Error | Mensaje estable sin detalle crudo | Mensaje accionable sin ruta ni traceback |

La interfaz no contiene la regla de Churn, no carga directamente el estimador
Wine y no reconstruye el preprocesado. El esquema Wine viene completo en el
starter de 5.2 y no procede de 5.1.

## Material de clase 1

- [Sesión 01 — teoría y práctica Churn](sessions/01-streamlit-basics/README.md)
- [Guion docente 60+60](guides/class-1-practices.md)
- [Práctica 5.1 — miniapp Churn](exercises/01-churn-streamlit/README.md)
- [Solución docente 5.1](solutions/01-churn-streamlit/README.md)

## Material de clase 2

- [Sesión 02 — taller Wine](sessions/02-first-model-ui/README.md)
- [Guion docente del taller](guides/class-2-workshop.md)
- [Práctica 5.2 — frontal Wine](exercises/02-first-streamlit/README.md)
- [Solución docente 5.2](solutions/02-first-streamlit/README.md)

## Límite deliberado

S5 se concentra en widgets, formulario, rerun, una llamada controlada y
presentación. Persistencia con `st.session_state`, caché, FSM, telemetría,
latencia y recuperación avanzada se estudian en S6.

## Resultado esperado

Al terminar la semana, una persona puede:

1. abrir la miniapp Churn, editar un perfil y obtener un resultado explicable;
2. abrir la app Wine con su bundle S4, enviar las once variables y ver la
   predicción con sus versiones;
3. distinguir con claridad qué patrón se transfiere y qué elementos pertenecen
   a cada caso.
