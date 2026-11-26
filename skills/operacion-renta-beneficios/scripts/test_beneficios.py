import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_d = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("beneficios", os.path.join(_d, "beneficios.py"))
b = importlib.util.module_from_spec(s); s.loader.exec_module(b)
UTA = 1_000_000.0  # valor ficticio, solo para los tests


class T(unittest.TestCase):
    def test_hipotecario_bajo_90_uta_es_total_con_tope_8_uta(self):
        self.assertEqual(b.rebaja_intereses_hipotecarios(5 * UTA, 80, UTA), 5 * UTA)
        self.assertEqual(b.rebaja_intereses_hipotecarios(12 * UTA, 80, UTA), 8 * UTA)

    def test_hipotecario_sobre_150_uta_no_procede(self):
        self.assertEqual(b.rebaja_intereses_hipotecarios(5 * UTA, 150.1, UTA), 0.0)

    def test_hipotecario_tramo_intermedio_es_continuo_en_los_bordes(self):
        self.assertAlmostEqual(b.rebaja_intereses_hipotecarios(8 * UTA, 90, UTA) / (8 * UTA), 0.99970, places=4)
        self.assertAlmostEqual(b.rebaja_intereses_hipotecarios(8 * UTA, 150, UTA) / (8 * UTA), 0.0, places=3)
        self.assertAlmostEqual(b.rebaja_intereses_hipotecarios(8 * UTA, 120, UTA) / (8 * UTA), 0.4996, places=4)

    def test_credito_educacion(self):
        self.assertAlmostEqual(b.credito_educacion(2, 40_000, 700), 2 * 4.4 * 40_000)
        self.assertEqual(b.credito_educacion(2, 40_000, 793), 0.0)

    def test_gasto_presunto_con_tope(self):
        self.assertEqual(b.gasto_presunto(10 * UTA, UTA), 3 * UTA)
        self.assertEqual(b.gasto_presunto(100 * UTA, UTA), 15 * UTA)


if __name__ == "__main__":
    unittest.main()
