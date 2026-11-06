# Módulo — Streamlit avanzado para consumo de modelos

Este módulo recibe una app básica de S5 y la refactoriza para que el modelo se
pueda consumir de forma más robusta dentro del modelo de ejecución de Streamlit.

## Arquitectura de continuidad

```text
formulario de S5
      ↓
st.session_state ← PredictionController → InferenceGateway → bundle de S4
      ↓                         ↓
   UiState                 TelemetrySnapshot
      ↓
presentación Streamlit
```

El formulario y los nombres de las features no se vuelven a diseñar. El
trabajo nuevo es controlar el rerun y hacer explícita la experiencia de una
petición.

## Secuencia

| Sesión | Foco | Resultado |
| --- | --- | --- |
| 1 | Reruns, sesión, caché y máquina de estados | La pareja entrega el mapa de transición de la app S5 y decide qué conservar. |
| 2 | Refactorización avanzada | La pareja entrega la app S5 evolucionada con estado, errores, latencia y telemetría. |

## Material

| Recurso | Uso |
| --- | --- |
| [Sesión 1](sessions/01-ux-estados-confianza/README.md) | Conceptos, inspección de S5 y demo de transiciones. |
| [Sesión 2](sessions/02-interfaz-robusta/README.md) | Taller de implementación sobre el snapshot de S5. |
| [Práctica 01](exercises/01-ui-contract/problem/README.md) | Diseñar el estado y los eventos de la app existente. |
| [Práctica 02](exercises/02-robust-streamlit/README.md) | Completar el refactor avanzado y sus pruebas. |
| [Solución docente](solutions/02-robust-streamlit/) | Referencia del debrief. |

## Decisiones avanzadas que se evalúan

- `st.session_state` conserva solo estado de sesión, no payloads completos ni
  secretos;
- `st.cache_resource` evita cargar el bundle en cada rerun;
- `PredictionController` permite probar la máquina de estados sin importar
  Streamlit;
- `st.empty`, `st.status` o un equivalente representan el estado de carga;
- el resultado válido puede marcarse como lento sin convertirse en error;
- los errores técnicos se traducen a mensajes y acciones de recuperación;
- la telemetría registra agregados, códigos, latencias y versiones.

S7 podrá sustituir `InferenceGateway` por un cliente HTTP sin rehacer la
política de estados ni la pantalla básica.
