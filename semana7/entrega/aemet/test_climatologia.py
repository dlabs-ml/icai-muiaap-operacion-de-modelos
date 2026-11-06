from unittest import TestCase
from unittest.mock import Mock

import requests
from climatologia import obtener_climatologia


class ClimatologiaTest(TestCase):
    def test_busca_indicativo_y_descarga_el_periodo_del_enunciado(self):
        sesion = Mock(spec=requests.Session)
        base = "https://opendata.aemet.es"
        datos = [
            {"estado": 200, "datos": f"{base}/datos/inventario"},
            [
                {"nombre": "OTRA", "indicativo": "0000"},
                {"nombre": "MADRID, CIUDAD UNIVERSITARIA", "indicativo": "DEMO"},
            ],
            {"estado": 200, "datos": f"{base}/datos/climatologia"},
            [{"fecha": "2019-10-01", "tmed": "15,6"}],
        ]
        respuestas = [Mock(**{"json.return_value": dato}) for dato in datos]
        sesion.get.side_effect = respuestas

        indicativo, filas = obtener_climatologia(sesion, "clave-ficticia")

        self.assertEqual(indicativo, "DEMO")
        self.assertEqual(filas[0]["fecha"], "2019-10-01")
        inventario, enlace1, diario, enlace2 = sesion.get.call_args_list
        self.assertTrue(inventario.args[0].endswith("/todasestaciones/"))
        self.assertTrue(
            diario.args[0].endswith(
                "/fechaini/2019-10-01T00:00:00UTC/fechafin/2019-10-30T23:59:59UTC/estacion/DEMO/"
            )
        )
        for peticion in (inventario, diario):
            self.assertEqual(peticion.kwargs["params"], {"api_key": "clave-ficticia"})
        for peticion in (enlace1, enlace2):
            self.assertNotIn("params", peticion.kwargs)
        for respuesta in respuestas:
            respuesta.raise_for_status.assert_called_once()

    def test_no_descarga_un_enlace_ajeno_a_aemet(self):
        sesion = Mock(spec=requests.Session)
        sesion.get.return_value.json.return_value = {
            "estado": 200,
            "datos": "https://opendata.aemet.es.example.org/datos",
        }
        with self.assertRaisesRegex(ValueError, "enlace"):
            obtener_climatologia(sesion, "clave-ficticia")
        sesion.get.assert_called_once()
