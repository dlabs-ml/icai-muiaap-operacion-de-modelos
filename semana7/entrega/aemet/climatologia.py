"""Práctica de AEMET: climatología diaria de Ciudad Universitaria."""

import json
import os
import re
from urllib.parse import urlparse

import requests

BASE = "https://opendata.aemet.es/opendata/api/valores/climatologicos"
ESTACION = "MADRID, CIUDAD UNIVERSITARIA"
INICIO = "2019-10-01T00:00:00UTC"
FIN = "2019-10-30T23:59:59UTC"


def descargar_datos(sesion, ruta, clave):
    # La primera respuesta contiene el enlace al JSON, no las observaciones.
    respuesta = sesion.get(
        f"{BASE}/{ruta}", params={"api_key": clave}, timeout=30, allow_redirects=False
    )
    respuesta.raise_for_status()
    sobre = respuesta.json()
    if not isinstance(sobre, dict) or sobre.get("estado") != 200:
        raise ValueError("AEMET no devolvió un enlace de descarga válido.")

    enlace = sobre.get("datos")
    url = urlparse(enlace) if isinstance(enlace, str) else None
    if not url or url.scheme != "https" or url.netloc != "opendata.aemet.es":
        raise ValueError("El enlace de descarga no pertenece a AEMET.")

    # No reenvío la clave a la URL temporal de descarga.
    descarga = sesion.get(enlace, timeout=30, allow_redirects=False)
    descarga.raise_for_status()
    filas = descarga.json()
    if not isinstance(filas, list) or any(not isinstance(fila, dict) for fila in filas):
        raise ValueError("La descarga no contiene una lista de registros.")
    return filas


def obtener_climatologia(sesion, clave):
    inventario = descargar_datos(sesion, "inventarioestaciones/todasestaciones/", clave)
    indicativos = [
        fila.get("indicativo")
        for fila in inventario
        if str(fila.get("nombre", "")).strip().upper() == ESTACION
    ]
    if len(indicativos) != 1 or not re.fullmatch(r"[A-Z0-9]+", str(indicativos[0])):
        raise ValueError("No pude identificar de forma única la estación solicitada.")

    indicativo = indicativos[0]
    ruta = f"diarios/datos/fechaini/{INICIO}/fechafin/{FIN}/estacion/{indicativo}/"
    return indicativo, descargar_datos(sesion, ruta, clave)


def main():
    clave = os.getenv("AEMET_API_KEY")
    if not clave:
        raise SystemExit("Configura AEMET_API_KEY en tu entorno antes de ejecutar.")
    try:
        with requests.Session() as sesion:
            indicativo, observaciones = obtener_climatologia(sesion, clave)
    except requests.HTTPError as error:
        # No imprimo la URL de la petición: puede incluir la clave.
        estado = (
            error.response.status_code if error.response is not None else "desconocido"
        )
        raise SystemExit(f"AEMET devolvió HTTP {estado}.") from None
    except requests.RequestException:
        raise SystemExit("No se pudo completar la conexión con AEMET.") from None
    except ValueError:
        raise SystemExit(
            "La respuesta de AEMET no coincide con el contrato esperado."
        ) from None

    print(
        json.dumps(
            {"indicativo": indicativo, "observaciones": observaciones},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
