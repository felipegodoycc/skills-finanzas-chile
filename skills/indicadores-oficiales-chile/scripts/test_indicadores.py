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


# HTML SIMULADO: fila de día con 12 meses y fila de mes.
SII_UF = "<table>" + "".join(
    "<tr><td>%d</td>%s</tr>" % (d, "".join("<td>%s</td>" % ("41.412,34" if (d, mm) == (26, 11) else "" if d == 27 else "39.000,00") for mm in range(1, 13)))
    for d in range(1, 32)) + "<tr><td>1</td><td>x</td><td>1,0</td><td>2</td><td>1,0</td><td>3</td></tr></table>"
SII_UTM = ("<table><tr><td>Octubre</td><td>72.100</td><td>865.200</td><td>110,00</td></tr>"
           "<tr><td>Noviembre</td><td>72.440</td><td>869.280</td><td>&nbsp;</td></tr></table>")


class T(unittest.TestCase):
    def test_sii_uf_utm_uta(self):
        self.assertEqual(m.leer("uf", SII_UF, "sii", "2026-11-26")["datos"][0]["valor"], 41412.34)
        self.assertEqual(m.leer("utm", SII_UTM, "sii", "2026-11")["datos"][0]["valor"], 72440.0)
        self.assertEqual(m.leer("uta", SII_UTM, "sii", "2026-11")["datos"][0]["valor"], 869280.0)

    def test_sii_sin_dato_o_formato_cambiado(self):
        with self.assertRaises(ValueError):   # día sin valor publicado
            m.leer("uf", SII_UF, "sii", "2026-11-27")
        with self.assertRaises(ValueError):   # IPC aún vacío
            m.leer("ipc", SII_UTM, "sii", "2026-11")
        with self.assertRaises(ValueError):   # página distinta
            m.leer("uf", "<p>nada</p>", "sii", "2026-11-26")
        with self.assertRaises(ValueError):
            m.leer("dolar", SII_UTM, "sii", "2026-11")

    def test_cmf_y_bcch(self):
        self.assertEqual(m.leer("uf", CMF, "cmf")["datos"], [{"fecha": "2026-11-26", "valor": 39123.45}])
        r = m.leer("uf", BCCH, "bcch")
        self.assertEqual(len(r["datos"]), 1)   # ignora la observación sin dato
        self.assertIn("Banco Central", r["fuente"])

    def test_numero(self):
        self.assertEqual(m.numero("20.939,49"), 20939.49)
        self.assertEqual(m.numero("0,3"), 0.3)
        self.assertEqual(m.numero("39123.45"), 39123.45)

    def test_fecha_invalida(self):
        with self.assertRaises(ValueError):
            m.leer("uf", SII_UF, "sii", "26-11-2026")

    def test_respuesta_inesperada(self):
        with self.assertRaises(ValueError):
            m.parse_cmf('{"Mensaje": "apikey invalida"}')
        with self.assertRaises(ValueError):
            m.parse_bcch('{"Codigo": -1, "Descripcion": "Usuario invalido"}')

    def test_cli_lee_archivo_y_no_usa_red(self):
        import tempfile, io, contextlib
        with open(_p, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("urllib", src)
        self.assertNotIn("socket", src)
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "utm2026.htm")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(SII_UTM)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(m.main(["--fuente", "sii", "--archivo", ruta, "utm", "--fecha", "2026-11"]), 0)
            self.assertEqual(json.loads(buf.getvalue())["datos"][0]["valor"], 72440.0)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(m.main(["--fuente", "sii", "--archivo", os.path.join(d, "no.htm"), "uf"]), 1)


    def test_interfaz_antigua_explica_el_cambio(self):
        import io, contextlib
        antiguas = (["uf"], ["uf", "--fecha", "2026-11-26"], ["--fuente", "auto", "uf"],
                    ["--fuente", "mindicador", "uf"], ["--fuente", "cmf", "utm", "--fecha", "2026-11"],
                    ["serie", "--codigo", "F073.UFF.PRE.Z.D", "--desde", "2026-11-01"])
        for args in antiguas:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(m.main(args), 2, args)
            self.assertIn("--archivo", err.getvalue(), args)

if __name__ == "__main__":
    unittest.main()
