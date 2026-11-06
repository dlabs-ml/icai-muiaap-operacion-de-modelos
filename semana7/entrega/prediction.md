# Ficha del recurso Prediction · API docente de bombas

`->` Pido una predicción de mantenimiento a partir de cuatro mediciones, con el identificador de la bomba separado de las medidas.

`>` Uso `POST /v1/predictions` con `Content-Type: application/json` y `Accept: application/json`. El identificador va en `machine_id`; las medidas van en el objeto `measurements`.

```json
{
  "machine_id": "pump-017",
  "measurements": {
    "temperature_c": 91.2,
    "vibration_mm_s": 8.4,
    "pressure_bar": 4.7,
    "runtime_hours": 12840
  }
}
```

`>>` La respuesta de éxito contiene `machine_id`, `prediction.label`, `prediction.risk_score`, `model_version` y `request_id`. El ID también aparece en `X-Request-Id`. En la [captura de curl](evidencias/pump-maintenance-api.txt) el resultado `maintenance_required` tiene score 0,85 y HTTP 200: la clase predicha no indica un fallo del servicio.

| HTTP | Qué significa | Qué hago |
| --- | --- | --- |
| 200 | El servicio devolvió la predicción. | Leo el JSON y compruebo que sea un objeto. |
| 400 | El cuerpo no se puede interpretar como JSON. | Corrijo cómo se construye o serializa la petición. |
| 422 | El JSON se entiende pero no cumple el contrato. | Corrijo la medida rechazada; en el ejemplo, `measurements.vibration_mm_s`. |
| 404 | La ruta solicitada no existe. | Reviso la base URL y el path; no hay consulta de predicciones en este servidor. |
| 503 | El modelo o el servicio no está disponible. | Compruebo el servicio y decido si envío una nueva petición. |

`~>` Un timeout no me dice si el servidor recibió la petición. Repetir a ciegas un POST puede ejecutar el trabajo dos veces. Si necesitara deduplicar, tendría que acordar un identificador de idempotencia con el servidor.

`=>` Registré salud, éxito e input rechazado con status, headers, cuerpo e identificador. Los cinco tests del starter fallaban por el hueco intencional y pasan con el cliente.
