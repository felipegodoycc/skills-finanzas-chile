import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presupuesto.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

BASE = {"ingreso_mensual": 1_000_000, "fijos": {"arriendo": 400_000},
        "cuotas_pactadas": {"2026-12": 200_000, "2027-01": 100_000},
        "variable_actual": {"a": 400_000}, "metas": {"a": 300_000}, "meses_para_la_meta": 2}

class T(unittest.TestCase):
    def test_limites_bajan_gradualmente_y_brecha(self):
        r = m.planificar(BASE)
        dic, ene = r["transicion"]
        self.assertEqual(dic["limites_por_categoria"]["a"], 350_000)
        self.assertEqual(ene["limites_por_categoria"]["a"], 300_000)
        self.assertEqual(dic["brecha"], 50_000)
        self.assertEqual(r["colchon_requerido_para_cubrir_transicion"], 0)

    def test_regimen(self):
        r = m.planificar(BASE)["regimen_estable"]
        self.assertEqual(r["margen_para_variable"], 600_000)
        self.assertEqual(r["ahorro_posible"], 300_000)
        self.assertEqual(r["recorte_necesario"], 100_000)

    def test_colchon_si_hay_deficit(self):
        d = dict(BASE, ingreso_mensual=900_000)
        r = m.planificar(d)
        self.assertEqual(r["transicion"][0]["brecha"], -50_000)
        self.assertEqual(r["colchon_requerido_para_cubrir_transicion"], 50_000)

    def test_ingreso_invalido(self):
        with self.assertRaises(ValueError):
            m.planificar(dict(BASE, ingreso_mensual=0))

if __name__ == "__main__":
    unittest.main()
