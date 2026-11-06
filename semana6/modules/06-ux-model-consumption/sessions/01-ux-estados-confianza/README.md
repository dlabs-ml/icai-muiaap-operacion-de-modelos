# Clase 1 — Streamlit avanzado: reruns, sesión y máquina de estados

**Duración:** 1 hora de teoría participativa + 1 hora de demo guiada

## Resultado de aprendizaje

La pareja puede inspeccionar la app de S5, explicar qué ocurre en un rerun y
definir qué estado debe persistir para servir una inferencia sin perder el
resultado ni cargar el modelo repetidamente.

## Punto de partida: la app de S5

Abrir la solución o la copia entregada de S5. Identificar:

1. dónde se dibuja el formulario;
2. cuándo se llama a `gateway.predict()`;
3. qué pasa si la app se vuelve a ejecutar;
4. dónde se carga el bundle;
5. qué información se pierde después de la ejecución.

La app de S5 es válida como primera interfaz. Sus limitaciones son
deliberadas: no conserva la última respuesta con `st.session_state`, no cachea
explícitamente el gateway y no comunica estados intermedios.

## Contenidos

- rerun como modelo de ejecución de Streamlit;
- diferencia entre variables locales y `st.session_state`;
- inicialización idempotente del estado;
- `st.cache_resource` para recursos compartidos, como el gateway o bundle;
- callbacks, formularios y momento del envío;
- placeholders y `st.status` para representar una operación en curso;
- máquina de estados `idle → loading → success/error`;
- confianza, latencia, errores y trazabilidad como parte de la UX del modelo.

## Secuencia

| Minutos | Concepto | Actividad | Evidencia |
| ---: | --- | --- | --- |
| 0–10 | Recuperar S5 | Ejecutan la app y localizan el formulario y el gateway. | Mapa de componentes. |
| 10–25 | Rerun | Predicen qué variables sobreviven al pulsar y al editar. | Lista de estado perdido. |
| 25–40 | `session_state` | Deciden qué claves conservar y cuáles no. | Contrato de sesión. |
| 40–55 | Caché de recursos | Comparan cargar el bundle una vez con cargarlo por rerun. | Decisión de `cache_resource`. |
| 55–70 | Máquina de estados | Diseñan eventos y transiciones. | Tabla `idle/loading/success/error`. |
| 70–90 | Demo guiada | Observan éxito, error, reintento y limpieza. | Predicción antes de cada evento. |
| 90–110 | Confianza y latencia | Separan resultado válido de respuesta lenta. | Copy y criterio técnico. |
| 110–120 | Puente al taller | Traducen el diseño a funciones y tests. | Orden de implementación. |

## Notebook

[Abrir demo guiada](notebooks/01-ux-modelo-guiada.ipynb)

La demo no vuelve a enseñar `number_input` ni el formulario. Usa un gateway
determinista para centrar la discusión en las transiciones y mostrar cómo S6
extiende S5.
