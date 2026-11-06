# Semana 7 — Requests y AEMET

Consulta de la climatología diaria de Madrid, Ciudad Universitaria, del 1 al 30 de octubre de 2019.

[Enunciado (PDF)](enunciado_aemet.pdf) · [Informe de la práctica](REPORT.md) · [Código](entrega/aemet/climatologia.py) · [Datos del primer día](entrega/evidencias/datos_primerdia_octubre_2019.json)

Con Python 3.12 o superior y `uv`, desde la raíz del repositorio:

```bash
cd semana7
uv sync --locked
uv run --locked python -m unittest discover -s entrega/aemet -v
```

Para hacer la consulta real, configura `AEMET_API_KEY` en el entorno y ejecuta:

```bash
uv run --locked python entrega/aemet/climatologia.py \
  --guardar-primer-dia /tmp/datos_primerdia_octubre_2019.json
```
