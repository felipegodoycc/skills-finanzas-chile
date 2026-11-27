import datetime as dt, importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_d = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("check_tmc", os.path.join(_d, "check_tmc.py"))
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

# Datos ficticios, solo para los tests (la TMC real se lee de la CMF cada mes).
DATOS = {"vigencia_desde": "2026-11-01", "fuente": "ficticia",
         "tramos": [{"clave": "t", "tasa_anual_pct": 40.0}]}
HOY = dt.date(2026, 11, 15)


class Pruebas(unittest.TestCase):
    def test_no_excede(self):
        r = m.evaluar(DATOS, "t", 0.025, HOY)  # 30% nominal, 34,5% compuesta
        self.assertEqual(r["veredicto"], "NO EXCEDE")
        self.assertAlmostEqual(r["tasa_anual_nominal_x12"], 0.30)
        self.assertAlmostEqual(r["tasa_anual_compuesta"], round(1.025 ** 12 - 1, 5))

    def test_depende_de_la_base(self):
        r = m.evaluar(DATOS, "t", 0.03, HOY)  # 36% nominal, 42,6% compuesta
        self.assertEqual(r["excede_tmc"], {"nominal_x12": False, "compuesta": True})
        self.assertTrue(r["veredicto"].startswith("DEPENDE"))

    def test_excede(self):
        self.assertEqual(m.evaluar(DATOS, "t", 0.04, HOY)["veredicto"], "EXCEDE")

    def test_datos_desactualizados(self):
        self.assertFalse(m.evaluar(DATOS, "t", 0.02, dt.date(2026, 12, 16))["datos_desactualizados"])
        r = m.evaluar(DATOS, "t", 0.02, dt.date(2026, 12, 17))  # 46 días
        self.assertTrue(r["datos_desactualizados"])
        self.assertIsNotNone(r["aviso"])

    def test_tramo_inexistente(self):
        with self.assertRaises(KeyError):
            m.evaluar(DATOS, "otro", 0.02, HOY)


if __name__ == "__main__":
    unittest.main()
