# Microejercicios · HTTP y JSON

| Caso | ¿Sale del proceso? | ¿Usa HTTP? | Ruta |
| --- | --- | --- | --- |
| A · llamada a `infer_measurements` | No | No | No hay ruta; es una función local |
| B · `POST /runPumpModel` | Sí | Sí | Acción |
| C · `POST /v1/predictions` | Sí | Sí | Recurso: colección de predicciones |

En `http://127.0.0.1:8000/v1/predictions/pred-42?include=explanation&limit=1`, el scheme es `http`, el host es `127.0.0.1`, el puerto es `8000`, el path es `/v1/predictions/pred-42` y los parámetros de query son `include=explanation` y `limit=1`. El ID va en el path, el límite de una colección en la query y las mediciones estructuradas en el body JSON.

```json
{"machine_id":"pump-017","ready":true,"comment":null,"axes":[1,2]}
```

Validé el bloque con `json.loads()`: obtuve `True`, `None` y la lista `[1, 2]`.

| Caso | Código | Razón |
| --- | --- | --- |
| Predicción devuelta | `200` | La petición se procesó correctamente. |
| Texto JSON truncado | `400` | El servidor no puede interpretar el cuerpo. |
| `vibration_mm_s` con valor `"alta"` | `422` | El JSON se puede leer, pero la medida incumple el tipo numérico. |
| Modelo temporalmente ausente | `503` | El servicio no puede procesar una petición válida en ese momento. |

Se crea con `POST /v1/predictions`, enviando las mediciones en el body JSON. Se consultaría con `GET /v1/predictions/pred-42`, con el identificador en el path. En ese diseño POST no es seguro ni idempotente por defecto: repetirlo podría crear dos resultados. GET es seguro e idempotente: repetir la consulta no debería cambiar el estado. La ruta de consulta es un ejercicio de diseño; los servidores docentes usados en el laboratorio exponen salud y predicción.
