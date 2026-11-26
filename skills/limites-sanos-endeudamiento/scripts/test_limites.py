import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "limites.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

class T(unittest.TestCase):
    def test_interpolacion_en_nodo_y_entre_nodos(self):
        xs, ys = [1_000_000, 2_000_000], [0.22, 0.31]
        self.assertAlmostEqual(m.interpolar(1_000_000, xs, ys)[0], 0.22)
        self.assertAlmostEqual(m.interpolar(1_500_000, xs, ys)[0], 0.265)

    def test_sin_hipotecario_bandas(self):
        r = m.evaluar(1_000_000, 100_000)
        self.assertEqual(r["banda"], "holgado")
        self.assertEqual(m.evaluar(1_000_000, 300_000)["banda"], "sobre_el_umbral")

    def test_con_hipotecario_umbral_mayor(self):
        r = m.evaluar(1_000_000, 350_000, hipotecario=True)
        self.assertAlmostEqual(r["umbral_rci_cmf_dt"], 0.43)
        self.assertEqual(r["banda"], "cercano_al_umbral")

    def test_fuera_de_rango_y_rdi(self):
        r = m.evaluar(150_000, 10_000, deuda_sin_interes=100_000)
        self.assertTrue(r["ingreso_fuera_del_rango_del_estudio"])
        self.assertIn("rdi_sobre_umbral", r)

    def test_aviso_y_50pct(self):
        r = m.evaluar(1_000_000, 600_000, hipotecario=True)
        self.assertTrue(r["sobre_50pct_reporte_cmf"])
        self.assertIn("aviso", r)

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            m.evaluar(0, 1)

if __name__ == "__main__":
    unittest.main()
