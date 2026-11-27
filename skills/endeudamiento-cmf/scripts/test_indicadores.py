import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_d = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("indicadores", os.path.join(_d, "indicadores.py"))
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)


class Pruebas(unittest.TestCase):
    def test_ejemplo_del_readme(self):
        r = m.indicadores(1_500_000, 300_000, 6_000_000)
        self.assertEqual(r["carga_financiera"], 0.2)
        self.assertEqual(r["apalancamiento_veces_ingreso"], 4.0)
        self.assertFalse(r["alta_carga_cmf"])

    def test_umbral_es_estrictamente_mayor_que_50(self):
        self.assertFalse(m.indicadores(1_000_000, 500_000, 0)["alta_carga_cmf"])
        self.assertTrue(m.indicadores(1_000_000, 500_001, 0)["alta_carga_cmf"])

    def test_ingreso_no_positivo(self):
        for ingreso in (0, -1):
            with self.assertRaises(ValueError):
                m.indicadores(ingreso, 100, 100)


if __name__ == "__main__":
    unittest.main()
