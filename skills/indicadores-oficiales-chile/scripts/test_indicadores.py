import importlib.util, json, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "indicadores.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

# Fixtures con la forma esperada (NO son respuestas reales: ver "LIMITES").
CMF = json.dumps({"UFs": [{"Valor": "39.123,45", "Fecha": "2026-11-26"}]})
BCCH = json.dumps({"Codigo": 0, "Descripcion": "Success",
                   "Series": {"Obs": [{"indexDateString": "26-11-2026", "value": "39123.45",
                                       "statusCode": "OK"},
                                      {"indexDateString": "27-11-2026", "value": "",
                                       "statusCode": "ND"}]}})


# HTML SIMULADO (no se pudo descargar el real): fila de día con 12 meses y fila de mes.
SII_UF = "<table>" + "".join(
    "<tr><td>%d</td>%s</tr>" % (d, "".join("<td>%s</td>" % ("41.412,34" if (d, mm) == (26, 11) else "" if d == 27 else "39.000,00") for mm in range(1, 13)))
    for d in range(1, 32)) + "<tr><td>1</td><td>x</td><td>1,0</td><td>2</td><td>1,0</td><td>3</td></tr></table>"
SII_UTM = ("<table><tr><td>Octubre</td><td>72.100</td><td>865.200</td><td>110,00</td></tr>"
           "<tr><td>Noviembre</td><td>72.440</td><td>869.280</td><td>&nbsp;</td></tr></table>")


class T(unittest.TestCase):
    def test_sii_uf_utm_uta(self):
        r = m.consultar("uf", "2026-11-26", "sii", env={}, fetch=lambda u: SII_UF)
        self.assertEqual(r["datos"][0]["valor"], 41412.34)
        r = m.consultar("utm", "2026-11", "sii", env={}, fetch=lambda u: SII_UTM)
        self.assertEqual(r["datos"][0]["valor"], 72440.0)
        r = m.consultar("uta", "2026-11", "sii", env={}, fetch=lambda u: SII_UTM)
        self.assertEqual(r["datos"][0]["valor"], 869280.0)

    def test_sii_sin_dato_o_formato_cambiado(self):
        with self.assertRaises(ValueError):   # día sin valor publicado
            m.consultar("uf", "2026-11-27", "sii", env={}, fetch=lambda u: SII_UF)
        with self.assertRaises(ValueError):   # IPC aún vacío
            m.consultar("ipc", "2026-11", "sii", env={}, fetch=lambda u: SII_UTM)
        with self.assertRaises(ValueError):   # página distinta
            m.consultar("uf", "2026-11-26", "sii", env={}, fetch=lambda u: "<p>nada</p>")

    def test_mindicador_marcado_como_terceros(self):
        j = json.dumps({"serie": [{"fecha": "2026-11-26T03:00:00.000Z", "valor": 41412.34}]})
        r = m.consultar("uf", "2026-11-26", "mindicador", env={}, fetch=lambda u: j)
        self.assertIn("TERCEROS", r["fuente"])
        self.assertEqual(r["datos"][0], {"fecha": "2026-11-26", "valor": 41412.34})

    def test_auto_no_elige_fuentes_no_oficiales(self):
        with self.assertRaises(RuntimeError) as e:
            m.consultar("uf", env={})
        self.assertIn("sii", str(e.exception))

    def test_cmf_no_ofrece_uta(self):
        with self.assertRaises(ValueError):
            m.consultar("uta", fuente="cmf", env={"CMF_API_KEY": "K"}, fetch=lambda u: CMF)

    def test_numero(self):
        self.assertEqual(m.numero("20.939,49"), 20939.49)
        self.assertEqual(m.numero("0,3"), 0.3)
        self.assertEqual(m.numero("39123.45"), 39123.45)

    def test_rutas_cmf(self):
        self.assertEqual(m.ruta_cmf("uf"), "uf")
        self.assertEqual(m.ruta_cmf("uf", "2026-11-26"), "uf/2026/11/dias/26")
        self.assertEqual(m.ruta_cmf("utm", "2026-11"), "utm/2026/11")
        with self.assertRaises(ValueError):
            m.ruta_cmf("uf", "26-11-2026")

    def test_cmf_parsea_y_no_filtra_la_clave(self):
        vistas = []
        r = m.consultar("uf", "2026-11-26", "cmf", env={"CMF_API_KEY": "SECRETA"},
                        fetch=lambda u: vistas.append(u) or CMF)
        self.assertEqual(r["datos"], [{"fecha": "2026-11-26", "valor": 39123.45}])
        self.assertIn("apikey=SECRETA", vistas[0])          # se envía...
        self.assertNotIn("SECRETA", json.dumps(r))          # ...pero no se devuelve

    def test_bcch_ignora_observaciones_sin_dato(self):
        r = m.consultar("uf", "2026-11-26", "bcch", env={"BCCH_API_TOKEN": "T"},
                        fetch=lambda u: BCCH)
        self.assertEqual(len(r["datos"]), 1)
        self.assertEqual(r["datos"][0]["valor"], 39123.45)
        self.assertNotIn("token=T", json.dumps(r))

    def test_auto_elige_segun_entorno(self):
        r = m.consultar("uf", fuente="auto", env={"BCCH_API_TOKEN": "T"}, fetch=lambda u: BCCH)
        self.assertIn("Banco Central", r["fuente"])

    def test_sin_clave_falla_claro(self):
        with self.assertRaises(RuntimeError):
            m.consultar("uf", env={})

    def test_respuesta_inesperada(self):
        with self.assertRaises(ValueError):
            m.parse_cmf('{"Mensaje": "apikey invalida"}')
        with self.assertRaises(ValueError):
            m.parse_bcch('{"Codigo": -1, "Descripcion": "Usuario invalido"}')

    def test_indicador_fuera_de_cmf(self):
        with self.assertRaises(ValueError):
            m.consultar("tmc", fuente="cmf", env={"CMF_API_KEY": "K"}, fetch=lambda u: CMF)


if __name__ == "__main__":
    unittest.main()
