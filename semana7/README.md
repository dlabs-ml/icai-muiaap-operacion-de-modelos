# Semana 7 — HTTP, REST, JSON y clientes de API

[Ver mi entrega, comprobaciones y evidencias](REPORT.md).

La semana introduce la frontera HTTP sin adelantar la construcción de un
backend. El alumnado observa contratos, consume endpoints y conecta el proyecto
Wine Quality iniciado en la semana 1 con un servicio remoto preparado.

## Dos clases, dos contextos

- **Clase 1 — fundamentos HTTP:** métodos, rutas, JSON, códigos de estado y
  clientes con curl, Postman y Python sobre el caso autocontenido de bombas.
- **Clase 2 — continuidad del proyecto:** la app Wine Quality de la semana 6
  sustituye su gateway local por `HttpInferenceGateway`. La API se entrega como
  caja negra y la interfaz, el controlador y la presentación no cambian.

En **S8** se implementará el servidor con FastAPI. En S7 solo se diseña y
consume su contrato público.

## Acceso al material

[Abrir el módulo 07-http-rest-clients](modules/07-http-rest-clients/README.md)

**Requisitos:** Python 3.12 y `uv`. En la raíz, `uv sync` puede crear un
`uv.lock` local no versionado. Solo los locks de los subproyectos starter y
solución forman parte del material reproducible; allí se usa
`uv sync --locked --extra app`.
