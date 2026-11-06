# Guion docente — Clase 2: construir una interfaz Streamlit operable

**Resultado:** cada pareja entrega la app de S5 evolucionada con estado,
caché, máquina de estados y una interfaz que comunica éxito, carga, lentitud y
error de forma útil.

## Antes de empezar

- Distribuir el snapshot de S5 y el starter de S6.
- Aclarar que `collect_values()` ya está resuelto: no es el objetivo del
  taller.
- Mantener cerrada la solución hasta el debrief.
- Ejecutar primero los tests unitarios sin abrir todavía la app.
- Tener visible el plano de interfaz elaborado en Clase 1 y el laboratorio
  visual como referencia, no como código que copiar.

## Secuencia de 120 minutos

| Minutos | Hito | Pista | Comprobación |
| ---: | --- | --- | --- |
| 0–10 | Arranque orientado a comportamiento | Ejecutan tests rojos y localizan qué TODO satisface cada archivo. | Mapa test → función → decisión de Clase 1. |
| 10–25 | Estado de sesión | “`setdefault` protege la sesión; limpiar no borra observabilidad.” | Inicialización idempotente y limpieza parcial. |
| 25–40 | Políticas y copy | “Confianza y latencia son mensajes de UX, no una métrica nueva del modelo.” | Umbrales y mensajes seguros pasan tests. |
| 40–58 | Vista sin Streamlit | “Primero convierte un payload en una vista; después la dibujas.” | `PredictionView` y errores accionables. |
| 58–78 | Controlador | “El callback observa `loading`; la telemetría nunca observa features.” | Secuencias `loading → success/error`. |
| 78–95 | Integración Streamlit | “Cachea el gateway, no la petición.” | Estado persistente, caché y formulario de S5 conectados. |
| 95–108 | Prueba visual por escenarios | “Los tests verdes no garantizan una interfaz comprensible.” | Inicio, éxito, error, retry y limpiar comprobados. |
| 108–115 | Revisión entre parejas | “Busca datos de entrada en la telemetría y detalle técnico fuera de lugar.” | Checklist visual y privacidad revisados. |
| 115–120 | Debrief | “¿Qué cambiaría en S7?” | El gateway queda reemplazable por HTTP. |

## Evidencias obligatorias

- diff o nota que identifique qué se conserva de S5;
- captura de carga, éxito, error y reintento;
- prueba de que el resultado sobrevive a un rerun;
- prueba de que limpiar no borra telemetría;
- tests y lint verdes;
- explicación de qué se cachea y por qué.
- captura donde categoría, confianza y latencia tengan jerarquía visible y las
  versiones queden bajo trazabilidad;
- prueba de que la pantalla no muestra traceback, rutas internas ni valores de
  las features cuando falla una petición.
