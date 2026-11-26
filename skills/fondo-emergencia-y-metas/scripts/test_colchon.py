import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "colchon.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

class T(unittest.TestCase):
    D = {"gastos_esenciales_mensuales": 1_000_000, "liquido": 1_500_000, "no_liquido": 500_000}

    def test_meses_cubiertos_y_faltante(self):
        r = m.evaluar(self.D)
        self.assertEqual(r["meses_cubiertos_liquido"], 1.5)
        self.assertEqual(r["meses_cubiertos_total_con_no_liquido"], 2.0)
        self.assertEqual(r["metas"]["3_meses"]["falta"], 1_500_000)
        self.assertFalse(r["bajo_el_piso"])

    def test_meses_con_aporte(self):
        self.assertEqual(m.evaluar(dict(self.D, aporte_mensual=500_000))["metas"]["3_meses"]["meses_para_alcanzar"], 3)

    def test_liberaciones(self):
        d = dict(self.D, liberaciones=[{"desde_mes": 2, "monto": 500_000}])
        self.assertEqual(m.evaluar(d)["metas"]["3_meses"]["meses_para_alcanzar"], 4)

    def test_sin_aporte_no_alcanza(self):
        self.assertIsNone(m.evaluar(self.D)["metas"]["6_meses"]["meses_para_alcanzar"])

    def test_ingreso_variable_sube_metas(self):
        r = m.evaluar(dict(self.D, ingreso_variable=True))
        self.assertIn("9_meses", r["metas"])
        self.assertNotIn("3_meses", r["metas"])

    def test_bajo_el_piso(self):
        self.assertTrue(m.evaluar(dict(self.D, liquido=500_000))["bajo_el_piso"])

    def test_gasto_invalido(self):
        with self.assertRaises(ValueError):
            m.evaluar(dict(self.D, gastos_esenciales_mensuales=0))

if __name__ == "__main__":
    unittest.main()
