import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_d = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("rentabilidad", os.path.join(_d, "rentabilidad.py"))
r = importlib.util.module_from_spec(s); s.loader.exec_module(r)


class T(unittest.TestCase):
    def test_tasa_real_exacta(self):
        self.assertAlmostEqual(r.tasa_real(0.06, 0.03), 1.06 / 1.03 - 1, places=12)
        self.assertLess(r.tasa_real(0.03, 0.04), 0)  # inflación mayor que la tasa: pierde poder de compra

    def test_anualizar_es_neutra_a_365_dias(self):
        self.assertAlmostEqual(r.anualizar(0.05, 365), 0.05, places=12)
        self.assertAlmostEqual(r.anualizar(0.005, 30), 1.005 ** (365 / 30) - 1, places=12)

    def test_ida_y_vuelta_uf(self):
        nom = r.tasa_dap_uf_a_nominal(0.02, 0.04)
        self.assertAlmostEqual(r.tasa_real(nom, 0.04), 0.02, places=12)

    def test_dias_invalidos(self):
        with self.assertRaises(ValueError):
            r.anualizar(0.01, 0)


if __name__ == "__main__":
    unittest.main()
