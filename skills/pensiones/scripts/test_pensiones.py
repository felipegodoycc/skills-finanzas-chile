import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_d = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("pensiones", os.path.join(_d, "pensiones.py"))
p = importlib.util.module_from_spec(s); s.loader.exec_module(p)


class T(unittest.TestCase):
    def test_tope_es_2_5_uf(self):
        self.assertAlmostEqual(p.beneficio_anos_cotizados_bruto_uf(300), 2.5)
        self.assertAlmostEqual(p.beneficio_anos_cotizados_bruto_uf(600), 2.5)  # más de 300 meses no suma

    def test_proporcional_y_jornada(self):
        self.assertAlmostEqual(p.beneficio_anos_cotizados_bruto_uf(120), 1.0)
        self.assertAlmostEqual(p.beneficio_anos_cotizados_bruto_uf(120, 0.5), 0.5)
        self.assertAlmostEqual(p.beneficio_anos_cotizados_bruto_uf(6), 0.05)  # fracción de año proporcional

    def test_invalidos(self):
        with self.assertRaises(ValueError):
            p.beneficio_anos_cotizados_bruto_uf(-1)
        with self.assertRaises(ValueError):
            p.beneficio_anos_cotizados_bruto_uf(10, 1.5)

    def test_factor_compensacion(self):
        self.assertEqual(p.factor_compensacion(65), 1.0)
        self.assertEqual(p.factor_compensacion(63), 0.5)
        self.assertEqual(p.factor_compensacion(60), 0.05)
        self.assertEqual(p.factor_compensacion(59), 0.0)


if __name__ == "__main__":
    unittest.main()
