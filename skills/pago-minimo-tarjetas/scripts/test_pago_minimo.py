import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pago_minimo.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

from datetime import date

class T(unittest.TestCase):
    def test_etapa1_ejemplo_5pct_mf(self):
        r = m.pago_minimo(200_000, 0, 800_000, date(2026, 6, 10))
        self.assertEqual(r["pago_minimo"], 240_000)

    def test_etapa1_cuotas_sin_interes_solo_5pct(self):
        self.assertEqual(m.pago_minimo(0, 100_000, 0, date(2026, 6, 10))["pago_minimo"], 5_000)

    def test_etapa2_25pct(self):
        r = m.pago_minimo(0, 100_000, 0, date(2026, 12, 10))
        self.assertEqual(r["pago_minimo"], 28_750)
        self.assertEqual(r["estatus_de_la_fecha_del_calendario"], "norma")

    def test_100pct_en_2028(self):
        r = m.pago_minimo(0, 100_000, 0, date(2028, 6, 10))
        self.assertEqual(r["pago_minimo"], 100_000)
        self.assertEqual(r["estatus_de_la_fecha_del_calendario"], "norma")

    def test_antes_de_vigencia(self):
        with self.assertRaises(ValueError):
            m.pago_minimo(0, 1, 1, date(2026, 5, 1))

    def test_solo_minimo(self):
        r = m.solo_minimo(1_000_000, 0.025)
        self.assertEqual(r["primer_minimo"], 75_000)
        self.assertTrue(250 < r["meses_para_saldar"] < 300)
        self.assertAlmostEqual(r["intereses_total"] / 500_000, 1, delta=0.01)

    def test_proyeccion_alerta(self):
        r = m.proyectar([{"mes": "2026-12", "cuotas_sin_interes": 400_000, "otros_financiable": 0}], 10_000)
        self.assertTrue(r[0]["alerta_minimo_supera_flujo"])

if __name__ == "__main__":
    unittest.main()
