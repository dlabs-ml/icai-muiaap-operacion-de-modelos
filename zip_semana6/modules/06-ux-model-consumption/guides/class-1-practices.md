# Guion docente — Clase 1: de la app básica a una experiencia operable

**Resultado:** cada pareja inspecciona su app de S5 y sale con un diseño
implementable de sesión, caché, transiciones y presentación. El formulario se
conserva; la experiencia de consumo del modelo mejora.

## Preparación

- Pedir que cada pareja traiga la app de S5 funcionando.
- Tener disponible la solución de S5 como snapshot común si alguna pareja no
  terminó su app.
- Abrir el [notebook guiado](../sessions/01-ux-estados-confianza/notebooks/01-ux-modelo-guiada.ipynb).
- Compartir el [notebook de la práctica](../exercises/01-ui-contract/problem/01-estado-streamlit-alumno.ipynb).
- Recordar que S4 sigue siendo la frontera de inferencia y que S6 no copia su
  preprocesado.
- Tener abierta la app de S5 para comparar una pantalla que funciona con una
  pantalla que además comunica qué está ocurriendo.

## Secuencia de 120 minutos

| Minutos | Acción docente | Actividad | Evidencia |
| ---: | --- | --- | --- |
| 0–12 | Ejecutar una app de S5 | Localizan formulario, gateway, resultado y el límite de una variable local. | Mapa de S5. |
| 12–25 | Provocar reruns | Predicen qué se pierde, qué se redibuja y qué no debe recalcularse. | Tabla variable → ciclo de vida. |
| 25–38 | Introducir `session_state` | Deciden las claves mínimas y qué se borra al limpiar. | `last_state`, `last_values`, `telemetry`. |
| 38–48 | Introducir `cache_resource` | Deciden qué recurso se cachea y anotan el requisito de concurrencia. | Regla de caché. |
| 48–63 | Diseñar jerarquía visual | Asignan un componente Streamlit a formulario, operación, resultado y trazabilidad. | Plano de pantalla. |
| 63–78 | Máquina de estados | Definen eventos, zonas que cambian y acciones permitidas. | Tabla de transición. |
| 78–95 | Ejecutar demo avanzada | Comparan `loading`, éxito, error, limpieza y reintento. | Predicción frente a resultado. |
| 95–108 | Confianza, latencia y copy | Redactan mensajes que informan sin prometer certeza. | Cuatro mensajes revisados. |
| 108–120 | Preparar taller | Relacionan el plano y los estados con funciones y tests. | Orden de implementación. |

## Invariantes

- El formulario de S5 no se duplica ni se rediseña sin motivo.
- El bundle se carga como recurso, no en cada interacción.
- Limpiar la pantalla no borra la telemetría de sesión.
- La confianza no se presenta como certeza.
- Un fallo visible tiene una recuperación y un `request_id`.
- El resultado muestra categoría, confianza y latencia; el detalle técnico se
  aplaza a un `st.expander`.
- Una barra de progreso comunica avance de una tarea, no confianza del modelo.
