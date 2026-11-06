# Informe de la práctica 7 — Clientes HTTP y consumo remoto

## Leyenda utilizada

- `->` Objetivo o problema que quiero resolver.
- `~>` Decisión o cambio realizado y su justificación.
- `>` Acción técnica ejecutada.
- `>>` Evidencia verificable: archivo, salida o comprobación.
- `=>` Resultado obtenido y estado de verificación.

## Objetivo y preparación

`->` Mi objetivo ha sido practicar el contrato HTTP con la API docente de bombas y conectar la interfaz Wine Quality de S6 al servicio de predicciones.

## Relación entre requisitos y entrega

| Práctica | Entrega | Comprobación |
| --- | --- | --- |
| 7.1 · API de bombas | [Microejercicios](entrega/microejercicios.md), [ficha de Prediction](entrega/prediction.md) y [cliente](modules/07-http-rest-clients/exercises/02-api-client-lab/problem/starter/client.py) | [curl](entrega/evidencias/pump-maintenance-api.txt), [cliente real](entrega/evidencias/7.1-cliente-real.txt) y [tests](entrega/evidencias/7.1-pruebas.txt) |
| 7.2 · Wine Quality por HTTP | [Starter](modules/07-http-rest-clients/exercises/03-wine-http-gateway/problem/starter) | [curl](entrega/evidencias/wine-quality-api.txt), [Streamlit](entrega/evidencias/7.2-streamlit.txt) y [34 tests](entrega/evidencias/7.2-pruebas.txt) |
| APIs públicas | [Colección Postman](entrega/postman/APIs-publicas.postman_collection.json) | [Respuestas resumidas](entrega/evidencias/apis-publicas.txt) y [Newman](entrega/evidencias/postman-newman.txt): 8 peticiones, 24 comprobaciones |
| Requests + AEMET | [Cliente](entrega/aemet/climatologia.py) y [pruebas](entrega/aemet/test_climatologia.py) | [Descarga real de 30 observaciones](entrega/evidencias/aemet-ejecucion-real.txt), [JSON del primer día](entrega/evidencias/datos_primerdia_octubre_2019.json) y [pruebas con respuestas simuladas](entrega/evidencias/aemet-pruebas.txt) |

## Decisiones de implementación

`~>` Uso `json=` para serializar el cuerpo, `Accept` para indicar que espero JSON y un timeout para limitar la espera. Valido status y estructura por separado. Un `POST` que supera el timeout puede haber llegado al servidor, así que dejo el reintento como decisión de la persona que usa la app y rechazo redirecciones que reenviarían las medidas.

`~>` En Wine mantengo la [interfaz de S6](../semana6/zip_semana6/REPORT.md). El gateway distingue errores de entrada, indisponibilidad, timeout, fallo de conexión y respuestas inválidas. Conserva el ID remoto si la API lo devuelve en el cuerpo de éxito o en la cabecera; el identificador que ve el usuario lo genera el controlador local.

## Ejecución reproducible

`>` Desde la [raíz del módulo](modules/07-http-rest-clients):

```bash
uv sync --locked
uv run --locked python -m unittest discover -s exercises/02-api-client-lab/problem/starter -p 'test_*.py' -v
uv run --locked python -m pytest -q
uv run --locked python examples/wine-quality-api/server.py
```

`>` En otra terminal, desde `problem/starter` de 7.2:

```bash
uv sync --locked --extra app
uv run --locked --extra app python -m pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
MODEL_API_URL=http://127.0.0.1:8000 uv run --locked --extra app streamlit run app.py
```

`>` Para las APIs públicas puedo importar la colección en Postman. Desde la carpeta de la semana la ejecuto con `npx --yes newman@6 run entrega/postman/APIs-publicas.postman_collection.json`. El POST simulado en JSONPlaceholder devolvió un ID que no apareció en el GET posterior, como indica su [guía](https://jsonplaceholder.typicode.com/guide/).

`>` Para AEMET uso el entorno de `uv` del módulo, que instala `requests` desde el lockfile. Configuro `AEMET_API_KEY` en mi entorno y ejecuto desde la raíz del módulo `uv run --locked python ../../entrega/aemet/climatologia.py`. Envío la clave como parámetro de consulta `api_key` al pedir el inventario y la climatología diaria. Busco Madrid, Ciudad Universitaria en el inventario para obtener el indicativo `3194U`. [Ficha de la estación](https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?l=3194U) · [AEMET OpenData](https://opendata.aemet.es/dist/).

`~>` El PDF de `AEMET.zip` fija el cierre en el 30 de octubre de 2019 a las 23:59:59 UTC. El script de ejemplo del ZIP usa el día 31. Seguí el intervalo explícito del PDF.

## Comprobaciones y resultados

`>>` Las APIs docentes devolvieron `200` para salud y predicción válida y `422` para la entrada inválida. En Streamlit probé [modo demo](entrega/evidencias/7.2-demo.jpg), [HTTP 503](entrega/evidencias/7.2-http-503.jpg) y [reintento con el servicio restaurado](entrega/evidencias/7.2-http-reintento.jpg). El modelo remoto de aula se identifica como `wine-quality-demo-v1`.

`=>` He verificado los clientes docentes, los recorridos de la UI y las ocho peticiones de la colección de APIs públicas. En AEMET confirmé el indicativo `3194U` y recibí una observación por día del 1 al 30 de octubre de 2019, sin fechas repetidas ni registros de otra estación. El registro completo del 1 de octubre coincide campo por campo con el JSON del ZIP.
