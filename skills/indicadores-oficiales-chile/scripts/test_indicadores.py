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


class T(unittest.TestCase):
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
