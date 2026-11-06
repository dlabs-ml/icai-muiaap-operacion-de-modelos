# Informe de la práctica 7 — Requests y AEMET

## Leyenda utilizada

- `->` Objetivo o problema que quiero resolver.
- `~>` Decisión o cambio realizado y su justificación.
- `>` Acción técnica ejecutada.
- `>>` Evidencia verificable: archivo, salida o comprobación.
- `=>` Resultado obtenido y estado de verificación.

## Consulta a AEMET

`->` Quería descargar con `requests` la climatología diaria de Madrid, Ciudad Universitaria, para el intervalo del enunciado.

`>` Consulté el inventario de estaciones por nombre y obtuve el indicativo `3194U`. Con ese identificador pedí la climatología diaria y descargué el JSON desde el enlace temporal que devuelve AEMET.

`~>` Leí la clave de `AEMET_API_KEY` y la envié como parámetro `api_key` al solicitar el inventario y la climatología. Los enlaces temporales se descargan sin la clave.

`~>` Seguí el intervalo del [enunciado](enunciado_aemet.pdf), del 1 al 30 de octubre de 2019, con cierre a las 23:59:59 UTC. Para exportar la observación del primer día, la seleccioné por fecha para que el resultado no dependiera del orden de la respuesta.

## Ejecución y resultados

`>` Usé un entorno virtual con `requests`. El [README](README.md) recoge los comandos para instalar las dependencias, ejecutar las pruebas y repetir la consulta.

`>>` [Cliente](entrega/aemet/climatologia.py) · [Pruebas con respuestas simuladas](entrega/aemet/test_climatologia.py) · [Salida de las pruebas](entrega/evidencias/aemet-pruebas.txt) · [Ejecución real](entrega/evidencias/aemet-ejecucion-real.txt) · [JSON del 1 de octubre](entrega/evidencias/datos_primerdia_octubre_2019.json).

`=>` Recibí 30 observaciones de la estación `3194U`, una por cada día del intervalo. Comprobé que el registro del 1 de octubre coincidía campo por campo con el JSON de la solución facilitada.
